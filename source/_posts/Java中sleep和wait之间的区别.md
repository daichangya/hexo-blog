---
title: Java中sleep（）和wait（）之间的区别
id: 1263
date: 2024-10-31 22:01:50
author: daichangya
excerpt: " Java sleep（）和wait（）–讨论sleep（）是一种用于暂停该过程几秒钟或我们想要的时间的方法。但是在使用wait（）方法的情况下，线程进入等待状态，直到我们调用notify()or ，线程才会自动返回notifyAll()。主要区别在于等待wait()时sleep()不释放锁定或监视器，而等待时不释放锁定或监视器。wait()通常用于线程间通信，而sleep()通常用于引入执行暂停。Thread.sleep（）将当前线程发送到“ Not Runnable ”状态一段时间。该线程保留已获取的监视器，即，如果该线程当前在某个synchronized块或方法中，则没有其他线程可以进入该块或方法。如果另一个线程调用t.interrupt()。它将唤醒睡眠线程。While sleep()是一种static方法，这意味着它始终会影响当前线程（正在执行sleep方法的线程）。一个常见的错误是调用t.sleep()where t是另一个线程。即使这样，当前线程也会进入休眠状态，而不是t线程。"
permalink: /archives/java%E4%B8%ADsleep%E5%92%8Cwait%E4%B9%8B%E9%97%B4%E7%9A%84%E5%8C%BA%E5%88%AB/
categories:
 - java并发教程
---

了解Java中sleep（）和wait（）方法之间的区别。了解何时使用哪种方法以及它们对Java并发带来什么影响。

## 1. Java sleep（）和wait（）–讨论
sleep（）是一种用于暂停该过程几秒钟或我们想要的时间的方法。但是在使用wait（）方法的情况下，线程进入等待状态，直到我们调用notify()or ，线程才会自动返回notifyAll()。

主要区别在于等待wait()时sleep()不释放锁定或监视器，而等待时不释放锁定或监视器。wait()通常用于线程间通信，而sleep()通常用于引入执行暂停。

Thread.sleep（）将当前线程发送到“ Not Runnable ”状态一段时间。该线程保留已获取的监视器，即，如果该线程当前在某个synchronized块或方法中，则没有其他线程可以进入该块或方法。如果另一个线程调用t.interrupt()。它将唤醒睡眠线程。

While sleep()是一种static方法，这意味着它始终会影响当前线程（正在执行sleep方法的线程）。一个常见的错误是调用t.sleep()where t是另一个线程。即使这样，当前线程也会进入休眠状态，而不是t线程。

阅读更多：使用wait（）和notify（）

## 2. Java sleep（）和wait（）–示例
sleep（）示例
```
synchronized(LOCK) {   
    Thread.sleep(1000); // LOCK is held
}
```
wait（）示例
```
synchronized(LOCK) 
{   
    LOCK.wait(); // LOCK is not held
}
```
阅读更多：yield（）和join（）之间的区别

## 3. Java sleep（）vs wait（）–摘要
简而言之，让我们对以上所有要点进行分类以记住。

#### 3.1. Method called on
- wait()–调用对象；当前线程必须在锁对象上同步。
- sleep()–调用线程；始终当前正在执行的线程。
#### 3.2. Synchronized
- wait() –同步时，多个线程将一一访问同一对象。
- sleep() –同步时，多个线程等待休眠线程的休眠。
#### 3.3. Lock duration(锁定时间)
- wait() –释放锁，以使其他对象有机会执行。
- sleep() –如果指定了超时或有人中断，请保持锁定至少t次。
#### 3.4. wake up condition(唤醒条件)
- wait() –直到从对象调用notify（），notifyAll（）
- sleep() –直到至少时间到期或调用interrupt（）。
#### 3.5. Usage(用法)
- sleep() –用于时间同步
- wait() –用于多线程同步。
希望以上信息将为您的知识库增加一些价值。

学习愉快！