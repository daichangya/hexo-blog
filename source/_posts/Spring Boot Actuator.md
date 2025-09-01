---
title: Spring Boot Actuator
id: 1435
date: 2024-10-31 22:01:55
author: daichangya
excerpt: "1.概述在本文中,我们将介绍SpringBootActuator.**我们将首先介绍基础知识,然后详细讨论SpringBoot2.x和1.x中的可用内容.**我们将学习如何利用反应式编程模型在SpringBoot2.x和WebFlux中使用,配置和扩展此监视工具.然后,我们将讨论如何使用Boot1."
permalink: /archives/springbootactuator/
tags: 
 - springboot
---

## **1.概述**

在本文中,我们将介绍Spring Boot Actuator.  **我们将首先介绍基础知识,然后详细讨论Spring Boot 2.x和1.x中的可用内容.**

我们将学习如何利用反应式编程模型在Spring Boot 2.x和WebFlux中使用,配置和扩展此监视工具. 然后,我们将讨论如何使用Boot 1.x执行相同的操作. 

自2014年4月起,Spring Boot Actuator随Spring Boot一起发布. 

随着Spring Boot 2,对Actuator进行了重新设计,并添加了新的令人兴奋的Endpoints. 

我们将本指南分为三个主要部分:

*   [What is an Actuator?]
*   [Spring Boot 2.x Actuator]
*   [Spring Boot 1.x Actuator]

## 2. What is an Actuator?

本质上,Actuator为我们的应用带来了生产就绪功能. 

**监视我们的应用程序,收集指标,了解流量或数据库状态对于这种依赖性变得微不足道.**

该库的主要好处是,我们可以获得生产级工具,而不必自己真正实现这些功能. 

Actuator主要用于**公开有关正在运行的应用程序的操作信息** \- **运行**状况,指标,信息,转储,环境等. 它使用HTTPEndpoints或JMX Bean使我们能够与其交互. 

一旦此依赖关系位于类路径上,便可以立即使用几个Endpoints. 与大多数Spring模块一样,我们可以通过多种方式轻松地对其进行配置或扩展. 

### **2.1. 入门**

要启用Spring Boot Actuator,我们只需要将*spring-boot-actuator*依赖项添加到我们的包管理器中即可. 在Maven中:



