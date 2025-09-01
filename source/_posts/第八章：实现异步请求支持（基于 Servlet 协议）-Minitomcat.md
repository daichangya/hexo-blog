---
title: 第八章：实现异步请求支持（基于 Servlet 协议）-Minitomcat
id: 9b723349-275c-417a-a6f1-324e2866fd3f
date: 2024-11-19 14:48:53
author: daichangya
cover: https://images.jsdiff.com/tomcat192.jpg
excerpt: "在本章中，我们将进一步扩展 MiniTomcat，加入对 Servlet 协议的支持，特别是 异步请求处理。Servlet 3.0 引入了异步请求处理的机制，允许请求在后台异步处理，从而避免了阻塞主线程，提高服务器处理效率，特别是在处理长时间运行的请求（如文件上传、大数据处理等）时。 8.1 功能目"
permalink: /archives/di-ba-zhang-shi-xian-yi-bu-qing-qiu-zhi-chi-ji-yu-servlet-xie-yi--minitomcat/
categories:
 - minitomcat
tags: 
 - tomcat
---

在本章中，我们将进一步扩展 `MiniTomcat`，加入对 **Servlet 协议**的支持，特别是 **异步请求处理**。Servlet 3.0 引入了异步请求处理的机制，允许请求在后台异步处理，从而避免了阻塞主线程，提高服务器处理效率，特别是在处理长时间运行的请求（如文件上传、大数据处理等）时。

### 8.1 功能目标

+   实现 Servlet 3.0 异步请求处理功能。
    
+   通过 `AsyncContext` 提供异步请求和响应的处理机制，允许在后台线程处理长时间任务而不阻塞主线程。
    
+   支持异步响应，确保在异步任务完成后能够向客户端发送正确的响应。
    

### 8.2 异步处理流程

1.  **启动异步请求**：客户端发起请求后，Servlet 容器检查请求是否需要异步处理。如果需要异步处理，调用 `request.startAsync()` 启动异步请求。
    
2.  **异步任务执行**：Servlet 容器将请求分配到后台线程进行处理，主线程立即返回，继续处理其他请求。
    
3.  **完成异步处理**：后台线程执行完任务后，调用 `AsyncContext.complete()` 完成异步处理，向客户端发送响应。
    

### 8.3 代码实现

#### 8.3.1 修改 `HttpServletRequestImpl` 类，支持异步请求

为了支持异步请求，我们需要在 `HttpServletRequestImpl` 中引入 `AsyncContext`，并修改 `HttpServletRequestImpl` 类以支持异步任务的启动。

```java
public class HttpServletRequestImpl  implements HttpServletRequest {
         ....
    private boolean asyncStarted = false;
    private AsyncContext asyncContext;

    public HttpServletRequestImpl(String method, String requestURI, String queryString, Map<String, String> headers) {
        ......
    }

    @Override
    public boolean isAsyncStarted() {
        return asyncStarted;
    }

    @Override
    public AsyncContext getAsyncContext() {
        if (!asyncStarted) {
            throw new IllegalStateException("Async not started");
        }
        return asyncContext;
    }


    @Override
    public AsyncContext startAsync(ServletRequest servletRequest, ServletResponse servletResponse) throws IllegalStateException {
        if (asyncStarted) {
            throw new IllegalStateException("Async already started");
        }
        asyncStarted = true;
        asyncContext = new AsyncContextImpl(this, servletResponse);
        return asyncContext;
    }

    @Override
    public boolean isAsyncSupported() {
        return asyncStarted;
    }
    .....
}
```

#### 8.3.2 修改 `HttpProcessor` 类，支持异步请求

在 `HttpProcessor` 中，我们需要判断当前请求是否需要异步处理。如果是，调用 `startAsync()` 启动异步请求。

