---
title: LongAdder and LongAccumulator in Java
id: 15
date: 2024-10-31 22:01:39
author: daichangya
excerpt: "1.Overview在本文中，我们将研究java.util.concurrent包中的两个构造：LongAdder和LongAccumulator。两者都被创建为在多线程环境中非常高效，并且都利用非常巧妙的策略来实现无锁且仍保持线程安全。LongAdder让我们考虑一些逻辑，该逻辑经常增加一些值，而"
permalink: /archives/longadderandlongaccumulatorinjava/
categories:
 - 多线程
---

1.Overview
在本文中，我们将研究java.util.concurrent包中的两个构造：LongAdder和LongAccumulator。

两者都被创建为在多线程环境中非常高效，并且都利用非常巧妙的策略来实现无锁且仍保持线程安全。


2. LongAdder
让我们考虑一些逻辑，该逻辑经常增加一些值，而使用AtomicLong可能会成为瓶颈。这使用了比较交换操作，在激烈的竞争中，这可能会导致大量的CPU周期浪费。

另一方面，LongAdder使用非常巧妙的技巧来减少线程之间的争用（当线程递增时）。

当我们想增加LongAdder的实例时，我们需要调用 increment() method。该实现保留了可以按需增长的一系列计数器。

因此，当更多线程正在调用 increment()时，数组将更长。数组中的每个记录都可以单独更新-减少了争用。因此，LongAdder是从多个线程递增计数器的非常有效的方法。

让我们创建LongAdder类的实例，并从多个线程中对其进行更新：

```
LongAdder counter = new LongAdder();
ExecutorService executorService = Executors.newFixedThreadPool(8);
 
int numberOfThreads = 4;
int numberOfIncrements = 100;
 
Runnable incrementAction = () -> IntStream
  .range(0, numberOfIncrements)
  .forEach(i -> counter.increment());
 
for (int i = 0; i < numberOfThreads; i++) {
    executorService.execute(incrementAction);
}
```
在我们调用sum（）方法之前，LongAdder中计数器的结果不可用。该方法将迭代下面的数组的所有值，并对这些值求和以返回正确的值。但是，我们需要小心，因为对sum（）方法的调用可能会非常昂贵：

```
assertEquals(counter.sum(), numberOfIncrements * numberOfThreads);
```
有时，在调用sum（）之后，我们想清除与LongAdder实例相关联的所有状态，并从头开始计数。我们可以使用sumThenReset（）方法来实现：
```
assertEquals(counter.sumThenReset(), numberOfIncrements * numberOfThreads);
assertEquals(counter.sum(), 0);
```
请注意，随后对sum（）方法的调用返回零，表示状态已成功重置。

3. LongAccumulator
LongAccumulator也是一个非常有趣的类–它使我们可以在许多情况下实现无锁算法。例如，它可以根据所提供的LongBinaryOperator来累积结果– 与Stream API 的reduce（）操作类似。

可以通过将LongBinaryOperator及其初始值提供给其构造函数来创建LongAccumulator的实例。重要的是要记住，如果我们为LongAccumulator提供一个交换函数，而该函数的累加顺序无关紧要，它将可以正常工作。
```
LongAccumulator accumulator = new LongAccumulator(Long::sum, 0L);
```
我们正在创建一个LongAccumulator WHI的通道将一个新值添加到已经在累加器的值。我们将LongAccumulator的初始值设置为零，因此在第一次调用accumulate（）方法时，previousValue将具有零值。

让我们从多个线程中调用accumulate（）方法：

```
int numberOfThreads = 4;
int numberOfIncrements = 100;
 
Runnable accumulateAction = () -> IntStream
  .rangeClosed(0, numberOfIncrements)
  .forEach(accumulator::accumulate);
 
for (int i = 0; i < numberOfThreads; i++) {
    executorService.execute(accumulateAction);
}
```
请注意，我们如何将数字作为参数传递给accumulate（）方法。该方法将调用我们的sum（）函数。

该LongAccumulator使用比较并交换实现-这导致了这些有趣的语义。

首先，它执行一个定义为LongBinaryOperator的操作，然后检查previousValue是否更改。如果已更改，则使用新值再次执行该动作。如果不是，它将成功更改存储在累加器中的值。

现在我们可以断言，所有迭代的所有值之和为20200：

```
assertEquals(accumulator.get(), 20200);
```
4。Conclusion
在本快速教程中，我们了解了LongAdder和LongAccumulator，并展示了如何使用这两种构造来实现非常有效且无锁的解决方案。

所有这些示例和代码段的实现都可以在[github](https://github.com/daichangya/Java-Concurrency-in-Practice)项目中找到–这是一个Maven项目，因此应该很容易直接导入和运行。

