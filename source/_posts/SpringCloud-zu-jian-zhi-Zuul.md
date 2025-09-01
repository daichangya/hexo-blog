---
title: SpringCloud组件之Zuul
id: 1511
date: 2024-10-31 22:01:59
author: daichangya
excerpt: Zuul是Netflix开源的微服务网关，可以和Eureka、Ribbon、Hystrix等组件配合使用，SpringCloud对Zuul进行了整合与增强，Zuul默认使用的HTTP客户端是ApacheHTTPClient，也可以使用RestClient或okhttp3.OkHttpClient。Z
permalink: /archives/SpringCloud-zu-jian-zhi-Zuul/
categories:
- spring-cloud
---


Zuul是Netflix开源的微服务网关，可以和Eureka、Ribbon、Hystrix等组件配合使用，Spring Cloud对Zuul进行了整合与增强，Zuul默认使用的HTTP客户端是Apache HTTPClient，也可以使用RestClient或okhttp3.OkHttpClient。 Zuul的主要功能是路由转发和过滤器。路由功能是微服务的一部分，比如／demo/test转发到到demo服务。zuul默认和Ribbon结合实现了负载均衡的功能

### 本文介绍zuul的工作原理和如何搭建zuul服务以及介绍相关知识点

### 一、工作原理

**zuul的核心是一系列的filters, 其作用类比Servlet框架的Filter，或者AOP。zuul把请求路由到用户处理逻辑的过程中，这些filter参与一些过滤处理，比如Authentication，Load Shedding等**  

