---
title: 第九章：实现过滤器（Filter）和监听器（Listener）-Minitomcat
id: 81143f52-cd8c-435a-afe8-c73d20183317
date: 2024-11-19 14:50:41
author: daichangya
cover: https://images.jsdiff.com/Leonardo_Phoenix_A_stylized_modern_illustration_of_a_miniature_2.jpg
excerpt: "功能目标： 增加 Filter 和 Listener 支持，用于在请求处理过程中插入额外的操作或监听事件。 实现 Filter 接口，支持请求过滤，例如日志记录、认证拦截等功能。 实现 Listener 接口，支持监听 Servlet 上下文或会话的创建和销毁事件。 实现内容： 实现 Filter "
permalink: /archives/di-jiu-zhang-shi-xian-guo-lu-qi-filter-he-jian-ting-qi-listener--minitomcat/
categories:
 - minitomcat
tags: 
 - tomcat
---

## 功能目标：

+   增加 Filter 和 Listener 支持，用于在请求处理过程中插入额外的操作或监听事件。
    
+   实现 Filter 接口，支持请求过滤，例如日志记录、认证拦截等功能。
    
+   实现 Listener 接口，支持监听 Servlet 上下文或会话的创建和销毁事件。
    

### 实现内容：

+   实现 `Filter` 接口，拦截 HTTP 请求并在请求前后插入自定义逻辑。
    
+   实现 `Listener` 接口，监听 Servlet 上下文、会话或请求的生命周期事件。
    
+   实现一个简单的日志过滤器，记录每个请求的访问时间和路径。
    

### 示例功能：

+   实现一个日志过滤器，记录每个请求的访问时间和请求路径。
    
+   在 Servlet 上下文初始化时创建一个监听器，监听上下文和会话的创建销毁事件。
    

* * *

### 9.1 过滤器（Filter）

`Filter` 是 Servlet 容器提供的一个接口，它允许开发者在请求到达 Servlet 之前和响应返回客户端之前插入自定义的处理逻辑。过滤器可以用于执行常见的任务，如日志记录、权限验证、请求重定向、输入输出数据处理等。

#### 1\. `Filter` 接口的实现

`Filter` 接口提供了三个方法：

+   `init(FilterConfig config)`：初始化过滤器。
    
+   `doFilter(ServletRequest request, ServletResponse response, FilterChain chain)`：执行过滤器的核心逻辑，并将请求传递给下一个过滤器或目标 Servlet。
    
+   `destroy()`：销毁过滤器。
    

#### 2\. 日志过滤器的实现

我们实现一个简单的日志过滤器，用于记录每个请求的访问时间和请求路径。

```java
package com.daicy.minitomcat;

import javax.servlet.*;
import javax.servlet.http.HttpServletRequest;
import java.io.IOException;
import java.util.Date;


public class LoggingFilter implements Filter {

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        // 初始化操作，如果有需要可以在这里读取配置参数等
    }

    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        long startTime = System.currentTimeMillis();
        HttpServletRequest request = (HttpServletRequest) servletRequest;
        System.out.println("Request started at: " + startTime + " for path: " + request.getRequestURI());

        filterChain.doFilter(servletRequest, servletResponse);

        long endTime = System.currentTimeMillis();
        System.out.println("Request completed at: " + endTime + " for path: " + request.getRequestURI() + " Took: " + (endTime - startTime) + "ms");
    }

    @Override
    public void destroy() {
        // 清理资源操作
    }
}
```

在 `LogFilter` 中，`doFilter()` 方法记录了请求的访问时间和请求路径，并通过 `chain.doFilter()` 将请求传递给下一个过滤器或目标 Servlet。过滤器结束后，我们记录了请求处理的结束时间及耗时。

#### 3\. `FilterChain` 接口的实现

在实现 `FilterChain` 时，我们需要设计一个链式调用结构，它能够依次调用过滤器列表中的每个 `Filter`，直到最后一个过滤器或者目标 Servlet 被调用。`FilterChain` 的具体实现会将请求和响应对象传递给过滤器，并在每个过滤器执行完之后，继续执行下一个过滤器或最终的 Servlet 处理。

下面是一个具体的 `FilterChain` 实现：

### **FilterChain 设计概念**

+   `FilterChain` 是一个责任链模式的实现，每个过滤器执行完后，调用链中的下一个过滤器。
    
+   `doFilter` 方法将在链中的每个过滤器之间传递请求和响应对象。
    
+   一旦所有过滤器执行完，`FilterChain` 会将请求传递给实际的 Servlet 处理。
    

### **FilterChain 代码实现**

#### **FilterChain 接口**

```java
public interface FilterChain {
    // 执行链中的下一个过滤器或目标处理
    void doFilter(ServletRequest request, ServletResponse response) throws IOException, ServletException;
}
```

#### **FilterChain 实现类**

我们需要实现 `FilterChain` 接口，并在其内部维护过滤器列表。每次调用 `doFilter` 方法时，会依次执行过滤器链中的过滤器，直到最终的 Servlet 被调用。

```java
package com.daicy.minitomcat.servlet;

import com.google.common.collect.Lists;

import javax.servlet.*;
import java.io.IOException;
import java.util.LinkedList;
import java.util.List;

/**
 * @author: create by daichangya
 * @version: v1.0
 * @description: com.daicy.panda.netty.servlet.impl
 * @date:19-11-12
 */
public class FilterChainImpl implements FilterChain {

    private List<Filter> filters;  // 存储过滤器的列表
    private int currentIndex = 0;  // 当前过滤器的索引

    public FilterChainImpl(List<Filter> filters) {
        this.filters = filters;
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response) throws IOException, ServletException {
        // 如果当前索引小于过滤器链的长度，执行下一个过滤器
        if (currentIndex < filters.size()) {
            Filter filter = filters.get(currentIndex);
            currentIndex++;  // 递增索引，指向下一个过滤器
            filter.doFilter(request, response, this);  // 递归调用，传入下一个过滤器
        }
    }
}
```

