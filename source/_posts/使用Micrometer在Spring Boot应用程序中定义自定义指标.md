---
title: 使用Micrometer在Spring Boot应用程序中定义自定义指标
id: 1424
date: 2024-10-31 22:01:55
author: daichangya
permalink: /archives/%E4%BD%BF%E7%94%A8micrometer%E5%9C%A8springboot%E5%BA%94%E7%94%A8%E7%A8%8B%E5%BA%8F%E4%B8%AD%E5%AE%9A%E4%B9%89%E8%87%AA%E5%AE%9A%E4%B9%89%E6%8C%87%E6%A0%87/
---

Spring Boot 2.0将大量新功能带入了我们最喜欢的Java框架。  
这些新功能之一是将测微计集成到Spring Boot Actuator中。  
Micrometer是一种维度度量和监视外观，帮助开发人员将其应用程序度量集成到各种监视系统中，同时使应用程序独立于实际的监视实现。
正如该项目的首页所述，它类似于SLF4J，但用于metrics准。

Micrometer
------

在深入探讨使用测微表定义自定义指标的细节之前，让我们花一些时间在此定义上。  
首先，我们说Micrometer是一个检测适配工具。  
真正的含义是，使用该库，您作为开发人员可以使用一种方式将您的度量标准传送到各种监视系统中。  
您可能会认为这没什么大不了的。  
好吧，是的。  
有很多用于监视应用程序的解决方案，每种解决方案都有不同的方法来满足您的监视需求。  
这些差异可能与它们使用的命名约定一样细微，或者甚至在收集数据的基本方法上也可能有所不同。  
在这里，在AutSoft，我们使用Prometheus轮询应用程序中的新数据，而不是依赖于推入模型的DataDog。  
Micrometer可以为您解决所有这些差异，因此您可以为所有这些解决方案使用统一的界面。

接下来，我们说Micrometer遵循维度方法，这意味着您可以使用任意数量的标签来标记指标。  
例如，如果您有一个度量标准来统计应用程序中的HTTP请求，则可以使用请求被击中的URI对其进行注释。  
一旦Prometheus收集了这些指标，您就可以看到请求的总数，还可以向下钻取并检查特定URI的请求数。

Micrometer和Spring
------

借助新版本的Spring Boot Actuator，Spring团队决定使用Micrometer来报告使用Micrometer框架的内置指标。  
（这并不奇怪，因为他们首先是开发图书馆的人...）

要在现有的Spring Boot 2应用程序中检查这些指标，您实际上不需要做很多工作。  
就像导入Spring Boot Actuator和Micrometer依赖项并进行一些配置一样简单。  
首先，将以下行添加到您`pom.xml`的`dependencies`部分：

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>
    
    <dependency>
        <groupId>io.micrometer</groupId>
        <artifactId>micrometer-core</artifactId>
    </dependency>
    
    <dependency>
        <groupId>io.micrometer</groupId>
        <artifactId>micrometer-registry-prometheus</artifactId>
    </dependency>
    

然后，将以下配置粘贴到`application.properties`（或`application.yml`）文件中以显示Prometheus抓取端点：

    management.endpoints.web.exposure.include=prometheus
    

现在，如果启动应用程序并打开`http://localhost:8080/actuator/prometheus`端点，您将看到Actuator已经导出的大量指标。  
如果您看一下前几行，您已经可以看到Micrometer和Prometheus的尺寸方法在起作用：

    # HELP logback_events_total Number of error level events that made it to the logs
    # TYPE logback_events_total counter
    logback_events_total{level="warn",} 0.0
    logback_events_total{level="debug",} 0.0
    logback_events_total{level="error",} 0.0
    logback_events_total{level="trace",} 0.0
    logback_events_total{level="info",} 7.0
    

指标的名称是，`logback_events_total`但是有一个标签（或维度）被调用`level`来帮助您进行深入分析，并准确检查每个日志记录级别发生了多少事件。

定义您的自定义指标
---------

现在，让我们使用Micrometer和Spring Boot定义和导出我们自己的自定义指标。  
为此，我们将使用我们最喜欢的示例，`BeerService`我们将对其进行彻底监视。  
（您应该始终注意啤酒，不是吗？）

