---
title: JDK 7 中的 Fork/Join 模式
id: 1177
date: 2024-10-31 22:01:50
author: daichangya
excerpt: "轻松实现多核时代的并行计算随着多核时代的来临，软件开发人员不得不开始关注并行编程领域。而 JDK 7 中将会加入的 Fork/Join 模式是处理并行编程的一个经典的方法。虽然不能解决所有的问题，但是在它的适用范围之内，能够轻松的利用多个 CPU 提供的计算资源来协作完成一个复杂的计算任务。通过利用 Fork/Join 模式，我们能够更加顺畅的过渡到多核的时代。本文将介绍使用 "
permalink: /archives/jdk-7-zhong-de-fork-join-mo-shi/
categories:
 - 多线程-并发
---



## 介绍

随着多核芯片逐渐成为主流，大多数软件开发人员不可避免地需要了解并行编程的知识。而同时，主流程序语言正在将越来越多的并行特性合并到标准库或者语言本身之中。我们可以看到，JDK 在这方面同样走在潮流的前方。在 JDK 标准版 5 中，由 Doug Lea 提供的并行框架成为了标准库的一部分（JSR-166）。随后，在 JDK 6 中，一些新的并行特性，例如并行 collection 框架，合并到了标准库中（JSR-166x）。直到今天，尽管 Java SE 7 还没有正式发布，一些并行相关的新特性已经出现在 JSR-166y 中：

1.  Fork/Join 模式；
2.  TransferQueue，它继承自 BlockingQueue 并能在队列满时阻塞“生产者”；
3.  ArrayTasks/ListTasks，用于并行执行某些数组/列表相关任务的类；
4.  IntTasks/LongTasks/DoubleTasks，用于并行处理数字类型数组的工具类，提供了排序、查找、求和、求最小值、求最大值等功能；

其中，对 Fork/Join 模式的支持可能是对开发并行软件来说最通用的新特性。在 JSR-166y 中，Doug Lea 实现 ArrayTasks/ListTasks/IntTasks/LongTasks/DoubleTasks 时就大量的用到了 Fork/Join 模式。读者还需要注意一点，因为 JDK 7 还没有正式发布，因此本文涉及到的功能和发布版本有可能不一样。

