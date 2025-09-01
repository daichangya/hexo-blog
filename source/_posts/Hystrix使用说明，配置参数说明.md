---
title: Hystrix使用说明，配置参数说明
id: 1439
date: 2024-10-31 22:01:56
author: daichangya
permalink: /archives/hystrix%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E%E9%85%8D%E7%BD%AE%E5%8F%82%E6%95%B0%E8%AF%B4%E6%98%8E/
tags: 
 - hystrix
---

# 一、什么情况下会触发fallback方法？

<table><tbody><tr><td valign="top"><p><strong>名字</strong></p></td><td valign="top"><p><strong>描述</strong></p></td><td valign="top"><p><strong>触发<span style="font-family:'Times New Roman';">fallback</span></strong></p></td></tr><tr><td valign="top"><p>EMIT</p></td><td valign="top"><p>值传递</p></td><td valign="top"><p>NO</p></td></tr><tr><td valign="top"><p>SUCCESS</p></td><td valign="top"><p>执行完成，没有错误</p></td><td valign="top"><p>NO</p></td></tr><tr><td valign="top"><p>FAILURE</p></td><td valign="top"><p>执行抛出异常</p></td><td valign="top"><p>YES</p></td></tr><tr><td valign="top"><p>TIMEOUT</p></td><td valign="top"><p>执行开始，但没有在允许的时间内完成</p></td><td valign="top"><p>YES</p></td></tr><tr><td valign="top"><p>BAD_REQUEST</p></td><td valign="top"><p>执行抛出<span style="font-family:'Times New Roman';">HystrixBadRequestException</span></p></td><td valign="top"><p>NO</p></td></tr><tr><td valign="top"><p>SHORT_CIRCUITED</p></td><td valign="top"><p>断路器打开，不尝试执行</p></td><td valign="top"><p>YES</p></td></tr><tr><td valign="top"><p>THREAD_POOL_REJECTED</p></td><td valign="top"><p>线程池拒绝，不尝试执行</p></td><td valign="top"><p>YES</p></td></tr><tr><td valign="top"><p>SEMAPHORE_REJECTED</p></td><td valign="top"><p>信号量拒绝，不尝试执行</p></td><td valign="top"><p>YES</p></td></tr></tbody></table>

# 二、fallback方法在什么情况下会抛出异常

<table><tbody><tr><td valign="top"><p><strong>名字</strong></p></td><td valign="top"><p><strong>描述</strong></p></td><td valign="top"><p><strong>抛异常</strong></p></td></tr><tr><td valign="top"><p align="justify">FALLBACK_EMIT</p></td><td valign="top"><p align="justify">Fallback值传递</p></td><td valign="top"><p align="justify">NO</p></td></tr><tr><td valign="top"><p align="justify">FALLBACK_SUCCESS</p></td><td valign="top"><p align="justify">Fallback执行完成，没有错误</p></td><td valign="top"><p align="justify">NO</p></td></tr><tr><td valign="top"><p align="justify">FALLBACK_FAILURE</p></td><td valign="top"><p align="justify">Fallback执行抛出出错</p></td><td valign="top"><p align="justify">YES</p></td></tr><tr><td valign="top"><p align="justify">FALLBACK_REJECTED</p></td><td valign="top"><p align="justify">Fallback信号量拒绝，不尝试执行</p></td><td valign="top"><p align="justify">YES</p></td></tr><tr><td valign="top"><p align="justify">FALLBACK_MISSING</p></td><td valign="top"><p align="justify">没有Fallback<span style="font-family:'宋体';">实例</span></p></td><td valign="top"><p align="justify">YES</p></td></tr></tbody></table>

