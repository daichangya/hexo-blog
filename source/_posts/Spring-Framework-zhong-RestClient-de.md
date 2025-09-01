---
title: Spring Framework 中 RestClient 的详细介绍及示例
id: 473925de-0f38-486a-8f6d-92599ce6fca9
date: 2025-03-15 15:51:02
author: daichangya
excerpt: 以下是关于 Spring Framework 中 RestClient 的详细介绍及示例，适用于 Spring 6.1+ 版本： 什么是 RestClient？
  RestClient 是 Spring Framework 6.1 引入的一个同步 HTTP 客户端，旨在替代旧的 RestTemplat
permalink: /archives/Spring-Framework-zhong-RestClient-de/
categories:
- spring
tags:
- http
---

以下是关于 Spring Framework 中 `RestClient` 的详细介绍及示例，适用于 **Spring 6.1+** 版本：

---

### 什么是 `RestClient`？
`RestClient` 是 Spring Framework 6.1 引入的一个**同步 HTTP 客户端**，旨在替代旧的 `RestTemplate`，提供更简洁、现代的 API 设计。它专注于同步请求场景，语法链式调用（Fluent API），并支持与 Spring 生态（如错误处理、拦截器等）无缝集成。

---

### 核心特性
1. **同步请求**：适合传统阻塞式调用。
2. **链式调用**：方法链式设计，代码更简洁。
3. **灵活配置**：支持自定义请求头、拦截器、错误处理等。
4. **与 Spring 集成**：可直接注入 Bean，或与 `RestTemplate` 的组件（如 `HttpMessageConverter`）复用。

---

### 依赖配置
确保使用 **Spring Boot 3.2+** 或手动引入 `spring-web 6.1+`：
```xml
<!-- Maven 依赖 -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <version>3.2.0+</version>
</dependency>
```

---

### 快速使用示例

#### 1. 创建 `RestClient` 实例
```java
import org.springframework.web.client.RestClient;

// 基础配置
RestClient client = RestClient.builder()
    .baseUrl("https://api.example.com")  // 基础 URL
    .defaultHeader("Accept", "application/json")  // 默认请求头
    .build();
```

#### 2. 发起 GET 请求
```java
// 获取 JSON 响应并反序列化为对象
User user = client.get()
    .uri("/users/{id}", 1)  // 路径参数
    .retrieve()             // 发起请求
    .body(User.class);      // 反序列化为 User 对象

System.out.println(user.getName());
```

#### 3. 发起 POST 请求
```java
// 提交 JSON 数据
User newUser = new User("Alice", 30);
User createdUser = client.post()
    .uri("/users")
    .contentType(MediaType.APPLICATION_JSON)
    .body(newUser)          // 请求体
    .retrieve()
    .body(User.class);
```

#### 4. 处理错误
```java
// 自定义错误处理
client.get()
    .uri("/users/{id}", 999)
    .retrieve()
    .onStatus(status -> status.value() == 404, (req, res) -> {
        throw new UserNotFoundException("User not found");
    })
    .body(User.class);
```

---

### 高级功能

#### 1. 添加拦截器
```java
RestClient client = RestClient.builder()
    .baseUrl("https://api.example.com")
    .requestInterceptor((request, body, execution) -> {
        // 添加认证头
        request.getHeaders().set("Authorization", "Bearer token");
        return execution.execute(request, body);
    })
    .build();
```

#### 2. 自定义消息转换器
```java
RestClient client = RestClient.builder()
    .messageConverters(converters -> {
        converters.add(new MappingJackson2HttpMessageConverter());
        converters.add(new StringHttpMessageConverter());
    })
    .build();
```

#### 3. 文件下载
```java
client.get()
    .uri("/files/{name}", "report.pdf")
    .accept(MediaType.APPLICATION_PDF)
    .retrieve()
    .body(InputStreamResource.class);  // 获取文件流
```

---

### 与旧组件的对比

| 特性                | `RestClient` (6.1+)     | `RestTemplate` (旧)     | `WebClient` (响应式)    |
|---------------------|-------------------------|-------------------------|-------------------------|
| **请求类型**         | 同步                   | 同步                   | 异步/非阻塞             |
| **API 设计**         | 链式调用               | 传统方法调用           | 链式调用 + Reactor      |
| **适用场景**         | 简单同步 HTTP 调用     | 旧项目兼容             | 响应式或复杂异步场景    |
| **依赖**             | `spring-web`           | `spring-web`           | `spring-webflux`        |

---

### 总结
- **推荐场景**：在 Spring 6.1+ 项目中，优先使用 `RestClient` 替代 `RestTemplate`。
- **优势**：语法简洁、易扩展、与 Spring 生态深度集成。
- **注意**：如果需要异步或响应式编程，继续使用 `WebClient`。