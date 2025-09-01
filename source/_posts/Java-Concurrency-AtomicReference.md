---
title: Java Concurrency:AtomicReference
id: 16
date: 2024-10-31 22:01:40
author: daichangya
excerpt: Java.util.concurrent.atomic.AtomicReference是一个旨在以线程安全的方式更新变量的类。WhydoweneedtheclassAtomicReference?为什么我们不能简单地使用一个volatile变量？我们如何正确使用它？WhyAtomicReferenc
permalink: /archives/Java-Concurrency-AtomicReference/
categories:
- 多线程
---

Java.util.concurrent.atomic.AtomicReference是一个旨在以线程安全的方式更新变量的类。Why do we need the class AtomicReference? 为什么我们不能简单地使用一个volatile变量？我们如何正确使用它？

Why AtomicReference?
对于我正在编写的工具，我需要检测是否从多个线程中调用了一个对象。我为此使用以下不可变类：
```
public class State {
	private final Thread thread;
	private final boolean accessedByMultipleThreads;
	public State(Thread thread, boolean accessedByMultipleThreads) {
		super();
		this.thread = thread;
		this.accessedByMultipleThreads = accessedByMultipleThreads;
	}
	public State() {
		super();
		this.thread = null;
		this.accessedByMultipleThreads = false;
	}
	public State update() {
		if(accessedByMultipleThreads) 	{
			return this;
		}
		if( thread == null  ) {
			return new  State(Thread.currentThread() , accessedByMultipleThreads);
		} 
		if(thread != Thread.currentThread()) {
			return new  State(null,true);
		}	
		return this;
	}
	public boolean isAccessedByMultipleThreads() {
		return accessedByMultipleThreads;
	}
}
```

您可以在[github](https://github.com/daichangya/Java-Concurrency-in-Practice)上下载所有示例的源代码  。

我将访问对象的第一个线程存储在变量线程的第2行中。当另一个线程访问该对象时，我将变量设置  accessedByMultipleThreads 为true，将变量线程设置为null，第23行。当变量  accessedByMultipleThreads 为true时，我不更改状态，第15行到第17行。

我在每个对象中使用此类来检测它是否被多个线程访问。以下示例在类中使用状态  UpdateStateNotThreadSafe：
```
public class UpdateStateNotThreadSafe {
	private volatile  State state = new State();
	public void update() {
		state = state.update();
	}
	public State getState() {
		return state;
	}	
}
```

我将状态存储在volatile变量状态（第2行）中。我需要volatile关键字以确保线程始终看到当前值，如此处更详细地解释。

要检查使用volatile变量是否是线程安全的，我使用以下测试：
```
import static org.junit.Assert.*;
import org.junit.Test;
import com.vmlens.tutorialAtomicReference.UpdateStateNotThreadSafe;
import com.vmlens.api.AllInterleavings;
public class TestNotThreadSafe {
	@Test
	public void test() throws InterruptedException {
		try (AllInterleavings allInterleavings = new AllInterleavings("TestNotThreadSafe");) {
			while (allInterleavings.hasNext()) {	
		final UpdateStateNotThreadSafe object = new UpdateStateNotThreadSafe();		
		Thread first = new Thread( () ->    {  object.update();  } ) ;
		Thread second = new Thread( () ->   {  object.update(); } ) ;
		first.start();
		second.start();
		first.join();
		second.join();	
		assertTrue(  object.getState().isAccessedByMultipleThreads() );
			}
		}
	}
}
```

我需要两个线程来测试在第9行和第10行中创建的使用volatile变量是否是线程安全的。我在第11行和第12行中启动了这两个线程，然后等待，直到使用线程联接第13行和第14行都结束了。在两个线程都停止之后，我检查标志accessedByMultipleThreads是否为真，第15行。

为了测试所有线程交织，我们使用来自vmlens的第7行的AllInterleavings类，将完整的测试放在while循环中，对所有线程交织进行迭代。运行测试，我看到以下错误：

```
java.lang.AssertionError:
    at org.junit.Assert.fail(Assert.java:91)
    at org.junit.Assert.assertTrue(Assert.java:43)
    at org.junit.Assert.assertTrue(Assert.java:54)
```

vmlens报告显示出了什么问题：

![incorectupdate.png](http://images.jsdiff.com/upload/2020/04/incorectupdate-591e36e4419d4d37b524b27c943bda69.png)

问题在于，对于特定线程而言，交织两个线程首先读取状态。因此，一个线程将覆盖另一个线程的结果。

如何使用AtomicReference？
为了解决这种竞争状况，我使用中的  compareAndSet 方法  AtomicReference。

该  compareAndSet 方法采用两个参数，期望的当前值和新的值。该方法自动检查当前值是否等于期望值。如果是，则该方法将值更新为新值并返回true。如果不是，则该方法使当前值保持不变并返回false。

使用此方法的想法是让  compareAndSet 我们在计算新值时检查当前值是否被另一个线程更改。如果没有，我们可以安全地更新当前值。否则，我们需要使用更改后的当前值重新计算新值。

下面显示了如何使用该  compareAndSet 方法自动更新状态：

```
import java.util.concurrent.atomic.AtomicReference;

public class UpdateStateWithCompareAndSet {
    private final AtomicReference<State> state = new AtomicReference<State>(new State());

    public void update() {
        State current = state.get();
        State newValue = current.update();
        while (!state.compareAndSet(current, newValue)) {
            current = state.get();
            newValue = current.update();
        }
    }

    public State getState() {
        return state.get();
    }
}
```
现在  AtomicReference ，我将状态2用于第2行。要更新状态，我首先需要获取当前值（第5行）。然后，计算新值（第6行），并尝试更新  AtomicReference using  compareAndSet（第7行）。更新成功，我完成了。如果不是，我需要在第8行再次获取当前值，并在第9行重新计算新值。然后，我可以再次尝试更新  AtomicReference using  compareAndSet。我需要一个while循环，因为  compareAndSet 可能会失败多次。

正如Grzegorz Borczuch在对本文的评论中指出的那样，自从JDK 1.8以来，在AtomicReference中使用了一种更容易使用的方法，该方法可实现相同的结果：updateAndGet。此方法在内部使用带有while循环的compareAndSet来
更新AtomicReference。

Conclusion
使用易失性变量会导致争用情况，因为针对某个线程的特定线程交织会覆盖其他线程的计算。通过使用compareAndSet 类中的  方法  AtomicReference，我们可以规避这种竞争条件。我们自动检查当前值是否与开始计算时相同。如果是，我们可以安全地更新当前值。否则，我们需要使用更改后的当前值重新计算新值。

