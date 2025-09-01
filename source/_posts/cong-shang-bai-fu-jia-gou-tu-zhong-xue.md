---
title: 从上百幅架构图中学大型网站建设经验（上）
id: 660
date: 2024-10-31 22:01:45
author: daichangya
excerpt: 近段时间以来，通过接触有关海量数据处理和搜索引擎的诸多技术，常常见识到不少精妙绝伦的架构图。除了每每感叹于每幅图表面上的绘制的精细之外，更为架构图背后所隐藏的设计思想所叹服。个人这两天一直在搜集各大型网站的架构设计图，一为了一饱眼福，领略各类大型网站架构设计的精彩之外，二来也可供闲时反复琢磨体会，何乐而不为呢?特此，总结整理了诸如国外wikipedia，Facebook，Yahoo！，
permalink: /archives/cong-shang-bai-fu-jia-gou-tu-zhong-xue/
categories:
- 系统架构
---

> > > ###  从上百幅架构图中学大型网站建设经验（上）

### 引言

    近段时间以来，通过接触有关海量数据处理和搜索引擎的诸多技术，常常见识到不少精妙绝伦的架构图。除了每每感叹于每幅图表面上的绘制的精细之外，更为架构图背后所隐藏的设计思想所叹服。个人这两天一直在搜集各大型网站的架构设计图，一为了一饱眼福，领略各类大型网站架构设计的精彩之外，二来也可供闲时反复琢磨体会，何乐而不为呢?特此，总结整理了诸如国外**wikipedia，Facebook，Yahoo！，YouTube，MySpace，Twitter**，国内如**优酷网**等大型网站的技术架构（本文重点分析优酷网的技术架构），以飨读者。

    本文着重凸显每一幅图的精彩之处与其背后含义，而图的说明性文字则从简从略。ok，好好享受此番架构盛宴吧。当然，若有任何建议或问题，欢迎不吝指正。谢谢。

*   ### 1、WikiPedia 技术架构
    

