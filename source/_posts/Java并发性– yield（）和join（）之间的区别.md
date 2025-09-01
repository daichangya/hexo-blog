---
title: Java并发性– yield（）和join（）之间的区别
id: 1261
date: 2024-10-31 22:01:50
author: daichangya
excerpt: "sleep执行后线程进入阻塞状态yield执行后线程进入就绪状态join执行后线程进入阻塞状态==Thread.wait(0)main(){      threadA.join(); //等线程A执行完，(main)我再执行,我先等等wait(0)      .............}"
permalink: /archives/java%E5%B9%B6%E5%8F%91%E6%80%A7yield%E5%92%8Cjoin%E4%B9%8B%E9%97%B4%E7%9A%84%E5%8C%BA%E5%88%AB/
categories:
 - java并发教程
---

长期以来，多线程是访问者中非常受欢迎的话题。虽然我个人觉得很少有人真正有机会从事复杂的多线程应用程序的工作（最近7年我只有一次机会），但仍然可以帮助您方便地使用这些概念，仅能增强您的信心。之前，我讨论了一个有关 wait（）和sleep（）方法之间差异的类似问题，这一次，我正在讨论 join（）和yield（）方法之间的差异。坦白地说，我在实践中并未同时使用这两种方法，因此，如果您在任何时候都感到不满意，请提出意见。

## A little background on java thread scheduling
需要Java虚拟机在其各个线程之间实施基于优先级的抢占式调度程序。这意味着为Java程序中的每个线程分配了一定的优先级，该优先级在明确定义的范围内。开发人员可以更改此优先级。Java虚拟机永远不会更改线程的优先级，即使该线程已经运行了一段时间。

优先级值很重要，因为Java虚拟机与基础操作系统之间的约定是，操作系统通常必须选择以最高优先级运行Java线程。这就是说Java实现基于优先级的调度程序时的意思。此调度程序以抢先方式实现，这意味着，当出现更高优先级的线程时，该线程会中断（抢占）当时运行的更低优先级的线程。但是，与操作系统的合同不是绝对的，这意味着操作系统有时可以选择运行优先级较低的线程。[ 我恨这个关于多线程..没有保证 ????]

>还要注意，java并不要求对其线程进行时间分段，但是大多数操作系统都这样做。这里的术语经常有一些混淆：抢占经常与时间片混淆。实际上，抢占仅意味着优先级较高的线程运行，而不是优先级较低的线程运行，但是当线程具有相同的优先级时，它们不会相互抢占。它们通常受时间限制，但这不是Java的要求。

## 了解线程优先级
了解线程优先级是学习多线程的下一个重要步骤，尤其是yield（）的工作方式。

1. 请记住，未指定优先级时，所有线程均具有正常优先级。
2. 可以在1到10之间指定优先级。10是最高优先级，1是最低优先级，5是正常优先级。
3. 请记住，优先级最高的线程将在执行时被赋予优先级。但是不能保证它一开始就处于运行状态。
4. 与正在等待机会的池中的线程相比，当前正在执行的线程始终始终具有更高的优先级。
5. 线程调度程序决定应该执行哪个线程。
6. t.setPriority（）可用于设置线程的优先级。
7. 请记住，应该在调用线程启动方法之前设置优先级。
8. 您可以使用常量MIN_PRIORITY，MAX_PRIORITY和NORM_PRIORITY设置优先级。
现在，当我们对线程调度和线程优先级有了一些基本了解时，让我们进入主题。

## yield（）方法
从理论上讲，“屈服”意味着放手，放弃，投降。产生线程告诉虚拟机，它愿意让其他线程在其位置进行调度。这表明它并没有做太重要的事情。注意，这只是一个提示，并不保证完全有效。

yield（）在Thread.java中定义如下。

```
/**
  * A hint to the scheduler that the current thread is willing to yield its current use of a processor. The scheduler is free to ignore
  * this hint. Yield is a heuristic attempt to improve relative progression between threads that would otherwise over-utilize a CPU. 
  * Its use should be combined with detailed profiling and benchmarking to ensure that it actually has the desired effect. 
  */
 
public static native void yield();
```
让我们从上面的定义中列出要点：

