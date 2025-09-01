---
title: Tomcat处理HTTP请求源码分析
id: 746
date: 2024-10-31 22:01:45
author: daichangya
excerpt: 很多开源应用服务器都是集成tomcat作为web container的，而且对于tomcat的servlet container这部分代码很少改动。这样，这些应用服务器的性能基本上就取决于Tomcat处理HTTP请求的connector模块的性能。本文首先从应用层次分析了tomcat所有的connector种类及用法，接着从架构上分析了connector模块在整个tomcat中所处的位置，最后对c
permalink: /archives/Tomcat-chu-li-HTTP-qing-qiu-yuan-ma-fen/
categories:
- Tomcat
---



很多开源应用服务器都是集成 tomcat 作为 web container 的，而且对于 tomcat 的 servlet container 这部分代码很少改动。这样，这些应用服务器的性能基本上就取决于 Tomcat 处理 HTTP 请求的 connector 模块的性能。本文首先从应用层次分析了 tomcat 所有的 connector 种类及用法，接着从架构上分析了 connector 模块在整个 tomcat 中所处的位置，最后对 connector 做了详细的源代码分析。并且我们以 Http11NioProtocol 为例详细说明了 tomcat 是如何通过实现 ProtocolHandler 接口而构建 connector 的。

通过本文的学习，应该可以轻松做到将 tomcat 做为 web container 集成到第三方系统，并且自定义任何你想要的高性能的 HTTP 连接器。

## 1 Connector 介绍

### 1.1 Connector 的种类

Tomcat 源码中与 connector 相关的类位于 org.apache.coyote 包中，Connector 分为以下几类：

*   Http Connector, 基于 HTTP 协议，负责建立 HTTP 连接。它又分为 BIO Http Connector 与 NIO Http Connector 两种，后者提供非阻塞 IO 与长连接 Comet 支持。
*   AJP Connector, 基于 AJP 协议，AJP 是专门设计用来为 tomcat 与 http 服务器之间通信专门定制的协议，能提供较高的通信速度和效率。如与 Apache 服务器集成时，采用这个协议。
*   APR HTTP Connector, 用 C 实现，通过 JNI 调用的。主要提升对静态资源（如 HTML、图片、CSS、JS 等）的访问性能。现在这个库已独立出来可用在任何项目中。Tomcat 在配置 APR 之后性能非常强劲。

### 1.2 Connector 的配置

对 Connector 的配置位于 conf/server.xml 文件中。

#### 1.2.1 BIO HTTP/1.1 Connector 配置

一个典型的配置如下：


	<Connector port=”8080” protocol=”**HTTP/1.1**” maxThreads=”150” 
	connectionTimeout=”20000” redirectPort=”8443”

其它一些重要属性如下：

*   acceptCount : 接受连接 request 的最大连接数目，默认值是 10
*   address : 绑定 IP 地址，如果不绑定，默认将绑定任何 IP 地址
*   allowTrace : 如果是 true, 将允许 TRACE HTTP 方法
*   compressibleMimeTypes : 各个 mimeType, 以逗号分隔，如 text/html,text/xml
*   compression : 如果带宽有限的话，可以用 GZIP 压缩
*   connectionTimeout : 超时时间，默认为 60000ms (60s)
*   maxKeepAliveRequest : 默认值是 100
*   maxThreads : 处理请求的 Connector 的线程数目，默认值为 200

如果是 SSL 配置，如下：


	<Connector port="8181" protocol="HTTP/1.1" SSLEnabled="true" 
		maxThreads="150" scheme="https" secure="true" 
		clientAuth="false" sslProtocol = "TLS" 
		address="0.0.0.0" 
		**keystoreFile="E:/java/jonas-full-5.1.0-RC3/conf/keystore.jks"** 
		**keystorePass="changeit"** /\> 

其中，keystoreFile 为证书位置，keystorePass 为证书密码

#### 1.2.2 NIO HTTP/1.1 Connector 配置


	<Connector port=”8080” protocol=”**org.apache.coyote.http11.Http11NioProtocol**” 
		maxThreads=”150” connectionTimeout=”20000” redirectPort=”8443” 

#### 1.2.3 Native APR Connector 配置

