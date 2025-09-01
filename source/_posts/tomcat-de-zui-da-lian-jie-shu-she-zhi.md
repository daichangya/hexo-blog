---
title: tomcat 的最大连接数设置
id: 1453
date: 2024-10-31 22:01:56
author: daichangya
permalink: /archives/tomcat-de-zui-da-lian-jie-shu-she-zhi/
categories:
- Tomcat
---

## 前提说明

为了确保服务不会被过多的http长连接压垮，我们需要对tomcat设定个最大连接数，超过这个连接数的请求会拒绝，让其负载到其它机器。达到保护自己的同时起到连接数负载均衡的作用。

## 动手去做

一开始根据故障todoList提供的参数MaxKeepAliveRequests，进行验证，我们将tomcat配置server.xml修改为：  
[![screenshot](http://img1.tbcdn.cn/L1/461/1/d40af74ed622c343aaadc6040d49d7f79454faea.png "screenshot")](http://img1.tbcdn.cn/L1/461/1/d40af74ed622c343aaadc6040d49d7f79454faea.png)  
同时，启动客户端模拟30个长连接。

预期应该只有10个连接能保持住。  
结果与预期不符，30个连接都连上了，而且正常。  
这由此怀疑提供的配置参数是否是真正限制最大连接数的含义了。  
[![screenshot](http://img3.tbcdn.cn/L1/461/1/e9db0476f67ec2c8286b178e601b8c36dd0076d8.png "screenshot")](http://img3.tbcdn.cn/L1/461/1/e9db0476f67ec2c8286b178e601b8c36dd0076d8.png)  
KeepAlive是在HTTP1.1中定义的，用来保持客户机和服务器的长连接，通过减少建立TCP Session的次数来提高性能。常用的配置参数有{KeepAlive, KeepAliveTimeout, MaxKeepAliveRequests}。逐个说来：  
KeepAlive是决定开启KeepAlive支持；  
KeepAliveTimeout决定一 个KeepAlive的连接能保持多少时间，Timeout就尽快shutdown链接，若还有数据必须再建立新的连接 了；  
MaxKeepAliveRequests于KeepAliveTimeout相似，意思是服务多少个请求就shutdown连接。

显然与我们想到的要求不符，再搜索其它配置参数：

maxConnections  
根据字面意思觉得就应该是这个了。  
去验证吧，  
[![screenshot](http://img2.tbcdn.cn/L1/461/1/4224a6dfb04a5f100c3e949ca283db1662fb6625.png "screenshot")](http://img2.tbcdn.cn/L1/461/1/4224a6dfb04a5f100c3e949ca283db1662fb6625.png)!  
最大连接数为10，我们启动30个长连接，  
预期应该是只有10个长连接，实际结果却是远超过10个。这个有点不应该啊。

## 实验验证

原来还有个参数可以觉得连接数的大小  
[![screenshot](http://img1.tbcdn.cn/L1/461/1/07a474cbf34217bdafcc2ef89b2107003c13cdff.png "screenshot")](http://img1.tbcdn.cn/L1/461/1/07a474cbf34217bdafcc2ef89b2107003c13cdff.png)

maxThreads：tomcat起动的最大线程数，即同时处理的任务个数，默认值为200  
acceptCount：当tomcat起动的线程数达到最大时，接受排队的请求个数，默认值为100

这两个值如何起作用，请看下面三种情况  
情况1：接受一个请求，此时tomcat起动的线程数没有到达maxThreads，tomcat会起动一个线程来处理此请求。  
情况2：接受一个请求，此时tomcat起动的线程数已经到达maxThreads，tomcat会把此请求放入等待队列，等待空闲线程。  
情况3：接受一个请求，此时tomcat起动的线程数已经到达maxThreads，等待队列中的请求个数也达到了acceptCount，此时tomcat会直接拒绝此次请求，返回connection refused

同时加上maxConnections  
[![screenshot](http://img2.tbcdn.cn/L1/461/1/9d885179ca25d66921ca55908f61c2c419e13391.png "screenshot")](http://img2.tbcdn.cn/L1/461/1/9d885179ca25d66921ca55908f61c2c419e13391.png)

原来tomcat最大连接数取决于maxConnections这个值加上acceptCount这个值，在连接数达到了maxConenctions之后，tomcat仍会保持住连接，但是不处理，等待其它请求处理完毕之后才会处理这个请求。

## 源码分析

tomcat的最大连接数参数是maxConnections，这个值表示最多可以有多少个socket连接到tomcat上。BIO模式下默认最大连接数是它的最大线程数(缺省是200)，NIO模式下默认是10000，APR模式则是8192(windows上则是低于或等于maxConnections的1024的倍数)。如果设置为-1则表示不限制。

在tomcat里通过一个计数器来控制最大连接，比如在Endpoint的Acceptor里大致逻辑如下：

```
while (running) {
    ...    
    //if we have reached max connections, wait
    countUpOrAwaitConnection(); //计数+1，达到最大值则等待
 
    ...
    // Accept the next incoming connection from the server socket
    socket = serverSock.accept();
 
    ...
    processSocket(socket);
 
    ...
    countDownConnection(); //计数-1
    closeSocket(socket);
}
```

计数器是通过LimitLatch锁来实现的，它内部主要通过一个java.util.concurrent.locks.AbstractQueuedSynchronizer的实现来控制。

我们将最大连接数设置为10，同时启动超过30个长连接，  
然后通过jstack可以看到acceptor线程阻塞在countUpOrAwaitConnection方法上：

```
http-nio-8080-Acceptor-0" daemon prio=10 tid=0x00007f9cfc191000 nid=0x1e07 waiting on condition [0x00007f9ca9fde000]
   java.lang.Thread.State: WAITING (parking)
        at sun.misc.Unsafe.park(Native Method)
        - parking to wait for  <0x000000076595b688> (a org.apache.tomcat.util.threads.LimitLatch$Sync)
        at java.util.concurrent.locks.LockSupport.park(LockSupport.java:156)
        at java.util.concurrent.locks.AbstractQueuedSynchronizer.parkAndCheckInterrupt(AbstractQueuedSynchronizer.java:811)
        at java.util.concurrent.locks.AbstractQueuedSynchronizer.doAcquireSharedInterruptibly(AbstractQueuedSynchronizer.java:969)
        at java.util.concurrent.locks.AbstractQueuedSynchronizer.acquireSharedInterruptibly(AbstractQueuedSynchronizer.java:1281)
        at org.apache.tomcat.util.threads.LimitLatch.countUpOrAwait(LimitLatch.java:115)
        at org.apache.tomcat.util.net.AbstractEndpoint.countUpOrAwaitConnection(AbstractEndpoint.java:755)
        at org.apache.tomcat.util.net.NioEndpoint$Acceptor.run(NioEndpoint.java:787)
        at java.lang.Thread.run(Thread.java:662)

```

代码层面也解释了这种现象。

## 总结

tomcat能支持最大连接数由maxConnections加上acceptCount来决定。同时maxThreads如何设定？

以下部分结论引用自：[http://duanfei.iteye.com/blog/1894387](http://duanfei.iteye.com/blog/1894387)  
一般的服务器操作都包括两方面：1计算（主要消耗cpu），2等待（io、数据库等）

第一种极端情况，如果我们的操作是纯粹的计算，那么系统响应时间的主要限制就是cpu的运算能力，此时maxThreads应该尽量设的小，降低同一时间内争抢cpu的线程个数，可以提高计算效率，提高系统的整体处理能力。

第二种极端情况，如果我们的操作纯粹是IO或者数据库，那么响应时间的主要限制就变为等待外部资源，此时maxThreads应该尽量设的大，这样 才能提高同时处理请求的个数，从而提高系统整体的处理能力。此情况下因为tomcat同时处理的请求量会比较大，所以需要关注一下tomcat的虚拟机内 存设置和linux的open file限制。

现实应用中，我们的操作都会包含以上两种类型（计算、等待），所以maxThreads的配置并没有一个最优值，一定要根据具体情况来配置。

最好的做法是：在不断测试的基础上，不断调整、优化，才能得到最合理的配置。

acceptCount的配置，我一般是设置的跟maxThreads一样大，这个值应该是主要根据应用的访问峰值与平均值来权衡配置的。

如果设的较小，可以保证接受的请求较快相应，但是超出的请求可能就直接被拒绝

如果设的较大，可能就会出现大量的请求超时的情况，因为我们系统的处理能力是一定的

### [Linux查看连接数，并发数](http://duanfei.iteye.com/blog/1894387)

软连接   

Bat代码  

	ln -s /home/ictfmcg/data/photo /var/jtnd/data/photo  

tomcat 6的Connector配置如下   

Xml代码  

	<Connector port="8080" protocol="HTTP/1.1"  
	                 connectionTimeout="20000"  
	                 redirectPort="8443"  
	                maxThreads="800" acceptCount="1000"/>  

其中最后两个参数意义如下：   
maxThreads：tomcat起动的最大线程数，即同时处理的任务个数，默认值为200   
acceptCount：当tomcat起动的线程数达到最大时，接受排队的请求个数，默认值为100   
这两个值如何起作用，请看下面三种情况   
情况1：接受一个请求，此时tomcat起动的线程数没有到达maxThreads，tomcat会起动一个线程来处理此请求。   
情况2：接受一个请求，此时tomcat起动的线程数已经到达maxThreads，tomcat会把此请求放入等待队列，等待空闲线程。   
情况3：接受一个请求，此时tomcat起动的线程数已经到达maxThreads，等待队列中的请求个数也达到了acceptCount，此时tomcat会直接拒绝此次请求，返回connection refused   
maxThreads如何配置   
一般的服务器操作都包括量方面：1计算（主要消耗cpu），2等待（io、数据库等）   
第一种极端情况，如果我们的操作是纯粹的计算，那么系统响应时间的主要限制就是cpu的运算能力，此时maxThreads应该尽量设的小，降低同一时间内争抢cpu的线程个数，可以提高计算效率，提高系统的整体处理能力。   
第二种极端情况，如果我们的操作纯粹是IO或者数据库，那么响应时间的主要限制就变为等待外部资源，此时maxThreads应该尽量设的大，这样才能提高同时处理请求的个数，从而提高系统整体的处理能力。此情况下因为tomcat同时处理的请求量会比较大，所以需要关注一下tomcat的虚拟机内存设置和linux的open file限制。   
我在测试时遇到一个问题，maxThreads我设置的比较大比如3000，当服务的线程数大到一定程度时，一般是2000出头，单次请求的响应时间就会急剧的增加，   
百思不得其解这是为什么，四处寻求答案无果，最后我总结的原因可能是cpu在线程切换时消耗的时间随着线程数量的增加越来越大，   
cpu把大多数时间都用来在这2000多个线程直接切换上了，当然cpu就没有时间来处理我们的程序了。   
以前一直简单的认为多线程=高效率。。其实多线程本身并不能提高cpu效率，线程过多反而会降低cpu效率。   
当cpu核心数<线程数时，cpu就需要在多个线程直接来回切换，以保证每个线程都会获得cpu时间，即通常我们说的并发执行。   
所以maxThreads的配置绝对不是越大越好。   
现实应用中，我们的操作都会包含以上两种类型（计算、等待），所以maxThreads的配置并没有一个最优值，一定要根据具体情况来配置。   
最好的做法是：在不断测试的基础上，不断调整、优化，才能得到最合理的配置。   
acceptCount的配置，我一般是设置的跟maxThreads一样大，这个值应该是主要根据应用的访问峰值与平均值来权衡配置的。   
如果设的较小，可以保证接受的请求较快相应，但是超出的请求可能就直接被拒绝   
如果设的较大，可能就会出现大量的请求超时的情况，因为我们系统的处理能力是一定的。   
1、查看apache当前并发访问数：  

Bat代码  

	netstat -an | grep ESTABLISHED | wc -l  

   对比httpd.conf中MaxClients的数字差距多少。   
2、查看有多少个进程数：   

Bat代码  

	ps aux|grep httpd|wc -l  

3、可以使用如下参数查看数据   

Bat代码  

	#ps -ef|grep httpd|wc -l  
	1388   

　　统计httpd进程数，连个请求会启动一个进程，使用于Apache服务器。   
　　表示Apache能够处理1388个并发请求，这个值Apache可根据负载情况自动调整。   

Bat代码  

	#netstat -nat|grep -i "80"|wc -l  
	434	

　　netstat -an会打印系统当前网络链接状态，而grep -i "80"是用来提取与80端口有关的连接的，wc -l进行连接数统计。  www.2cto.com    
　　最终返回的数字就是当前所有80端口的请求总数。   

Bat代码  

	#netstat -na|grep ESTABLISHED|wc -l  
	376   
　　netstat -an会打印系统当前网络链接状态，而grep ESTABLISHED 提取出已建立连接的信息。 然后wc -l统计。   
　　最终返回的数字就是当前所有80端口的已建立连接的总数。   

Bat代码  

	netstat -nat||grep ESTABLISHED|wc  

    \- 可查看所有建立连接的详细记录   
　　查看Apache的并发请求数及其TCP连接状态：   
　　Linux命令：   

Bat代码  

	netstat -n | awk '/^tcp/ {++S\[$NF\]} END {for（a in S） print a, S\[a\]}'  

　　返回结果示例：   
　　LAST_ACK 5   
　　SYN_RECV 30   
　　ESTABLISHED 1597   
　　FIN_WAIT1 5	
　　FIN_WAIT2 504   
　　TIME_WAIT 1057   
　　其中的   
　　SYN_RECV表示正在等待处理的请求数；   
　　ESTABLISHED表示正常数据传输状态；   
　　TIME_WAIT表示处理完毕，等待超时结束的请求数。