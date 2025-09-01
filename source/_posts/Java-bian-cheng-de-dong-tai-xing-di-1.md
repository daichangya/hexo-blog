---
title: Java 编程的动态性，第 1 部分:类和类装入
id: 105
date: 2024-10-31 22:01:40
author: daichangya
excerpt: 本文是这个新系列文章的第一篇，该系列文章将讨论我称之为 *Java 编程的动态性* 的一系列主题。这些主题的范围从 Java 二进制类文件格式的基本结构，以及使用反射进行运行时元数据访问，一直到在运行时修改和构造新类。贯穿整篇文章的公共线索是这样一种思想：在
  Java 平台上编程要比使用直接编译成本机代码的语言更具动态性。如果您理解了这些动态方面，就可以使用 Java 编程完成那些在任何其它主流编程语言中不能完成的事情。
permalink: /archives/Java-bian-cheng-de-dong-tai-xing-di-1/
categories:
- jvm
---


### 系列内容：
*   第 1 部分: 类和类装入
*   [第3部分: 应用反射](http://www.ibm.com/developerworks/cn/java/j-dyn0715/index.html?ca=drs-)
*   [第 5 部分: 动态转换类](http://www.ibm.com/developerworks/cn/java/j-dyn0203/index.html?ca=drs-)
*   [第 6 部分: 利用 Javassist 进行面向方面的更改](http://www.ibm.com/developerworks/cn/java/j-dyn0302/index.html?ca=drs-)
*   [第 7 部分: 用 BCEL 设计字节码](http://www.ibm.com/developerworks/cn/java/j-dyn0414/index.html?ca=drs-)
*   [第 8 部分: 用代码生成取代反射](http://www.ibm.com/developerworks/cn/java/j-dyn0610/index.html?ca=drs-)

本文是这个新系列文章的第一篇，该系列文章将讨论我称之为 *Java 编程的动态性* 的一系列主题。这些主题的范围从 Java 二进制类文件格式的基本结构，以及使用反射进行运行时元数据访问，一直到在运行时修改和构造新类。贯穿整篇文章的公共线索是这样一种思想：在 Java 平台上编程要比使用直接编译成本机代码的语言更具动态性。如果您理解了这些动态方面，就可以使用 Java 编程完成那些在任何其它主流编程语言中不能完成的事情。

本文中，我将讨论一些基本概念，它们是这些 Java 平台动态特性的基础。这些概念的核心是用于表示 Java 类的二进制格式，包括这些类装入到 JVM 时所发生的情况。本文不仅是本系列其余几篇文章的基础，而且还演示了开发人员在使用 Java 平台时碰到的一些非常实际的问题。

## 用二进制表示的类

使用 Java 语言的开发人员在用编译器编译他们的源代码时，通常不必关心对这些源代码做了些什么这样的细节。但是本系列文章中，我将讨论从源代码到执行程序所涉及的许多幕后细节，因此我将首先探讨由编译器生成的二进制类。

二进制类格式实际上是由 JVM 规范定义的。通常这些类表示是由编译器从 Java 语言源代码生成的，而且它们通常存储在扩展名为 `.class` 的文件中。但是，这些特性都无关紧要。已经开发了可以使用 Java 二进制类格式的其它一些编程语言，而且出于某些目的，还构建了新的类表示，并被立即装入到运行中的 JVM。就 JVM 而言，重要的部分不是源代码以及如何存储源代码，而是格式本身。

那么这个类格式实际看上去是什么样呢？清单 1 提供了一个（非常）简短的类的源代码，还附带了由编译器输出的类文件的部分十六进制显示：

##### 清单 1\. Hello.java 的源代码和（部分）二进制类文件

```
public class Hello
{
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
0000: cafe babe 0000 002e 001a 0a00 0600 0c09  ................
0010: 000d 000e 0800 0f0a 0010 0011 0700 1207  ................
0020: 0013 0100 063c 696e 6974 3e01 0003 2829  .....<init>...()
0030: 5601 0004 436f 6465 0100 046d 6169 6e01  V...Code...main.
0040: 0016 285b 4c6a 6176 612f 6c61 6e67 2f53  ..([Ljava/lang/S
0050: 7472 696e 673b 2956 0c00 0700 0807 0014  tring;)V........
0060: 0c00 1500 1601 000d 4865 6c6c 6f2c 2057  ........Hello, W
0070: 6f72 6c64 2107 0017 0c00 1800 1901 0005  orld!...........
0080: 4865 6c6c 6f01 0010 6a61 7661 2f6c 616e  Hello...java/lan
0090: 672f 4f62 6a65 6374 0100 106a 6176 612f  g/Object...java/
00a0: 6c61 6e67 2f53 7973 7465 6d01 0003 6f75  lang/System...ou
...
```

### 二进制类文件的内幕

清单 1 显示的二进制类表示中首先是“cafe babe”特征符，它标识 Java 二进制类格式（并顺便作为一个永久的 ― 但在很大程度上未被认识到的 ― 礼物送给努力工作的 *barista*，他们本着开发人员所具备的精神构建 Java 平台）。这个特征符恰好是一种验证一个数据块 *确实*声明成 Java 类格式的一个实例的简单方法。任何 Java 二进制类（甚至是文件系统中没有出现的类）都需要以这四个字节作为开始。

该数据的其余部分不太吸引人。该特征符之后是一对类格式版本号（本例中，是由 1.4.1 javac 生成的次版本 0 和主版本 46 ― 用十六进制表示就是 0x2e），接着是常量池中项的总数。项总数（本例中，是 26，或 0x001a）后面是实际的常量池数据。这里放着类定义所用的所有常量。它包括类名和方法名、特征符以及字符串（您可以在十六进制转储右侧的文本解释中识别它们），还有各种二进制值。

常量池中各项的长度是可变的，每项的第一个字节标识项的类型以及对它解码的方式。这里我不详细探究所有这些内容的细节，如果感兴趣，有许多可用的的参考资料，从实际的 JVM 规范开始。关键之处在于常量池包含对该类所用的其它类和方法的所有引用，还包含了该类及其方法的实际定义。常量池往往占到二进制类大小的一半或更多，但平均下来可能要少一些。

常量池后面还有几项，它们引用了类本身、其超类以及接口的常量池项。这些项后面是有关字段和方法的信息，它们本身用复杂结构表示。方法的可执行代码以包含在方法定义中的 *代码属性*的形式出现。用 JVM 的指令形式表示该代码，一般称为 *字节码*，这是下一节要讨论的主题之一。

在 Java 类格式中， *属性*被用于几个已定义的用途，包括已提到的字节码、字段的常量值、异常处理以及调试信息。但是属性并非只可能用于这些用途。从一开始，JVM 规范就已经要求 JVM 忽略未知类型的属性。这一要求所带来的灵活性使得将来可以扩展属性的用法以满足其它用途，例如提供使用用户类的框架所需的元信息，这种方法在 Java 派生的 C# 语言中已广泛使用。遗憾的是，对于在用户级利用这一灵活性还没有提供任何挂钩。

## 字节码和堆栈

构成类文件可执行部分的字节码实际上是针对特定类型的计算机 ― JVM ― 的机器码。它被称为 *虚拟*机，因为它被设计成用软件来实现，而不是用硬件来实现。每个用于运行 Java 平台应用程序的 JVM 都是围绕该机器的实现而被构建的。

这个虚拟机实际上相当简单。它使用堆栈体系结构，这意味着在使用指令操作数之前要先将它们装入内部堆栈。指令集包含所有的常规算术和逻辑运算，以及条件转移和无条件转移、装入／存储、调用／返回、堆栈操作和几种特殊类型的指令。有些指令包含立即操作数值，它们被直接编码到指令中。其它指令直接引用常量池中的值。

尽管虚拟机很简单，但实现却并非如此。早期的（第一代）JVM 基本上是虚拟机字节码的解释器。这些虚拟机实际上 *的确*相对简单，但存在严重的性能问题 ― 解释代码的时间总是会比执行本机代码的时间长。为了减少这些性能问题，第二代 JVM 添加了 *即时*（just-in-time，JIT）转换。在第一次执行 Java 字节码之前，JIT 技术将它编译成本机代码，从而对于重复执行提供了更好的性能。当代 JVM 的性能甚至还要好得多，因为使用了适应性技术来监控程序的执行并有选择地优化频繁使用的代码。

## 装入类

诸如 C 和 C++ 这些编译成本机代码的语言通常在编译完源代码之后需要链接这个步骤。这一链接过程将来自独立编译好的各个源文件的代码和共享库代码合并起来，从而形成了一个可执行程序。Java 语言就不同。使用 Java 语言，由编译器生成的类在被装入到 JVM 之前通常保持原状。即使从类文件构建 JAR 文件也不会改变这一点 ― JAR 只是类文件的容器。

链接类不是一个独立步骤，它是在 JVM 将这些类装入到内存时所执行作业的一部分。在最初装入类时这一步会增加一些开销，但也为 Java 应用程序提供了高度灵活性。例如，在编写应用程序以使用接口时，可以到运行时才指定其实际实现。这个用于组装应用程序的 *后联编*方法广泛用于 Java 平台，servlet 就是一个常见示例。

JVM 规范中详细描述了装入类的规则。其基本原则是只在需要时才装入类（或者至少看上去是这样装入 ― JVM 在实际装入时有一些灵活性，但必须保持固定的类初始化顺序）。每个装入的类都可能拥有其它所依赖的类，所以装入过程是递归的。清单 2 中的类显示了这一递归装入的工作方式。 `Demo` 类包含一个简单的 `main` 方法，它创建了 `Greeter` 的实例，并调用 `greet` 方法。 `Greeter` 构造函数创建了 `Message` 的实例，随后会在 `greet` 方法调用中使用它。

##### 清单 2\. 类装入演示的源代码

```
public class Demo
{
    public static void main(String[] args) {
        System.out.println("**beginning execution**");
        Greeter greeter = new Greeter();
        System.out.println("**created Greeter**");
        greeter.greet();
    }
}
public class Greeter
{
    private static Message s_message = new Message("Hello, World!");
     
    public void greet() {
        s_message.print(System.out);
    }
}
public class Message
{
    private String m_text;
     
    public Message(String text) {
        m_text = text;
    }
     
    public void print(java.io.PrintStream ps) {
        ps.println(m_text);
    }
}
```

在 `java` 命令行上设置参数 `-verbose:class` 会打印类装入过程的跟踪记录。清单 3 显示了使用这一参数运行清单 2 程序的部分输出：

##### 清单 3\. -verbose:class 的部分输出

```
[Opened /usr/java/j2sdk1.4.1/jre/lib/rt.jar]
[Opened /usr/java/j2sdk1.4.1/jre/lib/sunrsasign.jar]
[Opened /usr/java/j2sdk1.4.1/jre/lib/jsse.jar]
[Opened /usr/java/j2sdk1.4.1/jre/lib/jce.jar]
[Opened /usr/java/j2sdk1.4.1/jre/lib/charsets.jar]
[Loaded java.lang.Object from /usr/java/j2sdk1.4.1/jre/lib/rt.jar]
[Loaded java.io.Serializable from /usr/java/j2sdk1.4.1/jre/lib/rt.jar]
[Loaded java.lang.Comparable from /usr/java/j2sdk1.4.1/jre/lib/rt.jar]
[Loaded java.lang.CharSequence from /usr/java/j2sdk1.4.1/jre/lib/rt.jar]
[Loaded java.lang.String from /usr/java/j2sdk1.4.1/jre/lib/rt.jar]
...
[Loaded java.security.Principal from /usr/java/j2sdk1.4.1/jre/lib/rt.jar]
[Loaded java.security.cert.Certificate
  from /usr/java/j2sdk1.4.1/jre/lib/rt.jar]
[Loaded Demo]
**beginning execution**
[Loaded Greeter]
[Loaded Message]
**created Greeter**
Hello, World!
[Loaded java.util.HashMap$KeySet
  from /usr/java/j2sdk1.4.1/jre/lib/rt.jar]
[Loaded java.util.HashMap$KeyIterator
  from /usr/java/j2sdk1.4.1/jre/lib/rt.jar]
```

这只列出了输出中最重要的部分 ― 完整的跟踪记录由 294 行组成，我删除了其中大部分，形成了这个清单。最初的一组类装入（本例中是 279 个）都是在尝试装入 `Demo` 类时触发的。这些类是每个 Java 程序（不管有多小）都要使用的核心类。即使删除 `Demo main` 方法的所有代码也不会影响这个初始的装入顺序。但是不同版本的类库所涉及的类数量和名称都不同。

在上面这个清单中，装入 `Demo` 类之后的部分更有趣。这里的顺序显示了只有在准备创建 `Greeter` 类的实例时才会装入该类。不过， `Greeter` 类使用了 `Message` 类的静态实例，所以在可以创建 `Greeter` 类的实例之前，还必须先装入 `Message` 类。

在装入并初始化类时，JVM 内部会完成许多操作，包括解码二进制类格式、检查与其它类的兼容性、验证字节码操作的顺序以及最终构造 `java.lang.Class` 实例来表示新类。这个 `Class` 对象成了 JVM 创建新类的所有实例的基础。它还是已装入类本身的标识 ― 对于装入到 JVM 的同一个二进制类，可以有多个副本，每个副本都有其自己的 `Class` 实例。即使这些副本都共享同一个类名，但对 JVM 而言它们都是独立的类。

### 非常规（类）路径

装入到 JVM 的类是由 *类装入器*控制的。JVM 中构建了一个 *引导程序*类装入器，它负责装入基本的 Java 类库类。这个特殊的类装入器有一些专门的特性。首先，它只装入在引导类路径上找到的类。因为这些是可信的系统类，所以引导程序装入器跳过了对常规（不可信）类所做的大量验证。

引导程序不是唯一的类装入器。对于初学者而言，JVM 为装入标准 Java 扩展 API 中的类定义了一个 *扩展*类装入器，并为装入一般类路径上的类（包括应用程序类）定义了一个 *系统*类装入器。应用程序还可以定义它们自己的用于特殊用途（例如运行时类的重新装入）的类装入器。这样添加的类装入器派生自 `java.lang.ClassLoader` 类（可能是间接派生的），该类对从字节数组构建内部类表示（ `java.lang.Class` 实例）提供了核心支持。每个构造好的类在某种意义上是由装入它的类装入器所“拥有”。类装入器通常保留它们所装入类的映射，从而当再次请求某个类时，能通过名称找到该类。

每个类装入器还保留对父类装入器的引用，这样就定义了类装入器树，树根为引导程序装入器。在需要某个特定类的实例（由名称来标识）时，无论哪个类装入器最初处理该请求，在尝试直接装入该类之前，一般都会先检查其父类装入器。如果存在多层类装入器，那么会递归执行这一步，所以这意味着通常不仅在装入该类的类装入器中该类是 *可见*的，而且对于所有后代类装入器也都是可见的。这还意味着如果一条链上有多个类装入器可以装入某个类，那么该树最上端的那个类装入器会是实际装入该类的类装入器。

在许多环境中，Java 程序会使用多个应用程序类装入器。J2EE 框架就是一个示例。该框架装入的每个 J2EE 应用程序都需要拥有一个独立的类装入器以防止一个应用程序中的类干扰其它应用程序。该框架代码本身也将使用一个或多个其它类装入器，同样用来防止对应用程序产生的或来自应用程序的干扰。整个类装入器集合形成了树状结构的层次结构，在其每个层次上都可装入不同类型的类。

### 装入器树

作为类装入器层次结构的实际示例，图 1 显示了 Tomcat servlet 引擎定义的类装入器层次结构。这里 Common 类装入器从 Tomcat 安装的某个特定目录的 JAR 文件进行装入，旨在用于在服务器和所有 Web 应用程序之间共享代码。Catalina 装入器用于装入 Tomcat 自己的类，而 Shared 装入器用于装入 Web 应用程序之间共享的类。最后，每个 Web 应用程序有自己的装入器用于其私有类。

##### 图 1\. Tomcat 类装入器

![Tomcat 类装入器](https://www.ibm.com/developerworks/cn/java/j-dyn0429/images/tomcat-loaders.gif)

在这种环境中，跟踪合适的装入器以用于请求新类会很混乱。为此，在 Java 2 平台中将 `setContextClassLoader` 方法和 `getContextClassLoader` 方法添加到了 `java.lang.Thread` 类中。这些方法允许该框架设置类装入器，使得在运行每个应用程序中的代码时可以将类装入器用于该应用程序。

能装入独立的类集合这一灵活性是 Java 平台的一个重要特性。尽管这个特性很有用，但是它在某些情况中会产生混淆。一个令人混淆的方面是处理 JVM 类路径这样的老问题。例如，在图 1 显示的 Tomcat 类装入器层次结构中，由 Common 类装入器装入的类决不能（根据名称）直接访问由 Web 应用程序装入的类。使这些类联系在一起的唯一方法是通过使用这两个类集都可见的接口。在这个例子中，就是包含由 Java servlet 实现的 `javax.servlet.Servlet` 。

无论何种原因在类装入器之间移动代码时都会出现问题。例如，当 J2SE 1.4 将用于 XML 处理的 JAXP API 移到标准分发版中时，在许多环境中都产生了问题，因为这些环境中的应用程序以前是依赖于装入它们自己选择的 XML API 实现的。使用 J2SE 1.3，只要在用户类路径中包含合适的 JAR 文件就可以解决该问题。在 J2SE 1.4 中，这些 API 的标准版现在位于扩展的类路径中，所以它们通常将覆盖用户类路径中出现的任何实现。

使用多个类装入器还可能引起其它类型的混淆。图 2 显示了 *类身份危机（class identity crisis）*的示例，它是在两个独立类装入器都装入一个接口及其相关的实现时产生的危机。即使接口和类的名称和二进制实现都相同，但是来自一个装入器的类的实例不能被认为是实现了来自另一个装入器的接口。图 2 中通过将接口类 `I` 移至 System 类装入器的空间就可以解除这种混淆。类 `A` 仍然有两个独立的实例，但它们都实现了同一个接口 `I` 。

##### 图 2\. 类身份危机

![类身份危机](https://www.ibm.com/developerworks/cn/java/j-dyn0429/images/identity-crisis.gif)



## 结束语

Java 类定义和 JVM 规范一起为运行时组装代码定义了功能极其强大的框架。通过使用类装入器，Java 应用程序能使用多个版本的类，否则这些类就会引起冲突。类装入器的灵活性甚至允许动态地重新装入已修改的代码，同时应用程序继续执行。

这里，Java 平台灵活性在某种程度上是以启动应用程序时较高的开销作为代价的。在 JVM 可以开始执行甚至最简单的应用程序代码之前，它都必须装入数百个独立的类。相对于频繁使用的小程序，这个启动成本通常使 Java 平台更适合于长时间运行的服务器类型的应用程序。服务器应用程序还最大程度地受益于代码在运行时进行组装这种灵活性，所以对于这种开发，Java 平台正日益受宠也就不足为奇了。

在本系列文章的第 2 部分中，我将介绍使用 Java 平台动态基础的另一个方面：反射 API（Reflection API）。反射使执行代码能够访问内部类信息。这可能是构建灵活代码的极佳工具，可以不使用类之间任何源代码链接就能够在运行时将代码挂接在一起。但象使用大多数工具一样，您必须知道何时及如何使用它以获得最大利益。请阅读 *Java 编程的动态性*第 2 部分以了解有效反射的诀窍和利弊。

* * *

#### 相关主题

*   您可以参阅本文在 developerWorks 全球站点上的 [英文原文](http://www.ibm.com/developerworks/library/j-dyn0429/index.html?S_TACT=105AGX52&S_CMP=cn-a-j).
*   直接到 [*The Java Virtual Machine Specification*](http://java.sun.com/docs/books/vmspec/)的出处，以了解二进制类格式、类的装入以及实际的 Java 字节码等细节。
*   Martyn Honeyford 广受欢迎的“ [衡量 Java 本机编译](https://www.ibm.com/developerworks/cn/java/j-native/index.html)”一文（ *developerWorks*，2002 年 1 月）提供了有关 Java 语言本机代码编译问题及利弊的更多详细信息。
*   二进制类格式包含大量重要的信息，通常这些信息甚至足够让您重新构造源代码（注释除外）。在 Greg Travis 的“ [How to lock down your Java code (or open up someone else's)](http://www.ibm.com/developerworks/java/library/j-obfus/?S_TACT=105AGX52&S_CMP=cn-a-j)”一文（ *developerWorks*，2001 年 5 月）中，他向您显示了可以如何使用这些信息。
*   获取有关 [Jikes Research Virtual Machine (RVM)](http://www.ibm.com/developerworks/oss/jikesrvm/?S_TACT=105AGX52&S_CMP=cn-a-j)的细节，它是用 Java 语言实现的，并是自我托管的（即，它的 Java 代码是依靠自身运行的，不需要另一个虚拟机）。
*   通过 Java 规范请求 175（Java Specification Request 175，JSR 175）的 [A Metadata Facility for the Java Programming Language](http://www.jcp.org/en/jsr/detail?id=175)，紧跟使属性可用于 Java 开发人员的发展。
*   了解 Apache Software Foundation 的 [Apache Tomcat](http://jakarta.apache.org/tomcat/index.html)Java 语言 Web 服务器项目的细节，包括 [Tomcat 类装入器用法](http://jakarta.apache.org/tomcat/tomcat-4.1-doc/class-loader-howto.html)的细节。
