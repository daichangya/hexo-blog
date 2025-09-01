---
title: 常见的Java问题排查方法
id: 493
date: 2024-10-31 22:01:43
author: daichangya
excerpt: "以下是Java应用在运行时常见的一些问题，总结了运行时黑盒方式的一些排查方法，也希望看到的同学能给予补充，无论是补充碰到的问题，还是补充解决方法。

类装载的相关问题
写过Java代码的同学估计都碰到过ClassNotFoundException/NoClassDefFoundError/NoSuchMethodException（还有一个常见的ClassCastException就不在这里"
permalink: /archives/8872552/
categories:
 - java
---

 

以下是Java应用在运行时常见的一些问题，总结了运行时黑盒方式的一些排查方法，也希望看到的同学能给予补充，无论是补充碰到的问题，还是补充解决方法。

类装载的相关问题  
写过Java代码的同学估计都碰到过ClassNotFoundException/NoClassDefFoundError/NoSuchMethodException（还有一个常见的ClassCastException就不在这里说了）。

当碰到ClassNotFoundException/NoClassDefFound时，如果很确定这个class应该是从哪个路径装载的，则可以去相应的路径找下是否有对应的class文件存在，例如web应用通常会在*.war(ear)/WEB-INF/lib或classes目录下，对于lib下的jar包，可通过写个小脚本jar -tvf的方式找找；  
如不确定class是从哪装载的，则可以先看看日志里是否有堆栈信息，如果有的话则可以看到具体是哪个ClassLoader实现在装载class，之后则可以通过www.grepcode.com或jar包反编译（推荐一个挺好用的[反编译工具](http://java.decompiler.free.fr/?q=jdgui "挺好用的反编译工具")）看看具体是从哪装载的class；  
如日志中没有，则可以用btrace来跟踪下抛出以上两个异常的堆栈信息，btrace脚本类似如下：

	import static com.sun.btrace.BTraceUtils.*;
	import com.sun.btrace.annotations.*;
	@BTrace public class Trace{
	   @OnMethod(
		   clazz="java.lang.ClassNotFoundException",
		   method="<init>"
	   )
	   public static void traceExecute(){
			jstack();
	   }
	}

拿到堆栈信息后，可以继续使用上面的方法进行排查，在确认了class装载的位置后，则可将相应的class/jar加上即可。  
这里还有个[NoClassDefFoundError排查的case](http://bluedavy.me/?p=300 "NoClassDefFoundError")，感兴趣的话可以看看。

当碰到NoSuchMethodException时，通常是由于不存在需要的class版本或class版本冲突造成的，在这种情况下，可通过在启动参数上增加-XX:+TraceClassLoading，重启后在日志里看看此class是在哪load的，然后可以在对应的路径下用jar -tvf找找是不是有正确的版本的jar存在，通常可能会发现是版本冲突造成的，对于版本冲突的问题通常需要删掉有冲突的版本的jar，对于没有正确版本的，则需要用正确版本的jar替换掉（当然，这种通常还会出现一些恶心的问题，例如和容器/框架的jar冲突等）。

cpu us消耗高  
当出现cpu us消耗高时，通常的排查方法如下。

从经验上来说，有些时候是由于频繁cms gc或fgc造成的（频繁的意思是差不多每次cms gc或fgc一结束后又立刻继续），在gc log是记录的情况下（-Xloggc:），可通过gc log看看，如果没打开gc log，可通过jstat -gcutil来查看，如是gc频繁造成的，则可跳到后面的内存问题 | GC频繁部分看排查方法。

如不是上面的原因，可使用top -H查看线程的cpu消耗状况，这里有可能会看到有个别线程是cpu消耗的主体，这种情况通常会比较好解决，可根据top看到的线程id进行十六进制的转换，用转换出来的值和jstack出来的java线程堆栈的nid=0x\[十六进制的线程id\]进行关联，即可看到此线程到底在做什么动作，这个时候需要进一步的去排查到底是什么原因造成的，例如有可能是正则计算，有可能是很深的递归或循环，也有可能是[错误的在并发场景使用HashMap](http://bugs.caucho.com/view.php?id=1588 "hessian知名的hashmap bug")等，例如这里还有一段[随即生成字符串的耗cpu的代码case](http://bluedavy.me/?p=269 "一段耗CPU的随机生成字符串的代码，why？")。

如top -H看到的消耗cpu的线程是不断变化的，就比较麻烦了，有个同学写了个[脚本](https://github.com/oldratlee/useful-shells "关联top和jstack的脚本")自动的去通过top -H看到的消耗cpu的线程找到对应的Java线程堆栈，在这种情况下可以用这个脚本去试试，如果看到的线程堆栈确实是比较耗cpu的动作，则基本可以定位到。

如仍然看不出，则可以尝试多jstack看看，然后多看看是否经常有一些耗cpu的动作在不同的线程不断的出现。

如可使用perf，则可用perf top看看cpu消耗的热点，不过默认的版本上只能看到jit后的代码，因此可能会比较难对应到具体的代码，这里有一个[基于perf排查的Java应用cpu us诡异现象的case](http://bluedavy.me/?p=409 "一个Java应用频繁抛异常导致cpu us诡异现象的案例")。

总结来说，cpu us消耗高的问题排查还是有一定复杂性，例如之前我碰到过反序列化的对象比较大，请求又非常频繁，导致cpu us消耗增高了很多，但当时的机器内核版本不够，不支持perf，从jstack等等上都看不出什么，后来是由于从业务监控的变化上才排查出问题。

cpu iowait高  
具体可见[一个cpu iowait高的case的排查](http://hellojava.info/?p=71)。

cpu sy高  
具体可见[这个case的排查](http://hellojava.info/?p=101)。

内存问题  
尽管JVM是自动管理内存的分配和回收的，但Java程序员们还是会经常碰到各种各样的内存问题。

最常见的第一个问题是java.lang.OutOfMemoryError，估计写Java的同学都碰到过。  
在日志中可能会看到java.lang.OutOfMemoryError: Unable to create new native thread，可以先统计下目前的线程数(例如ps -eLf | grep java -c)，然后可以看看ulimit -u的限制值是多少，如线程数已经达到限制值，如限制值可调整，则可通过调整限制值来解决；如不能调限制值，或者创建的线程已经很多了，那就需要看看线程都是哪里创建出来的，同样可通过btrace来查出是哪里创建的，脚本类似如下：

	import static com.sun.btrace.BTraceUtils.*;
	import com.sun.btrace.annotations.*;
	@BTrace public class Trace{
	   @OnMethod(
		   clazz="java.lang.Thread",
		   method="start"
	   )
	   public static void traceExecute(){
			jstack();
	   }
	}

在找到是哪里创建造成了后，之后就可以想办法解决了，例如这种情况下常见的有可能是用了Executors.newCachedThreadPool这种来创建了一个没限制大小的线程池。  
还有一种可能是ulimit -u的限制还没到，内存也空闲，但仍然创建不了，这有可能是由于在2.6.18/32内核上kernel.pid_max默认的32768造成的，这个值其实直接限制了最多能创建的线程数就是32768（即使ulimit -u的值比这大也没用）。

java.lang.OutOfMemoryError: Heap Size或GC overhead limit exceeded也是常见的现象，在出现了这两种现象的情况下，最重要的是dump出内存，一种方法是通过在启动参数上增加-XX:+HeapDumpOnOutOfMemoryError，另一种方法是在当出现OOM时，通过jmap -dump获取到内存dump，在获取到内存dump文件后，可通过MAT进行分析，但通常来说仅仅靠MAT可能还不能直接定位到具体应用代码中哪个部分造成的问题，例如MAT有可能看到是某个线程创建了很大的ArrayList，但这样是不足以解决问题的，所以通常还需要借助btrace来定位到具体的代码，可以看看这两个[OOM排查的case](http://bluedavy.me/?p=205 "两个OOM排查的Case")。

java.lang.OutOfMemoryError: PermGen Space，当碰到这个现象时，可以通过调整permgen size来试试，如果放大了一点后还是不断的消耗，则可以通过btrace来跟踪下装载class的现象，脚本类似如下：

	import static com.sun.btrace.BTraceUtils.*;
	import com.sun.btrace.annotations.*;
	@BTrace public class Trace{
	   @OnMethod(
		   clazz="java.lang.ClassLoader",
		   method="defineClass"
	   )
	   public static void traceExecute(){
			jstack();
	   }
	}

还有一种OOM是native OOM，就是物理内存被耗光，对于这种现象，解决起来会麻烦一些，从经验上来说，Native OOM有很大概率是由于错误使用Deflater/Inflater造成的，所以在碰到这类现象时，可以先用btrace跟进下看看使用了Deflater/Inflater的有没有显式去调用end方法；另外一种常见的原因是使用Direct ByteBuffer的场景（例如NIO框架等），如使用了Direct ByteBuffer的对象是比较长存活的，当其被转到旧生代后，在fgc没触发前，其实其占用的JVM堆外内存是不会被释放的，在这种情况下，可以做的一个尝试是先强制执行几次fgc（jmap -histo:live），然后看看堆外内存的使用是不是下降了，如果下降了则说明是这个问题，对于这类问题，可以用的一个解决方案是增加一个启动参数：-XX:MaxDirectMemorySize=500m来实现当Direct ByteBuffer使用到500m后主动触发fgc来回收（到底设置成多大应用可以自己调整）。  
如上面两招都没用，则需要挂上[google perf-tools](https://code.google.com/p/gperftools/ "google perftools")来跟踪下看看到底是哪里在malloc，不过这里看到的是c堆栈上的东西，因此需要自己想办法根据这个对应到java的代码上去。  
关于native OOM，这篇文章里有一些具体排查的[case](http://bluedavy.me/?p=300 "Java问题排查的Cases")。

除了OOM外，还有可能会碰到GC频繁的问题（有很多同学会问我，到底什么算频繁，我觉得基本上如果每隔10s或更短时间就来一次cms gc或full gc才算得上吧）。  
GC频繁的现象出现时，如果发现cms gc或full gc后，存活的对象始终很多，这种情况下可以通过jmap -dump来获取下内存dump文件，然后通过MAT/btrace来定位到具体的原因。  
如cms gc或full gc频繁，但触发时old还有空闲空间，这种情况下有可能会是由于悲观策略造成，具体可以看看这篇文章里的几个[cases](http://bluedavy.me/?p=300 "Java问题排查的Cases")，这种情况下通常的解决方法可以是调大old或减小young。  
如不是悲观策略造成的，对于采用cms gc的情况，还有可能是cms gc的碎片问题造成的，这种情况下可以通过强制执行下jmap -histo:live来触发fgc，不过悲催的是cms gc的碎片问题是无解的，暂时只能靠强制触发fgc等来避免在高峰期时出现问题。  
对于cms gc而言，还有可能会出现promotion failed或concurrent mode failure问题，具体也可以看看上面那篇文章的cases。

Java进程crash或退出  
Java进程crash或无故退出也是会碰到的现象，对于进程crash，默认情况下jdk会生成hs\_err\[pid\].log的文件，core dump打开的话也会生成core dump文件，当进程crash发生时，可以先看看hs\_err\[pid\].log，如没找到此文件，但有core dump文件，有可能的原因是代码中出现了无限递归或死循环，可通过jstack

\[core dump文件\]来提取出java的线程堆栈，从而具体定位到具体的代码；如有hs_err\[pid\].log以及core dump文件，则需要具体原因具体排查，这个比较麻烦，常见的可能会有上面的native oom（还有可能是32 bit机器，但java进程已经申请了超过3g的地址空间），某些代码jit编译出问题了（可通过指定某些代码不让jit编译来避免，但会影响性能：-XX:CompileCommand=exclude,类名/方法名）等。  
在上面的招还无效时，可以尝试dmesg看看是不是系统出了什么问题或系统主动杀掉过进程（例如内存超出限制等），仍然没找到原因的话需要去翻翻应用的日志，看看是不是能找到什么线索，因为有些时候是应用上主动退出了（对于应用主动退出的问题可通过btrace来排查是不是有主动调用过System.exit）。

硬件资源未到瓶颈，但吞吐量上不去  
如在压测时，出现这个现象时，首先可以看看施加压力的一端是否真的压力传递到了服务端。  
如确认，则可以看看从server接到请求的地方开始，是不是处理线程池满了（例如假设是tomcat，最大的线程数大小是不是已经到了），如处理线程池满了，可考虑扩大线程数大小，这个地方的排查其实有点麻烦，需要从接收请求的部分一直到纯粹的业务处理部分，看看每步的瓶颈状况，例如有些时候新建连接这种还有可能是由于系统参数的问题；  
另外，需要看的就是锁的状况，可通过jstack -l来查看，也许是由于锁竞争激烈造成，在锁竞争激烈出现时，需要考虑使用j.u.c里的数据结构或使用无锁算法等来优化。