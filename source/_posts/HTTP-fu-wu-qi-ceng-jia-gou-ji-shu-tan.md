---
title: HTTP服务七层架构技术探讨
id: 970
date: 2024-10-31 22:01:47
author: daichangya
excerpt: 1. 为什么分层？　　计算机领域的体系结构普遍采用了分层的方式。　　从整体结构来看：　　从最底层的硬件往高层依次有：　　操作系统 -> 驱动程序
  -> 运行库 -> 系统程序 -> 应用程序等等。　　从网络分层模型OSI
permalink: /archives/HTTP-fu-wu-qi-ceng-jia-gou-ji-shu-tan/
categories:
- 软件设计
---


**前言：太久没有做过技术分享了，这里把曾经老的新浪论坛里面使用过的架构技术做了改进和整理，最后总结了这么一篇，欢迎拍砖。**

**1.为什么分层？**

计算机领域的体系结构普遍采用了分层的方式。

   从整体结构来看： 

   从最底层的硬件往高层依次有操作系统->驱动程序->运行库->系统程序->应用程序等等。

   从网络分层模型OSI来讲,由上至下为：

   应用层->表示层-\> 会话层->传输层->网络层->数据链路层->物理层       

   当然实际应用的TCP/IP协议的分层就没OSI标准这么复杂。   

  

   从C语言文件编写到生成可执行文件的过程来看： 

   预处理(展开后的C语言代码)->编译成汇编语言(特定CPU体系结构的汇编语言源文件)->汇编器生成目标文件（CPU可执行的二进制指令机器码）->链接器连接目标文件生成可执行文件（操作系统可以加载执行的二进制文件）

   这不算是软件的分层结构，但是可以理解为一种通过分层来简化复杂问题的思想。那么PHP语言可以认为是建立在C语言之上的层----其解释器Zend引擎是用C语言实现。毕竟用PHP这样的脚本语言编写动态网页要比用C语言方便得多。

   当然还有我们最熟悉的MVC分层技术了，后面会做详细介绍。

   那么分层的好处想必大家都已经比较熟悉，这是一种 “分而治之  大而化小”  的思想。说到分层就不得不提模块了，其实分层和模块是从两种维度来进行“分而治之”的方式。模块是从横向维度来将一个整体分割成若干个独立的部分，每个部分行使独立自己的职责，当然它们之间也可能有依赖关系，这通过其对外提供的服务来实现。如果将整个系统比做中国版图的话，那么模块方式将中国分为省，自治区等。 分层则是从纵向纬度将一个整体从高至低划分为若干个独立的层，一个完整的服务由底层至上层，层层传递最终产出。分层和模块可以同时运用，例如中国用模块方式分为省之后，然后每个省的行政机构利用分层方式来行使职责,从低到高有户，村，乡，区，市，省等等，每一层都向上一层汇报。 分层和模块会提高系统复杂度并影响效率（户不能直接向省汇报，而需要一级一级向上汇报），但是这样有利用系统的扩展和维护，每一层只需要关注自己提供的服务接口以及它下一层所提供的服务接口，试想一下如果省需要接受来自市，区，乡，村等所有下级层的汇报，那些省干部会很头疼的。

  

**2.HTTP服务传统的三层架构MVC**

  HTTP服务中最经典的分层架构非MVC莫属了， 几乎任何一个PHP开发框架都是支持MVC分层模式，此模式历史也比较悠久，是在上个世纪八十年代为编程语言Smalltalk设计的软件模式，至今已经被广泛引用。

 这里引用了百度百科中的图片：

