---
title: JVM执行篇：使用HSDIS插件分析JVM代码执行细节
id: 758
date: 2024-10-31 22:01:45
author: daichangya
excerpt: 在《Java虚拟机规范》之中，详细描述了虚拟机指令集中每条指令的执行过程、执行前后对操作数栈、对局部变量表的影响等细节。这些细节描述与Sun的早期虚拟机（Sun
  Classic VM）高度吻合，但随着技术的发展，高性能虚拟机真正的细节实现方式已经渐渐与虚拟机规范所描述产生越来越大的差距，虚拟机规范中的描述逐渐成了虚拟机实现的“概念模型”——即实现只能保证规范描述等效。
permalink: /archives/JVM-zhi-xing-pian-shi-yong-HSDIS-cha/
categories:
- jvm
---

在《Java虚拟机规范》之中，详细描述了虚拟机指令集中每条指令的执行过程、执行前后对操作数栈、对局部变量表的影响等细节。这些细节描述与Sun的早期虚拟机（Sun Classic VM）高度吻合，但随着技术的发展，高性能虚拟机真正的细节实现方式已经渐渐与虚拟机规范所描述产生越来越大的差距，虚拟机规范中的描述逐渐成了虚拟机实现的“概念模型”——即实现只能保证规范描述等效。

基于上面的原因，我们分析程序的执行语义问题（虚拟机做了什么）时，在字节码层面上分析完全可行，但分析程序的执行行为问题（虚拟机是怎样做的、性能如何）时，在字节码层面上分析就没有什么意义了，需要通过其他方式解决。

## 准备工作

分析程序如何执行，通过软件调试工具（GDB、Windbg等）来断点调试是最常见的手段，但是这样的调试方式在JVM中会遇到很大困难，因为大量执行代码是通过JIT编译器动态生成到CodeBuffer中的，没有很简单的手段来处理这种混合模式的调试（不过相信虚拟机开发团队内部肯定是有内部工具的）。因此我们要通过一些曲线手段来解决问题，基于这种背景下，本文的主角——HSDIS插件就正式登场了。

  
当然，既然是通过-XX:+PrintAssembly指令使用的插件，那自然还要求一份FastDebug版的JDK，在OpenJDK网站上各个JDK版本发布时一般都伴随有FastDebug版的可以下载，不过听说JDK 7u02之后不再提供了，要用最新的JDK版本就可能需要自己编译。笔者所使用的虚拟机是HotSpot B127 FastDebug（JDK 7 EA时的VM），默认为Client VM，后面的案例都基于这个运行环境之下：HSDIS是由Project Kenai（http://kenai.com/projects/base-hsdis）提供并得到Sun官方推荐的HotSpot VM JIT编译代码的反汇编插件，作用是让HotSpot的-XX:+PrintAssembly指令调用它来把动态生成的本地代码还原为汇编代码输出，同时还生成了大量非常有价值的注释，这样我们就可以通过输出的代码来分析问题。读者可以根据自己的操作系统和CPU类型从Kenai的网站上下载编译好的插件，直接放到JDK\_HOME/jre/bin/client和JDK\_HOME/jre/bin/server目录中即可。如果没有找到所需操作系统（譬如Windows的就没有）的成品，那就得自己拿源码编译一下，或者去HLLVM圈子（http://hllvm.group.iteye.com/）中下载也可以。

代码清单1：

	>java -version
	java version "1.7.0-ea-fastdebug"
	Java(TM) SE Runtime Environment (build 1.7.0-ea-fastdebug-b127)
	Java HotSpot(TM) Client VM (build 20.0-b06-fastdebug, mixed mode)

## 案例一：Java堆、栈在本地代码中的存在形式

环境准备好后，本篇的话题正式开始。三个案例都是笔者给朋友的回信，第一个案例的问题是“在Java虚拟机规范中把虚拟机内存划分为Java Heap、Java VM Stack、Method Area等多个运行时区域，那当ByteCode编译为Native Code后，Java堆、栈、方法区还是原来那个吗？在Java堆、栈、方法区中的数据是如何访问的？”

我们通过下面这段简单代码的实验来回答这个问题：

代码清单2

	public class Bar {
	    int a = 1;
	    static int b = 2;

	    public int sum(int c) {
		return a + b + c;
	    }

	    public static void main(String[] args) {
		new Bar().sum(3);
	    }
	}

代码很简单，sum()方法使用到3个变量a、b、c，按照概念模型中的划分，其中a是实例变量，来自Java Heap，b是类变量，来自Method Area，c是参数，来自VM Stack。那我们来看看JIT之后，它们是怎么访问的。使用下面命令来执行上述代码：

	>java -XX:+PrintAssembly -Xcomp -XX:CompileCommand=dontinline,\*Bar.sum -XX:CompileCommand=compileonly,\*Bar.sum test.Bar 

