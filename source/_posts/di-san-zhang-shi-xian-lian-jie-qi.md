---
title: 第三章：实现连接器（Connector）组件-MiniTomcat
id: 15250a83-725d-4db0-a519-c99d937192a4
date: 2024-11-09 23:46:27
author: daichangya
cover: https://images.jsdiff.com/MiniTomcat3.jpg
excerpt: 上一章内容：第二章：解析 HTTP 请求，支持静态文件-MiniTomcat 在本章节中，我们将引入连接器（Connector）组件，用于管理 HTTP
  连接和请求数据的解析。连接器的作用是负责客户端的网络连接，同时解耦网络传输和请求处理的逻辑。 3.1 功能目标 管理 HTTP 连接：连接器组件负
permalink: /archives/di-san-zhang-shi-xian-lian-jie-qi/
categories:
- minitomcat
tags:
- tomcat
---

上一章内容：[第二章：解析 HTTP 请求，支持静态文件-MiniTomcat](https://blog.jsdiff.com/archives/di-er-zhang-jie-xi-http-qing-qiu-zhi-chi-jing-tai-wen-jian)

在本章节中，我们将引入连接器（Connector）组件，用于管理 HTTP 连接和请求数据的解析。连接器的作用是负责客户端的网络连接，同时解耦网络传输和请求处理的逻辑。

### 3.1 功能目标

+   **管理 HTTP 连接**：连接器组件负责与客户端建立连接，监听和读取传入的数据包。
    
+   **解耦网络传输和请求解析**：连接器将网络传输逻辑和请求处理逻辑分离，提升代码的清晰度和容错性。
    

### 3.2 代码结构

以下是 MiniTomcat 项目的基本代码结构，我们在 com.daicy.minitomcat 包中添加 `HttpConnector` ， `HttpProcessor，Request`，`Response`，`StaticResourceProcessor` 几个类,同时修改`SimpleHttpServer` 为`HttpServer`。

```
MiniTomcat
├─ src
│  ├─ main
│  │  ├─ java
│  │  │  ├─ com.daicy.minitomcat
│  │  │  │  ├─ HttpConnector.java          // 连接器类
│  │  │  │  ├─ HttpProcessor.java          // 请求处理器
│  │  │  │  ├─ HttpServer.java             // 主服务器类
│  │  │  │  ├─ Request.java                // 请求封装类
│  │  │  │  ├─ Response.java               // 响应封装类
│  │  │  │  ├─ StaticResourceProcessor.java // 静态资源处理器
│  │  ├─ resources
│  ├─ test
│  ├─ webroot
│  │  ├─ index.html
├─ pom.xml
```

### 3.3 代码实现

#### 3.3.1 创建 `HttpConnector` 类

`HttpConnector` 作为服务器的连接器类，负责监听指定端口，接受客户端连接，并将请求交给 `HttpProcessor` 进行处理。

```java
package com.daicy.minitomcat;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

public class HttpConnector implements Runnable {
    private static final int PORT = 8080;

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
                processor.process();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

#### 3.3.2 创建 `HttpProcessor` 类

`HttpProcessor` 类负责处理传入的 HTTP 请求，将请求解析为 `Request` 对象，并构建响应。

```java
package com.daicy.minitomcat;

import java.io.*;
import java.net.Socket;

public class HttpProcessor {
    private Socket socket;

    private StaticResourceProcessor staticProcessor = new StaticResourceProcessor();


    public HttpProcessor(Socket socket) {
        this.socket = socket;
    }

    public void process() {
        try (InputStream inputStream = socket.getInputStream();
             OutputStream outputStream = socket.getOutputStream()) {

            // 解析请求
            Request request = parseRequest(inputStream);

            // 构建响应
            Response response = new Response(outputStream);
            if(null == request){
                return;
            }
            String uri = request.getUri();
            if (uri.endsWith(".html") || uri.endsWith(".css") || uri.endsWith(".js")) {
                staticProcessor.process(request, response);
            } else {
                staticProcessor.process(request, response);
            }

        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                socket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private Request parseRequest(InputStream inputStream) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));

        String requestLine = reader.readLine();
        if (requestLine == null || requestLine.isEmpty()) {
            return null;
        }

        System.out.println("Request Line: " + requestLine);
        String[] parts = requestLine.split(" ");
        String method = parts[0];
        String path = parts[1];

        return new Request(method, path);
    }

}
```

#### 3.3.3 创建 `StaticResourceProcessor` 类

`StaticResourceProcessor` 类负责查找读取静态文件，并构建响应。

```java
package com.daicy.minitomcat;

import java.io.*;
import java.net.URL;

import static com.daicy.minitomcat.HttpServer.WEB_ROOT;

