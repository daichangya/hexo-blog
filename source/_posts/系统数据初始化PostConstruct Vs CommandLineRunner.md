---
title: 系统数据初始化PostConstruct Vs CommandLineRunner
id: 1422
date: 2024-10-31 22:01:55
author: daichangya
permalink: /archives/%E7%B3%BB%E7%BB%9F%E6%95%B0%E6%8D%AE%E5%88%9D%E5%A7%8B%E5%8C%96postconstructvscommandlinerunner/
---

有时我们只需要在应用程序启动时运行一小段代码，要么只是记录某个bean已加载，要么应用程序已准备好处理请求。

Spring Boot在启动时提供了至少5种不同的执行代码的方式，那么我们应该选择哪一种呢？本文概述了这些不同的方法，并说明了何时使用哪种方法。

不过，让我们从一些用例开始。

[](#code-example)[](https://github.com/thombergs/code-examples/tree/master/spring-boot/startup)代码示例
---------------------------------------------------------------------------------------------------

本文随附[GitHub上](https://github.com/thombergs/code-examples/tree/master/spring-boot/startup)的工作代码示例。

[](#why-would-i-want-to-execute-code-at-startup)为什么我要在启动时执行代码？
--------------------------------------------------------------

在应用程序启动时做某事的最关键的用例是，当我们希望我们的应用程序仅在设置所有内容以支持该处理时才开始处理某些数据。

假设我们的应用程序是事件驱动的，并从队列中提取事件，对其进行处理，然后将新事件发送到另一个队列。在这种情况下，我们希望应用程序仅在与目标队列的连接已准备好接收事件时才开始从源队列中提取事件。因此，我们包含了一些启动逻辑，一旦与目标队列的连接准备就绪，便可以激活事件处理。

在更常规的设置中，我们的应用程序响应HTTP请求，从数据库加载数据，并将数据存储回数据库。我们只想在数据库连接准备好开始工作时才开始响应HTTP请求，否则，我们将以HTTP状态500提供响​​应，直到连接准备好为止。

**Spring Boot会自动处理许多情况，并且仅在应用程序“热”时才会激活某些连接。**

但是，对于自定义方案，我们需要一种使用自定义代码对应用程序启动做出反应的方法。Spring和Spring Boot提供了几种方法。

让我们依次看一下它们。

[](#commandlinerunner)`CommandLineRunner`
-----------------------------------------

`CommandLineRunner` 这是一个简单的接口，我们可以在Spring应用程序成功启动后执行以下代码：

    @Component
    @Order(1)
    class MyCommandLineRunner implements CommandLineRunner {
    
      private static final Logger logger = ...;
    
      @Override
      public void run(String... args) throws Exception {
      if(args.length > 0) {
        logger.info("first command-line parameter: '{}'", args[0]);
      }
      }
    
    }
    

当Spring Boot `CommandLineRunner`在应用程序上下文中找到一个bean时，它将`run()`在应用程序启动后调用其方法，并传递用于启动应用程序的命令行参数。

现在，我们可以使用如下命令行参数启动应用程序：

    java -jar application.jar --foo=bar
    

这将产生以下日志输出：

    first command-line parameter: '--foo=bar'
    

如我们所见，该参数未解析，而是解释为带有value的单个参数`--foo=bar`。稍后我们将看到`ApplicationRunner`解析如何为我们解析参数。

请注意`Exception`中的签名`run()`。即使我们不需要在案例中将其添加到签名中，因为我们不会引发异常，但它表明Spring Boot将在我们的中处理异常`CommandLineRunner`。**Spring Boot认为a `CommandLineRunner`是应用程序启动的一部分，当它引发异常时将中止启动**。

`CommandLineRunner`使用`@Order`注解可以将几个s排列在一起。

**当我们要访问简单的以空格分隔的命令行参数时，a `CommandLineRunner`是一种方法。**

#### [](#dont-order-too-much)不要`@Order`太多

尽管`@Order`注释非常方便，可以将某些启动逻辑片段放入序列中，但这也表明这些启动片段彼此依赖。我们应该努力使依赖关系尽可能少，以创建可维护的代码库。

而且，`@Order`注释创建了一个难以理解的**逻辑依赖性，**而不是易于捕获的编译时依赖性。将来，您可能会想知道该`@Order`注释并删除它，从而导致大决战。

[](#applicationrunner)`ApplicationRunner`
-----------------------------------------

`ApplicationRunner`如果我们要解析命令行参数，可以改用：

    @Component
    @Order(2)
    class MyApplicationRunner implements ApplicationRunner {
    
      private static final Logger logger = ...;
    
      @Override
      public void run(ApplicationArguments args) throws Exception {
      logger.info("ApplicationRunner#run()");
      logger.info("foo: {}", args.getOptionValues("foo"));
      }
    
    }
    

该`ApplicationArguments`对象使我们可以访问已解析的命令行参数。每个参数可以具有多个值，因为它们可能在命令行中多次使用。我们可以通过调用获取特定参数值的数组`getOptionValues()`。

让我们`foo`再次使用参数启动应用程序：

    java -jar application.jar --foo=bar
    

结果日志输出如下所示：

    foo: [bar]
    

与一样`CommandLineRunner`，`run()`方法中的异常将中止应用程序启动，并且`ApplicationRunners`可以使用`@Order`批注按顺序放置多个异常。由创建的序列`@Order`在`CommandLineRunner`s和`ApplicationRunner`s 之间共享。

**`ApplicationRunner`如果需要创建一些可以访问复杂命令行参数的全局启动逻辑，我们将使用。**

[](#applicationlistener)`ApplicationListener`
---------------------------------------------

如果我们不需要访问命令行参数，可以将启动逻辑绑定到Spring的`ApplicationReadyEvent`：

    @Component
    @Order(0)
    class MyApplicationListener 
        implements ApplicationListener<ApplicationReadyEvent> {
    
      private static final Logger logger = ...;
    
      @Override
      public void onApplicationEvent(ApplicationReadyEvent event) {
        logger.info("ApplicationListener#onApplicationEvent()");
      }
    
    }
    

该`ApplicationReadyEvent`只申请后发射准备（废话），使 **上述听众将在本文中描述的所有其他解决方案执行后，做了他们的工作**。

多`ApplicationListeners`可放于同一个顺序`@Order`标注。订单序列仅与其他`ApplicationListener`s 共享，而不与`ApplicationRunner`s或`CommandLineRunner`s 共享。

**一个`ApplicationListener`用于监听`ApplicationReadyEvent`是去，如果我们需要在不访问命令行参数来创建一些全球启动逻辑的方式。**我们仍然可以通过使用Spring Boot对[配置属性](/spring-boot-configuration-properties/)的支持注入环境参数来访问它们。

[](#postconstruct)`@PostConstruct`
----------------------------------

创建启动逻辑的另一种简单解决方案是提供一种在bean创建期间由Spring调用的初始化方法。我们要做的就是将`@PostConstruct`注释添加到方法中：

    @Component
    @DependsOn("myApplicationListener")
    class MyPostConstructBean {
    
      private static final Logger logger = ...;
    
      @PostConstruct
      void postConstruct(){
        logger.info("@PostConstruct");
      }
    
    }
    

一旦`MyPostConstructBean`成功实例化类型的bean，Spring就会调用此方法。

该`@PostConstruct`方法是在Spring创建bean之后立即调用的，因此我们无法通过`@Order`注释自由地对其进行排序，因为它可能依赖于`@Autowired`我们bean中其他的Spring bean。

相反，它将在依赖于它的所有bean被初始化之后被调用。如果要添加人为的依赖关系并由此创建订单，则可以使用`@DependsOn`批注（与批注同样警告`@Order`！）。

**甲`@PostConstruct`方法固有地依赖于特定的Spring bean所以应该只用于该单个bean的初始化逻辑**。

对于全局初始化逻辑，一个`CommandLineRunner`，`ApplicationRunner`或`ApplicationListener`提供了一个更好的解决方案。

[](#initializingbean)`InitializingBean`
---------------------------------------

在效果上与`@PostConstruct`解决方案非常相似，我们可以实现`InitializingBean`接口并让Spring调用某种初始化方法：

    @Component
    class MyInitializingBean implements InitializingBean {
    
      private static final Logger logger = ...;
    
      @Override
      public void afterPropertiesSet() throws Exception {
        logger.info("InitializingBean#afterPropertiesSet()");
      }
    
    }
    

Spring将`afterPropertiesSet()`在应用程序启动期间调用该方法。顾名思义，我们可以确保Spring填充了bean的所有属性。如果我们`@Autowired`在某些属性上使用（我们不应该-应该使用[构造函数注入](/constructor-injection)），那么Spring将在调用之前将Bean注入到这些属性中`afterPropertiesSet()`\-与with相同`@PostConstruct`。

**对于这两者`InitializingBean`，`@PostConstruct`我们必须小心不要依赖于在另一个bean 的`afterPropertiesSet()`or `@PostConstruct`方法中已初始化的状态。该状态可能尚未初始化，并导致`NullPointerException`**。

如果可能的话，我们应该使用[构造函数注入](/constructor-injection)并初始化[构造](/constructor-injection)函数中所需的所有内容，因为这使这种错误成为不可能。

[](#conclusion)结论
-----------------

在Spring Boot应用程序启动期间，有多种执行代码的方法。尽管它们看上去很相似，但是每个人的行为略有不同或提供不同的功能，因此它们都有生存的权利。

我们可以通过`@Order`注释影响不同启动bean的顺序，但只能将其作为最后的手段，因为它在这些bean之间引入了难以掌握的逻辑依赖性。

如果您想查看所有正在使用的解决方案，请查看[GitHub存储库](https://github.com/thombergs/code-examples/tree/master/spring-boot/startup)。