# 三、hystrix dashboard界面监控参数

 ![](https://img-blog.csdn.net/20171123110838020?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdG9uZ3RvbmdfdXNl/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

# 四、配置信息（default或HystrixCommandKey）最常用的几项

**超时时间（默认1000ms，单位：ms）** 

（1）hystrix.command.default.execution.isolation.thread.timeoutInMilliseconds

在调用方配置，被该调用方的所有方法的超时时间都是该值，优先级低于下边的指定配置

（2）hystrix.command.HystrixCommandKey.execution.isolation.thread.timeoutInMilliseconds

在调用方配置，被该调用方的指定方法（HystrixCommandKey方法名）的超时时间是该值

线程池核心线程数

hystrix.threadpool.default.coreSize（默认为10）

Queue

（1）hystrix.threadpool.default.maxQueueSize（最大排队长度。默认-1，使用SynchronousQueue。其他值则使用 LinkedBlockingQueue。如果要从-1换成其他值则需重启，即该值不能动态调整，若要动态调整，需要使用到下边这个配置）

（2）hystrix.threadpool.default.queueSizeRejectionThreshold（排队线程数量阈值，默认为5，达到时拒绝，如果配置了该选项，队列的大小是该队列）

注意：如果maxQueueSize=-1的话，则该选项不起作用

断路器

（1）hystrix.command.default.circuitBreaker.requestVolumeThreshold（当在配置时间窗口内达到此数量的失败后，进行短路。默认20个）

For example, if the value is 20, then if only 19 requests are received in the rolling window (say a window of 10 seconds) the circuit will not trip open even if all 19 failed.

简言之，10s内请求失败数量达到20个，断路器开。

（2）hystrix.command.default.circuitBreaker.sleepWindowInMilliseconds（短路多久以后开始尝试是否恢复，默认5s）

（3）hystrix.command.default.circuitBreaker.errorThresholdPercentage（出错百分比阈值，当达到此阈值后，开始短路。默认50%）

**fallback**

hystrix.command.default.fallback.isolation.semaphore.maxConcurrentRequests（调用线程允许请求HystrixCommand.GetFallback()的最大数量，默认10。超出时将会有异常抛出，注意：该项配置对于THREAD隔离模式也起作用）

# **五、属性配置参数**

参数说明英文地址：[https://github.com/Netflix/Hystrix/wiki/Configuration](https://github.com/Netflix/Hystrix/wiki/Configuration)

HystrixProperty参考代码地址：[http://www.programcreek.com/java-api-examples/index.php?source_dir=Hystrix-master/hystrix-contrib/hystrix-javanica/src/test/java/com/netflix/hystrix/contrib/javanica/test/common/configuration/command/BasicCommandPropertiesTest.java](http://www.programcreek.com/java-api-examples/index.php?source_dir=Hystrix-master/hystrix-contrib/hystrix-javanica/src/test/java/com/netflix/hystrix/contrib/javanica/test/common/configuration/command/BasicCommandPropertiesTest.java)

## **（一）**[](#command-properties)**Command Properties**

以下属性控制HystrixCommand行为：

### 1、[](#execution)**Execution**

以下属性控制HystrixCommand.run()如何执行。

<table><tbody><tr><td valign="top"><p><strong>参数</strong></p></td><td valign="top"><p><strong>描述</strong></p></td><td valign="top"><p><strong>默认值</strong></p></td></tr><tr><td valign="top"><p>execution.isolation.strategy</p></td><td valign="top"><p>隔离策略，有<span style="font-family:'Times New Roman';">THREAD</span><span style="font-family:'宋体';">和</span><span style="font-family:'Times New Roman';">SEMAPHORE</span></p><p>THREAD - <span style="font-family:'宋体';">它在单独的线程上执行，并发请求受线程池中的线程数量的限制</span><br>SEMAPHORE - <span style="font-family:'宋体';">它在调用线程上执行，并发请求受到信号量计数的限制</span></p></td><td valign="top"><p>默认使用<span style="font-family:'Times New Roman';">THREAD</span><span style="font-family:'宋体';">模式，以下几种</span>场景可以使用<span style="font-family:'Times New Roman';">SEMAPHORE</span><span style="font-family:'宋体';">模式：</span></p><p>只想控制并发度</p><p>外部的方法已经做了线程隔离</p><p>调用的是本地方法或者可靠度非常高、耗时特别小的方法（如<span style="font-family:'Times New Roman';">medis</span><span style="font-family:'宋体';">）</span></p><p>&nbsp;</p></td></tr><tr><td valign="top"><p>execution.isolation.thread.timeoutInMilliseconds</p></td><td valign="top"><p>超时时间</p></td><td valign="top"><p>默认值：<span style="font-family:'Times New Roman';">1000</span></p><p>在<span style="font-family:'Times New Roman';">THREAD</span><span style="font-family:'宋体';">模式下，达到超时时间，可以中断</span></p><p>在<span style="font-family:'Times New Roman';">SEMAPHORE</span><span style="font-family:'宋体';">模式下，会等待执行完成后，再去判断是否超时</span></p><p>设置标准：</p><p>有<span style="font-family:'Times New Roman';">retry</span><span style="font-family:'宋体';">，</span><span style="font-family:'Times New Roman';">99meantime+avg meantime</span></p><p>没有<span style="font-family:'Times New Roman';">retry</span><span style="font-family:'宋体';">，</span><span style="font-family:'Times New Roman';">99.5meantime</span></p><p>&nbsp;</p></td></tr><tr><td valign="top"><p>execution.timeout.enabled</p></td><td valign="top"><p>HystrixCommand.run<span style="font-family:'宋体';">（）执行是否应该有超时。</span></p></td><td valign="top"><p>默认值：true</p></td></tr><tr><td valign="top"><p>execution.isolation.thread.interruptOnTimeout</p></td><td valign="top"><p>在发生超时时是否应中断<span style="font-family:'Times New Roman';">HystrixCommand.run</span><span style="font-family:'宋体';">（）执行。</span></p></td><td valign="top"><p>默认值：true</p><p>THREAD<span style="font-family:'宋体';">模式有效</span></p></td></tr><tr><td valign="top"><p><a href="#executionisolationthreadinterruptoncancel" rel="nofollow" target="_self"></a>execution.isolation.thread.interruptOnCancel</p></td><td valign="top"><p>当发生取消时，执行是否应该中断。</p></td><td valign="top"><p>默认值为false</p><p>THREAD<span style="font-family:'宋体';">模式有效</span></p></td></tr><tr><td valign="top"><p>execution.isolation.semaphore.maxConcurrentRequests</p></td><td valign="top"><p>设置在使用时允许到<span style="font-family:'Times New Roman';">HystrixCommand.run</span><span style="font-family:'宋体';">（）方法的最大请求数。</span></p></td><td valign="top"><p>默认值：<span style="font-family:'Times New Roman';">10</span></p><p>SEMAPHORE<span style="font-family:'宋体';">模式有效</span></p></td></tr></tbody></table>

### 2、[](#fallback)**Fallback**

以下属性控制HystrixCommand.getFallback()如何执行。这些属性适用于ExecutionIsolationStrategy.THREAD和ExecutionIsolationStrategy.SEMAPHORE。

<table><tbody><tr><td valign="top"><p><strong>参数</strong></p></td><td valign="top"><p><strong>描述</strong></p></td><td valign="top"><p><strong>默认值</strong></p></td></tr><tr><td valign="top"><p align="justify">fallback.isolation.semaphore.maxConcurrentRequests</p></td><td valign="top"><p>设置从调用线程允许<span style="font-family:'Times New Roman';">HystrixCommand.getFallback</span><span style="font-family:'宋体';">（）方法的最大请求数。</span></p></td><td valign="top"><p>SEMAPHORE<span style="font-family:'宋体';">模式有效</span></p><p>默认值：<span style="font-family:'Times New Roman';">10</span></p></td></tr><tr><td valign="top"><p align="justify">fallback.enabled</p></td><td valign="top"><p>确定在发生失败或拒绝时是否尝试调用<span style="font-family:'Times New Roman';">HystrixCommand.getFallback</span><span style="font-family:'宋体';">（）。</span></p></td><td valign="top"><p>默认值为true</p></td></tr></tbody></table>

### 3、**Circuit Breaker**

断路器属性控制HystrixCircuitBreaker的行为。

<table><tbody><tr><td valign="top"><p><strong>参数</strong></p></td><td valign="top"><p><strong>描述</strong></p></td><td valign="top"><p><strong>默认值</strong></p></td></tr><tr><td valign="top"><p>circuitBreaker.enabled</p></td><td valign="top"><p>确定断路器是否用于跟踪运行状况和短路请求（如果跳闸）。</p></td><td valign="top"><p>默认值为true</p></td></tr><tr><td valign="top"><p>circuitBreaker.requestVolumeThreshold</p></td><td valign="top"><p>熔断触发的最小个数<span style="font-family:'Times New Roman';">/10s</span></p></td><td valign="top"><p>默认值：<span style="font-family:'Times New Roman';">20</span></p></td></tr><tr><td valign="top"><p>circuitBreaker.sleepWindowInMilliseconds</p></td><td valign="top"><p>熔断多少秒后去尝试请求</p></td><td valign="top"><p>默认值：<span style="font-family:'Times New Roman';">5000</span></p></td></tr><tr><td valign="top"><p>circuitBreaker.errorThresholdPercentage</p></td><td valign="top"><p>失败率达到多少百分比后熔断</p></td><td valign="top"><p>默认值：<span style="font-family:'Times New Roman';">50</span></p><p>主要根据依赖重要性进行调整</p><p>&nbsp;</p></td></tr><tr><td valign="top"><p><a href="#circuitbreakerforceopen" rel="nofollow" target="_self"></a>circuitBreaker.forceOpen</p><p>&nbsp;</p></td><td valign="top"><p>属性如果为真，强制断路器进入打开（跳闸）状态，其中它将拒绝所有请求。</p></td><td valign="top"><p>默认值为<span style="font-family:'Times New Roman';">false</span></p><p>此属性优先于<span style="font-family:'Times New Roman';">circuitBreaker.forceClosed</span></p></td></tr><tr><td valign="top"><p>circuitBreaker.forceClosed</p></td><td valign="top"><p>该属性如果为真，则迫使断路器进入闭合状态，其中它将允许请求，而不考虑误差百分比。</p></td><td valign="top"><p>默认值为<span style="font-family:'Times New Roman';">false</span></p><p>如果是强依赖，应该设置为<span style="font-family:'Times New Roman';">true</span></p><p>circuitBreaker.forceOpen<span style="font-family:'宋体';">属性优先，因此如果</span><span style="font-family:'Times New Roman';">forceOpen</span><span style="font-family:'宋体';">设置为</span><span style="font-family:'Times New Roman';">true</span><span style="font-family:'宋体';">，此属性不执行任何操作。</span></p></td></tr></tbody></table>

### 4、[](#metrics)**Metrics**

以下属性与从HystrixCommand和HystrixObservableCommand执行捕获指标有关。

<table><tbody><tr><td valign="top"><p><strong>参数</strong></p></td><td valign="top"><p><strong>描述</strong></p></td><td valign="top"><p><strong>默认值</strong></p></td></tr><tr><td valign="top"><p>metrics.rollingStats.timeInMilliseconds</p></td><td valign="top"><p>此属性设置统计滚动窗口的持续时间（以毫秒为单位）。对于断路器的使用和发布<span style="font-family:'Times New Roman';">Hystrix</span><span style="font-family:'宋体';">保持多长时间的指标。</span></p></td><td valign="top"><p>默认值：10000</p></td></tr><tr><td valign="top"><p>metrics.rollingStats.numBuckets</p></td><td valign="top"><p>此属性设置rollingstatistical窗口划分的桶数。</p><p>以下必须为<span style="font-family:'Times New Roman';">true - “metrics.rollingStats.timeInMilliseconds</span>%metrics.rollingStats.numBuckets == 0” -<span style="font-family:'宋体';">否则将抛出异常。</span></p></td><td valign="top"><p>默认值：10</p></td></tr><tr><td valign="top"><p>metrics.rollingPercentile.enabled</p></td><td valign="top"><p>此属性指示是否应以百分位数跟踪和计算执行延迟。 如果禁用它们，则所有摘要统计信息（平均值，百分位数）都将返回<span style="font-family:'Times New Roman';">-1</span><span style="font-family:'宋体';">。</span></p></td><td valign="top"><p>默认值为true</p></td></tr><tr><td valign="top"><p><a href="#metricsrollingpercentiletimeinmilliseconds" rel="nofollow" target="_self"></a>metrics.rollingPercentile.timeInMilliseconds</p><p>&nbsp;</p></td><td valign="top"><p>此属性设置滚动窗口的持续时间，其中保留执行时间以允许百分位数计算，以毫秒为单位。</p></td><td valign="top"><p>默认值：60000</p></td></tr><tr><td valign="top"><p>metrics.rollingPercentile.numBuckets</p></td><td valign="top"><p>此属性设置<span style="font-family:'Times New Roman';">rollingPercentile</span><span style="font-family:'宋体';">窗口将划分的桶的数量。</span></p><p>以下内容必须为<span style="font-family:'Times New Roman';">true - “metrics.rollingPercentile.timeInMilliseconds</span>%metrics.rollingPercentile.numBuckets == 0” -<span style="font-family:'宋体';">否则将抛出异常。</span></p></td><td valign="top"><p>默认值：6</p></td></tr><tr><td valign="top"><p>metrics.rollingPercentile.bucketSize</p></td><td valign="top"><p>此属性设置每个存储桶保留的最大执行次数。如果在这段时间内发生更多的执行，它们将绕回并开始在桶的开始处重写。</p></td><td valign="top"><p>默认值：100</p></td></tr><tr><td valign="top"><p>metrics.healthSnapshot.intervalInMilliseconds</p></td><td valign="top"><p>此属性设置在允许计算成功和错误百分比并影响断路器状态的健康快照之间等待的时间（以毫秒为单位）。</p></td><td valign="top"><p>默认值：500</p></td></tr></tbody></table>

### 5、**Request Context**

这些属性涉及HystrixCommand使用的HystrixRequestContext功能。

<table><tbody><tr><td valign="top"><p><strong>参数</strong></p></td><td valign="top"><p><strong>描述</strong></p></td><td valign="top"><p><strong>默认值</strong></p></td></tr><tr><td valign="top"><p>requestCache.enabled</p></td><td valign="top"><p>HystrixCommand.getCacheKey<span style="font-family:'宋体';">（）是否应与</span><span style="font-family:'Times New Roman';">HystrixRequestCache</span><span style="font-family:'宋体';">一起使用，以通过请求范围的缓存提供重复数据删除功能。</span></p></td><td valign="top"><p>默认值为true</p></td></tr><tr><td valign="top"><p>requestLog.enabled</p></td><td valign="top"><p>HystrixCommand<span style="font-family:'宋体';">执行和事件是否应记录到</span><span style="font-family:'Times New Roman';">HystrixRequestLog</span><span style="font-family:'宋体';">。</span></p></td><td valign="top"><p>默认值为true</p></td></tr></tbody></table>

## **（二）Collapser Properties**

下列属性控制HystrixCollapser行为。

<table><tbody><tr><td valign="top"><p><strong>参数</strong></p></td><td valign="top"><p><strong>描述</strong></p></td><td valign="top"><p><strong>默认值</strong></p></td></tr><tr><td valign="top"><p>maxRequestsInBatch</p><p>&nbsp;</p></td><td valign="top"><p>此属性设置在触发批处理执行之前批处理中允许的最大请求数。</p></td><td valign="top"><p>Integer.MAX_VALUE</p></td></tr><tr><td valign="top"><p>timerDelayInMilliseconds</p><p>&nbsp;</p></td><td valign="top"><p>此属性设置创建批处理后触发其执行的毫秒数。</p></td><td valign="top"><p>默认值：10</p></td></tr><tr><td valign="top"><p>requestCache.enabled</p><p>&nbsp;</p></td><td valign="top"><p>此属性指示是否为<span style="font-family:'Times New Roman';">HystrixCollapser.execute</span><span style="font-family:'宋体';">（）和</span><span style="font-family:'Times New Roman';">HystrixCollapser.queue</span><span style="font-family:'宋体';">（）调用启用请求高速缓存。</span></p></td><td valign="top"><p>默认值：true</p></td></tr></tbody></table>

## （三）**ThreadPool Properties**

以下属性控制Hystrix命令在其上执行的线程池的行为。

大多数时候，默认值为10的线程会很好（通常可以做得更小）。

<table><tbody><tr><td valign="top"><p><strong>参数</strong></p></td><td valign="top"><p><strong>描述</strong></p></td><td valign="top"><p><strong>默认值</strong></p></td></tr><tr><td valign="top"><p>coreSize</p></td><td valign="top"><p>线程池<span style="font-family:'Times New Roman';">coreSize</span></p></td><td valign="top"><p>默认值：<span style="font-family:'Times New Roman';">10</span></p><p>设置标准：<span style="font-family:'Times New Roman';">qps*99meantime+breathing room</span></p></td></tr><tr><td valign="top"><p>maximumSize</p></td><td valign="top"><p>此属性设置最大线程池大小。 这是在不开始拒绝<span style="font-family:'Times New Roman';">HystrixCommands</span><span style="font-family:'宋体';">的情况下可以支持的最大并发数。 请注意，此设置仅在您还设置</span><span style="font-family:'Times New Roman';">allowMaximumSizeToDivergeFromCoreSize</span><span style="font-family:'宋体';">时才会生效。</span></p></td><td valign="top"><p>默认值：10</p></td></tr><tr><td valign="top"><p>maxQueueSize</p></td><td valign="top"><p>请求等待队列</p></td><td valign="top"><p>默认值：<span style="font-family:'Times New Roman';">-1</span></p><p>如果使用正数，队列将从<span style="font-family:'Times New Roman';">SynchronizeQueue</span><span style="font-family:'宋体';">改为</span><span style="font-family:'Times New Roman';">LinkedBlockingQueue</span></p></td></tr><tr><td valign="top"><p>queueSizeRejectionThreshold</p></td><td valign="top"><p>此属性设置队列大小拒绝阈值 <span style="font-family:'Times New Roman';">- </span><span style="font-family:'宋体';">即使未达到</span><span style="font-family:'Times New Roman';">maxQueueSize</span><span style="font-family:'宋体';">也将发生拒绝的人为最大队列大小。 此属性存在，因为</span><span style="font-family:'Times New Roman';">BlockingQueue</span><span style="font-family:'宋体';">的</span><span style="font-family:'Times New Roman';">maxQueueSize</span><span style="font-family:'宋体';">不能动态更改，我们希望允许您动态更改影响拒绝的队列大小。</span></p></td><td valign="top"><p>默认值：<span style="font-family:'Times New Roman';">5</span></p><p>注意：如果<span style="font-family:'Times New Roman';">maxQueueSize == -1</span><span style="font-family:'宋体';">，则此属性不适用。</span></p></td></tr><tr><td valign="top"><p>keepAliveTimeMinutes</p></td><td valign="top"><p>此属性设置保持活动时间，以分钟为单位。</p></td><td valign="top"><p>默认值：1</p></td></tr><tr><td valign="top"><p>allowMaximumSizeToDivergeFromCoreSize</p></td><td valign="top"><p>此属性允许<span style="font-family:'Times New Roman';">maximumSize</span><span style="font-family:'宋体';">的配置生效。 那么该值可以等于或高于</span><span style="font-family:'Times New Roman';">coreSize</span><span style="font-family:'宋体';">。 设置</span><span style="font-family:'Times New Roman';">coreSize &lt;maximumSize</span><span style="font-family:'宋体';">会创建一个线程池，该线程池可以支持</span><span style="font-family:'Times New Roman';">maximumSize</span><span style="font-family:'宋体';">并发，但在相对不活动期间将向系统返回线程。 （以</span><span style="font-family:'Times New Roman';">keepAliveTimeInMinutes</span><span style="font-family:'宋体';">为准）</span></p></td><td valign="top"><p>默认值：false</p></td></tr><tr><td valign="top"><p>metrics.rollingStats.timeInMilliseconds</p></td><td valign="top"><p>此属性设置statistical rolling窗口的持续时间（以毫秒为单位）。 这是为线程池保留多长时间。</p></td><td valign="top"><p>默认值：10000</p></td></tr><tr><td valign="top"><p>metrics.rollingStats.numBuckets</p></td><td valign="top"><p>此属性设置滚动统计窗口划分的桶数。<br>注意：以下必须为<span style="font-family:'Times New Roman';">true - “metrics.rollingStats.timeInMilliseconds</span>%metrics.rollingStats.numBuckets == 0” -<span style="font-family:'宋体';">否则将引发异常。</span></p></td><td valign="top"><p>默认值：10</p></td></tr></tbody></table>

## （四）**其他**

<table><tbody><tr><td valign="top"><p><strong>参数</strong></p></td><td valign="top"><p><strong>描述</strong></p></td><td valign="top"><p><strong>默认值</strong></p></td></tr><tr><td valign="top"><p>groupKey</p></td><td valign="top"><p>表示所属的<span style="font-family:'Times New Roman';">group</span><span style="font-family:'宋体';">，一个</span><span style="font-family:'Times New Roman';">group</span><span style="font-family:'宋体';">共用线程池</span></p></td><td valign="top"><p>默认值：<span style="font-family:'Times New Roman';">getClass().getSimpleName();</span></p></td></tr><tr><td valign="top"><p>commandKey</p></td><td valign="top"><p>&nbsp;</p></td><td valign="top"><p>默认值：当前执行方法名</p></td></tr></tbody></table>

