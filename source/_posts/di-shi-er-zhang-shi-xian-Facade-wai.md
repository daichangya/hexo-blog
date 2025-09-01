---
title: 第十二章：实现 Facade（外观模式）-MiniTomcat
id: d4b4a2a7-c464-4d61-bb13-e2b1ddc1ae61
date: 2024-11-23 16:18:56
author: daichangya
cover: https://images.jsdiff.com/MiniTomcat314.jpg
excerpt: 功能目标： 使用 Facade 模式简化外部对 Servlet API 的访问，隐藏内部复杂的实现细节，提供更简洁的接口供外部调用。 实现内容：
  Facade 模式：Facade 是一种设计模式，用于封装复杂的子系统。通过封装，Facade 提供了一个统一的接口，使得外部系统在不需要了解内部实现的情
permalink: /archives/di-shi-er-zhang-shi-xian-Facade-wai/
categories:
- minitomcat
- 设计模式
tags:
- tomcat
---

### 功能目标：

+   使用 **Facade** 模式简化外部对 Servlet API 的访问，隐藏内部复杂的实现细节，提供更简洁的接口供外部调用。
    

### 实现内容：

+   **Facade 模式**：Facade 是一种设计模式，用于封装复杂的子系统。通过封装，Facade 提供了一个统一的接口，使得外部系统在不需要了解内部实现的情况下，依然能够轻松访问子系统的功能。
    
+   在 Servlet 容器中，我们可以通过 Facade 包装如 `HttpServletRequest` 和 `HttpServletResponse` 等对象，限制对内部结构的直接访问，简化对外接口的复杂度。
    
+   **RequestFacade** 和 **ResponseFacade** 类作为具体实现，它们封装了 `HttpServletRequest` 和 `HttpServletResponse`，隐藏了请求和响应的复杂细节，提供标准的请求和响应接口。
    

### 示例功能：

+   创建一个 `RequestFacade` 类，封装实际的请求对象，屏蔽不必要的内部细节，简化外部对请求的访问。
    

* * *

### 12.1 Facade 模式设计

**Facade 模式**的关键是将复杂的子系统操作封装在一个简单的接口中。对于 Web 容器而言，我们需要简化客户端访问 `HttpServletRequest` 和 `HttpServletResponse` 的复杂性，同时隐藏底层实现的细节。

我们将 `RequestFacade` 和 `ResponseFacade` 提供给用户，代替直接使用 `HttpServletRequest` 和 `HttpServletResponse`。

* * *

### 12.2 实现 RequestFacade 类

`RequestFacade` 类封装了对 `HttpServletRequest` 的操作，隐藏了请求的复杂实现细节。客户端通过 `RequestFacade` 来访问请求的相关信息。

```java
package com.daicy.minitomcat;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletRequestWrapper;

public class RequestFacade extends HttpServletRequestWrapper {
    /**
     * Constructs a request object wrapping the given request.
     *
     * @param request
     * @throws IllegalArgumentException if the request is null
     */
    public RequestFacade(HttpServletRequest request) {
        super(request);
    }
}
```

+   `getRequestURI()`：获取请求的 URI。
    
+   `getHeaderNames()`：获取请求头的名称。
    
+   `getHeader(String name)`：根据头名称获取请求头的值。
    
+   `getParameter(String name)`：获取请求参数。
    
+   `getMethod()`：获取请求方法（如 GET、POST 等）。
    

通过封装 `HttpServletRequest`，外部系统不需要直接与复杂的请求对象交互，只需使用 `RequestFacade` 提供的简洁接口。

* * *

### 12.3 实现 ResponseFacade 类

`ResponseFacade` 类封装了对 `HttpServletResponse` 的操作，隐藏了响应的复杂实现细节。客户端通过 `ResponseFacade` 来操作响应数据。

```java
package com.daicy.minitomcat;

import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpServletResponseWrapper;

public class ResponseFacade extends HttpServletResponseWrapper {
    /**
     * Constructs a response adaptor wrapping the given response.
     *
     * @param response
     * @throws IllegalArgumentException if the response is null
     */
    public ResponseFacade(HttpServletResponse response) {
        super(response);
    }
}
```

+   `setStatus(int statusCode)`：设置响应的状态码。
    
+   `setHeader(String name, String value)`：设置响应头。
    
+   `write(String content)`：将内容写入响应体。
    
+   `sendRedirect(String location)`：发送重定向响应。
    

通过 `ResponseFacade`，外部系统可以更简单地管理 HTTP 响应。

* * *

### 12.4 使用 Facade 模式简化代码

在 Web 服务器的实现中，`RequestFacade` 和 `ResponseFacade` 简化了请求和响应的处理，让外部调用更加直观。

```java
RequestFacade requestFacade = new RequestFacade(request);
ResponseFacade responseFacade = new ResponseFacade(response);

headerHandler.applyHeaders(requestFacade, responseFacade, requestFacade.getSession().getId());
List<Filter> filters = HttpServer.filterManager.getFilters();
FilterChain filterChain = new FilterChain() {
    int index = 0;
    @Override
    public void doFilter(ServletRequest request, ServletResponse response) throws IOException, ServletException {
        if (index == filters.size()) {
            try {
                wrapper.invoke((HttpServletRequest) request, (HttpServletResponse) response);
            } catch (Exception e) {
                HttpServletResponse httpServletResponse = (HttpServletResponse) response;
                // 捕获异常并设置错误状态码
                httpServletResponse.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
                httpServletResponse.getWriter().write("Internal Server Error: " + e.getMessage());
            }
        } else {
            Filter filter = filters.get(index);
            index++;
            filter.doFilter(request, response, this);
        }
    }
};
filterChain.doFilter(requestFacade, responseFacade);
```

+   在 `ServletProcessor` 类中，通过 `RequestFacade` 和 `ResponseFacade` 处理请求和响应，使得外部调用变得简单。
    

* * *

### 12.5 学习收获

通过实现 Facade 模式，我们学到了以下内容：

1.  **Facade 模式的设计思想**：Facade 模式通过封装复杂的子系统，提供了一个简化的接口，使得外部系统不需要了解内部的实现细节。
    
2.  **简化接口设计**：通过 `RequestFacade` 和 `ResponseFacade`，我们能够把复杂的请求和响应处理逻辑隐藏在内部，只暴露简单易用的接口给外部调用者。
    
3.  **提高安全性和易用性**：Facade 模式通过限制对复杂系统的直接访问，提供了更高的安全性，同时降低了外部系统的使用难度。
    

通过 Facade 模式，我们使得 Web 服务器的接口变得更加简洁和安全，同时也更易于扩展和维护。

项目源代码地址：

https://github.com/daichangya/MiniTomcat/tree/chapter12/mini-tomcat