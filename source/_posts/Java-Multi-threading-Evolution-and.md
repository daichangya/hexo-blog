---
title: Java Multi-threading Evolution and Topics
id: 17
date: 2024-10-31 22:01:39
author: daichangya
permalink: /archives/Java-Multi-threading-Evolution-and/
categories:
- java并发教程
---

## JDK release-wise multi-threading concepts
根据JDK 1.x发行版，此初始发行版中仅提供了很少的类。具体来说，这些类/接口是：
```
java.lang.Thread
java.lang.ThreadGroup
java.lang.Runnable
java.lang.Process
java.lang.ThreadDeath
```
和一些异常类
例如
```
java.lang.IllegalMonitorStateException
java.lang.IllegalStateException
java.lang.IllegalThreadStateException。
```
它还没有几个同步的集合，例如java.util.Hashtable。

JDK 1.2和JDK 1.3没有与多线程相关的明显变化。（如果我错过任何事情，请纠正我）。

JDK 1.4中，几乎没有JVM级别更改，可以通过一次调用挂起/恢复多个线程。但是没有出现重大的API更改。

JDK 1.5是继JDK 1.x之后的第一个重要版本。它包括多个并发实用程序。Executor，semaphore，mutex，barrier，latches，concurrent collections和blocking queues; 所有这些都包含在此版本本身中。Java多线程应用程序云的最大变化发生在此版本中。

阅读此链接中的全部更改集：http : //docs.oracle.com/javase/1.5.0/docs/guide/concurrency/overview.html

与API升级相比，JDK 1.6不仅仅是平台修复。因此，JDK 1.6中出现了新变化。

JDK 1.7添加了对它的支持，ForkJoinPool该支持通过实施工作窃取技术来最大化吞吐量。还Phaser添加了类。

JDK 1.8以Lambda更改而闻名，但是它并发更改也很少。在 java.util.concurrent包（例如CompletableFuture和中）中添加了两个新接口和四个新类CompletionException。

集合框架在Java 8中进行了重大修改，以基于新添加的流工具和lambda表达式添加聚合操作; 导致几乎所有Collection类中都添加了大量方法，因此并发集合中也添加了很多方法。

