---
title: Java ThreadLocalRandom指南
id: 14
date: 2024-10-31 22:01:39
author: daichangya
excerpt: 1.Overview生成随机值是非常常见的任务。这就是Java提供java.util.Random类的原因。但是，此类在多线程环境中表现不佳。以简化的方式，在多线程环境中，Random性能不佳的原因是由于争用–假设多个线程共享同一个Random实例。为了解决该限制，Java在JDK7中引入了java
permalink: /archives/Java-ThreadLocalRandom-zhi-nan/
categories:
- 多线程
---

1.Overview
生成随机值是非常常见的任务。这就是Java提供java.util.Random类的原因。


但是，此类在多线程环境中表现不佳。

以简化的方式，在多线程环境中，Random性能不佳的原因是由于争用–假设多个线程共享同一个Random实例。

为了解决该限制，Java 在JDK 7中引入了java.util.concurrent.ThreadLocalRandom类–用于在多线程环境中生成随机数。

让我们看看ThreadLocalRandom是如何执行的以及如何在实际应用程序中使用它。

2. ThreadLocalRandom Over Random
ThreadLocalRandom是ThreadLocal和Random类的组合，它们与当前线程隔离。因此，通过简单地避免对 Random实例的任何并发访问，它可以在多线程环境中实现更好的性能。

一个线程获得的随机数不受另一线程的影响，而java.util.Random则全局提供随机数。

另外，与Random 不同，ThreadLocalRandom不支持显式设置种子。相反，它将重写从Random继承的setSeed（long seed）方法，以在调用时始终抛出UnsupportedOperationException。

2.1。Thread Contention
到目前为止，我们已经确定  Random 类在高度并发的环境中性能较差。为了更好地理解这一点，让我们看看如何实现其主要操作之一next（int）：

```
private final AtomicLong seed;
 
protected int next(int bits) {
    long oldseed, nextseed;
    AtomicLong seed = this.seed;
    do {
        oldseed = seed.get();
        nextseed = (oldseed * multiplier + addend) & mask;
    } while (!seed.compareAndSet(oldseed, nextseed));
 
    return (int)(nextseed >>> (48 - bits));
}
```
这是线性同余生成器算法的Java实现。显而易见，所有线程都共享相同的种子实例变量。

为了生成下一个随机位集，它首先尝试通过compareAndSet  或CAS 简短地自动更改共享  种子 值  。


当多个线程尝试使用CAS同时更新  种子时 ，一个线程会获胜并更新种子， 而其他线程则会  失败。丢失的线程将反复尝试相同的过程，直到它们有机会更新值并  最终生成随机数。

该算法是无锁的，并且不同的线程可以同时进行。但是，当竞争激烈时，CAS失败和重试的次数将严重损害整体性能。

另一方面，  ThreadLocalRandom  完全消除了这一争用，因为每个线程都有自己的Random 实例  ，因此有自己的受限  种子。

现在，让我们看一下生成随机int，long和double值的一些方法。

3.Generating Random Values Using ThreadLocalRandom
根据Oracle文档，我们只需要调用ThreadLocalRandom.current（）方法，它将为当前线程返回ThreadLocalRandom的实例。然后，我们可以通过调用该类的可用实例方法来生成随机值。

让我们生成一个没有任何限制的随机整数值：

1
int unboundedRandomValue = ThreadLocalRandom.current().nextInt());
接下来，让我们看看如何生成一个随机有界的int值，即一个介于给定下限和上限之间的值。

这是生成介于0到100之间的随机int值的示例：

1
int boundedRandomValue = ThreadLocalRandom.current().nextInt(0, 100);
请注意，0是包含下限，而100是包含上限。

如上例所示，通过调用nextLong（）和nextDouble（）方法，我们可以为long和double生成随机值。

Java 8还添加了nextGaussian（）方法来生成下一个正态分布的值，该值与生成器的序列的平均值为0.0，标准差为1.0。

与Random类一样，我们也可以使用doubles（），ints（）和longs（）方法生成随机值流。

4. Comparing ThreadLocalRandom and Random Using JMH
让我们看看如何通过使用两个类在多线程环境中生成随机值，然后使用JMH比较它们的性能。

首先，让我们创建一个示例，其中所有线程共享一个Random实例。在这里，我们正在将使用Random实例生成随机值的任务提交给ExecutorService：

```
ExecutorService executor = Executors.newWorkStealingPool();
List<Callable<Integer>> callables = new ArrayList<>();
Random random = new Random();
for (int i = 0; i < 1000; i++) {
    callables.add(() -> {
         return random.nextInt();
    });
}
executor.invokeAll(callables);
```
让我们使用JMH基准测试来检查以上代码的性能：

```
# Run complete. Total time: 00:00:36
Benchmark                                            Mode Cnt Score    Error    Units
ThreadLocalRandomBenchMarker.randomValuesUsingRandom avgt 20  771.613 ± 222.220 us/op
```
同样，让我们​​现在使用ThreadLocalRandom代替Random实例，该实例为池中的每个线程使用ThreadLocalRandom的一个实例：

```
ExecutorService executor = Executors.newWorkStealingPool();
List<Callable<Integer>> callables = new ArrayList<>();
for (int i = 0; i < 1000; i++) {
    callables.add(() -> {
        return ThreadLocalRandom.current().nextInt();
    });
}
executor.invokeAll(callables);
```
这是使用ThreadLocalRandom的结果：

```
# Run complete. Total time: 00:00:36
Benchmark                                                       Mode Cnt Score    Error   Units
ThreadLocalRandomBenchMarker.randomValuesUsingThreadLocalRandom avgt 20  624.911 ± 113.268 us/op
```
最后，通过比较上述针对Random和ThreadLocalRandom的JMH结果，我们可以清楚地看到，使用Random生成1000个随机值所需的平均时间为772微秒，而使用ThreadLocalRandom则约为625微秒。

因此，我们可以得出结论，在高度并发的环境中ThreadLocalRandom效率更高。

要了解有关JMH的更多信息，请在此处查看我们以前的文章。

5.Conclusion
本文说明了java.util.Random和java.util.concurrent.ThreadLocalRandom之间的区别。

我们还看到了在多线程环境中ThreadLocalRandom优于Random的优势，以及性能以及如何使用该类生成随机值的方法。
ThreadLocalRandom是对JDK的简单添加，但是它可以在高度并发的应用程序中产生显着的影响。

而且，与往常一样，所有这些示例的实现都可以在[github](https://github.com/daichangya/Java-Concurrency-in-Practice)中找到。

