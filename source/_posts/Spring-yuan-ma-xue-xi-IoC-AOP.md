---
title: Spring源码学习 ------ IoC——AOP
id: 307
date: 2024-10-31 22:01:42
author: daichangya
excerpt: '一直想抽空把Spring源码拿来读读，但真正去做这件事的时候发现不简单，Spring发展这么多年，它的规模已不是一个一般的开源框架所能比的，它的主要架构和流程不是非常清晰，很难抓到要害，但有一点可以肯定，它的根基是IoC和AOP，所有的功能扩展和对其他开源框架的支持都是基于这两点来做的，因此要搞定Spring源码主要就是要搞定IoC和AOP这两块。

  IoC从原理上来说是非常简单的，无非就是从'
permalink: /archives/Spring-yuan-ma-xue-xi-IoC-AOP/
categories:
- spring
---

 

一直想抽空把Spring源码拿来读读，但真正去做这件事的时候发现不简单，Spring发展这么多年，它的规模已不是一个一般的开源框架所能比的，它的主要架构和流程不是非常清晰，很难抓到要害，但有一点可以肯定，它的根基是IoC和AOP，所有的功能扩展和对其他开源框架的支持都是基于这两点来做的，因此要搞定Spring源码主要就是要搞定IoC和AOP这两块。

IoC从原理上来说是非常简单的，无非就是从配置文件解析开始到最后在内置容器中管理各个对象，但从Spring IoC源码上看是个非常庞大的体系，因为Spring能支持的特性太多，针对这一点，我已不太可能仔细地阅读每一个细节，也不太可能通过什么方式把这些细节在有限的篇幅中表达出来，只能抓住关键生命周期中关键步骤。

在我看来，IoC最核心就是两个过程：IoC容器初始化和IoC依赖注入，下面通过简单的图示来表述其中的关键过程。

![](http://hi.csdn.net/attachment/201101/12/0_1294835160s16b.gif)

![](http://hi.csdn.net/attachment/201101/12/0_1294835233K4T0.gif)

[Spring源码学习（二）------ AOP](http://blog.csdn.net/cutesource/article/details/6136275)  

AOP有些特有的概念，如：advisor、advice和pointcut等等，使用或配置起来有点绕，让人感觉有些距离感，其实它的实现就是一组标准的设计模式的组合使用：Factory、Proxy、Chain of Responsibility，只要搞清楚这几个设计模式，读AOP的源码是比较容易的。

首先看看ProxyFactoryBean这个类，这是AOP使用的入口，从AOP拿到的bean object就是ProxyFactoryBean.getObject得到的，从这条线下去，发现AOP就是通过Proxy模式从实际要执行的target做了包装，而Proxy还不止一套方案，通过Factory封装了两套Proxy实现方案：JDK 动态Proxy和Cglib Proxy。有两套实现主要是因为JDK 动态Proxy必须要target实现某个接口，如果不满足这个条件就会用Cglib增强字节码的方式来实现proxy。

就拿JDK Proxy为例，Spring AOP使用了标准的JDK提供的动态Proxy方案，我们先看看标准的动态Proxy是什么样子，看下面类图：

![](http://hi.csdn.net/attachment/201101/13/0_1294919505ncNK.gif)

Cilent通过Proxy.newProxyInstance(classLoader, proxiedInterfaces, invocationHandler);就能拿到target的proxy object，在执行target的方法时就会先执行到DynamicProxy中的invoke方法从而实现代理包装。基于这个道理来看Spring AOP的实现，实际上就是标准地基于这个方式来做的，Spring AOP的所有花招都体现在JdkDynamicAopProxy.invoke中（当然在Cglib中是通过callback来做的，道理类似）。

通过看JdkDynamicAopProxy.invoke的源码会发现，Spring AOP的各种花招是通过Chain of Responsibility模式串起来的，先看看一个标准的Chain of Responsibility是什么样子，看下面的类图：

![](http://hi.csdn.net/attachment/201101/13/0_1294920720hR9B.gif)

而Chain of Responsibility的关键在于Invocation与Interceptor的配合，主要原则就两条：

1）Invocation需要维护Interceptor集合和游标，每次调用invoke时需要先调用游标所在的Interceptor.invoke，如果游标已超过最后一个Interceptor，则调用实际target的方法

2）Interceptor的invoke中除了要执行自己的拦截逻辑，还要通过Invocation.invoke把调用传递下去，拦截的灵活性就体现在Invocation.invoke执行与否和执行的顺序。

以上逻辑通过时序图来看，如下图所示：

![](http://hi.csdn.net/attachment/201101/13/0_1294922085Yhm1.gif)

理解Chain of Responsibility后再来看Spring AOP，JdkDynamicAopProxy.invoke做的事情就是以上Client做的事情，

1）首先通过this.advised.getInterceptorsAndDynamicInterceptionAdvice(method, targetClass);组装interceptor chain

2）然后new ReflectiveMethodInvocation(proxy, target, method, args, targetClass, chain);得到invocation

3）最后通过invocation.proceed();启动责任链

## advice 

英 \[əd'vaɪs\] 美 \[əd'vaɪs\]

*   n. 建议；忠告；劝告；通知

## advise 

英 \[əd'vaɪz\] 美 \[əd'vaɪz\]

*   vt. 建议；劝告，忠告；通知；警告
*   vi. 建议；与…商量

  

而Spring AOP的那些概念都体现在组装interceptor chain中，advisor、advice和pointcut无非就是帮助你描述如何对Target进行拦截，对这一块感兴趣的朋友可以好好读读里面的代码。另外，Spring AOP提供了各种各样的Interceptor，来实现各种形式的横切，具体做法可以详细看看各Interceptor的实现。

综上所述，整个流程如下图所示：

![](http://hi.csdn.net/attachment/201101/13/0_1294923277nIlz.gif)

总之，把握了Factory、Proxy、Chain of Responsibility的运用也就把握了Spring AOP的实现原理，道理虽然简单，但其中的精髓和原由还是值得我们继续深思的。