```
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

请注意,这与Boot版本无关,因为Spring Boot材料清单(BOM)中已指定版本. 

## 3. Spring Boot 2.x Actuator

在2.x中,Actuator保留了其基本意图,但简化了其模型,扩展了其功能并合并了更好的默认设置. 

首先,该版本与技术无关. 此外,它通过与应用程序合并来简化其安全模型. 

最后,在各种更改中,请务必记住其中一些正在中断. 这包括HTTP请求和响应以及Java API. 

此外,与旧的读/写模型相比,最新版本现在支持CRUD模型. 

### **3.1. 技术支持**

在第二个主要版本中,Actuator现在与技术无关,而在1.x中,它与MVC关联,因此与Servlet API关联. 

在2.x中,Actuator定义了其模型,可插入且可扩展,而无需依赖MVC. 

**因此,通过这种新模型,我们能够利用MVC和WebFlux作为基础Web技术.**

而且,可以通过实现正确的适配器来添加即将到来的技术. 

最后,仍然支持JMX公开Endpoints,而无需任何其他代码. 

### **3.2. 重要变化**

与以前的版本不同,**Actuator禁用了大多数Endpoints**. 

因此,默认情况下唯一可用的两个是/health*和/info*. 

如果要启用所有这些功能,可以设置*management.endpoints.web.exposure.include = *. *或者,我们可以列出应启用的Endpoints. 

**现在,Actuator与常规App安全规则共享安全配置. 因此,极大地简化了安全模型.**

因此,要调整Actuator安全性规则,我们可以为/actuator/**添加一个条目:



```
@Bean
public SecurityWebFilterChain securityWebFilterChain(
  ServerHttpSecurity http) {
    return http.authorizeExchange()
      .pathMatchers("/actuator/**").permitAll()
      .anyExchange().authenticated()
      .and().build();
}
```

我们可以在[全新的Actuator官方文档中](https://docs.spring.io/spring-boot/docs/2.0.x/actuator-api/html/)找到更多详细信息. 

另外,**默认情况下,所有ActuatorEndpoints现在都放在/actuator*路径下*.***

与以前的版本相同,我们可以使用新的属性*management.endpoints.web.base-path*来调整此*路径. *

### **3.3. 预定义Endpoints**

让我们看一下一些可用的Endpoints,其中大多数已经在1.x中可用. 

尽管如此,**还是添加了一些Endpoints,删除了一些Endpoints,并重新**构造了**一些Endpoints:**

*   /auditevents –列出与安全审核相关的事件,例如用户登录/注销. 此外,我们可以在其他字段中按主体或类型进行过滤
*   /beans –返回*BeanFactory中*所有可用的bean . 与/auditevents*不同,它不支持过滤
*   /conditions –以前称为/ *autoconfig*,围绕自动配置生成条件报告
*   /configprops –允许我们获取所有*@ConfigurationProperties* bean
*   /env –返回当前环境属性. 此外,我们可以检索单个属性
*   /flyway –提供有关我们的Flyway数据库迁移的详细信息
*  /health –总结我们应用程序的健康状态
*   /heapdump –从我们的应用程序使用的JVM构建并返回堆转储
*  /info –返回常规信息. 它可能是自定义数据,构建信息或有关最新提交的详细信息
*   /liquibase – behaves like /flyway but for Liquibase
*   /logfile –返回普通的应用程序日志
*   /loggers –使我们能够查询和修改应用程序的日志记录级别
*   /metrics –详细说明我们应用程序的指标. 这可能包括一般指标和自定义指标
*   /prometheus –返回与上一个相似的指标,但其格式可以与Prometheus服务器一起使用
*   /scheduledtasks –提供有关我们应用程序中每个计划任务的详细信息
*   /sessions –列出我们正在使用Spring Session的HTTP会话
*   /shutdown –正常关闭应用程序
*   /threaddump –转储底层JVM的线程信息

### **3.4. 健康指标**

就像以前的版本一样,我们可以轻松添加自定义指标. 与其他API相反,用于创建自定义健康状况终结点的抽象保持不变. 但是,添加**了新接口*ReactiveHealthIndicator*来实现反应式健康检查**. 

让我们看一个简单的自定义反应式健康检查:



```
@Component
public class DownstreamServiceHealthIndicator implements ReactiveHealthIndicator {
 
    @Override
    public Mono<Health> health() {
        return checkDownstreamServiceHealth().onErrorResume(
          ex -> Mono.just(new Health.Builder().down(ex).build())
        );
    }
 
