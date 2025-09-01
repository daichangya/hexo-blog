---
title: 使用 ASM 实现 Java 语言的“多重继承”
id: 183
date: 2024-10-31 22:01:41
author: daichangya
excerpt: 问题的提出在大部分情况下，需要多重继承往往意味着糟糕的设计。但在处理一些遗留项目的时候，多重继承可能是我们能做出的选择中代价最小的。由于 Java
  语言本身不支持多重继承，这常常会给我们带来麻烦，最后的结果可能就是大量的重复代码。本文试图使用 ASM 框架来解决这一问题。在扩展类的功能的同时，不产生任何重复代码。考虑如下的实际情况：有一组类，名为
  SubClass1、SubClas
permalink: /archives/shi-yong-ASM-shi-xian-Java-yu-yan-de/
tags:
- aop
---

## 问题的提出

在大部分情况下，需要多重继承往往意味着糟糕的设计。但在处理一些遗留项目的时候，多重继承可能是我们能做出的选择中代价最小的。由于 Java 语言本身不支持多重继承，这常常会给我们带来麻烦，最后的结果可能就是大量的重复代码。本文试图使用 ASM 框架来解决这一问题。在扩展类的功能的同时，不产生任何重复代码。

考虑如下的实际情况：有一组类，名为 SubClass1、SubClass2、SubClass3 和 SubClass4，它们共同继承了同一个父类 SuperClass。现在，我们需要这组类中的一部分，例如 SubClass1 和 SubClass2，这两个类还要实现另外两个接口，它们分别为：IFibonacciComputer 和 ITimeRetriever。然而，这两个接口已经有了各自的实现类 FibonacciComputer 和 TimeRetriever。并且这两个类的实现逻辑就是我们想要的，我们不想做任何改动，只希望在 SubClass1 和 SubClass2 两个类中包含这些实现逻辑。

它们的结构如图 1 所示：

##### 图 1\. 结构类图

