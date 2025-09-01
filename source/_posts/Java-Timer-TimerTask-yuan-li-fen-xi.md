---
title: Java Timer&TimerTask原理分析
id: 453
date: 2024-10-31 22:01:43
author: daichangya
excerpt: 如果你使用Java语言进行开发，对于定时执行任务这样的需求，自然而然会想到使用Timer和TimerTask完成任务，我最近就使用 Timer和TimerTask完成了一个定时执行的任务，实现得没有问题，但当在TimerTaks的run()方法中使用
  Thread.sleep()方式时，可能会出现奇怪的现象，好像Timer失效了，网上查了一下，倒是有人遇到了相同的问题，但是并没有找到一篇解释为什么
permalink: /archives/Java-Timer-TimerTask-yuan-li-fen-xi/
categories:
- 多线程
- java源码分析
---

如果你使用Java语言进行开发，对于定时执行任务这样的需求，自然而然会想到使用Timer和TimerTask完成任务，我最近就使用 Timer和TimerTask完成了一个定时执行的任务，实现得没有问题，但当在TimerTaks的run()方法中使用 Thread.sleep()方式时，可能会出现奇怪的现象，好像Timer失效了，网上查了一下，倒是有人遇到了相同的问题，但是并没有找到一篇解释为什么会出现这种情况，期待有某位达人能够分析清楚这个问题。



遇到了这样的问题，始终让我不爽，于是看了一下Timer的源码，先将了解到的内容整理如下，接下来再看看Thread.sleep()的源码，看能否找到问题所在。



在Java中，与定时任务执行相关的类很少，只有Timer、TimerTask、TimerThread、TaskQueue几个，其中每个类的职责大致如下：

Timer：一个Task的调度类，和TimerTask一样，暴露给最终用户使用的类，通过schedule方法安排Task的执行计划。该类通过TaskQueue和TimerThread类完成Task的调度。

TimerTask：实现Runnable接口，表明每一个任务均为一个独立的线程。通过run()方法提供用户定制自己任务。该类有一个比较重要的成员变量nextExecutionTime ，表示下一次执行该任务的时间。以后会看到，Timer机制就是靠这个值安排Task执行的。

TimerThread：继承于Thread，是真正执行Task的类。

TaskQueue：一个存储Task的数据结构，内部由一个最小堆实现，堆的每个成员为一个TimeTask，每个Task依靠其 nextExecutionTime值进行排序，也就是说，nextExecutionTime最小的任务在队列的最前端，从而能够现实最早执行。



要想使用Timer，用户只需要了解Timer和TimerTask，下面现已一个最基本的Timer和TimerTask使用案例入手，来看一下Timer内部的实现原理。
```
	import java.util.Timer;
	import java.util.TimerTask;
	import org.junit.Test;
	class TestTimerTask extends TimerTask {
	  @Override
	  public void run() {
	    System.out.println("TestTimerTask is running......");
	  }
	}
	public class TimerTaskTest {
	  @Test
	  public void testTimerTask() {
	    Timer timer = new Timer();
	    timer.schedule(new TestTimerTask(), 0, );
	  }
	}
```


上面的代码是一个典型的Timer&TimerTask的应用，下面先来看一下new Timer()干了什么事，其源码如下：
```
public Timer(String name) {

        thread.setName(name);    //thread为TimerThread实例。

        thread.start();

}
```
从上面的源代码可以知道，创建Timer对象的同时也启动了TimerThread线程。下面来看看TimerThread干了什么事：

```
	public void run() {
	        try {
	            mainLoop();                 //线程真正执行的代码在这个私有方法中
	        } finally {
	            // Someone killed this Thread, behave as if Timer cancelled
	            synchronized(queue) {
	                newTasksMayBeScheduled = false;
	                queue.clear();  // Eliminate obsolete references
	            }
	        }
	}
```

接着来看看私有方法mainLoop()干了什么事：


