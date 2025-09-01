---
title: JUC (Java Util Concurrency) 基础内容概述
id: 82
date: 2024-10-31 22:01:40
author: daichangya
excerpt: "1. JUC概况2. 原子操作3. 指令重排4. Happens-before法则：（Java 内存模型）JMM的特性：volatile语义：5. CAS操作6. Lock 锁7. AQS"
permalink: /archives/21291063/
categories:
 - 多线程-并发
---


### 1\. JUC概况

以下是Java JUC包的主体结构：  
[![](http://static.oschina.net/uploads/img/201307/24132945_rpmS.jpg)](http://static.oschina.net/uploads/img/201307/24132945_rpmS.jpg)

*   Atomic : AtomicInteger
*   Locks : Lock, Condition, ReadWriteLock
*   Collections : Queue, ConcurrentMap
*   Executer : Future, Callable, Executor
*   Tools : CountDownLatch, CyclicBarrier, Semaphore

### 2\. 原子操作

多个线程执行一个操作时，其中任何一个线程要么完全执行完此操作，要么没有执行此操作的任何步骤，那么这个操作就是原子的。出现原因: synchronized的代价比较高。

以下以AtomicInteger为例：

*   int addAndGet(int delta)：以原子方式将给定值与当前值相加。 实际上就是等于线程安全版本的i =i+delta操作。
*   boolean compareAndSet(int expect, int update)：如果当前值 == 预期值，则以原子方式将该值设置为给定的更新值。 如果成功就返回true，否则返回false，并且不修改原值。
*   int decrementAndGet()：以原子方式将当前值减 1。 相当于线程安全版本的–i操作。
*   int getAndAdd(int delta)：以原子方式将给定值与当前值相加。 相当于线程安全版本的t=i;i+=delta;return t;操作。
*   int getAndDecrement()：以原子方式将当前值减 1。 相当于线程安全版本的i–操作。
*   int getAndIncrement()：以原子方式将当前值加 1。 相当于线程安全版本的i++操作。
*   int getAndSet(int newValue)：以原子方式设置为给定值，并返回旧值。 相当于线程安全版本的t=i;i=newValue;return t;操作。
*   int incrementAndGet()：以原子方式将当前值加 1。 相当于线程安全版本的++i操作。

### 3\. 指令重排

你的程序并不能总是保证符合CPU处理的特性。

要程序的最终结果等同于它在严格的顺序化环境下的结果，那么指令的执行顺序就可能与代码的顺序不一致。

[![](http://static.oschina.net/uploads/img/201307/24132945_rgfp.jpg)](http://static.oschina.net/uploads/img/201307/24132945_rgfp.jpg)

多核CPU，大压力下，两个线程交替执行，x，y输出结果不确定。可能结果：

<table border="0" cellpadding="0" cellspacing="0" style="font-family:Consolas, 'Bitstream Vera Sans Mono', 'Courier New', Courier, monospace !important;border:0px !important;font-size:1em !important;"><tbody><tr><td style="border:0px !important;vertical-align:baseline !important;font-family:Consolas, 'Bitstream Vera Sans Mono', 'Courier New', Courier, monospace !important;font-size:1em !important;color:rgb(120,120,120) !important;"><div>1</div><div>2</div><div>3</div><div>4</div></td><td style="border:0px !important;vertical-align:baseline !important;font-family:Consolas, 'Bitstream Vera Sans Mono', 'Courier New', Courier, monospace !important;font-size:1em !important;"><div><div>x =0， y =1</div><div>x =1， y =1</div><div>x =1， y =0</div><div>x =0， y =0</div></div></td></tr></tbody></table>

### 4\. Happens-before法则：（Java 内存模型）

如果动作B要看到动作A的执行结果（无论A/B是否在同一个线程里面执行），那么A/B就需要满足happens-before关系。

Happens-before的几个规则：

*   Program order rule：同一个线程中的每个Action都happens-before于出现在其后的任何一个Action。
*   Monitor lock rule：对一个监视器的解锁happens-before于每一个后续对同一个监视器的加锁。
*   Volatile variable rule：对volatile字段的写入操作happens-before于每一个后续的同一个字段的读操作。
*   Thread start rule：Thread.start()的调用会happens-before于启动线程里面的动作。
*   Thread termination rule：Thread中的所有动作都happens-before于其他线程检查到此线程结束或者Thread.join（）中返回或者Thread.isAlive()==false。
*   Interruption rule：一个线程A调用另一个另一个线程B的interrupt（）都happens-before于线程A发现B被A中断（B抛出异常或者A检测到B的isInterrupted（）或者interrupted()）。
*   Finalizer rule：一个对象构造函数的结束happens-before与该对象的finalizer的开始
*   Transitivity：如果A动作happens-before于B动作，而B动作happens-before与C动作，那么A动作happens-before于C动作。  
    因为CPU是可以不按我们写代码的顺序执行内存的存取过程的，也就是指令会乱序或并行运行， 只有上面的happens-before所规定的情况下，才保证顺序性。

#### JMM的特性：

多个CPU之间的缓存也不保证实时同步；  
JMM不保证创建过程的原子性，读写并发时，可能看到不完整的对象。（so D-check）

#### volatile语义：

volatile实现了类似synchronized的语义，却又没有锁机制。它确保对  volatile字段的更新以可预见的方式告知其他的线程。

1.  Java 存储模型不会对volatile指令的操作进行重排序：这个保证对volatile变量的操作时按照指令的出现顺序执行的。
2.  volatile变量不会被缓存在寄存器中（只有拥有线程可见），每次总是从主存中读取volatile变量的结果。

ps：volatile并不能保证线程安全的，也就是说volatile字段的操作不是原子性的，volatile变量只能保证可见性。

### 5\. CAS操作

Compare and Swap

CAS有3个操作数，内存值V，旧的预期值A，要修改的新值B。当且仅当预期值A和内存值V相同时，将内存值V修改为B，否则什么都不做。

实现简单的非阻塞算法:

	private volatile int value;// 借助volatile原语，保证线程间的数据是可见的
	 
	public final int get() {
		return value;
	}
	 
	public final int incrementAndGet() {
		for(;;) {
			int current = get();
			int next = current +1;
			if(compareAndSet(current, next))
				returnnext;
		}//Spin自旋等待直到返为止置
	}

整个J.U.C都是建立在CAS之上的，对于synchronized阻塞算法，J.U.C在性能上有了很大的提升。会出现所谓的“ABA”问题

### 6\. Lock 锁

Synchronized属于独占锁，高并发时性能不高，JDK5以后开始用JNI实现更高效的锁操作。

Lock—->

ReentrantLock—->

ReentrantReadWriteLock.ReadLock / ReentrantReadWriteLock.writeLock

ReadWriteLock—-> ReentrantReadWriteLock

LockSupport

Condition

<table style="font-family:'Segoe UI', Calibri, 'Myriad Pro', Myriad, 'Trebuchet MS', Helvetica, Arial, sans-serif;border-collapse:collapse;border-spacing:1px;border:1px solid rgb(248,248,248);font-size:13px;color:rgb(51,51,51);"><tbody><tr><td style="border:1px solid rgb(248,248,248);vertical-align:top;">方法名称</td><td style="border:1px solid rgb(248,248,248);vertical-align:top;">作用</td></tr><tr><td style="border:1px solid rgb(248,248,248);vertical-align:top;">void lock()</td><td style="border:1px solid rgb(248,248,248);vertical-align:top;">获取锁。如果锁不可用，出于线程调度目的，将禁用当前线程，并且在获得锁之前，该线程将一直处于休眠状态。</td></tr><tr><td style="border:1px solid rgb(248,248,248);vertical-align:top;">void lockInterruptibly() throws InterruptedException;</td><td style="border:1px solid rgb(248,248,248);vertical-align:top;">如果当前线程未被中断，则获取锁。如果锁可用，则获取锁，并立即返回。</td></tr><tr><td style="border:1px solid rgb(248,248,248);vertical-align:top;">Condition newCondition();</td><td style="border:1px solid rgb(248,248,248);vertical-align:top;">返回绑定到此&nbsp;Lock&nbsp;实例的新&nbsp;Condition<br>实例</td></tr><tr><td style="border:1px solid rgb(248,248,248);vertical-align:top;">boolean tryLock();</td><td style="border:1px solid rgb(248,248,248);vertical-align:top;">仅在调用时锁为空闲状态才获取该锁</td></tr><tr><td style="border:1px solid rgb(248,248,248);vertical-align:top;">boolean tryLock(long time, TimeUnit unit) throws InterruptedException;</td><td style="border:1px solid rgb(248,248,248);vertical-align:top;">如果锁在给定的等待时间内空闲，并且当前线程未被中断，则获取锁</td></tr><tr><td style="border:1px solid rgb(248,248,248);vertical-align:top;">void unlock();</td><td style="border:1px solid rgb(248,248,248);vertical-align:top;">释放锁</td></tr></tbody></table>

PS : 一般来说，获取锁和释放锁是成对儿的操作，这样可以避免死锁和资源的浪费。

注：在 finally 里面做释放锁的操作

### 7\. AQS

锁机制实现的核心所在。AbstractQueuedSynchronizer是Lock/Executor实现的前提。

[![](http://static.oschina.net/uploads/img/201307/24132945_S2dq.jpg)](http://static.oschina.net/uploads/img/201307/24132945_S2dq.jpg)

#### AQS实现：

基本的思想是表现为一个同步器，AQS支持下面两个操作：

acquire：

	while(synchronization state does not allow acquire){
		enqueue current threadifnot already queued;
		possibly block current thread;
	}
	dequeue current threadifit was queued;

release：

	update synchronization state;
	if(state may permit a blocked thread to acquire)
		unlock one or more queued threads;

要支持这两个操作，需要实现的三个条件：

*   Atomically managing synchronization state（原子性操作同步器的状态位）
*   Blocking and unblocking threads（阻塞和唤醒线程）
*   Maintaining queues（维护一个有序的队列）

##### Atomically managing synchronization state

使用一个32位整数来描述状态位：private volatile int state; 对其进行CAS操作，确保值的正确性。

##### Blocking and unblocking threads

JDK 5.0以后利用JNI在LockSupport类中实现了线程的阻塞和唤醒。

LockSupport.park() //在当前线程中调用，导致线程阻塞  
LockSupport.park(Object)  
LockSupport.unpark(Thread)

##### Maintaining queues

在AQS中采用CHL列表来解决有序的队列的问题。（CHL= Craig, Landin, and Hagersten）

[![](http://static.oschina.net/uploads/img/201307/24132946_XXNs.jpg)](http://static.oschina.net/uploads/img/201307/24132946_XXNs.jpg)

Node里面是什么结构？

[![](http://static.oschina.net/uploads/img/201307/24132946_Wzch.jpg)](http://static.oschina.net/uploads/img/201307/24132946_Wzch.jpg)

WaitStatus –>节点的等待状态，一个节点可能位于以下几种状态：

*   CANCELLED = 1： 节点操作因为超时或者对应的线程被interrupt。节点不应该不留在此状态，一旦达到此状态将从CHL队列中踢出。
*   SIGNAL = -1： 节点的继任节点是（或者将要成为）BLOCKED状态（例如通过LockSupport.park()操作），因此一个节点一旦被释放（解锁）或者取消就需要唤醒（LockSupport.unpack()）它的继任节点。
*   CONDITION = -2：表明节点对应的线程因为不满足一个条件（Condition）而被阻塞。
*   0： 正常状态，新生的非CONDITION节点都是此状态。

非负值标识节点不需要被通知（唤醒）。  
队列管理操作：

入队enqueue：

采用CAS操作，每次比较尾结点是否一致，然后插入的到尾结点中。

	do{
		pred = tail;
	}while( !compareAndSet(pred,tail,node) );

出队dequeue：

	while(pred.status != RELEASED) ;
		head  = node;

[![](http://static.oschina.net/uploads/img/201307/24132946_vUYP.jpg)](http://static.oschina.net/uploads/img/201307/24132946_vUYP.jpg)

加锁操作：

	public final void acquire(intarg) {
		if(!tryAcquire(arg))
			acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
		selfInterrupt();
	}

释放操作：

	public final boolean release(intarg) {
		if(tryRelease(arg)) {
			Node h = head;
			if(h !=null && h.waitStatus !=0)
				unparkSuccessor(h);
			return true;
		}
		return false;
	}

The synchronizer framework provides a ConditionObject class for use by synchronizers that maintain exclusivesynchronization and conform to the Lock interface.     —— Doug Lea《 The java.util.concurrent Synchronizer Framework 》

以下是AQS队列和Condition队列的出入结点的示意图，可以通过这几张图看出线程结点在两个队列中的出入关系和条件。

[![](http://static.oschina.net/uploads/img/201307/24132946_axG5.jpg)](http://static.oschina.net/uploads/img/201307/24132946_axG5.jpg)

[![](http://static.oschina.net/uploads/img/201307/24132946_blQs.jpg)](http://static.oschina.net/uploads/img/201307/24132946_blQs.jpg)

[![](http://static.oschina.net/uploads/img/201307/24132946_L0TJ.jpg)](http://static.oschina.net/uploads/img/201307/24132946_L0TJ.jpg)
