---
title: Spring MVC 3.2 技术预览（一）：Servlet 3介绍，异步支持
id: 1436
date: 2024-10-31 22:01:55
author: daichangya
excerpt: 概述：SpringMVC3.2M1将引入基于Servlet3.0支持的异步请求处理，我将针对SpringMVC3.2的新特性发布一系列文章，并通过对背景知识和相关内容的充分介绍，让你了解你为什么需要这些新特性，以及如何使用这些新特性。这是这一系列文章中的第一篇。    SpringMVC3.2的更新
permalink: /archives/Spring-MVC-3-2-ji-shu-yu-lan-yi-Servlet/
categories:
- spring
tags:
- servlet
---


# 概述：

 Spring MVC 3.2 M1将引入基于Servlet 3.0支持的异步请求处理，我将针对Spring MVC 3.2的新特性发布一系列文章，并通过对背景知识和相关内容的充分介绍，让你了解你为什么需要这些新特性，以及如何使用这些新特性。这是这一系列文章中的第一篇。

  

        Spring MVC 3.2的更新内容已经可以在[Spring Framework Github](https://github.com/SpringSource/spring-framework/pull/69 "Spring Framework Github")中查看，也可以将http://repo.springsource.org/snapshot设置在你的项目仓库中，来获取快照版本。在后面的文章中，我也将提供一些源码示例的链接。但如果你想现在就尝试这些新特性，也可以在GitHub上签出[spring-mvc-async](https://github.com/SpringSource/spring-mvc-showcase/tree/spring-mvc-async "spring-mvc-async")中的spring-mvc-showcase项目，并通过[提交记录](https://github.com/SpringSource/spring-mvc-showcase/commit/8b9e275f55428324731b4ef6f3679d7341b67c35 "提交记录")查看其中的更新信息。

# 惊鸿一瞥：

        从编程模型的角度来看，可能会出现看似简单的新功能。现在，控制层（Controller）的方法可以返回Callable类型来完成异步请求的处理。Spring MVC 3.2会在[TaskExecutor](http://static.springsource.org/spring/docs/3.1.x/spring-framework-reference/html/scheduling.html)的帮助下在一个独立的线程中调用这个返回值，可以查看下面这个代码片段：


	@RequestMapping(method=RequestMethod.POST)
	public Callable<String> processUpload(final MultipartFile file) {
	 
	  return new Callable<String>() {
		public Object call() throws Exception {
		  // ...
		  return "someView";
		}
	  };
	}

         另一种方式，是在控制层（Controller）方法中返回DeferredResult类型（这是Spring MVC 3.2中的新成员），在任意的线程中完成异步处理。例如对一个外部事件（例如JMS信息、AMQP信息、Redis信息等）作出反应，下面是另外一个代码片段：



	@RequestMapping("/quotes")
	@ResponseBody
	public DeferredResult quotes() {
	  DeferredResult deferredResult = new DeferredResult();
	  // Add deferredResult to a Queue or a Map...
	  return deferredResult;
	}
	 
	// In some other thread..
	// Set the return value on the deferredResult
	 
	deferredResult.set(data);

         大家肯定对上面的代码片段有很多问题，我会在后面一系列的文章中给出更多的细节信息。在我们深入了解之前，我先介绍一些可能会用到的相关技术背景知识。

# 长连接请求：

        当前一些网络应用最常用的异步处理方式就是长连接方式，例如运行一个缓慢的数据库查询、调用一个外部的REST API或者执行其他I/O操作。这些方式很快就会消耗光Servlet容器的线程池，影响程序的可扩展性。

        在一些情况下，你可能需要等待一个处理完成，例如发送邮件、删除数据库操作等。在这种“即发即忘”（fire-and-forget）情况下，你可以使用Spring注解@Async或设置Spring Integration事件并迅速返回，也许还可以返回一个用于确认的ID，为后续的响应所用。这在Spring MVC 3.2之前就可以实现，并且可以避免请求死锁。

        对于结果返回之前需要的其他情况下，你需要先释放处理请求的Servlet容器线程来提高程序的可扩展性。为了实现这个功能，Servlet 3允许一个Servlet在返回请求之后声明保持响应为打开状态，这样请求就可以在一个独立线程中完成。

        为了实现这个功能，可以调用Servlet 3中的request.startAsync()方法，并使用返回的AsyncContext在一个独立线程内继续写入（并最终完成）响应。这在客户端看来没有任何变化，请求仍然看起来像是其他HTTP标准的“请求—相应”一样。但是，在服务器端看来，异步请求处理可以让你以扩展性更好的方式处理请求。下面就是处理异步请求的事件顺序：


        关于Servlet对异步请求处理的支持，还有很多内容，你可以找到[很多](http://www.javaworld.com/javaworld/jw-02-2009/jw-02-servlet3.html)[示例](http://codingjunkie.net/jee-6-and-spring-mvc/)和[文章](http://nurkiewicz.blogspot.com/2011/03/tenfold-increase-in-server-throughput.html)（文章被墙了），但是上面总结的这些是所需要的最基本的概念。

# 总结：

        在下一篇文章中，我将介绍第二种异步请求处理的方式：客户端浏览器无延时的实时获取服务器的更新信息。过去已经发展出了很多方式实现这个功能，一些停留在HTTP标准的“请求—相应”的语义环境下，另一些则以更好的方式实现。

原文地址：[http://blog.springsource.org/2012/05/06/spring-mvc-3-2-preview-introducing-servlet-3-async-support/](http://blog.springsource.org/2012/05/06/spring-mvc-3-2-preview-introducing-servlet-3-async-support/)
