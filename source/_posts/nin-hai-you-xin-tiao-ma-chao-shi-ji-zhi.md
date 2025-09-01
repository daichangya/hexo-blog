---
title: 您还有心跳吗？超时机制分析
id: 512
date: 2024-10-31 22:01:44
author: daichangya
excerpt: 问题描述 在C/S模式中，有时我们会长时间保持一个连接，以避免频繁地建立连接，但同时，一般会有一个超时时间，在这个时间内没发起任何请求的连接会被断开，以减少负载，节约资源。并且该机制一般都是在服务端实现，因为client强制关闭或意外断开连接，server端在此刻是感知不到的，如果放到client端实现，在上
permalink: /archives/nin-hai-you-xin-tiao-ma-chao-shi-ji-zhi/
categories:
- 多线程-并发
---

 

## **问题描述 **

在C/S模式中，有时我们会长时间保持一个连接，以避免频繁地建立连接，但同时，一般会有一个超时时间，在这个时间内没发起任何请求的连接会被断开，以减少负载，节约资源。并且该机制一般都是在服务端实现，因为client强制关闭或意外断开连接，server端在此刻是感知不到的，如果放到client端实现，在上述情况下，该超时机制就失效了。本来这问题很普通，不太值得一提，但最近在项目中看到了该机制的一种糟糕的实现，故在此深入分析一下。

## **问题分析及解决方案 **

服务端一般会保持很多个连接，所以，一般是创建一个定时器，定时检查所有连接中哪些连接超时了。此外我们要做的是，当收到客户端发来的数据时，怎么去刷新该连接的超时信息？

最近看到一种实现方式是这样做的:

```
public class Connection {
  private long lastTime;
  public void refresh() {
    lastTime = System.currentTimeMillis();
  }
 
  public long getLastTime() {
    return lastTime;
  }
  //......
}
```

在每次收到客户端发来的数据时，调用refresh方法。

然后在定时器里，用当前时间跟每个连接的getLastTime()作比较，来判定超时:

```
public class TimeoutTask  extends TimerTask{
  public void run() {
    long now = System.currentTimeMillis();
    for(Connection c: connections){
      if(now - c.getLastTime()> TIMEOUT_THRESHOLD)
        ;//timeout, do something
    }
  }
}
```

看到这，可能不少读者已经看出问题来了，那就是内存可见性问题，调用refresh方法的线程跟执行定时器的线程肯定不是一个线程，那run方法中读到的lastTime就可能是旧值，即可能将活跃的连接判定超时，然后被干掉。

有读者此时可能想到了这样一个方法，将lastTime加个volatile修饰，是的，这样确实解决了问题，不过，作为服务端，很多时候对性能是有要求的，下面来看下在我电脑上测出的一组数据，测试代码如下，供参考

```
public class PerformanceTest {
    private static long i;
    private volatile static long vt;
    private static final int TEST_SIZE = 10000000;

    public static void main(String[] args) {
        long time = System.nanoTime();
        for (int n = 0; n < TEST_SIZE; n++)
            vt = System.currentTimeMillis();
        System.out.println(-time + (time = System.nanoTime()));
        for (int n = 0; n < TEST_SIZE; n++)
            i = System.currentTimeMillis();
        System.out.println(-time + (time = System.nanoTime()));
        for (int n = 0; n < TEST_SIZE; n++)
            synchronized (PerformanceTest.class) {
            }
        System.out.println(-time + (time = System.nanoTime()));
        for (int n = 0; n < TEST_SIZE; n++)
            vt++;
        System.out.println(-time + (time = System.nanoTime()));
        for (int n = 0; n < TEST_SIZE; n++)
            vt = i;
        System.out.println(-time + (time = System.nanoTime()));
        for (int n = 0; n < TEST_SIZE; n++)
            i = vt;
        System.out.println(-time + (time = System.nanoTime()));
        for (int n = 0; n < TEST_SIZE; n++)
            i++;
        System.out.println(-time + (time = System.nanoTime()));
        for (int n = 0; n < TEST_SIZE; n++) i = n;
        System.out.println(-time + (time = System.nanoTime()));
    }
}

```

	测试一千万次，结果是（耗时单位：纳秒，包含循环本身的时间）：
	238932949       volatile写+取系统时间
	144317590       普通写+取系统时间
	135596135       空的同步块（synchronized）
	80042382        volatile变量自增
	15875140        volatile写
	6548994         volatile读
	2722555         普通自增
	2949571         普通读写

从上面的数据看来，volatile写+取系统时间的耗时是很高的，取系统时间的耗时也比较高，跟一次无竞争的同步差不多了，接下来分析下如何优化该超时时机。 首先：同步问题是肯定得考虑的，因为有跨线程的数据操作；另外，取系统时间的操作比较耗时，能否不在每次刷新时都取时间？因为刷新调用在高负载的情况下很频繁。如果不在刷新时取时间，那又该怎么去判定超时？ 我想到的办法是，在refresh方法里，仅设置一个volatile的boolean变量reset（这应该是成本最小的了吧，因为要处理同步问题，要么同步块，要么volatile，而volatile读在此处是没什么意义的），对时间的掌控交给定时器来做，并为每个连接维护一个计数器，每次加一，如果reset被设置为true了，则计数器归零，并将reset设为false（因为计数器只由定时器维护，所以不需要做同步处理，从上面的测试数据来看，普通变量的操作，时间成本是很低的），如果计数器超过某个值，则判定超时。 下面给出具体的代码：

```
public class Connection {
    int count = 0;
    volatile boolean reset = false;

    public void refresh() {
        if (reset == false) reset = true;
    }
}

public class TimeoutTask extends TimerTask {
    public void run() {
        for (Connection c : connections) {
            if (c.reset) {
                c.reset = false;
                c.count = 0;
            } else if (++c.count >= TIMEOUT_COUNT)
                ;// timeout, do something
        }
    }
}
```

代码中的TIMEOUT_COUNT 等于超时时间除以定时器的周期，周期大小既影响定时器的执行频率，也会影响实际超时时间的波动范围（这个波动，第一个方案也存在，也不太可能避免，并且也不需要多么精确）。

代码很简洁，下面来分析一下。

reset加上了volatile，所以保证了多线程操作的可见性，虽然有两个线程都对变量有写操作，但无论这两个线程怎么穿插执行，都不会影响其逻辑含义。

再说下refresh方法，为什么我在赋值语句上多加了个条件？这不是多了一次volatile读操作吗？我是这么考虑的，高负载下，refresh会被频繁调用，意味着reset长时间为true，那么加上条件后，就不会执行写操作了，只有一次读操作，从上面的测试数据来看，volatile变量的读操作的性能是显著优于写操作的。只不过在reset为false的时候，多了一次读操作，但此情况在定时器的一个周期内最多只会发一次，而且对高负载情况下的优化显然更有意义，所以我认为加上条件还是值得的。

最后提及一下，我有点完美主义，自认为上面的方案在我当前掌握的知识下，已经很漂亮了，如果你发现还有可优化的地方，或更好的方案，希望能分享。