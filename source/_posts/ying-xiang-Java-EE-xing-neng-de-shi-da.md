---
title: 影响Java EE性能的十大问题
id: 1008
date: 2024-10-31 22:01:48
author: daichangya
excerpt: 本文作者是一名有10多年经验的高级系统架构师，他的主要专业领域是Java EE、中间件和JVM技术。他在性能优化和提升方面也有很深刻的见解，下面他将和大家分享一下常见的10个影响Java
  EE性能问题。1.缺乏正确的容量规划容量规划是一个全面的和发展的过程标准，预测当前和未来的IT环境容量需求。制定合理的容量规划不仅会确保和跟踪当前IT生产能力和稳定性，同时也会确保新项目以最小的风
permalink: /archives/ying-xiang-Java-EE-xing-neng-de-shi-da/
categories:
- java
---



本文作者是一名有10多年经验的高级系统架构师，他的主要专业领域是Java EE、中间件和JVM技术。他在性能优化和提升方面也有很深刻的见解，下面他将和大家分享一下常见的10个影响Java EE性能问题。


**1.缺乏正确的容量规划**


容量规划是一个全面的和发展的过程标准，预测当前和未来的IT环境容量需求。制定合理的容量规划不仅会确保和跟踪当前IT生产能力和稳定性，同时也会确保新项目以最小的风险部署到现有的生产环境中。硬件、中间件、JVM、调整等在项目部署之前就应该准备好。

以我的经验，这通常是最常见的“过程”问题，可能会导致短期和长期的性能问题。以下是一些示例。

<table style="border-collapse: collapse; border: 2px none #000000" border="2" cellpadding="0" cellspacing="0"><tbody><tr><td style="width: 221.4pt; border: 1pt solid windowtext; padding: 0in 5.4pt" valign="top" width="221"><p class="MsoNormal"><strong><span style="font-family: Arial; font-size: 11pt;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">观察到的问题</font></font></span></strong></p></td><td style="width: 221.4pt; border-width: 1pt 1pt 1pt medium; border-style: solid solid solid none; border-color: windowtext windowtext windowtext -moz-use-text-color; -moz-border-top-colors: none; -moz-border-right-colors: none; -moz-border-bottom-colors: none; -moz-border-left-colors: none; -moz-border-image: none; padding: 0in 5.4pt" valign="top" width="221"><p class="MsoNormal"><strong><span style="font-family: Arial; font-size: 11pt;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">可能的产能规划差距</font></font></span></strong></p></td></tr><tr><td style="width: 221.4pt; border-width: medium 1pt 1pt; border-style: none solid solid; border-color: -moz-use-text-color windowtext windowtext; -moz-border-top-colors: none; -moz-border-right-colors: none; -moz-border-bottom-colors: none; -moz-border-left-colors: none; -moz-border-image: none; padding: 0in 5.4pt" valign="top" width="221"><p class="MsoNormal"><span style="font-family: Arial; font-size: 10pt;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">新部署的应用程序会触发当前Java Heap或Native Heap空间的重载（例如，</font><font style="vertical-align: inherit;">观察到</font></font><span style="color: rgb(192, 0, 0);"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">java.lang.OutOfMemoryError</font></font></span><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">）。</font></font></span></p></td><td style="width: 221.4pt; border-width: medium 1pt 1pt medium; border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; padding: 0in 5.4pt" valign="top" width="221"><p style="margin-left: 0.5in; text-indent: -0.25in" class="MsoNormal"><span style="font-family: Arial; font-size: 10pt;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">-对当前的JVM Java堆（YoungGen和OldGen空间）利用率缺乏了解</font></font></span></p><p style="margin-left: 0.5in; text-indent: -0.25in" class="MsoNormal"><span style="font-family: Arial; font-size: 10pt;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">-新部署的应用程序缺少内存静态和/或动态占用空间计算</font></font></span></p><p style="margin-left: 0.5in; text-indent: -0.25in" class="MsoNormal"><span style="font-family: Arial; font-size: 10pt;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">-缺乏性能和负载测试，无法检测到Java Heap内存泄漏等问题</font></font></span></p></td></tr><tr><td style="width: 221.4pt; border-width: medium 1pt 1pt; border-style: none solid solid; border-color: -moz-use-text-color windowtext windowtext; -moz-border-top-colors: none; -moz-border-right-colors: none; -moz-border-bottom-colors: none; -moz-border-left-colors: none; -moz-border-image: none; padding: 0in 5.4pt" valign="top" width="221"><p class="MsoNormal"><span style="font-family: Arial; font-size: 10pt;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">新部署的应用程序会触发CPU利用率的大幅提高以及Java EE中间件JVM进程的性能下降。</font></font></span></p></td><td style="width: 221.4pt; border-width: medium 1pt 1pt medium; border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; padding: 0in 5.4pt" valign="top" width="221"><p style="margin-left: 0.5in; text-indent: -0.25in" class="MsoNormal"><span style="font-family: Arial; font-size: 10pt;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">-对当前的CPU使用率缺乏了解（例如，已建立的基准）</font></font></span></p><p style="margin-left: 0.5in; text-indent: -0.25in" class="MsoNormal"><span style="font-family: Arial; font-size: 10pt;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">-对当前的JVM垃圾回收状况缺乏了解（新的应用程序/额外的负载可能触发增加的GC和CPU）</font></font></span></p><p style="margin-left: 0.5in; text-indent: -0.25in" class="MsoNormal"><span style="font-family: Arial; font-size: 10pt;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">-缺乏负载和性能测试，无法预测对现有CPU利用率的影响</font></font></span></p></td></tr><tr><td style="width: 221.4pt; border-width: medium 1pt 1pt; border-style: none solid solid; border-color: -moz-use-text-color windowtext windowtext; -moz-border-top-colors: none; -moz-border-right-colors: none; -moz-border-bottom-colors: none; -moz-border-left-colors: none; -moz-border-image: none; padding: 0in 5.4pt" valign="top" width="221"><p class="MsoNormal"><span style="font-family: Arial; font-size: 10pt;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">新的Java EE中间件系统已部署到生产环境，但无法处理预期的数量。</font></font></span></p></td><td style="width: 221.4pt; border-width: medium 1pt 1pt medium; border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; padding: 0in 5.4pt" valign="top" width="221"><p style="margin-left: 0.5in; text-indent: -0.25in" class="MsoNormal"><span style="font-family: Arial; font-size: 10pt;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">-缺少或不充分的性能和负载测试</font></font></span></p><p style="margin-left: 0.5in; text-indent: -0.25in" class="MsoNormal"><span style="font-family: Arial;"><span style="font-size: 11pt;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">- </font></font></span><span style="font-size: 10pt;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">用于性能和负载测试的数据和测试用例不能反映真实的流量和业务流程</font></font></span></span></p><p style="margin-left: 0.5in; text-indent: -0.25in" class="MsoNormal"><span style="font-family: Arial; font-size: 10pt;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">-带宽不足（或页面比预期的容量规划大得多）</font></font></span></p></td></tr></tbody></table>

