---
title: 基于Spring的安全管理框架Spring Security
id: 1575
date: 2024-10-31 22:02:02
author: daichangya
excerpt: "一、什么是SpringSecurity?   SpringSecurity是基于Spring的安全框架.它提供全面的安全性解决方案,同时在Web请求级别和调用级别确认和授权.在SpringFramework基础上,SpringSecurity充分利用了依赖注入(DI)和面向切面编程(AOP)功能,为"
permalink: /archives/%E5%9F%BA%E4%BA%8Espring%E7%9A%84%E5%AE%89%E5%85%A8%E7%AE%A1%E7%90%86%E6%A1%86%E6%9E%B6springsecurity/
tags: 
 - oauth
---

**一、****什么是****Spring** **Security?**

   Spring Security是基于Spring的安全框架.它提供全面的安全性解决方案,同时在Web请求级别和调用级别确认和授权.在Spring Framework基础上,Spring Security充分利用了依赖注入(DI)和面向切面编程(AOP)功能,为应用系统提供声明式的安全访问控制功能,建晒了为企业安全控制编写大量重复代码的工作,是一个轻量级的安全框架,并且很好集成Spring MVC

**二、Spring** **Security的核心功能有哪些?**

1、认证(Authentication)：指的是验证某个用户是否为系统中的合法主体，也就是说用户能否访问该系统。

2、授权(Authorization)：指的是验证某个用户是否有权限执行某个操作

## **三、Spring** **Security基于哪些技术实现?**

　**Filter,Servlet,AOP实现**

众所周知想要对Web资源进行保护，最好的办法莫过于Filter，要想对方法调用进行保护，最好的办法莫过于AOP。所以SpringSecurity在我们进行用户认证以及授予权限的时候，通过各种各样的拦截器来控制权限的访问，从而实现安全。

Spring Security功能的实现主要是由一系列过滤器链相互配合完成。

