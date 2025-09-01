---
title: Tomcat中Servlet的创建初始化体系结构及工作
id: 1013
date: 2024-10-31 22:01:48
author: daichangya
excerpt: "一个 Web 应用对应一个 Context 容器，在Tomcat中Context容器就是管理 Servlet的，是Servlet 运行时的 Servlet容器，添加一个 Web 应用时将会创建一个 StandardContext 容器，并且给这个 Context 容器设置必要的参数，url 和path 分别代表这个应用在 Tomcat 中的访问路径和这个应用实际的物理路径。Web 应用"
permalink: /archives/19809281/
categories:
 - Tomcat
tags: 
 - servlet
---

   一个 Web 应用对应一个 Context 容器，在Tomcat中Context容器就是管理 Servlet的，是Servlet 运行时的 Servlet 容器，添加一个 Web 应用时将会创建一个 StandardContext 容器，并且给这个 Context 容器设置必要的参数，url 和 path 分别代表这个应用在 Tomcat 中的访问路径和这个应用实际的物理路径。  

**Web** **应用的初始化工作**

对于一个Tomcat中的Web 应用，它的初始化工作是在ContextConfig的configureStart方法中实现的，应用的初始化主要是要解析 web.xml 文件，这个文件描述了一个 Web 应用的关键信息，也是一个 Web 应用的入口。Tomcat 首先会找 globalWebXml 这个文件是在以下两个文件中的任一个 org/apache/catalin/startup/NO\_DEFAULT\_XML 或 conf/web.xml。接着会找 hostWebXml，即寻找应用的配置文件examples/WEB-INF/web.xml。web.xml 文件的各个配置项将会被解析成相应的属性保存在WebXml对象中。接下去将会将 WebXml 对象中的属性设置到 Context 容器中，这里包括创建 Servlet 对象、filter、listener 等等。

然后将Servlet 包装成 StandardWrapper 并作为子容器添加到 Context 中，则Context 容器才是真正运行 Servlet 的 Servlet 容器。一个 Web 应用对应一个 Context 容器，容器的配置属性由应用的 web.xml 指定。  
**创建** **Servlet** **对象**

如果 Servlet 的 load-on-startup 配置项大于0，那么在 Context 容器启动的时候就会被实例化，前面提到在解析配置文件时会读取默认的globalWebXml，在 conf 下的 web.xml 文件中定义了一些默认的配置项，其定义了两个Servlet，分别是：org.apache.catalina.servlets.DefaultServlet 和 org.apache.jasper.servlet.JspServlet 它们的 load-on-startup 分别是 1 和 3，也就是当 Tomcat 启动时这两个 Servlet 就会被启动，JspServlet 这个主要就是为了将JSP页面翻译成一个Servlet的，它会拦截所有的以.jsp后缀名的文件。

创建 Servlet 实例的方法是从 Wrapper. loadServlet开始的。loadServlet 方法要完成的就是获取 servletClass 然后把它交给 InstanceManager 去创建一个基于 servletClass.class 的对象。

**初始化** **Servlet**

由于Servlet 在Web初始化的时候已经包装在StandardWrapper ，则对于初始化 Servlet，是在StandardWrapper的initServlet方法中，这个方法很简单就是调用 Servlet 的 init 的方法，同时把包装了 StandardWrapper 对象的 StandardWrapperFacade 作为 ServletConfig 传给 Servlet。

如果该 Servlet 关联的是一个 jsp 文件，那么前面初始化的就是 JspServlet，接下去会模拟一次简单请求，请求调用这个 jsp 文件，以便编译这个 jsp 文件为 class，并初始化这个 class。

**Servlet** **体系结构**

我们知道 Java Web 应用是基于 Servlet 规范运转，下面介绍一下Servlet的体系结构。