容量规划的一个关键方面是每个人都应该熟悉的负载和性能测试。这涉及针对类生产环境或生产环境本身生成负载，以便：

*   确定您的应用程序可以支持多少并发用户/订单量
*   揭示平台和Java EE应用程序的瓶颈，使您能够采取纠正措施（中间件调整，代码更改，基础结构和容量改进等）。


**2.Java EE中间件环境规范不足**


“没有规矩，不成方圆”。第二个比较普遍的原因是Java EE中间件或者基础架构不规范。在项目初始，新平台上面没有制定合理的规范，导致系统稳定性差。这会增加客户成本，所以花时间去制定合理的Java EE中间件环境规范是必须的。这项工作应与初始容量规划迭代相结合。

![](https://dzone.com/sites/all/files/image003_0.png)

现在，在下面找到我以往经验中观察到的问题的典型示例：

*   单个32位JVM中部署了太多的Java EE应用程序
*   在一个中间件域中部署了太多的Java EE应用程序
*   缺乏适当的垂直扩展和未充分利用的硬件（例如，由一个或几个JVM进程驱动的流量）
*   过多的垂直扩展和过度使用的硬件（例如，太多的JVM进程与可用的CPU内核和RAM）
*   缺乏环境冗余和故障转移功能

从成本的角度来看，尝试将单个中间件和/或JVM用于许多大型Java EE应用程序可能会很有吸引力。但是，这可能会导致操作方面的噩梦和严重的性能问题，例如过多的JVM垃圾回收以及许多产生多米诺骨牌效应的场景（例如，“粘滞线程”）会导致高业务影响（例如，App A导致App B，App C和App D失败，因为通常需要重新启动JVM才能解决问题）。

### 推荐建议

*   项目团队应该花足够的时间为Java EE生产环境创建适当的操作模型。
*   尝试为您的Java EE中间件规范找到一个良好的“平衡点”，以在业务中断的情况下为业务和运营团队提供适当的灵活性。
*   避免在单个32位JVM中部署太多Java EE应用程序。中间件旨在处理许多应用程序，但是您的JVM可能遭受的影响最大。
*   需要时，请选择32位JVM上的64位，但要结合适当的容量规划和性能测试以确保您的硬件将支持它。

**3.Java虚拟机垃圾回收过度**

现在，从过多的JVM垃圾收集开始，跳到纯粹的技术问题。你们中的大多数人都熟悉这个著名（或臭名昭著）的Java错误：java.lang.OutOfMemoryError。这是JVM内存空间耗尽（Java堆，本机堆等）的结果。

![](https://dzone.com/sites/all/files/image005_0.png)

我敢肯定，像Oracle和IBM这样的中间件供应商可以定期为您提供数十种涉及JVM OutOfMemoryError问题的支持案例，因此它在我们的列表中排名第三是不足为奇的。

请记住，垃圾回收问题不一定会表现为OOM条件。过多的垃圾回收可以定义为JVM GC线程（收集器）在短时间内执行过多的次要和/或主要收集，从而导致大量的JVM暂停时间和性能下降。有许多可能的原因：

*   与JVM并发负载和应用程序的内存占用相比，选择的Java堆大小太小。
*   使用了不适当的JVM GC策略。
*   您的应用程序的静态和/或动态内存占用量太大，无法容纳在32位JVM中。
*   JVM OldGen空间随着时间的推移正在泄漏*相当普遍的问题*; 数小时/天后，观察到过量的GC（大量收集）。
*   JVM PermGen空间（仅适用于HotSpot VM）或本机堆随着时间的流逝而泄漏*相当普遍的问题*；在应用程序动态重新部署后，随着时间的推移经常会观察到OOM错误。
*   对于您的应用程序，YoungGen / OldGen空间的比率不是最佳的（例如，生成大量短期对象的应用程序需要更大的YoungGen空间）。创建大量长寿命/缓存对象的应用程序需要更大的OldGen空间。
*   用于32位VM的Java堆大小太大，无法为本机堆留出空间。尝试使用新的Java EE应用程序，创建新的Java线程或需要本地内存分配的任何计算任务时，问题可能会显示为OOM。

在指责JVM之前，请记住实际的“根本”原因可能与我们的＃1和＃2原因有关。中间件环境过载将产生许多症状，包括过多的JVM垃圾收集。

正确分析与JVM相关的数据（内存空间，GC频率，CPU相关性等）将使您能够确定是否遇到问题。要进行更深入的分析以了解您的应用程序内存占用量，您将需要分析JVM堆转储和/或使用您选择的探查器工具（*例如JProfiler）*对您的应用程序进行探查。

### 建议

*   确保非常密切地监视和了解JVM垃圾收集。有几种商业和免费工具可以做到这一点。至少，您应该启用详细GC，它将提供健康评估所需的所有数据
*   请记住，在开发或功能测试期间不太可能发现与GC相关的问题。正确的垃圾收集调整将需要您从同时进行的用户中执行负载并进行大量测试。通过本练习，您可以根据应用程序行为和负载水平预测来微调Java Heap内存占用量。

**4.与外部系统集成过多或过少**

下一个导致Java EE性能下降的常见原因主要是适用于高度分布式的系统。通常用于电信IT环境。在这样的环境中，中间件域（例如，服务总线）将很少执行所有工作，而是将某些业务流程（例如产品鉴定，客户资料和订单管理）“委托”给其他Java EE中间件平台或旧版。各种有效负载类型和通信协议的系统，例如大型机。

![](https://dzone.com/sites/all/files/image007.png)

这样的外部系统调用意味着客户端Java EE应用程序将触发套接字连接的创建或重用，以通过专用网络向/从外部系统写入和读取数据。根据实现和业务流程的性质，其中一些调用可以配置为同步或异步。需要特别注意的是，响应时间可能会随着时间的推移而变化，具体取决于外部系统的运行状况，因此，通过正确使用超时来保护Java EE应用程序和中间件非常重要。

![](https://dzone.com/sites/all/files/image009.png)  
在以下情况下，可以观察到主要问题和性能下降：

*   以同步和顺序方式执行太多外部系统调用。这样的实现也完全暴露于其外部系统的不稳定和缓慢。
*   Java EE客户端应用程序和外部系统之间的超时丢失或值太大。这将导致客户端线程**卡住**，从而导致完全的多米诺骨牌效应。
*   可以正确实现超时，但不能对中间件进行微调以处理“不愉快”的路径。外部系统响应时间（或中断）的任何增加都将导致线程利用率和Java堆利用率的提高（待处理有效载荷数据的数量增加）。中间件环境和JVM必须以预测和处理“快乐”和“不快乐”路径的方式进行调整，以防止发生完全的多米诺骨牌效应。

最后，我还建议您花足够的时间进行负面测试。这意味着应该将问题条件“人为地”引入外部系统，以测试您的应用程序和中间件环境如何处理这些外部系统的故障。此练习也应在高容量情况下执行，以使您可以微调应用程序和外部系统之间的不同超时值。



**5.缺乏适当的数据库SQL调优和容量规划**



下一个常见的性能问题对任何人都不应该感到惊讶：数据库问题。大多数Java EE企业系统都依赖关系数据库来执行从门户内容管理到订单供应系统的各种业务流程。坚实的数据库环境和基础将确保您的IT环境能够适当扩展以支持您的客户不断增长的业务。

![](https://dzone.com/sites/all/files/image011.png)

以我的生产支持经验，与数据库相关的性能问题非常常见。由于大多数数据库事务通常都是通过JDBC数据源执行的（*包括关系持久性API（如Hibernate*）），因此性能问题最初将表现为Java EE容器线程管理器中的“阻塞线程”。以下是我在过去十年中看到的与数据库有关的常见问题：

**请注意，以Oracle数据库为例，因为它是我的IT客户使用的通用产品。**

*   孤立的，长期运行的SQL。此问题将表现为线程卡住，通常表现为缺少SQL调整，缺少索引，执行计划不理想，返回的数据集太大等。
*   表或行级别的数据锁定。特别是在处理两阶段提交事务模型（*例如：臭名昭著的Oracle In-Doubt Transactions*）时，此问题尤其明显。在这种情况下，Java EE容器可以留下一些未决的事务来等待最终提交或回滚，从而留下可能触发性能问题的数据锁，直到这些锁被删除为止。这可能是由于触发事件（例如中间件中断或服务器崩溃）而发生的。
*   执行计划突然更改。我经常看到此问题，通常是某些数据模式更改的结果，这可能（例如）导致Oracle动态更新查询执行计划并触发严重的性能下降。
*   缺乏适当的数据库设施管理。例如，Oracle有几个方面需要检查，例如REDO日志，数据库数据文件等。诸如磁盘空间不足和日志文件未旋转之类的问题可能会引发主要的性能问题和断电情况。

### 推荐建议

*   在此处进行包含负载和性能测试的正确容量规划对于微调数据库环境并检测SQL级别的任何问题至关重要。
*   如果您使用的是Oracle数据库，请确保您的DBA团队定期检查AWR报告，尤其是在事件和根本原因分析过程中。其他数据库供应商也应执行相同的分析方法。
*   利用JVM线程转储和AWR报告来查明运行缓慢的SQL和/或使用您选择的监视工具来执行此操作。 
*   确保花费足够的时间来加强数据库环境的“操作”方面（磁盘空间，数据文件，REDO日志，表空间等）以及适当的监视和警报。否则，可能会使您的客户端IT环境面临严重的停机情况，并造成大量的停机时间。

**6.特定应用程序性能问题**

回顾一下，到目前为止，我们已经看到了适当的容量计划，负载和性能测试，中间件环境规范，JVM运行状况，外部系统集成以及关系数据库环境的重要性。但是Java EE应用程序本身呢？毕竟，您的IT环境可能拥有市场上最快的硬件，其中包含数百个CPU内核，大量的RAM和数十个64位JVM进程。但是如果应用程序实现不足，性能仍然会很糟糕。本节将重点介绍各种Java EE环境中最严重的Java EE应用程序问题。

我的主要建议是确保代码审查与发布管理流程一起成为常规开发周期的一部分。这将使您能够按照下面以及在主要测试和实施阶段之前查明主要实施问题。

### 线程安全代码问题

使用Java同步和非最终静态变量/对象时，必须格外小心。在Java EE环境中，任何静态变量或对象都必须是线程安全的，以确保数据完整性和可预测的结果。错误地将静态变量用于Java类成员变量，可能会导致负载下无法预测的结果，因为这些变量/对象在Java EE容器线程之间共享（例如，线程B可以修改线程A的静态变量值，从而导致意外和错误的行为）。应该将类成员变量定义为非静态变量，以保留在当前类实例上下文中，以便每个线程都有自己的副本。

在处理非线程安全的数据结构（例如java.util.HashMap）时，Java同步也非常重要。否则，可能会触发HashMap损坏和无限循环。处理Java同步时要小心，因为过度使用还可能导致线程卡住和性能下降。

### 缺少通信API超时

对于每个通信API ，实现和测试事务（套接字read（）和write（）操作）和连接超时（Socket connect（）操作）非常重要。Java EE应用程序与外部系统之间缺少适当的HTTP / HTTPS / TCP IP ...超时，可能会由于线程卡住而导致严重的性能下降和中断。正确的超时实现将防止在下游系统严重减速的情况下线程等待太长时间。

以下是一些较旧的和当前的API（Apache和Weblogic）的示例：

<table style="border-collapse: collapse; border: 2px none #000000" border="2" cellpadding="0" cellspacing="0"><tbody><tr><td style="width: 19.52%; border: 1pt solid windowtext; padding: 0in 5.4pt" width="19%"><p class="MsoNormal" style="text-align: center" align="center"><strong><span style="font-size: 10pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">通讯API</font></font></span></strong></p></td><td style="width: 10.16%; border-width: 1pt 1pt 1pt medium; border-style: solid solid solid none; border-color: windowtext windowtext windowtext -moz-use-text-color; -moz-border-top-colors: none; -moz-border-right-colors: none; -moz-border-bottom-colors: none; -moz-border-left-colors: none; -moz-border-image: none; padding: 0in 5.4pt" width="10%"><p class="MsoNormal" style="text-align: center" align="center"><strong><span style="font-size: 10pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">供应商</font></font></span></strong></p></td><td style="width: 13.2%; border-width: 1pt 1pt 1pt medium; border-style: solid solid solid none; border-color: windowtext windowtext windowtext -moz-use-text-color; -moz-border-top-colors: none; -moz-border-right-colors: none; -moz-border-bottom-colors: none; -moz-border-left-colors: none; -moz-border-image: none; padding: 0in 5.4pt" width="13%"><p class="MsoNormal" style="text-align: center" align="center"><strong><span style="font-size: 10pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">协议</font></font></span></strong></p></td><td style="width: 57.12%; border-width: 1pt 1pt 1pt medium; border-style: solid solid solid none; border-color: windowtext windowtext windowtext -moz-use-text-color; -moz-border-top-colors: none; -moz-border-right-colors: none; -moz-border-bottom-colors: none; -moz-border-left-colors: none; -moz-border-image: none; padding: 0in 5.4pt" width="57%"><p class="MsoNormal" style="text-align: center" align="center"><strong><span style="font-size: 10pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">超时代码段</font></font></span></strong></p></td></tr><tr><td style="width: 19.52%; border-width: medium 1pt 1pt; border-style: none solid solid; border-color: -moz-use-text-color windowtext windowtext; -moz-border-top-colors: none; -moz-border-right-colors: none; -moz-border-bottom-colors: none; -moz-border-left-colors: none; -moz-border-image: none; padding: 0in 5.4pt" width="19%"><p class="MsoNormal" style="text-align: center" align="center"><span style="font-size: 8pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">commons-httpclient 3.0.1</font></font></span></p></td><td style="width: 10.16%; border-width: medium 1pt 1pt medium; border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; padding: 0in 5.4pt" width="10%"><p class="MsoNormal" style="text-align: center" align="center"><span style="font-size: 8pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">阿帕奇</font></font></span></p></td><td style="width: 13.2%; border-width: medium 1pt 1pt medium; border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; padding: 0in 5.4pt" width="13%"><p class="MsoNormal" style="text-align: center" align="center"><span style="font-size: 8pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">HTTP / HTTPS</font></font></span></p></td><td style="width: 57.12%; border-width: medium 1pt 1pt medium; border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; padding: 0in 5.4pt" width="57%"><p class="MsoNormal"><span style="font-size: 8pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">HttpConnectionManagerParams。</font></font><span style="color: navy;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">setSoTimeout</font></font></span><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">（txTimeout）; </font></font><span style="color: green;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">//交易超时</font></font></span></span></p><p class="MsoNormal"><span style="font-size: 8pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">HttpConnectionManagerParams。</font></font><span style="color: navy;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">setConnectionTimeout</font></font></span><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">（connTimeout）; </font></font><span style="color: green;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">// 连接超时</font></font></span></span></p></td></tr><tr><td style="width: 19.52%; border-width: medium 1pt 1pt; border-style: none solid solid; border-color: -moz-use-text-color windowtext windowtext; -moz-border-top-colors: none; -moz-border-right-colors: none; -moz-border-bottom-colors: none; -moz-border-left-colors: none; -moz-border-image: none; padding: 0in 5.4pt" width="19%"><p class="MsoNormal" style="text-align: center" align="center"><span style="font-size: 8pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">axis.jar（v1.4 1855）</font></font></span></p></td><td style="width: 10.16%; border-width: medium 1pt 1pt medium; border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; padding: 0in 5.4pt" width="10%"><p class="MsoNormal" style="text-align: center" align="center"><span style="font-size: 8pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">阿帕奇</font></font></span></p></td><td style="width: 13.2%; border-width: medium 1pt 1pt medium; border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; padding: 0in 5.4pt" width="13%"><p class="MsoNormal" style="text-align: center" align="center"><span style="font-size: 8pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">WS通过HTTP / HTTPS</font></font></span></p></td><td style="width: 57.12%; border-width: medium 1pt 1pt medium; border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; padding: 0in 5.4pt" width="57%"><p class="MsoNormal"><em><span style="color: red; font-size: 8pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">***请注意，AXIS 1.x版存在</font><font style="vertical-align: inherit;">SSL套接字创建</font><font style="vertical-align: inherit;">的</font></font><u><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">已知问题</font></font></u><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">，该问题忽略了指定的超时值。</font><font style="vertical-align: inherit;">解决方案是重写client-config.wsdd并将HTTPS传输设置为&lt;transport name =“ https” </font></font></span><span style="color: blue; font-size: 8pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">ivot </font></font></span><font style="vertical-align: inherit;"><span style="color: red; font-size: 8pt;" lang="EN-CA"><font style="vertical-align: inherit;">=“ java：org.apache.axis.transport.http。CommonsHTTPSender </font></span></font><span style="color: red; font-size: 8pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">” /&gt; ***“</font></font></span></em></p><p class="MsoNormal"><span style="font-size: 8pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">（（（org.apache.axis.client.Stub）端口）。</font></font><span style="color: navy;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">setTimeout</font></font></span><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">（timeoutMilliseconds）; </font></font><span style="color: green;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">//交易和连接超时</font></font></span></span></p></td></tr><tr><td style="width: 19.52%; border-width: medium 1pt 1pt; border-style: none solid solid; border-color: -moz-use-text-color windowtext windowtext; -moz-border-top-colors: none; -moz-border-right-colors: none; -moz-border-bottom-colors: none; -moz-border-left-colors: none; -moz-border-image: none; padding: 0in 5.4pt" width="19%"><p class="MsoNormal" style="text-align: center" align="center"><span style="font-size: 8pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">WLS103（旧的JAX-RPC）</font></font></span></p></td><td style="width: 10.16%; border-width: medium 1pt 1pt medium; border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; padding: 0in 5.4pt" width="10%"><p class="MsoNormal" style="text-align: center" align="center"><span style="font-size: 8pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">甲骨文</font></font></span></p></td><td style="width: 13.2%; border-width: medium 1pt 1pt medium; border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; padding: 0in 5.4pt" width="13%"><p class="MsoNormal" style="text-align: center" align="center"><span style="font-size: 8pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">WS通过HTTP / HTTPS</font></font></span></p></td><td style="width: 57.12%; border-width: medium 1pt 1pt medium; border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; padding: 0in 5.4pt" width="57%"><p class="MsoNormal"><span style="color: green; font-size: 8pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">//交易和连接超时</font></font></span></p><p class="MsoNormal"><span style="font-size: 8pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">（（Stub）servicePort）._ setProperty（“ </font></font><span style="color: navy;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">weblogic.webservice.rpc.timeoutsecs</font></font></span><font style="vertical-align: inherit;"><font style="vertical-align: inherit;"> ”，timeoutSecs）;</font></font></span></p></td></tr><tr><td style="width: 19.52%; border-width: medium 1pt 1pt; border-style: none solid solid; border-color: -moz-use-text-color windowtext windowtext; -moz-border-top-colors: none; -moz-border-right-colors: none; -moz-border-bottom-colors: none; -moz-border-left-colors: none; -moz-border-image: none; padding: 0in 5.4pt" width="19%"><p class="MsoNormal" style="text-align: center" align="center"><span style="font-size: 8pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">WLS103（JAX-RPC 1.1）</font></font></span></p></td><td style="width: 10.16%; border-width: medium 1pt 1pt medium; border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; padding: 0in 5.4pt" width="10%"><p class="MsoNormal" style="text-align: center" align="center"><span style="font-size: 8pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">甲骨文</font></font></span></p></td><td style="width: 13.2%; border-width: medium 1pt 1pt medium; border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; padding: 0in 5.4pt" width="13%"><p class="MsoNormal" style="text-align: center" align="center"><span style="font-size: 8pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">WS通过HTTP / HTTPS</font></font></span></p></td><td style="width: 57.12%; border-width: medium 1pt 1pt medium; border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; padding: 0in 5.4pt" width="57%"><p class="MsoNormal"><span style="font-size: 8pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">（（Stub）servicePort）._ setProperty（“ </font></font><span style="color: navy;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">weblogic.wsee.transport.read.timeout</font></font></span><font style="vertical-align: inherit;"><font style="vertical-align: inherit;"> ”，timeoutMills）; </font></font><span style="color: green;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">//交易超时</font></font></span></span></p><p class="MsoNormal"><span style="font-size: 8pt;" lang="EN-CA"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">（（Stub）servicePort）._ setProperty（“ </font></font><span style="color: navy;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">weblogic.wsee.transport.connection.timeout</font></font></span><font style="vertical-align: inherit;"><font style="vertical-align: inherit;"> ”，timeoutMills）; </font></font><span style="color: green;"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">// 连接超时</font></font></span></span></p></td></tr></tbody></table>

### I / O，JDBC或关系持久性API资源管理问题

在实现原始DAO层或使用关系持久性API（例如Hibernate）时，正确的编码最佳实践很重要。目的是确保正确关闭会话/连接资源。必须在finally {}块中关闭此类与JDBC相关的资源，以正确处理任何故障情况。否则可能导致JDBC连接池泄漏，并最终导致线程卡住和完全中断的情况。

相同的规则适用于I / O资源，例如InputStream。当不再使用时，需要适当的关闭；否则，它可能导致Socket / File Descriptor泄漏并导致JVM完全挂起。

### 缺乏适当的数据缓存

性能问题可能是由于重复和过多的计算任务而导致的，例如I / O /磁盘访问，关系数据库中的内容数据以及与客户相关的数据。具有合理内存占用量的静态数据应正确地缓存在Java Heap内存中或通过数据缓存系统缓存。

静态文件（例如属性文件）也应缓存，以防止过多的磁盘访问。简单的缓存策略可以对Java EE应用程序的性能产生非常积极的影响。

在处理Web服务和与XML相关的API时，数据缓存也很重要。此类API可能会产生过多的动态类加载和I / O /磁盘访问。确保遵循此类API最佳做法，并在适用时使用适当的缓存策略（Singleton等）。我建议您阅读有关该主题的[JAXB案例研究](http://javaeesupportpatterns.blogspot.com/2011/09/jaxbcontext-performance-problem-case.html)。

### 数据缓存过多

具有讽刺意味的是，尽管数据缓存对于确保适当的性能至关重要，但它也可能会导致严重的性能问题。为什么？好吧，如果您尝试在Java Heap上缓存太多数据，那么您将在过多的垃圾回收和OutOfMemoryError条件下苦苦挣扎。目标是在数据缓存，Java堆大小和可用硬件容量之间找到适当的平衡（*通过您的容量计划过程*）。

这是我的一位IT客户提出的一个问题案例的示例：

*   从Weblogic门户应用程序观察到非常差的性能。
*   实施数据缓存是为了提高性能并产生最初的积极影响。
*   他们在产品目录中添加的产品越多，数据缓存的需求就越大，Java Heap内存也就越大。
*   最终，IT团队不得不升级到具有每个JVM进程8 GB的64位JVM，以及更多的CPU内核。
*   最终，这种情况是不可持续的，必须对设计进行审查。
*   最终的解决方案最终在Java EE中间件和JVM之外通过单独的硬件使用了分布式数据缓存系统。

从这个故事中要记住的重要一点是，当需要太多的数据缓存来达到适当的性能水平时，就该回顾整体解决方案和设计了。

### 日志过多

最后但并非最不重要的一点是：过多的日志记录。确保在Java EE应用程序实现中正确记录日志是一种很好的做法。但是，请注意在生产环境中启用的日志记录级别。过多的日志记录将触发服务器上的高IO，并增加CPU使用率。对于使用较旧硬件的较旧环境或处理大量并发卷的环境而言，这尤其可能成为问题。我还建议您实现“可重载”日志记录级别功能，以便在日常生产支持中需要时打开/关闭额外的日志记录。

**7.Java EE中间件调优问题**

重要的是要认识到您的Java EE中间件规范可能足够但可能缺乏适当的调整。如今，大多数Java EE容器都可以根据您的应用程序和业务流程需求为您提供多种调优机会。

如果无法执行适当的调整和最佳实践，可能会使Java EE容器处于非最佳状态。我强烈建议您在适用时查看并实施适当的Java EE中间件供应商建议。

在高级视图下面找到所需内容的样本清单。

![](https://dzone.com/sites/all/files/image013_0.png)


**8.主动监控不足**


缺乏监控，并不会带来实际性能问题，但它会影响你对Java EE平台性能和健康状况的了解。最终，这个环境可以达到一个破发点，这可能会暴露出一些缺陷和问题(JVM的内存泄漏，等等)。


以我的经验来看，如果一开始不进行监控，而是运行几个月或者几年后再进行，平台稳定性将大打折扣。


也就是说，改善现有的环境永远都不会晚。下面是一些建议：

1. 复查现有Java EE环境监测能力和找到需改进的地方。
2. 监测方案应该尽可能的覆盖整个环境。
3. 监控方案应该符合容量规划进程。

**9.公共基础设施硬件饱和**

性能问题的另一个常见原因是硬件饱和。当在现有硬件上部署太多Java EE中间件环境及其JVM进程时，通常会观察到此问题。太多的JVM进程与物理CPU内核的可用性可能是一个真正的问题，会破坏您的应用程序性能。同样，随着客户业务的增长，容量规划过程还应注意硬件容量。

我的主要建议是研究硬件虚拟化。如今，这种方法非常普遍，并具有许多好处，例如减少了物理服务器，数据中心的大小，每个虚拟主机专用的物理资源，快速实现并降低了客户成本。每个虚拟主机的专用物理资源非常重要，因为您想要的最后一件事是一个Java EE容器，由于过度的CPU使用率而导致所有其他容器崩溃。

![](https://dzone.com/sites/all/files/image015_0.png)

**10.网络延迟**


最后一个影响性能问题的是网络，网络问题时不时的都会发生，如路由器、交换机和DNS服务器失败。更常见的是在一个高度分散的IT环境中定期或间歇性延迟。下面图片中的例子是一个位于同一区域的Weblogic集群通信与Oracle数据库服务器之间的延迟。


<img border="0" alt="" src="http://www.kuqin.com/upimg/allimg/120703/22550T224-7.png" width="500" height="400" style="margin:0px 0px 10px; padding:0px; border:none; max-width:580px">


间歇或定期的延迟会触发一些重要的性能问题，以不同的方式影响Java EE应用程序。

1. 因为大量的fetch迭代（网络传入和传出），涉及大数据集的数据查询问题的应用会非常受网络延迟的影响1. 应用程序在处理外部系统大数据负载（例如XML数据）时也会很受网络延迟的影响，会在发送和接收响应时产生巨大的响应间隔。1. Java EE容器复制过程（集群）也会受到影响，并且会让故障转移功能（如多播或单播数据包损失）处于风险中。

JDBC行数据“预取”、XML数据压缩和数据缓存可以减少网络延迟。在设计一个新的网络拓扑时，应该仔细检查这种网络延迟问题。
性能问题的最后一个来源是网络。主要的网络问题可能会不时发生，例如路由器，交换机和DNS服务器故障。但是，观察到的更常见的问题通常是由于在高度分布式的IT环境上工作时有规律或间歇性的延迟。下图突出显示了一个Weblogic群集的两个地理区域与仅位于一个地理区域中的Oracle数据库服务器通信的网络延迟差距的示例。

![](https://dzone.com/sites/all/files/image017_0.png)

间歇性或常规延迟问题肯定会触发一些主要的性能问题，并以不同的方式影响Java EE应用程序。

*   由于大量的获取迭代（跨网络来回转发），使用具有大型数据集的数据库查询的应用程序完全暴露于网络延迟。
*   处理来自外部系统的大数据有效载荷（例如大XML数据）的应用程序也暴露于网络等待时间，这可能会在发送和接收响应时触发间歇的高响应时间。
*   Java EE容器复制过程（集群）可能会受到影响，并使其故障转移功能（例如，多播或单播数据包丢失）面临风险。

诸如JDBC行数据“预取”，XML数据压缩和数据缓存之类的调整策略可以帮助减轻网络延迟。但是，在首先设计新的IT环境的网络拓扑时，应仔细检查此类延迟问题。

我希望本文能帮助您了解在开发和支持Java EE生产系统时可能遇到的一些常见性能问题和压力点。由于每个IT环境都是唯一的，所以我并不希望每个人都会面临完全相同的问题。因此，我邀请您发表评论并分享您对该主题的看法。

[英文链接](https://dzone.com/articles/top-10-causes-java-ee)