- 产量也是静态方法，也是本机方法。
- Yield告诉当前正在执行的线程给线程池中具有相同优先级的线程一个机会。
- 无法保证Yield将使当前正在执行的线程立即变为可运行状态。
- 它只能使线程从运行状态变为可运行状态，而不能处于等待或阻塞状态。
## yield（）方法示例用法
在下面的示例程序中，我创建了两个没有特定原因的线程，分别称为生产者和消费者。生产者设置为最小优先级，而消费者设置为最大优先级。我将在有/无注释行Thread.yield（）的情况下运行以下代码。没有yield（）时，尽管输出有时会更改，但是通常首先打印所有使用者行，然后才打印所有生产者行。

使用yield（）方法，两者都一次打印一行，并且几乎总是将机会传递给另一线程。

```
package com.daicy.concurrency.thread;

/**
 * @author: create by daichangya
 * @version: v1.0
 * @description: com.daicy.concurrency.thread
 * @date:20-4-17
 */
public class YieldTest {
    public static void main(String[] args) {
        Thread producer = new Producer();
        Thread consumer = new Consumer();

        producer.setPriority(Thread.MIN_PRIORITY); //Min Priority
        consumer.setPriority(Thread.MAX_PRIORITY); //Max Priority

        producer.start();
        consumer.start();
    }
}

class Producer extends Thread {
    public void run() {
        for (int i = 0; i < 5; i++) {
            System.out.println("I am Producer : Produced Item " + i);
            Thread.yield();
        }
    }
}

class Consumer extends Thread {
    public void run() {
        for (int i = 0; i < 5; i++) {
            System.out.println("I am Consumer : Consumed Item " + i);
            Thread.yield();
        }
    }
}
```
#### Output of above program “without” yield() method
```
I am Producer : Produced Item 0
I am Producer : Produced Item 1
I am Producer : Produced Item 2
I am Producer : Produced Item 3
I am Producer : Produced Item 4
I am Consumer : Consumed Item 0
I am Consumer : Consumed Item 1
I am Consumer : Consumed Item 2
I am Consumer : Consumed Item 3
I am Consumer : Consumed Item 4
```
Output of above program “with” yield() method added
```
I am Producer : Produced Item 0
I am Consumer : Consumed Item 0
I am Producer : Produced Item 1
I am Consumer : Consumed Item 1
I am Producer : Produced Item 2
I am Consumer : Consumed Item 2
I am Producer : Produced Item 3
I am Consumer : Consumed Item 3
I am Producer : Produced Item 4
I am Consumer : Consumed Item 4
```
## join（）方法
线程实例的join（）方法可用于将线程执行的开始“联接”到另一个线程的执行的结束，以便线程在另一个线程结束之前不会开始运行。如果在Thread实例上调用join（），则当前正在运行的线程将阻塞，直到Thread实例完成执行。
```
//Waits for this thread to die. 
 
public final void join() throws InterruptedException
```
在join（）中设置超时，将使特定超时后的join（）效果无效。当达到超时时，主线程和taskThread是执行任务的同等可能性。但是，与睡眠一样，join的运行时间也取决于操作系统，因此，您不应假定join会完全按照您指定的时间等待。

像睡眠一样，join通过退出InterruptedException来响应中断。

## join（）方法示例用法
```
package com.daicy.concurrency.thread;

/**
 * @author: create by daichangya
 * @version: v1.0
 * @description: com.daicy.concurrency.thread
 * @date:20-4-17
 */
public class JoinTest {
    public static void main(String[] args) throws InterruptedException {
        Thread t = new Thread(new Runnable() {
            public void run() {
                System.out.println("First task started");
                System.out.println("Sleeping for 2 seconds");
                try {
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("First task completed");
            }
        });
        Thread t1 = new Thread(new Runnable() {
            public void run() {
                System.out.println("Second task completed");
            }
        });
        t.start(); // Line 15
        t.join(); // Line 16 我先执行,你等等 t.wait(0)
        t1.start();
    }
}
```
 
Output:
 
First task started
Sleeping for 2 seconds
First task completed
Second task completed
仅此一个很小但很重要的概念。在评论部分让我知道您的想法。

学习愉快！