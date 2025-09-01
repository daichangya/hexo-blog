---
title: Spring MVC 3.2 技术预览（二）：实时更新技术
id: 619
date: 2024-10-31 22:01:44
author: daichangya
excerpt: "在上一篇文章中，我介绍了新的Servlet 3，这是Spring MVC 3.2的新特性——异步支持——的运行环境。第二种使用异步处理的非常主要的原因是使浏览器接受信息的实时更新。例如网页聊天室、股票报价、状态更新、体育赛事直播等。虽然这些应用对于信息延迟的敏感度不同，但是它们的功能需求是类似的。"
permalink: /archives/spring-mvc-3-2-preview-techniques-for-real-time-updates/
categories:
 - spring
---


        在[上一篇文章](https://blog.jsdiff.com/archives/spring-mvc-3-2-preview-introducing-servlet-3-async-support)中，我介绍了新的Servlet 3，这是Spring MVC 3.2的新特性——异步支持——的运行环境。第二种使用异步处理的非常主要的原因是使浏览器接受信息的实时更新。例如网页聊天室、股票报价、状态更新、体育赛事直播等。虽然这些应用对于信息延迟的敏感度不同，但是它们的功能需求是类似的。

        在标准的HTTP的“请求—响应”语义中，浏览器发出一个请求，服务器端响应一个请求，这就意味着直到浏览器发送请求，服务器才能够返回更新信息。要想实时获取服务器的更新信息，当前有很多种方法可以实现，例如传统轮询、长轮询、HTTP流和最近兴起的WebSocket协议。

  

# 传统轮询：

        传统轮询采用浏览器不断发送请求，而服务器在收到请求后立即返回信息的方式进行。这种方式适合发送请求较少的情况下使用（请求发送过多服务器就崩溃了）。例如邮箱客户端可以每十分钟检查一次是否有新邮件到来。这种方式简单有效。但是如果需要信息实时反馈给客户端时，请求的发送就非常频繁，这种方式的实现效率就会大大降低。

  

# 长轮询：

        长轮询中浏览器不断发送请求，而服务器只在有新信息更新的时候相应请求。在客户端看来，这种方式与传统轮询的方式完全一样。而在服务器端看来，这种方式与长请求方式非常类似，而且可以比传统轮询方式有更好的扩展性。

        一个响应可以保持打开状态多久呢？浏览器设置的时间范围为5分钟，而一些网络中介——例如代理服务器——设置的时间范围可能更短。所以，即使没有信息更新，一个长轮询请求也要在时间范围内完成响应，以便浏览器发送下一个新请求。[IETF的文档](http://tools.ietf.org/html/rfc6202)建议将时间范围设置为30至120秒之间，但通常实际的时间范围取决于你所使用的网络中介所设置的时间。

        长轮询方式可以显著的降低实时信息更新的延时现象，特别是在新信息的更新间隔时间不确定（不规律）的情况下。但是，信息更新频率越高，这种方式就越像传统轮询一样效率低下。

  

# HTTP流：

        HTTP流采用浏览器不断发送请求，而服务器只在有信息可以返回时相应请求。但是与长轮询不同，HTTP流中服务器保持相应的打开状态，并且随着请求的到来不断向响应中添加更新信息。这种方式不需要进行轮询，但这也是与标准HTTP“请求—相应”的最大不同之处。例如客户端和服务器可以就相应流达成协议，以解决客户端如何识别相应就中不同的更新信息。但是，网络中介可以将相应流缓存，这样就阻止了这种方式的进行。这也是HTTP流不如长轮询方式使用广泛的原因。

  

# WebSocket协议：

        浏览器发送一个HTTP请求，这个请求将在服务器端被转换为WebSocket协议，服务器在确认有更新信息后再返回相应。这样一来，浏览器和服务器之间就可以建立一个双向连接，通过TCP协议按帧来发送数据。

        WebSocket协议的设计就是用来避免轮询，并且非常适合在浏览器和服务器之间频繁交换信息的情况下使用。通过HTTP的初始化握手可以保证WebSocket请求通过防火墙。但是，由于主流浏览器很少支持WebSocket协议（Chrome支持的哦），因此基于WebSocket协议的应用开发具有非常大的挑战性，而且在经过网络中介时还存在[更多问题](http://www.infoq.com/articles/Web-Sockets-Proxy-Servers)。

        WebSocket以浏览器和服务器双向交互文本信息或二进制数据为中心。这导致它与传统的RESTful、以HTTP为基础的架构有很大的不同。事实上，还有很多其他协议需要建立在WebSocket基础之上，例如XMPP、AMQP、STOMP等，而哪个（些）协议将成为主流协议还需要拭目以待。

        IETF组织已经将[WebSocket协议](http://tools.ietf.org/html/rfc6455)制定为一个标准，而由W3C组织制定的[WebSocket API](http://www.w3.org/TR/websockets)标准也已经进入了最后一个阶段。很多Java工具——包括Servlet容器Jetty和Tomcat——都已经开始支持WebSocket。Servlet 3.1规范也很有可能将WebSocket包含在内，同时一个[新的JSR规范](http://jcp.org/en/jsr/detail?id=356)也将定义WebSocket API。

  

# 总结：

        尽管挑选出一个最优秀的方式很诱人，但是——和其他问题一样——最简单最符合实际面对的问题的解决方式才是最好的解决方式。WebSocket协议给了我们很好的解决方案，而且也将适用于越来越多的情况下。浏览器的支持情况和网络问题先放在一边，双向信息的传输和RESTful的HTTP架构是两种完全不同的方式。在REST中你为资源建模并应用HTTP动词来获取资源。而在双向信息传输中，你将按规定路线发送、过滤、处理信息。记住这点不同非常的重要。

        回到我[上一篇文章](https://blog.jsdiff.com/archives/spring-mvc-3-2-preview-introducing-servlet-3-async-support)中介绍的Spring MVC 3.2新特性中，我们可以使用长请求来实现实时更新功能，这种方式建立于标准的HTTP“请求—响应”架构中，就像常轮询和一些扩展自HTTP流的技术类似。[Filip Hanik](http://www.tomcatexpert.com/blog/2012/04/24/websockets-tomcat-7)将这称为“客户端可以调用的服务器端AJAX”（the server version of client AJAX calls）。虽然Spring MVC 3.2 M1版本中没有包含WebSocket的支持，但在最终版本中仍然可能会包含。

        在下一篇文章中，我将出示一个源码示例，并对Spring MVC 3.2的一些技术细节进行分析。
原文地址：[http://blog.springsource.org/2012/05/08/spring-mvc-3-2-preview-techniques-for-real-time-updates/](http://blog.springsource.org/2012/05/08/spring-mvc-3-2-preview-techniques-for-real-time-updates/)
