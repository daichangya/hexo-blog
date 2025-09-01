---
title: 继承关系的类初始化和实例化的顺序
id: 546
date: 2024-10-31 22:01:44
author: daichangya
excerpt: 一切都是java编译器搞得鬼. JVM只是负责解析字节码.字节码虽然不是最原始的原子汇编码,但字节码已经可以完全解释JVM的指令执行过程了。就像之前的一个评论.我们学习的是思路.
  很多人都知道继承关系的类的初始化和实例化的顺序,但如果忘记了怎么办? 如何找到自己的答案? 又如果遇到的问题是关于泛型的擦除问题,又该
permalink: /archives/ji-cheng-guan-xi-de-lei-chu-shi-hua-he/
categories:
- jvm
---



就像之前的一个评论.我们学习的是思路. 很多人都知道继承关系的类的初始化和实例化的顺序,但如果忘记了怎么办? 如何找到自己的答案? 又如果遇到的问题是关于泛型的擦除问题,又该如何去分析?

思路,重点是思路.泛型擦除先不谈.看继承. 首先给出一个例子,看看它的输出是什么.

```
public class A {
	private static String a = "NA";
	private String i="NA";
	{
		i = "A";
		System.out.println(i);
	}
	
	static {
		a = "Static A";
		System.out.println(a);
	}
	
	public A() {
		System.out.println("Construct A");
	}
}
```

```
public class B extends A {
	private static String b = "NB";
	private String j="NB";
	{
		j = "B";
		System.out.println(j);
	}
	
	static {
		b = "Static B";
		System.out.println(b);
	}
	
	public B() {
		System.out.println("Construct B");
	}
}
```

```java
public class C {
	public static void main(String[] args) {
		new B();
	}

}
```

以上输出是:  

Static A  
Static B  
A  
Construct A  
B  
Construct B

一切都是java编译器搞得鬼. JVM只是负责解析字节码.字节码虽然不是最原始的原子汇编码,但字节码已经可以完全解释JVM的指令执行过程了.一般来说,字节码和java源码相差比较大,javac会做前期优化,修改增加删除源码产生jvm解释器可以理解的字节码. java语法带来的安全,易用,易读等功能让我们忽略了字节码会和java源码有出路.

当遇到new的时候,比如new B(),将会尝试去初始化B类.如果B已经初始化,则开始实例化B类.如果B类没有初始化,则初始化B类,但B类继承A,所以在初始化B类之前需要先初始化A类.所以类的初始化过程是:A->B. 类在初始化的时候会执行static域和块. 类的实例化在类初始化之后,实例化的时候必须先实例化父类.实例化会先执行域和块,然后再执行构造函数.

上面的理论如果靠这种死记硬背,总会忘记.哦,还有父类的构造函数必须放在子类构造函数的第一行.为什么?

遇到这种语法问题的时候,看教科书不如自己找出答案.工具就在JDK中,一个名叫javap的命令. javap会打出一个class的字节码伪码. 我们只需要分析B的字节码,就可以找到答案.

```yaml
joeytekiMacBook-Air:bin joey$ javap -verbose B
Compiled from "B.java"
public class B extends A
  SourceFile: "B.java"
  minor version: 0
  major version: 50
  Constant pool:
const #1 = class	#2;	//  B
const #2 = Asciz	B;
const #3 = class	#4;	//  A
const #4 = Asciz	A;
const #5 = Asciz	b;
const #6 = Asciz	Ljava/lang/String;;
const #7 = Asciz	j;
const #8 = Asciz	<clinit>;
const #9 = Asciz	()V;
const #10 = Asciz	Code;
const #11 = String	#12;	//  NB
const #12 = Asciz	NB;
const #13 = Field	#1.#14;	//  B.b:Ljava/lang/String;
const #14 = NameAndType	#5:#6;//  b:Ljava/lang/String;
const #15 = String	#16;	//  Static B
const #16 = Asciz	Static B;
const #17 = Field	#18.#20;	//  java/lang/System.out:Ljava/io/PrintStream;
const #18 = class	#19;	//  java/lang/System
const #19 = Asciz	java/lang/System;
const #20 = NameAndType	#21:#22;//  out:Ljava/io/PrintStream;
const #21 = Asciz	out;
const #22 = Asciz	Ljava/io/PrintStream;;
const #23 = Method	#24.#26;	//  java/io/PrintStream.println:(Ljava/lang/String;)V
const #24 = class	#25;	//  java/io/PrintStream
const #25 = Asciz	java/io/PrintStream;
const #26 = NameAndType	#27:#28;//  println:(Ljava/lang/String;)V
const #27 = Asciz	println;
const #28 = Asciz	(Ljava/lang/String;)V;
const #29 = Asciz	LineNumberTable;
const #30 = Asciz	LocalVariableTable;
const #31 = Asciz	<init>;
const #32 = Method	#3.#33;	//  A."<init>":()V
const #33 = NameAndType	#31:#9;//  "<init>":()V
const #34 = Field	#1.#35;	//  B.j:Ljava/lang/String;
const #35 = NameAndType	#7:#6;//  j:Ljava/lang/String;
const #36 = String	#2;	//  B
const #37 = String	#38;	//  Construct B
const #38 = Asciz	Construct B;
const #39 = Asciz	this;
const #40 = Asciz	LB;;
const #41 = Asciz	SourceFile;
const #42 = Asciz	B.java;

{
static {};
  Code:
   Stack=2, Locals=0, Args_size=0
   0:	ldc	#11; //String NB
   2:	putstatic	#13; //Field b:Ljava/lang/String;
   5:	ldc	#15; //String Static B
   7:	putstatic	#13; //Field b:Ljava/lang/String;
   10:	getstatic	#17; //Field java/lang/System.out:Ljava/io/PrintStream;
   13:	getstatic	#13; //Field b:Ljava/lang/String;
   16:	invokevirtual	#23; //Method java/io/PrintStream.println:(Ljava/lang/String;)V
   19:	return
  LineNumberTable: 
   line 3: 0
   line 11: 5
   line 12: 10
   line 13: 19



public B();
  Code:
   Stack=2, Locals=1, Args_size=1
   0:	aload_0
   1:	invokespecial	#32; //Method A."<init>":()V
   4:	aload_0
   5:	ldc	#11; //String NB
   7:	putfield	#34; //Field j:Ljava/lang/String;
   10:	aload_0
   11:	ldc	#36; //String B
   13:	putfield	#34; //Field j:Ljava/lang/String;
   16:	getstatic	#17; //Field java/lang/System.out:Ljava/io/PrintStream;
   19:	aload_0
   20:	getfield	#34; //Field j:Ljava/lang/String;
   23:	invokevirtual	#23; //Method java/io/PrintStream.println:(Ljava/lang/String;)V
   26:	getstatic	#17; //Field java/lang/System.out:Ljava/io/PrintStream;
   29:	ldc	#37; //String Construct B
   31:	invokevirtual	#23; //Method java/io/PrintStream.println:(Ljava/lang/String;)V
   34:	return
  LineNumberTable: 
   line 15: 0
   line 4: 4
   line 6: 10
   line 7: 16
   line 16: 26
   line 17: 34

  LocalVariableTable: 
   Start  Length  Slot  Name   Signature
   0      35      0    this       LB;


}
```

