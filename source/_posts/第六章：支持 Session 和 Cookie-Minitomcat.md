---
title: 第六章：支持 Session 和 Cookie-Minitomcat
id: f90b244f-d2b5-4397-a998-4af9baaf12bd
date: 2024-11-19 10:57:30
author: daichangya
cover: https://images.jsdiff.com/tomcat194.jpg
excerpt: "本步骤将实现对 HTTP Session 和 Cookie 的支持，以便维护客户端的会话状态，使每次请求能够识别为同一客户端并跟踪状态。我们将实现一个计数器 Servlet，用于记录每个客户端的访问次数。 6.1 功能目标 实现会话管理：通过 HttpSession 支持为每个客户端分配唯一的 Se"
permalink: /archives/di-liu-zhang-zhi-chi-session-he-cookie-minitomcat/
categories:
 - minitomcat
tags: 
 - tomcat
---

本步骤将实现对 HTTP Session 和 Cookie 的支持，以便维护客户端的会话状态，使每次请求能够识别为同一客户端并跟踪状态。我们将实现一个计数器 Servlet，用于记录每个客户端的访问次数。

### 6.1 功能目标

+   **实现会话管理**：通过 `HttpSession` 支持为每个客户端分配唯一的 Session ID，并保持会话状态。
    
+   **支持 Cookie**：实现对 Cookie 的解析，将请求中的 Cookie 信息提取出来，并在响应中设置新的 Cookie 信息。
    

### 6.2 代码结构

更新后的 MiniTomcat 代码结构，新增了 `CustomHttpSession`、`SessionManager` 、`HttpRequestParser`相关类，以及 `CounterServlet` 示例。

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
│ │ │ │ ├─ WebXmlServletContainer.java // Servlet 容器相关类
│ │ ├─ resources
│ │ │ ├─ webroot
│ │ │ │ ├─ index.html
│ │ │ ├─ web.xml
│ ├─ test
├─ pom.xml
```

### 6.3 代码实现

#### 6.3.1 创建 `HttpSession` 类

`HttpSession` 类负责管理每个客户端的会话数据，并为每个会话分配唯一的 `Session ID`。

```java
package com.daicy.minitomcat.servlet;

import javax.servlet.ServletContext;
import javax.servlet.http.HttpSession;
import java.util.*;

// 自定义类模拟实现HttpSession接口的部分功能
public class CustomHttpSession implements HttpSession {

    private String id;
    private Date creationTime;
    private Date lastAccessedTime;
    private int maxInactiveInterval;
    private Map<String, Object> attributes = new HashMap<>();

    public CustomHttpSession(String sessionId) {
        this.id = sessionId;
        this.creationTime = new Date();
        this.lastAccessedTime = new Date();
        this.maxInactiveInterval = 1800; // 设置默认的会话超时时间为30分钟（单位：秒）
    }

    @Override
    public String getId() {
        return id;
    }

    @Override
    public long getCreationTime() {
        return creationTime.getTime();
    }

    @Override
    public long getLastAccessedTime() {
        return lastAccessedTime.getTime();
    }

    @Override
    public ServletContext getServletContext() {
        return null;
    }

    @Override
    public void setMaxInactiveInterval(int interval) {
        this.maxInactiveInterval = interval;
    }

    @Override
    public int getMaxInactiveInterval() {
        return maxInactiveInterval;
    }

    @Override
    public javax.servlet.http.HttpSessionContext getSessionContext() {
        // 在Servlet 3.1之后，HttpSessionContext接口已被废弃，这里返回null
        return null;
    }

    @Override
    public Object getAttribute(String name) {
        return attributes.get(name);
    }

    @Override
    public Object getValue(String name) {
        return null;
    }

    @Override
    public Enumeration<String> getAttributeNames() {
        return new Enumeration<String>() {
            private final Iterator<String> iterator = attributes.keySet().iterator();

            @Override
            public boolean hasMoreElements() {
                return iterator.hasNext();
            }

            @Override
            public String nextElement() {
                return iterator.next();
            }
        };
    }

