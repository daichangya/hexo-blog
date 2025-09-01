---
title: 第十三章：实现生命周期管理（Lifecycle）-MiniTomcat
id: 0fabe3ea-edfd-48e9-af66-f1aee15a677a
date: 2024-11-23 16:20:06
author: daichangya
cover: https://images.jsdiff.com/MiniTomcat313.jpg
excerpt: 功能目标： 实现 Lifecycle 组件，用于统一管理各个组件的启动、停止等生命周期操作。 实现内容： 定义 Lifecycle 接口，提供 start
  和 stop 方法，供容器中的 Context、Wrapper 等组件使用，方便容器统一管理不同组件的生命周期。 背景： 在 Web 容器中，不
permalink: /archives/di-shi-san-zhang-shi-xian-sheng-ming/
categories:
- minitomcat
---

### 功能目标：

+   实现 **Lifecycle** 组件，用于统一管理各个组件的启动、停止等生命周期操作。
    

### 实现内容：

+   定义 **Lifecycle** 接口，提供 `start` 和 `stop` 方法，供容器中的 **Context**、**Wrapper** 等组件使用，方便容器统一管理不同组件的生命周期。
    

### 背景：

在 Web 容器中，不同的组件（如 Servlet、Web 应用等）通常有明确的生命周期，从创建到销毁需要一系列的管理操作。为了简化对这些组件生命周期的管理，可以引入统一的生命周期管理机制。通过定义 `Lifecycle` 接口，容器能够统一控制组件的启动、停止，确保资源的正确初始化与销毁。

* * *

### 13.1 生命周期管理的设计思路

我们首先需要定义一个 **Lifecycle** 接口，所有需要管理生命周期的组件（如 `Context`、`Wrapper`、`Servlet`）都可以实现该接口。该接口定义了两个基本方法：

+   `start()`：表示组件的启动操作。
    
+   `stop()`：表示组件的停止操作。
    

这些组件在容器中启动时，将通过调用 `start()` 方法进行初始化，停止时通过调用 `stop()` 方法释放资源。

* * *

### 13.2 定义 Lifecycle 接口

首先定义 `Lifecycle` 接口，它将为实现生命周期管理的组件提供统一的接口。

```java
package server;

public interface Lifecycle {
    void start() throws Exception;  // 启动操作
    void stop() throws Exception;   // 停止操作
}
```

+   `start()` 方法用于启动组件，可能会执行初始化操作。
    
+   `stop()` 方法用于停止组件，通常执行清理工作，如释放资源。
    

* * *

### 13.3 实现 Context 和 Wrapper 的 Lifecycle 管理

我们将 **Context** 和 **Wrapper** 组件实现 **Lifecycle** 接口，以便统一管理它们的生命周期。

#### 13.3.1 实现 StandardWrapper 类

`StandardWrapper` 是 Servlet 的封装容器，负责管理单个 Servlet 的生命周期。我们通过实现 `Lifecycle` 接口，来控制 Servlet 的启动和停止。

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
    public void start() throws ServletException {
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
    public void stop() {
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

+   `start()` 方法通过反射加载 Servlet 类，并创建实例，接着调用 `init()` 方法初始化 Servlet。
    
+   `stop()` 方法调用 `destroy()` 销毁 Servlet。
    

#### 13.3.2 实现 StandardContext 类

`StandardContext` 是 Web 应用的上下文容器，它管理应用的生命周期，包括加载和卸载多个 `Wrapper`。我们同样需要实现 `Lifecycle` 接口来管理整个 Web 应用的启动和停止。

```java
package com.daicy.minitomcat.core;

import com.daicy.minitomcat.WebXmlServletContainer;
import com.google.common.collect.Lists;

import javax.servlet.Servlet;
import javax.servlet.ServletConfig;
import javax.servlet.ServletException;

import java.util.*;
import java.util.stream.Collectors;

public class StandardContext implements Context{

    private Map<String, Wrapper> wrapperMap = new HashMap<>();

    private WebXmlServletContainer config;

    public StandardContext(String configFilePath) throws Exception {
        config = new WebXmlServletContainer();
        config.loadConfig(configFilePath);
        start();
    }

    public Wrapper getWrapper(String servletPath) {
        String servletName = config.getServletName(servletPath);
        return getWrapperByName(servletName);
    }

    public Wrapper getWrapperByName(String servletName) {
        return wrapperMap.get(servletName);
    }

    @Override
    public void start() throws Exception {
        Map<String, ServletConfig> servletConfigMap = config.getServletConfigMap();
        for (String className : servletConfigMap.keySet()) {
            ServletConfig servletConfig = servletConfigMap.get(className);
            Wrapper wrapper = new StandardWrapper(servletConfig, className);
            wrapper.start();
            wrapperMap.put(servletConfig.getServletName(), wrapper);
        }
    }

    @Override
    public void stop() throws Exception {
        List<Wrapper> wrappers = getWrappers();
        if(null == wrappers){
            return ;
        }
        for (Wrapper wrapper : wrappers){
            wrapper.stop();
        }
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

+   `start()` 方法启动 Web 应用中的所有 `Wrapper`，即加载所有的 Servlet。
    
+   `stop()` 方法停止 Web 应用中的所有 `Wrapper`，即销毁所有的 Servlet。
    

* * *

### 13.4 示例功能：启动和停止 Web 应用

现在我们可以测试 `Lifecycle` 接口的功能，通过启动和停止 Web 应用来验证我们实现的生命周期管理。

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

    public static void main(String[] args) throws Exception {
        servletContextListenerManager.addListener(new ServletContextListenerImpl());
        sessionListenerManager.addListener(new HttpSessionListenerImpl());
        // 启动监听器
        servletContextListenerManager.notifyContextInitialized(new ServletContextEvent(servletContext));
        context = new StandardContext("/web.xml");
        context.start();
        filterManager.addFilter(new LoggingFilter());
        HttpConnector connector = new HttpConnector();
        connector.start();

        // 模拟服务器关闭
        Runtime.getRuntime().addShutdownHook(new Thread(HttpServer::stop));
    }

    public static void stop() {
        try {
            System.out.println("Server stopping...");
            context.stop();
            servletContextListenerManager.notifyContextDestroyed(new ServletContextEvent(servletContext));
            SessionManager.removeSession();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
```

在这个示例中，我们创建了一个 `Context` 实例并向其中添加了多个 `Wrapper`，每个 `Wrapper` 关联一个 Servlet 类。然后调用 `context.start()` 启动应用，`context.stop()` 停止应用。

* * *

### 13.5 学习收获

通过实现生命周期管理，我们学到了以下几点：

1.  **统一的生命周期管理**：通过 `Lifecycle` 接口，我们实现了一个统一的方式来管理组件的启动和停止。容器可以通过统一接口控制各个组件的生命周期，简化了代码结构。
    
2.  **Web 应用的生命周期**：通过 `Context` 和 `Wrapper` 类的管理，我们能够模拟 Web 应用和 Servlet 的生命周期，理解 Web 容器如何管理多个 Servlet 的生命周期。
    
3.  **组件化管理**：生命周期管理让 Web 容器的各个组件可以独立管理，提升了系统的可扩展性和灵活性。
    

通过生命周期管理机制，我们为 Web 容器提供了更加清晰、规范的组件管理流程，使得每个组件的生命周期操作更加明确。

项目源代码地址：

https://github.com/daichangya/MiniTomcat/tree/chapter13/mini-tomcat