---
title: java开源测试工具大汇总
id: 976
date: 2024-10-31 22:01:47
author: daichangya
excerpt: "java开源测试工具大汇总"
permalink: /archives/6178963/
tags: 
 - 测试
---



<p style="margin: 0px; padding: 0px;">JUnit

JUnit

　　JUnit是由Erich Gamma 和Kent Beck 编写的一个回归测试框架(regression testing framework)。Junit测试是程序员测试，即所谓白盒测试，因为程序员知道被测试的软件如何(How)完成功能和完成什么样(What)的功能。Junit是一套框架，继承TestCase类，就可以用Junit进行自动测试了。

　　http://www.junit.org/

　　Cactus

　　Cactus是一个基于JUnit框架的简单测试框架，用来单元测试服务端[Java](http://dev.yesky.com/devjava/)代码。Cactus框架的主要目标是能够单元测试服务端的使用Servlet对象的Java方法如HttpServletRequest,HttpServletResponse,HttpSession等

　　http://jakarta.apache.org/cactus/

　　Abbot

　　Abbot是一个用来测试Java GUIs的框架。用简单的基于XML的脚本或者Java代码，你就可以开始一个GUI。

　　http://abbot.sourceforge.net/

　　JUnitPerf

　　Junitperf实际是junit的一个decorator，通过编写用于junitperf的单元测试，我们也可使测试过程自动化。

　　http://www.clarkware.com/software/JUnitPerf.html

　　DbUnit

　　DbUnit是为数据库驱动的项目提供的一个对JUnit 的扩展，除了提供一些常用功能，它可以将你的数据库置于一个测试轮回之间的状态。

　　http://dbunit.sourceforge.net/

　　Mockrunner

　　Mockrunner用在J2EE环境中进行应用程序的单元测试。它不仅支持Struts actions, servlets，过滤器和标签类还包括一个JDBC和一个JMS测试框架，可以用于测试基于EJB的应用程序。

　　http://mockrunner.sourceforge.net/index.html

　　DBMonster

　　DBMonster是一个用生成随机数据来测试SQL数据库的压力测试工具。

　　http://dbmonster.kernelpanic.pl/

　　MockEJB

　　MockEJB是一个不需要EJB容器就能运行EJB并进行测试的轻量级框架。

　　http://mockejb.sourceforge.net/

　　StrutsTestCase

　　StrutsTestCase 是Junit TestCase类的扩展，提供基于Struts框架的代码测试。StrutsTestCase同时提供Mock 对象方法和Cactus方法用来实际运行Struts ActionServlet，你可以通过运行servlet引擎来测试。因为StrutsTestCase使用ActionServlet控制器来测试你的代码，因此你不仅可以测试Action对象的实现，而且可以测试mappings，from beans以及forwards声明。StrutsTestCase不启动servlet容器来测试struts应用程序(容器外测试)也属于Mock对象测试，但是与EasyMock不同的是，EasyMock是提供了创建Mock对象的API，而StrutsTest则是专门负责测试Struts应用程序的Mock对象测试框架。

　　[http://strutstestcase.sourceforge.net/](http://strutstestcase.sourceforge.net/)

JFCUnit

　　JFCUnit使得你能够为Java偏移应用程序编写测试例子。它为从用代码打开的窗口上获得句柄提供了支持;为在一个部件层次定位部件提供支持;为在部件中发起事件(例如按一个按钮)以及以线程安全方式处理部件测试提供支持。

　　http://jfcunit.sourceforge.net/

　　JTestCase

　　JTestCase 使用XML文件来组织多测试案例数据，声明条件(操作和期望的结果)，提供了一套易于使用的方法来检索XML中的测试案例，按照数据文件的定义来声明结果。

　　http://jtestcase.sourceforge.net/

　　SQLUnit

　　SQLUnit是一个单元测试框架，用于对数据库存储过程进行回归测试。用Java/JUnit/XML开发。

　　http://sqlunit.sourceforge.net

　　JTR

　　JTR (Java Test Runner)是一个开源的基于反转控制(IOC)的J2EE测试框架。它允许你构建复杂的J2EE测试套件(Test Suites)并连到应用服务器执行测试,可以包括多个测试实例。JTR的licensed是GPL协议。

　　http://jtrunner.sourceforge.net/

　　Marathon

　　Marathon是一个针对使用Java/Swing开发GUI应用程序的测试框架，它由recorder, runner 和editor组成，测试脚本是python代码。Marathon的焦点是放在最终用户的测试上。

　　http://marathonman.sourceforge.net

　　TestNG

　　TestNG是根据JUnit 和NUnit思想而构建的一个测试框架，但是TestNG增加了许多新的功能使得它变得更加强大与容易使用比如：

　　*支持JSR 175注释(JDK 1.4利用JavaDoc注释同样也支持)

　　*灵活的Test配置

　　*支持默认的runtime和logging JDK功能

　　*强大的执行模型(不再TestSuite)

　　*支持独立的测试方法。

　　http://testng.org/

　　Surrogate Test framework

　　Surrogate Test framework是一个值得称赞单元测试框架，特别适合于大型，复杂Java系统的单元测试。这个框架能与JUnit,MockEJB和各种支持模拟对象(mock object )的测试工具无缝给合。这个框架基于AspectJ技术。

　　http://surrogate.sourceforge.net

　　MockCreator

　　MockCreator可以为给定的interface或class生成模拟对象(Mock object)的源码。

　　[http://mockcreator.sourceforge.net/](http://mockcreator.sourceforge.net/)

jMock

　　jMock利用mock objects思想来对Java code进行测试。jMock具有以下特点:容易扩展，让你快速简单地定义mock objects,因此不必打破程序间的关联，让你定义灵活的超越对象之间交互作用而带来测试局限，减少你测试地脆弱性。

　　http://www.jmock.org/

　　EasyMock

　　EasyMock为Mock Objects提供接口并在JUnit测试中利用Java的proxy设计模式生成它们的实例。EasyMock最适合于测试驱动开发。

　　http://www.easymock.org/

　　The Grinder

　　The Grinder是一个负载测试框架。在BSD开源协议下免费使用。

　　http://grinder.sourceforge.net/

　　XMLUnit

　　XMLUnit不仅有Java版本的还有.Net版本的。Java开发的XMLUnit提供了两个JUnit 扩展类XMLAssert和XMLTestCase,和一组支持的类。这些类可以用来比较两张XML之间的不同之处，展示XML利用XSLT来,校验XML,求得XPath表达式在XML中的值,遍历XML中的某一节点利DOM展开,

　　http://xmlunit.sourceforge.net/

　　Jameleon

　　Jameleon一个自动化测试工具。它被用来测试各种各样的应用程序，所以它被设计成插件模式。为了使整个测试过程变得简单Jameleon提供了一个GUI,因此Jameleon实现了一个Swing 插件。

　　http://jameleon.sourceforge.net/index.html

　　J2MEUnit

　　J2MEUnit是应用在J2ME应用程序的一个单元测试框架。它基于JUnit.

　　http://j2meunit.sourceforge.net/

　　Jetif

　　Jetif是一个用纯Java实现的回归测试框架。它为Java程序单元测试以及功能测试提供了一个简单而且可伸缩的架构，可以用于个人开发或企业级开发的测试。它容易使用，功能强大，而且拥有一些企业级测试的重要功能。Jetif来源于JUnit, JTestCase以及TestNG的启发，有几个基本的概念直接来自于JUnit，比如说断言机制，Test Listener的概念，因此从JUnit转到Jetif是非常容易的。

　　http://jetif.sourceforge.net/

　　GroboUtils

　　GroboUtils使得扩展Java测试变得可能。它包括用在Java不同方面测试的多个子项目。在GroboUtils中最常被到的工具是:多线程测试(multi-threaded tests),整体单元测试(hierarchial unit tests),代码覆盖工具(code coverage tool)。

　　http://groboutils.sourceforge.net/

　　Testare

　　TESTARE是用来简化分布式应用程序(比如:在SERVLETS,JMS listeners, CORBA ORBs或RMI环境下)测试开发过程的一个测试框架.

　　[https://testare.dev.java.net/](https://testare.dev.java.net/)

本文转自：[http://joerong666.javaeye.com/blog/325997](http://joerong666.javaeye.com/blog/325997)
