---
title: Java内存管理面试指南一
id: 1393
date: 2024-10-31 22:01:53
author: daichangya
excerpt: 1.简介在本文中，我们将探讨一些在Java开发人员访谈中经常出现的内存管理问题。内存管理是一个很少有开发人员熟悉的领域。实际上，开发人员通常不必直接处理这个概念，因为JVM会处理所有细节。除非出现严重问题，否则即使是经验丰富的开发人员也可能一触即发就无法获得有关内存管理的准确信息。另一方面，这些概念
permalink: /archives/Java-nei-cun-guan-li-mian-shi-zhi-nan-yi/
categories:
- 面试指南
---

1. [Java内存管理面试指南一](https://blog.jsdiff.com/archives/java-memory-interview-1)
2. [Java基础面试指南一](https://blog.jsdiff.com/archives/java-basic-interview-1)
3. [Java基础面试指南二](https://blog.jsdiff.com/archives/java-basic-interview-2)
4. [Java基础面试指南三](https://blog.jsdiff.com/archives/java-basic-interview-3)
5. [Java基础面试指南四](https://blog.jsdiff.com/archives/java-basic-interview-4)
6. [Java线程面试指南一](https://blog.jsdiff.com/archives/java-thread-interview-1)
7. [Java线程面试指南二](https://blog.jsdiff.com/archives/java-thread-interview-2)
8. [Redis面试指南一](https://blog.jsdiff.com/archives/redis-interview-1)
9. [Kafka面试指南一](https://blog.jsdiff.com/archives/kafka-interview-1)
10. [Spring面试指南一](https://blog.jsdiff.com/archives/spring-interview-1)
11. [SpringBoot面试指南一](https://blog.jsdiff.com/archives/springboot-interview-1)
12. [微服务面试指南一](https://blog.jsdiff.com/archives/microservice-interview-1)

1.简介[](#introduction)
---------------------

在本文中，我们将探讨一些在Java开发人员访谈中经常出现的内存管理问题。内存管理是一个很少有开发人员熟悉的领域。

实际上，开发人员通常不必直接处理这个概念，因为JVM会处理所有细节。除非出现严重问题，否则即使是经验丰富的开发人员也可能一触即发就无法获得有关内存管理的准确信息。

另一方面，这些概念实际上在面试中非常普遍-因此，让我们直接进入。

2.问题[](#questions)
------------------

### **Q1。“用Java管理内存”是什么意思?**[](#q1-what-does-the-statement-memory-is-managed-in-java-mean)

内存是应用程序有效运行所必需的关键资源，并且像任何资源一样，它是稀缺的。因此，在应用程序或应用程序的不同部分之间来回分配和重新分配需要很多注意和考虑。

但是，在Java中，开发人员无需显式分配和取消分配内存-JVM，更具体地说是垃圾回收器-负责处理内存分配，因此开发人员不必这样做。

这与C语言(程序员可以直接访问内存并在其代码中直接引用内存单元)产生了很大的内存泄漏空间相反。

### **Q2。什么是垃圾回收及其优势?**[](#q2-what-is-garbage-collection-and-what-are-its-advantages)

垃圾收集是查看堆内存，识别正在使用的对象和未使用的对象以及删除未使用的对象的过程。

使用中的对象或引用的对象意味着程序的某些部分仍维护着指向该对象的指针。程序的任何部分都不再引用未使用的对象或未引用的对象。因此，可以回收未引用对象使用的内存。

垃圾回收的最大优点是，它减轻了我们手动分配/释放内存的负担，因此我们可以专注于解决手头的问题。

### **Q3。是否存在垃圾回收的缺点?**[](#q3-are-there-any-disadvantages-of-garbage-collection)

是。每当垃圾收集器运行时，它都会影响应用程序的性能。这是因为必须停止应用程序中的所有其他线程，以允许垃圾回收器线程有效地完成其工作。

根据应用程序的要求，这可能是客户无法接受的实际问题。但是，通过熟练的优化和垃圾收集器调整以及使用不同的GC算法，可以大大减少甚至消除此问题。

### **Q4。“Stop-The-World”一词的含义是什么?**[](#q4-what-is-the-meaning-of-the-term-stop-the-world)

当垃圾收集器线程正在运行时，其他线程也会停止，这意味着应用程序会立即停止。这类似于房屋清洁或熏蒸，在此过程完成之前，居民不得进入。


根据应用程序的需求，“Stop-The-World”垃圾收集可能会导致无法接受的冻结。这就是为什么进行垃圾收集器优化和JVM优化以使遇到的冻结至少可以接受的原因很重要。

### **Q5。什么是堆栈和堆?这些存储器结构中的每一个存储什么，以及它们如何相互关联?**[](#q5-what-are-stack-and-heap-what-is-stored-in-each-of-these-memory-structures-and-how-are-they-interrelated)

堆栈是内存的一部分，其中包含有关嵌套方法调用的信息，这些信息直到程序中的当前位置。它还包含所有局部变量和对当前执行的方法中定义的堆上对象的引用。

这种结构允许运行时从知道调用地址的地址的方法返回，并在退出方法后清除所有局部变量。每个线程都有自己的堆栈。

堆是用于分配对象的大量内存。使用_new_关键字创建对象时，该对象将在堆上分配。但是，对该对象的引用仍然存在于堆栈中。

### **Q6。什么是分代垃圾收集?什么使它成为流行的垃圾收集方法?**[](#q6-what-is-generational-garbage-collection-and-what-makes-it-a-popular-garbage-collection-approach)

可以将分代垃圾收集大致定义为垃圾收集器使用的策略，在该策略中，将堆分为称为“分代”的多个部分，每个部分将根据对象在堆上的“年龄”保存对象。

每当垃圾收集器运行时，过程的第一步称为标记。在这里，垃圾收集器会识别正在使用的内存块和未使用的内存块。如果必须扫描系统中的所有对象，这可能是一个非常耗时的过程。

随着分配的对象越来越多，对象列表越来越多，导致垃圾收集时间越来越长。但是，对应用程序的经验分析表明，大多数对象都是短暂的。

对于分代垃圾回收，根据对象的存活时间将其按照其“年龄”进行分组。这样，大部分工作分散在各个次要和主要的收集周期中。

今天，几乎所有垃圾收集器都是几代。这种策略之所以如此流行是因为随着时间的推移，它已被证明是最佳解决方案。

### **Q7。详细描述分代垃圾回收的工作方式**[](#q7-describe-in-detail-how-generational-garbage-collection-works)

为了正确理解分代垃圾回收的工作原理，重要的是首先**记住Java堆的结构**如何促进分代垃圾回收。

堆分划分位几个部分。分别是是年轻代，老年代以及永久代。


在**年轻代的主机大部分新创建的对象的**。对大多数应用程序的经验研究表明，大多数对象寿命短，因此很快就有资格进行收集。因此，新物体在这里开始其旅程，并且只有在达到一定的“年龄”后才被“提升”到老年代空间。

术语**“年龄”**在代垃圾回收**是指该对象已存活回收周期的数量**。

年轻代空间又分为三个空间：一个Eden空间和两个幸存者空间，例如Survivor 1(s1)和Survivor 2(s2)。

在**那个老年代主机的对象** **不再住在内存中超过一定的“年龄”**。幸免于年轻代垃圾收集的物体被提升到这个空间。它通常比年轻代大。由于垃圾收集的大小较大，因此与年轻代相比，垃圾收集更昂贵且发生频率更低。

的**永久代** **或更通常称为，_PermGen的，_包含由JVM所需的元数据**来描述应用程序使用的类和方法。它还包含用于存储内部字符串的字符串池。它由JVM在运行时根据应用程序使用的类来填充。另外，平台库类和方法可以存储在这里。

首先，将**任何新对象分配给Eden空间**。两个幸存者空间开始都是空的。当Eden空间填满时，将触发次要垃圾回收。引用的对象将移动到第一个幸存者空间。未引用的对象将被删除。

在下一个次要GC期间，伊甸园空间也会发生同样的事情。删除未引用的对象，并将引用的对象移到幸存者空间。然而，在这种情况下，它们被移动到第二幸存者空间(S2)。

另外，来自第一个幸存者空间(S1)中最后一个次要GC的对象的年龄增加，并移动到S2。将所有尚存的对象移至S2之后，将清除S1和Eden空间。此时，S2包含具有不同年龄的对象。

在下一个次要GC中，重复相同的过程。但是，这次幸存者空间切换了。引用的对象从Eden和S2都移到S1。幸存的对象会老化。Eden和S2被清除。

在每个次要垃圾回收周期之后，将检查每个对象的寿命。那些达到某个任意年龄(例如8)的对象从年轻代晋升为老年代。对于随后的所有minor GC周期，将继续将对象提升到旧空间。

这几乎耗尽了年轻代中垃圾收集的过程。最终，将对老年代进行大规模的垃圾收集，以清理并压缩该空间。对于每个major GC，都有几个minor GC。


### **Q8。什么时候对象才有资格进行垃圾收集?描述Gc如何收集合格对象?**[](#q8-when-does-an-object-become-eligible-for-garbage-collection-describe-how-the-gc-collects-an-eligible-object)

如果无法通过任何活动线程或任何静态引用访问该对象，则该对象可以进行垃圾回收或GC。

对象最有资格进行垃圾回收的最直接的情况是，如果其所有引用均为null。没有任何实时外部引用的循环依赖项也可以使用GC。因此，如果对象A引用对象B而对象B引用对象A，并且它们没有任何其他实时引用，则对象A和B都将有资格进行垃圾回收。

另一个明显的情况是将父对象设置为null。当一个厨房对象内部引用一个冰箱对象和一个水槽对象，并且该厨房对象设置为null时，冰箱和水槽都将与父厨房一起进行垃圾收集。

### **Q9。如何从Java代码触发垃圾回收?**[](#q9-how-do-you-trigger-garbage-collection-from-java-code)

**作为Java程序员，您不能在Java中强制进行垃圾回收**；仅当JVM认为它需要基于Java堆大小的垃圾回收时才会触发。

在从内存中删除对象之前，垃圾回收线程会调用该对象的finalize()方法，并提供执行所需的各种清理的机会。您也可以调用目标代码的此方法，但是，不能保证调用此方法时将发生垃圾回收。

此外，还有诸如System.gc()和Runtime.gc()之类的方法，这些方法用于将垃圾收集请求发送到JVM，但不能保证会发生垃圾收集。

### **Q10。当没有足够的堆空间来容纳新对象时会发生什么?**[](#q10-what-happens-when-there-is-not-enough-heap-space-to-accommodate-storage-of-new-objects)

如果在Heap中没有用于创建新对象的内存空间，则Java虚拟机将抛出_OutOfMemoryError_或更确切地说是**_java.lang.OutOfMemoryError_****堆空间。**

### **Q11。是否有可能“复活”成为垃圾收集对象的对象?**[](#q11-is-it-possible-to-resurrect-an-object-that-became-eligible-for-garbage-collection)

当某个对象可以进行垃圾回收时，GC必须在其上运行_finalize_方法。在_finalize_方法为该对象打上Gc标识，直到下一个周期回收。

在_finalize_方法中，您可以从技术上“复活”对象，例如，通过将其分配给_静态_字段。该对象将再次变为活动状态，并且不符合垃圾收集的条件，因此GC将不会在下一个周期中对其进行收集。

但是，该对象将被标记为finalize，因此当它再次可回收时，将不会调用finalize方法。从本质上讲，您可以在对象的整个生命周期中仅一次旋转此“复活”技巧。请注意，只有在您真正知道自己在做什么的情况下，才应使用此丑陋的技巧-但是，了解此技巧可以使您对GC的工作原理有一些了解。

### **Q12。描述强，弱，软和幻影引用及其在垃圾收集中的作用。**[](#q12-describe-strong-weak-soft-and-phantom-references-and-their-role-in-garbage-collection)

与使用Java管理内存一样，工程师可能需要在关键应用程序中执行尽可能多的优化，以最大程度地减少延迟并最大化吞吐量。尽管**无法明确控制何时**在JVM中**触发垃圾回收**，**但对于我们创建的对象来说，有可能影响****垃圾回收的****发生方式。**


Java为我们提供了参考对象，以控制我们创建的对象与垃圾收集器之间的关系。

默认情况下，我们在Java程序中创建的每个对象都由变量强引用：
```
StringBuilder sb = new StringBuilder();
```

在以上代码段中，_new_关键字创建一个新的_StringBuilder_对象并将其存储在堆中。然后，变量_sb_存储对该对象的**强引用**。对于垃圾收集器来说，这意味着特定的_StringBuilder_对象由于_sb_对它的强烈引用而根本不符合收集条件。只有当我们这样使_sb_无效时，故事才会改变：

```
sb = null;
```
调用上述行后，该对象将有资格进行回收。

我们可以通过将对象显式包装在位于_java.lang.ref_包内的另一个引用对象中，来更改对象与垃圾收集器之间的关系。

可以为上述对象创建一个**软引用**，如下所示：
```
StringBuilder sb = new StringBuilder();
SoftReference<StringBuilder> sbRef = new SoftReference<>(sb);
sb = null;
```

在上面的代码片段中，我们创建了对_StringBuilder_对象的两个引用。第一行创建一个**强引用** _sb_，第二行创建一个**软引用** _sbRef_。第三行应该使对象符合收集条件，但是由于_sbRef_，垃圾收集器将推迟收集_对象_。

只有在内存变紧并且JVM即将抛出_OutOfMemory_错误时，故事才会改变。换句话说，只回收具有软引用的对象是恢复内存的最后手段。

**弱引用**可以使用类似的方式来创建_的WeakReference_类。当_sb_设置为null且_StringBuilder_对象仅具有弱引用时，JVM的垃圾收集器将完全没有妥协，并在下一个周期立即收集该对象。

**幻象参考**类似于弱引用，并用仅虚引用的对象将无需等待被收集。但是，幻影引用在其对象被收集后就立即入队。我们可以轮询参考队列以确切了解对象何时被收集。

### **Q13。假设我们有一个循环引用(两个互相引用的对象)。这样的对象可以成为垃圾收集的资格吗?为什么?**[](#q13-suppose-we-have-a-circular-reference-two-objects-that-reference-each-other-could-such-pair-of-objects-become-eligible-for-garbage-collection-and-why)

是的，一对具有循环引用的对象可以进行垃圾回收。这是因为Java的垃圾收集器如何处理循环引用。它不考虑对象是否存在，只要它们有任何引用，而是通过从某个垃圾回收根(活动线程或静态字段的局部变量)开始导航对象图来确定它们是否存在。如果无法从任何根目录访问具有循环引用的一对对象，则认为该对象可以进行垃圾回收。

### **Q14。字符串在内存中如何表示?**[](#q14-how-are-strings-represented-in-memory)

字符串_在Java实例是具有两个字段的对象：一个char[] value 和_int hash field。value是表示字符串本身字符数组，hash包含 字符串的hashCode_其被初始化为零，如果字符串的_hashCode_值为零，则每次调用_hashCode()时_都必须重新计算它。

重要的是_String_实例是不可变的：您无法获取或修改char[] value 。字符串的另一个功能是将静态常量字符串加载并缓存在字符串池中。如果源代码中有多个相同的_String_对象，则它们在运行时都由单个实例表示。

### **Q15。什么是Stringbuilder及其用例?将字符串附加到Stringbuilder和使用+运算符连接两个字符串之间有什么区别?Stringbuilder与Stringbuffer有何不同?**[](#q15-what-is-a-stringbuilder-and-what-are-its-use-cases-what-is-the-difference-between-appending-a-string-to-a-stringbuilder-and-concatenating-two-strings-with-a--operator-how-does-stringbuilder-differ-from-stringbuffer)

_StringBuilder_允许通过追加，删除和插入字符和字符串来操纵字符序列。与不可变的_String_类相反，这是一种可变的数据结构。

连接两个_String_实例时，将创建一个新对象，并复制字符串。如果我们需要在循环中创建或修改字符串，这可能会带来巨大的垃圾回收器开销。_StringBuilder_允许更有效地处理字符串操作。

_StringBuffer的_和_的StringBuilder_不同，它是线程安全的。如果需要在单个线程中处理字符串，请改用_StringBuilder_。

**3.结论**[](#conclusion)
-----------------------

在本文中，我们讨论了Java工程师访谈中经常出现的一些最常见的问题。有关内存管理的问题通常是针对高级Java Developer候选人的，因为面试官希望您已经构建了很多琐碎的应用程序，而这些应用程序经常受到内存问题的困扰。

这不应被视为详尽的问题清单，而应作为进一步研究的起点。我们祝您在接下来的面试中取得成功。
