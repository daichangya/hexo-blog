---
title: Java虚拟机（JVM）的Java内存管理
id: 1332
date: 2024-10-31 22:01:51
author: daichangya
excerpt: Java内存管理是一项持续的挑战，并且是必须掌握的技能，才能正确调整可扩展功能的应用程序。从根本上讲，这是分配新对象并正确删除未使用对象的过程。在本文中，我们将讨论Java虚拟机（JVM），了解内存管理，内存监视工具，内存使用情况监视和垃圾回收（GC）活动。正如您将看到的，有许多不同的模型，方法，工
permalink: /archives/Java-xu-ni-ji-JVM-de-Java-nei-cun-guan/
categories:
- jvm
---

Java内存管理是一项持续的挑战，并且是必须掌握的技能，才能正确调整可扩展功能的应用程序。从根本上讲，这是分配新对象并正确删除未使用对象的过程。

在本文中，我们将讨论Java虚拟机（JVM），了解内存管理，内存监视工具，内存使用情况监视和垃圾回收（GC）活动。

正如您将看到的，有许多不同的模型，方法，工具和技巧可用于真正优化。

### Java虚拟机（JVM）

JVM是使计算机能够运行Java程序的抽象计算机。JVM有三种概念： **规范** （指定JVM的工作方式。但是实现已由Sun和其他公司提供）， **实现** （称为（JRE）Java Runtime Environment）和 **实例** （在编写Java命令之后运行） Java类，将创建JVM的实例）。

JVM加载代码，验证代码，执行代码，管理内存（这包括从操作系统（OS）分配内存，管理Java分配，包括堆压缩和垃圾对象的删除），并最终提供运行时环境。

#### **Java（JVM）内存结构**

