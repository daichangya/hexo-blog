---
title: Java多线程设计模式(两阶段终止模式)
id: 230
date: 2024-10-31 22:01:41
author: daichangya
excerpt: '一 Two-Phase Termination Pattern

  Two-Phase Termination Pattern,指的就是当希望结束一个线程的时候，送出一个终止请求，但是不会马上停止，做一些刷新工作。进入“终止处理中”，在该状态下，不会进行该线程日常工作任务的操作，而是进行一些终止操作。

  这个方式所考虑的因素如下：

  1，必须要考虑到使得该线程能够安全的结束'
permalink: /archives/Java-duo-xian-cheng-she-ji-mo-shi-liang/
categories:
- 多线程-并发
- 设计模式
---

**一 Two-Phase Termination Pattern**

  Two-Phase Termination Pattern,指的就是当希望结束一个线程的时候，送出一个终止请求，但是不会马上停止，做一些刷新工作。进入“终止处理中”，在该状态下，不会进行该线程日常工作任务的操作，而是进行一些终止操作。

   **这个方式所考虑的因素如下**：

  **1，必须要考虑到使得该线程能够安全的结束**，Thread中的stop会有问题的，因为它会不管线程执行到哪里，都会马上停止，不能保证安全的结束。

  **2，一定能够进行正常的终止处理**，在java中，这点可以使用**finally**来实现

  **3，能够高响应的终止**，收到终止后，当线程在wait或者sleep或者join的时候，不用等到时间到才终止，而是马上中断线程的这些状态，进而进行终止操作。

   当一个线程正在执行周期性的工作时候，在“作业中”发了停止执行绪的请求，此时该线程不能马上离开停止，而应该先做完本次周期内部的工作，然后进入“善后阶段”完成一些善后的工作，所谓的两阶段终止，即中止“运作阶段”，并完成“善后阶段”，完整的完成执行绪的工作。

两阶段终止线程的架构模式如下：

```
public class WorkerTerminalThread extends Thread {
    // 已经送出终止请求为true，初始化的时候为false
    //由于该字段可能会被多个线程访问修改，为了保护就使用这个
    private volatile boolean shutdownRequested = false;

    // 终止请求
    public void shutdownRequest() {
        shutdownRequested = true;
        interrupt();
    }

    public boolean isShutdownRequest() {
        return shutdownRequested;
    }

    // 具体动作
    public final void run() {
        try {
            while (!shutdownRequested)
                doWork();
        } catch (InterruptedException e) {
        }
        // 终止处理中的工作，不会进行平常操作，但是会进行终止处理
        finally {
            doShutdown();
        }
    }

    // 具体工作操作
    private void doWork() throws InterruptedException {
    }

    // 终止后进行善后处理
    private void doShutdown() {
    }
}
```

**解释：**

  1，利用Volatile的原因是，这个字段可能会被多个线程所使用，进行修改，为了保护该字段，则可以利用同步方法或者同步代码块来保护，或者利用Volatile。用Volatile修饰的字段，强制了该成员变量在每次被线程访问时，都强迫从共享内存中重读该成员变量的值。而且，当成员变量发生变化时，强迫线程将变化值回写到共享内存。这样在任何时刻，两个不同的线程总是看到某个成员变量的同一个值。

  2，这里运用了标识和中断状态来终止线程，之所以不单独用一个。原因是如果仅仅利用标识，无法是的那些处于wait、sleep或者join中的线程马上停止，响应性就会很差。加入了interrupt后，就可以立刻使得这些状态下的线程中断。如果仅仅利用interrupt，由于interrupt仅仅对于wait，sleep或join处进行抛出异常，如果工作代码执行在catch里，捕获了InterruptedException后，则此时interrupt就不起作用了。