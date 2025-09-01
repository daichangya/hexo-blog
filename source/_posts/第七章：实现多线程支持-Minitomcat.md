---
title: 第七章：实现多线程支持-Minitomcat
id: ce221da0-dac1-4f4e-9ce1-71be83ac991b
date: 2024-11-19 10:58:36
author: daichangya
cover: https://images.jsdiff.com/tomcat192.jpg
excerpt: "在这一阶段，我们将为 MiniTomcat 添加多线程支持，以提高服务器的并发处理能力。通过使用线程池，我们能够同时处理多个客户端请求，而不阻塞其他请求。这将使服务器在处理并发请求时更加高效，能够更好地支持多个用户同时访问。 7.1 功能目标 多线程支持：使用线程池来管理线程，并为每个客户端请求分配"
permalink: /archives/di-qi-zhang-shi-xian-duo-xian-cheng-zhi-chi-minitomcat/
categories:
 - minitomcat
tags: 
 - tomcat
---

在这一阶段，我们将为 MiniTomcat 添加多线程支持，以提高服务器的并发处理能力。通过使用线程池，我们能够同时处理多个客户端请求，而不阻塞其他请求。这将使服务器在处理并发请求时更加高效，能够更好地支持多个用户同时访问。

### 7.1 功能目标

+   **多线程支持**：使用线程池来管理线程，并为每个客户端请求分配一个独立的线程。
    
+   **线程池**：避免为每个请求创建新线程，通过线程池提高效率，防止线程创建和销毁的开销。
    
+   **并发处理**：支持多个客户端同时访问不同的 Servlet，保证请求之间互不干扰。
    

### 7.2 代码结构

本次修改将引入线程池机制，通过 `ExecutorService` 来管理工作线程。代码结构更新如下：

```
MiniTomcat
├─ src
│ ├─ main
│ │ ├─ java
│ │ │ ├─ com.daicy.minitomcat
│ │ │ │ ├─ servlet
│ │ │ │ │ ├─ CustomServletOutputStream.java // 自定义的 Servlet 输出流类
│ │ │ │ │ ├─ CustomHttpSession.java // 自定义的 HttpSession
│ │ │ │ │ ├─ HttpServletRequestImpl.java // HTTP 请求的实现类
│ │ │ │ │ ├─ HttpServletResponseImpl.java // HTTP 响应的实现类
│ │ │ │ │ ├─ ServletConfigImpl.java // Servlet 配置的实现类
│ │ │ │ │ ├─ ServletContextImpl.java // Servlet 上下文的实现类
│ │ │ │ ├─ CounterServlet.java // session功能 Servlet 示例类
│ │ │ │ ├─ HelloServlet.java // Servlet 示例类
│ │ │ │ ├─ HttpConnector.java // 连接器类
│ │ │ │ ├─ HttpProcessor.java // 请求处理器
│ │ │ │ ├─ HttpServer.java // 主服务器类
│ │ │ │ ├─ HttpRequestParser.java // HttpRequest信息解析类
│ │ │ │ ├─ ServletLoader.java // Servlet 加载器
│ │ │ │ ├─ ServletProcessor.java // Servlet 处理器
│ │ │ │ ├─ StaticResourceProcessor.java// 静态资源处理器
│ │ │ │ ├─ SessionManager.java // SessionManager
│ │ │ │ ├─ ThreadPool.java           // 线程池管理
│ │ │ │ ├─ WebXmlServletContainer.java // Servlet 容器相关类
│ │ ├─ resources
│ │ │ ├─ webroot
│ │ │ │ ├─ index.html
│ │ │ ├─ web.xml
│ ├─ test
├─ pom.xml
```

### 7.3 代码实现

#### 7.3.1 创建 `ThreadPool` 类

我们将使用 `ThreadPoolExecutor` 来实现线程池。`ThreadPool` 类将管理线程池的生命周期，提供一个执行请求的接口。

```java
package com.daicy.minitomcat;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

public class ThreadPool {
    private ExecutorService executor;

    public ThreadPool(int poolSize) {
        executor = Executors.newFixedThreadPool(poolSize);
    }

    public void submitTask(Runnable task) {
        executor.submit(task);
    }

    public void shutdown() {
        if (executor != null) {
            executor.shutdown();
        }
    }

    public boolean isShutdown() {
        return executor.isShutdown();
    }

    public ThreadPoolExecutor getExecutor() {
        return (ThreadPoolExecutor) executor;
    }
}
```

#### 7.3.2 修改 `HttpProcessor` 类以支持多线程

`HttpProcessor` 类将通过线程池来处理每一个客户端的请求。每个请求将由线程池中的一个线程来处理，从而避免阻塞。

```java
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
......
}
```

#### 7.3.3 修改 `HttpConnector` 类以启动线程池

`HttpConnector` 类负责启动服务器，并利用线程池处理客户端连接。

```java
package com.daicy.minitomcat;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

public class HttpConnector implements Runnable {
    private static final int PORT = 8080;

    private static ThreadPool threadPool = new ThreadPool(10);  // 创建一个线程池，最多支持 10 个并发请求

    public void start() {
        Thread thread = new Thread(this);
        thread.start();
    }

    @Override
    public void run() {
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("HTTP Connector is running on port " + PORT);

            while (true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println("Accepted connection from " + clientSocket.getInetAddress());

                // 将连接交给 HttpProcessor 处理
                HttpProcessor processor = new HttpProcessor(clientSocket);
                threadPool.submitTask(processor);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

### 7.4 测试

1.  启动服务器并访问多个客户端请求，确保每个请求都能够同时得到处理而不会阻塞。
    
2.  使用多个浏览器或 HTTP 客户端同时访问不同的路径，验证服务器能并发处理多个请求。
    
3.  观察服务器的性能和响应时间，确保线程池有效提高了并发能力。
    

### 7.5 学习收获

+   **线程池**：了解了线程池的概念，如何使用 `ExecutorService` 和 `ThreadPoolExecutor` 来管理线程并避免创建过多线程的开销。
    
+   **多线程编程**：深入理解了如何将多线程引入 Web 服务器，实现并发处理请求，提升服务器的吞吐量和响应速度。
    
+   **并发安全**：学习了如何设计并发安全的服务器，使多个请求能够同时处理而互不干扰。
    

项目源代码地址：

https://github.com/daichangya/MiniTomcat/tree/chapter7/mini-tomcat