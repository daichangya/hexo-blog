---
title: HTTP 请求与响应的封装 - HttpServletRequest 和 HttpServletResponse-MiniTomcat系列课程准备
id: 0b2ca861-c04a-4e90-981c-25b4b68f8c6f
date: 2024-11-19 10:01:45
author: daichangya
cover: https://images.jsdiff.com/MiniTomcat313.jpg
excerpt: "在 MiniTomcat 的开发过程中，我们需要将请求数据从低级的 Socket 输入输出流中抽象出来，以简化后续处理和响应的构建。通过创建 HttpServletRequest 和 HttpServletResponse 接口，我们可以为开发者提供更易用的请求和响应操作接口，类似于标准的 Serv"
permalink: /archives/http-qing-qiu-yu-xiang-ying-de-feng-zhuang/
categories:
 - minitomcat
---

在 MiniTomcat 的开发过程中，我们需要将请求数据从低级的 Socket 输入输出流中抽象出来，以简化后续处理和响应的构建。通过创建 `HttpServletRequest` 和 `HttpServletResponse` 接口，我们可以为开发者提供更易用的请求和响应操作接口，类似于标准的 Servlet API。

* * *

### 1\. HttpServletRequest 接口设计

`HttpServletRequest` 是对客户端请求的抽象封装，主要包含请求方法、URL、头信息、参数等。

#### 1.1 主要属性

+   **请求方法**（如 GET、POST）
    
+   **请求路径**（如 `/index.html`）
    
+   **请求头**（如 `User-Agent`、`Accept` 等）
    
+   **请求参数**（GET 参数和 POST 参数）
    
+   **Cookie 和 Session**：用于跟踪用户状态（后续会进一步实现）
    

#### 1.2 主要方法

<table style="width: 672px"><colgroup><col style="width: 262px"><col style="width: 410px"></colgroup><tbody><tr style="height: 60px;"><th colspan="1" rowspan="1" colwidth="262"><p style="">方法</p></th><th colspan="1" rowspan="1" colwidth="410"><p style="">说明</p></th></tr><tr style="height: 60px;"><td colspan="1" rowspan="1" colwidth="262"><p style=""><code>getMethod()</code></p></td><td colspan="1" rowspan="1" colwidth="410"><p style="">返回请求方法（如 GET）</p></td></tr><tr style="height: 60px;"><td colspan="1" rowspan="1" colwidth="262"><p style=""><code>getRequestURI()</code></p></td><td colspan="1" rowspan="1" colwidth="410"><p style="">返回请求的 URI</p></td></tr><tr style="height: 60px;"><td colspan="1" rowspan="1" colwidth="262"><p style=""><code>getHeader(String name)</code></p></td><td colspan="1" rowspan="1" colwidth="410"><p style="">获取指定名称的请求头的值</p></td></tr><tr style="height: 60px;"><td colspan="1" rowspan="1" colwidth="262"><p style=""><code>getParameter(String name)</code></p></td><td colspan="1" rowspan="1" colwidth="410"><p style="">获取指定名称的请求参数的值</p></td></tr><tr style="height: 60px;"><td colspan="1" rowspan="1" colwidth="262"><p style=""><code>getCookies()</code></p></td><td colspan="1" rowspan="1" colwidth="410"><p style="">获取请求中的 Cookie 列表</p></td></tr></tbody></table>

#### 1.3 HttpServletRequest 示例代码

```
public class HttpServletRequest {
    private String method;
    private String requestURI;
    private Map<String, String> headers = new HashMap<>();
    private Map<String, String> parameters = new HashMap<>();
    private List<Cookie> cookies = new ArrayList<>();

    // 构造函数，根据请求数据初始化各个属性
    public HttpServletRequest(InputStream inputStream) {
        parseRequest(inputStream);
    }

    private void parseRequest(InputStream inputStream) {
        // 解析请求行、请求头和参数逻辑
    }

    public String getMethod() { return method; }
    public String getRequestURI() { return requestURI; }
    public String getHeader(String name) { return headers.get(name); }
    public String getParameter(String name) { return parameters.get(name); }
    public List<Cookie> getCookies() { return cookies; }
}
```

