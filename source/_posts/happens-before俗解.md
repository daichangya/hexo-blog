---
title: happens-before俗解
id: 1048
date: 2024-10-31 22:01:48
author: daichangya
excerpt: "学习Java并发，到后面总会接触到happens-before偏序关系。初接触玩意儿简直就是不知所云，下面是经过一段时间折腾后个人对此的一点浅薄理解，希望对初接触的人有帮助。如有不正确之处，欢迎指正。synchronized、大部分锁，众所周知的一个功能就是使多个线程互斥/串行的（共享锁允许多个线程同时访问，如读锁）访问临界区，但他们的第二个功能 —— 保证变量的可见性 —— 常被遗忘。"
permalink: /archives/21472751/
categories:
 - 多线程-并发
---



### happens-before俗解

学习Java并发，到后面总会接触到happens-before偏序关系。初接触玩意儿简直就是不知所云，下面是经过一段时间折腾后个人对此的一点浅薄理解，希望对初接触的人有帮助。如有不正确之处，欢迎指正。

synchronized、大部分锁，众所周知的一个功能就是使多个线程互斥/串行的（共享锁允许多个线程同时访问，如读锁）访问临界区，但他们的第二个功能 —— 保证变量的可见性 —— 常被遗忘。

为什么存在可见性问题？简单介绍下。相对于内存，CPU的速度是极高的，如果CPU需要存取数据时都直接与内存打交道，在存取过程中，CPU将一直空闲，这是一种极大的浪费，妈妈说，浪费是不好的，所以，现代的CPU里都有很多寄存器，多级cache，他们比内存的存取速度高多了。某个线程执行时，内存中的一份数据，会存在于该线程的工作存储中（***working memory，是cache和寄存器的一个抽象，这个解释源于《Concurrent Programming in Java: Design Principles and Patterns, Second Edition》§2.2.7，原文：Every thread is defined to have a working memory (an abstraction of caches and registers) in which to store values. 有不少人觉得working memory是内存的某个部分，这可能是有些译作将working memory译为工作内存的缘故，为避免混淆，这里称其为工作存储，每个线程都有自己的工作存储***），并在某个特定时候回写到内存。单线程时，这没有问题，如果是多线程要同时访问同一个变量呢？内存中一个变量会存在于多个工作存储中，线程1修改了变量a的值什么时候对线程2可见？此外，编译器或运行时为了效率可以在允许的时候对指令进行**重排序**，重排序后的执行顺序就与代码不一致了，这样线程2读取某个变量的时候线程1可能还没有进行写入操作呢，虽然代码顺序上写操作是在前面的。这就是可见性问题的由来。

我们无法枚举所有的场景来规定某个线程修改的变量何时对另一个线程可见。但可以制定一些通用的规则，这就是happens-before。它是一个偏序关系，Java内存模型中定义了许多Action，有些Action之间存在happens-before关系（并不是所有Action两两之间都有happens-before关系）。“ActionA happens-before ActionB”这样的描述很扰乱视线，是不是？OK，换个描述，如果ActionA happens-before ActionB，我们可以记作*hb(ActionA,ActionB)*或者记作ActionA < ActionB，这货在这里已经不是小于号了，它是偏序关系，是不是隐约有些离散数学的味道，不喜欢？嗯，我也不喜欢，so，下面都用hb(ActionA,ActionB)这种方式来表述。

从Java内存模型中取两条happens-before关系来瞅瞅：

*   An unlock on a monitor happens-before every subsequent lock on that monitor.
*   A write to a volatile field happens-before every subsequent read of that volatile.

“对一个monitor的解锁操作happens-before后续对同一个monitor的加锁操作”、“对某个volatile字段的写操作happens-before后续对同一个volatile字段的读操作”……莫名其妙、不知所云、不能理解……就是这个心情。是不是说解锁操作要先于锁定操作发生？这有违常规啊。确实不是这么理解的。happens-before规则不是描述实际操作的先后顺序，它是用来描述可见性的一种规则，下面我给上述两条规则换个说法：