    @Override
    public String[] getValueNames() {
        return new String[0];
    }

    @Override
    public void setAttribute(String name, Object value) {
        attributes.put(name, value);
    }

    @Override
    public void putValue(String name, Object value) {

    }

    @Override
    public void removeAttribute(String name) {
        attributes.remove(name);
    }

    @Override
    public void removeValue(String name) {

    }

    @Override
    public void invalidate() {
        attributes.clear();
    }

    @Override
    public boolean isNew() {
        // 简单判断，如果会话创建时间和最后访问时间相差在一定范围内，认为是新会话
        long timeDiff = getLastAccessedTime() - getCreationTime();
        return timeDiff < 1000; // 这里假设1秒内为新会话
    }

    public boolean isExpired() {
        long currentTime = System.currentTimeMillis();
        return (currentTime - lastAccessedTime.getTime()) > (maxInactiveInterval * 1000L);
    }

    // 辅助方法，用于根据请求更新最后访问时间
    public void updateLastAccessedTime() {
        this.lastAccessedTime = new Date();
    }
}
```

#### 6.3.2 创建 `SessionManager` 类

`SessionManager` 类用于管理存储 Session 信息。

```java
package com.daicy.minitomcat;

import com.daicy.minitomcat.servlet.CustomHttpSession;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public class SessionManager {
    private static final Map<String, CustomHttpSession> sessions = new HashMap<>();

    public static CustomHttpSession getSession(String sessionId) {
        CustomHttpSession session = sessions.get(sessionId);
        if (session != null) {
            session.updateLastAccessedTime();
        }
        return session;
    }

    public static CustomHttpSession createSession() {
        String sessionId = UUID.randomUUID().toString();
        CustomHttpSession session = new CustomHttpSession(sessionId);
        sessions.put(sessionId, session);
        return session;
    }

    public static CustomHttpSession getOrCreateSession(String sessionId) {
        CustomHttpSession session = sessions.get(sessionId);
        if (session == null) {
            session = createSession();
        }
        session.updateLastAccessedTime();
        return session;
    }

    public static void invalidateSession(String sessionId) {
        sessions.remove(sessionId);
    }
}
```

#### 6.3.3 修改 `HttpServletRequest` 和 `HttpServletResponse` 支持 Session 和 Cookie

在 `HttpServletRequest` 中添加获取 `Session` 和解析请求中 `Cookie` 的方法。

```java
   public HttpServletRequestImpl(String method, String requestURI, String queryString, Map<String, String> headers) {
        this.method = method;
        this.requestURI = requestURI;
        this.queryString = queryString;
        this.headers = headers;

        // 解析 queryString 并填充参数映射
        if (queryString != null) {
            String[] pairs = queryString.split("&");
            for (String pair : pairs) {
                String[] keyValue = pair.split("=");
                if (keyValue.length == 2) {
                    parameters.put(keyValue[0], new String[]{keyValue[1]});
                }
            }
        }

        // 解析 cookies
        String cookieHeader = headers.get("Cookie");
        if (cookieHeader != null) {
            String[] cookiePairs = cookieHeader.split("; ");
            for (String cookiePair : cookiePairs) {
                String[] keyValue = cookiePair.split("=");
                if (keyValue.length == 2) {
                    Cookie cookie = new Cookie(keyValue[0], keyValue[1]);
                    cookies.add(cookie);
                    // 检查是否有 session ID
                    if ("JSESSIONID".equals(cookie.getName())) {
                        session = SessionManager.getOrCreateSession(cookie.getValue());
                    }
                }
            }
        }
        // 如果没有找到 JSESSIONID，则创建一个新的 session
        if (session == null) {
            session = SessionManager.createSession();
            cookies.add(new Cookie("JSESSIONID", session.getId()));
        }
    }


    @Override
    public HttpSession getSession() {
        return session;
    }

    @Override
    public HttpSession getSession(boolean create) {
        if (session == null && create) {
            session = SessionManager.createSession();
            cookies.add(new Cookie("JSESSIONID", session.getId()));
        }
        return session;
    }

    @Override
    public String getRequestedSessionId() {
        return this.sessionId;
    }

    @Override
    public boolean isRequestedSessionIdValid() {
        if (sessionId == null) return false;
        HttpSession existingSession = SessionManager.getSession(sessionId);
        return existingSession != null && !((CustomHttpSession) existingSession).isExpired();
    }

    @Override
    public boolean isRequestedSessionIdFromCookie() {
        return this.sessionIdFromCookie;
    }

    @Override
    public boolean isRequestedSessionIdFromURL() {
        return !this.sessionIdFromCookie;
    }

    @Override
    public String changeSessionId() {
        if (session == null) {
            getSession(true);
        }
        String newSessionId = UUID.randomUUID().toString();

        // 从存储中移除旧的 sessionId
        if (sessionId != null) {
            SessionManager.invalidateSession(sessionId);
        }

        // 更新新的 sessionId 并保存会话到存储
        sessionId = newSessionId;
        sessionIdChanged = true;
        return sessionId;
    }

    public boolean isSessionIdChanged() {
        return sessionIdChanged;
    }