其中，参数-Xcomp是让虚拟机以编译模式执行代码，这样代码可以偷懒，不需要执行足够次数来预热都能触发JIT编译。两个-XX:CompileCommand意思是让编译器不要内联sum()并且只编译sum()，-XX:+PrintAssembly就是输出反汇编内容。如果一切顺利的话，屏幕上出现类似下面代码清单3所示的内容：

代码清单3

	[Disassembling for mach='i386']
	[Entry Point]
	[Constants]
	  # {method} 'sum' '(I)I' in 'test/Bar'
	  # this:     ecx       = 'test/Bar'
	  # parm0:    edx       = int
	  #           [sp+0x20]  (sp of caller)
	  ……
	  0x01cac407: cmp    0x4(%ecx),%eax
	  0x01cac40a: jne    0x01c6b050         ;   {runtime_call}
	[Verified Entry Point]
	  0x01cac410: mov    %eax,-0x8000(%esp)
	  0x01cac417: push   %ebp
	  0x01cac418: sub    $0x18,%esp         ;*aload_0
		                                ; \- test.Bar::sum@0 (line  8)
	  ;;  block B0 [0, 10]

	  0x01cac41b: mov    0x8(%ecx),%eax     ;*getfield a
		                                ; \- test.Bar::sum@1 (line 8)
	  0x01cac41e: mov    $0x3d2fad8,%esi    ;   {oop(a 
	'java/lang/Class' = 'test/Bar')}
	  0x01cac423: mov    0x68(%esi),%esi    ;*getstatic b
		                                ; \- test.Bar::sum@4 (line 8)
	  0x01cac426: add    %esi,%eax
	  0x01cac428: add    %edx,%eax
	  0x01cac42a: add    $0x18,%esp
	  0x01cac42d: pop    %ebp
	  0x01cac42e: test   %eax,0x2b0100      ;   {poll_return}
	  0x01cac434: ret   

代码并不多，一句一句来看：

	1.  mov %eax,-0x8000(%esp)：检查栈溢。
	2.  push %ebp：保存上一栈帧基址。
	3.  sub $0x18,%esp：给新帧分配空间。
	4.  mov 0x8(%ecx),%eax：取实例变量a，这里0x8(%ecx)就是ecx+0x8的意思，前面“[Constants]”节中提示了“this:ecx = 'test/Bar'”，即ecx寄存器中放的就是this对象的地址。偏移0x8是越过this对象的对象头，之后就是实例变量a的内存位置。这次是访问“Java堆”中的数据。
	5.  mov $0x3d2fad8,%esi：取test.Bar在方法区的指针。
	6.  mov 0x68(%esi),%esi：取类变量b，这次是访问“方法区”中的数据。
	7.  add %esi,%eax 、add %edx,%eax：做2次加法，求a+b+c的值，前面的代码把a放在eax中，把b放在esi中，而c在[Constants]中提示了，“parm0:edx = int”，说明c在edx中。
	8.  add $0x18,%esp：撤销栈帧。
	9.  pop %ebp：恢复上一栈帧。
	10.  test %eax,0x2b0100：轮询方法返回处的SafePoint
	11.  ret：方法返回。

从汇编代码中可见，访问Java堆、栈和方法区中的数据，都是直接访问某个内存地址或者寄存器，之间并没有看见有什么隔阂。HotSpot虚拟机本身是一个运行在物理机器上的程序，Java堆、栈、方法区都在Java虚拟机进程的内存中分配。在JIT编译之后，Native Code面向的是HotSpot这个进程的内存，说变量a还在Java Heap中，应当理解为a的位置还在原来的那个内存位置上，但是Native Code是不理会Java Heap之类的概念的，因为那并不是同一个层次的概念。

## 案例二：循环语句的写法以及Client和Server的性能差异

如果第一个案例还有点抽象的话，那这个案例就更具体实际一些：有位朋友给了笔者下面这段代码（如代码清单4所示），并提出了2个问题：

1.  在写循环语句时，“for (int i = 0, n = list.size(); i < n; i++)”的写法是否会比“for (int i = 0; i < list.size(); i++)”更快？
2.  为何这段代码在Server VM下测出来的速度比Client VM还慢？

