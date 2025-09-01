---
title: 第五章：支持 Servlet 配置和 URL 映射-MiniTomcat
id: cd4ce4a1-c4d8-43f5-b6d7-74a3696cfaa6
date: 2024-11-19 10:17:44
author: daichangya
cover: https://images.jsdiff.com/tomcat193.jpg
excerpt: 本步骤将实现基于 web.xml 配置文件的 Servlet 路由映射和初始化参数支持，使得 MiniTomcat 能根据配置自动调用相应的 Servlet
  处理请求。 5.1 功能目标 配置文件管理路由和初始化参数：通过 web.xml 文件管理 Servlet 映射和初始化参数。 URL 路径映
permalink: /archives/di-wu-zhang-zhi-chi-Servlet-pei-zhi-he/
categories:
- minitomcat
tags:
- tomcat
---

本步骤将实现基于 `web.xml` 配置文件的 Servlet 路由映射和初始化参数支持，使得 MiniTomcat 能根据配置自动调用相应的 Servlet 处理请求。

### 5.1 功能目标

+   **配置文件管理路由和初始化参数**：通过 `web.xml` 文件管理 Servlet 映射和初始化参数。
    
+   **URL 路径映射**：根据配置文件中的路径映射，将请求 URL 映射到对应的 Servlet。
    
+   **支持** `ServletConfigImpl` **获取初始化参数**：提供 `ServletConfigImpl` 类，支持从配置中读取初始化参数。
    

### 5.2 代码结构

以下是更新后的 MiniTomcat 代码结构，新增了 `ServletConfigImpl`、`ServletContextImpl`、`ServletLoader`和`WebXmlServletContainer`等类和 `web.xml` 配置文件。

```
MiniTomcat
├─ src
│ ├─ main
│ │ ├─ java
│ │ │ ├─ com.daicy.minitomcat
│ │ │ │ ├─ servlet
│ │ │ │ │ ├─ CustomServletOutputStream.java // 自定义的 Servlet 输出流类
│ │ │ │ │ ├─ HttpServletRequestImpl.java // HTTP 请求的实现类
│ │ │ │ │ ├─ HttpServletResponseImpl.java // HTTP 响应的实现类
│ │ │ │ │ ├─ ServletConfigImpl.java // Servlet 配置的实现类
│ │ │ │ │ ├─ ServletContextImpl.java // Servlet 上下文的实现类
│ │ │ │ ├─ HelloServlet.java // Servlet 示例类
│ │ │ │ ├─ HttpConnector.java // 连接器类
│ │ │ │ ├─ HttpProcessor.java // 请求处理器
│ │ │ │ ├─ HttpServer.java // 主服务器类
│ │ │ │ ├─ ServletLoader.java // Servlet 加载器
│ │ │ │ ├─ ServletProcessor.java // Servlet 处理器
│ │ │ │ ├─ StaticResourceProcessor.java// 静态资源处理器
│ │ │ │ ├─ WebXmlServletContainer.java // Servlet 容器相关类
│ │ ├─ resources
│ │ │ ├─ webroot
│ │ │ │ ├─ index.html
│ │ │ ├─ web.xml
│ ├─ test
├─ pom.xml
```

### 5.3 代码实现

#### 5.3.1 创建 `ServletConfigImpl` 类

`ServletConfigImpl` 用于存储 `web.xml` 中的初始化参数，提供 `getInitParameter()` 方法获取这些参数。

```java
package com.daicy.minitomcat.servlet;


public class ServletConfigImpl implements ServletConfig {

    private String servletName;
    private ServletContext servletContext;
    private Map<String, String> initParameters;

    public ServletConfigImpl(String servletName, ServletContext servletContext, Map<String, String> initParameters) {
        this.servletName = servletName;
        this.servletContext = servletContext;
        this.initParameters = initParameters != null ? initParameters : new HashMap<>();
    }

    @Override
    public String getInitParameter(String name) {
        return initParameters.get(name);
    }
    ......
}
```

#### 5.3.2 添加 `web.xml` 文件

在 `resources` 目录下创建 `web.xml` 文件，用于配置 Servlet 映射和初始化参数。配置 `/hello` 路径映射到 `HelloServlet` 类。

```xml
<web-app>
    <servlet>
        <servlet-name>HelloServlet</servlet-name>
        <servlet-class>com.daicy.minitomcat.HelloServlet</servlet-class>
        <init-param>
            <param-name>greeting</param-name>
            <param-value>Hello from web.xml!</param-value>
        </init-param>
    </servlet>

    <servlet-mapping>
        <servlet-name>HelloServlet</servlet-name>
        <url-pattern>/hello</url-pattern>
    </servlet-mapping>
</web-app>
```

#### 5.3.3 解析 `web.xml` 配置文件

创建一个 `WebXmlServletContainer` 类，用于解析 `web.xml` 文件，并将 Servlet 路径映射到对应的类。

