---
title: JAVA并发编程学习笔记之AQS源码分析
id: 1145
date: 2024-10-31 22:01:49
author: daichangya
excerpt: "同步状态AQS采用的是CLH队列，CLH队列是由一个一个结点构成的，前面提到结点中有一个状态位，这个状态位与线程状态密切相关，这个状态位(waitStatus)是一个32位的整型常量，它的取值如下："
permalink: /archives/15856563/
categories:
 - 多线程-并发
---

## 同步状态

AQS采用的是CLH队列，CLH队列是由一个一个结点构成的，前面提到结点中有一个状态位，这个状态位与线程状态密切相关，这个状态位(waitStatus)是一个32位的整型常量，它的取值如下：

```java
static final int CANCELLED =  1;
static final int SIGNAL    = -1;
static final int CONDITION = -2;
static final int PROPAGATE = -3;
```

下面解释一下每个值的含义

CANCELLED：因为超时或者中断，结点会被设置为取消状态，被取消状态的结点不应该去竞争锁，只能保持取消状态不变，不能转换为其他状态。处于这种状态的结点会被踢出队列，被GC回收；

SIGNAL：表示这个结点的继任结点被阻塞了，到时需要通知它；

CONDITION：表示这个结点在条件队列中，因为等待某个条件而被阻塞；

PROPAGATE：使用在共享模式头结点有可能牌处于这种状态，表示锁的下一次获取可以无条件传播；

0：None of the above，新结点会处于这种状态。

  

## 获取

AQS中比较重要的两个操作是获取和释放，以下是各种获取操作：  

```java
public final void acquire(int arg);
public final void acquireInterruptibly(int arg);
public final void acquireShared(int arg);
public final void acquireSharedInterruptibly(int arg);
protected boolean tryAcquire(int arg); 
protected int tryAcquireShared(int arg);
public final boolean tryAcquireNanos(int arg, long nanosTimeout) throws InterruptedException;
public final boolean tryAcquireSharedNanos(int arg, long nanosTimeout) throws InterruptedException;		
```

获取操作的流程图如下：  