代码清单4：

	public class Client1 {
	    public static void main(String[] args) {
		List<Object> list = new ArrayList<Object>();
		Object obj = new Object();
		// 填充数据
		for (int i = 0; i < 200000; i++) {
		    list.add(obj);
		}
		long start;

		start = System.nanoTime();
		// 初始化时已经计算好条件
		for (int i = 0, n = list.size(); i < n; i++) {
		}
		System.out.println("判断条件中计算：" + (System.nanoTime() - start) + " ns");

		start = System.nanoTime();
		// 在判断条件中计算
		for (int i = 0; i < list.size(); i++) {
		}
		System.out.println("判断条件中计算：" + (System.nanoTime() - start) + " ns");
	    }
	}

首先来看，代码最终执行时，for (int i = 0, n = list.size(); i < n; i++)的写法所生成的代码与for (int i = 0; i < list.size(); i++)有何差别。它们反汇编的结果如下（提取循环部分的代码）：

代码清单5：for (int i = 0, n = list.size(); i < n; i++)的循环体

	0x01fcd554: inc    %edx               ; OopMap{[60]=Oop off=245}
		                                 ;*if_icmplt
		                                 ; \- Client1::main@63 (line 17)
	0x01fcd555: test   %eax,0x1b0100    ;   {poll}
	0x01fcd55b: cmp    %eax,%edx
	;;  124 branch [LT] [B5] 
	0x01fcd55d: jl     0x01fcd554        ;*if_icmplt
		                                  ; \- Client1::main@63 (line 17)

变量i放在edx中，变量n放在eax中，inc指令对应i++（被优化成++i了），test指令是在回边处进行轮询SafePoint，cmp是比较n和i的值，jl就是当i<n的时候进行跳转，跳转的地址是回到inc指令。

代码清单6：for (int i = 0; i < list.size(); i++)的循环体

	0x01b6d610: inc    %esi
	  ;;  block B7 [110, 118]

	0x01b6d611: mov    %esi,0x50(%esp)
	0x01b6d615: mov    0x3c(%esp),%esi
	0x01b6d619: mov    %esi,%ecx          ;*invokeinterface size
		                                ; \- Client1::main@113 (line 23)
	0x01b6d61b: mov    %esi,0x3c(%esp)
	0x01b6d61f: nop    
	0x01b6d620: nop    
	0x01b6d621: nop    
	0x01b6d622: mov    $0xffffffff,%eax   ;   {oop(NULL)}
	0x01b6d627: call   0x01b2b210         ; OopMap{[60]=Oop off=460}
		                                ;*invokeinterface size
		                                ; \- Client1::main@113 (line 23)
		                                ;   {virtual_call}
	0x01b6d62c: nop                       ; OopMap{[60]=Oop off=461}
		                                ;*if_icmplt
		                                ; \- Client1::main@118 (line 23)
	0x01b6d62d: test   %eax,0x160100      ;   {poll}
	0x01b6d633: mov    0x50(%esp),%esi
	0x01b6d637: cmp    %eax,%esi
	;;  224 branch [LT] [B8] 
	0x01b6d639: jl     0x01b6d610         ;*if_icmplt
		                                ; \- Client1::main@118 (line 23)

可以看到，除了上面原有的几条指令外，确实还多了一次invokeinterface方法调用，执行的方法是size()，方法接收者是list对象，除此之外，其他指令都和上面的循环体一致。所以至少在HotSpot Client VM中，第一种循环的写法是能提高性能的，因为实实在在地减少了一次方法调用。

但是这个结论并不是所有情况都能成立，譬如这里把list对象从ArrayList换成一个普通数组，把list.size()换成list.length。那将可以观察到两种写法输出的循环体是完全一样的（都和前面第一段汇编的循环一样），因为虚拟机不能保证ArrayList的size()方法调用一次和调用N次是否会产生不同的影响，但是对数组的length属性则可以保证这一点。也就是for (int i = 0, n = list.length; i < n; i++)和for (int i = 0; i < list.length; i++)的性能是没有什么差别的。

再来继续看看为何这段代码在Server VM下测出来的速度比Client VM还慢，这个问题不好直接比较Server VM和Client VM所生成的汇编代码，因为Server VM经过重排序后，代码结构完全混乱了，很难再和前面代码的比较，不过我们还是可以注意到两者编译过程的不同，加入-XX:+ PrintCompilation参数后，它们的编译过程输出如下：

代码清单7：Server VM和Client VM的编译过程

// 下面是Client VM的编译过程

	VM option '+PrintCompilation'
	    169   1       java.lang.String::hashCode (67 bytes)
	    172   2       java.lang.String::charAt (33 bytes)
	    174   3       java.lang.String::indexOf (87 bytes)
	    179   4       java.lang.Object::<init> (1 bytes)
	    185   5       java.util.ArrayList::add (29 bytes)
	    185   6       java.util.ArrayList::ensureCapacityInternal (26 bytes)
	    186   1%      Client1::main @ 21 (79 bytes)