### 2\. HttpServletResponse 接口设计

`HttpServletResponse` 用于封装服务器端的响应数据，包括响应状态、头部和内容。

#### 2.1 主要属性

+   **状态码**（如 200、404、500）
    
+   **响应头**（如 `Content-Type`、`Set-Cookie` 等）
    
+   **响应体**（通常是 HTML、JSON 或文件内容）
    

#### 2.2 主要方法

<table style="width: 796px"><colgroup><col style="width: 362px"><col style="width: 434px"></colgroup><tbody><tr style="height: 60px;"><th colspan="1" rowspan="1" colwidth="362"><p style="">方法</p></th><th colspan="1" rowspan="1" colwidth="434"><p style="">说明</p></th></tr><tr style="height: 60px;"><td colspan="1" rowspan="1" colwidth="362"><p style=""><code>setStatus(int statusCode)</code></p></td><td colspan="1" rowspan="1" colwidth="434"><p style="">设置响应的状态码</p></td></tr><tr style="height: 60px;"><td colspan="1" rowspan="1" colwidth="362"><p style=""><code>setHeader(String name, String value)</code></p></td><td colspan="1" rowspan="1" colwidth="434"><p style="">设置响应头</p></td></tr><tr style="height: 60px;"><td colspan="1" rowspan="1" colwidth="362"><p style=""><code>getWriter()</code></p></td><td colspan="1" rowspan="1" colwidth="434"><p style="">获取 <code>PrintWriter</code> 对象，用于写入响应体内容</p></td></tr><tr style="height: 60px;"><td colspan="1" rowspan="1" colwidth="362"><p style=""><code>addCookie(Cookie cookie)</code></p></td><td colspan="1" rowspan="1" colwidth="434"><p style="">设置 Cookie，用于保持会话状态</p></td></tr></tbody></table>

#### 2.3 HttpServletResponse 示例代码

```
public class HttpServletResponse {
    private int statusCode = 200;
    private Map<String, String> headers = new HashMap<>();
    private StringBuilder body = new StringBuilder();

    public void setStatus(int statusCode) { this.statusCode = statusCode; }
    public void setHeader(String name, String value) { headers.put(name, value); }
    public PrintWriter getWriter() {
        return new PrintWriter(new StringWriter(body));
    }

    // 生成完整的 HTTP 响应数据
    public void sendResponse(OutputStream outputStream) throws IOException {
        PrintWriter writer = new PrintWriter(outputStream, true);
        writer.println("HTTP/1.1 " + statusCode + " OK");
        headers.forEach((key, value) -> writer.println(key + ": " + value));
        writer.println();
        writer.println(body.toString());
        writer.flush();
    }
}
```

### 3\. 示例：将 HttpServletRequest 和 HttpServletResponse 应用于服务端

在服务器中，当接收到请求时，我们可以创建 `HttpServletRequest` 和 `HttpServletResponse` 实例进行处理，便于抽象底层的流操作。

```
Socket clientSocket = serverSocket.accept();

// 创建 HttpServletRequest 和 HttpServletResponse
HttpServletRequest request = new HttpServletRequest(clientSocket.getInputStream());
HttpServletResponse response = new HttpServletResponse();

// 设置响应头和内容
response.setStatus(200);
response.setHeader("Content-Type", "text/html");
PrintWriter writer = response.getWriter();
writer.println("<h1>Hello, World!</h1>");

// 发送响应
response.sendResponse(clientSocket.getOutputStream());
clientSocket.close();
```

### 4\. 实践任务 📝

1.  **实现** `HttpServletRequest` **的构造方法**：解析请求的输入流，提取请求行、请求头和参数。
    
2.  **实现** `HttpServletResponse` **的** `sendResponse` **方法**：构建 HTTP 响应字符串，并通过输出流发送。
    
3.  **编写测试代码**：模拟客户端请求，验证 `HttpServletRequest` 和 `HttpServletResponse` 是否能够正确封装请求与生成响应。
    

* * *

通过实现 `HttpServletRequest` 和 `HttpServletResponse`，我们将为 MiniTomcat 提供更加标准化和易用的接口，为后续实现 Servlet 容器和业务处理逻辑提供基础支持。