![](https://img-my.csdn.net/uploads/201205/13/1336904890_5310.jpg)

1、如果尝试获取锁成功整个获取操作就结束，否则转到2. 尝试获取锁是通过方法tryAcquire来实现的，AQS中并没有该方法的具体实现，只是简单地抛出一个不支持操作异常，在AQS简介中谈到tryAcquire有很多实现方法，这里不再细化，只需要知道如果获取锁成功该方法返回true即可；

2、如果获取锁失败，那么就创建一个代表当前线程的结点加入到等待队列的尾部，是通过addWaiter方法实现的，来看该方法的具体实现：

```java
    /**
     * Creates and enqueues node for current thread and given mode.
     *
     * @param mode Node.EXCLUSIVE for exclusive, Node.SHARED for shared
     * @return the new node
     */
    private Node addWaiter(Node mode) {
        Node node = new Node(Thread.currentThread(), mode);
        // Try the fast path of enq; backup to full enq on failure
        Node pred = tail;
        if (pred != null) {
            node.prev = pred;
            if (compareAndSetTail(pred, node)) {
                pred.next = node;
                return node;
            }
        }
        enq(node);
        return node;
    }
```

该方法创建了一个独占式结点，然后判断队列中是否有元素，如果有（pred!=null）就设置当前结点为队尾结点，返回；

如果没有元素（pred==null），表示队列为空，走的是入队操作

```java
    /**
     * Inserts node into queue, initializing if necessary. See picture above.
     * @param node the node to insert
     * @return node's predecessor
     */
    private Node enq(final Node node) {
        for (;;) {
            Node t = tail;
            if (t == null) { // Must initialize
                if (compareAndSetHead(new Node()))
                    tail = head;
            } else {
                node.prev = t;
                if (compareAndSetTail(t, node)) {
                    t.next = node;
                    return t;
                }
            }
        }
    }
```

enq方法采用的是变种CLH算法，先看头结点是否为空，如果为空就创建一个傀儡结点，头尾指针都指向这个傀儡结点，这一步只会在队列初始化时会执行；

如果头结点非空，就采用CAS操作将当前结点插入到头结点后面，如果在插入的时候尾结点有变化，就将尾结点向后移动直到移动到最后一个结点为止，然后再把当前结点插入到尾结点后面，尾指针指向当前结点，入队成功。

3、将新加入的结点放入队列之后，这个结点有两种状态，要么获取锁，要么就挂起，如果这个结点不是头结点，就看看这个结点是否应该挂起，如果应该挂起，就挂起当前结点，是否应该挂起是通过shouldParkAfterFailedAcquire方法来判断的

```java
 /**
     * Checks and updates status for a node that failed to acquire.
     * Returns true if thread should block. This is the main signal
     * control in all acquire loops.  Requires that pred == node.prev
     *
     * @param pred node's predecessor holding status
     * @param node the node
     * @return {@code true} if thread should block
     */
    private static boolean shouldParkAfterFailedAcquire(Node pred, Node node) {
        int ws = pred.waitStatus;
        if (ws == Node.SIGNAL)
            /*
             * This node has already set status asking a release
             * to signal it, so it can safely park.
             */
            return true;
        if (ws > 0) {
            /*
             * Predecessor was cancelled. Skip over predecessors and
             * indicate retry.
             */
            do {
                node.prev = pred = pred.prev;
            } while (pred.waitStatus > 0);
            pred.next = node;
        } else {
            /*
             * waitStatus must be 0 or PROPAGATE.  Indicate that we
             * need a signal, but don't park yet.  Caller will need to
             * retry to make sure it cannot acquire before parking.
             */
            compareAndSetWaitStatus(pred, ws, Node.SIGNAL);
        }
        return false;
    }
```

该方法首先检查前趋结点的waitStatus位，如果为SIGNAL,表示前趋结点会通知它，那么它可以放心大胆地挂起了；

如果前趋结点是一个被取消的结点怎么办呢？那么就向前遍历跳过被取消的结点，直到找到一个没有被取消的结点为止，将找到的这个结点作为它的前趋结点，将找到的这个结点的waitStatus位设置为SIGNAL,返回false表示线程不应该被挂起。  
上面谈的不是头结点的情况决定是否应该挂起，是头结点的情况呢？

是头结点的情况，当前线程就调用tryAcquire尝试获取锁，如果获取成功就将头结点设置为当前结点，返回；如果获取失败就循环尝试获取锁，直到获取成功为止。整个acquire过程就分析完了。

  

## 释放

释放操作有以下方法：

```java
public final boolean release(int arg); 
protected boolean tryRelease(int arg); 
protected boolean tryReleaseShared(int arg); 
```

下面看看release方法的实现过程

![](https://img-my.csdn.net/uploads/201205/13/1336907071_3068.jpg)  

1、release过程比acquire要简单，首先调用tryRelease释放锁，如果释放失败，直接返回；

2、释放锁成功后需要唤醒继任结点，是通过方法unparkSuccessor实现的

```java
 /**
     * Wakes up node's successor, if one exists.
     *
     * @param node the node
     */
    private void unparkSuccessor(Node node) {
        /*
         * If status is negative (i.e., possibly needing signal) try
         * to clear in anticipation of signalling.  It is OK if this
         * fails or if status is changed by waiting thread.
         */
        int ws = node.waitStatus;
        if (ws < 0)
            compareAndSetWaitStatus(node, ws, 0);
 
        /*
         * Thread to unpark is held in successor, which is normally
         * just the next node.  But if cancelled or apparently null,
         * traverse backwards from tail to find the actual
         * non-cancelled successor.
         */
        Node s = node.next;
        if (s == null || s.waitStatus > 0) {
            s = null;
            for (Node t = tail; t != null && t != node; t = t.prev)
                if (t.waitStatus <= 0)
                    s = t;
        }
        if (s != null)
            LockSupport.unpark(s.thread);
    }
```

1、node参数传进来的是头结点，首先检查头结点的waitStatus位，如果为负，表示头结点还需要通知后继结点，这里不需要头结点去通知后继，因此将该该标志位清0.

2、然后查看头结点的下一个结点，如果下一个结点不为空且它的waitStatus<=0,表示后继结点没有被取消，是一个可以唤醒的结点，于是唤醒后继结点返回；如果后继结点为空或者被取消了怎么办？寻找下一个可唤醒的结点，然后唤醒它返回。

这里并没有从头向尾寻找，而是相反的方向寻找，为什么呢？

因为在CLH队列中的结点随时有可能被中断，被中断的结点的waitStatus设置为CANCEL,而且它会被踢出CLH队列，如何个踢出法，就是它的前趋结点的next并不会指向它，而是指向下一个非CANCEL的结点,而它自己的next指针指向它自己。一旦这种情况发生，如何从头向尾方向寻找继任结点会出现问题，因为一个CANCEL结点的next为自己，那么就找不到正确的继任接点。

有的人又会问了，CANCEL结点的next指针为什么要指向它自己，为什么不指向真正的next结点？为什么不为NULL？

第一个问题的答案是这种被CANCEL的结点最终会被GC回收，如果指向next结点，GC无法回收。

对于第二个问题的回答，JDK中有这么一句话： The next field of cancelled nodes is set to point to the node itself instead of null, to make life easier for isOnSyncQueue.大至意思是为了使isOnSyncQueue方法更新简单。isOnSyncQueue方法判断一个结点是否在同步队列，实现如下：

```java
    /**
     * Returns true if a node, always one that was initially placed on
     * a condition queue, is now waiting to reacquire on sync queue.
     * @param node the node
     * @return true if is reacquiring
     */
    final boolean isOnSyncQueue(Node node) {
        if (node.waitStatus == Node.CONDITION || node.prev == null)
            return false;
        if (node.next != null) // If has successor, it must be on queue
            return true;
        /*
         * node.prev can be non-null, but not yet on queue because
         * the CAS to place it on queue can fail. So we have to
         * traverse from tail to make sure it actually made it.  It
         * will always be near the tail in calls to this method, and
         * unless the CAS failed (which is unlikely), it will be
         * there, so we hardly ever traverse much.
         */
        return findNodeFromTail(node);
    }
```

如果一个结点next不为空，那么它在同步队列中，如果CANCEL结点的后继为空那么CANCEL结点不在同步队列中，这与事实相矛盾。

因此将CANCEL结点的后继指向它自己是合理的选择。

  

### 参考资料：

[The java.util.concurrent Synchronizer Framework](http://gee.cs.oswego.edu/dl/papers/aqs.pdf)  

[java.util.concurrent 包下的 Synchronizer 框架](http://bruce008.iteye.com/blog/1482115)