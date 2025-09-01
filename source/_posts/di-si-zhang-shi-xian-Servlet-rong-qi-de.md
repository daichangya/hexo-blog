---
title: 第四章：实现 Servlet 容器的基本功能-MiniTomcat系列
id: 82900bc1-709e-4ea9-9cae-852f9bc38acc
date: 2024-11-11 14:21:25
author: daichangya
cover: https://images.jsdiff.com/MiniTomcat2.jpg
excerpt: 上一章内容：第三章：实现连接器（Connector）组件-MiniTomcat系列 各位技术大神、编程爱好者们！今天我们将一同深入探索 MiniTomcat
  的一个超级重要的进阶环节——实现 Servlet 容器的基本功能。这就像是给我们的 MiniTomcat 注入了强大的“智慧大脑”，使其能够处
permalink: /archives/di-si-zhang-shi-xian-Servlet-rong-qi-de/
categories:
- minitomcat
tags:
- tomcat
---

上一章内容：[第三章：实现连接器（Connector）组件-MiniTomcat系列](https://blog.jsdiff.com/archives/di-san-bu-shi-xian-lian-jie-qi-connector-zu-jian-minitomcat)

各位技术大神、编程爱好者们！今天我们将一同深入探索 MiniTomcat 的一个超级重要的进阶环节——实现 Servlet 容器的基本功能。这就像是给我们的 MiniTomcat 注入了强大的“智慧大脑”，使其能够处理充满活力的动态请求，瞬间让我们的服务器变得更加智能和强大。准备好跟我一起揭开这背后的神秘面纱，看看如何通过巧妙的代码设计让 MiniTomcat 实现这一华丽蜕变吧！💥

## 一、Servlet 容器：MiniTomcat 的“智慧大脑”🧠

### （一）Servlet 容器的重要使命

在 MiniTomcat 这个神奇的小世界里，Servlet 容器就像是一颗超级智能的“智慧大脑”，掌控着整个服务器处理动态请求的核心逻辑。它的主要任务就是精心管理 Servlet 的生命周期，从 Servlet 的诞生（初始化）、茁壮成长（处理请求）到最后的谢幕（销毁），每一个环节都安排得井井有条。并且，当 HTTP 请求如同潮水般涌来时，它能够凭借着敏锐的“洞察力”，迅速找到最合适的 Servlet，并准确无误地调用其强大的 `service()` 方法来处理请求，就像一位经验丰富的指挥家，精准指挥着每一个音符（请求），奏响美妙的乐章（响应）。🎵

### （二）功能目标解读

1.  **请求与响应的精美包装**：`HttpServletRequest` 和 `HttpServletResponse` 这两个类就像是一对神奇的“魔法盒子”，专门用来封装 HTTP 请求和响应数据。它们把那些杂乱无章、分散各处的请求信息（如请求路径、方法、头部等）和需要返回给客户端的响应数据，整整齐齐地收纳进这两个“盒子”里，使得数据的管理和传递变得更加高效、有序，就像把散落的珍珠串成美丽的项链一样。💎
    
2.  **请求路径的精准导航**：实现请求路径映射功能就像是为服务器安装了一套超级智能的“导航系统”。根据客户端发送的请求路径，这个“导航系统”能够迅速在众多的 Servlet 中找到与之匹配的那个，并引领请求顺利到达目的地（对应的 Servlet），然后触发其 `service()` 方法开始处理请求，确保每一个请求都能被准确送达，不会迷路。🚗
    

## 二、项目结构升级：构建更强大的“代码大厦”🏗

随着 Servlet 容器功能的加入，我们的 MiniTomcat 项目结构也迎来了一次华丽升级，变得更加丰富和完善，就像一座大厦增添了新的楼层和功能区域。以下是更新后的代码结构，每一个类都在自己的位置上发挥着不可或缺的作用：

```
MiniTomcat 
├─ src 
│  ├─ main 
│  │  ├─ java 
│  │  │  ├─ com.daicy.minitomcat 
│  │  │  │  ├─ CustomServletOutputStream.java  // ServletOutputStream封装，精心处理输出流相关操作
│  │  │  │  ├─ HttpConnector.java          // 连接器类，依旧坚守连接管理的重要岗位
│  │  │  │  ├─ HttpProcessor.java          // 请求处理器，经过升级，能更好地处理动态请求
│  │  │  │  ├─ HttpServer.java             // 主服务器类，作为整个服务器的核心启动点
│  │  │  │  ├─ HttpServletRequest.java     // 请求封装类，承载请求的各种详细信息
│  │  │  │  ├─ HttpServletResponse.java    // 响应封装类，负责构建和发送响应数据
│  │  │  │  ├─ ServletProcessor.java       // Servlet处理器，新加入的重要角色，负责调度Servlet
│  │  │  │  ├─ StaticResourceProcessor.java // 静态资源处理器，专注于处理静态文件请求
│  │  │  │  ├─ HelloServlet.java        // 示例Servlet，展示如何编写和运行Servlet
│  │  ├─ resources 
│  │  │  ├─ webroot 
│  │  │  │  ├─ index.html 
├─ pom.xml
```

## 三、代码实现剖析：揭开“智慧大脑”的运作奥秘🧐

### （一）请求与响应的精致封装

1.  `HttpServletRequestImpl` **类**：
    
    ```java
    package com.daicy.minitomcat;
    public class HttpServletRequestImpl implements HttpServletRequest {
    private String method;
    private String requestUri;
    public HttpServletRequestImpl(String method, String requestURI) {
        this.method = method;
        this.requestUri = requestURI;
    }
    // 这里省略了其他方法的实现，但可以想象它内部对请求信息的整理和存储逻辑
    }
    ```
    
    这个类就像是一个细心的“请求信息收集员”，它认真收集并整理请求的路径、方法和头部等重要信息，将它们有条不紊地存储起来，为后续的请求处理提供准确无误的“情报”支持。就像一个探险家在出发前仔细整理装备和地图一样，确保每一个细节都不会被遗漏。📋
    
2.  `HttpServletResponseImpl` **类**：
    
    ```java
    package com.daicy.minitomcat;
    public class HttpServletResponseImpl implements HttpServletResponse {
    private OutputStream outputStream;
    public HttpServletResponseImpl(OutputStream outputStream) {
        this.outputStream = outputStream;
    }
    @Override
    public ServletOutputStream getOutputStream() {
        return new CustomServletOutputStream(outputStream);
    }
    @Override
    public PrintWriter getWriter() throws IOException {
        PrintWriter writer = new PrintWriter(outputStream, true);
        return writer;
    }
    // 同样省略了其他部分，但能看出它对输出流和响应构建的关键作用
    }
    ```
    
    作为响应数据的“包装大师”，它负责将服务器准备返回给客户端的数据进行精心包装。通过巧妙地管理输出流，它不仅能够准确地发送响应内容，还能设置各种响应头信息，如 `Content-Type` 等，确保客户端能够正确地解析和处理收到的响应。这就像一个专业的快递员，不仅要把包裹（响应数据）准确无误地送到目的地（客户端），还要确保包裹的包装（响应头）完好无损、标识清晰。📦
    

### （二）Servlet 处理器：请求的“智能调度员”

```java
package com.daicy.minitomcat;
import javax.servlet.Servlet;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Map;
import static com.daicy.minitomcat.HttpProcessor.send404Response;
public class ServletProcessor {
    private Map<String, Servlet> servletMappings = new HashMap<>();
    public void process(HttpServletRequest request, HttpServletResponse response) {
        String servletName = getServletName(request.getRequestURI());
        try {
            PrintWriter writer = response.getWriter();
            if ("HelloServlet".equals(servletName)) {
                writeResponseHeaders(writer, 200, "OK");
                Servlet servlet;
                if (servletMappings.containsKey(servletName)){
                    servlet = servletMappings.get(servletName);
                }else {
                    servlet = new HelloServlet();
                    servlet.init(null);
                    servletMappings.put(servletName, servlet);
                }
                servlet.service(request, response);
            } else {
                send404Response(writer);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ServletException e) {
            throw new RuntimeException(e);
        }
    }
    private String getServletName(String path) {
        if ("/hello".equals(path)) {
            return "HelloServlet";
        }
        return null;
    }
    private void writeResponseHeaders(PrintWriter writer, int statusCode, String statusMessage) {
        writer.println("HTTP/1.1 " + statusCode + " " + statusMessage);
        writer.println("Content-Type: text/html; charset=UTF-8");
        writer.println();
    }
}
```

`ServletProcessor` 类堪称一位聪明绝顶的“智能调度员”，它的核心任务就是根据请求路径快速找到对应的 Servlet 类，并巧妙地调用其 `service()` 方法来处理请求。它内部维护着一个 `servletMappings` 映射表，就像一本神奇的“路径 - Servlet 对应手册”，通过查询这个手册，它能够迅速定位到目标 Servlet。如果是首次遇到某个请求路径，它还会机智地创建对应的 Servlet 实例，并进行初始化操作，然后将其加入到映射表中，为后续的请求做好充分准备。这就像一个火车站的调度员，根据列车的目的地（请求路径），准确地将其引导到对应的站台（Servlet），确保每一趟列车（请求）都能顺利出发和到达。🚉

### （三）示例 Servlet：功能展示的“小能手”

```java
package com.daicy.minitomcat;
import javax.servlet.*;
import java.io.IOException;
public class HelloServlet implements Servlet {
    @Override
    public void init(ServletConfig config) throws ServletException {
        System.out.println("HelloServlet initialized.");
    }
    @Override
    public ServletConfig getServletConfig() {
        return null;
    }
    @Override
    public void service(ServletRequest req, ServletResponse res) {
        try {
            res.getWriter().println("<html><body><h1>Hello from HelloServlet!</h1></body></html>");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    @Override
    public String getServletInfo() {
        return "";
    }
    @Override
    public void destroy() {
        System.out.println("HelloServlet destroyed.");
    }
}
```

`HelloServlet` 作为一个示例 Servlet，就像是一个热情好客的“小导游”，它向我们展示了 Servlet 的基本结构和功能。在 `init()` 方法中，它会友好地打招呼，告诉我们它已经准备好迎接请求啦。而在 `service()` 方法里，它精心准备了一段简单而温馨的欢迎信息（“Hello from HelloServlet!”），并将其发送回客户端，让我们能够直观地看到 Servlet 的运行效果。当服务器关闭时，它在 `destroy()` 方法中也会礼貌地告别，结束自己的使命。这个示例 Servlet 就像是一个小小的样板间，让我们能够清楚地了解 Servlet 的工作流程和生命周期，为我们开发更复杂的 Servlet 提供了宝贵的参考。🏠

### （四）`HttpProcessor` 的升级：动态请求的“智能分流器”

```java
package com.daicy.minitomcat;
import java.io.*;
import java.net.Socket;
public class HttpProcessor {
    private Socket socket;
    private final static ServletProcessor processor = new ServletProcessor();
    private final static StaticResourceProcessor staticProcessor = new StaticResourceProcessor();
    public HttpProcessor(Socket socket) {
        this.socket = socket;
    }
    public void process() {
        try (InputStream inputStream = socket.getInputStream();
             OutputStream outputStream = socket.getOutputStream()) {
            // 解析请求
            HttpServletRequestImpl request = parseRequest(inputStream);
            // 构建响应
            HttpServletResponseImpl response = new HttpServletResponseImpl(outputStream);
            if (null == request){
                return;
            }
            String uri = request.getRequestURI();
            if (uri.endsWith(".html") || uri.endsWith(".css") || uri.endsWith(".js")) {
                staticProcessor.process(request, response);
            } else {
                processor.process(request, response);
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
    private HttpServletRequestImpl parseRequest(InputStream inputStream) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
        String requestLine = reader.readLine();
        if (requestLine == null || requestLine.isEmpty()) {
            return null;
        }
        System.out.println("Request Line: " + requestLine);
        String[] parts = requestLine.split(" ");
        String method = parts[0];
        String path = parts[1];
        return new HttpServletRequestImpl(method, path);
    }
    static void send404Response(PrintWriter writer) {
        sendResponse(writer, 404, "Not Found", "The requested resource was not found.");
    }
    // 发送普通文本响应
    private static void sendResponse(PrintWriter writer, int statusCode, String statusText, String message) {
        String html = "<html><body><h1>" + statusCode + " " + statusText + "</h1><p>" + message + "</p></body></html>";
        writer.println("HTTP/1.1 " + statusCode + " " + statusText);
        writer.println("Content-Type: text/html; charset=UTF-8");
        writer.println("Content-Length: " + html.length());
        writer.println();
        writer.println(html);
    }
}
```

`HttpProcessor` 经过升级后，摇身一变成为了一个智能的“请求分流器”。当它接收到请求时，会先仔细分析请求路径，判断是静态资源请求还是动态请求。如果是静态资源请求，它会毫不犹豫地将任务交给 `StaticResourceProcessor` 去处理；而如果是动态请求，它就会明智地把请求转交给 `ServletProcessor` 进行处理。这种智能分流的设计，使得服务器能够更加高效地处理不同类型的请求，就像一个交通警察在路口根据车辆类型（请求类型）指挥交通，确保道路畅通无阻。🚦

## 四、测试与验证：见证奇迹的时刻✨

现在，让我们启动服务器，在浏览器中输入 `http://localhost:8080/hello`，然后屏住呼吸，见证奇迹的发生吧！哇哦，我们看到了由 `HelloServlet` 返回的热情洋溢的响应内容：“Hello from HelloServlet!”。这一刻，我们的努力和付出得到了最好的回报，我们成功地让 MiniTomcat 具备了处理动态请求的能力，这是一个了不起的成就！🎉

## 五、学习收获与展望：技术成长的新起点🎓

通过实现 Servlet 容器的基础功能，我们就像勇敢的探险家发现了新的宝藏一样，收获了满满的知识和经验：

### （一）请求与响应处理的精湛技巧

我们熟练掌握了如何使用 `HttpServletRequest` 和 `HttpServletResponse` 这两个强大的工具，将请求和响应数据进行完美封装和高效传递。这就像学会了一门精湛的手艺，在未来的开发中，我们能够更加熟练地处理各种复杂的请求和构建多样化的响应，为用户提供更加优质的服务。💪

### （二）为后续功能拓展奠定坚实基础

这次的实现为我们后续进一步拓展 Servlet 容器的功能，如实现更灵活的 Servlet 映射、支持配置文件管理等，打下了坚如磐石的基础。这就像是盖房子，我们已经搭建好了坚实的框架，接下来就可以根据需求添加更多的功能模块，让我们的 MiniTomcat 变得更加完善和强大。🏢

未来，我们可以继续深入探索 Servlet 容器的更多高级功能，如优化 Servlet 的加载机制、增强安全性、提升性能等。相信在不断的学习和实践中，我们能够将 MiniTomcat 打造成一个功能强大、性能卓越的服务器，为更多的应用场景提供稳定可靠的支持。让我们一起怀揣着对技术的热爱和追求，继续前行，在编程的道路上创造更多的精彩吧！🚀

项目源代码地址：

https://github.com/daichangya/MiniTomcat/tree/chapter4/mini-tomcat