    private Mono<Health> checkDownstreamServiceHealth() {
        // we could use WebClient to check health reactively
        return Mono.just(new Health.Builder().up().build());
    }
}
```

**健康指标的一个方便功能是我们可以将它们汇总为层次结构的一部分.**因此,根据前面的示例,我们可以将所有下游服务归为“ *下游**服务”*类别. 只要可以访问每个嵌套*服务*,此类别就很正常. 

复合健康检查通过*CompositeHealthIndicator*在1.x中进行*. *另外,在2.x中,我们可以将*CompositeReactiveHealthIndicator*用作其反应性对象. 

与Spring Boot 1.x中的*Endpoints不同. *<id>. *敏感*标志已被删除. 要隐藏完整的健康报告,我们可以利用新的*management.endpoint.health.show-details. *默认情况下,此标志为false. 

### **3.5. Spring Boot 2中的指标**

**在Spring Boot 2.0中,内部指标已被Micrometer支持所取代.**因此,我们可以期待重大的变化. 如果我们的应用程序使用的是度量服务,例如*GaugeService或CounterService,则*它们将不再可用. 

相反,我们应该直接与[Micrometer](https://www.baeldung.com/micrometer)进行交互. 在Spring Boot 2.0中,我们将获得为我们自动配置的*MeterRegistry*类型的Bean . 

此外,千分尺现在已成为Actuator依赖项的一部分. 因此,只要Actuator依赖项在类路径中,我们就应该很好. 

此外,我们将从/metrics*Endpoints获得全新的响应*:*



```
{
  "names": [
    "jvm.gc.pause",
    "jvm.buffer.memory.used",
    "jvm.memory.used",
    "jvm.buffer.count",
    // ...
  ]
}
```

正如我们在前面的示例中所观察到的,没有像1.x那样的实际指标. 

要获取特定指标的实际值,我们现在可以导航到所需指标,即*/actuator/metrics/jvm.gc.pause*并获得详细的响应:



```
{
  "name": "jvm.gc.pause",
  "measurements": [
    {
      "statistic": "Count",
      "value": 3.0
    },
    {
      "statistic": "TotalTime",
      "value": 7.9E7
    },
    {
      "statistic": "Max",
      "value": 7.9E7
    }
  ],
  "availableTags": [
    {
      "tag": "cause",
      "values": [
        "Metadata GC Threshold",
        "Allocation Failure"
      ]
    },
    {
      "tag": "action",
      "values": [
        "end of minor GC",
        "end of major GC"
      ]
    }
  ]
}
```

如我们所见,指标现在更加全面. 不仅包括不同的值,还包括一些相关的元数据. 

### **3.6. 自定义/info Endpoints**

该*/info*Endpoints保持不变.**和以前一样,我们可以使用Maven或Gradle各自的依赖项添加git详细信息**:



```
<dependency>
    <groupId>pl.project13.maven</groupId>
    <artifactId>git-commit-id-plugin</artifactId>
</dependency>
```

同样,**我们也可以使用Maven或Gradle插件来包含构建信息,包括名称,组和版本:**



```
<plugin>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-maven-plugin</artifactId>
    <executions>
        <execution>
            <goals>
                <goal>build-info</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

### **3.7. 创建自定义Endpoints**

如前所述,我们可以创建自定义Endpoints. 但是,Spring Boot 2重新设计了实现此目标的方法,以支持与技术无关的新范例. 

**让我们创建一个ActuatorEndpoints来查询,启用和禁用应用程序中的功能标志**:



```
@Component
@Endpoint(id = "features")
public class FeaturesEndpoint {
 
    private Map<String, Feature> features = new ConcurrentHashMap<>();
 
    @ReadOperation
    public Map<String, Feature> features() {
        return features;
    }
 
    @ReadOperation
    public Feature feature(@Selector String name) {
        return features.get(name);
    }
 
    @WriteOperation
    public void configureFeature(@Selector String name, Feature feature) {
        features.put(name, feature);
    }
 
    @DeleteOperation
    public void deleteFeature(@Selector String name) {
        features.remove(name);
    }
 
    public static class Feature {
        private Boolean enabled;
 
        // [...] getters and setters
    }
 
}
```

为了获得Endpoints,我们需要一个bean. 在我们的示例中,我们为此使用*@Component*. 另外,我们需要使用*@Endpoint*装饰该bean . 

Endpoints的路径由*@Endpoint*的*id*参数确定,在本例中,它将把请求路由到/actuator/features. *

准备就绪后,我们可以使用以下方法开始定义操作:

*   *@ReadOperation –它将映射到HTTP *GET*
*   *@WriteOperation* –它将映射到HTTP *POST*
*   *@DeleteOperation* –它将映射到HTTP *DELETE*

当我们使用应用程序中的上一个Endpoints运行该应用程序时,Spring Boot将对其进行注册. 

