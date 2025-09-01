---
title: Java 网络基础-MiniTomcat系列课程准备
id: 09453b64-056d-4a30-948d-c611c35fa8f6
date: 2024-11-19 09:50:34
author: daichangya
cover: https://images.jsdiff.com/MiniTomcat313.jpg
excerpt: "在这个模块中，我们将深入学习 Java 网络编程的基础知识。这些技能是构建 MiniTomcat 必不可少的，因为 MiniTomcat 需要通过 HTTP 协议与客户端（如浏览器）进行通信。掌握网络编程的基本概念将帮助我们更好地理解 HTTP 连接、请求和响应等重要组件的实现。 1. Java 网"
permalink: /archives/java-wang-luo-ji-chu/
categories:
 - minitomcat
---

在这个模块中，我们将深入学习 Java 网络编程的基础知识。这些技能是构建 MiniTomcat 必不可少的，因为 MiniTomcat 需要通过 HTTP 协议与客户端（如浏览器）进行通信。掌握网络编程的基本概念将帮助我们更好地理解 HTTP 连接、请求和响应等重要组件的实现。

* * *

### 1\. Java 网络编程概览

Java 中的网络编程通过 **Socket** 和 **ServerSocket** 类实现。Socket 是网络通信的基础，允许我们在客户端和服务器之间传输数据。

+   **Socket**：用于客户端，与服务器建立连接并进行数据交换。
    
+   **ServerSocket**：用于服务器，监听客户端连接请求并响应。
    

### 2\. 了解 TCP 和 UDP

在网络通信中，常见的协议有两种：

+   **TCP（传输控制协议）**：面向连接，数据传输可靠，适用于 HTTP 等需要可靠传输的协议。
    
+   **UDP（用户数据报协议）**：无连接，数据传输不可靠但速度快，适用于视频流、在线游戏等应用。
    

在 MiniTomcat 中，我们主要使用 TCP 协议来处理客户端的 HTTP 请求。

### 3\. 使用 Socket 和 ServerSocket

#### 3.1 创建服务器端 (ServerSocket)

通过 `ServerSocket`，我们可以创建一个服务器并等待客户端的连接请求。示例如下：

```
import java.io.*;
import java.net.*;

public class SimpleServer {
    public static void main(String[] args) {
        try (ServerSocket serverSocket = new ServerSocket(8080)) {
            System.out.println("Server is listening on port 8080");
            while (true) {
                Socket socket = serverSocket.accept();
                System.out.println("New client connected");
                
                // 处理客户端请求
                InputStream input = socket.getInputStream();
                BufferedReader reader = new BufferedReader(new InputStreamReader(input));
                String line;
                while ((line = reader.readLine()) != null) {
                    System.out.println(line);
                    if (line.isEmpty()) break;
                }
                socket.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

#### 3.2 创建客户端 (Socket)

客户端通过 `Socket` 连接服务器，发送请求并接收响应。示例如下：

```
import java.io.*;
import java.net.*;

public class SimpleClient {
    public static void main(String[] args) {
        try (Socket socket = new Socket("localhost", 8080)) {
            OutputStream output = socket.getOutputStream();
            PrintWriter writer = new PrintWriter(output, true);
            writer.println("Hello, Server!");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

### 4\. 实践任务 📝

1.  **创建一个简单的 Java 服务器**，监听特定端口并接受客户端的连接。
    
2.  **创建一个 Java 客户端**，连接到你刚创建的服务器，并发送一条简单的信息。
    

* * *

这些练习将帮助你理解服务器和客户端之间的基本通信方式。完成后，你将为实现 MiniTomcat 的 HTTP 连接组件做好准备！有疑问随时问我 🦌