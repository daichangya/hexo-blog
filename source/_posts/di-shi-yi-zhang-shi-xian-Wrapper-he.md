---
title: 第十一章：实现 Wrapper 和 Context-MiniTomcat
id: 189b79bc-39ed-4b7c-8799-042a71f962c2
date: 2024-11-23 08:37:30
author: daichangya
cover: https://images.jsdiff.com/tomcat192.jpg
excerpt: 功能目标： Wrapper：负责管理单个 Servlet 的生命周期，封装 Servlet 的创建、初始化、调用和销毁过程。 Context：用于管理
  Web 应用的上下文，一个 Context 可以包含多个 Wrapper，每个 Wrapper 代表一个 Servlet。Context 负责加载和
permalink: /archives/di-shi-yi-zhang-shi-xian-Wrapper-he/
categories:
- minitomcat
tags:
- tomcat
---

### 功能目标：

+   **Wrapper**：负责管理单个 Servlet 的生命周期，封装 Servlet 的创建、初始化、调用和销毁过程。
    
+   **Context**：用于管理 Web 应用的上下文，一个 Context 可以包含多个 Wrapper，每个 Wrapper 代表一个 Servlet。Context 负责加载和卸载整个 Web 应用，并维护应用的配置和生命周期。
    

### 实现内容：

+   **Wrapper**：每个 Wrapper 对象封装了一个特定的 Servlet 实例，负责该 Servlet 的生命周期管理。Wrapper 管理 Servlet 的初始化、销毁，并提供对 Servlet 的访问。
    
+   **Context**：Context 代表 Web 应用的上下文，它包含多个 Wrapper，每个 Wrapper 对应一个 Servlet。Context 管理 Web 应用的配置、生命周期以及 Servlet 的加载和卸载。
    

### 示例功能：

+   在 Context 中配置多个 Wrapper，每个 Wrapper 绑定到不同的 Servlet，支持多个 Servlet 在同一 Web 应用中共存。
    

* * *

### 11.1 Wrapper 接口设计

Wrapper 负责管理单个 Servlet 的生命周期。它提供了 Servlet 的初始化、销毁方法，并可以访问和执行该 Servlet。

```java
package com.daicy.minitomcat.core;

import javax.servlet.Servlet;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public interface Wrapper {
    // 初始化 Wrapper，加载 Servlet
    void loadServlet() throws ServletException;

    // 调用 Servlet 的 service 方法处理请求
    void invoke(HttpServletRequest request, HttpServletResponse response) throws Exception;

    // 销毁 Servlet
    void unloadServlet();

    // 获取绑定的 Servlet 实例
    Servlet getServlet();
}
```

+   `loadServlet()`：加载并初始化 Servlet。
    
+   `invoke(HttpServletRequest request, HttpServletResponse response)`：调用 Servlet 的 `service()` 方法处理请求。
    
+   `unloadServlet()`：销毁 Servlet 实例。
    
+   `getServlet()`：获取当前 Wrapper 绑定的 Servlet 实例。
    

* * *

### 11.2 Wrapper 实现

`StandardWrapper` 类实现了 Wrapper 接口，它封装了一个 Servlet 实例，并提供了初始化、调用、销毁等操作。

```java
package com.daicy.minitomcat.core;

import javax.servlet.*;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class StandardWrapper implements Wrapper {


    private Servlet servlet;

    private String className;

    private ServletConfig servletConfig;

    public StandardWrapper(ServletConfig servletConfig, String className) {
        this.servletConfig = servletConfig;
        this.className = className;
    }

    @Override
    public void loadServlet() throws ServletException {
        try {
            // 加载 Servlet 实例
            servlet = (Servlet) Class.forName(className).newInstance();
            servlet.init(servletConfig);
        } catch (Exception e) {
            throw new ServletException("Failed to load servlet", e);
        }
    }

    @Override
    public void invoke(HttpServletRequest request, HttpServletResponse response) throws Exception {
        servlet.service(request, response);
    }


    @Override
    public void unloadServlet() {
        if (servlet != null) {
            servlet.destroy();
        }
    }

    @Override
    public Servlet getServlet() {
        return servlet;
    }
}
```

+   `loadServlet()`：通过反射加载 Servlet 类，并调用 `init()` 方法进行初始化。
    
+   `invoke(HttpServletRequest request, HttpServletResponse response)`：调用 Servlet 的 `service()` 方法处理请求。
    
+   `unloadServlet()`：调用 Servlet 的 `destroy()` 方法销毁 Servlet 实例。
    
+   `getServlet()`：返回当前绑定的 Servlet 实例。
    

* * *

### 11.3 Context 接口设计

Context 管理着 Web 应用中的所有 Wrapper，它负责加载、初始化和卸载 Web 应用中的 Servlet，并提供相关配置。

```java
package com.daicy.minitomcat.core;

import javax.servlet.ServletException;
import java.util.List;

public interface Context {
    // 加载所有 Servlet
    void load() throws ServletException;

    // 卸载所有 Servlet
    void unload();

    // 获取 Web 应用中的所有 Wrapper
    List<Wrapper> getWrappers();
}
```

+   `load()`：加载所有 Servlet，初始化 Web 应用。
    
+   `unload()`：卸载所有 Servlet，释放资源。
    
+   `getWrappers()`：返回当前 Context 中的所有 Wrapper。
    

