---
title: Spring MVC 3.2 技术预览（三）：动手写一个异步Controller方法
id: 763
date: 2024-10-31 22:01:45
author: daichangya
excerpt: "前面的文章中我介绍了Servlet 3、Spring MVC 3.2中支持异步的新特性，并介绍了一些实时更新的技术背景。在这篇文章中，我将展示一些Spring MVC 3.2新特性的技术细节，以及对Spring MVC request生命周期多方面的影响。如果需要将Controller层的方法转变为异步方法，只要将方法的返回值类型改为Callable就可以了。例如，返回视图名String类型的方法，可以改为返回Callable类型；返回ResponseEntity类型的方法，可以改为返回Callable类型；其他的返回值类型都可以以此类推。"
permalink: /archives/spring-mvc-3-2-preview-making-a-controller-method-asynchronous/
categories:
 - spring
---

  

        [前面的文章](https://blog.jsdiff.com/archives/spring-mvc-3-2-preview-techniques-for-real-time-updates)中我介绍了Servlet 3、Spring MVC 3.2中支持异步的新特性，并介绍了一些[实时更新的技术背景](https://www.iteye.com/blog/1534902)。在这篇文章中，我将展示一些Spring MVC 3.2新特性的技术细节，以及对Spring MVC request生命周期多方面的影响。

        如果需要将Controller层的方法转变为异步方法，只要将方法的返回值类型改为Callable就可以了。例如，返回视图名String类型的方法，可以改为返回Callable<String>类型；返回ResponseEntity类型的方法，可以改为返回Callable<ResponseEntity>类型；其他的返回值类型都可以以此类推。

        这种处理方式中，除了Controller层方法在另外一个线程中处理完成外，其他的工作方式没有发生任何变化。当方法改变成异步处理后，保持处理方式的简单非常重要。因为你会发现，今天我仅仅讲方法改为异步方式，但还是有很多相关问题需要考虑到。

  

# 示例代码：

        GitHub上spring-mvc-showcase项目中的[spring-mvc-async](https://github.com/SpringSource/spring-mvc-showcase/tree/spring-mvc-async)分支里，有很多Controller层异步方法的示例。

        例如下面的[@ResponseBody](https://github.com/SpringSource/spring-mvc-showcase/blob/8b9e275f55428324731b4ef6f3679d7341b67c35/src/main/java/org/springframework/samples/mvc/response/ResponseController.java#L16)方法，其中返回了视图名String：


		@RequestMapping(value="/response/annotation", method=RequestMethod.GET)
		public @ResponseBody Callable<String> responseBody() {

			return new Callable<String>() {
				public String call() throws Exception {

					// Do some work..
					Thread.sleep(3000L);

					return "The String ResponseBody";
				}
			};
		}

        以及下面的[ResponseEntity](https://github.com/SpringSource/spring-mvc-showcase/blob/8b9e275f55428324731b4ef6f3679d7341b67c35/src/main/java/org/springframework/samples/mvc/response/ResponseController.java#L48)方法：


		@RequestMapping(value="/response/entity/headers", method=RequestMethod.GET)
		public Callable<ResponseEntity<String>> responseEntityCustomHeaders() {

			return new Callable<ResponseEntity<String>>() {
				public ResponseEntity<String> call() throws Exception {

					// Do some work..
					Thread.sleep(3000L);

					HttpHeaders headers = new HttpHeaders();
					headers.setContentType(MediaType.TEXT_PLAIN);
					return new ResponseEntity<String>(
							"The String ResponseBody with custom header Content-Type=text/plain", headers, HttpStatus.OK);
				}
			};
		}

        还有[redirect类型的视图名方法](https://github.com/SpringSource/spring-mvc-showcase/blob/8b9e275f55428324731b4ef6f3679d7341b67c35/src/main/java/org/springframework/samples/mvc/redirect/RedirectController.java#L30)：


		@RequestMapping(value="/uriTemplate", method=RequestMethod.GET)
		public Callable<String> uriTemplate(final RedirectAttributes redirectAttrs) {

			return new Callable<String>() {
				public String call() throws Exception {

					// Do some work..
					Thread.sleep(3000L);

					redirectAttrs.addAttribute("account", "a123");  // Used as URI template variable
					redirectAttrs.addAttribute("date", new LocalDate(2011, 12, 31));  // Appended as a query parameter
					return "redirect:/redirect/{account}";
				}
			};
		}

        添加了@RequestMapping注解和@ResponseBody注解的方法中，这些注解同样会应用到返回值Callable中。添加了[@ExceptionHandler](https://github.com/SpringSource/spring-mvc-showcase/blob/8b9e275f55428324731b4ef6f3679d7341b67c35/src/main/java/org/springframework/samples/mvc/exceptions/ExceptionController.java#28)注解的方法也一样，它调用了Controller层方法返回的Callable中抛出的异常。




	package org.springframework.samples.mvc.exceptions;

	import java.util.concurrent.Callable;

	import org.springframework.stereotype.Controller;
	import org.springframework.web.bind.annotation.ExceptionHandler;
	import org.springframework.web.bind.annotation.RequestMapping;
	import org.springframework.web.bind.annotation.ResponseBody;

	@Controller
	public class ExceptionController {

		@RequestMapping("/exception")
		public @ResponseBody Callable<String> exception() {

			return new Callable<String>() {
				public String call() throws Exception {

					// Do some work..
					Thread.sleep(2000L);

					throw new IllegalStateException("Sorry!");
				}
			};
		}

		@ExceptionHandler
		public @ResponseBody String handle(IllegalStateException e) {
			return "IllegalStateException handled!";
		}

	}

        在GitHub中提交的[这个版本](https://github.com/SpringSource/spring-mvc-showcase/commit/8b9e275f55428324731b4ef6f3679d7341b67c35)，记录了其中全部更新的情况。

        如果你运行了上面的任意一个方法，将会在控制台看到如下信息：


	16:19:23 [http-bio-8080-exec-3] DispatcherServlet - DispatcherServlet with name 'appServlet' processing ...  
	16:19:23 [http-bio-8080-exec-3] RequestMappingHandlerMapping - Looking up handler method for path /views/html  
	16:19:23 [http-bio-8080-exec-3] RequestMappingHandlerMapping - Returning handler method ...  
	16:19:23 [http-bio-8080-exec-3] DispatcherServlet - Exiting request thread and leaving the response open  
	16:19:23 [SimpleAsyncTaskExecutor-1] DispatcherServlet - Resuming asynchronous processing of ...  
	16:19:26 [SimpleAsyncTaskExecutor-1] DispatcherServlet - Rendering view ...  
	16:19:26 [SimpleAsyncTaskExecutor-1] JstlView - Added model object 'fruit'  
	16:19:26 [SimpleAsyncTaskExecutor-1] JstlView - Added model object 'foo'  
	16:19:26 [SimpleAsyncTaskExecutor-1] JstlView - Forwarding to resource [/WEB-INF/views/views/html.jsp]  
	16:19:26 [SimpleAsyncTaskExecutor-1] DispatcherServlet - Successfully completed request  
	16:19:26 [SimpleAsyncTaskExecutor-1] AsyncExecutionChainRunnable - Completing async request processing 

        从上面的日志信息中可以看出，Servlet容器调用的线程马上就执行完了方法，而余下的处理内容则在3秒钟后由另外一个线程完成。除了这些意外，上面的日志信息与普通的请求处理信息是一样的。

  

# 线程池配置：

        正如上面的日志信息所示，返回值Callable会默认调用[SimpleAsyncTaskExecutor](http://static.springsource.org/spring/docs/3.1.x/javadoc-api/org/springframework/core/task/SimpleAsyncTaskExecutor.html)类来处理，这个类非常简单而且没有重用线程。而在实际的产品中，你将可能会需要使用AsyncTaskExecutor类来针对你所处的环境进行适当的配置，甚至有可能你已经有了一个配置好的AsyncTaskExecutor类。可以用RequestMappingHandlerAdapter类中的asyncTaskExecutor属性来引用它。

  

超时设定：

        超时设定是我们需要考虑的非常重要的一个方面。因为Servlet容器可能会强制将一个超时的未完成的异步请求关闭，你可以通过RequestMappingHandlerAdapter类中的asyncRequestTimeout属性指定超时时间。如果不指定超时时间，超时的时间将取决于Servlet容器所设定的时间。在Tomcat中，这个超时时间被默认设定为10秒钟（Servlet容器调用的线程执行时就开始计时）。

        在超时后仍然使用一个request或response的影响是不确定的。在实际使用中，Servlet容器将尝试重用request和response对象。这样一来，避免在超时后仍然使用request和response将变得非常重要。

        事实上，没有方法可以检测request是否已经超时。但是Servlet API中，当请求超时或网络出现问题时，将提供一个声明式的回调函数。Spring MVC中自动注册了这个声明，因此可以得知，一对请求响应是否不应该被使用。

        下面是执行过程中的事件序列：


        如果想要完全理解上面的过程，可以参考其中涉及到的三个线程——请求处理开始的线程（Servlet容器调用的线程）、执行Callable方法的线程（异步线程）和Servlet容器向Spring MVC声明超时的线程。

  

# 异常：

        异步处理中HandlerExceptionResolver类和异常处理的机制没有太多不同。当返回Callable之前发生了异常，处理方式与普通异常一样；当执行Callable方法的过程中产生异常，处理方式也与普通异常一样，只不过将在当前线程（异步线程）中处理，并将仍然返回未处理的500状态的response。

  

# ThreadLocal属性：

        Spring MVC的一些部分和Spring MVC应用程序可能会以来ThreadLocal存储来获取request、locale及其他。当以异步的方式执行Callable方法时，异步线程将拥有相同的ThreadLocal属性。

        OpenSessionInViewFilter和OpenSessionInViewInterceptor也被更新为以透明的方式工作。而当Controller层的方法使用了@Transactional注解时，方法返回时就将完成事务，而不会扩展到执行Callable方法的内部。如果Callable需要处理事务，则需要委托（delegate）一个事务组件。

  

# 拦截器处理：

        已注册的HandlerInterceptor实例将与异步请求协作工作。主要的区别是：preHandle在Servlet容器线程开始的时候调用，而postHandle和afterCompletion方法则在异步线程中调用。在大多数情况下不会出现问题，除非HandlerInterceptor设置并清除了ThreadLocal属性。需要如此做的拦截器可能实现了AsyncHandlerInterceptor接口，这个借口为异步请求的处理添加了生命周期。

  

# Servlet过滤器：

        一些过滤器将正常工作。而其他的过滤器将尝试在Servlet容器线程退出后执行后置处理（post-processing）。这样的过滤器需要进行一定的修改用来在异步线程中完成后置处理。所有的Spring过滤器都已经按照要求（按照异步请求处理的要求）进行修改，来与异步请求协同工作。但是第三方的过滤器是否能够在Spring MVC下正常处理异步请求，取决于这些过滤器的实现细节。

  

# 总结：

        在我的下一篇文章中，我将使用一个基于接收外部事件（AMQP消息）的示例，将其使用传统轮询的方式修改为使用长轮询的方式，用来在浏览器中显示实时信息。

原文地址：[http://blog.springsource.org/2012/05/10/spring-mvc-3-2-preview-making-a-controller-method-asynchronous/](http://blog.springsource.org/2012/05/10/spring-mvc-3-2-preview-making-a-controller-method-asynchronous/)