**图** **5.Servlet** **顶层类关联图**  
![](https://s4.51cto.com/attachment/201305/195756953.jpg "1.jpg")  

从上图可以看出 Servlet 规范就是基于这几个类运转的，与 Servlet 主动关联的是三个类，分别是 ServletConfig、ServletRequest 和 ServletResponse。这三个类都是通过容器传递给 Servlet 的，其中 ServletConfig 是在 Servlet 初始化时就传给 Servlet 了，而后两个是在请求达到时调用 Servlet 时传递过来的。我们很清楚 ServletRequest 和 ServletResponse 在 Servlet 运行的意义，ServletConfig对 Servlet 主要是为了获取这个 Servlet 的一些配置属性，而这些配置属性可能在 Servlet 运行时被用到。Servlet 的运行模式是一个典型的“握手型的交互式”运行模式。所谓“握手型的交互式”就是两个模块为了交换数据通常都会准备一个交易场景，这个场景一直跟随这个交易过程直到这个交易完成为止。这个交易场景的初始化是根据这次交易对象指定的参数来定制的，这些指定参数通常就会是一个配置类。所以对号入座，交易场景就由 ServletContext 来描述，而定制的参数集合就由 ServletConfig 来描述。而 ServletRequest 和 ServletResponse 就是要交互的具体对象了，它们通常都是作为运输工具来传递交互结果。  
下图是 ServletConfig 和 ServletContext 在 Tomcat 容器中的类关系图。

**图** **6\. ServletConfig** **在容器中的类关联图**  
![](https://s4.51cto.com/attachment/201305/195840994.jpg "2.jpg")

上图可以看出 StandardWrapper 和 StandardWrapperFacade 都实现了 ServletConfig 接口，而 StandardWrapperFacade 是 StandardWrapper 门面类。所以传给 Servlet 的是 StandardWrapperFacade 对象，这个类能够保证从 StandardWrapper 中拿到 ServletConfig 所规定的数据，而又不把 ServletConfig 不关心的数据暴露给 Servlet。

同样 ServletContext 也与 ServletConfig 有类似的结构，Servlet 中能拿到的 ServletContext 的实际对象也是 ApplicationContextFacade 对象。ApplicationContextFacade 同样保证 ServletContext 只能从容器中拿到它该拿的数据，它们都起到对数据的封装作用，它们使用的都是门面设计模式也就是外观模式。

通过 ServletContext 可以拿到 Context 容器中一些必要信息，比如应用的工作路径，容器支持的 Servlet 最小版本等。

我们在创建自己的 Servlet 类时通常使用的都是 HttpServletRequest 和 HttpServletResponse，它们继承了 ServletRequest 和 ServletResponse。为何 Context 容器传过来的 ServletRequest、ServletResponse 可以被转化为 HttpServletRequest 和 HttpServletResponse 呢？

**图** **7.Request** **相关类结构图**  
![](https://s4.51cto.com/attachment/201305/195920322.jpg "3.jpg")

Tomcat 一接受到请求首先将会创建 org.apache.coyote.Request和 org.apache.coyote.Response，这两个类是 Tomcat 内部使用的描述一次请求和相应的信息类它们是一个轻量级的类，它们作用就是在服务器接收到请求后，经过简单解析将这个请求快速的分配给后续线程去处理，所以它们的对象很小，很容易被 JVM 回收。接下去当交给一个用户线程去处理这个请求时又创建 org.apache.catalina.connector. Request和 org.apache.catalina.connector. Response对象。这两个对象一直穿越整个 Servlet 容器直到要传给 Servlet，传给 Servlet 的是 Request 和 Response 的门面类 RequestFacade 和 RequestFacade，这里使用门面模式与前面一样都是基于同样的目的——封装容器中的数据。

一次请求对应的 Request 和 Response 的类转化如下图所示：  
**图** **8.Request** **和** **Response** **的转变过程**  
![](https://s4.51cto.com/attachment/201305/195957939.jpg "4.jpg")  
**Servlet** **如何工作**

当用户从浏览器向服务器发起一个请求，通常会包含如下信息：http://hostname: port /contextpath/servletpath，

hostname 和 port 是用来与服务器建立 TCP 连接，而后面的 URL 才是用来选择服务器中那个子容器服务用户的请求。

在Tomcat7.0，这种映射工作用一个专门的类来完成的，这个就是 org.apache.tomcat.util.http.mapper，这个类保存了 Tomcat 的 Container 容器中的所有子容器的信息，当org.apache.catalina.connector. Request 类在进入 Container 容器之前，mapper 将会根据这次请求的 hostname 和 contextpath 将 host 和 context 容器设置到 Request 的 mappingData 属性中。所以当 Request 进入 Container 容器之前，它要访问那个子容器这时就已经确定了。  
当Rquest 请求到达了最终的 Wrapper 容器后，此时还需要真正的到达最终的 Servlet ，这里还需要一些步骤，必须要执行 Filter 链，以及要通知你在 web.xml 中定义的 listener。

接下去就要执行 Servlet 的 service 方法了，通常情况下，我们自己定义的 servlet 并不是直接去实现 javax.servlet.servlet 接口，而是去继承更简单的 HttpServlet 类或者 GenericServlet 类，我们可以有选择的覆盖相应方法去实现我们要完成的工作。

Servlet 的确已经能够帮我们完成所有的工作了，但是现在的 web 应用很少有直接将交互全部页面都用 servlet 来实现，而是采用更加高效的 MVC 框架来实现。这些 MVC 框架基本的原理都是将所有的请求都映射到一个 Servlet，然后去实现 service 方法，这个方法也就是 MVC 框架的入口。

   当 Servlet 从 Servlet 容器中移除时，也就表明该 Servlet 的生命周期结束了，这时 Servlet 的 destroy 方法将被调用，做一些扫尾工作。