---
title: 第二章：解析 HTTP 请求，支持静态文件-MiniTomcat
id: 7594e301-3106-46a7-a735-facb379d458d
date: 2024-11-07 15:36:52
author: daichangya
cover: https://images.jsdiff.com/MiniTomcat312.jpg
excerpt: "上一章内容 第一章：实现基础 HTTP 服务器-MiniTomcat 在本章节中，我们将为 HTTP 服务器增加对请求路径、方法和头部信息的解析能力，并基于请求路径返回服务器上的静态文件内容。通过实现这一功能，我们将使服务器能够类似于静态资源服务器，为客户端提供 HTML、CSS、JavaScrip"
permalink: /archives/di-er-zhang-jie-xi-http-qing-qiu-zhi-chi-jing-tai-wen-jian/
categories:
 - minitomcat
tags: 
 - tomcat
---

上一章内容 [第一章：实现基础 HTTP 服务器-MiniTomcat](https://blog.jsdiff.com/archives/di-1bu-shi-xian-ji-chu-http-fu-wu-qi)

在本章节中，我们将为 HTTP 服务器增加对请求路径、方法和头部信息的解析能力，并基于请求路径返回服务器上的静态文件内容。通过实现这一功能，我们将使服务器能够类似于静态资源服务器，为客户端提供 HTML、CSS、JavaScript 等文件的访问。

### 2.1 功能目标

+   **解析 HTTP 请求**：识别请求路径、请求方法（如 `GET`、`POST`）。
    
+   **静态文件支持**：根据请求路径查找服务器上的文件（如 `index.html`），返回文件内容。
    
+   **MIME 类型支持**：根据文件类型设置正确的 `Content-Type` 响应头，确保浏览器可以正确解析文件。
    

### 2.2 代码实现

我们将扩展之前的 `SimpleHttpServer` 类，增加对 HTTP 请求解析的逻辑，并在服务器文件系统中查找并返回请求的静态文件。

```java
import java.io.*;
import java.net.*;

public class SimpleHttpServer {
    private static final int PORT = 8080;
    private static final String WEB_ROOT = "webroot"; // 静态文件根目录

    public static void main(String[] args) {
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("HTTP Server is running on port " + PORT);

            while (true) {
                // 接受客户端连接
                Socket clientSocket = serverSocket.accept();
                System.out.println("New connection from " + clientSocket.getInetAddress());

                // 处理请求并发送响应
                handleRequest(clientSocket);
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void handleRequest(Socket clientSocket) {
        try (InputStream inputStream = clientSocket.getInputStream();
             OutputStream outputStream = clientSocket.getOutputStream();
             BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream))) {

            // 读取并解析请求行
            String requestLine = reader.readLine();
            if (requestLine == null || requestLine.isEmpty()) return;
            System.out.println("Request: " + requestLine);

            // 解析请求方法和路径
            String[] parts = requestLine.split(" ");
            String method = parts[0];
            String path = parts[1];

            // 检查是否为 GET 请求
            if (!method.equals("GET")) {
                sendResponse(outputStream, 405, "Method Not Allowed", "Only GET method is supported.");
                return;
            }
            // 查找请求的静态文件
            URL url = SimpleHttpServer.class.getClassLoader().getResource(WEB_ROOT+ path);
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

        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                clientSocket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
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

### 2.3 代码解析

1.  **请求解析**：
    
    ```
    > GET /index.html HTTP/1.1
    > Host: localhost:8080
    > User-Agent: curl/8.7.1
    > Accept: */*
    > Proxy-Connection: Keep-Alive
    ```
    
    上面是一个普通的Http请求传输的文本，我们目前只需要解析第一行
    
    ```java
    String requestLine = reader.readLine();
    String[] parts = requestLine.split(" ");
    String method = parts[0];
    String path = parts[1];
    ```
    
    我们读取请求行，并将其按空格分割，从而提取请求方法和路径。这里仅支持 `GET` 请求，对于其他请求方法返回 405 错误。
    
2.  **静态文件查找**：
    
    ```java
    // 查找请求的静态文件
    URL url = Resources.getResource(WEB_ROOT+ path);
    File file = new File(url.getPath())
    ```
    
    将请求的路径和服务器的根目录 `WEB_ROOT` 拼接，找到相应的文件。如果文件存在且不是目录，就返回该文件的内容，否则返回 404 错误。
    
3.  **文件响应**：
    
    ```java
    try (FileInputStream fis = new FileInputStream(file)) {
       byte[] buffer = new byte[1024];
       int bytesRead;
       while ((bytesRead = fis.read(buffer)) != -1) {
           outputStream.write(buffer, 0, bytesRead);
       }
    }
    ```
    
    我们通过文件流读取文件内容，并将其写入输出流发送给客户端。
    
4.  **MIME 类型判断**：
    
    ```java
    private static String getContentType(File file) { ... }
    ```
    
    根据文件后缀来确定文件的 MIME 类型，从而设置正确的 `Content-Type`，如 `text/html`、`application/javascript`，确保客户端能正确解析文件内容。
    
5.  **完整的响应信息文本**：
    
    ```
    < HTTP/1.1 200 OK
    < Content-Length: 111
    < Connection: keep-alive
    < Content-Type: text/html
    < Keep-Alive: timeout=4
    < Proxy-Connection: keep-alive
    < 
    <!DOCTYPE html>
    <html>
    <head><title>Test Page</title></head>
    <body><h1>This is a test page.</h1></body>
    </html>%            
    ```
    

### 2.4 测试静态文件支持

1.  在项目根目录下创建 `webroot` 文件夹，并放入测试文件 `index.html`：
    
    ```html
    <!DOCTYPE html>
    <html>
    <head><title>Test Page</title></head>
    <body><h1>This is a test page.</h1></body>
    </html>
    ```
    
2.  启动服务器，并在浏览器中访问 `http://localhost:8080/index.html`，应显示 `index.html` 的内容。
    
3.  请求一个不存在的文件（如 `http://localhost:8080/notfound.html`），应返回 404 错误。
    

### 2.5 学习收获

通过本章节的实现，我们深入理解了以下知识点：

+   **HTTP 请求解析**：解析请求的路径、方法，处理不同请求的基本逻辑。
    
+   **静态文件的处理**：利用文件系统中的路径查找和返回内容，为客户端提供静态资源的访问。
    
+   **响应头的设置**：根据请求的文件类型，设置 `Content-Type` 响应头，从而确保客户端正确渲染不同类型的文件。
    

项目源代码地址：

https://github.com/daichangya/MiniTomcat/tree/chapter2/mini-tomcat

在下一章中，我们将继续实现连接器组件，以便进一步解耦网络连接处理和请求解析。