![](http://hi.csdn.net/attachment/201203/8/0_13311825358kGQ.gif) ![](http://hi.csdn.net/attachment/201203/8/0_1331182554WM6v.gif)  

那么关于MVC的优点我不做介绍，搜索引擎中能找到大量相关资料。

本文的标题是HTTP服务七层架构技术探讨，比MVC多出了四层，这样复杂的分层是否有必要呢？

关于这个问题仁者见仁智者见智，本人认为MVC分层粒度不够精细，当然你也可以继续坚持传统的三层，那么后文你也没必要看下去了。

那么为什么MVC分层不够精细呢，在我曾经使用开源框架的MVC模式的经验中发现，V和C层功能职责一般都很清晰稳定，但是M层却常常显得臃肿笨拙。

C层主要是负责整体流程控制，一般规范的架构中，流程都可以用一张或几张流程图画出，那么表明流程一般都是固定的。

V层主要是负责页面呈现，可能使用smarty模板引擎，也可能是自带的模板引擎，显示的页面可能是HTML，XML或则JSON，这些种类再多也都是可以度量的，所以M层也可以说是固定的。

而M层却关系到系统的业务逻辑，随着系统不断迭代更新，M层中的内容也会不断演变，而这一层中也有很多复杂的处理，如文件读取，数据库查询，缓存策略，逻辑运算，数据加工，数据打包等等。 

所以MVC三层模型中，M层是还能再做细分的，当M层有一个更精细合理的分层方式之后，我们的业务逻辑演变过程会更加的得心应手。

  

**3.七层架构**

  由上面的介绍，那么我们对MVC中的M层再进行分层规划，我这里给出的是一种对M层分五层的方式，读者如果觉得五层太多或则太少那么可以参考这个再进行规划。

原来的M层被分为：

A层： Application      应用层

B层：Business         业务层

C层：Component     组件层

D层：Datadriver        数据驱动层

S层： Systemdriver  系统驱动层

那么整个七层架构则为:

1.Controller

2\. View 

3\. Application 

4.Business

5.Component

6.Datadriver 

7.Systemdriver 

结构图还是参考经典MVC，将其中M层换成新的五层即可。

  

现在依次介绍这几个新的层：

1.Application

   应用层在最上面，其针对实际中的单个页面或则单个接口。Controller通过HTTP请求地址中的参数找到对应的Application，然后执行中指定的公共方法，比如main()，然后应用就开始启动。应用层的职责包括接受HTTP参数（一般是间接接受，比如从request对象中获取），调用Business层的特定业务，保存业务执行结果，这些结果最终会由View显示出来，当然是通过Controller协调。应用层是M层分解成五层之后最高的层，Controller会与此层直接通信。

2.Business

  业务层在应用层之下，通常一个应用实例对应一个业务实例，而一个业务有可能为多个应用服务，业务是一个执行流，它通过执行一系列的操作来完成应用的需求。这些操作来自下层的组件层Component,可能一个业务需要一个或则多个组件来完成一个完整的需求。因为一个业务实例通常只对应一个功能，所以只有一个固定的方法会被上层的应用调用，比如flow()。业务层的职责是帮应用层执行业务流并且有必要的时候返回数据给应用层，它会调用下层Component的方法。

3.Component

  从组件层开始和上面两层有一个本质的区别，组件层开始有了类库的概念。 前面两层的实例通常只暴露一个特殊约定的公共的方法让上层调用，从这一层开始一个实例会提供多个方法给上层。组件层通常和系统中一个角色对应，例如在博客系统中，博文是一个角色，用户是一个角色，那么就会有博文组件BlogComponent，用户组件UserComponent，每个角色都有对应的操作，例如博文和用户都可以添加删除修改。

  需要注意组件层中不应该有任何数据读取的操作，数据读取是下层数据驱动层来做的。如果组件层从下层获取了数据，那么它的一个职责就是对数据进行加工。例如BlogComponent有一个方法是获取一个博文getBlog($id)，那么getBlog()方法中，从数据驱动层中取得了对应id的博文数据之后，需要对博文数据进行一定的处理，比如将博文中的HTML特殊标签过滤等等。组件层不关心数据的读取方式，但是会关心数据的结果，比如数据不存在或则数据已经过期。

4.Datadriver

  数据驱动层的职责是为组件层提供源数据，此层关心数据的存取介质，存取方式等等。数据可能被存储在DB，MC，Filesystem或则远程的HTTP服务器上。数据驱动层不关心数据的内容，只关心数据读取的操作结果，例如假设数据存在DB中，但是数据驱动层在执行数据库查询的时候出错了，那么需要在此层处理。 假设数据存储在远程的HTTP服务器上，那么数据驱动层需要关心HTTP返回码是否为正确的200系列或则错误的400，500系列，哪怕HTTP请求返回了错误的数据实体，但是返回码为200，那么数据驱动层也不关心，这种情况需要上层组件层来处理。

5.Systemdriver

  系统驱动层是系统环境提供的数据访问实例，例如数据库服务的Systemdriver可能是一个db handler或则，HTTP服务的Systemdriver可能是一个http handler，文件存储系统驱动层可能是一个file handler, 系统驱动层相对简单，这层可以和数据驱动层进行合并，其职责也较少。仅仅只是执行数据驱动层的数据访问指令。

  

通常情况下这五个层中，上层的实例数量比下层的实例数量要多， 整体类似一个倒置的梯形：

  

![](http://hi.csdn.net/attachment/201203/8/0_1331188523HMzA.gif)  

  

在上图中一共有6个Application，5个Business，4个Component，3个Datadriver，2个Systemdriver

每个Application都由一个Business为其服务

每个Business都服务一个或则多个Application（B5同时服务A5 A6），都有一个或则多个Componet为其服务         

每个Component为一个或则多个Business服务，都有一个或则多个Datadriver为其服务

每个Datadriver为一个或则多个Component服务，都有一个或则多个Systemdriver为其服务  

每个Systemdriver为一个或则多个Datadriver服务。  

  

**4.七层架构运用**

现在运用这样的架构来设计一个简单的博客系统,服务端用PHP语言实现。当然，架构是思想，不区分语言。

整个系统包含以下功能

1.发布博文 2.修改博文 3.删除博文 4.评论博文 5.修改用户信息 

要求每个功能都记录操作日志。

  

设计的数据存储包括

1.博文数据表 2.用户数据表  3.评论数据表   4.  日志（存文件系统）

在表结构设计的时候我们加入了一些冗余字段信息，例如在博文表中有评论数量字段comment_nums, 博文每被评论一次其值加1，每删除一个评论其值减1

用户数据表中我们添加了用户发布的博文数量字段blog_nums,用户每发布一篇博文其值加1，每删除一篇博文其值减1

  

下面设计分层：

应用层： 一共有5个应用

1.PostBlogApplication        发布博文

2.UpdateBlogApplication   修改博文

3.DeleteBlogApplication     删除博文

4.CommentBlogApplication  评论博文

5.UpdateUserApplication  修改用户信息

  

业务层：这5个应用分别有5个业务对其服务

1.PostBlogBusiness          博文发布业务

2.UpdateBlogBusiness     博文修改业务

3.DeleteBlogBusiness       博文删除业务

4.CommentBlogBusiness 博文评论业务

5.UpdateUserBusiness     用户修改业务

  

组件层：系统一共有4个角色对应4个组件

1.BlogComponent         博文组件

    提供方法包括

   1>postBlog() 发布博文

   2>deleteBlog()删除博文

   3>updateBlog()修改博文

   4>getBlog()获取博文内容

2.CommentComponent   评论组件

    提供方法包括

     1>postComment()  发布评论

     2>deleteComment() 删除评论

3.UserComponent         用户组件

     提供方法包括

     1>updateUser() 修改用户信息

4.LogComponent           日志组件

     提供方法包括

     1>logMsg() 记录日志信息

  

数据驱动层:和4个组件对应

1.BlogDatadriver        DB类型  提供blog的select insert delete update

2.CommentDatadriver  DB类型  提供comment的select insert delete update

3.UserDatadriver        DB类型  提供user的select insert delete update

4.LogDatadriver           FS类型  提供file的read write

  

系统驱动层: DB类型和FS类型

1.MySqlSystemdriver  DB的handler

2.FileSystemdriver      FS的handler

  

  

现在以发布博文操作来介绍流程。假设接口地址为: http://www.xxxxx.com/postBlog：

1.Controller通过重写规则发现其对应的Application为PostBlogApplication，于是PostBlogApplication被实例化，并且其中的特殊方法main()会被自动调用。

2.postBlogApplication需要PostBlogBusiness业务来完成博文发布操作，PostBlogBusiness被实例化，并且其中的特殊方法flow()会被调用。

3.根据需求，发布博文的时候需要在博文表中插入一条博文，然后修改用户信息中的博文数量字段。那么postBlogBusiness业务流就包括两个操作，这两个操作分别由BlogComponent中的postBlog()方法和UserComponent 中的updateUser()方法来实现，其中前者往博文表中插入博文信息，后者将用户信息中的博文数量字段加1.由于系统要求任何操作都需要记录日志，因此还有第三个操作就是记录日志，通过BlogComponent的logMsg()方法实现。那么PostBlogBusiness业务流一共包括了三个操作，分别由三个组件来完成。

4.下面就需要分别考虑上面三个组件的下层调用了

   其中BlogComponet的postBlog()调用BlogDatadriver的insert相关方法来插入博文数据，BlogDatadriver是DB类型，因此通过MySqlSystemdriver 来实现。

            UserComponent的updateUser()调用UserDatadriver的update相关方法来实现博文数量更新，UserDatadriver也是DB类型，因此也通过MySqlSystemdriver 来实现。

            LogComponent的logMsg()调用LogDatadriver的write相关方法，LogDatadriver是FS类型，因此通过FileSystemdriver 来实现。

5\. 三个组件的操作都执行成功后，PostBlogBusiness告诉postBlogApplication博文发布成功，然后postBlogApplication通过Controller来调用View相关的方法显示执行结果。

  

其他几个操作流程读者可以举一反三，这里不再多介绍了。

那么现在我们通过几个系统功能的演变用例来看看这个分层带来的益处。

用例1：为了方便对日志的管理，现在希望能够将日志存储在DB中而不是FS中。

解决方法：这是对数据存储的改造，我们知道应该从数据驱动层入手。日志功能是由日志组件LogComponent实现的， 其中LogComponet的了logMsg()方法调用LogDatadriver 来存日志。我们将LogDatadriver由FS类型改造成DB类型，接口方法保持不变，这样很快就完成了改造。

  

用例2：新增需求-用户A可以将一篇博文转移给另外一个用户B。

解决方法：

    步骤1.首先这个新需求对应了一个新的应用,于是我们新增了一个SendBlogApplication,

    步骤2.需要有一个业务完成操作，新增业务为SendBlogBusiness

    步骤3.考虑转移一篇博文涉及到的操作 1.将博文表中对应的用户ID字段由A的ID切换到B的ID  2.A用户的博文数量减1   3.B用户的博文数量加1 

               这三个操作需要两个组件来完成，这两个组件我们系统中已经有了，BlogComponent的updateBlog ()完成操作1，UserComponent的updateUser()完成操作2，3

从用例2可以看出，当新增了这么一个需求的时候，我们在应用层和业务层添加了实例，组件层以下都不变，这是因为现在的组件层已经能够满足新的业务的需求，当我们现有组件无法满足新的一业务需求的时候，我们则需要对组件层做修改。    

  

通过这两个简单的用例我们发现我们对系统的修改要么可以很明确的确定在哪些层，要么就是从上层组件往下层进行，操作起来很方便。

  

**5.小结**

这种纵向的分层和横向的模块结合起来，能让整个系统的结构清晰流畅，在本人设计的一款框架里面，原生的支持这样的分层架构和模块，使用者只需要按照同一个模式简单的操作，层之间的接口和协议已经由框架本身约定好，框架还不够完善，自己内部用用可以，暂时不发布了。