1.  ARP 是用 C/C++ 写的，对静态资源（HTML，图片等）进行了优化。所以要下载本地库
    
    tcnative-1.dll 与 openssl.exe，将其放在 %tomcat%\\bin 目录下。
    
    下载地址是： [http://tomcat.heanet.ie/native/1.1.10/binaries/win32/](http://tomcat.heanet.ie/native/1.1.10/binaries/win32/)
    
2.  在 server.xml 中要配置一个 Listener, 如下图。这个配置 tomcat 是默认配好的。
    
    
    <!--APR library loader. Documentation at /docs/apr.html --> 
    <Listener className="org.apache.catalina.core.AprLifecycleListener" SSLEngine="on" /> 
    
3.  配置使用 APR connector
    
    
    <Connector port=”8080” protocol=”**org.apache.coyote.http11.Http11AprProtocol**” 
    
    maxThreads=”150” connectionTimeout=”20000” redirectPort=”8443”
    
4.  如果配置成功，启动 tomcat, 会看到如下信息：
    
    
    org.apache.coyote.http11.Http11AprProtocol init 
    

## 2 Connector 在 Tomcat 中所处的位置

### 2.1 Tomcat 架构

![](https://static001.infoq.cn/resource/image/59/05/59a324e70eab7cf85ca1ea7173a6e005.jpg)

**图 2-1 Tomcat 架构**

*   Server(服务器) 是 Tomcat 构成的顶级构成元素，所有一切均包含在 Server 中，Server 的实现类 StandardServer 可以包含一个到多个 Services;
*   次顶级元素 Service 的实现类为 StandardService 调用了容器 (Container) 接口，其实是调用了 Servlet Engine(引擎)，而且 StandardService 类中也指明了该 Service 归属的 Server；
*   接下来次级的构成元素就是容器 (Container)，主机 (Host)、上下文 (Context) 和引擎 (Engine) 均继承自 Container 接口，所以它们都是容器。但是，它们是有父子关系的，在主机 (Host)、上下文 (Context) 和引擎 (Engine) 这三类容器中，引擎是顶级容器，直接包含是主机容器，而主机容器又包含上下文容器，所以引擎、主机和上下文从大小上来说又构成父子关系，虽然它们都继承自 Container 接口。
*   连接器 (Connector) 将 Service 和 Container 连接起来，首先它需要注册到一个 Service，它的作用就是把来自客户端的请求转发到 Container(容器)，这就是它为什么称作连接器的原因。

故我们从功能的角度将 Tomcat 源代码分成 5 个子模块，它们分别是：

1.  Jsper 子模块：这个子模块负责 jsp 页面的解析、jsp 属性的验证，同时也负责将 jsp 页面动态转换为 java 代码并编译成 class 文件。在 Tomcat 源代码中，凡是属于 org.apache.jasper 包及其子包中的源代码都属于这个子模块；
2.  Servlet 和 Jsp 规范的实现模块：这个子模块的源代码属于 javax.servlet 包及其子包，如我们非常熟悉的 javax.servlet.Servlet 接口、javax.servet.http.HttpServlet 类及 javax.servlet.jsp.HttpJspPage 就位于这个子模块中；
3.  Catalina 子模块：这个子模块包含了所有以 org.apache.catalina 开头的 java 源代码。该子模块的任务是规范了 Tomcat 的总体架构，定义了 Server、Service、Host、Connector、Context、Session 及 Cluster 等关键组件及这些组件的实现，这个子模块大量运用了 Composite 设计模式。同时也规范了 Catalina 的启动及停止等事件的执行流程。从代码阅读的角度看，这个子模块应该是我们阅读和学习的重点。
4.  Connectors 子模块：如果说上面三个子模块实现了 Tomcat 应用服务器的话，那么这个子模块就是 Web 服务器的实现。所谓连接器 (Connector) 就是一个连接客户和应用服务器的桥梁，它接收用户的请求，并把用户请求包装成标准的 Http 请求 (包含协议名称，请求头 Head，请求方法是 Get 还是 Post 等等)。同时，这个子模块还按照标准的 Http 协议，负责给客户端发送响应页面，比如在请求页面未发现时，connector 就会给客户端浏览器发送标准的 Http 404 错误响应页面。
5.  Resource 子模块：这个子模块包含一些资源文件，如 Server.xml 及 Web.xml 配置文件。严格说来，这个子模块不包含 java 源代码，但是它还是 Tomcat 编译运行所必需的。

### 2.2 Tomcat 运行流程

![](https://static001.infoq.cn/resource/image/f1/d4/f1aa8a781479109792f43efbc6793fd4.jpg)

**图 2-2 tomcat 运行流程**

假设来自客户的请求为： [http://localhost:8080/test/index.jsp](http://localhost:8080/test/index.jsp)

1.  请求被发送到本机端口 8080，被在那里侦听的 Coyote HTTP/1.1 Connector 获得
2.  Connector 把该请求交给它所在的 Service 的 Engine 来处理，并等待 Engine 的回应
3.  Engine 获得请求 localhost:8080/test/index.jsp，匹配它所有虚拟主机 Host
4.  Engine 匹配到名为 localhost 的 Host（即使匹配不到也把请求交给该 Host 处理，因为该 Host 被定义为该 Engine 的默认主机）
5.  localhost Host 获得请求 /test/index.jsp，匹配它所拥有的所有 Context
6.  Host 匹配到路径为 /test 的 Context（如果匹配不到就把该请求交给路径名为""的 Context 去处理）
7.  path="/test"的 Context 获得请求 /index.jsp，在它的 mapping table 中寻找对应的 servlet
8.  Context 匹配到 URL PATTERN 为 *.jsp 的 servlet，对应于 JspServlet 类
9.  构造 HttpServletRequest 对象和 HttpServletResponse 对象，作为参数调用 JspServlet 的 doGet 或 doPost 方法
10.  Context 把执行完了之后的 HttpServletResponse 对象返回给 Host
11.  Host 把 HttpServletResponse 对象返回给 Engine
12.  Engine 把 HttpServletResponse 对象返回给 Connector
13.  Connector 把 HttpServletResponse 对象返回给客户 browser

## 3 Connector 源码分析

### 3.1 Tomcat 的启动分析与集成设想

我们知道，启动 tomcat 有两种方式：

*   双击 bin/startup.bat
*   运行 bin/catalina.bat run

它们对应于 Bootstrap 与 Catalina 两个类，我们现在只关心 Catalina 这个类，这个类使用 Apache Digester 解析 conf/server.xml 文件生成 tomcat 组件，然后再调用 Embedded 类的 start 方法启动 tomcat。

所以，集成 Tomcat 的方式就有以下两种了：

*   沿用 tomcat 自身的 server.xml
*   自己定义一个 xml 格式来配置 tocmat 的各参数，自己再写解析这段 xml，然后使用 tomcat 提供的 API 根据这些 xml 来生成 Tomcat 组件，最后调用 Embedded 类的 start 方法启动 tomcat

个人觉得第一种方式要优越，给开发者比较好的用户体验，如果使用这种，直接模仿 Catalina 类的方法即可实现集成。

目前，JOnAS 就使用了这种集成方式，JBoss、GlassFish 使用的第二种自定义 XML 的方式。

### 3.2 Connector 类图与顺序图

![](https://static001.infoq.cn/resource/image/96/6e/96a9a2835ef2e2ad0d7ed0bda9643b6e.jpg)

**图 3-1 Connector 相关类图**

![](https://static001.infoq.cn/resource/image/e0/46/e0ae1bbf830029d7987ec352097aa746.jpg)

**图 3-2 Connector 工作流程顺序图**

从上面二图中我们可以得到如下信息：

1.  Tomcat 中有四种容器 (Context、Engine、Host、Wrapper)，前三者常见，第四个不常见但它也是实现了 Container 接口的容器
2.  如果要**自定义一个 Connector 的话，只需要实现 ProtocolHander 接口**, 该接口定义如下：

![](https://static001.infoq.cn/resource/image/d6/41/d68e087d447f8aa1430fb43d80733b41.jpg)

**图 3-3 自定义 connector 时需实现的 ProtocolHandler 接口**

Tomcat 以 HTTP（包括 BIO 与 NIO）、AJP、APR、内存四种协议实现了该接口（它们分别是：AjpAprProtocol、AjpProtocol、Http11AprProtocol、Http11NioProtocol、Http11Protocal、JkCoyoteHandler、MemoryProtocolHandler），要使用哪种 Connector 就在 conf/server.xml 中配置，在 Connector 的构造函数中会通过反射实例化所配置的实现类：


	<Connector port="8181" 
	   protocol="org.apache.coyote.http11.Http11AprProtocol " /> 

### 3.3 Connector 的工作流程

下面我们以 Http11AprProtocol 为例说明 Connector 的工作流程。

1.  它将工作委托给 NioEndpoint 类。在 NioEndpoint 类的 init 方法中构建一个 SocketServer(当然，不同的实现类会有一些微小的变化，例如如果是 NIO，它构建的就是 SocketServerChannel)
2.  在 NioEndpoint.Acceptor 类中会接收一个客户端新的连接请求，如下图：
    
    ![](https://static001.infoq.cn/resource/image/60/c2/60d40698ebc98c35b716482674940dc2.jpg)
    
3.  在 NioEndpoint 类中，有一个内部接口 Handle，该接口定义如下：
    
    ![](https://static001.infoq.cn/resource/image/f1/86/f146a6241cd6ba3891202b856f3c8186.jpg)
    
4.  在 Http11NioProtocol 类中实现了 Handle 这个内部接口，并调用 Http11NioProcessor 类 (该类实现了 ActionHook 回调接口)。在 Response 类中会调用 ActionHook 实现类的相关方法的，Response 类的 action 方法如下：
    
    ![](https://static001.infoq.cn/resource/image/2a/12/2a01ddee8e5102e131b20890f706c012.jpg)
    
5.  Http11NioProcessor 的 process 实现方法中，会通过 Adapter 来调用 Servler 容器生成响应结果。


## 4 如何实现 Connector

由上面的介绍我们可以知道，实现 Connector 就是实现 ProtocolHander 接口的过程。

AjpAprProtocol、AjpProtocol、Http11AprProtocol、Http11Protocol、JkCoyoteHandler、MemoryProtocolHandler 这些实现类的实现流程与 Http11NioProtocol 相同，下面我们以 Http11NioProtocol 为类重点说明 tomcat 中如何实现 ProtocolHander 接口的。

Http11NioProtocol 实现了 ProtocolHander 接口，它将所有的操作委托给 NioEndpoint 类去做，如下图：

![Tomcat处理HTTP请求源码分析（下）](https://static001.infoq.cn/resource/image/e4/cf/e4c16485fdc13ad112808d8fbcacd8cf.jpg)

NioEndpoint 类中的 init 方法中首先以普通阻塞方式启动了 SocketServer：

![Tomcat处理HTTP请求源码分析（下）](https://static001.infoq.cn/resource/image/44/ea/44afe6c9ce6e933c2a7f11f5e3f2d3ea.jpg)

NioEndpoint 类的 start 方法是关键，如下：

![Tomcat处理HTTP请求源码分析（下）](https://static001.infoq.cn/resource/image/c3/44/c34acd57bfe631c970c7fcdc6750ab44.jpg)

可以看出，在 start 方法中启动了两个线程和一个线程池：

*   Acceptor 线程，该线程以普通阻塞方式接收客户端请求（socket.accep()），将客户 Socket 交由线程池是处理，线程池要将该 Socket 配置成非阻塞模式（socket.configureBlocking(false)）, 并且向 Selector 注册 READ 事件。该线程数目可配置，默认为 1 个。
*   Poller 线程，由于 Acceptor 委托线程为客户端 Socket 注册了 READ 事件，当 READ 准备好时，就会进入 Poller 线程的循环，Poller 线程也是委托线程池去做，线程池将 NioChannel 加入到 ConcurrentLinkedQueue<NioChannel> 队列中。该线程数目可配置，默认为 1 个。
*   线程池，就是上面说的做 Acceptor 与 Poller 线程委托要做的事情。

### 4.1 Init 接口实现方法中阻塞方式启动 ServerSocketChannel

在 Init 接口实现方法中阻塞方式启动 ServerSocketChannel。

![Tomcat处理HTTP请求源码分析（下）](https://static001.infoq.cn/resource/image/a6/a5/a6e38845a31b919986a4742065eaaea5.jpg)

### 4.2 Start 接口实现方法中启动所有线程

Start 方法中启动了线程池，acceptor 线程与 Poller 线程。其中 acceptor 与 poller 线程一般数目为 1，当然，数目也可配置。

![Tomcat处理HTTP请求源码分析（下）](https://static001.infoq.cn/resource/image/1f/2a/1f7450c44901b246a9e0855c5709df2a.jpg)

可以看出，线程池有两种实现方式：

*   普通 queue + wait + notify 方式，默认使用的方式，据说实际测试这种比下种效率高
*   JDK1.5 自带的线程池方式

### 4.3 Acceptor 线程接收客户请求、注册 READ 事件

在 Acceptor 线程中接收了客户请求，同时委托线程池注册 READ 事件。

1.  在 Acceptior 线程中接收了客户请求（serverSock.accept()）

![Tomcat处理HTTP请求源码分析（下）](https://static001.infoq.cn/resource/image/e1/e2/e143151da91784a7a228ac4514fc2fe2.jpg)

3.  委托线程池处理

![Tomcat处理HTTP请求源码分析（下）](https://static001.infoq.cn/resource/image/94/29/9426d4a6b8618f26ea829237ab4bc029.jpg)

5.  在线程池的 Worker 线程的 run 方法中有这么几句：

![Tomcat处理HTTP请求源码分析（下）](https://static001.infoq.cn/resource/image/43/e6/434d09be627008e6a66ae441937670e6.jpg)

在 setSocketOptions 方法中，首先将 socket 配置成非阻塞模式：

![Tomcat处理HTTP请求源码分析（下）](https://static001.infoq.cn/resource/image/59/16/594bf66635c87354a7c8aa5bb4927716.jpg)

在 setSocketOptions 方法中，最后调用 getPoller0().register(channel); 一句为 SocketChannel 注册 READ 事件，register 方法代码如下 (注意：这是 Poller 线程的方法)：

![Tomcat处理HTTP请求源码分析（下）](https://static001.infoq.cn/resource/image/87/e6/87c169617da9a657b59a8757674631e6.jpg)

其中 attachment 的结构如下，它可以看做是一个共享的数据结构：

![Tomcat处理HTTP请求源码分析（下）](https://static001.infoq.cn/resource/image/97/03/97d7b508d0c8e7ec6f12a1532933bf03.jpg)

### 4.4 Poller 线程读请求、生成响应数据、注册 WRITE 事件

1.  在上面说的 setSocketOptions 方法中调用 Poller 线程的 register 方法注册读事件之后，当 READ 准备就绪之后，就开始读了。下面代码位于 Poller 线程的 run 方法之中：

![Tomcat处理HTTP请求源码分析（下）](https://static001.infoq.cn/resource/image/f2/2e/f28165e9de7acd199a3902f1b479672e.jpg)

3.  可以看到，可读之后调用 processSocket 方法，该方法将读处理操作委拖给线程池处理 (注意此时加入到线程池的是 NioChannel，不是 SocketChannel)：

![Tomcat处理HTTP请求源码分析（下）](https://static001.infoq.cn/resource/image/96/89/96f50083f76eb885d0f55e41548b9289.jpg)

5.  线程池的 Worker 线程中的 run 方法中的部分代码如下（请注意 handler.process(socket) 这一句）：

![Tomcat处理HTTP请求源码分析（下）](https://static001.infoq.cn/resource/image/5c/98/5c173faa46c7c8771565a067aaff8498.jpg)

注意：

*   调用了 hanler.process(socket) 来生成响应数据）
*   数据生成完之后，注册 WRITE 事件的，代码如下：

![Tomcat处理HTTP请求源码分析（下）](https://static001.infoq.cn/resource/image/56/ea/56e0162b9b494fc5ae873c8e45fae1ea.jpg)

### 4.5 Handle 接口实现类通过 Adpater 调用 Servlet 容器生成响应数据

NioEndpoint 类中的 Handler 接口定义如下：

![Tomcat处理HTTP请求源码分析（下）](https://static001.infoq.cn/resource/image/f1/86/f146a6241cd6ba3891202b856f3c8186.jpg)

其中 process 方法通过 Adapter 来调用 Servlet Container 生成返回结果。Adapter 接口定义如下：

![Tomcat处理HTTP请求源码分析（下）](https://static001.infoq.cn/resource/image/39/25/39e657e678cafa38b29f2fd303151025.jpg)

### 4.6 小结

实现一个 tomcat 连接器 Connector 就是实现 ProtocolHander 接口的过程。Connector 用来接收 Socket Client 端的请求，通过内置的线程池去调用 Servlet Container 生成响应结果，并将响应结果同步或异步的返回给 Socket Client。在第三方应用集成 tomcat 作为 Web 容器时，一般不会动 Servlet Container 端的代码，那么 connector 的性能将是整个 Web 容器性能的关键。