public class StaticResourceProcessor {
    public void process(Request request, Response response) {
        try {

            OutputStream outputStream = response.getOutputStream();
            // 查找请求的静态文件
            String path = request.getUri();
            URL url = HttpServer.class.getClassLoader().getResource(WEB_ROOT+ path);
            if(null == url){
                sendResponse(outputStream, 404, "Not Found", "The requested resource was not found.");
                return;
            }
            File file = new File(url.getPath());
            if (file.exists() && !file.isDirectory()) {
                sendFileResponse(outputStream, file);
            } else {
                sendResponse(outputStream, 404, "Not Found", "The requested resource was not found.");
            }
        }catch (IOException e){
            e.printStackTrace();
        }
    }

    // 发送普通文本响应
    private static void sendResponse(OutputStream outputStream, int statusCode, String statusText, String message) throws IOException {
        PrintWriter writer = new PrintWriter(outputStream, true);
        writer.println("HTTP/1.1 " + statusCode + " " + statusText);
        writer.println("Content-Type: text/html; charset=UTF-8");
        writer.println();
        writer.println("<html><body><h1>" + statusCode + " " + statusText + "</h1><p>" + message + "</p></body></html>");
    }

    // 发送文件响应
    private static void sendFileResponse(OutputStream outputStream, File file) throws IOException {
        PrintWriter writer = new PrintWriter(outputStream, true);
        writer.println("HTTP/1.1 200 OK");
        writer.println("Content-Type: " + getContentType(file));
        writer.println("Content-Length: " + file.length());
        writer.println();

        // 发送文件内容
        try (FileInputStream fis = new FileInputStream(file)) {
            byte[] buffer = new byte[1024];
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                outputStream.write(buffer, 0, bytesRead);
            }
        }
    }

    // 根据文件后缀返回 Content-Type
    private static String getContentType(File file) {
        String name = file.getName().toLowerCase();
        if (name.endsWith(".html") || name.endsWith(".htm")) {
            return "text/html";
        } else if (name.endsWith(".css")) {
            return "text/css";
        } else if (name.endsWith(".js")) {
            return "application/javascript";
        } else if (name.endsWith(".jpg") || name.endsWith(".jpeg")) {
            return "image/jpeg";
        } else if (name.endsWith(".png")) {
            return "image/png";
        } else {
            return "application/octet-stream";
        }
    }
}
```

#### 3.3.4 `Request` 和 `Response` 类

`Request` 封装客户端请求数据，而 `Response` 用于生成和发送服务器响应。

```java
package com.daicy.minitomcat;

public class Request {
    private String method;
    private String path;

    public Request(String method, String path) {
        this.method = method;
        this.path = path;
    }

    public String getMethod() {
        return method;
    }

    public String getPath() {
        return path;
    }
}
```

```java
package com.daicy.minitomcat;

import java.io.*;
import java.net.URL;

public class Response {
    private OutputStream outputStream;

    public Response(OutputStream outputStream) {
        this.outputStream = outputStream;
    }

    public OutputStream getOutputStream() {
        return outputStream;
    }
}
```

#### 3.3.5 启动 `HttpConnector`

`HttpServer` 类作为服务器的入口，用于启动 `HttpConnector`，并接受客户端请求。

```java
package com.daicy.minitomcat;

public class HttpServer {
    public static void main(String[] args) {
        HttpConnector connector = new HttpConnector();
        connector.start();
    }
}
```

### 3.4 代码解析

1.  **连接器的创建**：
    
    +   `HttpConnector` 监听指定端口，当客户端连接建立后，创建新的 `HttpProcessor` 线程处理该连接。
        
    +   连接器与请求处理器解耦，每个连接的处理逻辑独立。
        
2.  **请求解析**：
    
    +   `HttpProcessor` 读取并解析请求行，构建 `Request` 对象，提取方法和路径信息。
        
    +   简化了请求解析的逻辑，确保连接器和处理器职责分离。
        
3.  **响应生成**：
    
    +   `StaticResourceProcessor` 类根据 `Request` 的路径生成响应内容，支持静态资源返回。
        
    +   响应类可以灵活扩展，如支持更多类型的请求和响应。
        

### 3.5 学习收获

通过实现连接器，我们实现了网络传输与请求处理的解耦：

+   **职责分离**：将网络连接和请求解析分别交由连接器和处理器管理，提升了代码的可读性和维护性。
    
+   **面向组件设计**：连接器作为服务器组件之一，符合后续扩展不同类型连接（如 HTTPS）的需求。
    

项目源代码地址：

https://github.com/daichangya/MiniTomcat/tree/chapter3/mini-tomcat