![image.png](https://images.jsdiff.com/image_1604566282550.png)

#### Zuul使用一系列不同类型的过滤器，使我们能够快速灵活地将功能应用于我们的边缘服务。这些过滤器可帮助我们执行以下功能

*   身份验证和安全性 \- 确定每个资源的身份验证要求并拒绝不满足这些要求的请求
*   洞察和监控 \- 在边缘跟踪有意义的数据和统计数据，以便为我们提供准确的生产视图
*   动态路由 \- 根据需要动态地将请求路由到不同的后端群集
*   压力测试 \- 逐渐增加群集的流量以衡量性能。
*   Load Shedding - 为每种类型的请求分配容量并删除超过限制的请求
*   静态响应处理 \- 直接在边缘构建一些响应，而不是将它们转发到内部集群

#### 过滤器的生命周期

![image.png](https://images.jsdiff.com/image_1604566300874.png)

### 二、zuul组件

*   zuul-core--zuul核心库，包含编译和执行过滤器的核心功能
*   zuul-simple-webapp--zuul Web应用程序示例，展示了如何使用zuul-core构建应用程序
*   zuul-netflix--lib包，将其他NetflixOSS组件添加到Zuul中，例如使用功能区进去路由请求处理
*   zuul-netflix-webapp--webapp，它将zuul-core和zuul-netflix封装成一个简易的webapp工程包

### 三、搭建一个注册Eureka中心的Web服务

#### 1、导入依赖

```xml  language-xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>

```

#### 2、启动类

```java  language-java
/**
 * @author Gjing
 */
@SpringBootApplication
@EnableEurekaClient
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}

```

#### 3、配置文件

```yaml  language-yaml
server:
  port: 8090
spring:
  application:
    name: demo
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/

```

#### 4、提供接口外部访问

```java  language-java
/**
 * @author Gjing
 **/
@RestController
public class TestController {

    @GetMapping("/test")
    public ResponseEntity test() {
        return ResponseEntity.ok("ok");
    }
}

```

### 四、搭建Zuul服务

#### 1、导入zuul和eureka依赖

```xml  language-xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-zuul</artifactId>
</dependency>

```

#### 2、启动类标注注解

```java  language-java
/**
 * @author Gjing
 */
@SpringBootApplication
@EnableZuulProxy
@EnableEurekaClient
public class ZuulApplication {
    public static void main(String[] args) {
        SpringApplication.run(ZuulApplication.class, args);
    }
}

```

#### 3、配置文件

##### a、使用Eureka负载路由方式

```yaml  language-yaml
server:
  port: 8080
spring:
  application:
    name: zuul
# 配置Eureka地址
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
# 构建路由地址
zuul:
  routes:
    # 这里可以自定义
    demo2:
      # 匹配的路由规则
      path: /demo/**
      # 路由的目标服务名
      serviceId: demo

```

#### b、不使用eureka负载方式路由，采取请求地址路由

```yaml  language-yaml
server:
  port: 8080
spring:
  application:
    name: zuul
# 配置eureka地址
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
# 构建路由地址
zuul:
  routes:
    # 这里可以自定义
    demo2:
      # 匹配的路由规则
      path: /demo/**
      # 路由的目标服务名
      url: demo
# 关闭使用eureka负载路由
ribbon:
  eureka:
    enabled: false
# 如果不使用eureka的话，需要自己定义路由的那个服务的其他负载服务
demo:
  ribbon:
    # 这里写你要路由的demo服务的所有负载服务请求地址，本项目只启动一个，因此只写一个
    listOfServers: http://localhost:8090/

```

##### c、如果不想依赖于Eureka使用zuul，那么可使用以下配置方式

```yaml  language-yaml
server:
  port: 8080
spring:
  application:
    name: zuul
# 构建路由地址
zuul:
  routes:
    # 这里可以自定义
    demo2:
      # 匹配的路由规则
      path: /demo/**
      # 路由的目标地址
      url: http://localhost:8090/

```

#### 4、启动项目并访问即可

`http://localhost:8080/demo/test`

### 五、使用Zuul过滤器

为了让api网关组件可以被更方便的使用，它在http请求生命周期的各个阶段默认实现了一批核心过滤器，它们会在api网关服务启动的时候被自动加载和启动。我们可以在源码中查看和了解它们，它们定义与spring-cloud-netflix-core模块的org.springframework.cloud.netflix.zuul.filters包下。在默认启动的过滤器中包含三种不同生命周期的过滤器，这些过滤器都非常重要，可以帮组我们理解zuul对外部请求处理的过程，以及帮助我们在此基础上扩展过滤器去完成自身系统需要的功能

#### 1、pre过滤器

*   **ServletDetectionFilter**

> ServletDetectionFilter：它的执行顺序为-3，是最先被执行的过滤器。该过滤器总是会被执行，主要用来检测当前请求是通过Spring的DispatcherServlet处理运行的，还是通过ZuulServlet来处理运行的。它的检测结果会以布尔类型保存在当前请求上下文的isDispatcherServletRequest参数中，这样后续的过滤器中，我们就可以通过RequestUtils.isDispatcherServletRequest()和RequestUtils.isZuulServletRequest()方法来判断请求处理的源头，以实现后续不同的处理机制。一般情况下，发送到api网关的外部请求都会被Spring的DispatcherServlet处理，除了通过/zuul/*路径访问的请求会绕过DispatcherServlet（比如之前我们说的大文件上传），被ZuulServlet处理，主要用来应对大文件上传的情况。另外，对于ZuulServlet的访问路径/zuul/*，我们可以通过zuul.servletPath参数进行修改。

*   **Servlet30WrapperFilter**

> 它的执行顺序为-2，是第二个执行的过滤器，目前的实现会对所有请求生效，主要为了将原始的HttpServletRequest包装成Servlet30RequestWrapper对象。

*   **FormBodyWrapperFilter**

> 它的执行顺序为-1，是第三个执行的过滤器。该过滤器仅对两类请求生效，第一类是Context-Type为application/x-www-form-urlencoded的请求，第二类是Context-Type为multipart/form-data并且是由String的DispatcherServlet处理的请求（用到了ServletDetectionFilter的处理结果）。而该过滤器的主要目的是将符合要求的请求体包装成FormBodyRequestWrapper对象

*   **DebugFilter**

> 它的执行顺序为1，是第四个执行的过滤器，该过滤器会根据配置参数zuul.debug.request和请求中的debug参数来决定是否执行过滤器中的操作。而它的具体操作内容是将当前请求上下文中的debugRouting和debugRequest参数设置为true。由于在同一个请求的不同生命周期都可以访问到这二个值，所以我们在后续的各个过滤器中可以利用这二个值来定义一些debug信息，这样当线上环境出现问题的时候，可以通过参数的方式来激活这些debug信息以帮助分析问题，另外，对于请求参数中的debug参数，我们可以通过zuul.debug.parameter来进行自定义

*   **PreDecorationFilter**

> 执行顺序是5，是pre阶段最后被执行的过滤器，该过滤器会判断当前请求上下文中是否存在forward.do和serviceId参数，如果都不存在，那么它就会执行具体过滤器的操作（如果有一个存在的话，说明当前请求已经被处理过了，因为这二个信息就是根据当前请求的路由信息加载进来的）。而当它的具体操作内容就是为当前请求做一些预处理，比如说，进行路由规则的匹配，在请求上下文中设置该请求的基本信息以及将路由匹配结果等一些设置信息等，这些信息将是后续过滤器进行处理的重要依据，我们可以通过RequestContext.getCurrentContext()来访问这些信息。另外，我们还可以在该实现中找到对HTTP头请求进行处理的逻辑，其中包含了一些耳熟能详的头域，比如X-Forwarded-Host,X-Forwarded-Port。另外，对于这些头域是通过zuul.addProxyHeaders参数进行控制的，而这个参数默认值是true，所以zuul在请求跳转时默认会为请求增加X-Forwarded-*头域，包括X-Forwarded-Host,X-Forwarded-Port，X-Forwarded-For，X-Forwarded-Prefix,X-Forwarded-Proto。也可以通过设置zuul.addProxyHeaders=false关闭对这些头域的添加动作

#### 2、route过滤器

*   **RibbonRoutingFilter**

> 它的执行顺序为10，是route阶段的第一个执行的过滤器。该过滤器只对请求上下文中存在serviceId参数的请求进行处理，即只对通过serviceId配置路由规则的请求生效。而该过滤器的执行逻辑就是面向服务路由的核心，它通过使用ribbon和hystrix来向服务实例发起请求，并将服务实例的请求结果返回

*   **SimpleHostRoutingFilter**

> 它的执行顺序为100，是route阶段的第二个执行的过滤器。该过滤器只对请求上下文存在routeHost参数的请求进行处理，即只对通过url配置路由规则的请求生效。而该过滤器的执行逻辑就是直接向routeHost参数的物理地址发起请求，从源码中我们可以知道该请求是直接通过httpclient包实现的，而没有使用Hystrix命令进行包装，所以这类请求并没有线程隔离和断路器的保护

*   **SendForwardFilter**

> 它的执行顺序是500，是route阶段第三个执行的过滤器。该过滤器只对请求上下文中存在的forward.do参数进行处理请求，即用来处理路由规则中的forward本地跳转装配

#### 3、post过滤器

*   **SendErrorFilter**

> 它的执行顺序是0，是post阶段的第一个执行的过滤器。该过滤器仅在请求上下文中包含error.status_code参数（由之前执行的过滤器设置的错误编码）并且还没有被该过滤器处理过的时候执行。而该过滤器的具体逻辑就是利用上下文中的错误信息来组成一个forward到api网关/error错误端点的请求来产生错误响应

*   **SendResponseFilter**

> 它的执行顺序为1000，是post阶段最后执行的过滤器，该过滤器会检查请求上下文中是否包含请求响应相关的头信息，响应数据流或是响应体，只有在包含它们其中一个的时候执行处理逻辑。而该过滤器的处理逻辑就是利用上下文的响应信息来组织需要发送回客户端的响应内容

#### 使用案例

**如果前端发起请求没有带指定请求头将不进允许请求，如果需要读取cookie等敏感信息，要在配置文件中加入`sensitive-headers:`,下面有对该配置的详解**

```java  language-java
/**
 * @author Gjing
 **/
@Component
public class GlobalFilter extends ZuulFilter {
    @Override
    public String filterType() {
        //设置过滤类型
        return FilterConstants.PRE_TYPE;
    }

    @Override
    public int filterOrder() {
        //设置过过滤器优先级
        return -4;
    }

    @Override
    public boolean shouldFilter() {
        //是否需要过滤
        return true;
    }

    @Override
    public Object run() throws ZuulException {
        RequestContext context = RequestContext.getCurrentContext();
        HttpServletRequest request = context.getRequest();
        String token = request.getHeader("token");
        if (StringUtils.isEmpty(token)) {
            //返回错误信息
            context.setResponseStatusCode(HttpStatus.UNAUTHORIZED.value());
            context.setResponseBody(HttpStatus.UNAUTHORIZED.getReasonPhrase());
            context.setSendZuulResponse(false);
            return null;
        }
        return null;
    }
}

```

**项目启动后如果访问不带Token请求头，将被拦截，返回`Unauthorized`**

### Zuul相关知识点

#### 1、路由配置

zuul通过与eureka的整合，实现了对服务实例的自动化维护，所以使用服务路由配置的时候，不需要向传统路由配置方式那样为serviceId指定具体服务实例地址，只需要通过`zuul.routes.<route>.path`与`zuul.routes.<route>.serviceId`参数对的方式进行配置即可

```yaml  language-yaml
zuul:
  routes:
    # 这里可以自定义
    demo2:
      # 匹配的路由规则
      path: /demo/**
      # 路由的目标服务名
      serviceId: demo

```

除了path和serviceId键值对的配置方式之外，还有一种简单的配置:`zuul.routes.<serviceId>=<path>`，其中<serviceId>用来指定路由的具体服务名，<path>用来配置匹配的请求表达式

```yaml  language-yaml
zuul:
  routes:
    demo: /demo/**

```

#### 2、路径匹配

在zuul中，路由匹配的路径表达式采用ant风格定义

| 通配符 | 说明 |
| --- | --- |
| ？ | 匹配任意单个字符 |
| * | 匹配任意数量的字符 |
| ** | 匹配任意数量的字符，支持多级目录 |

#### 3、忽略表达式

通过path参数定义的ant表达式已经能够完成api网关上的路由规则配置功能，但是为了更细粒度和更为灵活地配置理由规则，zuul还提供了一个忽略表达式参数`zuul.ignored-patterns`。该参数可以用来设置不希望被api网关进行路由的url表达式

```yaml  language-yaml
zuul:
  routes:
    demo:
      path: /demo/**
      serviceId: demo
  # 不路由demo2开头的任意请求
  ignored-patterns: /demo2/**

```

#### 4、路由前缀

为了方便地为路由规则增加前缀信息，zuul提供了`zuul.prefix`参数来进行设置。比如，希望为网关上的路由规则增加/api前缀，那么我们可以在配置文件中增加配置:`zuul.prefix=/api`。另外，对于代理前缀会默认从路径中移除，我们可以通过设置`zuul.strip-prefix=false`(默认为true，默认为true时前缀生效，比如`http://localhost:8080/api/demo/test`）来关闭该移除代理前缀的动作

#### 5、本地跳转

在zuul实现的api网关路由功能中，还支持forward形式的服务端跳转配置。实现方式非常简单，只需要通过使用path与url的配置方式就能完成，通过url中使用forward来指定需要跳转的服务器资源路径。

##### a、在zuul服务中添加一个接口

```java  language-java
/**
 * @author Gjing
 **/
@RestController
public class HelloController {

    @GetMapping("/test/hello")
    public String test() {
        return "hello zuul";
    }
}

```

##### b、配置文件

```yaml  language-yaml
zuul:
  routes:
    zuul-service:
      path: /api/**
      serviceId: forward:/test/

```

**启动后访问`http://localhost:8080/api/hello`即可**

#### 6、cookie与头信息

默认情况下，spring cloud zuul在请求路由时，会过滤掉http请求头信息中一些敏感信息，防止它们被传递到下游的外部服务器。默认的敏感头信息通过zuul.sensitiveHeaders参数定义，默认包括cookie,set-Cookie,authorization三个属性。所以，我们在开发web项目时常用的cookie在spring cloud zuul网关中默认时不传递的，这就会引发一个常见的问题，如果我们要将使用了spring security，shiro等安全框架构建的web应用通过spring cloud zuul构建的网关来进行路由时，由于cookie信息无法传递，我们的web应用将无法实现登录和鉴权。为了解决这个问题，以下介绍两种配置方式

*   **通过设置全局参数为空来覆盖默认值**

```yaml  language-yaml
zuul:
  routes:
    demo:
      path: /demo/**
      serviceId: demo
  # 允许敏感头，设置为空就行了
  sensitive-headers:

```

*   **通过指定路由的参数来设置**

```yaml  language-yaml
zuul:
  routes:
    demo:
      path: /demo/**
      serviceId: demo
      # 将指定路由的敏感头设置为空
      sensitiveHeaders:

```