一种快速的验证方法是检查日志:



```
[...].WebFluxEndpointHandlerMapping: Mapped "{[/actuator/features/{name}],
  methods=[GET],
  produces=[application/vnd.spring-boot.actuator.v2+json || application/json]}"
[...].WebFluxEndpointHandlerMapping : Mapped "{[/actuator/features],
  methods=[GET],
  produces=[application/vnd.spring-boot.actuator.v2+json || application/json]}"
[...].WebFluxEndpointHandlerMapping : Mapped "{[/actuator/features/{name}],
  methods=[POST],
  consumes=[application/vnd.spring-boot.actuator.v2+json || application/json]}"
[...].WebFluxEndpointHandlerMapping : Mapped "{[/actuator/features/{name}],
  methods=[DELETE]}"[...]
```

在以前的日志中,我们可以看到WebFlux如何公开我们的新Endpoints. 我们将切换到MVC,它将简单地委托该技术,而无需更改任何代码. 

此外,对于这种新方法,我们需要牢记一些重要的注意事项:

*   MVC没有依赖关系
*   之前(*敏感,已启用...)*作为方法存在的所有元数据都不再存在. 但是,我们可以使用*@Endpoint(id =“ features”,enableByDefault = false)*启用或禁用Endpoints. 
*   与1.x不同,不再需要扩展给定的接口
*   与旧的读取/写入模型相反,现在我们可以使用*@DeleteOperation*定义*DELETE*操作

### **3.8. 扩展现有Endpoints**

假设我们要确保应用程序的生产实例绝不是*SNAPSHOT*版本. 我们决定通过更改返回此信息的ActuatorEndpoints的HTTP状态代码(即/info)来*执行此操作*. *如果我们的应用恰巧是*SNAPSHOT*. 我们将获得不同的*HTTP*状态代码. 

**我们可以使用@EndpointExtension批注**或其更具体的专长@EndpointWebExtension或@EndpointJmxExtension **轻松扩展预定义Endpoints的行为***:*



```
@Component
@EndpointWebExtension(endpoint = InfoEndpoint.class)
public class InfoWebEndpointExtension {
 
    private InfoEndpoint delegate;
 
    // standard constructor
 
    @ReadOperation
    public WebEndpointResponse<Map> info() {
        Map<String, Object> info = this.delegate.info();
        Integer status = getStatus(info);
        return new WebEndpointResponse<>(info, status);
    }
 
    private Integer getStatus(Map<String, Object> info) {
        // return 5xx if this is a snapshot
        return 200;
    }
}
```

### **3.9. 启用所有Endpoints**

**为了使用HTTP访问ActuatorEndpoints,我们需要同时启用和公开它们**. 默认情况下,除/shutdown之外的*所有Endpoints均处于启用状态. 只有 */health*和*/info*Endpoints默认情况下暴露出来. 

我们需要添加以下配置以公开所有Endpoints:



```
management.endpoints.web.exposure.include=*
```

要显式启用特定Endpoints(例如 /shutdown), *我们使用:



```
management.endpoint.shutdown.enabled=true
```

要公开除一个(例如/loggers*)以外的所有启用的Endpoints,我们使用:



```
management.endpoints.web.exposure.include=*
management.endpoints.web.exposure.exclude=loggers
```

## 4. Spring Boot 1.x Actuator

在1.x中,Actuator遵循R/W模型,这意味着我们可以对其进行读取或写入. 例如,我们可以检索指标或应用程序的运行状况. 另外,我们可以优雅地终止我们的应用程序或更改日志记录配置. 

为了使其工作,Actuator要求Spring MVC通过HTTP公开其Endpoints. 不支持其他技术. 

### 4.1. Endpoints

**在1.x中,Actuator带来了自己的安全模型. 它利用了Spring Security构造,但是需要与应用程序的其余部分独立配置.**

