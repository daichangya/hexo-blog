---
title: Linkedin网站技术架构简介
id: 377
date: 2024-10-31 22:01:43
author: daichangya
excerpt: 关于LinkedIn网站的架构技术的演讲可以看一下LinkedIn网站的基本情况：1. 2千2百万用户2. 每个月4百万独立用户访问3. 每天4千万Page
  View4. 每天2百万搜索流量5. 每天25万邀请发送6. 每天1百万的回答提交7. 每天2百万的Email消息
permalink: /archives/Linkedin-wang-zhan-ji-shu-jia-gou-jian/
categories:
- 系统架构
---

  
可以看一下LinkedIn网站的基本情况：  
  

1\. 2千2百万用户  
2\. 每个月4百万独立用户访问  
3\. 每天4千万Page View  
4\. 每天2百万搜索流量  
5\. 每天25万邀请发送  
6\. 每天1百万的回答提交  
7\. 每天2百万的Email消息发送  

  
**这是一个世界顶尖级别流量的网站了，看看LinkedIn的系统架构：**  
  

*   操作系统：Solaris (running on Sun x86 platform and Sparc)
*   应用服务器：Tomcat and Jetty as application servers
*   数据库：Oracle and MySQL as DBs
*   没有ORM，直接用JDBC No ORM (such as Hibernate); th** use straight JDBC
*   用ActiveMQ在发送JMS. (It"s partitioned by type of messages. Backed by MySQL.)
*   用lucene做搜索Lucene as a foundation for search
*   Spring做逻辑架构Spring as glue

  
**下面是随着流量增加，LinkedIn的架构演化：**  
  
2003~2005  
  

1 一个整体的web程序，  
2 一个核心数据库，  
3 在**Cloud**中缓存所有network图，Cloud是用来做缓存的独立server。  
4 用Lucene做搜索，也跑在Cloud中。  

  
2006年  
  

1 复制另外一个数据库，减少直接Load核心数据库，另外一个Server来管理非只读数据库的数据更新。  
2 把搜索从Cloud中移出来，单独一个Server跑搜索  
3 增加**Databus数据总线**来更新数据，这是通过分布式更新的核心组件，任何组件都需要Databus  

  
2008年  
  

1 Webapp不再任何事情都自己做，把业务逻辑分成很多部分，通过Server群来做。Webapp仍然提供用户界面给用户，但是，通过Server群来管理用户资料，小组等等。  
2 每个服务有自己的域数据库  
3 新的架构允许其他应用链接LinkedIn，比如增加的招聘和广告业务。  

  
  
The Cloud  
  

1 Cloud是整个架构最重要的部分，整个LinkedIn的网络图都缓存在Cloud里面  
2 Cloud大小：22M nodes, 120M edges  
3 需要12GB RAM  
4 在生产环境要跑40个实例  
5 从硬盘重建Cloud一个实例需要8个小时  
6 Cloud通过databus实时更新  
7 关闭时持久化到硬盘  
8 缓存通过C++实现，用JNI调用，LinkedIn选择C++而不是Java有两个原因：  

1）尽可能的减少RAM的使用  
2）垃圾收集暂停会杀死整个系统，LinkedIn用了最新的GC程序  

9 将所有东西放在缓存里面是一种限制，但是LinkedIn指出，分割业务图将更麻烦  
10 Sun提供了2TB的RAM  

  
Communication Architecture交流架构包括：  
  

Communication Service  
  
Communication Service是用来提供永久信息的，比如收件箱里面的消息和email  
  

1 整个系统通过JMS异步通讯  
2 客户端用JMS发送消息  
3 消息通过路径服务器来到达相应的邮箱或者直接放到email进程中  
4 消息发送：同时使用Pull主动寻求信息(如用户需要信息)和Push发送信息(如发email)  
5 使用Spring和LinkedIn专业Spring插件完成，使用HTTP-RPC  

  
Scaling Techniques  
  

1 通过功能来划分：发送，接受，文档等。  
2 通过类别来划分：用户信箱，访问者信箱等  
3 等级划分：用户ID等级，Email等级等  
4 所有的操作都是异步的。  

PPT分享：

1.  [LinkedIn Communication Architecture](http://www.slideshare.net/linkedin/linked-in-javaone-2008-tech-session-comm?type=presentation "LinkedIn Communication Architecture")
2.  [A Professional Network built with Java Technologies and Agile Practices](http://www.slideshare.net/linkedin/linkedins-communication-architecture?type=powerpoint "LinkedIn - A Professional Network built with Java Technologies and Agile Practices")

原文地址： http://www.liyingfei.com/read.php/9.htm 