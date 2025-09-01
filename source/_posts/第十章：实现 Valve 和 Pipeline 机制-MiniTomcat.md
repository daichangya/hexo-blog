---
title: 第十章：实现 Valve 和 Pipeline 机制-MiniTomcat
id: 2fc992df-4790-499d-9748-607983d25057
date: 2024-11-22 21:20:26
author: daichangya
cover: https://images.jsdiff.com/tomcat194.jpg
excerpt: "功能目标： 实现 Valve 和 Pipeline 机制，允许在请求处理流程中插入额外的控制和功能扩展。 Valve：是一种过滤器链机制，可以在请求和响应过程中插入额外的处理逻辑。例如，可以实现权限控制、日志记录和请求过滤等功能。 Pipeline：负责管理多个 Valve 的执行顺序，每个请求都会"
permalink: /archives/di-10-zhang-shi-xian-valve-he-pipeline-ji-zhi-minitomcat/
categories:
 - minitomcat
---

### 功能目标：

+   实现 Valve 和 Pipeline 机制，允许在请求处理流程中插入额外的控制和功能扩展。
    
+   **Valve**：是一种过滤器链机制，可以在请求和响应过程中插入额外的处理逻辑。例如，可以实现权限控制、日志记录和请求过滤等功能。
    
+   **Pipeline**：负责管理多个 Valve 的执行顺序，每个请求都会按顺序通过 Pipeline 中的 Valve 执行操作。
    

### 实现内容：

+   定义 **Valve 接口**，让每个 Valve 实现特定的逻辑，并将 Valve 按顺序添加到 **Pipeline** 中。
    
+   **Pipeline** 是一个容器，管理多个 **Valve** 的执行顺序。
    
+   每个请求都将通过一系列的 Valve，允许灵活地扩展请求处理逻辑。
    

### 示例功能：

+   实现一个日志记录 Valve，记录每个请求的 URI 和执行时间，并将该 Valve 添加到 Pipeline 中。
    

* * *

### 10.1 Valve 接口的设计

Valve 接口定义了一个处理请求和响应的标准接口。每个实现了 Valve 接口的类都可以在请求流中执行特定的功能。

```java
package com.daicy.minitomcat;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public interface Valve {
    void invoke(HttpServletRequest request, HttpServletResponse response, ValveContext context);
}
```

+   **invoke(Request request, Response response, ValveContext context)**：这个方法会在请求进入 Valve 时被调用。它接受 `Request`、`Response` 和 `ValveContext` 作为参数。
    
    +   `Request` 和 `Response` 对象表示当前请求和响应。
        
    +   `ValveContext` 提供了继续传递请求和响应到下一个 Valve 的能力。
        

* * *

### 10.2 ValveContext 类

`ValveContext` 类用于在 Valve 之间传递请求，它负责控制请求在 Valve 链中的传递。

```java
package com.daicy.minitomcat;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.List;

public class ValveContext {
    private int currentIndex = -1;
    private final List<Valve> valves;

    public ValveContext(List<Valve> valves) {
        this.valves = valves;
    }

    public void invokeNext(HttpServletRequest request, HttpServletResponse response) {
        currentIndex++;
        if (currentIndex < valves.size()) {
            valves.get(currentIndex).invoke(request, response, this);
        }
    }
}
```

+   `ValveContext` 保存了请求的处理流程顺序，并通过 `invokeNext()` 方法依次执行 Valve 链中的下一个 Valve。
    

* * *

### 10.3 Pipeline 类的设计

`Pipeline` 是一个管理 Valve 顺序的容器，它确保每个请求都按照预定的顺序通过各个 Valve 进行处理。

```java
package com.daicy.minitomcat;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.ArrayList;
import java.util.List;

public class Pipeline {
    private final List<Valve> valves = new ArrayList<>();
    private Valve basicValve; // BasicValve 处理最后的逻辑

    public void addValve(Valve valve) {
        valves.add(valve);
    }

    public void setBasicValve(Valve basicValve) {
        this.basicValve = basicValve;
    }

    public void invoke(HttpServletRequest request, HttpServletResponse response) {
        List<Valve> allValves = new ArrayList<>(valves);
        if (basicValve != null) {
            allValves.add(basicValve);
        }
        new ValveContext(allValves).invokeNext(request, response);
    }
}
```

+   **addValve(Valve valve)**：将一个新的 Valve 添加到 Pipeline 中。
    
+   **get(int index)**：获取 Pipeline 中指定索引的 Valve。
    
+   **size()**：返回 Pipeline 中的 Valve 数量。
    