* * *

### 11.4 Context 实现

`StandardContext` 类实现了 Context 接口，管理多个 Wrapper，并提供加载、调用和卸载 Web 应用的功能。

```java
package com.daicy.minitomcat.core;

import com.daicy.minitomcat.HttpServer;
import com.daicy.minitomcat.WebXmlServletContainer;
import com.daicy.minitomcat.servlet.HttpServletResponseImpl;
import com.google.common.collect.Lists;

import javax.servlet.Servlet;
import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.util.*;
import java.util.stream.Collectors;

public class StandardContext implements Context{

    private Map<String, Wrapper> wrapperMap = new HashMap<>();

    private WebXmlServletContainer config;

    public StandardContext(String configFilePath) throws ServletException {
        config = new WebXmlServletContainer();
        config.loadConfig(configFilePath);
        load();
    }

    public Wrapper getWrapper(String servletPath) {
        String servletName = config.getServletName(servletPath);
        return getWrapperByName(servletName);
    }

    public Wrapper getWrapperByName(String servletName) {
        return wrapperMap.get(servletName);
    }

    @Override
    public void load() throws ServletException {
        Map<String, ServletConfig> servletConfigMap = config.getServletConfigMap();
        for (String className : servletConfigMap.keySet()) {
            ServletConfig servletConfig = servletConfigMap.get(className);
            Wrapper wrapper = new StandardWrapper(servletConfig, className);
            wrapper.loadServlet();
            wrapperMap.put(servletConfig.getServletName(), wrapper);
        }
    }

    @Override
    public void unload() {
        List<Wrapper> wrappers = getWrappers();
        if(null == wrappers){
            return ;
        }
        wrappers.forEach(Wrapper::unloadServlet);
    }

    @Override
    public List<Wrapper> getWrappers() {
        return new ArrayList<>(wrapperMap.values());
    }

    public List<Servlet> getServlets() {
        List<Wrapper> wrappers = getWrappers();
        if(null == wrappers){
            return Lists.newArrayList();
        }
        return wrappers.stream().map(Wrapper::getServlet).collect(Collectors.toList());
    }


    public List<String> getServletNames() {
        return config.getServletNames();
    }
}
```

+   `load()`：初始化所有 Wrapper，并加载其对应的 Servlet。
    
+   `unload()`：卸载所有 Wrapper，销毁其绑定的 Servlet。
    
+   `getWrappers()`：返回当前 Context 中的所有 Wrapper。
    

* * *

### 11.5 整合 Wrapper 和 Context

在 Web 服务器中，我们将 `StandardContext` 和 `StandardWrapper` 结合，管理多个 Servlet。

```java
package com.daicy.minitomcat;

import com.daicy.minitomcat.core.StandardContext;
import com.daicy.minitomcat.servlet.CustomHttpSession;
import com.daicy.minitomcat.servlet.ServletContextImpl;

import javax.servlet.*;
import javax.servlet.http.HttpSessionEvent;
import java.util.Enumeration;

/**
 * @author 代长亚
 * 一个简单的 HTTP 服务器，用于处理 GET 请求并返回静态文件。
 */
public class HttpServer {
    static final String WEB_ROOT = "webroot"; // 静态文件根目录

    public static ServletContextImpl servletContext = new ServletContextImpl();

    public static StandardContext context;

    public static FilterManager filterManager = new FilterManager();

    private static ServletContextListenerManager servletContextListenerManager = new ServletContextListenerManager();

    public static HttpSessionListenerManager sessionListenerManager = new HttpSessionListenerManager();

    public static void main(String[] args) throws ServletException {
        servletContextListenerManager.addListener(new ServletContextListenerImpl());
        sessionListenerManager.addListener(new HttpSessionListenerImpl());
        // 启动监听器
        servletContextListenerManager.notifyContextInitialized(new ServletContextEvent(servletContext));
        context = new StandardContext("/web.xml");
        filterManager.addFilter(new LoggingFilter());
        HttpConnector connector = new HttpConnector();
        connector.start();

        // 模拟服务器关闭
        Runtime.getRuntime().addShutdownHook(new Thread(HttpServer::stop));
    }

    public static void stop() {
        System.out.println("Server stopping...");
        context.unload();
        servletContextListenerManager.notifyContextDestroyed(new ServletContextEvent(servletContext));
        SessionManager.removeSession();
    }

}
```

+   `HttpServer` 类负责启动 Web 应用，加载 Servlet，处理请求并卸载 Servlet。
    

* * *

### 11.6 学习收获

通过实现 Wrapper 和 Context，我们学到了以下内容：

+   **Wrapper**：负责管理单个 Servlet 的生命周期。每个 Wrapper 可以独立地加载、调用和销毁 Servlet。
    
+   **Context**：Web 应用的上下文容器，管理着所有 Wrapper 和 Servlet 的生命周期。Context 使得多个 Servlet 可以在同一个 Web 应用中共存。
    
+   **组件化管理**：通过 Wrapper 和 Context，我们将 Servlet 的生命周期管理进行了模块化设计，增强了 Web 应用的可维护性和扩展性。
    

这一结构有助于我们更好地理解 Web 容器的设计原理，并能灵活地管理和扩展 Web 应用。

项目源代码地址：

https://github.com/daichangya/MiniTomcat/tree/chapter11/mini-tomcat