// 下面是Server VM的编译过程

	VM option '+PrintCompilation'
	    203   1       java.lang.String::charAt (33 bytes)
	    218   2       java.util.ArrayList::add (29 bytes)
	    218   3       java.util.ArrayList::ensureCapacityInternal (26 bytes)
	    221   1%      Client1::main @ 21 (79 bytes)
	    230   1%     made not entrant  Client1::main @ -2 (79 bytes)
	    231   2%      Client1::main @ 51 (79 bytes)
	    233   2%     made not entrant  Client1::main @ -2 (79 bytes)
	    233   3%      Client1::main @ 65 (79 bytes)

可以看到，ServerVM中OSR编译发生了3次，丢弃了其中2次（made not entrant的输出），换句话说，在这个TestCase里面，main()方法的每个循环JIT编译器都要折腾一下子。当然这并不是ServerVM看起来比ClientVM看起来慢的唯一原因。ServerVM的优化目的是为了长期执行生成尽可能高度优化的执行代码，为此它会进行各种努力：譬如丢弃以前的编译成果、在解释器或者低级编译器（如果开启多层编译的话）收集性能信息等等，这些手段在代码实际执行时是必要和有效的，但是在Microbenchmark中就会显得很多余并且有副作用。因此写Microbenchmark来测试Java代码的性能，经常会出现结果失真。

## 案例三：volatile变量与指令重排序

在JMM模型（特指JDK 5修复后的JMM模型）中，对volatile关键字赋予的其中一个语义是禁止指令重排序优化，这个语义可以保证在并发访问volatile变量时保障一致性，在外部线程观察volatile变量确保不会得到脏数据。这也是为何在JDK 5后，将变量声明为volatile就可以使用DCL（Double Checked Locking）来实现单例模式的原因。那进一步的问题就是volatile变量访问时与普通变量有何不同？它如何实现禁止重排序的呢？

首先，我们编写一段标准的DCL单例代码，如代码清单8所示。观察加入volatile和未加入volatile关键字时生成汇编代码的差别。

代码清单8：

	public class Singleton {

	    private volatile static Singleton instance;

	    public static Singleton getInstance() {
		if (instance == null) {
		    synchronized (Singleton.class) {
		        if (instance == null) {
		            instance = new Singleton();
		        }
		    }
		}
		return instance;
	    }

	    public static void main(String[] args) {
		    Singleton.getInstance();
	    }
	}

编译后，这段代码对instance变量赋值部分代码清单9所示：

代码清单9：

	0x01a3de0f: mov    $0x3375cdb0,%esi   ;...beb0cd75 33
		                                ;   {oop('Singleton')}
	0x01a3de14: mov    %eax,0x150(%esi)   ;...89865001 0000
	0x01a3de1a: shr    $0x9,%esi          ;...c1ee09
	0x01a3de1d: movb   $0x0,0x1104800(%esi)  ;...c6860048 100100
	0x01a3de24: lock addl $0x0,(%esp)     ;...f0830424 00
		                                ;*putstatic instance
		                                ; \- Singleton::getInstance@24 

通过对比发现，关键变化在于有volatile修饰的变量，赋值后（前面mov %eax,0x150(%esi)这句便是赋值操作）多执行了一个“lock addl $0x0,(%esp)”操作，这个操作相当于一个内存屏障，只有一个CPU访问内存时，并不需要内存屏障；但如果有两个或更多CPU访问同一块内存，且其中有一个在观测另一个，就需要内存屏障来保证一致性了。

指令“addl $0x0,(%esp)”显然是一个空操作，关键在于lock前缀，查询IA32手册，它的作用是使得本CPU的Cache写入了内存，该写入动作也会引起别的CPU invalidate其Cache。所以通过这样一个空操作，可让前面volatile变量的修改对其他CPU立即可见。

那为何说它禁止指令重排序呢？从硬件架构上讲，指令重排序是指CPU采用了允许将多条指令不按程序规定的顺序分开发送给各相应电路单元处理。但并不是说指令任意重排，CPU需要能正确处理指令依赖情况保障程序能得出正确的执行结果。譬如指令1把地址A中的值加10，指令2把地址A中的值乘以2，指令3把地址B中的值减去3，这时指令1和指令2是有依赖的，它们之间的顺序不能重排——(A+10）\*2与A\*2+10显然不相等，但指令3可以重排到指令1、2之前或者中间，只要保证CPU执行后面依赖到A、B值的操作时能获取到正确的A和B值即可。所以在本内CPU中，重排序看起来依然是有序的。因此，lock addl $0x0,(%esp)指令把修改同步到内存时，所有之前的操作都已经执行完成，这样便形成了“指令重排序无法越过内存屏障”的效果。

* * *