```java
package com.daicy.minitomcat;

import com.daicy.minitomcat.servlet.HttpServletRequestImpl;
import com.daicy.minitomcat.servlet.HttpServletResponseImpl;

import javax.servlet.AsyncContext;
import javax.servlet.http.HttpServletRequest;
import java.io.*;
import java.net.Socket;
import java.util.HashMap;
import java.util.Map;

public class HttpProcessor implements Runnable{
    private Socket socket;

    private final static  ServletProcessor servletProcessor = new ServletProcessor();

    private final static  StaticResourceProcessor staticProcessor = new StaticResourceProcessor();

    public HttpProcessor(Socket socket) {
        this.socket = socket;
    }

    @Override
    public void run() {
        // 处理请求并返回响应
        process();
    }

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
            String uri = request.getRequestURI();
            WebXmlServletContainer parser = HttpServer.parser;
            String servletName = parser.getServletName(uri);
            if (uri.endsWith(".html") || uri.endsWith(".css") || uri.endsWith(".js")) {
                staticProcessor.process(request, response);
            }else if (null != servletName)  {
                // 普通请求处理
                servletProcessor.process(request, response);
            }else {
                send404Response(outputStream);
            }

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

    private boolean parseKeepAliveHeader(HttpServletRequest request) {
        String connectionHeader = request.getHeader("Connection");
        return connectionHeader != null && connectionHeader.equalsIgnoreCase("keep-alive");
    }

    public boolean isCloseConnection(HttpServletRequest request) {
        String connectionHeader = request.getHeader("Connection");
        return connectionHeader != null && connectionHeader.equalsIgnoreCase("close");
    }

    static void send404Response(OutputStream outputStream) {
        sendResponse(outputStream, 404, "Not Found", "The requested resource was not found.");
    }


    // 发送普通文本响应
    private static void sendResponse(OutputStream outputStream, int statusCode, String statusText, String message)  {
        PrintWriter writer = new PrintWriter(new OutputStreamWriter(outputStream));
        String html = "<html><body><h1>" + statusCode + " " + statusText + "</h1><p>" + message + "</p></body></html>";
        writer.println("HTTP/1.1 " + statusCode + " " + statusText);
        writer.println("Content-Type: text/html; charset=UTF-8");
        writer.println("Content-Length: " + html.length());
        writer.println();
        writer.println(html);
    }

} 
```

### 8.3.3 实现 `AsyncContext` 类

`AsyncContext` 是 Servlet 3.0 异步请求处理的核心接口。它提供了异步请求的生命周期管理、后台线程启动及任务完成的处理机制。在 `MiniTomcat` 中，我们需要自定义一个简单的 `AsyncContext` 类，负责管理异步请求的相关操作。

#### 1\. `AsyncContextImpl` 类实现

`AsyncContextImpl` 类是我们自定义的 `AsyncContext` 接口实现类，主要负责以下功能：

+   **start()**：启动异步请求处理任务，将任务分配给后台线程。
    
+   **complete()**：完成异步请求并发送响应。
    
+   **getRequest()**：返回当前的请求对象。
    
+   **getResponse()**：返回当前的响应对象。
    

```java
package com.daicy.minitomcat.servlet;

import javax.servlet.*;
import java.io.IOException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class AsyncContextImpl implements AsyncContext {

    private ServletRequest request;

    private ServletResponse response;

    private static ExecutorService executor = Executors.newCachedThreadPool();


    public AsyncContextImpl(ServletRequest request, ServletResponse response) {
        this.request = request;
        this.response = response;
    }

    @Override
    public void start(Runnable run) {
        executor.submit(run);
    }

    @Override
    public void complete() {
        try {
            // 完成异步响应
            HttpServletResponseImpl response = (HttpServletResponseImpl) this.response;
            response.sendResponse();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public ServletRequest getRequest() {
        return null;
    }

    @Override
    public ServletResponse getResponse() {
        return null;
    }

    @Override
    public boolean hasOriginalRequestAndResponse() {
        return false;
    }

    @Override
    public void dispatch() {

    }

    @Override
    public void dispatch(String path) {

    }

    @Override
    public void dispatch(ServletContext context, String path) {

    }


    @Override
    public void addListener(AsyncListener listener) {

    }

    @Override
    public void addListener(AsyncListener listener, ServletRequest servletRequest, ServletResponse servletResponse) {

    }

    @Override
    public <T extends AsyncListener> T createListener(Class<T> clazz) throws ServletException {
        return null;
    }

    @Override
    public void setTimeout(long timeout) {

    }

    @Override
    public long getTimeout() {
        return 0;
    }
}
```

### 8.3.4 实现 `AsyncServlet` 类

`AsyncServlet` 是一个简单的异步 Servlet，用于测试 异步 功能，每次访问该 Servlet 时，都会有有延迟并异步执行。

```java
package com.daicy.minitomcat;

import java.io.IOException;
import javax.servlet.AsyncContext;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class AsyncServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        AsyncContext asyncContext = request.startAsync(request,response);
        asyncContext.start(() -> {
            try {
                Thread.sleep(2000); // 模拟耗时操作
                response.getWriter().write("异步响应完成");
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                asyncContext.complete();
            }
        });
    }
}
```

### 8.4 测试

1.  启动服务器并访问支持异步操作的 URL，例如 `/async`。
    

### 8.5 学习收获

+   **Servlet 异步处理机制**：通过 `AsyncContext` 和 `startAsync()`，我们成功实现了异步请求处理。在高并发情况下，这能够显著提升服务器的响应速度和吞吐量。
    
+   **线程管理**：通过异步处理机制，将长时间操作的任务分配给后台线程，避免了阻塞主线程。
    
+   **性能优化**：引入异步处理使得服务器能够同时响应多个请求，优化了对高并发场景的支持。
    

通过实现这一功能，我们为 `MiniTomcat` 增添了更强的并发处理能力，特别是在面对长时间任务时，能够有效地提升整体的性能。

项目源代码地址：

https://github.com/daichangya/MiniTomcat/tree/chapter8/mini-tomcat