JVM内存分为多个部分：堆内存，非堆内存和其他。

 ![](https://betsol.com/wp-content/uploads/2017/06/JVM-Memory-Model.jpg) 

 ![](https://betsol.com/wp-content/uploads/2017/06/JVM-Memory-Model.jpg) 

图1.1来源[https://www.yourkit.com/docs/kb/sizes.jsp](https://www.yourkit.com/docs/kb/sizes.jsp)

#### **堆内存**

堆内存是运行时数据区，从中分配了所有java类实例和数组的内存。JVM启动时会创建堆，并且在应用程序运行时堆的大小可能会增加或减少。可以使用–Xms VM选项指定堆的大小。堆可以是固定大小的，也可以是可变大小的，具体取决于垃圾回收策略。可以使用–Xmx选项设置最大堆大小。默认情况下，最大堆大小设置为64 MB。

#### **非堆内存**

JVM具有堆以外的内存，称为非堆内存。它是在JVM启动时创建的，并存储每个类的结构，例如运行时常量池，字段和方法数据，方法和构造函数的代码以及内部字符串。非堆内存的默认最大大小为64 MB。可以使用–XX：MaxPermSize VM选项更改。

#### **其他记忆**

JVM使用此空间存储JVM代码本身，JVM内部结构，已加载的探查器代理代码和数据等。

#### **Java（JVM）堆内存结构**

 ![](https://betsol.com/wp-content/uploads/2017/06/java-memory-management-1.jpg) 

 ![](https://betsol.com/wp-content/uploads/2017/06/java-memory-management-1.jpg) 

图1.2来源 [http://www.journaldev.com/2856/java-jvm-memory-model-memory-management-in-java](http://www.journaldev.com/2856/java-jvm-memory-model-memory-management-in-java)

JVM堆在物理上分为两部分（或几代）： _托儿所_ （或 _年轻空间/年轻一代_）和 _旧空间_ （或 _旧一代_）。

托儿所是为分配新对象而保留的堆的一部分。当托儿所变满时，将通过运行特殊的_年轻集合_来收集垃圾，其中将在托儿所中生活了足够长的所有对象提升（移动）到旧空间，从而腾出了托儿所用于更多对象分配。此垃圾回收称为 **Minor GC**。托儿所分为三个部分– **伊甸园记忆区** 和两个 **幸存者记忆** 空间。

有关育儿空间的要点：

*   大多数新创建的对象位于Eden内存空间中
*   当伊甸园空间中充满对象时，将执行次要GC，并将所有幸存者对象移至其中一个幸存者空间
*   次要GC还可以检查幸存者对象并将其移动到其他幸存者空间。因此，一次，幸存者空间始终是空的
*   在许多GC循环中幸存下来的对象将移至旧的内存空间。通常，可以通过设置苗圃对象的年龄阈值，然后再有资格晋升为老一代

当旧一代内存已满时，将在此处收集垃圾，该过程称为旧集合。上一代存储器包含经过多次次要次要GC寿命长且可以存活的对象。通常，垃圾回收已满时在旧代内存中执行。较旧的垃圾回收称为**专业GC**，通常需要更长的时间。苗圃背后的原因是，大多数物体都是临时的且寿命短。一个年轻的收藏旨在迅速找到仍然活着的新分配对象并将其移出苗圃。通常，年轻的集合释放给定数量的内存比单代堆（没有托儿所的堆）的旧集合或垃圾回收要快得多。

最新版本包括称为_保管区_的托儿所的一部分，  并且已保留。保留区域包含托儿所中最近分配的对象，直到下一代出现时才进行垃圾收集。这样可以防止仅由于在开始年轻收集之前就已分配了对象而对其进行升级。

### Java内存模型

#### **永久生成（从Java 8开始由Metaspace代替）**

永久生成或“ Perm Gen”包含JVM所需的应用程序元数据，用于描述应用程序中使用的类和方法。JVM在运行时根据应用程序使用的类填充PermGen。Perm Gen还包含Java SE库类和方法。Perm Gen对象是在完整垃圾收集中收集的垃圾。

#### **元空间**

在Java 8中，没有Perm Gen，这意味着不再有“ java.lang.OutOfMemoryError：PermGen”空间问题。与驻留在Java堆中的Perm Gen不同，Metaspace不是堆的一部分。现在，类元数据的大多数分配都是从本机内存中分配的。默认情况下，元空间会自动增加其大小（达到基础操作系统所提供的大小），而Perm Gen始终具有固定的最大大小。可以使用两个新标志来设置元空间的大小，它们是：“ **\-XX：MetaspaceSize** ”和“ **\-XX：MaxMetaspaceSize** ”。Metaspace背后的主题是类及其元数据的生存期与类加载器的生存期匹配。也就是说，只要类加载器处于活动状态，元数据就在Metaspace中保持活动状态，并且无法释放。

#### **代码缓存**

运行Java程序时，它将以分层方式执行代码。在第一层中，它使用客户端编译器（C1编译器）以便通过检测来编译代码。分析数据在第二层（C2编译器）中用于服务器编译器，以优化的方式编译该代码。默认情况下，Java 7中未启用分层编译，而Java 8中已启用分层编译。

即时（JIT）编译器将编译后的代码存储在称为代码缓存的区域中。这是一个特殊的堆，用于存放已编译的代码。如果该区域的大小超过阈值，则将刷新该区域，并且GC无法重新定位这些对象。

Java 8中已解决了一些性能问题和编译器未重新启用的问题，而在Java 7中避免这些问题的解决方案之一是将代码缓存的大小增加到一个永远无法达到的程度。

#### **方法范围**

方法区域是Perm Gen中空间的一部分，用于存储类结构（运行时常量和静态变量）以及方法和构造函数的代码。

#### **内存池**

内存池是由JVM内存管理器创建的，用于创建不可变对象的池。内存池可以属于Heap或Perm Gen，具体取决于JVM内存管理器的实现。

#### **运行时常量池**

运行时常量池是类中常量池的每类运行时表示形式。它包含类运行时常量和静态方法。运行时常量池是方法区域的一部分。

#### **Java堆栈内存**

Java堆栈内存用于执行线程。它们包含短期的特定于方法的值以及对从该方法引用的堆中其他对象的引用。

#### **Java堆内存开关**

Java提供了很多内存开关，我们可以用来设置内存大小及其比率。一些常用的内存开关是：

| VM切换器           | VM切换器说明                                                                                               |
|-----------------|-------------------------------------------------------------------------------------------------------|
| – Xms           | 用于在JVM启动时设置初始堆大小                                                                                      |
| \-Xmx           | 用于设置最大堆大小                                                                                             |
| \-Xmn           | 为了确定年轻一代的大小，其余空间留给了老一代                                                                                |
| \-XX：PermGen    | 用于设置永久存储器的初始大小                                                                                        |
| \-XX：MaxPermGen | 用于设置Perm Gen的最大大小                                                                                     |
| \-XX：幸存者比率      | 为了提供Eden空间的比例，例如，如果年轻一代的大小为10m，并且VM切换器为–XX：SurvivorRatio = 2，则将为Eden空间保留5m，为两个Survivor空间保留2\.5m。默认值为8 |
| \-XX：NewRatio   | 用于提供新旧大小的比例。默认值为2                                                                                     |


### 垃圾收集

垃圾回收是释放堆中空间以分配新对象的过程。Java的最佳功能之一是自动垃圾收集。垃圾收集器是在后台运行的程序，它可以查看内存中的所有对象并找出程序的任何部分未引用的对象。删除所有这些未引用的对象，并回收空间以分配给其他对象。垃圾收集的基本方法之一涉及三个步骤：

*   **标记**：这是第一步，垃圾回收器将识别正在使用的对象和未使用的对象
*   **正常删除**：垃圾收集器删除未使用的对象并回收要分配给其他对象的可用空间
*   **压缩压缩**：为了获得更好的性能，在删除未使用的对象之后，可以将所有剩余的对象移动到一起。这将提高内存分配给较新对象的性能

### 垃圾收集的标记和扫描模型

JVM使用标记和清除垃圾收集模型来执行整个堆的垃圾收集。标记和清除垃圾收集包含两个阶段，标记阶段和清除阶段。

在标记阶段，将从Java线程，本机处理程序和其他根源可访问的所有对象以及从这些对象可访问的对象等标记为活动。此过程将识别并标记所有仍在使用的对象，其余的可以视为垃圾。

在清除阶段，遍历堆以查找活动对象之间的间隙。这些间隙记录在空闲列表中，可用于新对象分配。

#### **Java垃圾回收类型**

我们可以在应用程序中使用五种类型的垃圾收集类型。我们只需要使用JVM开关来为应用程序启用垃圾回收策略即可。

**串行GC（-XX：+ UseSerialGC）**：串行GC使用简单的mark-sweep-compact方法进行年轻一代和老一代的垃圾回收，即次要和主要GC

要启用串行收集器，请使用：

\-XX：+ UseSerialGC

**并行GC（-XX：+ UseParallelGC）**：并行GC与串行GC相同，不同之处在于，它生成N个线程用于年轻一代垃圾回收，其中N是系统中CPU内核的数量。我们可以使用**–XX：ParallelGCThreads = n** JVM选项来控制线程数 。这是JDK 8中JVM的默认收集器

要启用并行GC，请使用：

\-XX：+ UseParallelGC

**并行旧GC（-XX：+ UseParallelOldGC）**：与并行GC相同，只是它使用多个线程进行年轻代和旧代垃圾回收

要启用并行OLDGC，请使用：

\-XX：+ UseParallelOldGC

**并发标记扫描（CMS）收集器（-XX：+ UseConcMarkSweepGC）**：CMS也称为并发低暂停收集器。它为老一代进行垃圾收集。CMS收集器试图通过在应用程序线程中同时执行大多数垃圾收集工作来最大程度地减少由于垃圾收集而造成的暂停。年轻一代的CMS收集器使用与并行收集器相同的算法。此垃圾收集器适用于响应性应用程序，在这些应用程序中我们无法承受更长的暂停时间。我们可以使用**–XX：ParallelCMSThreads = n** JVM选项来限制CMS收集器中的线程数。

要启用CMS收集器，请使用：

\-XX：+ UseConcMarkSweepGC

**G1垃圾收集器（-XX：+ UseG1GC）**：Java 7中提供了垃圾优先或G1垃圾收集器，其长期目标是替换CMS收集器。G1收集器是一个并行，并发且增量紧凑的低中断垃圾收集器。垃圾优先收集器不能像其他收集器那样工作，也没有年轻一代空间的概念。它将堆空间分成多个相等大小的堆区域。调用垃圾收集器时，它将首先收集活动数据较少的区域，因此称为“垃圾优先”。

要启用G1收集器，请使用：

\-XX：+ UseG1GC

计划将G1作为并发标记扫描收集器（CMS）的长期替代产品。将G1与CMS进行比较，有一些差异使G1成为更好的解决方案。一个区别是G1是压紧收集器。G1足够紧凑，可以完全避免使用细粒度的空闲列表进行分配，而是依赖于区域。这大大简化了收集器的各个部分，并消除了潜在的碎片问题。同样，G1提供了比CMS收集器更可预测的垃圾收集暂停，并允许用户指定所需的暂停目标。

在Java 8中，G1收集器具有惊人的优化功能，即**String Deduplication**。它使GC能够识别在堆中多次出现的字符串，并修改它们以指向同一内部char \[\]数组，从而使堆中没有多个副本。可以使用-XX：+ UseStringDeduplication JVM启用它。论点。

G1是**JDK 9中**的**默认**垃圾收集器**。**

#### **使用案例**

超过50％的Java堆被实时数据占用。

对象分配率或提升率差异很大。

不必要的长时间垃圾收集或压缩暂停（长于0.5到1秒）

### 监视内存使用和GC活动

内存不足通常是Java应用程序不稳定和无响应的原因。因此，我们需要监视垃圾收集对响应时间和内存使用的影响，以确保稳定性和性能。但是，仅监视这两个元素并不能告诉我们应用程序响应时间是否受垃圾收集影响，因此监视内存利用率和垃圾收集时间是不够的。只有GC挂起会直接影响响应时间，并且GC也可以与应用程序并行运行。因此，我们需要将垃圾收集导致的暂停与应用程序的响应时间相关联。基于此，我们需要监视以下内容：

*   利用不同的内存池（Eden，Survivor和旧一代）。内存不足是增加GC活动的第一原因
*   如果尽管进行了垃圾回收，但总体内存利用率仍在不断提高，则存在内存泄漏，这将不可避免地导致 **内存不足**。在这种情况下，必须进行内存堆分析
*   年轻一代收藏的数量提供了有关流失率（对象分配率）的信息。数字越高，分配的对象越多。大量的年轻藏品可能是响应时间问题和老一辈人成长的原因（因为年轻一代无法再应付大量物品）
*   如果在GC之后老一代的利用率波动很大而又没有上升，则对象会不必要地从年轻一代复制到老一代。可能有以下三个原因：年轻一代太小，流失率高或事务性内存使用过多
*   高GC活动通常会对CPU使用率产生负面影响。但是，只有暂停（停止世界事件）会直接影响响应时间。与大众观点相反，停赛不限于主要GC。因此，重要的是要监视与应用程序响应时间相关的挂起

#### **jstat**

该_jstat_工具使用内置在Java HotSpot虚拟机的仪器，提供有关运行应用程序的性能和资源消耗的信息。诊断性能问题，尤其是与堆大小和垃圾回收有关的问题时，可以使用该工具。该_jstat_实用程序不需要虚拟机与任何特殊的选项启动。默认情况下，Java HotSpot VM中的内置工具是启用的。该实用程序包含在所有操作系统的JDK下载中。所述_jstat_实用程序使用所述虚拟机标识符（VMID）来识别目标的过程。

使用带有gc选项的_jstat_命令来查找JVM堆内存使用情况。

_<JAVA\_HOME> / bin / jstat –gc <JAVA\_PID>_

 ![](https://betsol.com/wp-content/uploads/2017/06/java-home.jpg) 

 ![](https://betsol.com/wp-content/uploads/2017/06/java-home.jpg) 

图1.3

| S0C  | Current survivor space 0 capacity \(KB\)             |
|------|------------------------------------------------------|
| S1C  | Current survivor space 1 capacity \(KB\)             |
| S0U  | Survivor space 0 utilization \(KB\)                  |
| S1U  | Survivor space 1 utilization \(KB\)                  |
| EC   | Current eden space capacity \(KB\)                   |
| EU   | Eden space utilization \(KB\)                        |
| OC   | Current old space capacity \(KB\)                    |
| OU   | Old space utilization \(KB\)                         |
| MC   | Metasapce capacity \(KB\)                            |
| MU   | Metaspace utilization \(KB\)                         |
| CCSC | Compressed class space capacity \(KB\)               |
| CCSU | Compressed class space used \(KB\)                   |
| YGC  | Number of young generation garbage collection events |
| YGCT | Young generation garbage collection time             |
| FGC  | Number of full GC events                             |
| FGCT | Full garbage collection time                         |
| GCT  | Total garbage collection time                        |

表1.2

#### **jmap**

该_JMAP_实用程序针对运行中的VM或核心文件的存储相关的统计信息。JDK 8引入了Java Mission Control，Java Flight Recorder和_jcmd_实用程序，用于诊断JVM和Java应用程序的问题。建议使用最新的实用程序_jcmd_代替_jmap_实用程序，以增强诊断功能并降低性能开销。

–heap选项可用于获取以下Java堆信息：

*   GC算法特定的信息，包括GC算法的名称（例如，并行GC）和特定于算法的详细信息（例如，并行GC的线程数）。
*   堆配置可能已被指定为命令行选项或由VM根据计算机配置选择。
*   堆使用情况摘要：对于每一代（堆的区域），该工具都会显示堆的总容量，使用中的内存和可用的可用内存。如果将一个世代组织为一组空间（例如，新一代），则将包括一个特定于空间的内存大小摘要。

_<JAVA\_HOME> / bin / jmap –heap <JAVA\_PID>_

 ![](https://betsol.com/wp-content/uploads/2017/06/java-process.jpg) 

 ![](https://betsol.com/wp-content/uploads/2017/06/java-process.jpg) 

图1.4

#### **jcmd**

该_jcmd_工具被用来发送诊断命令请求到JVM，这些请求是控制Java的飞行录像，排查有用的，诊断JVM和Java应用程序。它必须在运行JVM的同一台计算机上使用，并且必须具有用于启动JVM的相同有效用户和组标识符。

可以使用以下命令创建堆转储（hprof转储）：

_jcmd <JAVA\_PID> GC.heap\_dump filename = <文件>_

上面的命令与使用相同

_jmap –dump：file = <文件> <JAVA\_PID>_

但是_jcmd_是推荐使用的工具。

#### **jhat**

在_与jHat_工具提供了一个方便的手段来浏览对象拓扑在堆快照。该工具替代了堆分析工具（HAT）。该工具以二进制格式解析堆转储（例如，_jcmd_产生的堆转储）。该实用程序可以帮助调试**意外对象关系**。该术语用于描述不再需要的对象，但由于通过根集中的某些路径进行引用而使该对象保持活动状态。例如，如果在不再需要该对象之后仍然保留了对该对象的无意识静态引用，或者在不再需要该对象时观察者或侦听器无法从其对象注销自己，或者引用了该对象的线程，则可能会发生这种情况。对象在应有的情况下不会终止。意外对象关系是Java语言的内存泄漏等效项。

我们可以使用以下命令使用_jhat_分析堆转储

_jhat <HPROF\_FILE>_

此命令读取.hprof文件并在端口7000上启动服务器。

 ![](https://betsol.com/wp-content/uploads/2017/06/java-port-7000.jpg) 

 ![](https://betsol.com/wp-content/uploads/2017/06/java-port-7000.jpg) 

图1.5

当我们使用[http：// localhost：7000](http://localhost:7000)连接到服务器时[](http://localhost:7000)，我们可以执行标准查询或创建对象查询语言（OQL）。默认情况下显示“所有类”查询。该默认页面显示堆中存在的所有类，平台类除外。该列表按完全限定的类名排序，并按包分类。单击一个类的名称以转到“类”查询。此查询的第二个变体包括平台类。平台类包括其完全限定名称以诸如java，sun或javax.swing之类的前缀开头的类。另一方面，类查询显示有关类的信息。这包括其超类，任何子类，实例数据成员和静态数据成员。在此页面上，您可以导航到所引用的任何类，也可以导航至实例查询。

#### **HPROF**

HPROF是每个JDK版本附带的用于堆和CPU性能分析的工具。它是一个动态链接库（DLL），它使用Java虚拟机工具接口（JVMTI）与JVM接口。该工具以ASCII或二进制格式将概要分析信息写入文件或套接字。HPROF工具能够显示CPU使用率，堆分配统计信息并监视争用概要文件。另外，它可以报告完整的堆转储以及JVM中所有监视器和线程的状态。在诊断问题方面，HPROF在分析性能，锁争用，内存泄漏和其他问题时很有用。

我们可以使用以下命令调用HPROF工具：

_java –agentlib：hprof ToBeProfiledClass_

_java –agentlib：hprof = heap = sites ToBeProfiledClass_

根据请求的分析类型，HPROF指示JVM将其发送到相关事件。然后，该工具将事件数据处理为配置文件信息。默认情况下，堆分析信息被写到当前工作目录中的java.hprof.txt（ASCII）。

以下命令

_javac –J-agentlib：hprof = heap = sites Hello.java_

可用于获取堆分配配置文件。堆概要文件中的关键信息是程序各个部分中发生的分配量。

同样，可以使用_heap = dump_选项获得_堆转储_。输出

_javac –J-agentlib：hprof = heap = dump Hello.java_

包括由垃圾收集器确定的根集，以及可以从根集访问的堆中每个Java对象的条目。

HPROF工具可以通过采样线程来收集CPU使用率信息。

以下命令可用于获取CPU使用率采样概要文件结果：

_javac –J-agentlib：hprof = cpu = samples Hello.java_

HPROF代理会定期对所有正在运行的线程的堆栈进行采样，以记录最频繁的活动堆栈跟踪。

还有其他工具，例如VisualVM，它以GUI的形式向我们提供了内存使用情况，垃圾回收，堆转储，CPU和内存分析等详细信息。

#### **虚拟机**

VisualVM是从NetBeans平台派生的工具，其体系结构在设计上是模块化的，这意味着很容易通过使用插件进行扩展。当Java应用程序在JVM上运行时，VisualVM允许我们获取有关Java应用程序的详细信息，它可以在本地或远程系统中。可以使用Java开发工具包（JDK）工具检索生成的数据，并且可以快速查看本地和远程运行的应用程序上多个Java应用程序上的所有数据和信息。也可以保存和捕获有关JVM软件的数据，并将数据保存到本地系统。VisualVM可以执行CPU采样，内存采样，运行垃圾回收，分析堆错误，创建快照等等。

#### **启用JMX端口**

我们可以通过在启动Java应用程序时添加以下系统属性来启用JMX远程端口：

*   \-Dcom.sun.management.jmxremote
*   \-Dcom.sun.management.jmxremote.port = <端口>
*   \-Dcom.sun.management.jmxremote。

现在，我们可以使用VisualVM连接到远程计算机，并查看CPU利用率，内存采样，线程等。通过JMX远程端口连接时，我们还可以在远程计算机上生成线程转储和内存转储。

图1.6显示了在本地和远程系统上运行的应用程序列表。要连接到远程系统，请右键单击“远程”并添加主机名，然后在“高级设置”下定义在远程计算机上启动应用程序时使用的端口。一旦在本地或远程部分下列出了应用程序，请双击它们以查看应用程序的详细信息。

 ![](https://betsol.com/wp-content/uploads/2017/06/java-memory-management-2.jpg) 

 ![](https://betsol.com/wp-content/uploads/2017/06/java-memory-management-2.jpg) 

图1.6

该应用程序的详细信息有四个选项卡：“概述”，“监视器”，“线程”和“采样器”。

在 **概述** 选项卡包含有关启动的应用程序的主要信息。概述选项卡中提供了主类，命令行参数，JVM参数，PID，系统属性以及任何已保存的数据（例如线程转储或堆转储）。

有趣的选项卡是“ **监视”** 选项卡。此选项卡显示应用程序的CPU和内存使用情况。此视图中有四个图形。

 ![](https://betsol.com/wp-content/uploads/2017/06/java-memory-management-3.jpg) 

 ![](https://betsol.com/wp-content/uploads/2017/06/java-memory-management-3.jpg) 

图1.7

第一个图显示CPU使用率和垃圾收集器CPU使用率。X轴显示时间戳与利用率的百分比。

右上方的第二个图显示堆空间和Perm Gen空间或元空间。它还显示堆内存的最大大小，应用程序正在使用的内存量以及可用的内存量。该图在分析遇到**java.lang.OutOfMemoryError：Java堆空间的 **应用程序中特别有用错误。当应用程序正在执行内存密集型作业时，已使用的堆（在图上以蓝色表示）应始终小于堆大小（在图上以橙色表示）。当使用的堆与堆大小几乎相同时，或者当没有更多空间供系统分配/扩展堆大小并且使用的堆不断增加时，我们可以预料到堆错误。可以通过“堆转储”获取有关堆的更多信息。当出现内存不足错误时，可以通过添加流动的VM参数来获得堆转储：

**\-XX：+ HeapDumpOnOutOfMemoryError –XX：HeapDumpPath = \[文件路径\]**

这将使 **.hprof** 文件可以在指定的路径中创建。

 ![](https://betsol.com/wp-content/uploads/2017/06/java-memory-management-4.jpg) 

 ![](https://betsol.com/wp-content/uploads/2017/06/java-memory-management-4.jpg) 

图1.8

图1.8显示了其中一个应用程序的堆转储。摘要选项卡显示一些基本信息，例如类总数，实例总数，类加载器，GC根目录以及应用程序运行所在的环境详细信息。图1.8中的分析显示了分配最多的对象类型以及发生这些分配的位置。大型对象会在其构造函数中创建许多其他对象，或者具有许多字段。我们还应该分析在生产条件下大规模并发的代码区域。在负载下，这些位置不仅会分配更多空间，而且还会增加内存管理本身的同步性。高内存利用率是导致大量垃圾回收的原因。在某些情况下，硬件限制使得不可能简单地增加JVM的堆大小。在其他情况下，增加堆大小并不能解决问题，只会延迟问题，因为利用率一直在增长。使用堆转储标识内存泄漏和标识内存消耗者，可以进行以下分析。

不再需要但仍被应用程序引用的每个对象都可以视为内存泄漏。实际上，我们只关心正在增长的或占用大量内存的内存泄漏。典型的内存泄漏是指重复创建指定的对象类型但不进行垃圾收集的泄漏。为了标识此对象类型，需要多个堆转储，可以使用趋势转储进行比较。每个Java应用程序都有大量的 **String**， **char \[\]** 和其他Java标准对象。实际上，String和char \[\]通常具有最多的实例数，但是分析它们将使我们无所适从。即使我们泄漏String对象，也很可能是因为它们被应用程序对象引用，这代表了泄漏的根本原因。因此，专注于我们的应用程序类别将产生更快的结果。

我们有几种情况需要详细分析。

*   趋势分析并没有导致我们内存泄漏
*   我们的应用程序使用了过多的内存，但是没有明显的内存泄漏，因此我们需要优化代码
*   我们无法进行趋势分析，因为内存增长过快并且JVM崩溃了

在所有三种情况下，根本原因很可能是一个或多个对象位于较大对象树的根目录。这些对象可防止垃圾回收树中的许多其他对象。如果发生内存不足错误，则少数对象可能会阻止释放大量对象，从而触发内存不足错误。堆的大小通常是内存分析的大问题。生成堆转储需要内存本身。如果堆大小处于可用或可能的限制（32位JVM不能分配超过3.5 GB），则JVM可能无法生成一个。另外，堆转储将挂起JVM。手动找到一个阻止整个对象树迅速被垃圾收集的对象成为大海捞针。

幸运的是，诸如Dynatrace之类的解决方案能够自动识别这些对象。为此，我们需要使用基于图论的控制算法。该算法应该能够计算对象树的根。除了计算对象树的根，内存分析工具还可以计算特定树的内存量。这样，它可以计算哪些对象阻止释放大量内存–换句话说，哪个对象主导内存。

 ![](https://betsol.com/wp-content/uploads/2017/06/java-memory-management-5.jpg) 

 ![](https://betsol.com/wp-content/uploads/2017/06/java-memory-management-5.jpg) 

图1.9

回到“监视器”选项卡下可用于应用程序的图（图1.7），是位于左下角的类图。该图显示了应用程序中加载的类的总数，最后一个图显示了当前正在运行的线程数。通过这些图，我们可以查看我们的应用程序是否占用了过多的CPU或内存。

第三个选项卡是“ **线程”** 选项卡。

 ![](https://betsol.com/wp-content/uploads/2017/06/java-memory-management-6.jpg) 

 ![](https://betsol.com/wp-content/uploads/2017/06/java-memory-management-6.jpg) 

图1.10

在“线程”选项卡中，我们可以看到应用程序的不同线程如何改变状态以及它们如何演化。我们还可以观察每个状态下的时间流逝以及有关线程的许多其他细节。有过滤选项可仅查看活动线程或完成线程。如果我们需要线程转储，则可以使用顶部的“线程转储”按钮获得它。

第四个选项卡是“ **采样器”**选项卡。最初打开此选项卡时，它不包含任何信息。在查看信息之前，我们必须开始一种采样/分析。我们将从CPU采样开始。单击“ CPU”按钮后，表中将显示CPU采样的结果。

 ![](https://betsol.com/wp-content/uploads/2017/06/java-memory-management-7.jpg) 

 ![](https://betsol.com/wp-content/uploads/2017/06/java-memory-management-7.jpg) 

图1.11

从图1.11中，我们看到**doRun（）** 方法占用了CPU时间的54.8％。我们还看到 **getNextEvent** **（）**和**readAvailableBlocking（）** 是接下来的两个消耗更多CPU时间的方法。

下一个采样是内存采样。采样期间将冻结应用程序，直到获取结果。从图1.12，我们可以推断出应用程序存储了**Object**， **int** 和 **char**数组 。

在这两种类型的采样中，我们都可以将结果保存起来，以备以后使用。例如，可以以固定间隔多次采样，然后可以比较结果。这可以帮助我们改进应用程序以使用更少的CPU和内存。最后，开发人员的任务是检查这些区域并改进代码。

 ![](https://betsol.com/wp-content/uploads/2017/06/java-memory-management-8.jpg) 

 ![](https://betsol.com/wp-content/uploads/2017/06/java-memory-management-8.jpg) 

### Java垃圾收集优化

Java垃圾回收优化应该是我们用于提高应用程序吞吐量的最后一个选择，并且仅当由于较长的GC导致应用程序超时而导致性能下降时才使用。

如果遇到 **java.lang.OutOfMemoryError：PermGen空间** 错误，请尝试使用**–XX：PermGen** 和 **–XX：MaxPermGen** JVM选项监视并增加Perm Gen的内存空间 。对于Java 8及更高版本，我们看不到此错误。如果我们看到很多完整的GC操作，则应尝试增加旧的内存空间。总体而言，垃圾回收调整需要大量的精力和时间，对此没有硬性规定。我们需要尝试不同的选择并进行比较，以找出最适合我们应用的选择。

一些性能解决方案是：

*   应用软件采样/分析
*   服务器和JVM调优
*   正确的硬件和操作系统
*   根据应用程序的行为和采样结果进行代码改进（说起来容易做起来难！）
*   正确使用JVM（具有最佳JVM参数）
*   \-XX：+ UseParallelGC（如果有多处理器）

请记住一些其他有用的技巧：

*   除非我们在暂停方面遇到问题，否则请尝试为JVM分配尽可能多的内存
*   将–Xms和–Xmx设置为相同的值
*   请确保随着我们增加处理器数量而增加内存，因为分配可以并行化
*   别忘了调整Perm Gen
*   最小化同步的使用
*   如果有好处，请使用多线程，并注意线程开销。另外，请确保它在不同环境中的工作方式相同
*   避免过早创建对象。创作应接近实际使用地点。这是一个我们容易忽视的基本概念
*   JSP通常比servlet慢
*   StringBuilder代替字符串concat
*   使用基元并避免对象。（长而不是长）
*   尽可能重用对象，并避免创建不必要的对象
*   如果我们要测试一个空字符串，equals（）会很昂贵。请改用length属性。
*   “ ==”比equals（）快
*   n + = 5快于n = n +5。在第一种情况下，生成的字节码更少
*   定期刷新并清除休眠会话
*   批量执行更新和删除

### **为GC生成日志**

垃圾收集器日志或gc.log是存储所有JVM内存清除事件的文本文件：MinorGC，MajorGC和FullGC。

使用以下参数启动JVM以创建gc.log：

**直到Java 8**

XX：+ PrintGCDetails -Xloggc：/app/tmp/myapp-gc.log

**从Java 9**

Xlog：gc \*：file = / app / tmp / myapp-gc.log

> ### 资料来源
> 
> > [https://docs.oracle.com/cd/E13150\_01/jrockit\_jvm/jrockit/geninfo/diagnos/garbage\_collect.html](https://docs.oracle.com/cd/E13150_01/jrockit_jvm/jrockit/geninfo/diagnos/garbage_collect.html)
> 
> > [https://zh.wikipedia.org/wiki/Java\_virtual\_machine](https://en.wikipedia.org/wiki/Java_virtual_machine)
> 
> > [https://www.javatpoint.com/internal-details-of-jvm](https://www.javatpoint.com/internal-details-of-jvm)
> 
> > [https://dzone.com/articles/java-performance-tuning](https://dzone.com/articles/java-performance-tuning)
> 
> > [http://www.journaldev.com/2856/java-jvm-memory-model-memory-management-in-java](http://www.journaldev.com/2856/java-jvm-memory-model-memory-management-in-java)
> 
> > [https://www.yourkit.com/docs/kb/sizes.jsp](https://www.yourkit.com/docs/kb/sizes.jsp)
> 
> > [https://www.infoq.com/articles/Java-PERMGEN-已移除](https://www.infoq.com/articles/Java-PERMGEN-Removed)
> 
> > [http://blog.andresteingress.com/2016/10/19/java-codecache](http://blog.andresteingress.com/2016/10/19/java-codecache)
> 
> > [https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/toc.html](https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/toc.html)
> 
> > [https://javaperformance.wordpress.com/2017/02/05/java-heap-memory-usage-using-jmap-and-jstat-command/](https://javaperformance.wordpress.com/2017/02/05/java-heap-memory-usage-using-jmap-and-jstat-command/)