Fork/Join 模式有自己的适用范围。如果一个应用能被分解成多个子任务，并且组合多个子任务的结果就能够获得最终的答案，那么这个应用就适合用 Fork/Join 模式来解决。[图 1](#figure001) 给出了一个 Fork/Join 模式的示意图，位于图上部的 Task 依赖于位于其下的 Task 的执行，只有当所有的子任务都完成之后，调用者才能获得 Task 0 的返回结果。

##### 图 1\. Fork/Join 模式示意图

![图 1.  Fork/Join 模式示意图](https://www.ibm.com/developerworks/cn/java/j-lo-forkjoin/figure001.jpg)


可以说，Fork/Join 模式能够解决很多种类的并行问题。通过使用 Doug Lea 提供的 Fork/Join 框架，软件开发人员只需要关注任务的划分和中间结果的组合就能充分利用并行平台的优良性能。其他和并行相关的诸多难于处理的问题，例如负载平衡、同步等，都可以由框架采用统一的方式解决。这样，我们就能够轻松地获得并行的好处而避免了并行编程的困难且容易出错的缺点。

## 使用 Fork/Join 模式

在开始尝试 Fork/Join 模式之前，我们需要从 Doug Lea 主持的 Concurrency JSR-166 Interest Site 上下载 JSR-166y 的源代码，并且我们还需要安装最新版本的 JDK 6（下载网址请参阅 [参考资源](#artrelatedtopics)）。Fork/Join 模式的使用方式非常直观。首先，我们需要编写一个 ForkJoinTask 来完成子任务的分割、中间结果的合并等工作。随后，我们将这个 ForkJoinTask 交给 ForkJoinPool 来完成应用的执行。

通常我们并不直接继承 ForkJoinTask，它包含了太多的抽象方法。针对特定的问题，我们可以选择 ForkJoinTask 的不同子类来完成任务。RecursiveAction 是 ForkJoinTask 的一个子类，它代表了一类最简单的 ForkJoinTask：不需要返回值，当子任务都执行完毕之后，不需要进行中间结果的组合。如果我们从 RecursiveAction 开始继承，那么我们只需要重载 `protected void compute()` 方法。下面，我们来看看怎么为快速排序算法建立一个 ForkJoinTask 的子类：

##### 清单 1\. ForkJoinTask 的子类

```
class SortTask extends RecursiveAction {
    final long[] array;
    final int lo;
    final int hi;
    private int THRESHOLD = 30;
 
    public SortTask(long[] array) {
        this.array = array;
        this.lo = 0;
        this.hi = array.length - 1;
    }
 
    public SortTask(long[] array, int lo, int hi) {
        this.array = array;
        this.lo = lo;
        this.hi = hi;
    }
 
    protected void compute() {
        if (hi - lo < THRESHOLD)
            sequentiallySort(array, lo, hi);
        else {
            int pivot = partition(array, lo, hi);
            coInvoke(new SortTask(array, lo, pivot - 1), new SortTask(array,
                pivot + 1, hi));
        }
    }
 
    private int partition(long[] array, int lo, int hi) {
        long x = array[hi];
        int i = lo - 1;
        for (int j = lo; j < hi; j++) {
            if (array[j] <= x) {
                i++;
                swap(array, i, j);
            }
        }
        swap(array, i + 1, hi);
        return i + 1;
    }
 
    private void swap(long[] array, int i, int j) {
        if (i != j) {
            long temp = array[i];
            array[i] = array[j];
            array[j] = temp;
        }
    }
 
    private void sequentiallySort(long[] array, int lo, int hi) {
        Arrays.sort(array, lo, hi + 1);
    }
}
```

在 [清单 1](#list1) 中，SortTask 首先通过 `partition()` 方法将数组分成两个部分。随后，两个子任务将被生成并分别排序数组的两个部分。当子任务足够小时，再将其分割为更小的任务反而引起性能的降低。因此，这里我们使用一个 `THRESHOLD`，限定在子任务规模较小时，使用直接排序，而不是再将其分割成为更小的任务。其中，我们用到了 RecursiveAction 提供的方法 `coInvoke()`。它表示：启动所有的任务，并在所有任务都正常结束后返回。如果其中一个任务出现异常，则其它所有的任务都取消。`coInvoke()` 的参数还可以是任务的数组。

现在剩下的工作就是将 SortTask 提交到 ForkJoinPool 了。`ForkJoinPool()` 默认建立具有与 CPU 可使用线程数相等线程个数的线程池。我们在一个 JUnit 的 `test` 方法中将 SortTask 提交给一个新建的 ForkJoinPool：

##### 清单 2\. 新建的 ForkJoinPool

```
@Test
public void testSort() throws Exception {
    ForkJoinTask sort = new SortTask(array);
    ForkJoinPool fjpool = new ForkJoinPool();
    fjpool.submit(sort);
    fjpool.shutdown();
 
    fjpool.awaitTermination(30, TimeUnit.SECONDS);
 
    assertTrue(checkSorted(array));
}
```

在上面的代码中，我们用到了 ForkJoinPool 提供的如下函数：

1.  `submit()`：将 ForkJoinTask 类的对象提交给 ForkJoinPool，ForkJoinPool 将立刻开始执行 ForkJoinTask。
2.  `shutdown()`：执行此方法之后，ForkJoinPool 不再接受新的任务，但是已经提交的任务可以继续执行。如果希望立刻停止所有的任务，可以尝试 `shutdownNow()` 方法。
3.  `awaitTermination()`：阻塞当前线程直到 ForkJoinPool 中所有的任务都执行结束。

并行快速排序的完整代码如下所示：

##### 清单 3\. 并行快速排序的完整代码

```
package tests;
 
import static org.junit.Assert.*;
 
import java.util.Arrays;
import java.util.Random;
import java.util.concurrent.TimeUnit;
 
import jsr166y.forkjoin.ForkJoinPool;
import jsr166y.forkjoin.ForkJoinTask;
import jsr166y.forkjoin.RecursiveAction;
 
import org.junit.Before;
import org.junit.Test;
 
class SortTask extends RecursiveAction {
    final long[] array;
    final int lo;
    final int hi;
    private int THRESHOLD = 0; //For demo only
 
    public SortTask(long[] array) {
        this.array = array;
        this.lo = 0;
        this.hi = array.length - 1;
    }
 
    public SortTask(long[] array, int lo, int hi) {
        this.array = array;
        this.lo = lo;
        this.hi = hi;
    }
 
    protected void compute() {
        if (hi - lo < THRESHOLD)
            sequentiallySort(array, lo, hi);
        else {
            int pivot = partition(array, lo, hi);
            System.out.println("\npivot = " + pivot + ", low = " + lo + ", high = " + hi);
            System.out.println("array" + Arrays.toString(array));
            coInvoke(new SortTask(array, lo, pivot - 1), new SortTask(array,
                    pivot + 1, hi));
        }
    }
 
    private int partition(long[] array, int lo, int hi) {
        long x = array[hi];
        int i = lo - 1;
        for (int j = lo; j < hi; j++) {
            if (array[j] <= x) {
                i++;
                swap(array, i, j);
            }
        }
        swap(array, i + 1, hi);
        return i + 1;
    }
 
    private void swap(long[] array, int i, int j) {
        if (i != j) {
            long temp = array[i];
            array[i] = array[j];
            array[j] = temp;
        }
    }
 
    private void sequentiallySort(long[] array, int lo, int hi) {
        Arrays.sort(array, lo, hi + 1);
    }
}
 
public class TestForkJoinSimple {
    private static final int NARRAY = 16; //For demo only
    long[] array = new long[NARRAY];
    Random rand = new Random();
 
    @Before
    public void setUp() {
        for (int i = 0; i < array.length; i++) {
            array[i] = rand.nextLong()%100; //For demo only
        }
        System.out.println("Initial Array: " + Arrays.toString(array));
    }
 
    @Test
    public void testSort() throws Exception {
        ForkJoinTask sort = new SortTask(array);
        ForkJoinPool fjpool = new ForkJoinPool();
        fjpool.submit(sort);
        fjpool.shutdown();
 
        fjpool.awaitTermination(30, TimeUnit.SECONDS);
 
        assertTrue(checkSorted(array));
    }
 
    boolean checkSorted(long[] a) {
        for (int i = 0; i < a.length - 1; i++) {
            if (a[i] > (a[i + 1])) {
                return false;
            }
        }
        return true;
    }
}
```

运行以上代码，我们可以得到以下结果：

```
Initial Array: [46, -12, 74, -67, 76, -13, -91, -96]
 
pivot = 0, low = 0, high = 7
array[-96, -12, 74, -67, 76, -13, -91, 46]
 
pivot = 5, low = 1, high = 7
array[-96, -12, -67, -13, -91, 46, 76, 74]
 
pivot = 1, low = 1, high = 4
array[-96, -91, -67, -13, -12, 46, 74, 76]
 
pivot = 4, low = 2, high = 4
array[-96, -91, -67, -13, -12, 46, 74, 76]
 
pivot = 3, low = 2, high = 3
array[-96, -91, -67, -13, -12, 46, 74, 76]
 
pivot = 2, low = 2, high = 2
array[-96, -91, -67, -13, -12, 46, 74, 76]
 
pivot = 6, low = 6, high = 7
array[-96, -91, -67, -13, -12, 46, 74, 76]
 
pivot = 7, low = 7, high = 7
array[-96, -91, -67, -13, -12, 46, 74, 76]
```

## Fork/Join 模式高级特性

### 使用 RecursiveTask

除了 RecursiveAction，Fork/Join 框架还提供了其他 ForkJoinTask 子类：带有返回值的 RecursiveTask，使用 `finish()` 方法显式中止的 AsyncAction 和 LinkedAsyncAction，以及可使用 TaskBarrier 为每个任务设置不同中止条件的 CyclicAction。

从 RecursiveTask 继承的子类同样需要重载 `protected void compute()` 方法。与 RecursiveAction 稍有不同的是，它可使用泛型指定一个返回值的类型。下面，我们来看看如何使用 RecursiveTask 的子类。

##### 清单 4\. RecursiveTask 的子类

```
class Fibonacci extends RecursiveTask<Integer> {
    final int n;
 
    Fibonacci(int n) {
        this.n = n;
    }
 
    private int compute(int small) {
        final int[] results = { 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89 };
        return results[small];
    }
 
    public Integer compute() {
        if (n <= 10) {
            return compute(n);
        }
        Fibonacci f1 = new Fibonacci(n - 1);
        Fibonacci f2 = new Fibonacci(n - 2);
        f1.fork();
        f2.fork();
        return f1.join() + f2.join();
    }
}
```

在 [清单 4](#list4) 中， Fibonacci 的返回值为 Integer 类型。其 `compute()` 函数首先建立两个子任务，启动子任务执行，阻塞以等待子任务的结果返回，相加后得到最终结果。同样，当子任务足够小时，通过查表得到其结果，以减小因过多地分割任务引起的性能降低。其中，我们用到了 RecursiveTask 提供的方法 `fork()` 和 `join()`。它们分别表示：子任务的异步执行和阻塞等待结果完成。

现在剩下的工作就是将 Fibonacci 提交到 ForkJoinPool 了，我们在一个 JUnit 的 `test` 方法中作了如下处理：

##### 清单 5\. 将 Fibonacci 提交到 ForkJoinPool

```
@Test
public void testFibonacci() throws InterruptedException, ExecutionException {
    ForkJoinTask<Integer> fjt = new Fibonacci(45);
    ForkJoinPool fjpool = new ForkJoinPool();
    Future<Integer> result = fjpool.submit(fjt);
 
    // do something
    System.out.println(result.get());
}
```

### 使用 CyclicAction 来处理循环任务

CyclicAction 的用法稍微复杂一些。如果一个复杂任务需要几个线程协作完成，并且线程之间需要在某个点等待所有其他线程到达，那么我们就能方便的用 CyclicAction 和 TaskBarrier 来完成。图 2 描述了使用 CyclicAction 和 TaskBarrier 的一个典型场景。

##### 图 2\. 使用 CyclicAction 和 TaskBarrier 执行多线程任务

![图 2. 使用 CyclicAction 和 TaskBarrier 执行多线程任务](https://www.ibm.com/developerworks/cn/java/j-lo-forkjoin/figure002.jpg)


继承自 CyclicAction 的子类需要 TaskBarrier 为每个任务设置不同的中止条件。从 CyclicAction 继承的子类需要重载 `protected void compute()` 方法，定义在 `barrier` 的每个步骤需要执行的动作。`compute()` 方法将被反复执行直到 `barrier` 的 `isTerminated()` 方法返回 `True`。TaskBarrier 的行为类似于 CyclicBarrier。下面，我们来看看如何使用 CyclicAction 的子类。

##### 清单 6\. 使用 CyclicAction 的子类

```
class ConcurrentPrint extends RecursiveAction {
    protected void compute() {
        TaskBarrier b = new TaskBarrier() {
            protected boolean terminate(int cycle, int registeredParties) {
                System.out.println("Cycle is " + cycle + ";"
                        + registeredParties + " parties");
                return cycle >= 10;
            }
        };
        int n = 3;
        CyclicAction[] actions = new CyclicAction[n];
        for (int i = 0; i < n; ++i) {
            final int index = i;
            actions[i] = new CyclicAction(b) {
                protected void compute() {
                    System.out.println("I'm working " + getCycle() + " "
                            + index);
                    try {
                        Thread.sleep(500);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            };
        }
        for (int i = 0; i < n; ++i)
            actions[i].fork();
        for (int i = 0; i < n; ++i)
            actions[i].join();
    }
}
```

在 [清单 6](#list6) 中，`CyclicAction[]` 数组建立了三个任务，打印各自的工作次数和序号。而在 `b.terminate()` 方法中，我们设置的中止条件表示重复 10 次计算后中止。现在剩下的工作就是将 ConcurrentPrint 提交到 ForkJoinPool 了。我们可以在 ForkJoinPool 的构造函数中指定需要的线程数目，例如 `ForkJoinPool(4)` 就表明线程池包含 4 个线程。我们在一个 JUnit 的 `test` 方法中运行 ConcurrentPrint 的这个循环任务：

##### 清单 7\. 运行 ConcurrentPrint 循环任务

```
@Test
public void testBarrier () throws InterruptedException, ExecutionException {
    ForkJoinTask fjt = new ConcurrentPrint();
    ForkJoinPool fjpool = new ForkJoinPool(4);
    fjpool.submit(fjt);
    fjpool.shutdown();
}
```

RecursiveTask 和 CyclicAction 两个例子的完整代码如下所示：

##### 清单 8\. RecursiveTask 和 CyclicAction 两个例子的完整代码

```
package tests;
 
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Future;
 
import jsr166y.forkjoin.CyclicAction;
import jsr166y.forkjoin.ForkJoinPool;
import jsr166y.forkjoin.ForkJoinTask;
import jsr166y.forkjoin.RecursiveAction;
import jsr166y.forkjoin.RecursiveTask;
import jsr166y.forkjoin.TaskBarrier;
 
import org.junit.Test;
 
class Fibonacci extends RecursiveTask<Integer> {
    final int n;
 
    Fibonacci(int n) {
        this.n = n;
    }
 
    private int compute(int small) {
        final int[] results = { 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89 };
        return results[small];
    }
 
    public Integer compute() {
        if (n <= 10) {
            return compute(n);
        }
        Fibonacci f1 = new Fibonacci(n - 1);
        Fibonacci f2 = new Fibonacci(n - 2);
        System.out.println("fork new thread for " + (n - 1));
        f1.fork();
        System.out.println("fork new thread for " + (n - 2));
        f2.fork();
        return f1.join() + f2.join();
    }
}
 
class ConcurrentPrint extends RecursiveAction {
    protected void compute() {
        TaskBarrier b = new TaskBarrier() {
            protected boolean terminate(int cycle, int registeredParties) {
                System.out.println("Cycle is " + cycle + ";"
                        + registeredParties + " parties");
                return cycle >= 10;
            }
        };
        int n = 3;
        CyclicAction[] actions = new CyclicAction[n];
        for (int i = 0; i < n; ++i) {
            final int index = i;
            actions[i] = new CyclicAction(b) {
                protected void compute() {
                    System.out.println("I'm working " + getCycle() + " "
                            + index);
                    try {
                        Thread.sleep(500);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            };
        }
        for (int i = 0; i < n; ++i)
            actions[i].fork();
        for (int i = 0; i < n; ++i)
            actions[i].join();
    }
}
 
public class TestForkJoin {
    @Test
    public void testBarrier () throws InterruptedException, ExecutionException {
        System.out.println("\ntesting Task Barrier ...");
        ForkJoinTask fjt = new ConcurrentPrint();
        ForkJoinPool fjpool = new ForkJoinPool(4);
        fjpool.submit(fjt);
        fjpool.shutdown();
    }
 
    @Test
    public void testFibonacci () throws InterruptedException, ExecutionException {
        System.out.println("\ntesting Fibonacci ...");
        final int num = 14; //For demo only
        ForkJoinTask<Integer> fjt = new Fibonacci(num);
        ForkJoinPool fjpool = new ForkJoinPool();
        Future<Integer> result = fjpool.submit(fjt);
 
        // do something
        System.out.println("Fibonacci(" + num + ") = " + result.get());
    }
}
```

运行以上代码，我们可以得到以下结果：

```
testing Task Barrier ...
I'm working 0 2
I'm working 0 0
I'm working 0 1
Cycle is 0; 3 parties
I'm working 1 2
I'm working 1 0
I'm working 1 1
Cycle is 1; 3 parties
I'm working 2 0
I'm working 2 1
I'm working 2 2
Cycle is 2; 3 parties
I'm working 3 0
I'm working 3 2
I'm working 3 1
Cycle is 3; 3 parties
I'm working 4 2
I'm working 4 0
I'm working 4 1
Cycle is 4; 3 parties
I'm working 5 1
I'm working 5 0
I'm working 5 2
Cycle is 5; 3 parties
I'm working 6 0
I'm working 6 2
I'm working 6 1
Cycle is 6; 3 parties
I'm working 7 2
I'm working 7 0
I'm working 7 1
Cycle is 7; 3 parties
I'm working 8 1
I'm working 8 0
I'm working 8 2
Cycle is 8; 3 parties
I'm working 9 0
I'm working 9 2
 
testing Fibonacci ...
fork new thread for 13
fork new thread for 12
fork new thread for 11
fork new thread for 10
fork new thread for 12
fork new thread for 11
fork new thread for 10
fork new thread for 9
fork new thread for 10
fork new thread for 9
fork new thread for 11
fork new thread for 10
fork new thread for 10
fork new thread for 9
Fibonacci(14) = 610
```

## 结论

从以上的例子中可以看到，通过使用 Fork/Join 模式，软件开发人员能够方便地利用多核平台的计算能力。尽管还没有做到对软件开发人员完全透明，Fork/Join 模式已经极大地简化了编写并发程序的琐碎工作。对于符合 Fork/Join 模式的应用，软件开发人员不再需要处理各种并行相关事务，例如同步、通信等，以难以调试而闻名的死锁和 data race 等错误也就不会出现，提升了思考问题的层次。你可以把 Fork/Join 模式看作并行版本的 Divide and Conquer 策略，仅仅关注如何划分任务和组合中间结果，将剩下的事情丢给 Fork/Join 框架。

在实际工作中利用 Fork/Join 模式，可以充分享受多核平台为应用带来的免费午餐。

* * *

#### 相关主题

*   阅读文章“[The Free Lunch Is Over: A Fundamental Turn Toward Concurrency in Software](http://www.ddj.com/web-development/184405990?pgno=1)”：了解为什么从现在开始每个严肃的软件工作者都应该了解并行编程方法。
*   阅读 Doug Lea 的文章“[A Java Fork/Join Framework](http://gee.cs.oswego.edu/dl/papers/fj.pdf)”：了解 Fork/Join 模式的实现机制和执行性能。
*   阅读 developerWorks 文章“[驯服 Tiger：并发集合](http://www.ibm.com/developerworks/cn/java/j-tiger06164/)”：了解如何使用并行 Collection 库。
*   阅读 developerWorks 文章“[Java 理论与实践：非阻塞算法简介](http://www.ibm.com/developerworks/cn/java/j-jtp04186/)”：介绍了 JDK 5 在并行方面的重要增强以及在 JDK5 平台上如何实现非阻塞算法的一般介绍。
*   书籍“[Java Concurrency in Practice](http://www.javaconcurrencyinpractice.com/)”：介绍了大量的并行编程技巧、反模式、可行的解决方案等，它对于 JDK 5 中的新特性也有详尽的介绍。
*   [访问](http://g.oswego.edu/dl/concurrency-interest/) Doug Lea 的 JSR 166 站点获得最新的源代码。
*   从 [Sun 公司](http://java.sun.com/) 网站下载 Java SE 6。