```java
package com.daicy.minitomcat;

import javax.servlet.Servlet;
import javax.servlet.ServletContext;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import com.daicy.minitomcat.servlet.ServletConfigImpl;
import org.w3c.dom.*;

import java.util.HashMap;
import java.util.Map;
import javax.servlet.ServletConfig;


public class WebXmlServletContainer {

    private  Map<String, ServletConfig> servletConfigMap = new HashMap<>();

    private Map<String, Servlet> servletHashMap = new HashMap<>();

    private ServletContext servletContext;

    public void parse(String xmlPath, ServletContext servletContext) {
        try {
            this.servletContext = servletContext;

            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document doc = builder.parse(getClass().getResourceAsStream(xmlPath));

            NodeList servletNodes = doc.getElementsByTagName("servlet");
            for (int i = 0; i < servletNodes.getLength(); i++) {
                Element servletElement = (Element) servletNodes.item(i);
                String servletName = servletElement.getElementsByTagName("servlet-name").item(0).getTextContent();
                String servletClass = servletElement.getElementsByTagName("servlet-class").item(0).getTextContent();

                Map<String, String> initParamsMap = new HashMap<>();
                NodeList initParams = servletElement.getElementsByTagName("init-param");
                for (int j = 0; j < initParams.getLength(); j++) {
                    Element param = (Element) initParams.item(j);
                    String paramName = param.getElementsByTagName("param-name").item(0).getTextContent();
                    String paramValue = param.getElementsByTagName("param-value").item(0).getTextContent();
                    initParamsMap.put(paramName, paramValue);
                }
                ServletConfig servletConfig = new ServletConfigImpl(servletName, servletContext, initParamsMap);
                servletConfigMap.put(servletClass, servletConfig);
                servletContext.setAttribute(servletName, servletClass);
            }

            NodeList mappingNodes = doc.getElementsByTagName("servlet-mapping");
            for (int i = 0; i < mappingNodes.getLength(); i++) {
                Element mappingElement = (Element) mappingNodes.item(i);
                String servletName = mappingElement.getElementsByTagName("servlet-name").item(0).getTextContent();
                String urlPattern = mappingElement.getElementsByTagName("url-pattern").item(0).getTextContent();
                servletContext.setAttribute(urlPattern, servletName);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public ServletConfig getServletConfig(String urlPattern) {
        String servletClass = getServletClass(getServletName(urlPattern));
        return servletConfigMap.get(servletClass);
    }

    public String getServletName(String urlPattern) {
        return (String) servletContext.getAttribute(urlPattern);
    }

    public String getServletClass(String servletName) {
        return (String) servletContext.getAttribute(servletName);
    }

    public Servlet getServlet(String servletName) {
        return servletHashMap.get(servletName);
    }

    public void setServlet(String servletName,Servlet servlet) {
         servletHashMap.put(servletName,servlet);
    }

    public Map<String, Servlet> getServletHashMap() {
        return servletHashMap;
    }
}
```

#### 5.3.4 修改 `ServletProcessor` 类

在 `ServletProcessor` 中使用 `WebXmlServletContainer` 获取 Servlet 映射信息和初始化参数，并调用对应的 Servlet 处理请求。

```java
package com.daicy.minitomcat;


import javax.servlet.Servlet;
import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;

import static com.daicy.minitomcat.HttpProcessor.send404Response;

public class ServletProcessor {


    public void process(HttpServletRequest request, HttpServletResponse response) {
        String uri = request.getRequestURI();
        try {
            PrintWriter writer = response.getWriter();
            WebXmlServletContainer parser = HttpServer.parser;
            String servletName = parser.getServletName(uri);
            if (null != servletName) {
                writeResponseHeaders(writer, 200, "OK");
                Servlet servlet = parser.getServlet(servletName);
                if (null == servlet){
                    ServletConfig servletConfig = parser.getServletConfig(uri);
                    servlet = ServletLoader.loadServlet(servletConfig);
                    if (null == servlet){
                        return;
                    }
                    // 将初始化后的 Servlet 存储在 WebXmlServletContainer 中，后续可通过 WebXmlServletContainer 访问
                    parser.setServlet(servletName, servlet);
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

    private void writeResponseHeaders(PrintWriter writer, int statusCode, String statusMessage) {
        writer.println("HTTP/1.1 " + statusCode + " " + statusMessage);
        writer.println("Content-Type: text/html; charset=UTF-8");
        writer.println();
    }

}
```

#### 5.3.5 修改 `HelloServlet` 支持初始化参数

更新 `HelloServlet`，使用 `ServletConfig` 获取 `web.xml` 中的初始化参数。

```java
package server.servlet;

import server.HttpServletRequest;
import server.HttpServletResponse;
import server.ServletConfig;

import java.io.IOException;

public class HelloServlet {
    private ServletConfig config;

    public void init(ServletConfig config) {
        this.config = config;
    }

    public void service(HttpServletRequest request, HttpServletResponse response) {
        try {
            String greeting = config.getInitParameter("greeting");
            response.getWriter().println("<html><body><h1>" + greeting + "</h1></body></html>");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void destroy() {
        // Clean-up if needed
    }
}
```

### 5.4 测试

启动服务器并访问 `http://localhost:8080/hello`，将返回 `web.xml` 中设置的 `greeting` 参数：“Hello from web.xml!”

### 5.5 学习收获

通过本步骤的实现，我们学到了：

1.  **XML 配置文件解析**：掌握了解析 XML 文件的方法，并将 XML 数据映射为对象。
    
2.  **Servlet URL 路径映射**：基于配置文件实现了灵活的 URL 路径到 Servlet 的映射机制。
    
3.  **Servlet 初始化参数的使用**：学习了如何使用 `ServletConfig` 获取 `web.xml` 中的初始化参数。
    

这为后续的会话管理、过滤器支持等功能的实现打下了基础。

项目源代码地址：

https://github.com/daichangya/MiniTomcat/tree/chapter5/mini-tomcat