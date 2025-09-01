---
title: 贯穿应用开发始终的八大性能陷阱
id: 939
date: 2024-10-31 22:01:47
author: daichangya
excerpt: 摘要：将应用交付给终端用户正变得越来越难，因为会涉及到更多的组件，也因此更容易犯错。技术性能公司Compuware总结了贯穿应用始终的八大影响应用性能的陷阱，望开发者引以为戒。数据库访问低效、框架配置错误、内存使用过度、网页臃肿，以及不遵循常见Web性能最佳实践都是应用开发中常见的、影响应用性能的主要陷阱
  。技术性能公司Computeware从实际案例总结了贯穿应用始终的八大影响应用性
permalink: /archives/guan-chuan-ying-yong-kai-fa-shi-zhong/
categories:
- 系统架构
---

 

**摘要：** 将应用交付给终端用户正变得越来越难，因为会涉及到更多的组件，也因此更容易犯错。技术性能公司Compuware总结了贯穿应用始终的八大影响应用性能的陷阱，望开发者引以为戒。

数据库访问低效、框架配置错误、内存使用过度、网页臃肿，以及不遵循常见Web性能最佳实践都是应用开发中常见的、影响应用性能的主要陷阱 。技术性能公司Computeware从实际案例总结了贯穿应用始终的八大影响应用性能的陷阱，这些陷阱不仅仅局限于应用开发中，还涉及到整个应用交付流程，包括从终端用户到后台系统的所有组件、数据库以及第三方服务等等，望运维人员、架构师、测试人员和开发人员引以为戒。CSDN摘译如下：

