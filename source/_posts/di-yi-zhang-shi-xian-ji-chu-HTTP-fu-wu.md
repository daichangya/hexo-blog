---
title: 第一章：实现基础 HTTP 服务器-MiniTomcat
id: 562071c9-c324-40bb-bec9-dc498038c568
date: 2024-11-07 13:07:59
author: daichangya
cover: https://images.jsdiff.com/MiniTomcat4.jpg
excerpt: 在这一章中，我们将从零开始编写一个简单的 HTTP 服务器。这个服务器的基本功能是监听一个端口，接收来自客户端的 HTTP 请求，并返回一个 HTTP
  响应。我们将使用 Java 的 ServerSocket 类来实现网络监听，并通过简单的 InputStream 和 OutputStream 来处
permalink: /archives/di-yi-zhang-shi-xian-ji-chu-HTTP-fu-wu/
categories:
- minitomcat
tags:
- tomcat
---

在这一章中，我们将从零开始编写一个简单的 HTTP 服务器。这个服务器的基本功能是监听一个端口，接收来自客户端的 HTTP 请求，并返回一个 HTTP 响应。我们将使用 Java 的 `ServerSocket` 类来实现网络监听，并通过简单的 `InputStream` 和 `OutputStream` 来处理 HTTP 请求和响应。

#### **1.1 创建基础 HTTP 服务器**

我们的目标是创建一个能够监听客户端请求的 HTTP 服务器，并能返回一个简单的响应。我们将分为几个步骤：

1.  **创建一个 ServerSocket 监听端口**：使用 `ServerSocket` 类来创建一个监听指定端口的服务器套接字。
    
2.  **接受客户端连接并接收请求**：通过 `Socket` 接受客户端的连接，并从输入流读取 HTTP 请求。
    
3.  **发送 HTTP 响应**：构建一个简单的 HTTP 响应并通过输出流发送给客户端。
    

#### **1.2 实现代码**

```java
import java.io.*;
import java.net.*;

public class SimpleHttpServer {
    private static final int PORT = 8080;

    public static void main(String[] args) {
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("HTTP Server is running on port " + PORT);

            while (true) {
                // 接受客户端连接
                Socket clientSocket = serverSocket.accept();
                System.out.println("New connection from " + clientSocket.getInetAddress());

                // 获取输入流，读取客户端请求
                InputStream inputStream = clientSocket.getInputStream();
                BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
                String requestLine = reader.readLine();
                if (requestLine != null) {
                    System.out.println("Request: " + requestLine);
                }

                // 构建一个简单的 HTTP 响应
                OutputStream outputStream = clientSocket.getOutputStream();
                PrintWriter writer = new PrintWriter(outputStream, true);
                writer.println("HTTP/1.1 200 OK");
                writer.println("Content-Type: text/html; charset=UTF-8");
                writer.println();  // 空行，表示响应头结束
                writer.println("<html>");
                writer.println("<head><title>Simple HTTP Server</title></head>");
                writer.println("<body><h1>Hello, World!</h1></body>");
                writer.println("</html>");

                // 关闭连接
                clientSocket.close();
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

#### **1.3 代码解析**

1.  **创建 ServerSocket 实例**：
    
    ```java
    ServerSocket serverSocket = new ServerSocket(PORT);
    ```
    
    这行代码创建了一个监听指定端口（本例为 8080）的 `ServerSocket` 实例。`ServerSocket` 是 Java 提供的一个用于监听客户端连接的类。
    
2.  **接受客户端连接**：
    
    ```java
    Socket clientSocket = serverSocket.accept();
    ```
    
    通过调用 `accept()` 方法，服务器会阻塞并等待来自客户端的连接。一旦有客户端连接到服务器，就会返回一个 `Socket` 对象，代表与该客户端的连接。
    
3.  **读取 HTTP 请求**：
    
    ```java
    BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
    String requestLine = reader.readLine();
    ```
    
    通过输入流，我们从客户端读取 HTTP 请求的第一行（请求行），例如 `GET / HTTP/1.1`。这是 HTTP 请求的最基础信息，包含了请求方法、路径和 HTTP 版本。
    
4.  **发送 HTTP 响应**：
    
    ```java
    PrintWriter writer = new PrintWriter(outputStream, true);
    writer.println("HTTP/1.1 200 OK");
    writer.println("Content-Type: text/html; charset=UTF-8");
    writer.println();
    writer.println("<html>");
    writer.println("<head><title>Simple HTTP Server</title></head>");
    writer.println("<body><h1>Hello, World!</h1></body>");
    writer.println("</html>");
    ```
    
    构建一个简单的 HTTP 响应，响应内容为一个 HTML 页面，显示 "Hello, World!"。首先，我们发送 HTTP 响应的状态行，紧接着发送响应头（如 `Content-Type`）。响应体部分包含了一个简单的 HTML 页面。
    
5.  **关闭连接**：
    
    ```java
    clientSocket.close();
    ```
    
    每次处理完一个请求后，我们关闭与客户端的连接。
    

#### **1.4 测试 HTTP 服务器**

1.  编译并运行 `SimpleHttpServer` 类。
    
2.  在浏览器中访问 `http://localhost:8080`，你应该会看到一个显示 "Hello, World!" 的网页。
    
3.  你也可以使用 curl 命令来测试服务器：
    
    ```bash
    curl http://localhost:8080
    ```
    

#### **1.5 总结**

通过这一章，我们实现了一个非常简单的 HTTP 服务器，能够监听来自客户端的请求，并返回一个静态的 HTML 页面。这个 HTTP 服务器只是一个最基本的框架，但它为我们后续增加更多功能（如静态文件支持、Servlet 容器等）奠定了基础。

在下一章，我们将开始解析 HTTP 请求，并支持静态文件的提供。

文章出处：

https://blog.jsdiff.com/archives/di-1bu-shi-xian-ji-chu-http-fu-wu-qi

项目源代码地址：

https://github.com/daichangya/MiniTomcat/tree/chapter1/mini-tomcat