另外,大多数Endpoints都是敏感的,这意味着它们不是完全公开的,换句话说,大多数信息将被省略,而少数Endpoints不是例如/info*. 

以下是Boot提供的一些最常见的Endpoints:

*  /health* –显示应用程序健康信息(通过未经身份验证的连接访问时为简单的*“状态”*,或通过身份验证时显示为完整的消息详细信息);默认情况下不敏感
*  /info –显示任意应用程序信息;默认不敏感
*   /metrics –显示当前应用程序的“指标”信息;默认情况下也很敏感
*   /trace –显示跟踪信息(默认情况下,最后几个HTTP请求)

我们可以[在官方文档中](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#production-ready-endpoints)找到现有Endpoints的完整列表. 

### **4.2. 配置现有Endpoints**

我们可以使用以下格式,使用属性来自定义每个Endpoints:*endpoints. \[endpoint name\]. \[property to custom\]*

提供三个属性:

*   *id –将通过HTTP访问该Endpoints
*   *已启用* –如果为true,则可以访问,否则不能访问
*   *敏感* –如果为true,则需要授权以通过HTTP显示关键信息

例如,添加以下属性将自定义/ *bean*Endpoints*:  
*



```
endpoints.beans.id=springbeans
endpoints.beans.sensitive=false
endpoints.beans.enabled=true
```

### **4.3./health Endpoints**

**该*/health*Endpoints用于检查运行的应用程序的运行状况或状态.**监视软件通常会执行此操作,以警告我们正在运行的实例出现故障或由于其他原因而变得不正常. 例如,数据库的连接问题,磁盘空间不足…

默认情况下,未经授权的用户只能通过HTTP访问时看到状态信息:



```
{
    "status" : "UP"
}
```

此健康信息是从在我们的应用程序上下文中配置的,实现了*HealthIndicator*接口的所有bean收集的. 

*HealthIndicator*返回的某些信息本质上是敏感的–但是我们可以配置*endpoints.health.sensitive = false*来显示更多详细信息,例如磁盘空间,消息传递代理连接,自定义检查等等. 请注意,这仅适用于1.5.0以下的Spring Boot版本. 对于1.5.0及更高版本,我们还应该通过将*management.security.enabled = false*设置为未经授权的访问来禁用安全性. 

我们还可以**实现自己的自定义运行状况指示器** -可以收集特定于应用程序的任何类型的自定义运行状况数据,并通过/health*Endpoints自动将其公开:



```
@Component("myHealthCheck")
public class HealthCheck implements HealthIndicator {
  
    @Override
    public Health health() {
        int errorCode = check(); // perform some specific health check
        if (errorCode != 0) {
            return Health.down()
              .withDetail("Error Code", errorCode).build();
        }
        return Health.up().build();
    }
     
    public int check() {
        // Our logic to check health
        return 0;
    }
}
```

输出结果如下所示:



```
{
    "status" : "DOWN",
    "myHealthCheck" : {
        "status" : "DOWN",
        "Error Code" : 1
     },
     "diskSpace" : {
         "status" : "UP",
         "free" : 209047318528,
         "threshold" : 10485760
     }
}
```

### **4.4./info Endpoints**

我们还可以自定义/info*Endpoints显示的数据-例如:



```
info.app.name=Spring Sample Application
info.app.description=This is my first spring boot application
info.app.version=1.0.0
```

以及示例输出:



```
{
    "app" : {
        "version" : "1.0.0",
        "description" : "This is my first spring boot application",
        "name" : "Spring Sample Application"
    }
}
```

### **4.5. /metrics Endpoints**

**指标终结点发布有关OS,JVM以及应用程序级别指标的信息**. 启用后,我们将获得诸如内存,堆,处理器,线程,已加载类,已卸载类,线程池以及一些HTTP指标之类的信息. 

以下是该Endpoints的输出结果:



```
{
    "mem" : 193024,
    "mem.free" : 87693,
    "processors" : 4,
    "instance.uptime" : 305027,
    "uptime" : 307077,
    "systemload.average" : 0.11,
    "heap.committed" : 193024,
    "heap.init" : 124928,
    "heap.used" : 105330,
    "heap" : 1764352,
    "threads.peak" : 22,
    "threads.daemon" : 19,
    "threads" : 22,
    "classes" : 5819,
    "classes.loaded" : 5819,
    "classes.unloaded" : 0,
    "gc.ps_scavenge.count" : 7,
    "gc.ps_scavenge.time" : 54,
    "gc.ps_marksweep.count" : 1,
    "gc.ps_marksweep.time" : 44,
    "httpsessions.max" : -1,
    "httpsessions.active" : 0,
    "counter.status.200.root" : 1,
    "gauge.response.root" : 37.0
}
```

**为了收集自定义指标,我们支持“仪表”(即数据的单值快照)和“计数器”(即递增/递减指标).**

让我们在/metrics*Endpoints中实现我们自己的自定义指标. 例如,我们将自定义登录流程以记录成功和失败的登录尝试:



```
@Service
public class LoginServiceImpl {
 
    private final CounterService counterService;
     
    public LoginServiceImpl(CounterService counterService) {
        this.counterService = counterService;
    }
     
    public boolean login(String userName, char[] password) {
        boolean success;
        if (userName.equals("admin") && "secret".toCharArray().equals(password)) {
            counterService.increment("counter.login.success");
            success = true;
        }
        else {
            counterService.increment("counter.login.failure");
            success = false;
        }
        return success;
    }
}
```

输出内容如下所示:



```
{
    ...
    "counter.login.success" : 105,
    "counter.login.failure" : 12,
    ...
}
```

请注意,登录尝试和其他与安全性相关的事件都可以作为审计事件在Actuator中直接使用. 

### **4.6. 创建一个新Endpoints**

**除了使用Spring Boot提供的现有Endpoints之外,我们还可以创建一个全新的Endpoints.**

首先,我们需要让新的Endpoints实现*Endpoint <T>*接口:



```
@Component
public class CustomEndpoint implements Endpoint<List<String>> {
     
    @Override
    public String getId() {
        return "customEndpoint";
    }
 
    @Override
    public boolean isEnabled() {
        return true;
    }
 
    @Override
    public boolean isSensitive() {
        return true;
    }
 
    @Override
    public List<String> invoke() {
        // Custom logic to build the output
        List<String> messages = new ArrayList<String>();
        messages.add("This is message 1");
        messages.add("This is message 2");
        return messages;
    }
}
```

为了访问此新Endpoints,使用其*ID*对其进行映射,即,可以按/customEndpoint对其进行练习*. 

输出:



```
[ "This is message 1", "This is message 2" ]
```

### **4.7. 进一步定制**

为了安全起见,我们可能选择通过非标准端口公开ActuatorEndpoints\- 可以轻松地使用*management.port*属性进行配置. 

同样,正如我们已经提到的,在1.x中. Actuator基于Spring Security配置其自己的安全模型,但与应用程序的其余部分无关.   
因此,我们可以更改*management.address*属性以限制可以通过网络访问Endpoints的位置:



```
#port used to expose actuator
management.port=8081
 
#CIDR allowed to hit actuator
management.address=127.0.0.1
 
#Whether security should be enabled or disabled altogether
management.security.enabled=false
```

此外,默认情况下,除/info*外的所有内置终结点都是敏感的. 如果应用程序使用的是Spring Security,我们可以通过在application.properties文件中定义默认的安全属性(用户名,密码和角色)来保护这些Endpoints:



```
security.user.name=admin
security.user.password=secret
management.security.role=SUPERUSER
```

## **5.总结**

在本文中,我们讨论了Spring Boot Actuator. 我们开始定义Actuator的含义及其对我们的作用. 