*   如果线程1解锁了monitor a，接着线程2锁定了a，那么，线程1解锁a之前的写操作都对线程2可见（线程1和线程2可以是同一个线程）。
*   如果线程1写入了volatile变量v（这里和后续的“变量”都指的是对象的字段、类字段和数组元素），接着线程2读取了v，那么，线程1写入v及之前的写操作都对线程2可见（线程1和线程2可以是同一个线程）。

是不是很简单，瞬间觉得这篇文章弱爆了，说了那么多，其实就是在说“*如果hb(a,b)，那么a及之前的写操作在另一个线程t1进行了b操作时都对t1可见（同一个线程就不会有可见性问题，下面不再重复了）*”。虽然弱爆了，但还得有始有终，是不是，继续来，再看两条happens-before规则：

*   All actions in a thread happen-before any other thread successfully returns from a join() on that thread.
*   Each action in a thread happens-before every subsequent action in that thread.

通俗版：

*   线程t1写入的所有变量（所有action都与那个join有hb关系，当然也包括线程t1终止前的最后一个action了，最后一个action及之前的所有写入操作，所以是所有变量），在任意其它线程t2调用t1.join()成功返回后，都对t2可见。
*   线程中上一个动作及之前的所有写操作在该线程执行下一个动作时对该线程可见（也就是说，同一个线程中前面的所有写操作对后面的操作可见）

大致都是这个样子的解释。

happens-before关系有个很重要的性质，就是**传递性**，即，如果hb(a,b),hb(b,c)，则有hb(a,c)。

Java内存模型中只是列出了几种比较基本的hb规则，在Java语言层面，又衍生了许多其他happens-before规则，如ReentrantLock的unlock与lock操作，又如AbstractQueuedSynchronizer的release与acquire，setState与getState等等。

接下来用hb规则分析两个实际的可见性例子。

*   看个CopyOnWriteArrayList的例子，代码中的list对象是CopyOnWriteArrayList类型，a是个静态变量，初始值为0

假设有以下代码与执行线程：

<table><tbody><tr><td>线程1</td><td>线程2</td></tr><tr><td><div id="highlighter_745975" class="syntaxhighlighter  "><div class="bar"><div class="toolbar"><a href="#viewSource" title="view source" class="item viewSource" style="width: 16px; height: 16px;">view source</a><div class="item copyToClipboard"><embed width="16" height="16" id="highlighter_745975_clipboard" type="application/x-shockwave-flash" title="copy to clipboard" allowscriptaccess="always" wmode="transparent" flashvars="highlighterId=highlighter_745975" menu="false" src="http://ifeve.com/wp-content/plugins/syntaxhighlighter/syntaxhighlighter2/scripts/clipboard.swf"></div><a href="#printSource" title="print" class="item printSource" style="width: 16px; height: 16px;">print</a><a href="#about" title="?" class="item about" style="width: 16px; height: 16px;">?</a></div></div><div class="lines"><div class="line alt1"><table><tbody><tr><td class="number"><code>1</code></td><td class="content"><code class="plain">a = </code><code class="value">1</code><code class="plain">;</code></td></tr></tbody></table></div><div class="line alt2"><table><tbody><tr><td class="number"><code>2</code></td><td class="content"><code class="plain">list.set(</code><code class="value">1</code><code class="plain">,</code><code class="string">"t"</code><code class="plain">);</code></td></tr></tbody></table></div></div></div></td><td><div id="highlighter_546171" class="syntaxhighlighter  "><div class="bar "><div class="toolbar"><a href="#viewSource" title="view source" class="item viewSource" style="width: 16px; height: 16px;">view source</a><div class="item copyToClipboard"><embed width="16" height="16" id="highlighter_546171_clipboard" type="application/x-shockwave-flash" title="copy to clipboard" allowscriptaccess="always" wmode="transparent" flashvars="highlighterId=highlighter_546171" menu="false" src="http://ifeve.com/wp-content/plugins/syntaxhighlighter/syntaxhighlighter2/scripts/clipboard.swf"></div><a href="#printSource" title="print" class="item printSource" style="width: 16px; height: 16px;">print</a><a href="#about" title="?" class="item about" style="width: 16px; height: 16px;">?</a></div></div><div class="lines"><div class="line alt1"><table><tbody><tr><td class="number"><code>1</code></td><td class="content"><code class="plain">list.get(</code><code class="value">0</code><code class="plain">);</code></td></tr></tbody></table></div><div class="line alt2"><table><tbody><tr><td class="number"><code>2</code></td><td class="content"><code class="keyword">int</code> <code class="plain">b = a;</code></td></tr></tbody></table></div></div></div></td></tr></tbody></table>

