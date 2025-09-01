---
title: AbstractQueuedSynchronizer源码解析之ReentrantLock
id: 796
date: 2024-10-31 22:01:46
author: daichangya
excerpt: 可以看到公平锁与非公平锁，包括ReentrantLock都是在它的基础上实现的公平锁：每个线程抢占锁的顺序为先后调用lock方法的顺序，依次获取锁。非公平锁：每个线程抢占锁的顺序不定，谁运气好，谁就获取到锁，和调用lock方法的先后顺序无关（但因为抢占锁失败而加入到等待队列的线程不能参与下一次抢占，直到被unpark）
permalink: /archives/AbstractQueuedSynchronizer-yuan-ma-jie/
categories:
- java源码分析
- 多线程-并发
---


以下为部分重点摘录

![在这里插入图片描述](https://img-blog.csdnimg.cn/20191109164102907.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxcXFxMTk5M3FxcXFx,size_16,color_FFFFFF,t_70)  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191109164123951.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxcXFxMTk5M3FxcXFx,size_16,color_FFFFFF,t_70)

* * *

#### 前言

AbstractQueuedSynchronizer在JDK1.8中还有如下图所示的众多子类：  
![这里写图片描述](https://imgconvert.csdnimg.cn/aHR0cDovL2ltZy5ibG9nLmNzZG4ubmV0LzIwMTcwODA4MjE1NDE0ODQx)

可以看到公平锁与非公平锁，包括ReentrantLock都是在它的基础上实现的

公平锁：每个线程抢占锁的顺序为先后调用lock方法的顺序，依次获取锁。

非公平锁：每个线程抢占锁的顺序不定，谁运气好，谁就获取到锁，和调用lock方法的先后顺序无关（但因为抢占锁失败而加入到等待队列的线程不能参与下一次抢占，直到被unpark）

* * *

#### AQS结构

AQS通过内置的FIFO同步队列来完成资源获取线程的排队工作，如果当前线程获取同步状态失败（锁）时，AQS则会将当前线程以及等待状态等信息构造成一个节点（Node）并将其加入同步队列，同时会阻塞当前线程，当同步状态释放时，则会把节点中的线程唤醒，使其再次尝试获取同步状态。

```
public abstract class AbstractQueuedSynchronizer
    extends AbstractOwnableSynchronizer
    implements java.io.Serializable {
    protected AbstractQueuedSynchronizer() { }
    //同步器队列头结点
    private transient volatile Node head;
    //同步器队列尾结点
    private transient volatile Node tail;
    //同步状态（当state为0时，无锁，当state>0时说明有锁。）
    private volatile int state;
    //获取锁状态
    protected final int getState() {
        return state;
    }
    //设置锁状态
    protected final void setState(int newState) {
        state = newState;
    }

```

通过AQS的类结构我们可以看到它内部有一个队列和一个state的int变量。  
队列：通过一个双向链表实现的队列来存储等待获取锁的线程。  
state：锁的状态。  
head、tail和state 都是volatile类型的变量，volatile可以保证多线程的内存可见性。

同步队列的基本结构如下：  
![这里写图片描述](https://imgconvert.csdnimg.cn/aHR0cDovL3VwbG9hZC1pbWFnZXMuamlhbnNodS5pby91cGxvYWRfaW1hZ2VzLzI4NDMyMjQtZGY2ZGU0ZTYxODYyNWFmZC5wbmc)

```
static final class Node {
    static final Node SHARED = new Node();
    static final Node EXCLUSIVE = null;
    //表示当前的线程被取消；
    static final int CANCELLED =  1;
    //表示当前节点的后继节点包含的线程需要运行，也就是unpark；
    static final int SIGNAL    = -1;
    //表示当前节点在等待condition，也就是在condition队列中；
    static final int CONDITION = -2;
    //表示当前场景下后续的acquireShared能够得以执行；
    static final int PROPAGATE = -3;
    //表示节点的状态。默认为0，表示当前节点在sync队列中，等待着获取锁。
    //其它几个状态为：CANCELLED、SIGNAL、CONDITION、PROPAGATE
    volatile int waitStatus;
    //前驱节点
    volatile Node prev;
    //后继节点
    volatile Node next;
    //获取锁的线程
    volatile Thread thread;
    //存储condition队列中的后继节点。
    Node nextWaiter;
}

```

1.  Node节点中，除了存储当前线程，节点类型，队列中前后元素的变量，还有一个叫waitStatus的变量，该变量用于描述节点的状态，为什么需要这个状态呢？  
    原因是：AQS的队列中，在有并发时，肯定会存取一定数量的节点，每个节点 代表了一个线程的状态，有的线程可能“等不及”获取锁了，需要放弃竞争，退出队列，有的线程在等待一些条件满足，满足后才恢复执行（这里的描述很像某个J.U.C包下的工具类，ReentrankLock的Condition，事实上，Condition同样也是AQS的子类）等等，总之，各个线程有各个线程的状态，但总需要一个变量来描述它，这个变量就叫waitStatus,它有四种状态：

```
static final int CANCELLED =  1;
static final int SIGNAL    = -1;
static final int CONDITION = -2;
static final int PROPAGATE = -3;

```

![这里写图片描述](https://imgconvert.csdnimg.cn/aHR0cDovL2ltZy5ibG9nLmNzZG4ubmV0LzIwMTcwODA5MjAyNTUxNzYz)  
CANCELLED：因为超时或者中断，结点会被设置为取消状态，被取消状态的结点不应该去竞争锁，只能保持取消状态不变，不能转换为其他状态。处于这种状态的结点会被踢出队列，被GC回收；  
SIGNAL：表示这个结点的继任结点被阻塞了，所以自己被释放或取消的时候需要通知继任节点；  
CONDITION：表示这个结点在条件队列中，因为等待某个条件而被阻塞，它不会被作为同步节点直到其状态被置为0；  
PROPAGATE：使用在共享模式头结点有可能处于这种状态，表示锁的下一次获取可以无条件传播；  
0：None of the above，新结点会处于这种状态。

* * *

#### 应用之——公平锁

##### 公平锁的获取锁

```
final void lock() {
            acquire(1);
        }

```

调用到了AQS的acquire方法：

```
    public final void acquire(int arg) {
        if (!tryAcquire(arg) &&
            acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
            selfInterrupt(); // 自己给自己设置了一个中断标志，只有之前被中断过，前面才会返回true，这里相当于重新设置一个中断标志
    }

```

从方法名字上看，语义是，尝试获取一把锁，如果获取不到尝试将该线程（这里是类为Node的一个对象，等待队列的形式是将Node以队列的形式串起来，其中每一个Node类里都有一个线程）放到waiter队列中。（利用&&实现了短路性质）

```
    protected boolean tryAcquire(int arg) {
        throw new UnsupportedOperationException();
    }

```

AQS中这个方法留空了，是想留给子类去实现（**设计理念**：既然要给子类实现，应该用抽象方法，但是Doug Lea没有这么做，原因是AQS有两种功能，面向两种使用场景，需要给子类定义的方法都是抽象方法了，会导致子类无论如何都需要实现另外一种场景的抽象方法，显然，这对子类来说是不友好的。）

看下FairSync的tryAcquire方法：

```
protected final boolean tryAcquire(int acquires) {
	final Thread current = Thread.currentThread();//获取当前线程
	int c = getState();  //获取父类AQS中的标志位
	if (c == 0) {　// 0意味着锁还在
		if (!hasQueuedPredecessors() &&//如果前面没有已在队列中的线程！
			compareAndSetState(0, acquires)) { //修改一下状态位，注意：这里的acquires是在lock的时候传递来的，从上面的图中可以知道，这个值是写死的1
			setExclusiveOwnerThread(current);//如果通过CAS操作将状态位更新成功则代表当前线程获取锁，因此，将当前线程设置到AQS的一个变量中，说明这个线程拿走了锁。
			return true;
		}
	}
	else if (current == getExclusiveOwnerThread()) {//如果不为0意味着，锁已经被拿走了，但是，因为ReentrantLock是重入锁，是可以重复lock,unlock的，所以这里还要再判断一次 获取锁的线程是不是当前请求锁的线程。
		int nextc = c + acquires;//如果是的，累加在state字段上就可以了。
		if (nextc < 0) // 重入次数太多，溢出了
			throw new Error("Maximum lock count exceeded");
		setState(nextc);
		return true;
	}
	return false;
}

```

```
    public final boolean hasQueuedPredecessors() {
        // The correctness of this depends on head being initialized
        // before tail and on head.next being accurate if the current
        // thread is first in queue.
        Node t = tail; // Read fields in reverse initialization order
        Node h = head;
        Node s;
        return h != t &&
            ((s = h.next) == null || s.thread != Thread.currentThread());
    }

```

到此，如果获取锁，tryAcquire返回true，反之，返回false。回到AQS的acquire方法

如果没有获取到锁，按照我们的描述，应该讲当前线程放到队列中去，只不过，在放之前，需要做些包装。

```
    public final void acquire(int arg) {
        if (!tryAcquire(arg) &&
            acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
            selfInterrupt();
    }

```

```
    /**
     * Creates and enqueues node for current thread and given mode.
     *用当前线程去构造一个Node对象，mode是一个表示Node类型的字段，仅仅表示这个节点是独占的，还是共享的，或者说，AQS的这个队列中，哪些节点是独占的，哪些是共享的。
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

创建好节点后，将节点加入到队列尾部，此处，在队列不为空的时候，先尝试通过cas方式修改尾节点为最新的节点，如果修改失败，意味着有并发，这个时候才会进入enq中死循环，“自旋”方式（死循环直到return）修改。

```
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

在解释acquireQueued之前，我们需要先看下AQS中队列的内存结构，我们知道，队列由Node类型的节点组成，其中至少有两个变量，一个封装线程，一个封装节点类型。  
而实际上，它的内存结构是这样的（第一次节点插入时，第一个节点是一个空节点，代表有一个线程已经获取锁，事实上，队列的第一个节点就是代表持有锁的节点）：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190821110247932.png)

黄色节点为队列默认的头节点，每次有线程竞争失败，进入队列后其实都是插入到队列的尾节点（tail节点）后面。

```
    final boolean acquireQueued(final Node node, int arg) {
        boolean failed = true;
        try {
            boolean interrupted = false;
            for (;;) {
                final Node p = node.predecessor(); // 前任节点
                if (p == head && tryAcquire(arg)) { //如果当前的节点的前一个节点是head，说明他是队列中第一个“有效的”节点，因此尝试获取锁，上文中有提到这个类是交给子类去扩展的。
                    setHead(node);//成功后，将上图中的黄色节点移除，node变成头节点。
                    p.next = null; // help GC
                    failed = false;
                    return interrupted;
                }
            //如果p节点不是头节点，或者tryAcquire返回false，说明请求失败。  
            //那么首先需要判断请求失败后node节点是否应该被阻塞，如果应该  
            //被阻塞，那么阻塞node节点，并检测中断状态。 
                if (shouldParkAfterFailedAcquire(p, node) &&
                    parkAndCheckInterrupt())//如果需要，借助JUC包下的LockSopport类的静态方法Park挂起当前线程。直到被唤醒。
                    interrupted = true;
            }
        } finally {
            if (failed)//如果有异常
                cancelAcquire(node);// 取消请求，对应到队列操作，就是将当前节点从队列中移除。
        }
    }

```

判断是否应该被挂起（当且仅当前一个节点是signal状态时，才会return true，这之后才会执行挂起方法；若返回false，则跳出上面的if判定，会继续自旋）

```
    private static boolean shouldParkAfterFailedAcquire(Node pred, Node node) {
        int ws = pred.waitStatus;
        if (ws == Node.SIGNAL) // 如果这一步不满足，都会return false
            /*
             * 前一节点已经设置了signal状态，释放锁后会通知后继节点
             * 所以可以安全挂起
             */
            return true;
        if (ws > 0) {
            /*
            判断如果前驱节点状态为CANCELLED，那就一直往前找，直到找到最近一个正常等待的状态
             */
            do {
                node.prev = pred = pred.prev;
            } while (pred.waitStatus > 0);
            //放置在其后面
            pred.next = node;
        } else {
            /*
             * waitStatus must be 0 or PROPAGATE.  Indicate that we
             * need a signal, but don't park yet.  Caller will need to
             * retry to make sure it cannot acquire before parking.
             */
            //如果前驱节点正常，则修改前驱节点状态为SIGNAL 
            compareAndSetWaitStatus(pred, ws, Node.SIGNAL);
        }
        return false;
    }

```

```
     /* 
     * 为什么不关心是否成功却还要设置呢？ 
     * 
     * 如果设置失败，表示前驱已经被signal了。如果前驱是head，说明有机会获取锁，所以返回false后还可以再次tryAcquire 
     * 
     * 如果设置成功，表示前驱等待signal。如果再次确认pred.waitStatus仍然是Node.SIGNAL，则表明前驱等待释放锁的情况下必须阻塞当前线程 
     * 所以返回true后即被park 
     */  

```

```
    private final boolean parkAndCheckInterrupt() {
        LockSupport.park(this);
        return Thread.interrupted(); // 返回在这过程中是否被中断过，如果是，返回true，同时将interrupted标志（acquireQueued方法中）设为true
    }

```

**在acquireQueued方法中，当前线程通过自旋的方式来尝试获取同步状态，**

当前节点的前驱节点为头节点才能尝试获得锁，如果获得成功，则把当前线程设置成头结点，把之前的头结点从队列中移除，等待垃圾回收（没有对象引用）

如果获取锁失败则进入shouldParkAfterFailedAcquire方法中检测当前节点是否可以被安全的挂起（阻塞），如果可以安全挂起则进入parkAndCheckInterrupt方法，把当前线程挂起，并将interrupted置为true。

挂起的线程被唤醒后，继续在acquireQueued的for死循环中运行，直到获取锁后可以跳出循环。

（待验证结论）没有获得锁的线程，有可能在下次获得锁之前都不会被挂起。因为无法被安全挂起时，会把节点移到前驱节点为signal的节点后（这样下次就可以安全挂起了），然后再进行自旋，有可能在自旋的过程中，该节点已经成为了头结点后的节点，因此可以直接尝试获取锁而避免被挂起。

* * *

##### 公平锁的释放锁阶段

（似乎非公平锁调用的是同一个方法）

```
    public void unlock() {
        sync.release(1);
    }

```

```
    public final boolean release(int arg) {
        if (tryRelease(arg)) {
            Node h = head;
            // 0是初始值，不对应某个具体状态，所以不能为0
            if (h != null && h.waitStatus != 0)
                unparkSuccessor(h);
            return true;
        }
        return false;
    }

```

unlock方法调用了AQS的release方法，同样传入了参数1，和获取锁的相应对应，获取一个锁，标示为+1，释放一个锁，标志位-1

```
        protected final boolean tryRelease(int releases) {
            int c = getState() - releases;
            if (Thread.currentThread() != getExclusiveOwnerThread())//如果释放的线程和获取锁的线程不是同一个，抛出非法监视器状态异常。
                throw new IllegalMonitorStateException();
            boolean free = false;
            if (c == 0) {//因为是重入的关系，不是每次释放锁c都等于0，直到最后一次释放锁时，才通知AQS不需要再记录哪个线程正在获取锁，即当前锁是free状态。
                free = true;
                setExclusiveOwnerThread(null);
            }
            setState(c);
            return free;
        }

```

释放锁，成功后，找到AQS的头节点，并唤醒它即可：

```
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
                /* 
     * 为什么不关心是否成功却还要设置呢？ 
     * 
     * 注意这里的Node实际就是head 
     *  
     * 如果设置成功，即head.waitStatus=0，则可以让这时即将被阻塞的线程有机会再次调用tryAcquire获取锁。 
     * 也就是让shouldParkAfterFailedAcquire方法里的compareAndSetWaitStatus(pred, ws, Node.SIGNAL)执行失败返回false，这样就能再有机会再tryAcquire了 
     * 
     * 如果设置失败，新跟随在head后面的线程被阻塞，但是没关系，下面的代码会立即将这个阻塞线程释放掉 
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
            // 从后往前找，但仍是找离node最近的一个有效节点（也就是它的继承者）
            for (Node t = tail; t != null && t != node; t = t.prev)
                if (t.waitStatus <= 0)
                    s = t;
        }
        if (s != null)
            LockSupport.unpark(s.thread);
    }

```

* * *

#### 应用之——非公平锁

其实， 它和公平锁的唯一区别就是获取锁的方式不同，一个是按前后顺序一次获取锁，一个是抢占式的获取锁

##### 获取锁

```
        final void lock() {
            if (compareAndSetState(0, 1))
                setExclusiveOwnerThread(Thread.currentThread());
            else
                acquire(1);
        }

```

非公平锁的lock方法的处理方式是: 在lock的时候先直接cas修改一次state变量（尝试获取锁），成功就返回，不成功再排队，从而达到不排队直接抢占的目的。

https://www.zhihu.com/question/36964449/answer/71678967（关于具体场景的解析）

当等待队列中，某个结点内的线程被唤醒后，它参与到锁竞争中，同它一起竞争的有可能是之前没有竞争失败过的锁，等待队列中的其他结点，不会参与到竞争中