```

在 `HttpServletResponse` 中添加设置 `Cookie` 的方法。

```java
package server;

import java.util.ArrayList;
import java.util.List;

public class HttpServletResponse {
    private List<Cookie> cookies = new ArrayList<>();

    public void addCookie(Cookie cookie) {
        cookies.add(cookie);
    }

      public void sendResponse() throws IOException {
        // 确保 writer 的内容刷新到 body 中
        writer.flush();
        setCharacterEncoding(characterEncoding);
        if(null == getContentType()){
            setContentType("text/html; charset=UTF-8");
        }
        if(null == getHeader("Content-Length")){
            setContentLength(body.size());
        }
        PrintWriter responseWriter = new PrintWriter(new OutputStreamWriter(outputStream,characterEncoding));

        // 写入状态行
        responseWriter.printf("HTTP/1.1 %d %s\r\n", statusCode, statusMessage);

        // 写入头信息
        for (Map.Entry<String, List<String>> entry : headers.entrySet()) {
            String headerName = entry.getKey();
            for (String headerValue : entry.getValue()) {
                responseWriter.printf("%s: %s\r\n", headerName, headerValue);
            }
        }
        // 写入 Cookie
        for (Cookie cookie : cookies) {
            StringBuilder cookieHeader = new StringBuilder();
            cookieHeader.append(cookie.getName()).append("=").append(cookie.getValue());
            if (cookie.getMaxAge() > 0) {
                cookieHeader.append("; Max-Age=").append(cookie.getMaxAge());
            }
            if (cookie.getPath() != null) {
                cookieHeader.append("; Path=").append(cookie.getPath());
            }
            if (cookie.getDomain() != null) {
                cookieHeader.append("; Domain=").append(cookie.getDomain());
            }
            responseWriter.printf("Set-Cookie: %s\r\n", cookieHeader.toString());
        }

        // 空行标识头部结束
        responseWriter.print("\r\n");
        responseWriter.flush();

        // 写入主体内容
        body.writeTo(outputStream);

        responseWriter.flush();
//        outputStream.flush();
    }
}
```

#### 6.3.4 实现 `CounterServlet` 类

`CounterServlet` 是一个简单的计数器 Servlet，用于测试 Session 功能，每次访问该 Servlet 时，增加计数并返回当前计数值。

```java
package com.daicy.minitomcat;

import com.daicy.minitomcat.servlet.HttpServletResponseImpl;

import javax.servlet.*;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;
import java.io.IOException;

public class CounterServlet implements Servlet {
    @Override
    public void init(ServletConfig config) throws ServletException {

    }

    @Override
    public ServletConfig getServletConfig() {
        return null;
    }