![图 1. 结构类图](https://www.ibm.com/developerworks/cn/java/j-lo-asm/image003.jpg)


由于 SubClass1,SubClass2 已经继承了 SuperClass，所以我们无法让它们再继承 FibonacciComputer 或 TimeRetriever。

所以，想要它们再实现 IFibonacciComputer 和 ITimeRetriever 这两个接口，必然会产生重复代码。

下面，我们就使用 ASM 来解决这个问题。

## Java class 文件格式以及类加载器介绍

在后面的内容中，需要对 Java class 文件格式以及类加载器的知识有一定的了解，所以这里先对这些内容做一个简单介绍：

### class 文件格式

Java class 文件的结构如图 2 所示（图中“*”表示出现 0 次或任意多次）：

##### 图 2.Java class 文件结构

![图 2.Java class 文件结构](https://www.ibm.com/developerworks/cn/java/j-lo-asm/image005.jpg)


详细说明如下：

*   **Magic Number**: 每个 class 文件的前 4 个字节被称为“魔数”，它的内容为：0xCAFEBABE。魔数的作用在于可以轻松地分辨出一个文件是不是 class 文件。
*   **Version**: 该项指明该 class 文件的版本号。
*   **Constant Pool**: 常量池是 class 文件中结构最为复杂，也最为重要的部分。常量池包含了与文件中类和接口相关的常量。常量池中存储了诸如文字字符串，final 变量值。Java 虚拟机把常量池组织为入口列表的形式。常量池中许多入口都指向其他的常量入口，而且 class 文件中紧随着常量池的许多条目也都会指向常量池的入口。除了字面常量之外，常量池还可以容纳以下几种符号引用：类和接口的全限定名，字段的名称和描述符和方法的名称和描述符等。
*   **Modifiers**: 该项指明该文件中定义的是类还是接口，以及声明中用了哪种修饰符，类或接口是私有的，还是公共的，类的类型是否是 final 的，等等。
*   **This class**: 该项是对常量池的索引。在这个位置，Java 虚拟机能够找到一个容纳了类或接口全限定名的入口。这里需要注意的是：在 class 文件中，所有类的全限定名都是以内部名称形式表示的。内部名称是将原先类全限定名中的“.”替换为“/”。例如：java.lang.String 的内部名称为 java/lang/String。
*   **Super Class**: 该项也是对常量池的索引，指明了该类超类的内部名称。
*   **Interfaces**: 该项指明了由该类直接实现或由接口扩展的父接口的信息。

**注**：Modifiers,This Class,Super Class 和 Interfaces 这四项的和就是一个类的声明部分。

*   **Annotation**: 该项存储的是注解相关的内容，注解可能是关于类的，方法的以及字段的。
*   **Attribute**: 该项用来存储关于类，字段以及方法的附加信息。在 Java 5 引入了注解之后，该部分内容几乎已经没有用处。
*   **Field**: 该项用来存储类的字段信息。

*   **Method**: 该项用来存储类的方法信息。

### 类装载器介绍

类装载器负责查找并装载类。每个类在被使用之前，都必须先通过类装载器装载到 Java 虚拟机当中。Java 虚拟机有两种类装载器 :

*   **启动类装载器**
    
    启动类装载器是 Java 虚拟机实现的一部分，每个 Java 虚拟机都必须有一个启动类装载器，它知道怎么装载受信任的类，比如 Java API 的 class 文件。
    
*   **用户自定义装载器**
    
    用户自定义装载器是普通的 Java 对象，它的类必须派生自 java.lang.ClassLoader 类。ClassLoader 类中定义的方法为程序提供了访问类装载机制的接口。
    

## ASM 简介以及编程模型

### ASM 简介

ASM 是一个可以用来生成\\转换和分析 Java 字节码的代码库。其他类似的工具还有 [cglib](http://cglib.sourceforge.net/)、[serp](https://www.ibm.com/developerworks/cn/java/j-lo-asm/serp.sourceforge.net)和 [BCEL](http://commons.apache.org/bcel/)等。相较于这些工具，ASM 有以下的优点 :

*   ASM 具有简单、设计良好的 API，这些 API 易于使用。
*   ASM 有非常良好的开发文档，以及可以帮助简化开发的 Eclipse 插件
*   ASM 支持 Java 6
*   ASM 很小、很快、很健壮
*   ASM 有很大的用户群，可以帮助新手解决开发过程中遇到的问题
*   ASM 的开源许可可以让你几乎以任何方式使用它

### 编程模型

ASM 提供了两种编程模型：

*   Core API，提供了基于事件形式的编程模型。该模型不需要一次性将整个类的结构读取到内存中，因此这种方式更快，需要更少的内存。但这种编程方式难度较大。
*   Tree API，提供了基于树形的编程模型。该模型需要一次性将一个类的完整结构全部读取到内存当中，所以这种方法需要更多的内存。这种编程方式较简单。

下文中，我们将只使用 Core API，因此我们只介绍与其相关的类。

Core API 中操纵字节码的功能基于 ClassVisitor 接口。这个接口中的每个方法对应了 class 文件中的每一项。Class 文件中的简单项的访问使用一个单独的方法，方法参数描述了这个项的内容。而那些具有任意长度和复杂度的项，使用另外一类方法，这类方法会返回一个辅助的 Visitor 接口，通过这些辅助接口的对象来完成具体内容的访问。例如 visitField 方法和 visitMethod 方法，分别返回 FieldVisitor 和 MethodVisitor 接口的对象。

清单 1 为 ClassVisitor 中的方法列表：

##### 清单 1.ClassVisitor 接口中的方法

```
public interface ClassVisitor {
  // 访问类的声明部分
   void visit(int version, int access, String name, String
signature,String superName, String[] interfaces);
  // 访问类的代码
   void visitSource(String source, String debug);
  // 访问类的外部类
   void visitOuterClass(String owner, String name, String desc);
  // 访问类的注解
   AnnotationVisitor visitAnnotation(String desc, boolean visible);
  // 访问类的属性
   void visitAttribute(Attribute attr);
  // 访问类的内部类
   void visitInnerClass(String name, String outerName,
String innerName,int access);
  // 访问类的字段
   FieldVisitor visitField(int access, String name, String desc,
String signature, Object value);
  // 访问类的方法
   MethodVisitor visitMethod(int access, String name,
String desc,String signature, String[] exceptions);
  // 访问结束
   void visitEnd();
}
```

ClassVisitor 接口中的方法在被调用的时候是有严格顺序的，其顺序如清单 2 所示（其中“？”表示被调用 0 次或 1 次。“*”表示被调用 0 次或任意多次）：

##### 清单 2.ClassVisitor 中方法调用的顺序

```
visit
visitSource?
visitOuterClass?
( visitAnnotation| visitAttribute)*
( visitInnerClass| visitField| visitMethod)*
visitEnd
```

这就是说，visit 方法必须最先被调用，然后是最多调用一次 visitSource 方法，然后是最多调用一次 visitOuterClass 方法。然后是 visitAnnotation 和 visitAttribute 方法以任意顺序被调用任意多次。再然后是以任任意顺序调用 visitInnerClass ,visitField 或 visitMethod 方法任意多次。最终，调用一次 visitEnd 方法。

ASM 提供了三个基于 ClassVisitor 接口的类来实现 class 文件的生成和转换：

*   **ClassReader**：ClassReader 解析一个类的 class 字节码，该类的 accept 方法接受一个 ClassVisitor 的对象，在 accept 方法中，会按上文描述的顺序逐个调用 ClassVisitor 对象的方法。它可以被看做事件的生产者。
*   **ClassAdapter**：ClassAdapter 是 ClassVisitor 的实现类。它的构造方法中需要一个 ClassVisitor 对象，并保存为字段 protected ClassVisitor cv。在它的实现中，每个方法都是原封不动的直接调用 cv 的对应方法，并传递同样的参数。可以通过继承 ClassAdapter 并修改其中的部分方法达到过滤的作用。它可以看做是事件的过滤器。
*   **ClassWriter**：ClassWriter 也是 ClassVisitor 的实现类。ClassWriter 可以用来以二进制的方式创建一个类的字节码。对于 ClassWriter 的每个方法的调用会创建类的相应部分。例如：调用 visit 方法就是创建一个类的声明部分，每调用一次 visitMethod 方法就会在这个类中创建一个新的方法。在调用 visitEnd 方法后即表明该类的创建已经完成。它最终生成一个字节数组，这个字节数组中包含了一个类的 class 文件的完整字节码内容 。可以通过 toByteArray 方法获取生成的字节数组。ClassWriter 可以看做事件的消费者。

通常情况下，它们是组合起来使用的。

下面举一个简单的例子：假设现在需要对 class 文件的版本号进行修改，将其改为 Java 1.5。操作方法如下：

1.  首先通过 ClassReader 读取这个类；
2.  然后创建一个 ClassAdapter 的子类 ChangeVersionAdapter。在 ChangeVersionAdapter 中，覆盖 visit 方法，在调用 ClassVisitor#visit 方法时修改其中关于版本号的参数。该方法的签名如下：visit(int version, int access, String name, String signature, String superName, String\[\] interfaces)，其中每个参数的含义如下：
    1.  version：class 文件的版本号，这就是我们需要修改的内容；
    2.  access：该类的访问级别；
    3.  name：该类的内部名称；
    4.  signature：该类的签名，如果该类与泛型无关，这个参数就是 null;
    5.  superName：父类的内部名称；
    6.  interfaces：该类实现的接口的内部名称；

明白这些参数的含义之后，修改就很容易，只需要在调用 cv.visit 的时候，将 version 参数指定为 Opcodes.V1_5 即可（Opcodes 是 ASM 中的一个类），其他参数不加修改原样传递。这样，经过该 ClassAdapter 过滤后的类的版本号就都是 Java 1.5 了。

1.  在创建 ChangeVersionAdapter 对象时，构造方法传递一个 ClassWriter 的对象。该 ClassWriter 会随着 ChangeVersionAdapter 方法的调用按顺序创建出类的每一个部分。由于在 visit 方法中，version 参数已经被过滤为 Opcodes.V1_5，所以该 ClassWriter 最终产生的 class 字节码的版本号就是 V1.5 的；
2.  然后通过 ClassWriter#toByteArray 方法获取修改后的类的完整的字节码内容；
3.  当然，想要使用这个类，还需要通过一个自定义类加载器，将获得到的字节码加载到虚拟机当中，才可以创建这个类的实例；

代码片段如清单 3 所示：

##### 清单 3\. 使用 ASM 的代码示例

```
…
 // 使用 ChangeVersionAdapter 修改 class 文件的版本
 ClassReader cr = new ClassReader(className);
 ClasssWriter cw = new ClassWriter(0);
 // ChangeVersionAdapter 类是我们自定义用来修改 class 文件版本号的类
 ClassAdapter ca = new ChangeVersionAdapter (cw);
 cr.accept(ca, 0);
 byte[] b2 = cw.toByteArray();
…
```

图 3 是相应的 Sequence 图：

##### 图 3\. 修改版本号的 Sequence 图

![图 3. 修改版本号的 Sequence 图](https://www.ibm.com/developerworks/cn/java/j-lo-asm/image006.png)


### 代码示例

在了解了以上的知识之后再回到我们刚开始提出的问题中，我们希望 SubClass1 和 SubClass2 在继承自 SuperClass 的同时还要实现 IFibonacciComputer 以及 ITimeRetriever 两个接口。

为了后文描述方便，这里先确定三个名词：

*   **实现类**即完成了接口实现的类，这里为 FibonacciComputer 以及 TimeRetriever。
*   **待增强类**即需要实现功能增强，加入实现逻辑的类，这里为 SubClass1 和 SubClass2。
*   **增强类**即在待增强类的基础上，加入了接口实现的类。这个类目前没有实际的类与之对应。

如果只能在源代码级别进行修改，我们能做的仅仅是将实现类的代码拷贝进待增强类。（当然，有稍微好一点的做法在每一个待增强类中包含一个实现类，以组合的方式实现接口。但这仍然不能避免多个待增强类中的代码重复。）

在学习了 ASM 之后，我们可以直接从字节码的层次来进行修改。回忆一下上文中的内容：使用 ClassWrite 可以直接创建类的字节码，不同的方法创建了 class 文件的不同部分，尤其重要的是以下几个方法：

*   visit 方法创建一个类的声明部分
*   visitField 方法创建一个类的字段
*   visitMethod 方法创建一个类的方法
*   visitEnd 方法，表明该类已经创建完成

所以，现在我们可以直接从字节码的层次完成这一需求：**动态的创建一个新的类（即增强类）继承自待增强类，同时在该类中，将实现类的实现方法****添加****进来**。

完整的实现逻辑如下：

1.  创建一个 ClassAdapter 的子类 AddImplementClassAdapter，这个类将被用来访问待增强类。AddImplementClassAdapter 期待一个 ClassWriter 作为 ClassVisitor。该 ClassWriter 在访问待增强类的同时逐步完成增强类的创建。
2.  在 AddImplementClassAdapter 中覆盖 visitEnd 方法，在调用 ClassVisitor#visitEnd 方法之前，使用该 ClassVisitor 逐个访问每一个实现类。由于实现类中的内容也需要进行一定的过滤，所以这里的 ClassVisitor 在访问实现类的时候也需要经过一个 ClassAdapter 进行过滤。创建另一个 ClassAdapter 的子类 ImplementClassAdapter 来完成这个过滤。由于这个 ClassVisitor 是一个 ClassWriter。这样做的效果就是将实现类的内容添加到增强类中。
3.  在完成了所有实现类的访问之后，调用 ClassVisitor#visitEnd 方法表明增强类已经创建完成。
4.  使用一个 ClassReader 的对象读取待增强类。
5.  创建一个 AddImplementClassAdapter 的实例，同时提供一个 ClassWriter 作为 ClassVisitor。
6.  通过 accept 方法将前面创建的 AddImplementClassAdapter 对象传递给这个 ClassReader 对象。
7.  在访问完待增强类之后，ClassWriter 即完成了增强类的创建，所以最后通过 toByteArray 方法获取这个增强类的字节码。
8.  最后通过一个自定义类加载器将其加载到虚拟机当中。

下面是代码示例与讲解：

首先需要修改 SubClass1 以及 SubClass2 两个类，使其声明实现 IFibonacciComputer 和 ITimeRetriever 这两个接口。由于这两个类并没有真正的包含实现接口的代码，所以它们现在必须标记为抽象类。修改后的类结构如图 4 所示：

##### 图 4\. 修改后的类图

![图 4. 修改后的类图](https://www.ibm.com/developerworks/cn/java/j-lo-asm/image008.jpg)


然后创建以下几个类：

*   **AddImplementClassAdapter**: 过滤待增强类，并引导 ClassWriter 创建增强类的适配器。
*   **ImplementClassAdapter**: 实现类的适配器，过滤多余内容，将实现类中的内容通过 ClassWriter 添加到增强类中。
*   **ModifyInitMethodAdapter**: 修改待增强类构造方法的适配器。
*   **SimpleClassLoader**: 自定义类加载器，用来加载动态生成的增强类。
*   **EnhanceFactory**: 提供对外接口，方便使用。
*   **EnhanceException**: 对异常的统一包装，方便异常处理。

下面，我们来逐一实现这些类：

**AddImplementClassAdapter**： 首先在构造方法中，我们需要记录下待增强类的 Class 对象，增强类的类名，实现类的 Class 对象，以及一个 ClassWriter 对象，该构造方法代码如清单 4 所示：

##### 清单 4.AddImpelementClassAdapter 构造方法代码

```
public AddImplementClassAdapter( ClassWriter writer,
String enhancedClassName,Class<?> targetClass,
Class<?>... implementClasses) {
   super(writer);
   this.classWriter = writer;
   this.implementClasses = implementClasses;
   this.originalClassName = targetClass.getName();
   this.enhancedClassName = enhancedClassName;
}
```

在 visit 方法中需要完成增强类声明部分的创建，增强类继承自待增强类。该方法代码如清单 6 所示：

##### 清单 5.visit 方法代码

```
// 通过 visit 方法完成增强类的声明部分           
 public void visit(int version, int access, String name,
 String signature,String superName, String[] interfaces) {
      cv.visit(version, Opcodes.ACC_PUBLIC,
     // 将 Java 代码中类的名称替换为虚拟机中使用的形式
      enhancedClassName.replace('.', '/'),
      signature, name,interfaces);
 }
```

visitMethod 方法中需要对构造方法做单独处理，因为 class 文件中的构造方法与源代码中的构造方法有三点不一样的地方：

1.  每个 class 文件中至少有一个构造方法。即便你在类的源代码中没有编写构造方法，编译器也会为你生成一个默认构造方法 ;
2.  在 class 文件中与源代码中的构造方法名称不一样，class 文件的构造方法名称都为“<init>”;
3.  class 文件中每个构造方法都会最先调用一次父类的构造方法。

鉴于这些原因，增强类的构造方法需要在待增强类构造方法的基础上进行修改。修改的内容就是对于父构造方法的调用，因为增强类和待增强类的父类是不一样的。

visitMethod 方法中需要判断如果是构造方法就通过 ModifyInitMethodAdapter 修改构造方法。其他方法直接返回 null 丢弃（因为增强类已经从待增强类中继承了这些方法，所以这些方法不需要在增强类中再出现一遍），该方法代码如清单 7 所示：

##### 清单 6.visitMethod 方法代码

```
public MethodVisitor visitMethod(int access, String name,
String desc,String signature, String[] exceptions) {
   if (INTERNAL_INIT_METHOD_NAME.equals(name)) {
      // 通过 ModifyInitMethodAdapter 修改构造方法
       MethodVisitor mv = classWriter.visitMethod(access,
       INTERNAL_INIT_METHOD_NAME, desc, signature, exceptions);
       return new ModifyInitMethodAdapter(mv, originalClassName);
   }
   return null;
}
```

最后，在 visitEnd 方法，使用 ImplementClassAdapter 与 ClassWriter 将实现类的内容添加到增强类中，最后再调用 visitEnd 方法表明增强类已经创建完成：

##### 清单 7.visitEnd 方法代码

```
public void visitEnd() {
for (Class<?> clazz : implementClasses) {
   try {
     // 逐个将实现类的内容添加到增强类中。
     ClassReader reader = new ClassReader(clazz.getName());
     ClassAdapter adapter =
     new ImplementClassAdapter(classWriter);
     reader.accept(adapter, 0);
   } catch (IOException e) {
       e.printStackTrace();
   }
}
cv.visitEnd();
}
```

**ImplementClassAdapter**：该类对实现类进行过滤。

首先在 visit 方法中给于空实现将类的声明部分过滤掉，代码如清单 8 所示：

##### 清单 8.visit 方法代码

```
public void visit(int version, int access, String name,
String signature,String superName, String[] interfaces) {
   // 空实现，将该部分内容过滤掉
}
```

然后在 visitMethod 中，将构造方法过滤掉，对于其他方法，调用 ClassVisitor#visitMethod 进行访问。由于这里的 ClassVisitor 是一个 ClassWriter，这就相当于在增强类中创建了该方法，代码如清单 9 所示：

##### 清单 9.visitMethod 方法代码

```
public MethodVisitor visitMethod(int access, String name,
String desc,String signature, String[] exceptions) {
   // 过滤掉实现类中的构造方法
   if (AddImplementClassAdapter.INTERNAL_INIT_METHOD_NAME.equals(name)){
       return null;
   }
   // 其他方法原样保留
   return cv.visitMethod(access, name, desc, signature, exceptions);
}
```

**ModifyInitMethodAdapter**：上文中已经提到，ModifyInitMethodAdapter 是用来对增强类的构造方法进行修改的。MethodAdapter 中的 visitMethodInsn 是对方法调用指令的访问。该方法的参数含义如下：

*   opcode 为调用方法的 JVM 指令，
*   owner 为被调用方法的类名，
*   name 为方法名，
*   desc 为方法描述。

所以，我们需要将对于待增强类父类构造方法的调用改为对于待增强类构造方法的调用（因为增强类的父类就是待增强类），其代码如清单 10 所示：

##### 清单 10\. ModifyInitMethodAdapter 类代码

```
     /**
        专门用来修改构造方法的方法适配器
     */
public class ModifyInitMethodAdapter extends MethodAdapter {
private String className;
public ModifyInitMethodAdapter(MethodVisitor mv, String name) {
   super(mv);
   this.className = name;
}
public void visitMethodInsn(int opcode, String owner,
String name,String desc) {
   // 将 Java 代码中的类全限定名替换为虚拟机中使用的形式
   if (name.equals(AddImplementClassAdapter.INTERNAL_INIT_METHOD_NAME)) {
   mv.visitMethodInsn(opcode, className.replace(".", "/"),
   name, desc);
}
}
}
```

**SimpleClassLoader**：该自定义类装载器通过提供一个 defineClass 方法来装载动态生成的增强类。方法的实现是直接调用父类的 defineClass 方法，其代码如清单 11 所示：

##### 清单 11\. SimpleClassLoader 类代码

```
public class SimpleClassLoader extends ClassLoader {
public Class<?> defineClass(String className, byte[] byteCodes) {
       // 直接通过父类的 defineClass 方法加载类的结构
   return super.defineClass(className, byteCodes,
   0, byteCodes.length);
}
}
```

**EnhanceException**：这是一个异常包装类，其中包含了待增强类和实现类的信息，其逻辑很简单，代码如清单 12 所示：

##### 清单 12\. EnhanceException 类代码

```
/**
 异常类
*/
 public class EnhanceException extends Exception {
 private Class<?> enhanceClass;
 private Class<?> [] implementClasses;
 // 异常类构造方法
 public EnhanceException(Exception ex,Class<?> ec,Class<?>... imClazz){
    super(ex);
    this.enhanceClass = ec;
    this.implementClasses = imClazz;
 }
 public Class<?> getEnhanceClass() {
    return enhanceClass;
 }
 public Class<?>[] getImplementClasses() {
    return implementClasses;
 }
 }
```

**EnhanceFactory：**最后，通过 EnhanceFactory 提供对外调用接口，调用接口有两个：

*   `public static <T> Class<T> addImplementation(``Class<T> clazz,Class<?>... implementClasses)`
*   `public static <T> T newInstance(Class<T> clazz,``Class<?>... impls)`

为了方便使用，这两个方法都使用了泛型。它们的参数是一样的：第一个参数都是待增强类的 Class 对象，后面是任意多个实现类的 Class 对象，返回的类型和待增强类一致，用户在获取返回值之后不需要进行任何类型转换即可使用。

第一个方法创建出增强类的 Class 对象，并通过自定义类加载器加载，其代码如清单 13 所示：

##### 清单 13\. addImplementation 方法代码

```
/**
静态工具方法，在待增强类中加入实现类的内容，返回增强类。
*/
 public static <T> Class<T> addImplementation(Class<T> clazz,
 Class<?>... implementClasses) throws EnhanceException {
    String enhancedClassName = clazz.getName() + ENHANCED;
    try {
       // 尝试加载增强类
        return  (Class<T>) classLoader.loadClass(enhancedClassName);
        }
       // 如果没有找到增强类，则尝试直接在内存中构建出增强类的结构
    catch (ClassNotFoundException classNotFoundException) {
        ClassReader reader = null;
        try {
            reader = new ClassReader(clazz.getName());
        } catch (IOException ioexception) {
            throw new EnhanceException(ioexception,
            clazz, implementClasses);
        }
        ClassWriter writer = new ClassWriter(0);
       // 通过 AddImplementClassAdapter 完成实现类内容的织入
        ClassVisitor visitor = new AddImplementClassAdapter(
        enhancedClassName, clazz, writer, implementClasses);
        reader.accept(visitor, 0);
        byte[] byteCodes = writer.toByteArray();
        Class<T> result = (Class<T>) classLoader.defineClass(
        enhancedClassName, byteCodes);
        return result;
    }
 }
```

第二个方法先调用前一个方法，获取 `增强类`的 `Class`对象，然后使用反射创建实例，其代码如清单 14 所示：

##### 清单 14\. newInstance 方法代码

```
/**
通过待增强类和实现类，得到增强类的实例对象
*/
 public static <T> T newInstance(Class<T> clazz, Class<?>... impls)
 throws EnhanceException {
 Class<T> c = addImplementation(clazz, impls);
 if (c == null) {
    return null;
 }
 try {
       // 通过反射创建实例
    return c.newInstance();
 } catch (InstantiationException e) {
    throw new EnhanceException(e, clazz, impls);
 } catch (IllegalAccessException e) {
    throw new EnhanceException(e, clazz, impls);
 }
 }
```

下面是测试代码，先通过 EnhanceFactory 创建增强类的实例，然后就可以像普通对象一样的使用，代码如清单 15 所示：

##### 清单 15\. 使用演示代码

```
// 不用 new 关键字，而使用 EnhanceFactory.newInstance 创建增强类的实例
SubClass1 obj1 = EnhanceFactory.newInstance(SubClass1.class,
TimeRetriever.class,FibonacciComputer.class);
// 调用待增强类中的方法
obj1.methodInSuperClass();
obj1.methodDefinedInSubClass1();
// 调用实现类中的方法
System.out.println("The Fibonacci number of 10 is "+obj1.compute(10));
System.out.println("Now is :"+obj1.tellMeTheTime());
System.out.println("--------------------------------------");
// 对于 SubClass2 的增强类实例的创建也是一样的
SubClass2 obj2 = EnhanceFactory.newInstance(SubClass2.class,
TimeRetriever.class,FibonacciComputer.class);
// 调用待增强类中的方法
obj2.methodInSuperClass();
obj2.methodDefinedInSubClass2();
// 调用实现类中的方法
System.out.println("The Fibonacci number of 10 is "+obj1.compute(10));
System.out.println("Now is :"+obj1.tellMeTheTime());
```

这里，我们演示了使用 ASM 创建一个新的类，并且修改该类中的内容的方法。而这一切都是在运行的环境中动态生成的，这一点相较于源代码级别的实现有以下的好处：

*   **没有重复代码** 这是我们的主要目的，由于增强类是在运行的环境中生成的，并且动态的包含了实现类中的内容，所以，不会产生任何重复代码。
*   **灵活性** 使用 EnhanceFactory# addImplementation 方法，对于接口的实现完全是在运行时确定的，因此可以灵活的选择。
*   **可复用性** EnhanceFactory# addImplementation 是一个可以完全复用的方法，我们可以在任何需要的地方使用它。

需要注意的是，这里我们并没有真正的实现“多重继承”，由于 class 文件格式的限制，我们也不可能真正实现“多重继承”，我们只是在一个类中包含了多个实现类的内容而已。但是，如果你使用增强类的实例通过 instanceof 之类的方法来判断它是否是实现类的实例的时候，你会得到 false，因为增强类并没有真正的继承自实现类。

另外，为了让演示代码足够的简单，对于这个功能的实现还存在一些问题，例如：

*   FibonacciComputer 和 TimeRetriever 这两个类中，可能会包含一些其他方法，这些方法并非是为了实现接口的方法，而这些方法也会被增强类所包含。
*   如果多个实现类与待增强类中包含了同样签名的方法时，在创建增强类的过程中会产生异常，因为一个类中不能包含同样方法签名的两个方法。
*   如果实现类中包含了一些字段，并且实现类的构造方法中初始化了这些字段。但增强类中的这些字段并没有被初始化。因为实现类的构造方法被忽略了。
*   无法对同一个类做多次不同类型的增强。

不过，在理解了上文中的知识之后，这些问题也都是可以解决的。

作为一个可以操作字节码的工具而言，ASM 的功能远不止于此。它还可以用来实现 AOP，实现性能监测，方法调用统计等功能。通过 Google，可以很容易的找到这类文章。

示例代码包含在 ASM_Demo.zip 中，该文件中包含了上文中提到的所有代码。

该 zip 文件为 eclipse 项目的归档文件。可以通过 Eclipse 菜单导入至 Eclipse 中，导入方法：File -> Import … -> Existing Projects into Workspace, 然后选择该 zip 文件即可。

想要编译该项目，还需要 ASM 框架的 jar 包。请在以下地址下载 ASM 框架：[http://forge.ow2.org/projects/asm/](http://forge.ow2.org/projects/asm/)

目前该框架正式版的版本号为：3.3.1。

下载该框架归档文件后解压缩， 并通过 eclipse 将 asm-all-3.3.1.jar（可能是其他版本号）添加到项目编译的类路径中即可。

代码中包含的 Main 类，是一个包含了 main 方法的可执行类，在 eclipse 中运行该类即可看到运行结果。

* * *

#### 下载资源

*   [示例代码](http://www.ibm.com/developerworks/apps/download/index.jsp?contentid=779297&filename=ASM_Demo.zip&method=http&locale=zh_CN) (ASM_Demo.zip | 9KB)

* * *

#### 相关主题

*   [ASM 框架官方主页](http://asm.ow2.org/)：ASM 是一个通用的 Java 字节码操纵和分析框架。它能够用来修改已有 class 文件或直接以二进制的形式生成 class 文件。
*   [ASM 指南](http://download.forge.objectweb.org/asm/asm-guide.pdf)：深入介绍了 ASM 3.0，从基础特性到例如字节码分析的深入话题。
*   [The Java Virtual Machine Specification](http://java.sun.com/docs/books/jvms/second_edition/html/VMSpecTOC.doc.html)：Java 虚拟机规范，Sun 公司官方文档。
*   [深入 Java 虚拟机（第 2 版）](http://product.china-pub.com/14719)：作者以易于理解的方式深入揭示了 Java 虚拟机的内部工作原理，Java 开发工程师必备读物。
*   [Bytecode Outline](http://andrei.gmxhome.de/bytecode/links.html)：Eclipse 插件，简化使用 ASM 开发的有力工具。
*   [developerWorks Java 技术专区](http://www.ibm.com/developerworks/cn/java/)：这里有数百篇关于 Java 编程各个方面的文章。
