---
title: Java GC 调试手记
id: 623
date: 2024-10-31 22:01:44
author: daichangya
excerpt: "GC知识要点回顾问题1：为什么要调试GC参数？在32核处理器的系统上，10%的GC时间导致75%的吞吐量损失。所以在大型系统上，调试GC是以小博大的不错选择。'small improvements in reducing such a bottleneck can produce large gains in perform"
permalink: /archives/19044099/
categories:
 - javagc
---

 

## 摘要

本文记录GC调试的一次实验过程和结果。

## GC知识要点回顾

问题1：为什么要调试GC参数？  
[在32核处理器的系统上，10%的GC时间导致75%的吞吐量损失](http://www.oracle.com/technetwork/java/javase/gc-tuning-6-140523.html)。所以在大型系统上，调试GC是以小博大的不错选择。'small improvements in reducing such a bottleneck can produce large gains in performance.'

  

![](http://www.oracle.com/ocom/groups/public/@otn/documents/digitalasset/190242.gif)

问题2：怎么样调试GC?

调试GC，有[三个主要的参数](http://blogs.oracle.com/jonthecollector/entry/the_second_most_important_gc)：

*   选择合适的GC Collector
*   整个JVM Heap堆的大小
*   Young Generation的大小(-Xmn?m or -XX:NewRatio=?)

问题3：有哪些不同的GC Collector?

Tony Printezis (JVM大牛)在[Garbage Collection in the Java HotSpot Virtual Machine](http://www.devx.com/Java/Article/21977/1954)有图为证，还有一篇更早的[sun开发人员介绍GC调试](http://developers.sun.com/mobility/midp/articles/garbagecollection2/)也是有图为证

  

[neo4j](http://docs.neo4j.org/chunked/snapshot/configuration-jvm.html)总结如下
<table cellspacing="0" cellpadding="0" border="1" style="border:1px solid rgb(102,102,102);color:rgb(0,0,0);font-family:'Lucida Bright', Cambria, serif;line-height:19px;"><thead style="border-width:1px 1px 2px;border-style:solid;border-color:rgb(102,102,102);font-weight:bold;"><tr style="border:1px solid rgb(102,102,102);"><th align="left" valign="top" style="color:rgb(51,51,51);font-family:Candara, 'Myriad Pro', Myriad, 'Lucida Sans', 'Trebuchet MS', sans-serif;line-height:1.2;border:1px solid rgb(102,102,102);">
GC shortname</th>
<th align="left" valign="top" style="color:rgb(51,51,51);font-family:Candara, 'Myriad Pro', Myriad, 'Lucida Sans', 'Trebuchet MS', sans-serif;line-height:1.2;border:1px solid rgb(102,102,102);">
Generation</th>
<th align="left" valign="top" style="color:rgb(51,51,51);font-family:Candara, 'Myriad Pro', Myriad, 'Lucida Sans', 'Trebuchet MS', sans-serif;line-height:1.2;border:1px solid rgb(102,102,102);">
Command line parameter</th>
<th align="left" valign="top" style="color:rgb(51,51,51);font-family:Candara, 'Myriad Pro', Myriad, 'Lucida Sans', 'Trebuchet MS', sans-serif;line-height:1.2;border:1px solid rgb(102,102,102);">
Comment</th>
</tr></thead><tbody style="border:1px solid rgb(102,102,102);"><tr style="border:1px solid rgb(102,102,102);"><td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
Copy</p>
</td>
<td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
Young</p>
</td>
<td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
<code class="literal" style="color:#000080;font-family:Consolas, Monaco, monospace;font-size:.8em;">-XX:+UseSerialGC</code></p>
</td>
<td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
The Copying collector</p>
</td>
</tr><tr style="border:1px solid rgb(102,102,102);"><td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
MarkSweepCompact</p>
</td>
<td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
Tenured</p>
</td>
<td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
<code class="literal" style="color:#000080;font-family:Consolas, Monaco, monospace;font-size:.8em;">-XX:+UseSerialGC</code></p>
</td>
<td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
The Mark and Sweep Compactor</p>
</td>
</tr><tr style="border:1px solid rgb(102,102,102);"><td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
ConcurrentMarkSweep</p>
</td>
<td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
Tenured</p>
</td>
<td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
<code class="literal" style="color:#000080;font-family:Consolas, Monaco, monospace;font-size:.8em;">-XX:+UseConcMarkSweepGC</code></p>
</td>
<td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
The Concurrent Mark and Sweep Compactor</p>
</td>
</tr><tr style="border:1px solid rgb(102,102,102);"><td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
ParNew</p>
</td>
<td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
Young</p>
</td>
<td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
<code class="literal" style="color:#000080;font-family:Consolas, Monaco, monospace;font-size:.8em;">-XX:+UseParNewGC</code></p>
</td>
<td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
The parallel Young Generation Collector — can only be used with the Concurrent mark and sweep compactor.</p>
</td>
</tr><tr style="border:1px solid rgb(102,102,102);"><td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
PS Scavenge</p>
</td>
<td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
Young</p>
</td>
<td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
<code class="literal" style="color:#000080;font-family:Consolas, Monaco, monospace;font-size:.8em;">-XX:+UseParallelGC</code></p>
</td>
<td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
The parallel object scavenger</p>
</td>
</tr><tr style="border:1px solid rgb(102,102,102);"><td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
PS MarkSweep</p>
</td>
<td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
Tenured</p>
</td>
<td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
<code class="literal" style="color:#000080;font-family:Consolas, Monaco, monospace;font-size:.8em;">-XX:+UseParallelGC</code></p>
</td>
<td align="left" valign="top" style="line-height:1.2;border:1px solid rgb(102,102,102);">
<p style="font-family:'Lucida Bright', Cambria, serif;font-size:.9375em;line-height:1.6em;">
The parallel mark and sweep collector</p>
</td>
</tr></tbody></table>

简而言之，Young和Tenured各种三种Collector，分别是

*   Serial 单线程
*   Parallel 多线程并行, GC线程和App线程取一运行，即GC要Stop the (app) world。
*   Concurrent 多线程并发，GC线程和App线程可同时运行。(注: Young generation 没有CMS，取而代之的是可和CMS(Old)一起运行的ParNew)

![](http://www.devx.com/assets/articlefigs/11040.png)  

  

问题4：如何选择Collector?

Serial可以直接排除掉，现在最普通的服务器也有双核64位\\8G内存，默认的Collector是PS Scavenge和PS MarkSweep。所以Collector在并行(Parallel)和并发(Concurrent)两者之间选择。

  

问题5：选择的标准(参数指标)是什么?如何得到这些参数值(How to measure it)?

throughput和latency。[garbage-collection-in-java-part-3](http://www.softwareengineeringsolutions.com/blogs/2010/05/01/garbage-collection-in-java-part-3/)从GC的耗时给出了吞吐量和响应速度的公式

```
Total Execution Time = Useful Time + Paused Time  
throughput = Useful Time / Total Execution Time
latency = average paused time
```

  

如何得到Useful time 和 Paused Time?即如何得到JVM的GC时间，有以下几种方式

**GC Log**

打印GC log，java 启动参数中加入下面的语句(本文为tomcat应用)。GC Log 记录每次GC时间，可根据GC Log计算平均GC时间和累积GC时间。  

```
1.  CATALINA\_OPTS="$CATALINA\_OPTS -verbose:gc -Xloggc:/usr/local/tomcat/gc -XX:+PrintGCDetails -XX:+PrintGCTimeStamps"  
```

**[Jconsole](http://docs.oracle.com/javase/6/docs/technotes/guides/management/jconsole.html)**

JDK自带工具，java 启动参数中加入下面的语句(本文为tomcat应用)，然后在监控端可以远程连接1090端口。在内存一项，有累积GC时间和次数。注意在以min为单位显示时，只显示整数部分，如1min20s显示为1min。

```
1.  CATALINA\_OPTS="$CATALINA\_OPTS -Dcom.sun.management.jmxremote.port=1090 -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.authenticate=false"  
```
  

**[VisualGC](http://java.sun.com/performance/jvmstat/visualgc.html)**

JVM监控工具，未同JDK一起发布，可在[JVisualvm](http://visualvm.java.net/)(JDK自带)中以插件的方式使用，本文为独立使用。有累积GC时间和次数，并有曲线图直观显示。

首先在Server端启动jstatd

```

1.  vi jstatd.all.policy  

3.  grant codebase "file:${java.home}/../lib/tools.jar" {  
4.      permission java.security.AllPermission;  
5.  };  

7.  jstatd -J-Djava.security.policy=jstatd.all.policy  
```
  

然后在监控启动VisualGC，远程连接服务端进程id

**visualgc 102592@remote.domain**

  

问题5：应用请求的吞吐量和响应是否可以反映JVM的性能?

正是我们调优的目标。本文使用Jmeter来做压力测试，并给出吞吐量和响应 report。

## 测试

**硬件环境**

<table cellpadding="1"><tbody><tr><td align="left" colspan="2"><div class="table-box"><table cellpadding="1"><tbody><tr><th valign="top" align="right" nowrap="nowrap">操作系统:&nbsp;</th><td colspan="1">Linux 2.6.18-53.el5</td></tr><tr><th valign="top" align="right" nowrap="nowrap">体系结构:&nbsp;</th><td colspan="1">amd64</td></tr><tr><th valign="top" align="right" nowrap="nowrap">处理器的数目:&nbsp;</th><td colspan="1">2</td></tr><tr><th valign="top" align="right" nowrap="nowrap">分配的虚拟内存:&nbsp;</th><td colspan="1"><tt>2,680,408</tt>&nbsp;Kb</td></tr></tbody></table></div></td><td align="left" colspan="2"><div class="table-box"><table cellpadding="1"><tbody><tr><th valign="top" align="right" nowrap="nowrap">物理内存总量:&nbsp;</th><td colspan="1"><tt>8,175,632</tt>&nbsp;Kb</td></tr><tr><th valign="top" align="right" nowrap="nowrap">可用物理内存:&nbsp;</th><td colspan="1"><tt>1,140,520</tt>&nbsp;Kb</td></tr><tr><th valign="top" align="right" nowrap="nowrap">交换空间总量:&nbsp;</th><td colspan="1"><tt>8,594,764</tt>&nbsp;Kb</td></tr><tr><th valign="top" align="right" nowrap="nowrap">可用交换空间:&nbsp;</th><td colspan="1"><tt>8,594,680</tt>&nbsp;Kb</td></tr></tbody></table></div></td></tr></tbody></table>

  

**Test case**

1.  使用用[Jmeter](http://code.google.com/p/algo4j/wiki/JMeter)压力测试
2.  共6个client，每个client启动30个线程发送请求
3.  每个请求从16种测试样例中随机挑选一个，发送到server端
4.  测试持续10min

**参数值**

1.  server使用默认GC(PS Scavenge和PS MarkSweep)
2.  server使用CMS(-XX:+UseConcMarkSweepGC-XX:+UseParNewGC)
3.  server使用CMS(-XX:+UseConcMarkSweepGC -XX:+UseParNewGC)，设置Young generation的大小为200m(-Xmn200m)
4.  server使用CMS(-XX:+UseConcMarkSweepGC -XX:+UseParNewGC)，设置Young generation的大小为600m(-Xmn600m)

**观察值**

1.  Jmeter请求的summary report
2.  server端累积GC时间和次数

**测试结果**

1) CMS和Parallel比较

1.1) 吞吐量和响应

![](http://hi.csdn.net/attachment/201202/2/0_1328150404rqmC.gif)(PS Scavenge和PS MarkSweep)  

![](http://hi.csdn.net/attachment/201202/2/0_1328150506V2bH.gif)(ParNew和CMS)  

从Jmeter的report中可以看出, 使用CMS后吞吐量(对应总的请求数)下降18%，而最大响应时间(包括最小响应时间)有近30%的提升(变小)。这验证了Tony Printezis在Step-by-Step:Garbage Collection Tuning in the Java HotSpot™ Virtual Machine中说使用CMS应用的吞吐量会相对下降，但有更好的最差响应时间。

*   Expect longer young GC times
    *   Due to slower allocations into the old gen
*   Expect better worst-case latencies
    *   CMS does its work mostly-concurrently
    *   Shorter worst-case pauses
*   Expect lower throughput
    *   CMS does more work

在官方的JVM性能调优中给出的建议也是，如果你的应用对峰值处理有要求，而对一两秒的停顿可以接受，则使用(-XX:+UseParallelGC)；如果应用对响应有更高的要求，停顿最好小于一秒，则使用(-XX:+UseConcMarkSweepGC)。

  

1.2) GC 累积时间和次数  

![](http://hi.csdn.net/attachment/201202/2/0_132815152159A3.gif)(PS Scavenge和PS MarkSweep)  

![](http://hi.csdn.net/attachment/201202/2/0_13281516439zZa.gif)(ParNew和CMS)  

  

PS累积GC时间(visualgc)为1min25s，其中Eden 189次，共52s；old 13次，共33s。

CMS 累积GC(visualgc)为2min2s，其中Eden 2333次，共1min46s；old 55次，共16s。(Jconsole和GC log却显示没有Full GC，从[understanding cms gc logs](http://blogs.oracle.com/poonam/entry/understanding_cms_gc_logs)和[jstat显示的full GC次数与CMS周期的关系](http://rednaxelafx.iteye.com/blog/1108768)中我推测visualgc与jstat显示一致，都是统计old的回收次数；而Full GC则是Young和Old一起回收，在其他类型的GC里，Old只有Full GC时才触发)。  

  

可以看到PS的GC频率相对低，但每次GC时间长，每次Full在3s左右徘徊，Yong在0.3s左右；CMS则是短频快，频繁快速回收，yong在0.03s(<0.1s)左右，old<0.5s。从JMeter上，使用PS GC，Request Report会有间歇性的停顿，即server没有任何响应；CMS则相对较少，停顿不那么明显。

  

2) CMS下不同Xmn的比较  

由于CMS Young太多频繁，又测试了分别调整Xmn为200m和600m之后的结果。200m是仿照[cassandra](https://github.com/apache/cassandra/blob/trunk/conf/cassandra-env.sh)中100m * cpu #来设置Young gen的大小；600m则是与PS下的Young gen一致。

  

![](http://hi.csdn.net/attachment/201202/2/0_1328159817Dsf2.gif)200m  

![](http://hi.csdn.net/attachment/201202/2/0_1328159837zTBK.gif)600m  

  

随着Young gen的增大(40m -> 200m -> 600m)，Young 的回收次数减少，Old的回收次数增加，总体GC累积时间下降，应用吞吐量上升，最差响应时间变慢(即便和PS比较也更差，是我的测试有问题?)。

## 结论

app停顿3s是不可接受的，因此倾向于使用CMS；CMS的default young gen相当小，于是设置Xmn。对于更加Prefer响应的应用，下面配置是否是黄金标配:

```
JVM_OPTS="$JVM_OPTS -XX:+UseParNewGC"
JVM_OPTS="$JVM_OPTS -XX:+UseConcMarkSweepGC"
JVM_OPTS="$JVM_OPTS -XX:+CMSParallelRemarkEnabled"
JVM_OPTS="$JVM_OPTS -XX:SurvivorRatio=8"
JVM_OPTS="$JVM_OPTS -XX:MaxTenuringThreshold=1"
JVM_OPTS="$JVM_OPTS -XX:CMSInitiatingOccupancyFraction=75"
JVM_OPTS="$JVM_OPTS -XX:+UseCMSInitiatingOccupancyOnly"
```