首先，我们需要保留ApplicationContext的`MeterRegistry`实例：

    import io.micrometer.core.instrument.MeterRegistry;
    import org.springframework.stereotype.Component;
    
    @Component
    public class BeerService {
    
        private MeterRegistry meterRegistry;
    
        public BeerService(MeterRegistry meterRegistry) {
            this.meterRegistry = meterRegistry;
        }
    }
    

该`MeterRegistry`负责收集和管理应用程序的meters。

### 定义计数器

指标的最基本类型是计数器。  
计数器用于报告代表计数的单个数字。

在我们的示例中，我们将报告进入我们的订单数量`BeerService`：

    private void initOrderCounters() {
        lightOrderCounter = this.meterRegistry.counter("beer.orders", "type", "light"); // 1 - create a counter
        aleOrderCounter = Counter.builder("beer.orders")    // 2 - create a counter using the fluent API
                .tag("type", "ale")
                .description("The number of orders ever placed for Ale beers")
                .register(meterRegistry);
    }
    
    void orderBeer(Order order) {
        orders.add(order);
    
        if ("light".equals(order.type)) {
            lightOrderCounter.increment(1.0);  // 3 - increment the counter
        } else if ("ale".equals(order.type)) {
            aleOrderCounter.increment();
        }
    }
    

让我们看看这里发生了什么：

1.  我们可以使用创建计数器`meterRegistry`。创建的指标将自动注册到注册表。
2.  创建指标的更简洁的方法是使用流畅的Builder API。
3.  计数器可以增加一个或任何正数。

剩下要做的唯一一件事就是实际订购一些啤酒。  
将以下行粘贴到Application类中，然后启动应用程序：

    @SpringBootApplication
    public class MicrometerApplication {
    
        public static void main(String[] args) {
            SpringApplication.run(MicrometerApplication.class, args);
        }
    
        private BeerService beerService;
    
        public MicrometerApplication(BeerService beerService) {
            this.beerService = beerService;
        }
    
        @EventListener(ApplicationReadyEvent.class)
        public void orderBeers() {
            Flux.interval(Duration.ofSeconds(2))
                    .map(MicrometerApplication::toOrder)
                    .doOnEach(o -> beerService.orderBeer(o.get()))
                    .subscribe();
        }
    
        private static Order toOrder(Long l) {
            double amount = l % 5;
            String type = l % 2 == 0 ? "ale" : "light";
            return new Order(amount, type);
        }
    
    }
    

现在，如果您`http://localhost:8080/actuator/prometheus`在浏览器中打开该URL ，则可以在几行中找到我们的新指标：

    # HELP beer_orders_total  
    # TYPE beer_orders_total counter
    beer_orders_total{type="light",} 5.0
    beer_orders_total{type="ale",} 6.0
    

恭喜，我们已经使用Micrometer定义了第一个计数器指标！

### 定义Gauge

接下来，让我们看一下Gauges。  
量表也代表单个数值，但有一些显着差异。  
首先，计数器存储单调递增的值，而Gauge的值也可以递减。  
其次，Gauge的值仅在观察时才会更改，我们不会像在前面的示例中那样手动对其进行递增。  
相反，如果需要，我们提供了一个获取Gauge当前值的函数。  
此行为还意味着两次观察之间发生的任何事件都将丢失。

通常，建议对具有上限的值使用量表，不建议对计数器可表示的量度使用量表。

在我们的示例中，我们将`order`使用仪表监视列表的大小。  
（即使我们当前的“业务逻辑”并未对此列表实施上限，但我们假设我们可以处理的最大订单数量，除此以外的数量也将更多。）

扩展您`BeerService`的的构造函数，如下所示：

    public BeerService(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        initOrderCounters();
        Gauge.builder("beer.ordersInQueue", orders, Collection::size)
                .description("Number of unserved orders")
                .register(meterRegistry);
    }
    