* * *

### 10.4 示例：日志记录 Valve

接下来，我们实现一个简单的日志记录 Valve，它记录每个请求的 URI 和执行时间。

```java
package com.daicy.minitomcat;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class LogValve implements Valve {

    @Override
    public void invoke(HttpServletRequest request, HttpServletResponse response, ValveContext context) {
        System.out.println("LogValve: Logging request " + request.getRequestURI());
        context.invokeNext(request, response); // 调用下一个 Valve
    }
}
```

+   `LogValve` 在请求到达时记录 URI 和请求的处理时间。
    
+   通过 `context.invokeNext()`，它将请求传递给 Pipeline 中的下一个 Valve。
    

* * *

### 10.5 BasicValve：具体逻辑调用的 Valve

```java
    class BasicValve implements Valve {
        private OutputStream outputStream;
        @Override
        public void invoke(HttpServletRequest request, HttpServletResponse response, ValveContext context) {
            // 默认的 Valve，处理请求
            HttpServletRequestImpl requestImpl = (HttpServletRequestImpl) request;
            HttpServletResponseImpl responseImpl = (HttpServletResponseImpl) response;
            String uri = request.getRequestURI();
            WebXmlServletContainer parser = HttpServer.parser;
            String servletName = parser.getServletName(uri);
            if (uri.endsWith(".html") || uri.endsWith(".css") || uri.endsWith(".js")) {
                staticProcessor.process(requestImpl, responseImpl);
            }else if (null != servletName)  {
                // 普通请求处理
                servletProcessor.process(request, response);
            }else {
                send404Response(outputStream);
            }
        }
    }
```

+   `LogValve` 在请求到达时记录 URI 和请求的处理时间。
    
+   通过 `context.invokeNext()`，它将请求传递给 Pipeline 中的下一个 Valve。
    

* * *

### 10.6 整合 Valve 和 Pipeline

最后，我们需要将 `Valve` 和 `Pipeline` 整合到 Web 服务器的请求处理过程中。每次请求都会通过一个由多个 Valve 组成的 Pipeline 进行处理。

```java
package server;

import javax.servlet.*;
import java.io.IOException;

public class HttpProcessor {
    ....
    public void process() {
        boolean keepAlive = false;
        HttpServletRequestImpl request = null;
        try  {
            InputStream inputStream = socket.getInputStream();
            OutputStream outputStream = socket.getOutputStream();
            // 解析请求
            request = HttpRequestParser.parseHttpRequest(inputStream);
            // 构建响应
            HttpServletResponseImpl response = new HttpServletResponseImpl(outputStream);
            if(null == request){
                return;
            }
            keepAlive = parseKeepAliveHeader(request) && !isCloseConnection(request);
            Pipeline pipeline = new Pipeline();
            pipeline.addValve(new LogValve());
            pipeline.setBasicValve(new BasicValve());
            pipeline.invoke(request, response);

        } catch (Exception e) {
            System.out.println("HttpProcessor error " + e.getMessage());
        } finally {
            try {
                // 如果是 keep-alive，连接保持打开，否则关闭连接
                if (!keepAlive && (null!= request && !request.isAsyncSupported())) {
                    socket.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
.....
}
```

+   在 `HttpProcessor` 中，我们创建了一个 `Pipeline` 实例，并将 `LogValve` 添加到 Pipeline 中。
    
+   `process()` 方法启动请求的处理流程，通过 `ValveContext` 来依次执行 Pipeline 中的 Valve。
    

* * *

### 10.7 学习收获

通过实现 Valve 和 Pipeline 机制，我们加深了对请求处理链的理解，并掌握了如何设计灵活的请求处理流程。具体收获如下：

+   **Valve 机制**：通过实现自定义的 Valve，我们可以在请求处理过程中插入各种功能，如权限控制、日志记录、请求修改等。
    
+   **Pipeline 机制**：Pipeline 管理着多个 Valve，确保它们按照指定顺序执行。每个请求都会按照相同的流程通过 Pipeline 中的 Valve，保证了请求处理的灵活性和可扩展性。
    
+   **扩展性**：Valve 和 Pipeline 机制使得 Web 服务器的功能扩展更加简洁和模块化，类似于 Tomcat 中的 Valve 和 Pipeline 设计，方便开发者根据需求进行定制。
    

通过这一机制，我们能够实现更复杂、更灵活的请求处理功能，为后续的功能扩展提供了强大的支持。

项目源代码地址：

https://github.com/daichangya/MiniTomcat/tree/chapter10/mini-tomcat