![1686234202010181227256081610316777.png](https://images.jsdiff.com/1686234-20201018122725608-1610316777_1619964150908.png)

   1、springSecurityFilterChain中各个过滤器怎么创建的只需了解即可。不要太过关注。

   2、重点记忆UsernamePasswordAuthenticationFilter，ExceptionTranslationFilter， FilterSecurityInterceptor这三个过滤器的作用及源码分析。

   3、重点记忆认证中Authentication，AuthenticationManager，ProviderManager， AuthenticationProvider，UserDetailsService，UserDetails这些类的作用及源码分析。

  4、重点记忆授权中FilterInvoction，SecurityMetadataSource，AccessDecisionManager的作用。

## **四、框架的核心组件**

      SecurityContextHolder：提供对SecurityContext的访问

      SecurityContext：持有Authentication对象和其他可能需要的信息

      AuthenticationManager：其中可以包含多个AuthenticationProvider

      ProviderManager对象：为AuthenticationManager接口的实现类

      AuthenticationProvider：主要用来进行认证操作的类 调用其中的authenticate()方法去进行认证操作

      Authentication：Spring Security方式的认证主体

      GrantedAuthority：对认证主题的应用层面的授权，含当前用户的权限信息，通常使用角色表示

      UserDetails：构建Authentication对象必须的信息，可以自定义，可能需要访问DB得到

     UserDetailsService：通过username构建UserDetails对象，通过loadUserByUsername根据userName获取UserDetail对象

## **五、SpringSecurity的工作流程**

![1686234202010181228439881242133496.png](https://images.jsdiff.com/1686234-20201018122843988-1242133496_1619964173573.png)

**六、认证流程**

![1686234202010181229490111317919020.png](https://images.jsdiff.com/1686234-20201018122949011-1317919020_1619964184419.png)

**七、授权流程**

![16862342020101812302175992577888.png](https://images.jsdiff.com/1686234-20201018123021759-92577888_1619964195031.png)

**八、springsecurity入门示例**

**     1、构建maven项目，引入springsecurity相关依赖。   **

![168623420201018123101129475975440.png](https://images.jsdiff.com/1686234-20201018123101129-475975440_1619964234348.png)

**pom.xml配置文件主要部分：**

```
<properties>  
  <spring.version>4.2.0.RELEASE</spring.version>  
</properties>  
<dependencies>  
  <dependency>  
    <groupId>junit</groupId>  
    <artifactId>junit</artifactId>  
    <version>4.11</version>  
    <scope>test</scope>  
  </dependency>  
  <dependency>  
    <groupId>org.springframework</groupId>  
    <artifactId>spring-beans</artifactId>  
    <version>${spring.version}</version>  
  </dependency>  
  <dependency>  
    <groupId>org.springframework</groupId>  
    <artifactId>spring-context</artifactId>  
    <version>${spring.version}</version>  
  </dependency>  
  <dependency>  
    <groupId>org.springframework</groupId>  
    <artifactId>spring-webmvc</artifactId>  
    <version>${spring.version}</version>  
  </dependency>  
  <dependency>  
    <groupId>org.springframework.security</groupId>  
    <artifactId>spring-security-web</artifactId>  
    <version>${spring.version}</version>  
  </dependency>  
  <dependency>  
    <groupId>org.springframework.security</groupId>  
    <artifactId>spring-security-config</artifactId>  
    <version>${spring.version}</version>  
  </dependency>  
  <dependency>  
    <groupId>jstl</groupId>  
    <artifactId>jstl</artifactId>  
    <version>1.2</version>  
  </dependency>  
</dependencies>
```

**2、配置web.xml。**

```
<context-param>
  <param-name>contextConfigLocation</param-name>
  <param-value>classpath:spring-security.xml</param-value>
</context-param>

<servlet>
  <servlet-name>springmvc</servlet-name>
  <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
  <init-param>
    <param-name>contextConfigLocation</param-name>
    <param-value>classpath:spring-mvc.xml</param-value>
  </init-param>
  <load-on-startup>1</load-on-startup>
</servlet>
<servlet-mapping>
  <servlet-name>springmvc</servlet-name>
  <url-pattern>/</url-pattern>
</servlet-mapping>
<listener>
  <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
</listener>
<filter>
  <filter-name>springSecurityFilterChain</filter-name>
  <filter-class>org.springframework.web.filter.DelegatingFilterProxy</filter-class>
</filter>
<filter-mapping>
  <filter-name>springSecurityFilterChain</filter-name>
  <url-pattern>/*</url-pattern>
</filter-mapping>
<welcome-file-list>
  <welcome-file>index.jsp</welcome-file>
</welcome-file-list>
```

**3、书写AdminController.java类。**

```
@Controller
public class AdminController {
    @RequestMapping(value = {"/","/welcome**"},method = RequestMethod.GET)
    public ModelAndView welcome(){
        ModelAndView welcome = new ModelAndView();
        welcome.addObject("title","Welcome");
        welcome.addObject("message","This is a Security Page");
        welcome.setViewName("hello");
        return welcome;
    }
    @RequestMapping(value = {"/","/admin**"},method = RequestMethod.GET)
    public ModelAndView admin(){
        ModelAndView welcome = new ModelAndView();
        welcome.addObject("title","admin");
        welcome.addObject("message","This is Admin page");
        welcome.setViewName("admin");
        return welcome;
    }


```

**4、配置spring-mvc.xml**

```
<context:component-scan base-package="web.*"/>
<bean class="org.springframework.web.servlet.view.InternalResourceViewResolver">
    <property name="prefix" value="/WEB-INF/views/"/>
    <property name="suffix" value=".jsp"/>
</bean>
```
**5、配置spring-security.xml**

```
<security:http auto-config="true">
   <security:intercept-url pattern="/admin**" access="hasAnyRole('ROLE_USER')"/>
</security:http>
<security:authentication-manager>
    <security:authentication-provider>
        <security:user-service>
            <security:user name="admin" authorities="ROLE_USER" password="123456"/>
        </security:user-service>
    </security:authentication-provider>
</security:authentication-manager>
```

**注意：****<intercept-url pattern="/admin**" access="hasRole('ROLE\_USER')"/>这句配置中，4.0以后版本都使用hasRole('ROLE\_USER')取代原来的ROLE_USER。**

**6、准备页面。**

**admin.jsp**

```
<%@ page contentType="text/html;charset=UTF-8" language="java" isELIgnored="false" %>
<%@page session="true" %>
<%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
   <h2>title:${title}</h2>
   <h2>message:${message}</h2>
   <c:if test="${pageContext.request.userPrincipal.name != null }">
       <h2>welcome you ,${pageContext.request.userPrincipal.name}</h2>
       <a href="<c:url value='/j_spring_security_logout'/>">Logout</a>
   </c:if>
</body>
</html>
```

**hello.jsp**


```
<%@ page contentType="text/html;charset=UTF-8" language="java" isELIgnored="false" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
     <h2>title:${title }</h2>
     <h2>message:${message }</h2>
</body>
</html>

```



**7、启动tomcat,访问项目http://localhost:8080/springsecurity/admin**

**初次访问http://localhost:8080/springsecurity/admin提示登录，这是springsecurity为我们提供的默认的登录页面**

![1686234202010181232413521176915289.png](https://images.jsdiff.com/1686234-20201018123241352-1176915289_1619964264998.png)

**用户名或者密码错误，登录失败**


![1686234202010181233345451556544101.png](https://images.jsdiff.com/1686234-20201018123334545-1556544101_1619964280395.png)

**登录成功，跳转欢迎页面**

![16862342020101812335640044803764.png](https://images.jsdiff.com/1686234-20201018123356400-44803764_1619964294149.png)


https://www.cnblogs.com/ifme/p/12188982.html
https://blog.csdn.net/cxy35/article/details/105272078