> ![](http://hi.csdn.net/attachment/201110/1/0_1317461287Mxff.gif)
> 
>                                              WikiPedia 技术架构图Copy @Mark Bergsma

1.  来自wikipedia的数据：峰值每秒钟3万个 HTTP 请求 每秒钟 3G**bit** 流量, 近乎**375MB** 350 台 PC 服务器。
    
2.  GeoDNSA ：40-line patch for BIND to add geographical filters support to the existent views in BIND", 把用户带到最近的服务器。GeoDNS 在 WikiPedia 架构中担当重任当然是由 WikiPedia 的内容性质决定的--面向各个国家，各个地域。
    
3.  负载均衡：LVS，请看下图：
    

> ![](http://hi.csdn.net/attachment/201110/1/0_1317463441CuoV.gif)。

*   ### 2、Facebook 架构
    

> ![](http://hi.csdn.net/attachment/201110/1/0_13174616592X8w.gif)
> 
>  Facebook 搜索功能的架构示意图

    细心的读者一定能发现，上副架构图之前出现在此文之中：从几幅架构图中偷得半点海里数据处理经验。本文与前文最大的不同是，前文只有几幅，此文系列将有上百幅架构图，任您尽情观赏。

*   ### 3、Yahoo! Mail 架构
    

> ![](http://hi.csdn.net/attachment/201110/1/0_1317462333Jwy2.gif)
> 
>                                                Yahoo! Mail 架构

    Yahoo! Mail 架构部署了 Oracle RAC，用来存储 Mail 服务相关的 Meta 数据。

*   ### 4、twitter技术架构
    

> ![](http://hi.csdn.net/attachment/201110/1/0_1317462911fw7p.gif)
> 
>                                                      twitter的整体架构设计图

    twitter平台大致由twitter.com、手机以及第三方应用构成，如下图所示（其中流量主要以手机和第三方为主要来源）：

> ![](http://hi.csdn.net/attachment/201110/1/0_1317462967FrOt.gif)

    缓存在大型web项目中起到了举足轻重的作用，毕竟数据越靠近CPU存取速度越快。下图是twitter的缓存架构图：

![](http://hi.csdn.net/attachment/201110/1/0_1317463185teed.gif)

    关于缓存系统，还可以看看下幅图：

> ![](http://hi.csdn.net/attachment/201110/1/0_1317463547G26a.gif)

*   ### 5、Google App Engine技术架构
    

> ![](http://hi.csdn.net/attachment/201110/1/0_1317463945r6EB.gif)
> 
>                                             GAE的架构图

    简单而言，上述GAE的架构分为如图所示的三个部分：前端，Datastore和服务群。

1.  前端包括4个模块：Front End，Static Files，App Server，App Master。
    
2.  Datastore是基于BigTable技术的分布式数据库，虽然其也可以被理解成为一个服务，但是由于其是整个App Engine唯一存储持久化数据的地方，所以其是App Engine中一个非常核心的模块。其具体细节将在下篇和大家讨论。
    
3.  整个服务群包括很多服务供App Server调用，比如Memcache，图形，用户，URL抓取和任务队列等。
    

*   ### 6、Amazon技术架构
    

> ![](http://hi.csdn.net/attachment/201110/1/0_1317464553j28E.gif)
> 
>                                     Amazon的Dynamo Key-Value存储架构图

    可能有读者并不熟悉Amazon，它现在已经是全球商品品种最多的网上零售商和全球第2大互联网公司。而之前它仅仅是一个小小的网上书店。ok，下面，咱们来见识下它的架构。

    Dynamo是亚马逊的key-value模式的存储平台，可用性和扩展性都很好，性能也不错：读写访问中99.9%的响应时间都在300ms内。按分布式系统常用的哈希算法切分数据，分放在不同的node上。Read操作时，也是根据key的哈希值寻找对应的node。Dynamo使用了 Consistent Hashing算法，node对应的不再是一个确定的hash值，而是一个hash值范围，key的hash值落在这个范围内，则顺时针沿ring找，碰到的第一个node即为所需。

    Dynamo对Consistent Hashing算法的改进在于：它放在环上作为一个node的是一组机器（而不是memcached把一台机器作为node），这一组机器是通过同步机制保证数据一致的。

    下图是分布式存储系统的示意图，读者可观摩之：

> ![](http://hi.csdn.net/attachment/201110/1/0_1317464717tf8F.gif)

    Amazon的云架构图如下：

> ![](http://hi.csdn.net/attachment/201110/1/0_1317464976Za2W.gif)
> 
>                                            Amazon的云架构图

*   ### 7、优酷网的技术架构
    

    从一开始，优酷网就自建了一套CMS来解决前端的页面显示，各个模块之间分离得比较恰当，前端可扩展性很好，UI的分离，让开发与维护变得十分简单和灵活，下图是优酷前端的模块调用关系：

![](http://hi.csdn.net/attachment/201110/1/0_1317465660DmeX.gif)

    这样，就根据module、method及params来确定调用相对独立的模块，显得非常简洁。下图是优酷的前端局部架构图：

![](http://hi.csdn.net/attachment/201110/1/0_1317465622c0Ca.gif)

    优酷的数据库架构也是经历了许多波折，从一开始的单台MySQL服务器（Just Running）到简单的MySQL主从复制、SSD优化、垂直分库、水平sharding分库。

1.  **简单的MySQL主从复制。**  
    MySQL的主从复制解决了数据库的读写分离，并很好的提升了读的性能，其原来图如下：![](http://hi.csdn.net/attachment/201110/1/0_1317465817ZOzT.gif)
    
    其主从复制的过程如下图所示：![](http://hi.csdn.net/attachment/201110/1/0_1317465848lGG2.gif)
    
    但是，主从复制也带来其他一系列性能瓶颈问题：
    
    1.  写入无法扩展
    2.  写入无法缓存
    3.  复制延时
    4.  锁表率上升
    5.  表变大，缓存率下降
    
    那问题产生总得解决的，这就产生下面的优化方案。
    
2.   **MySQL垂直分区**
    
        如果把业务切割得足够独立，那把不同业务的数据放到不同的数据库服务器将是一个不错的方案，而且万一其中一个业务崩溃了也不会影响其他业务的正常进行，并且也起到了负载分流的作用，大大提升了数据库的吞吐能力。经过垂直分区后的数据库架构图如下：![](http://hi.csdn.net/attachment/201110/1/0_1317465908N0yV.gif)
    
        然而，尽管业务之间已经足够独立了，但是有些业务之间或多或少总会有点联系，如用户，基本上都会和每个业务相关联，况且这种分区方式，也不能解决单张表数据量暴涨的问题，因此为何不试试水平sharding呢？
    
3.   **MySQL水平分片（Sharding）**
    
        这是一个非常好的思路，将用户按一定规则（按id哈希）分组，并把该组用户的数据存储到一个数据库分片中，即一个sharding，这样随着用户数量的增加，只要简单地配置一台服务器即可，原理图如下：![](http://hi.csdn.net/attachment/201110/1/0_1317465946Eig2.gif)
    
      如何来确定某个用户所在的shard呢，可以建一张用户和shard对应的数据表，每次请求先从这张表找用户的shard id，再从对应shard中查询相关数据，如下图所示：![](http://hi.csdn.net/attachment/201110/1/0_1317465980MMM8.gif)    但是，优酷是如何解决跨shard的查询呢，这个是个难点，据介绍优酷是尽量不跨shard查询，实在不行通过多维分片索引、分布式搜索引擎，下策是分布式数据库查询（这个非常麻烦而且耗性能）。
    
4.   **缓存策略**
    
    貌似大的系统都对“缓存”情有独钟，从http缓存到memcached内存数据缓存，但优酷表示没有用内存缓存，理由如下：
    
    1.  避免内存拷贝，避免内存锁
    2.  如接到老大哥通知要把某个视频撤下来，如果在缓存里是比较麻烦的
    
    而且Squid 的 write() 用户进程空间有消耗，Lighttpd 1.5 的 AIO(异步I/O) 读取文件到用户内存导致效率也比较低下。
    
    但为何我们访问优酷会如此流畅，与土豆相比优酷的视频加载速度略胜一筹？这个要归功于优酷建立的比较完善的内容分发网络（CDN），它通过多种方式保证分布在全国各地的用户进行就近访问——用户点击视频请求后，优酷网将根据用户所处地区位置，将离用户最近、服务状况最好的视频服务器地址传送给用户，从而保证用户可以得到快速的视频体验。这就是CDN带来的优势，就近访问。
    

    附注：1、此段优酷网的技术架构整理于此处：[http://www.itivy.com/ivy/archive/2011/8/13/the-architecture-of-youku.html](http://www.itivy.com/ivy/archive/2011/8/13/the-architecture-of-youku.html)；2、同时推荐一个非常好的站点：[http://www.dbanotes.net/](http://www.dbanotes.net/)）。从上百幅架构图中学得半点大型网站建设经验（上），完。

### 后记

    此篇文章终于写完了，从昨日有整理此文的动机后，到今日上午找电脑上网而不得，再到此刻在网吧完成此文。着实也体味了一把什么叫做为技术狂热的感觉。大型网站架构是一个实战性很强的东西，而你我或许现在暂时还只是一个在外看热闹的门外汉而已。不过，没关系，小鱼小虾照样能畅游汪汪大洋，更何况日后亦能成长为大鱼大鲨。

    ok，欢迎关注从上百幅架构图中学得半点大型网站建设经验（下）。有任何问题或错误，欢迎不吝指正。谢谢大家。本文完。