那么，线程2中b的值会是1吗？来分析下。假设执行轨迹为以下所示：

	线程1					线程2
	p1:a = 1			
	p2:list.set(1,"t")		
						p3:list.get(2)
						p4:int b = a;

p1,p2是同一个线程中的，p3,p4是同一个线程中的，所以有hb(p1,p2),hb(p3,p4)，要使得p1中的赋值操作对p4可见，那么只需要有hb(p1,p4)，前面说过，hb关系具有传递性，那么若有hb(p2,p3)就能得到hb(p1,p4)，p2,p3是不是存在hb关系？翻翻[javaapi](http://docs.oracle.com/javase/7/docs/api/java/util/concurrent/package-summary.html)，发现有如下描述:

> Actions in a thread prior to **placing** an object into **any concurrent collection** happen-before actions subsequent to the access or removal of that element from the collection in another thread.

p2是放入一个元素到并发集合中，p3是从并发集合中取，符合上述描述，因此有hb(p2,p3).也就是说，在这样一种执行轨迹下，可以保证线程2中的b的值是1.如果是下面这样的执行轨迹呢？

	线程1					线程2
	p1:a = 1				
	        				p3:list.get(2)
	p2:list.set(1,"t")				
						p4:int b = a;

依然有hb(p1,p2)，hb(p3,p4)，但是没有了hb(p2,p3)，得不到hb(p1,p4)，虽然线程1给a赋值操作在执行顺序上是先于线程2读取a的，但jmm不保证最后b的值是1.这不是说一定不是1，只是不能保证。如果程序里没有采取手段（如加锁等）排除类似这样的执行轨迹，那么是无法保证b取到1的。像这样的程序，就是没有**正确同步**的，存在着**数据争用（data race）**。

既然提到了CopyOnWriteArrayList，那么顺便看下其set实现吧：

```
public E set(int index, E element) {
	final ReentrantLock lock = this.lock;
	lock.lock();
	try {
			Object[] elements = getArray();
			Object oldValue = elements[index];

		if (oldValue != element) {
			int len = elements.length;
			Object[] newElements = Arrays.copyOf(elements, len);
			newElements[index] = element;
			setArray(newElements);
		} else {
			// Not quite a no-op; ensures volatile write semantics
			setArray(elements);
		}
		return (E)oldValue;
	} finally {
		lock.unlock();
	}
}
```

有意思的地方是else里的setArray(elements)调用，看看setArray做了什么：

```
final void setArray(Object[] a) {
	array = a;
}
```

一个简单的赋值，array是volatile类型。elements是从getArray()方法取过来的，getArray()实现如下：

```
final Object[] getArray() {
	return array;
}
```
也很简单，直接返回array。取得array，又重新赋值给array，有甚意义？setArray(elements)上有条简单的注释，但可能不是太容易明白。正如前文提到的那条javadoc上的规定，放入一个元素到并发集合与从并发集合中取元素之间要有hb关系。set是放入，get是取（取还有其他方法），怎么才能使得set与get之间有hb关系，set方法的最后有unlock操作，如果get里有对这个锁的lock操作，那么就好满足了，但是get并没有加锁：

```
public E get(int index) {
	return (E)(getArray()[index]);
}
```
但是get里调用了getArray，getArray里有读volatile的操作，只需要set走任意代码路径都能遇到写volatile操作就能满足条件了，这里主要就是if…else…分支，if里有个setArray操作，如果只是从单线程角度来说，else里的setArray(elements)是没有必要的，但是为了使得走else这个代码路径时也有写volatile变量操作，就需要加一个setArray(elements)调用。

最后，以FutureTask结尾，这应该是个比较有名的例子了，随提一下。提交任务给线程池，我们可以通过FutureTask来获取线程的运行结果。绝大部分时候，将结果写入FutureTask的线程和读取结果的不会是同一个线程。写入结果的代码如下：

```
void innerSet(V v) {
	for (;;) {
		int s = getState();
		if (s == RAN)
			return;
		if (s == CANCELLED) {
			// aggressively release to set runner to null,
			// in case we are racing with a cancel request
			// that will try to interrupt runner
			releaseShared(0);
			return;
		}
		if (compareAndSetState(s, RAN)) {
			result = v;
			releaseShared(0);
			done();
			return;
		}
	}
}
```
获取结果的代码如下：

```
V innerGet(long nanosTimeout) throws InterruptedException, ExecutionException, TimeoutException {
	if (!tryAcquireSharedNanos(0, nanosTimeout))
		throw new TimeoutException();
	if (getState() == CANCELLED)
		throw new CancellationException();
	if (exception != null)
		throw new ExecutionException(exception);
	return result;
}
```

结果就是result变量，但result不是volatile变量，而这里有没有加锁操作，那么怎么保证写入到result的值对读取result的线程可见？这里是经过精心设计的，因为读写volatile的开销很小，但毕竟还是存在开销的，且作为一个基础类库，追求最后一点性能也不为过，因为无法预知所有可能的使用场景。这里主要利用了AbstractQueuedSynchronizer中的releaseShared与tryAcquireSharedNanos存在hb关系。

		线程1：			线程2：
		p1:result = v;
		p2:releaseShared(0);
					p3:tryAcquireSharedNanos(0, nanosTimeout)
					p4:return result;

正如前面分析的那样，在这个执行轨迹中，有hb(p1,p2),hb(p3,p4)且有hb(p2,p3)，所有有hb(p1,p4)，因此，即使result是普通变量，p1中的写操作也是对p4可见的。但，会不会存在这样的轨迹呢：

		线程1：				线程2：
		p1:result = v;			
		              			p3:tryAcquireSharedNanos(0, nanosTimeout)
		p2:releaseShared(0);
						p4:return result;

这也是一个关键点所在，这种情况是决计不会发生的。因为如果没有p2操作，那么p3在执行tryAcquireSharedNanos时会一直被阻塞，直到releaseShared操作执行了或超过了nanosTimeout超时时间或被中断抛出InterruptedException，若是releaseShared执行了，则就变成了第一个轨迹，若是超时，那么返回值是false，代码逻辑中就直接抛出了异常，不会去取result了，所以，这个地方设计的很精巧。这就是所谓的“**捎带同步**（piggybacking on synchronization）”，即，没有特意为result变量的读写设置同步，而是利用了其他同步动作时“捎带”的效果。但在我们自己写代码时，应该尽可能避免这样的做法，因为，不好理解，对编码人员要求高，维护难度大。

本文只是简单地解释了下hb规则，文中还出现了许多名词没有做更多介绍，为啥没介绍？介绍开来就是一本书啦，他们就是《Java Memory Model》、《Java Concurrency in Practice》、《Concurrent Programming in Java: Design Principles and Patterns》等，这些书里找定义与解释吧。
