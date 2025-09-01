---
title: Zuul 动态路由源码及几种实现方式
id: 1579
date: 2024-10-31 22:02:02
author: daichangya
permalink: /archives/Zuul-dong-tai-lu-you-yuan-ma-ji-ji/
categories:
- spring-cloud
tags:
- zuul
---



本文介绍Zuul路由的源码以及实现动态路由的几种方式，路由信息可以来自Properties文件、DB、Apollo等。

可以阅读 Spring Cloud源码学习之Zuul 简要了解路由源码流程。

本文基于 Spring Cloud `Finchley.SR1`，Spring Boot `2.0.6.RELEASE`。

## **路由源码**

本文基于下图场景做演示，文中代码来自源码，但存在大幅删减。

![ci830psb5s.jpeg](https://images.jsdiff.com/ci830psb5s_1624853878422.jpeg)

请求达到ZuulServlet后，ZuulServlet 组织了路由的处理逻辑，如下：
```
public void service(servletRequest, servletResponse) {
   // 执行 "pre" 类型 ZuulFilter
   preRoute();
   // 执行 "route" 类型 ZuulFilter
   route();
   // 执行 "post" 类型 ZuulFilter
   postRoute();
}
```
### **预处理**

**pre** 类型 ZuulFilte r中，PreDecorationFilter 会根据路由信息进行预处理，其处理结果决定了使用哪个 **route** 类型 ZuulFilter 来实际处理请求。

先看看 **route** 类型的 SimpleHostRoutingFilter、RibbonRoutingFilter 的处理条件(sholdFilter)，它们负责实际的请求转发。
```
// SimpleHostRoutingFilter
public boolean shouldFilter() {
  return RequestContext.getCurrentContext().getRouteHost() != null
      && RequestContext.getCurrentContext().sendZuulResponse();
}

// RibbonRoutingFilter
public boolean shouldFilter() {
  RequestContext ctx = RequestContext.getCurrentContext();
  return (ctx.getRouteHost() == null && ctx.get("serviceId") != null
      && ctx.sendZuulResponse());
}
```
*   **相同点**：都需要满足 sendZuulResponse() 即需要将Response反馈给客户端.
*   **不同点**：SimpleHostRoutingFilter 需要 **RouteHost** 不为空，RibbonRoutingFilter需要**serviceId** 不为空而且 **RouteHost** 为空。

下面是Zuul application.yml中的配置示例：
```
zuul:
servlet-path:
routes:
  service1:
    path: /api/service1/**
    serviceId: service1
  github:
    path: /github/**
    url: https://github.com/
```
routes 中 service1 有serviceId，github有host。

再看看 PreDecorationFilter 是如何预处理得到 **RouteHost、serviceId** 的，下面是其run().
```
@Override
public Object run() {
  RequestContext ctx = RequestContext.getCurrentContext();
  final String requestURI = 根据 request 提取requestURI;
    
    // 根据requestURI获取路由信息
  Route route = this.routeLocator.getMatchingRoute(requestURI);
  if (route != null) {
    String location = route.getLocation();
    if (location != null) {
            // 以https或http开头, 设置RouteHost
      if (location.startsWith("http:") || location.startsWith("https:")) {
        ctx.setRouteHost(getUrl(location));
      }
            // 以 forward: 开头
      else if (location.startsWith("forward:")) {
        ctx.setRouteHost(null);
        return null;
      }
            // 设置 serviceId, RouteHost置空
      else {
        ctx.set(SERVICE\_ID\_KEY, location);
        ctx.setRouteHost(null);
      }
    }
  }
}
```
**routeLocator.getMatchingRoute** 是重点，根据请求URL获取Route，再根据Route的location是否匹配 **http:、https:、forward:** 前缀来设置属性。

例如访问`http://localhost:8080/service1/echo` 、 `http://localhost:8080/github/echo` 获取的Route，其location分别为：`service1、https://github.com`。
```
Route{id='service1', fullPath='/service1/echo', path='/echo', location='service1', prefix='/service1'}
Route{id='github', fullPath='/github/echo', path='/echo', location='https://github.com/', prefix='/github'}
```
### **请求转发**

请求转发由 SimpleHostRoutingFilter、RibbonRoutingFilter 完成，前者通过Apache HttpClient来转发请求，后者与Ribbon、Hystrix一起，完成客户端[负载均衡](https://cloud.tencent.com/product/clb?from=10680)及应用守护工作。

### **路由定位**

PreDecorationFilter 中通过RouteLocator根据URL获取Route，**动态路由可以通过拓展RouteLocator来完成**。
```
public interface RouteLocator {
  Collection<String> getIgnoredPaths();
  List<Route> getRoutes();
  Route getMatchingRoute(String path);
}
```
RouteLocator 主要能力有：

*   根据path获取Route
*   获取所有Route

下面是类图，稍微简介下各子类。

![qs6lp1gws6.png](https://images.jsdiff.com/qs6lp1gws6_1624853931786.png)

#### **SimpleRouteLocator**

简单路由定位器，路由信息来自ZuulProperties，locateRoutes() 是定位路由的核心，从ZuulProperties中加载了路由数据。
```
public class SimpleRouteLocator implements RouteLocator, Ordered{
    // routes 用于存储路由信息
    private AtomicReference<Map<String, ZuulRoute>> routes = new AtomicReference<>();

    // 查找路由信息
    protected Map<String, ZuulRoute> locateRoutes() {
        LinkedHashMap<String, ZuulRoute> routesMap = new LinkedHashMap<>();
        // 提取ZuulProperties中的ZuulRoute
        for (ZuulRoute route : this.properties.getRoutes().values()) {
            routesMap.put(route.getPath(), route);
        }
        return routesMap;
    }
}
```
#### **DiscoveryClientRouteLocator**

它基于 DiscoveryClient，路由数据来自properties中的静态配置 和 DiscoveryClient从注册中心获取的数据。

DiscoveryClientRouteLocator拥有几个重要的能力：

*   动态添加Route
*   刷新路由
*   从DiscoveryClient获取路由信息，但用途不大
```
public interface RefreshableRouteLocator extends RouteLocator {
  void refresh();
}

public class DiscoveryClientRouteLocator extends SimpleRouteLocator
    implements RefreshableRouteLocator {

  // 动态添加路由能力,会同步把路由信息添加到ZuulProperties,参数也可以是ZuulRoute
  public void addRoute(String path, String location) {
    this.properties.getRoutes().put(path, new ZuulRoute(path, location));
    refresh();
  }

  @Override
  protected LinkedHashMap<String, ZuulRoute> locateRoutes() {
    LinkedHashMap<String, ZuulRoute> routesMap = new LinkedHashMap<>();
    // 通过父类获取静态路由信息
    routesMap.putAll(super.locateRoutes());
    if (this.discovery != null) {
      // 通过DiscoveryClient获取路由信息
      List<String> services = this.discovery.getServices();
    }
    return values;
  }
  
  // 刷新时会调用 locateRoutes()
  @Override
  public void refresh() {
    doRefresh();
  }
}
```
以service1为例，配置 `/api/service1/** -> service1`，存储的路由信息为：

/api/service1/** -\> service1
/service1/** -> service1

`/service1/** -> service1` 就是利用DiscoveryClient提取后根据默认规则生成的路由信息，用处不大。

#### **CompositeRouteLocator**

具备组合多个RouteLocator的能力，用Collection存储多个RouteLocator，调用 getRoutes()、getMatchingRoute()、refresh() 时都会逐一调用每个RouteLocator相应的方法。
```
public class CompositeRouteLocator implements RefreshableRouteLocator {
  private final Collection<? extends RouteLocator> routeLocators;
  private ArrayList<RouteLocator> rl;

  @Override
  public List<Route> getRoutes() {
    List<Route> route = new ArrayList<>();
    for (RouteLocator locator : routeLocators) {
      route.addAll(locator.getRoutes());
    }
    return route;
  }

  @Override
  public Route getMatchingRoute(String path) {}

  @Override
  public void refresh() {}
}
```
## **动态路由**

通过上面的内容，可以知道RouteLocator的Routes数据几个来源：

*   来源于ZuulProperties，它由 **@ConfigurationProperties** 标记
```
@ConfigurationProperties("zuul")
public class ZuulProperties {}
```
*   DiscoveryClientRouteLocator 提供了 addRoute() 支持动态添加路由，但没有删除方法
*   来源于DiscoveryClient

无论来源于那里，在更新路由信息后，都需要执行 refresh() 操作才能把路由信息更新到 RouteLocator的私有属性routes中。

### **实际场景**

实际使用中，会统一管理路由信息，包含动态添加、重置操作，路由信息的可以来自：

*   Spring Cloud Config
*   携程的 Apollo
*   自定义的数据库数据
*   ...

其实路由信息来自于哪都可以，只是一个数据源而已，最后都会进入 ZuulProperties，再执行 refresh().

### **刷新路由的方式**

有两种刷新方式。

*   在任意Bean中注入CompositeRouteLocator 或自定义的RouteLocator，然后调用refresh().
```
@Autowired
private CompositeRouteLocator compositeRouteLocator;
```
*   发布RoutesRefreshedEvent事件

Zuul 提供了 ZuulRefreshListener，监听到 RoutesRefreshedEvent 后，会调用ZuulHandlerMapping 的reset()方法，进而调用RouteLocator的refresh()方法。
```
private static class ZuulRefreshListener
    implements ApplicationListener<ApplicationEvent> {
    @Autowired
    private ZuulHandlerMapping zuulHandlerMapping;
    @Override
    public void onApplicationEvent(ApplicationEvent event) {
        if (event instanceof ContextRefreshedEvent
            || event instanceof RefreshScopeRefreshedEvent
            || event instanceof RoutesRefreshedEvent
            || event instanceof InstanceRegisteredEvent) {
            reset();
        }
    }

    private void reset() {
        this.zuulHandlerMapping.setDirty(true);
    }
}

// setDirty() 会调用refresh()方法
public class ZuulHandlerMapping extends AbstractUrlHandlerMapping {
    public void setDirty(boolean dirty) {
        this.dirty = dirty;
        if (this.routeLocator instanceof RefreshableRouteLocator) {
            ((RefreshableRouteLocator) this.routeLocator).refresh();
        }
    }
}
```
### **动态路由的实现**

#### **自定义PropertySource实现**

> 思路来自于 Apollo 的设计实现

先介绍PropertySource的原理。

PropertySource 代表 **name/value** 属性对，常见的如命令行参数、环境变量、properties文件、yaml文件等最终都会转为PropertySource，再提供给应用使用。

由 `@ConfigurationProperties` 标记的类，其数据源就是PropertySource。**当多个PropertySource中存在相同值时，默认从第一个PropertySource中获取。**下面是PropertySource的部分常见子类：

![c6p9ml7aqb.jpeg](https://images.jsdiff.com/c6p9ml7aqb_1624854022060.jpeg)

下图是 Environment中PropertySources截图，其中OriginTrackedMapPropertySource来自于classpath下的application.yml文件。

![9xh9pp2ce4.jpeg](https://images.jsdiff.com/9xh9pp2ce4_1624854040117.jpeg)

如果PropertySource有更新，通过发布 EnvironmentChangeEvent 事件，ConfigurationPropertiesRebinder 会监听该事件，然后利用最新的数据将 `@ConfigurationProperties` 标记的bean重新绑定一定，从而达到动态更新的效果。

下面写一个Demo类来实现动态路由，支持从任意数据源加载数据来初始化路由，然后支持动态调整路由。
```
@Component
public class DynamicRoutesProcessor implements BeanFactoryPostProcessor, EnvironmentAware, ApplicationContextAware, PriorityOrdered {

    private static final String ZUUL\_PROPERTY\_SOURCE = "custom.zuul.routes";
    private ConfigurableEnvironment environment;
    private ApplicationContext applicationContext;
    private MapPropertySource routePropertySource = null;

    @Autowired
    private CompositeRouteLocator compositeRouteLocator;

    // 初始化路由
    @Override
    public void postProcessBeanFactory(ConfigurableListableBeanFactory configurableListableBeanFactory) throws BeansException {
        MutablePropertySources propertySources = environment.getPropertySources();

        // 可以从任何地方加载数据, 如: DB、Redis、配置中心等, 下面做示例数据
        Map<String, Object> data = new HashMap<>();
        data.put("zuul.routes.service4.path", "/api/service4/**");
        data.put("zuul.routes.service4.serviceId", "service4");

        routePropertySource = new MapPropertySource(ZUUL\_PROPERTY\_SOURCE, data);

        // 设置最高优先级
        propertySources.addFirst(routePropertySource);
    }

    // 动态刷新
    public void refreshRoutes(List<ZuulProperties.ZuulRoute> routeList) {
        // 提取 routeList 数据并覆盖到 routePropertySource

        // 将 @ConfigurationProperties 标记的类重新与PropertySources绑定, 包含ZuulProperties
        applicationContext.publishEvent(new EnvironmentChangeEvent(new HashSet<>()));

        // 刷新路由, 也可以直接调用 compositeRouteLocator.refresh()
        applicationContext.publishEvent(new RoutesRefreshedEvent(compositeRouteLocator));
    }
}
```
上面Demo类的思路是：

*   自定义PropertySource(数据来源可以自定义)并提升为最高优先级，ZuulProperties数据来自于此，完成路由初始化
*   动态刷新时，直接更新PropertySource中数据，然后利用EnvironmentChangeEvent来更新ZuulProperties数据，再刷新路由

#### **直接更新路由**

可以直接往ZuulProperties中添加路由信息，然后使用RouteLocator进行refresh()
```
@Component
public class DynamicRoutesProcessor implements InitializingBean {

    @Autowired
    private CompositeRouteLocator compositeRouteLocator;
    @Autowired
    private ZuulProperties zuulProperties;

    /**
     * 动态刷新
     *
     * @param routeList 路由信息
     */
    public void refreshRoutes(List<ZuulProperties.ZuulRoute> routeList) {
        Map<String, ZuulProperties.ZuulRoute> routes = zuulProperties.getRoutes();

        // 提取 routeList 数据并添加到routes中
        for (ZuulProperties.ZuulRoute route : routeList) {
            routes.put(route.getId(), route);
        }

        compositeRouteLocator.refresh();
    }

    /**
     * 初始化路由信息, 可以加载任意数据源
     *
     * @throws Exception
     */
    @Override
    public void afterPropertiesSet() throws Exception {
        Map<String, ZuulProperties.ZuulRoute> routes = zuulProperties.getRoutes();
        routes.put("service4", new ZuulProperties.ZuulRoute("/api/service4/**", "service4"));
        compositeRouteLocator.refresh();
    }
}
```
#### **自定义RouteLocator**

也可以通过自定义 RouteLocator 来实现动态路由，自定义的RouteLocator会添加到CompositeRouteLocator中。

下面是例子，自行实现 locateRoutes()即可，可以参考DiscoveryClientRouteLocator的实现。
```
public class DynamicZuulRouteLocator extends SimpleRouteLocator implements RefreshableRouteLocator {

    private ZuulProperties properties;

    public DynamicZuulRouteLocator(String servletPath, ZuulProperties properties) {
        super(servletPath, properties);
        this.properties = properties;
    }

    @Override
    public void refresh() {
        doRefresh();
    }

    @Override
    protected Map<String, ZuulProperties.ZuulRoute> locateRoutes() {
        Map<String, ZuulProperties.ZuulRoute> routesMap = new LinkedHashMap<>();

        // 静态路由信息
        routesMap.putAll(super.locateRoutes());

        // 动态加载路由信息, 这里hardcode做演示
        Map<String, ZuulProperties.ZuulRoute> dynamicRoutes = new LinkedHashMap<>();
        dynamicRoutes.put("service4", new ZuulProperties.ZuulRoute("service4", "/api/service4/**"));
        routesMap.putAll(dynamicRoutes);

        Map<String, ZuulProperties.ZuulRoute> values = new LinkedHashMap<>();
        for (Map.Entry<String, ZuulProperties.ZuulRoute> entry : routesMap.entrySet()) {
            String path = entry.getKey();
            if (!path.startsWith("/")) {
                path = "/" + path;
            }
            if (StringUtils.hasText(this.properties.getPrefix())) {
                path = this.properties.getPrefix() + path;
                if (!path.startsWith("/")) {
                    path = "/" + path;
                }
            }
            values.put(path, entry.getValue());
        }
        return values;
    }
}
```
然后注入到IoC容器。
```
@Bean
public DynamicZuulRouteLocator dynamicZuulRouteLocator(ServerProperties serverProperties, ZuulProperties zuulProperties) {
    return new DynamicZuulRouteLocator(serverProperties.getServlet().getContextPath(), zuulProperties);
}
```
在 ZuulServerAutoConfiguration 注入了CompositeRouteLocator，参数是 Collection<RouteLocator> routeLocators，会把当前IoC容器中的RouteLocator作为参数，目前包含：DynamicZuulRouteLocator、DiscoveryClientRouteLocator，自定义的RouteLocator
```
@Bean
@Primary
public CompositeRouteLocator primaryRouteLocator(
    Collection<RouteLocator> routeLocators) {
  return new CompositeRouteLocator(routeLocators);
}
```
**参考资料**

*   Apollo配置中心设计 https://github.com/ctripcorp/apollo/wiki/Apollo%E9%85%8D%E7%BD%AE%E4%B8%AD%E5%BF%83%E8%AE%BE%E8%AE%A1
*   Zuul Wiki https://github.com/Netflix/zuul/wiki