```
	private void mainLoop() {
	        while (true) {
	            try {
	                TimerTask task;
	                booleantaskFired;       //是否已经到达Task的执行时间，如果已经到达，设置为true，否则置为false
	                synchronized(queue) {
	                    // Wait for queue to become non-empty
	                    while (queue.isEmpty() && newTasksMayBeScheduled)
	                        queue.wait();                //由此可以看出，Timer通过wait & notify 方法安排线程之间的同步
	                    if (queue.isEmpty())
	                        break; // Queue is empty and will forever remain; die
	                    // Queue nonempty; look at first evt and do the right thing
	                    long currentTime, executionTime;
	                    task = queue.getMin();
	                    synchronized(task.lock) {
	                        if (task.state == TimerTask.CANCELLED) {
	                            queue.removeMin();
	                            continue;  // No action required, poll queue again
	                        }
	                        currentTime = System.currentTimeMillis();
	                        executionTime = task.nextExecutionTime;
	                        if(taskFired = (executionTime<=currentTime)) {        //Task的执行时间已到，设置taskFired为true
	                            if (task.period == 0) { // Non-repeating, remove
	                                queue.removeMin();        //移除队列中的当前任务
	                                task.state = TimerTask.EXECUTED;
	                            } else { // Repeating task, reschedule
	                                queue.rescheduleMin(         //重新设置任务的下一次执行时间
	                                  task.period<0 ? currentTime   - task.period
	                                                : executionTime + task.period);
                                         如果服务在当天:分以前被启动,两个方法都会在在:分时执行任务. 第二次任务执行时间都是:+ *  *  * ,如果过了这个点后启服务两个方法都会马上执行任务.但第二次任务被执行的时间就是差别了,scheduleAtFixedRate是在你设置的date的基础上加 *  *  * 这个时间段后执行而,schedule是在服务启动时间的基础上加 *  *  * 这个时间段后执行. 
	                            }
	                        }
	                    }
	                    if (!taskFired) // Task hasn't yet fired; wait
	                        queue.wait(executionTime - currentTime);    //还没有执行时间，通过wait等待特定时间
	                }
	                if (taskFired)  // Task fired; run it, holding no locks
	                    task.run();    //已经到达执行时间，执行任务
	            } catch(InterruptedException e) {
	            }
	        }
	}

```
也就是说，一旦创建了Timer类的实例，就一直存在一个循环在遍历queue中的任务，如果有任务的话，就通过thread去执行该任务，否则线程通过wait()方法阻塞自己，由于没有任务在队列中，就没有必要继续thread中的循环。



上面提到，如果Timer的任务队列中不包含任务时，Timer中的TimerThread线程并不会执行，接着来看看为Timer添加任务后会出现怎样的情况。为Timer添加任务就是timer.schedule()干的事，schedule()方法直接调用Timer的私有方法 sched()，sched()是真正安排Task的地方，其源代码如下：

```

	private void sched(TimerTask task, long time, long period) {
	        if (time < 0)
	            throw new IllegalArgumentException("Illegal execution time.");
	        synchronized(queue) {
	            if (!thread.newTasksMayBeScheduled)
	                throw new IllegalStateException("Timer already cancelled.");
	            synchronized(task.lock) {
	                if(task.state != TimerTask.VIRGIN)             //我喜欢virgin状态，其他状态表明该Task已经被schedule过了
	                    throw new IllegalStateException(
	                        "Task already scheduled or cancelled");
	                 //设置Task下一次应该执行的时间, 由System.currentTimeMillis()+/-delay得到
	                task.nextExecutionTime = time;              
	                task.period = period;
	                task.state = TimerTask.SCHEDULED;
	            }
	            queue.add(task);            //queue为TaskQueue类的实例，添加任务到队列中
	            if(queue.getMin() == task)        //获取队列中nextExecutionTime最小的任务，如果与当前任务相同
	                queue.notify();                         //还记得前面看到的queue.wait()方法么
	        }
	}
```

不要奇怪，为什么要判断queue.getMin() == task时，才通过queue.notify()恢复执行。因为这种方式已经满足所有的唤醒要求了。

如果安排当前Task之前queue为空，显然上述判断为true，于是mainLoop()方法能够继续执行。

如果安排当前Task之前queue不为空，那么mainLoop()方法不会一直被阻塞，不需要notify方法调用。

调用该方法还有一个好处是，如果当前安排的Task的下一次执行时间比queue中其余Task的下一次执行时间都要小，通过notify方法可以提前打开queue.wait(executionTime - currentTime)方法对mainLoop()照成的阻塞，从而使得当前任务能够被优先执行，有点抢占的味道。



 上述分析可以看出，Java中Timer机制的实现仅仅使用了JDK中的方法，通过wait & notify机制实现，其源代码也非常简单，但可以想到的是这种实现机制会对开发者造成一种困扰，sched()方法中可以看出，对于一个重复执行的任务，Timer的实现机制是先安排Task下一次执行的时间，然后再启动Task的执行，如果Task的执行时间大于下一次执行的间隔时间，可能出现不可预期的错误。当然，了解了Timer的实现原理，修改这种实现方式也就非常简单了。