---
title: Java深度历险（二）——Java类的加载、链接和初始化
id: 518
date: 2024-10-31 22:01:44
author: daichangya
excerpt: 在上一篇文章中介绍了Java字节代码的操纵，其中提到了利用Java类加载器来加载修改过后的字节代码并在JVM上执行。本文接着上一篇的话题，讨论Java类的加载、链接和初始化。Java字节代码的表现形式是字节数组（byte[]），而Java类在JVM中的表现形式是java.lang.Class类的对象。一个Java类从字节代码到能够在JVM中被使用，需要经过加载、链接和初始化这三个步骤。这三个步骤中
permalink: /archives/Java-shen-du-li-xian-er-Java-lei-de-jia/
categories:
- java
---


在[上一篇文章](https://blog.jsdiff.com/archives/cf-java-byte-code)中介绍了Java 字节代码的操纵，其中提到了利用Java 类加载器来加载修改过后的字节代码并在JVM 上执行。本文接着上一篇的话题，讨论Java 类的加载、链接和初始化。Java 字节代码的表现形式是字节数组（byte[]），而Java 类在JVM 中的表现形式是 [java.lang.Class](http://download.oracle.com/javase/1.5.0/docs/api/java/lang/Class.html) 类的对象。一个 Java 类从字节代码到能够在 JVM 中被使用，需要经过加载、链接和初始化这三个步骤。这三个步骤中，对开发人员直接可见的是 Java 类的加载，通过使用 Java 类加载器（class loader）可以在运行时刻动态的加载一个 Java 类；而链接和初始化则是在使用 Java 类之前会发生的动作。本文会详细介绍 Java 类的加载、链接和初始化的过程。

## Java 类的加载

Java 类的加载是由类加载器来完成的。一般来说，类加载器分成两类：启动类加载器（bootstrap）和用户自定义的类加载器（user-defined）。两者的区别在于启动类加载器是由 JVM 的原生代码实现的，而用户自定义的类加载器都继承自 Java 中的 [java.lang.ClassLoader](http://download.oracle.com/javase/1.5.0/docs/api/java/lang/ClassLoader.html) 类。在用户自定义类加载器的部分，一般 JVM 都会提供一些基本实现。应用程序的开发人员也可以根据需要编写自己的类加载器。JVM 中最常使用的是系统类加载器（system），它用来启动 Java 应用程序的加载。通过 java.lang.ClassLoader 的 [getSystemClassLoader()](http://download.oracle.com/javase/1.5.0/docs/api/java/lang/ClassLoader.html#getSystemClassLoader%28%29) 方法可以获取到该类加载器对象。

类加载器需要完成的最终功能是定义一个 Java 类，即把 Java 字节代码转换成 JVM 中的 java.lang.Class 类的对象。但是类加载的过程并不是这么简单。Java 类加载器有两个比较重要的特征：层次组织结构和代理模式。层次组织结构指的是每个类加载器都有一个父类加载器，通过 [getParent()](http://download.oracle.com/javase/1.5.0/docs/api/java/lang/ClassLoader.html#getParent%28%29) 方法可以获取到。类加载器通过这种父亲 \- 后代的方式组织在一起，形成树状层次结构。代理模式则指的是一个类加载器既可以自己完成 Java 类的定义工作，也可以代理给其它的类加载器来完成。由于代理模式的存在，启动一个类的加载过程的类加载器和最终定义这个类的类加载器可能并不是一个。前者称为初始类加载器，而后者称为定义类加载器。两者的关联在于：一个 Java 类的定义类加载器是该类所导入的其它 Java 类的初始类加载器。比如类 A 通过 import 导入了类 B，那么由类 A 的定义类加载器负责启动类 B 的加载过程。

一般的类加载器在尝试自己去加载某个 Java 类之前，会首先代理给其父类加载器。当父类加载器找不到的时候，才会尝试自己加载。这个逻辑是封装在 java.lang.ClassLoader 类的 [loadClass()](http://download.oracle.com/javase/1.5.0/docs/api/java/lang/ClassLoader.html#loadClass%28java.lang.String%29) 方法中的。一般来说，父类优先的策略就足够好了。在某些情况下，可能需要采取相反的策略，即先尝试自己加载，找不到的时候再代理给父类加载器。这种做法在 Java 的 Web 容器中比较常见，也是 [Servlet 规范](http://jcp.org/aboutJava/communityprocess/mrel/jsr154/index2.html)推荐的做法。比如， [Apache Tomcat](http://tomcat.apache.org/tomcat-5.5-doc/class-loader-howto.html) 为每个 Web 应用都提供一个独立的类加载器，使用的就是自己优先加载的策略。 [IBM WebSphere Application Server](http://www.redbooks.ibm.com/redpapers/pdfs/redp4581.pdf) 则允许 Web 应用选择类加载器使用的策略。

类加载器的一个重要用途是在 JVM 中为相同名称的 Java 类创建隔离空间。在 JVM 中，判断两个类是否相同，不仅是根据该类的[二进制名称](http://java.sun.com/docs/books/jls/third_edition/html/binaryComp.html#44909)，还需要根据两个类的定义类加载器。只有两者完全一样，才认为两个类的是相同的。因此，即便是同样的Java 字节代码，被两个不同的类加载器定义之后，所得到的Java 类也是不同的。如果试图在两个类的对象之间进行赋值操作，会抛出 [java.lang.ClassCastException](http://download.oracle.com/javase/1.5.0/docs/api/java/lang/ClassCastException.html) 。这个特性为同样名称的 Java 类在 JVM 中共存创造了条件。在实际的应用中，可能会要求同一名称的 Java 类的不同版本在 JVM 中可以同时存在。通过类加载器就可以满足这种需求。这种技术在 [OSGi](http://www.osgi.org/Main/HomePage) 中得到了广泛的应用。

## Java 类的链接

Java 类的链接指的是将 Java 类的二进制代码合并到 JVM 的运行状态之中的过程。在链接之前，这个类必须被成功加载。类的链接包括验证、准备和解析等几个步骤。验证是用来确保 Java 类的二进制表示在结构上是完全正确的。如果验证过程出现错误的话，会抛出 [java.lang.VerifyError](http://download.oracle.com/javase/1.5.0/docs/api/java/lang/VerifyError.html) 错误。准备过程则是创建 Java 类中的静态域，并将这些域的值设为默认值。准备过程并不会执行代码。在一个 Java 类中会包含对其它类或接口的形式引用，包括它的父类、所实现的接口、方法的形式参数和返回值的 Java 类等。解析的过程就是确保这些被引用的类能被正确的找到。解析的过程可能会导致其它的 Java 类被加载。

不同的 JVM 实现可能选择不同的解析策略。一种做法是在链接的时候，就递归的把所有依赖的形式引用都进行解析。而另外的做法则可能是只在一个形式引用真正需要的时候才进行解析。也就是说如果一个 Java 类只是被引用了，但是并没有被真正用到，那么这个类有可能就不会被解析。考虑下面的代码：


	public class LinkTest {   
	   public static void main(String[] args) {       
	      ToBeLinked toBeLinked = null;       
	      System.out.println("Test link.");   
	   }
	}

类 LinkTest 引用了类 ToBeLinked，但是并没有真正使用它，只是声明了一个变量，并没有创建该类的实例或是访问其中的静态域。在 Oracle 的 JDK 6 中，如果把编译好的 ToBeLinked 的 Java 字节代码删除之后，再运行 LinkTest，程序不会抛出错误。这是因为 ToBeLinked 类没有被真正用到，而 Oracle 的 JDK 6 所采用的链接策略使得 ToBeLinked 类不会被加载，因此也不会发现 ToBeLinked 的 Java 字节代码实际上是不存在的。如果把代码改成 ToBeLinked toBeLinked = new ToBeLinked(); 之后，再按照相同的方法运行，就会抛出异常了。因为这个时候 ToBeLinked 这个类被真正使用到了，会需要加载这个类。

## Java 类的初始化

当一个 Java 类第一次被真正使用到的时候，JVM 会进行该类的初始化操作。初始化过程的主要操作是执行静态代码块和初始化静态域。在一个类被初始化之前，它的直接父类也需要被初始化。但是，一个接口的初始化，不会引起其父接口的初始化。在初始化的时候，会按照源代码中从上到下的顺序依次执行静态代码块和初始化静态域。考虑下面的代码：


	public class StaticTest {   
	   public static int X = 10;   
	   public static void main(String[] args) {       
	      System.out.println(Y); // 输出 60   
	   }   
	   static {       
	      X = 30;   
	   }  
	   public static int Y = X * 2;
	}

在上面的代码中，在初始化的时候，静态域的初始化和静态代码块的执行会从上到下依次执行。因此变量 X 的值首先初始化成 10，后来又被赋值成 30；而变量 Y 的值则被初始化成 60。

Java 类和接口的初始化只有在特定的时机才会发生，这些时机包括：

*   创建一个 Java 类的实例。如
    
    
    MyClass obj = new MyClass()
    
*   调用一个 Java 类中的静态方法。如
    
    
    MyClass.sayHello()
    
*   给 Java 类或接口中声明的静态域赋值。如
    
    
    MyClass.value = 10
    
*   访问 Java 类或接口中声明的静态域，并且该域不是常值变量。如
    
    
    int value = MyClass.value
    
*   在顶层 Java 类中执行 assert 语句。

通过 Java 反射 API 也可能造成类和接口的初始化。需要注意的是，当访问一个 Java 类或接口中的静态域的时候，只有真正声明这个域的类或接口才会被初始化。考虑下面的代码：


	class B {   
	   static int value = 100;   
	   static {       
	      System.out.println("Class B is initialized."); // 输出   
	   }
	}
	class A extends B {   
	   static {       
	      System.out.println("Class A is initialized."); // 不会输出   
	   }
	}
	public class InitTest {   
	   public static void main(String[] args) {       
	      System.out.println(A.value); // 输出 100   
	   }
	}

在上述代码中，类 InitTest 通过 A.value 引用了类 B 中声明的静态域 value。由于 value 是在类 B 中声明的，只有类 B 会被初始化，而类 A 则不会被初始化。

## 创建自己的类加载器

在 Java 应用开发过程中，可能会需要创建应用自己的类加载器。典型的场景包括实现特定的 Java 字节代码查找方式、对字节代码进行加密 / 解密以及实现同名 Java 类的隔离等。创建自己的类加载器并不是一件复杂的事情，只需要继承自 java.lang.ClassLoader 类并覆写对应的方法即可。 java.lang.ClassLoader 中提供的方法有不少，下面介绍几个创建类加载器时需要考虑的：

*   [defineClass()](http://download.oracle.com/javase/1.5.0/docs/api/java/lang/ClassLoader.html#defineClass%28java.lang.String,%20byte%5B%5D,%20int,%20int%29) ：这个方法用来完成从 Java 字节代码的字节数组到 java.lang.Class 的转换。这个方法是不能被覆写的，一般是用原生代码来实现的。
*   [findLoadedClass()](http://download.oracle.com/javase/1.5.0/docs/api/java/lang/ClassLoader.html#findLoadedClass%28java.lang.String%29) ：这个方法用来根据名称查找已经加载过的 Java 类。一个类加载器不会重复加载同一名称的类。
*   [findClass()](http://download.oracle.com/javase/1.5.0/docs/api/java/lang/ClassLoader.html#findClass%28java.lang.String%29) ：这个方法用来根据名称查找并加载 Java 类。
*   [loadClass()](http://download.oracle.com/javase/1.5.0/docs/api/java/lang/ClassLoader.html#loadClass%28java.lang.String%29) ：这个方法用来根据名称加载 Java 类。
*   [resolveClass()](http://download.oracle.com/javase/1.5.0/docs/api/java/lang/ClassLoader.html#resolveClass%28java.lang.Class%29) ：这个方法用来链接一个 Java 类。

这里比较 容易混淆的是 findClass() 方法和 loadClass() 方法的作用。前面提到过，在 Java 类的链接过程中，会需要对 Java 类进行解析，而解析可能会导致当前 Java 类所引用的其它 Java 类被加载。在这个时候，JVM 就是通过调用当前类的定义类加载器的 loadClass() 方法来加载其它类的。findClass() 方法则是应用创建的类加载器的扩展点。应用自己的类加载器应该覆写 findClass() 方法来添加自定义的类加载逻辑。 loadClass() 方法的默认实现会负责调用 findClass() 方法。

前面提到，类加载器的代理模式默认使用的是父类优先的策略。这个策略的实现是封装在 loadClass() 方法中的。如果希望修改此策略，就需要覆写 loadClass() 方法。

下面的代码给出了自定义的类加载的常见实现模式：


	public class MyClassLoader extends ClassLoader {   
	   protected Class<?> findClass(String name) throws ClassNotFoundException {       
	      byte[] b = null; // 查找或生成 Java 类的字节代码       
		  return defineClass(name, b, 0, b.length);   
	   }
	}

## 参考资料

*   Java 语言规范（第三版）- 第十三章：[执行](http://java.sun.com/docs/books/jls/third_edition/html/execution.html)
*   JVM 规范（第二版） - 第五章：[加载、链接和初始化](http://java.sun.com/docs/books/jvms/second_edition/html/ConstantPool.doc.html)
*   [深入探讨Java 类加载器](http://www.ibm.com/developerworks/cn/java/j-lo-classloader/index.html)