[![](http://cms.csdnimg.cn/article/201304/15/516c092c62191_middle.jpg) ](http://cms.csdnimg.cn/article/201304/15/516c092c62191.jpg)  

**一、臃肿的Web前端**

面向群体：运维人员、架构师、测试人员、开发人员

通常企业在重构代码、优化SQL语句、应用缓存等方面都作了充足的优化，其中大部分对应用的最终用户并不可见。然而直接与用户交互的Web前端却被常常被完全忽视。

根据我们跟踪的来源，传递给用户的页面在过去的3-4年里，无论是大小还是复杂度都稳步增长，同时增长的还有用户对性能的要求。企业需要意识到，他们认为重要的其实并不是最重要的，他们更需要解决的是迎合用户的需求。但如何判断Web前端是否臃肿？

通常的做法是和你的主要竞争对手以及行业领导者比较，同对横向对比更容易设定一个合理的目标。另外，理解为什么用户会离开你的网站也能够帮助解决客户体验问题：离开你网站的主要是哪类人群？臃肿、缓慢的页面上是否有应用功能？

[![](http://cms.csdnimg.cn/article/201304/15/516c0957233c7_middle.jpg) ](http://cms.csdnimg.cn/article/201304/15/516c0957233c7.jpg)  

你可以使用缓存、压缩以及CDN来应对这样的问题，同时应该更严格地去审核每一个新添加的功能，必要时做一些精简，这可以提供更好的用户体验。

**推荐阅读：**

*   [Performance Improvement is not Performance Optimization](http://apmblog.compuware.com/2012/10/03/performance-improvement-is-not-performance-optimization/)
*   [Super Bowl Sunday 2013 – Winners, Losers, and Casualties](http://apmblog.compuware.com/2013/02/07/super-bowl-sunday-2013-winners-losers-and-casualties/)

### 二、缓慢的第三方内容和CDN

面向群体：运维人员、架构师、测试人员

仅仅关注自己的内容容易导致忽略外部组织对网站性能的影响。随着企业越来越多地使用第三方资源，应用性能管理变得更加复杂，即使这些第三方服务是为提升性能而引入的。

通过观察过去12个月的性能峰值时期——比如假日购物季和超级碗——的数据，我们发现了两大趋势——第三方服务在用户集中访问的高峰期难以支撑，CDN也在庞大的流量下艰难应付。

分析、社会媒体、网络字体以及流行的JavaScript库等等项目往往来自于无法直接控制的第三方服务，但是你却依赖它来保证网站有效、可靠。当这些服务出问题时，用户记住的是“你”出问题了，而对这背后的第三方服务一无所知，导致你的企业品牌受损。

监视、管理第三方意味着需要将它们当作独立应用、独立的基准、独立的SLA（Service Level Agreement，服务品质协议）或者独立的SLO（Service Level Objective，服务水平目标）。因此你需要自问：

*   系统进行过负载测试了吗？
*   网站三大用户高峰期同时遇到时第三方服务是否能够抗住压力？
*   遇到性能问题时是否存在扩展计划？
*   过去的12个月最繁忙的8个小时中，网站用户体验达到平均性能要求了吗？

[![](http://cms.csdnimg.cn/article/201304/15/516c097aefc73_middle.jpg) ](http://cms.csdnimg.cn/article/201304/15/516c097aefc73.jpg)  

最后，你的团队还需要应对这样的场景：如果相关第三方服务/CDN遇到严重服务故障或者降低你网站的性能指标怎么办？永远要准备好B计划、C计划，以缓解这些意外的问题。具体操作包括在访问高峰期移除第三方标签、图片、内容；将内容移动到备用云服务商；多CDN间负载平衡；在访问高峰期将用户切换至简化版本的网站，直到流量恢复正常。

想要真正控制第三方服务，你必须了解其对网站性能的影响，甚至控制第三方组件的方方面面。

**推荐阅读：**

*   [You only control 1/3 of your Page Load Performance!](http://apmblog.compuware.com/2011/11/08/you-only-control-one-thrid-of-your-page-load-performance/)
*   [Third Party Content Management applied: Four steps to gain control of your Page Load Performance!](http://apmblog.compuware.com/2011/12/20/third-party-content-management-applied/)
*   [The Ripple Effect of Facebook’s Outage, Third-Party Issues and the Performance Ripple Effect](http://apmblog.compuware.com/2012/06/15/the-ripple-effect-of-facebooks-outage/)
*   [Website’s Vulnerability to Third-Party Services Exposed](http://apmblog.compuware.com/2012/11/05/websites-vulnerability-to-third-party-services-exposed/)
*   [Super Bowl Sunday 2013 – Winners, Losers, and Casualties](http://apmblog.compuware.com/2013/02/07/super-bowl-sunday-2013-winners-losers-and-casualties/)
*   [Why Bon Ton needs real-time visibility into 85% of its content delivered by Akamai](http://apmblog.compuware.com/2013/01/30/why-bon-ton-needs-real-time-visibility-into-85-of-its-content-delivered-by-akamai/)

### 三、框架的错误使用

面向群体：架构师、开发人员

通常网站或者应用少不了使用到第三方类库，比如Hibernate、Spring、Telerik RadControls、jQuery、ExtJS、GWT等等，因为这些第三方工具能够让你免于重写很多常见功能代码，大大提升了工作效率，因此这种现状可能永远不会改变。根据我们的调查，很多框架都没有被正确地使用，或者没有根据应用做专门的优化。

趋势表明开发人员习惯于在网络上寻找框架，往往在简单的示例上做过验证后就应用于企业应用，而并没有验证框架是否支持所有用例、是否易于扩展并且符合需求。在很多情况下，这些框架“仅仅”是需要更好的设置，比如为Hibernate做正确的缓存策略，或者换用高级API方法，访问SharePoint中List数据。

下面这张图片显示Hibernate多次执行了同一条SQL语句，而在优化的模式下，应该使用缓存来避免之后的重复查询。

[![](http://cms.csdnimg.cn/article/201304/15/516c09af28a6a_middle.jpg) ](http://cms.csdnimg.cn/article/201304/15/516c09af28a6a.jpg)  

最后，框架常常在更新中提升功能、性能、以及稳定性，您应该仔细查看这些更新以从中受益。常见的案例就是从不更新jQuery，以至于在过旧版本的浏览器中体验糟糕，甚至也无法充分发挥最新IE、Firefox、Chrome浏览器的性能。

**推荐阅读：**

*   [The Session Cache](http://apmblog.compuware.com/2009/02/16/understanding-caching-in-hibernate-part-one-the-session-cache/)
*   [The Query Cache](http://apmblog.compuware.com/2009/02/16/understanding-caching-in-hibernate-part-two-the-query-cache/)
*   [Second Level Cache](http://apmblog.compuware.com/2009/03/24/understanding-caching-in-hibernate-part-three-the-second-level-cache/)
*   [Top SharePoint Performance Mistakes](http://apmblog.compuware.com/2010/03/18/how-to-avoid-the-top-5-sharepoint-performance-mistakes/)
*   [101 on jQuery Selector Performance](http://apmblog.compuware.com/2009/11/09/101-on-jquery-selector-performance/)

### 四、网络基础设施问题

面向群体：运维人员、架构师、测试人员

网络基础设施是企业经营成功的基础，但是出问题时也难以分析原因，同一个问题可能有不同的起因，运维团队需要应用程序性能监控解决方案，以轻松、快速地将故障域隔离。

性能问题的代价可能非常昂贵。根据Aberdeen Group的报告，甚至可能降低9%的收入以及64%的生产效率。如果采用的是SAP基础设施，每分钟宕机成本甚至可能高达$15000。

[![](http://cms.csdnimg.cn/article/201304/15/516c09f119d21_middle.jpg) ](http://cms.csdnimg.cn/article/201304/15/516c09f119d21.jpg)  

判断究竟网络还是应用问题可以通过检查网络、服务器时间异常值与基准流量的比较而分辨出。但仅仅目测报告是不足以避免问题的，积极的应用性能管理首先需要及时响应关键衡量值在异常时APM工具发出的警报。

### 五、云平台的伸缩性

面向群体：运维人员、架构师

云计算提供了一个非常宏伟的承诺：只要你需要，可以提供无尽的资源、无尽的扩展性。这避免了硬件的过度闲置，同时可以随时应对超出预期的性能需求。

但云计算同样存在陷阱：如果你的应用程序并非为可扩展而设计，硬件上再大的可扩展性也没有意义。同时，你还需要明白，云计算——除非是私有云设施——实际上并不为你所有。直接访问底层硬件要更加困难得多，因此监控起起来也更困难。

云也不仅仅是一个无穷无尽的CPU、内存和磁盘的资源池，它同样提供了很多其他的服务,例如存储、通知，以及其它必须了解和监控的服务，它们都是非常关键的组件。

[![](http://cms.csdnimg.cn/article/201304/15/516c0a195beae_middle.jpg)](http://cms.csdnimg.cn/article/201304/15/516c0a195beae.jpg)

**推荐阅读：**

*   [Managing Hybrid Cloud Environments](http://apmblog.compuware.com/2011/12/21/clouds-on-cloud-nine-the-challenge-of-managing-hybrid-cloud-environments/)
*   [Analyzing Performance of Windows Azure Storage](http://apmblog.compuware.com/2012/07/04/how-to-monitor-and-analyze-performance-of-the-windows-azure-storage-service/)
*   [Why Performance Monitoring is easier in Public than onPremise Clouds](http://apmblog.compuware.com/2011/05/26/why-perfomance-management-is-easier-in-public-than-onpremise-clouds/)
*   [Monitoring your Clouds](http://apmblog.compuware.com/2011/04/22/the-rise-and-fall-of-the-machines-watching-out-for-clouds/)

### 六、过多的数据库调用

面向群体：架构师、测试人员、开发者

数据库访问也是我们经常遇到的应用问题,当我们在几乎所有共事的应用中都发现了这一问题。我们注意到一点，被问责的通常是应用对数据库的访问模式而非数据库设置。我们经常看到一条Web请求会查询数千条数据库状态，这背后常常有很多原因。

下面这张图中显示了某企业应用调用大型机的工作流程，该大型机每次事物会执行225条SQL。通过更仔细地观察我们发现，因为上面提到的原因，同一条声明被请求了数百次。

[![](http://cms.csdnimg.cn/article/201304/15/516c0a5f05683_middle.jpg) ](http://cms.csdnimg.cn/article/201304/15/516c0a5f05683.jpg)  

除了访问模式问题，我们同时发现某些语句的执行时间过长，在这种情况下，不仅需要关注调整索引指数等数据库，分析这些语句是否可以从应用内优化也至关重要。我们经常遇到很多数据从数据库中被检索出来（使用外部存储），然后迅速被释放（GC过于活跃）。常见的陷阱还有连接池配置错误以及应用维持连接过久导致其它线程访问数据库遭阻塞。

下面的图片显示某数据库查询执行的事务流程，其中多数需要很长时间来执行。解决这个问题需要同时就在应用和数据库端做优化。

[![](http://cms.csdnimg.cn/article/201304/15/516c0a81d59a6_middle.jpg) ](http://cms.csdnimg.cn/article/201304/15/516c0a81d59a6.jpg)  

**推荐阅读：**

*   [Don’t let your load balancers ruin your holiday business](http://apmblog.compuware.com/2012/10/31/dont-let-your-load-balancers-ruin-your-holiday-business/)
*   [Saving MIPS and Money](http://apmblog.compuware.com/2013/02/12/saving-mips-and-money-automated-mainframe-transaction-tracing-and-analysis/)
*   [The reason I don’t monitor connection pool usage](http://apmblog.compuware.com/2011/11/22/the-reason-i-dont-monitor-connection-pool-usage/)

### 七、大数据未经优化

面向群体：运维人员、架构师、测试人员、开发者

应用需要处理的数据正在持续增长，大数据解决方案（NoSQL、MapReduce……）提供了新的数据存储、处理方案，但是每一项新的技术都需要为你特定的应用做相应的优化。但是这常常被误解，甚至有人认为只要增加一个额外的功能/模块（比如MapReduce）就能处理/存储更多的数据。

实际上，这仅适用于应用可扩展的情况。

下面这张图中事务处理的大部分时间都花费在MongoDB上，仔细观察你会发现该框架访问MongoDB时会额外执行一次计数方法，而这是完全不必要的。在本例中，通过简单地消除不必要的调用就获得了15倍的事务性能提升。

[![](http://cms.csdnimg.cn/article/201304/15/516c0aa3bb276_middle.jpg) ](http://cms.csdnimg.cn/article/201304/15/516c0aa3bb276.jpg)  

**推荐阅读：**

*   [MongoDB Anti-Pattern](http://apmblog.compuware.com/2013/02/05/how-i-identified-a-mongodb-performance-anti-pattern-in-5-minutes/)
*   [NoSQL vs Traditional Databases](http://apmblog.compuware.com/2012/10/24/nosql-or-traditonal-database-from-an-apm-perspective-there-isnt-really-much-difference/)
*   [Inside Cassandra Write Performance](http://apmblog.compuware.com/2011/09/20/cassandra-write-performance-a-quick-look-inside/)
*   [What we can Learn from Cassandra Pagination](http://apmblog.compuware.com/2011/12/05/pagination-with-cassandra-and-what-we-can-learn-from-it/)
*   [15x Performance Improvements for Pig+HBase](http://apmblog.compuware.com/2013/02/19/speeding-up-a-pighbase-mapreduce-job-by-a-factor-of-15/)

### 八、隐秘的内存泄漏

面向群体：架构师、测试人员、开发者

内存和垃圾回收问题在任何企业应用中都非常突出，原因之一就在于GC的本质常常被人误解。除了常见的内存相关问题，比如高内存使用率、错误的缓存策略，同样的问题还存在于类的加载、过大的类以及本地内存。下面这张图中的的问题就在于需要加载一个庞大的类，它占据了过多的内存，这是给非常糟糕的做法。

[![](http://cms.csdnimg.cn/article/201304/15/516c0ac0d729d_middle.jpg) ](http://cms.csdnimg.cn/article/201304/15/516c0ac0d729d.jpg)  

内存泄漏通常会导致内存用尽异常，往往进一步导致虚拟机崩溃，甚至会使用户当前会话和活跃事务的丢失，带来的影响非常负面，因此避免内存泄漏非常有必要。

此外，高的内存占用率也会导致更为频繁的GC，对用户响应时间产生直接影响，会话会因为长期运行的GC进程而停止。这种情况可以通过优化GC设置来调整，同时保证不“浪费”内存。

即使equal/hashcode实现错误的相关问题也有可能导致内存问题。

**推荐阅读：**

*   [How Garbage Collection works](http://javabook.compuware.com/content/memory/how-garbage-collection-works.aspx)
*   [Difference between JVMs](http://javabook.compuware.com/content/memory/the-three-jvms.aspx)
*   [GC Tuning](http://javabook.compuware.com/content/memory/tuning-garbage-collection.aspx)
*   [High Memory Usage and the Root Cause](http://javabook.compuware.com/content/memory/problem-patterns/excessive-memory-use.aspx)
*   [Class Load Related Problems](http://javabook.compuware.com/content/memory/problem-patterns/class-loader-issues.aspx)
*   [Memory Monitoring in WebSphere Environments](http://apmblog.compuware.com/2011/05/10/field-report-application-performance-management-in-websphere-environments/)
*   [GC Bottlenecks in Heterogeneous Environments](http://apmblog.compuware.com/2009/04/08/performance-analysis-identify-gc-bottlenecks-in-distributed-heterogeneous-environments/)
*   [Leak Detection in Production Environments](https://apmcommunity.compuware.com/community/display/PUB/Field+Report+-+Memory+Leak+Detection+in+Production)
*   Top Memory Problems –  [Part I](http://apmblog.compuware.com/2011/04/20/the-top-java-memory-problems-part-1/)、 [Part II](http://apmblog.compuware.com/2011/12/15/the-top-java-memory-problems-part-2/)

原文链接：[Compuware Blog](http://apmblog.compuware.com/2013/04/10/top-8-application-performance-landmines/)