### **FilterManager 代码**

`FilterManager` 负责创建过滤器链，并传递请求和响应给链中的过滤器。它将 `FilterChain` 作为一个链式调用传递给每个过滤器。

```java
package com.daicy.minitomcat;

import com.daicy.minitomcat.servlet.FilterChainImpl;

import javax.servlet.*;
import java.io.IOException;
import java.util.*;

public class FilterManager {
    private List<Filter> filters = new ArrayList<>();

    // 添加过滤器
    public void addFilter(Filter filter) {
        filters.add(filter);
    }

    // 执行过滤器链
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        FilterChain defaultChain = new FilterChainImpl(filters);
        defaultChain.doFilter(request, response);  // 递归执行过滤器链
    }

    public List<Filter> getFilters() {
        return filters;
    }
}
```

### 9.2 监听器（Listener）

`Listener` 是 Servlet 容器提供的另一种机制，用于监听 Servlet 容器内的特定事件。监听器用于捕捉和响应 Servlet 上下文、会话或请求的生命周期变化。例如，可以用来监听会话的创建和销毁，或者在应用启动时初始化共享资源。

#### 1\. `ServletContextListener` 接口

`ServletContextListener` 接口用于监听 Servlet 上下文的生命周期事件。当 Servlet 容器启动或销毁时，会触发对应的事件。

```java
package com.daicy.minitomcat;

import javax.servlet.*;

public class ServletContextListenerImpl implements ServletContextListener {

    @Override
    public void contextInitialized(ServletContextEvent servletContextEvent) {
        ServletContext servletContext = servletContextEvent.getServletContext();
        System.out.println("Servlet context initialized.");
        // 在这里可以进行初始化操作，如加载配置文件等
        servletContext.setAttribute("initialized", true);
    }

    @Override
    public void contextDestroyed(ServletContextEvent servletContextEvent) {
        ServletContext servletContext = servletContextEvent.getServletContext();
        System.out.println("Servlet context destroyed.");
        // 在这里可以进行资源清理操作，如关闭数据库连接池等
        servletContext.removeAttribute("initialized");
    }
}
```

`contextInitialized()` 方法在 Servlet 上下文初始化时调用，`contextDestroyed()` 方法在 Servlet 上下文销毁时调用。这里我们简单打印了日志，表示 Servlet 上下文的生命周期。

#### 2\. `HttpSessionListener` 接口

`HttpSessionListener` 接口用于监听 HTTP 会话的创建和销毁。当用户的会话创建或销毁时，会触发对应的事件。

```java
package com.daicy.minitomcat;

import javax.servlet.http.HttpSession;
import javax.servlet.http.HttpSessionEvent;
import javax.servlet.http.HttpSessionListener;

public class HttpSessionListenerImpl implements HttpSessionListener {

    @Override
    public void sessionCreated(HttpSessionEvent httpSessionEvent) {
        HttpSession session = httpSessionEvent.getSession();
        System.out.println("Session created with ID: " + session.getId());
        // 可以在这里进行与新会话相关的初始化操作，如创建会话相关的缓存
        session.setAttribute("created", true);
    }

    @Override
    public void sessionDestroyed(HttpSessionEvent httpSessionEvent) {
        HttpSession session = httpSessionEvent.getSession();
        System.out.println("Session destroyed with ID: " + session.getId());
        // 可以在这里清理与该会话相关的资源
        session.removeAttribute("created");
    }
}
```

`sessionCreated()` 方法在会话创建时调用，`sessionDestroyed()` 方法在会话销毁时调用。

#### 3\. 注册监听器 `ServletContextListenerManager`,`HttpSessionListenerManager`

```java
  servletContextListenerManager.addListener(new ServletContextListenerImpl());
  sessionListenerManager.addListener(new HttpSessionListenerImpl());
```

上述配置分别监听 Servlet 上下文和 HTTP 会话的生命周期事件。

* * *

### 9.3 学习收获

通过实现 Filter 和 Listener，我们深入理解了 Servlet 规范中的两大重要机制：过滤器和监听器。具体来说：

+   **Filter**：允许我们在请求处理链中插入额外的处理逻辑，如日志记录、认证验证、数据修改等。通过实现 `Filter` 接口，我们能够自定义请求处理的前后逻辑。
    
+   **Listener**：使我们能够监听 Servlet 上下文、会话和请求的生命周期事件。通过实现 `Listener` 接口，我们能够在特定的生命周期阶段（如应用启动、会话创建等）执行特定的逻辑。
    

这两者的结合，使得我们能够对请求处理流程进行灵活的扩展和控制，并实现更加复杂和丰富的功能。

* * *

这样，我们成功地实现了一个基本的过滤器和监听器机制，可以在 Servlet 容器中进行请求过滤和事件监听。这对于开发者来说，是一个非常强大的扩展点，能够让我们轻松地插入横切逻辑，如日志、权限验证、性能监控等，同时也能方便地管理应用生命周期事件。

项目源代码地址：

https://github.com/daichangya/MiniTomcat/tree/chapter9/mini-tomcat