类的生命周期,将经历类的装载,链接,初始化,使用,卸载. 装载是将字节码读入到内存的方法区中, 而类的初始化则会在线程栈中执行static{}块的code. 在之前,这个块有另一个名字<cinit>即类初始化方法.现在改名为static{}了. 类的初始化只进行一次. 但是,每当一个类在装载和链接完毕以后,通过字节码的分析,JVM解析器已经知道B是继承A的,于是在初始化B类前,A类会先初始化.这是一个递归过程. 所以,B类的初始化会导致A类static{}执行,然后是B的static{}执行.让我们看看B的static{}块中执行了什么.

```objectivec
static {};
  Code:
   Stack=2, Locals=0, Args_size=0
栈深为2,本地变量0个,参数传递0个.
   0:	ldc	#11; //String NB
将常量池中#11放到栈顶.#11="NB".
   2:	putstatic	#13; //Field b:Ljava/lang/String;
将栈顶的值 "NB" 赋予常量池中的#13,也就是 static b="NB".
   5:	ldc	#15; //String Static B
将#15放入栈顶. #15="static B".
   7:	putstatic	#13; //Field b:Ljava/lang/String;
赋值static b = "static B".
   10:	getstatic	#17; //Field java/lang/System.out:Ljava/io/PrintStream;
将PrintStream引用压栈.
   13:	getstatic	#13; //Field b:Ljava/lang/String;
将static b的值压栈.
   16:	invokevirtual	#23; //Method java/io/PrintStream.println:(Ljava/lang/String;)V
调用虚函数PrintStream.println("static B")
   19:	return
退出函数,销毁函数栈帧.
```

通过注释,我们看到类B中的static域赋值和static块均被放到了类的初始化函数中.

当我们进行类的实例化的时候,会调用类的构造函数.我们看看类B的构造函数做了什么.

```kotlin
public B();
  Code:
   Stack=2, Locals=1, Args_size=1
栈深为2,本地变量1个(其实就是this),参数为1个(就是this).
   0:	aload_0
将第一个参数压栈.也就是this压栈.
   1:	invokespecial	#32; //Method A."<init>":()V
在this上调用父类的构造函数.在B的构造函数中并没有声明super(),但是java编译器会自动生成此字节码来调用父类的无参构造函数.如果在B类中声明了super(int),编译器会使用对应的A类构造函数来代替.JVM只是执行字节码而已,它并不对super进行约束,约束它们的是java的编译器.this出栈.
   4:	aload_0
将this压栈.
   5:	ldc	#11; //String NB
将"NB"压栈.
   7:	putfield	#34; //Field j:Ljava/lang/String;
给j赋值this.j="NB". this和"NB"出栈.
   10:	aload_0
将this压栈.
   11:	ldc	#36; //String B
把"B"压栈
   13:	putfield	#34; //Field j:Ljava/lang/String;
给j赋值this.j="B". this和"B"出栈.栈空
   16:	getstatic	#17; //Field java/lang/System.out:Ljava/io/PrintStream;
压栈PrintStream
   19:	aload_0
压栈this
   20:	getfield	#34; //Field j:Ljava/lang/String;
this出栈,调用this.j,压栈this.j.
   23:	invokevirtual	#23; //Method java/io/PrintStream.println:(Ljava/lang/String;)V
调用PrintStream.println(this.j).栈空.
   26:	getstatic	#17; //Field java/lang/System.out:Ljava/io/PrintStream;
压栈PrintStream
   29:	ldc	#37; //String Construct B
压栈"Construct B"
   31:	invokevirtual	#23; //Method java/io/PrintStream.println:(Ljava/lang/String;)V
调用PrintStream.println("Construct B")
   34:	return
```

从上面的字节码可以看出,java编译器在编译产生字节码的时候,将父类的构造函数,域的初始化,代码块的执行和B的真正的构造函数按照顺序组合在了一起,形成了新的构造函数. 一个类的编译后的构造函数字节码一定会遵循这样的顺序包含以下内容:  
父类的构造函数->  
当前类的域初始化->(按照书写顺序)  
代码块->(按照书写顺序)  
当前类的构造函数.

到这里,应该彻底明白继承类的初始化和实例化顺序了.