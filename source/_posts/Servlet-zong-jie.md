---
title: Servlet总结
id: 320
date: 2024-10-31 22:01:42
author: daichangya
excerpt: 'Servlet 什么是Servlet？ Servlet是一个JavaEE组件，是在服务器端运行以处理客户端请求并作出响应的程序。

  Servlet的执行过程？ 首先，客户端发送请求到服务器端； 其次，服务器端根据web.xml文件中的Servlet相关配置信息，将客户端请求转发到相应的Servlet；
  之后，Servlet会根据request对象中封装的用户请求'
permalink: /archives/Servlet-zong-jie/
tags:
- servlet
---

 

Servlet

## 什么是Servlet？

       Servlet是一个JavaEE组件，是在服务器端运行以处理客户端请求并作出响应的程序。

## Servlet的执行过程？

首先，客户端发送请求到服务器端；

其次，服务器端根据web.xml文件中的Servlet相关配置信息，将客户端请求转发到相应的Servlet；

之后，Servlet会根据request对象中封装的用户请求与数据库进行交互，返回数据之后，Servlet会将返回的数据封装到response对象中；

此时，控制权从Servlet重新回到服务器端，最后，服务器端将响应信息返回给客户端，并且跳转到相应的页面。

## Servlet的生命周期？

1）加载和实例化；在第一次请求Servlet时，Servlet容器将会创建Servlet实例；

2）初始化；Servlet容器加载完成Servlet之后，必须进行初始化，此时，init方法将被调用；

3）Servlet初始化之后，就处于响应请求的就绪状态，此时如有客户端请求发送，就会调用Servlet实例的service方法，并且根据用户的请求方式，调用doPost或者doGet方法；

4）最后，Servlet容器负责将Servlet实例进行销毁，调用destroy方法实现；

## Servlet与JSP的关系及区别？

Servlet是JSP的基础，JSP是Servlet技术的扩展。JSP运行之前首先将编译为一个Servlet。

JSP侧重于视图；Servlet主要用于控制业务逻辑。

## Servlet API中的forward()与redirect()的区别？

请求转发：forward是Request对象的方法，它是在服务器端执行，并且始终在同一个Request域中，所以页面间可以共享Request对象中的资源。转发后，客户端浏览器地址不会改变；请求转发性能优于重定向；

重定向：redirect是response对象的方法，发生在客户端浏览器，它有两次Request请求，第二次请求将丢失第一次Request中的资源。重定向之后，客户端浏览器地址发生改变。

## Servlet如何同时处理多个请求？

       Servlet采用多线程来处理多个请求的同时访问。Servlet容器通过线程池来管理维护服务请求。所谓线程池，相当于数据库连接池，实际上是等待执行代码的一组线程，叫做工作者线程。Servlet容器通过一个调度线程来管理工作者线程。

· 当容器收到一个Servlet的访问请求，调度者线程就从线程池中选出一个工作者线程，将用户请求传递给该线程，然后由该线程处理Servlet的service()方法；

· 当这个线程在执行的时候，容器收到一个新的请求，调度者线程再次从线程池中选出一个新的工作者线程；

· 当容器同时收到对同一个Servlet的多个请求时，那么Servlet的service方法将在多线程中并发执行。

注：1.Servlet容器默认采用单实例多线程的方式来处理请求。这样减少了产生Sevlet实例的开销，提升了对请求的响应时间；

       2.对于Tomcat容器来讲，可以在其server.xml中通过<Connector>中设置线程池中的线程数目。

问题：Servlet可不可以采用多实例多线程？或者多实例单线程？

## 如何开发线程安全的Servlet？

       Servlet容器采用多线程来处理请求，提高性能的同时也造成了线程安全问题。要开发线程安全的Servlet应该从一下几个方面进行：

1．变量的线程安全； 多线程并不共享局部变量，所以我们要尽可能的在Servlet中使用局部变量；

2．代码块的线程安全； 使用同步块Synchronized，防止可能调用的代码块；但是要注意的是，要尽可能得缩小同步代码的方范围，不要在service方法和响应方法上直接使用同步，这会严重影响性能。

3．属性的线程安全； ServletContext，HttpSession，ServletRequest对象中属性；

4．使用同步集合； 使用Vector代替ArrayList，使用HashTable代替HashMap；

5．不要在Servlet中创建自己的线程来完成某个功能； Servlet本身就是多线程的，如果再创建新的线程，将会导致线程执行复杂化，出现线程安全问题；

6．在多个Servlet中，对外部对象，比如：文件；进行修改操作一定要加锁，做到互斥访问；

## SingleThreadMode？

javax.servlet.SingleThreadModel接口是一个标识接口，如果一个Servlet实现了这个接口，那Servlet容器将保证在一个时刻仅有一个线程可以在给定的servlet实例的service方法中执行，将其他所有请求进行排队。

## 如何实现servlet的单线程模式？

实现方法：<%@ page isThreadSafe="false" %>