同样，如果重新启动应用程序并`http://localhost:8080/actuator/prometheus`在浏览器中检查URL，则应找到`beer.ordersInQueue`指标：

    # HELP beer_ordersInQueue Number of unserved orders
    # TYPE beer_ordersInQueue gauge
    beer_ordersInQueue 9.0
    

### 定义计时器

计时器具有两个功能，它测量某些事件（通常是方法执行）的时间，并同时对这些事件进行计数。  
如果您曾经维护或开发过Web应用程序，则很可能希望检查服务器的响应时间。  
这种用例是计时器最典型的用例。

计时器具有许多有用的功能，但我们只专注于测量给定方法的执行时间。  
在Spring中，配置Micrometer提供的Aspect 后可以使用`micrometer-core`的`@Timed`注释`TimedAspect`。  
将以下代码行放入Application类（或任何`@Configuration`类）中：

    @Bean
    public TimedAspect timedAspect(MeterRegistry registry) {
        return new TimedAspect(registry);
    }
    

（确保导入`spring-boot-starter-aop`Maven依赖关系。）

然后，在中创建一个方法`BeerService`以服务`orders`列表中的第一顺序：

    @Scheduled(fixedRate = 5000)
    @Timed(description = "Time spent serving orders")
    public void serveFirstOrder() throws InterruptedException {
        if (!orders.isEmpty()) {
            Order order = orders.remove(0);
            Thread.sleep(1000L * order.amount);
        }
    }
    

（要使`@Scheduled`注释生效，您需要使用注释应用程序或任何其他Configuration类`@EnableScheduling`。）

现在，如果启动该应用程序，您将找到以下导出到Prometheus的指标：

    # HELP method_timed_seconds Time spent serving orders
    # TYPE method_timed_seconds summary
    method_timed_seconds_count{class="com.demo.micrometer.BeerService",exception="none",method="serveFirstOrder",} 8.0
    method_timed_seconds_sum{class="com.demo.micrometer.BeerService",exception="none",method="serveFirstOrder",} 11.041940917
    # HELP method_timed_seconds_max Time spent serving orders
    # TYPE method_timed_seconds_max gauge
    method_timed_seconds_max{class="com.demo.micrometer.BeerService",exception="none",method="serveFirstOrder",} 4.003256321
    

您可以看到我们的应用程序在11.04秒内处理了8个订单，每个订单最多处理4秒。

在事件执行尚未完成之前，计时器通常不会报告测量的时间。  
如果您有很长的任务要在它们仍在运行时进行测量，请使用如下`@Timed`注释：

    @Timed(description = "Time spent serving orders", longTask = true)
    

摘要和下一步去
-------

在本文中，我们了解了Micrometer的基础知识，它与Spring Boot Actuator集成在一起，为了使事情变得更加令人兴奋，我们在Spring Boot应用程序中定义了自己的指标。

现在，您已经知道了测微仪的基础知识，但仍有很多需要探索的地方。  
我建议您查看[Micrometer文档](http://micrometer.io/docs/concepts)的“ [概念”页面](http://micrometer.io/docs/concepts)和/或在SpringOne Platform上观看Jon Schneider 关于Micrometer 的[演示](https://www.youtube.com/watch?v=HIUoeLYWo7o&t=2272s)。

在本文中，我们没有介绍所定义指标的可视化。  
为此，我们将[Prometheus](https://prometheus.io/)与[Grafana结合](https://grafana.com/)使用，因为它们非常适合我们的用例。

可以在我们的[GitHub页面](https://github.com/AutSoft/micrometer-demo)上找到本指南的源代码。

如果您喜欢这篇文章或有任何疑问，请不要在下面发表评论。

资料来源
----

*   [Micrometer：Spring Boot 2的新应用程序指标收集器](https://spring.io/blog/2018/03/16/micrometer-spring-boot-2-s-new-application-metrics-collector)
*   [Spring Boot参考指南-指标](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#production-ready-metrics)
*   [Micrometer文档-概念](https://micrometer.io/docs/concepts)
*   [Micrometer应用指标介绍-Jon Schneider](https://www.youtube.com/watch?v=HIUoeLYWo7o&t=2272s)