    @Override
    public void service(ServletRequest req, ServletResponse res) throws ServletException, IOException {
        HttpServletRequest request = (HttpServletRequest) req;
        HttpServletResponseImpl response = (HttpServletResponseImpl) res;
        HttpSession session = request.getSession();
        Integer count = (Integer) session.getAttribute("count");
        if (count == null) {
            count = 1;
        } else {
            count++;
        }
        session.setAttribute("count", count);
        response.getWriter().println("<html><body><h1>Visit Count: " + count + "</h1></body></html>");
    }

    @Override
    public String getServletInfo() {
        return "";
    }

    @Override
    public void destroy() {

    }
}
```

#### 6.3.5 实现HttpRequestParser解析类

```java
package com.daicy.minitomcat;

import com.daicy.minitomcat.servlet.HttpServletRequestImpl;

import javax.servlet.http.Cookie;
import java.io.*;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.Map;

public class HttpRequestParser {
    public static HttpServletRequestImpl parseHttpRequest(InputStream inputStream) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));

        // 读取请求行
        String requestLine = reader.readLine();
        if (requestLine == null || requestLine.isEmpty()) {
            System.out.println(reader.readLine());
            throw new IOException("Empty request line");
        }

        // 解析请求行
        String[] parts = requestLine.split(" ");
        if (parts.length < 3) {
            throw new IOException("Invalid request line: " + requestLine);
        }
        String method = parts[0];
        String uri = parts[1];
        int queryIndex = uri.indexOf('?');
        String requestURI = (queryIndex >= 0) ? uri.substring(0, queryIndex) : uri;
        String queryString = (queryIndex >= 0) ? uri.substring(queryIndex + 1) : null;

        // 读取并解析 headers
        Map<String, String> headers = new HashMap<>();
        String line;
        while ((line = reader.readLine()) != null && !line.isEmpty()) {
            int separatorIndex = line.indexOf(": ");
            if (separatorIndex != -1) {
                String headerName = line.substring(0, separatorIndex);
                String headerValue = line.substring(separatorIndex + 2);
                headers.put(headerName, headerValue);
            }
        }

        // 创建并返回 HttpServletRequestImpl
        return new HttpServletRequestImpl(method, requestURI, queryString, headers);
    }

    public static void main(String[] args) throws IOException {
        // 示例 HTTP 请求
        String httpRequest = "GET /hello?name=world HTTP/1.1\r\n" +
                "Host: localhost\r\n" +
                "User-Agent: TestAgent\r\n" +
                "Accept: */*\r\n" +
                "Cookie: sessionId=abc123; theme=light\r\n\r\n";
        InputStream inputStream = new ByteArrayInputStream(httpRequest.getBytes());

        HttpServletRequestImpl request = parseHttpRequest(inputStream);

        // 输出解析后的信息
        System.out.println("Method: " + request.getMethod());
        System.out.println("Request URI: " + request.getRequestURI());
        System.out.println("Query String: " + request.getQueryString());
        System.out.println("Session ID: " + request.getSession().getId());
        System.out.println("Cookies:");
        for (Cookie cookie : request.getCookies()) {
            System.out.println("  " + cookie.getName() + "=" + cookie.getValue());
        }
    }
}
```

### 6.4 测试

1.  启动服务器并访问 `http://localhost:8080/counter`。
    
2.  第一次访问时，页面将显示访问计数 `1`，并在响应头中设置 `JSESSIONID` Cookie。
    
3.  刷新页面后，计数器将继续增加，展示会话管理的效果。
    

### 6.5 学习收获

+   **Session 管理**：学习了如何通过 Session ID 管理用户会话，理解了客户端会话状态的存储。
    
+   **Cookie 使用**：掌握了使用 Cookie 在客户端和服务器间传递信息的方法。
    
+   **Servlet 状态维护**：实现了服务器与客户端间的状态管理基础，为后续实现更复杂的功能打下基础。
    

项目源代码地址：

https://github.com/daichangya/MiniTomcat/tree/chapter6/mini-tomcat