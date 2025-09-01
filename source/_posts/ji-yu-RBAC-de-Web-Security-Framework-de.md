---
title: 基于 RBAC 的 Web Security Framework 的研究与应用
id: 785
date: 2024-10-31 22:01:46
author: daichangya
excerpt: 基于角色的访问控制（RBAC）已经成为一种成熟的访问控制模型，被越来越多地用在认证授权系统中。本文首先分析了基于角色的访问控制模型的特点，研究了
  Web 开发领域中比较常见的框架，并基于 Spring Security 探讨如何在 Web 系统中快速便捷地实现认证和授权系统。
permalink: /archives/ji-yu-RBAC-de-Web-Security-Framework-de/
categories:
- spring
tags:
- 权限
---

## 访问控制与 RBAC 模型

### 访问控制

通常的多用户系统都会涉及到访问控制，所谓访问控制，是指通过某种方式允许活限制用户访问能力及范围的一种方法。这主要是由于系统需要对关键资源进行保护，防止由于非法入侵或者误操作对业务系统造成破坏。简而言之，访问控制即哪些用户可以访问哪些资源。

一般而言，访问控制系统包括三个组成部分：

*   主体：发出访问请求的实体，通常指用户或者用户进程。
*   客体：被保护的资源，通常是程序，数据，文件或者设备。
*   访问策略：主体和客体的映射规则，确定一个主体是否对客体具有访问能力。

### RBAC 模型

基于角色的访问控制（RBAC）的概念在七十年代就已经提出，但是直到九十年代由于安全需求的发展才又引起了广泛关注。RBAC 的核心思想是将系统资源的访问权限进行分类或者建立层次关系，抽象为角色的概念，然后根据安全策略将用户和角色关联，从而实现了用户和权限之间的对照。RBAC 通过引入角色并将其作为权限管理的中介，将访问控制系统分为两个部分，即权限与角色的关联和角色与用户的关联，具有灵活易控制的优点。

RBAC 模型的建立和实现是基于角色实现访问控制研究中的两大热点。RBAC96 模型因全面系统地描述了多层次的含义而得到广泛认可。美国国家标准技术协会（NIST）基于 RBAC96 制定了 RBAC 标准，将 RBAC 主要分为 :Core RBAC, Hierarchical RBAC, Constraint RBAC。

RBAC96 模型包含 4 个层次，如图 1 所示：

##### 图 1\. RBAC96 模型

![RBAC96 模型](https://www.ibm.com/developerworks/cn/java/j-lo-rbacwebsecurity/image003.gif)


其中：

*   RBAC0：包含 RBAC 的核心部分即 Core RBAC，是最基本的模型，仅包含基本的 RBAC 元素，即用户，角色，权限，会话。角色之间是平级关系，对象之间没有附加的约束。
*   RBAC1：在 RBAC0 的基础上定了角色继承关系。
*   RBAC2：同样包含了 RBAC0，并且定义了约束，实际中需要考虑的常见的约束包括角色互斥和角色基数两种。
*   RBAC3：包含了 RBAC1 和 RBAC2，即既有角色的继承关系，又包含约束关系，是最复杂的一种模型。

图 2 清晰描述了 RBAC 模型中的用户，角色，权限，继承关系，约束关系。

##### 图 2\. RBAC 模型关系图

![RBAC 模型关系图](https://www.ibm.com/developerworks/cn/java/j-lo-rbacwebsecurity/image005.gif)


约束是 RBAC 的一个重要组成部分，比较常见的约束包括：

*   互斥角色约束：指的是同一用户只可以分配到互斥角色集合中最多一个角色，以支持“职责分离”的原则。
*   必备角色约束：也称为先决条件约束，是定义在用户角色分配关系（UA）和权限角色分配关系（PA）上的重要约束，是指所分配的角色或者权限依赖于另外一种角色或者权限。
*   基数约束：同样也是定义在 UA 和 PA 上的约束，规定了一个角色可以被分配的最大用户数或者一项权限可允许分配的角色数目，从而来控制高级权限在系统中的分配。

## 流行的 Web Security Framework

随着网络应用的不断发展，越来越多的应用系统开始移植到 Web 环境，并且具有不同程度的访问控制的需求。随着这种需求的积累，出现了很多基于 RBAC 的 web 访问控制框架，这些框架的核心理论就是 RBAC，并且为开发人员提供了方便的接口来完成定制化的需求。

### Membership in Asp.net

ASP.NET 中提供了非常好的用户身份认证的管理框架 – Membership，提供的功能包括创建新用户，身份认证，密码管理等。默认情况下，ASP.NET Membership 可以支持所有的 ASP.NET 应用程序，并提供了非常友好的使用方式，甚至提供了向导来创建所需要的数据结构—— aspnet_regsql.exe。

##### 图 3\. Membership 数据模型

![Membership 数据模型](https://www.ibm.com/developerworks/cn/java/j-lo-rbacwebsecurity/image007.gif)

.NET 平台的易用性毋庸置疑，开发者只需要配置 web.config 文件，引入 authentication 配置，增加 membership 节点，再配置其角色管理 roleManager 基本上就完成了对 membership 的引用。并且 .NET 甚至提供了用户控件 login 和 createUserWizard 等，通过属性的简单配置即可激活 membership 的认证，完成创建用户的功能等等。

本文中的企业应用没有基于 .NET 平台的 membership 来实现，因此 membership 并不是本文的重点，不再赘述。

### Spring Security in Java

Java Web 开发领域中的用于进行认证授权的框架为数众多，单就从 RBAC 的角度而言，Spring Security 已经占据重要的地位，并且被越来越广泛，越来越多地应用在各种 web 系统中，为基于 J2EE 企业应用软件提供了全面安全服务。

Spring Security 来源于早期的 Spring 开发者邮件列表中的一个问题——提供一个基于 Spring 的安全实现，最初被称之为 Acegi，在 2003 年初作为 Sourceforge 的项目出现，并得到不断的应用和完善。2007 年底，它正式成为 Spring 的组合项目，更名为 Spring Security，目前的最新版本是 3.1.0。

接下来，我们将基于最新版本来重点研究 Spring Security 的架构，并基于实际应用需求来讨论一些定制化的实现方法。

## Spring Security 概述

### Spring Security 项目概览

Spring Security 的上手非常简单，当然，这需要您对基本的认证授权有一些应用的背景，并能了解一些其中的核心概念，如上文提到的用户，角色，权限等等。通过 Spring Security 项目的首页（http://static.springsource.org/spring-security/site/index.html），您可以方便地得到它的介绍、文档、样例等等，并且，您还可以基于 Spring Security 的源码构建您的工程。这样，您可以深入地了解它的底层实现，快速地定位问题，方便地进行进一步扩展。

### Spring Security 特性

Spring Security 为企业级应用提供了方便、灵活的安全解决方案，在众多的项目应用中得到锤炼和修正，已经非常稳定和强大。Spring Security 具有如下的特性：

*   易于部署：通过 Spring 的依赖注入，Spring Security 提供了自定义的 XML 命名空间，可以通过不超过 10 行的配置就可以让您的应用程序受到保护。当然，这并不要求您的应用程序一定是基于 Spring 的，Spring Security 和 Struts 的结合使用非常普遍。
*   非侵入式引用：通过 Spring Security 的 filter chain，应用程序基本上不需要做额外的太多的修改，通过可插拔的方式，保证了应用程序本身和 Security 相关的代码的各自独立。
*   明晰的授权服务：通过基于表达式的配置，安全访问控制规则可以方便灵活地基于当前请求上下文进行定义，不需要额外进行编码。

同时 Spring Security 支持多种认证方式，并提供了定义良好的 API，多样化的认证后端等等，并且允许客户应用程序使用多种授权库，比如 XML 文件，数据库等，方便和既有的数据库系统进行集成。而且，它还提供了很多实用的功能，比如密码加密、Remember-me 持久化登录信息等等。

### RBAC 中的主要概念在 Spring Security 中的对照

RBAC 中的几个主要构成在 Spring Security 中得到了很好的对应。

*   主体：Spring Security 中的 Authentication 对象就是 RBAC 中的主体，多数情况下，可以被强制转换为 UserDetails 对象，这是一个 Spring Security 的核心接口，它代表一个主体，是扩展的，而且是为特定程序服务的，获得用户信息的最常用方法就是 loadUserByUsername(String username)，当成功通过验证时，UserDetails 会被用来建立 Authentication 对象，保存在 SecurityContextHolder 里。
*   客体：Spring Security 中的客体可以是 url，也可以是 method。
*   访问策略接口：Spring Security 通过 getAuthorities() 方法提供了 GrantedAuthority 对象数组，代表赋予到主体的权限。 这些权限通常使用角色表示，比如本文中计费系统中声明的角色 ROLE\_ADMINISTRATOR 或 ROLE\_PROVIDER。

### Spring Security 核心服务

**Security Filter Chain**

Spring Security 框架提供了一个过滤器链，来提供各种服务。通过下面的过滤器链表格，我们可以看到 Spring Security 为我们提供了哪些实用的服务。

##### 表 1\. Spring Security 过滤器清单

| 别名 | 过滤器类 | 对应的命名空间元素 |
| --- | --- | --- |
| CHANNEL_FILTER | ChannelProcessingFilter | http/intercept-url@requires-channel |
| CONCURRENT\_SESSION\_FILTER | ConcurrentSessionFilter | session-management/concurrency-control |
| SECURITY\_CONTEXT\_FILTER | SecurityContextPersistenceFilter | http |
| LOGOUT_FILTER | LogoutFilter | http/logout |
| X509_FILTER | X509AuthenticationFilter | http/x509 |
| PRE\_AUTH\_FILTER | AstractPreAuthenticatedProcessingFilter | N/A |
| CAS_FILTER | CasAuthenticationFilter | N/A |
| FORM\_LOGIN\_FILTER | UsernamePasswordAuthenticationFilter | http/form-login |
| BASIC\_AUTH\_FILTER | BasicAuthenticationFilter | http/http-basic |
| SERVLET\_API\_SUPPORT_FILTER | SecurityContextHolderAwareFilter | http/@servlet-api-provision |
| REMEMBER\_ME\_FILTER | RememberMeAuthenticationFilter | http/remember-me |
| ANONYMOUS_FILTER | SessionManagementFilter | http/anonymous |
| SESSION\_MANAGEMENT\_FILTER | AnonymousAuthenticationFilter | session-management |
| EXCEPTION\_TRANSLATION\_FILTER | ExceptionTranslationFilter | http |
| FILTER\_SECURITY\_INTERCEPTOR | FilterSecurityInterceptor | http |
| SWITCH\_USER\_FILTER | SwitchUserAuthenticationFilter | N/A |

开发人员可以使用 before 或者 after 属性来将自定义的过滤器添加到过滤器链中。本文中的计费系统中采用了自定义的 loginFilter 和 logoutFilter，并使用 before 属性将其分别置于 FORM\_LOGIN\_FILTER 和 LOGOUT_FILTER 之前，如清单 1 所示：

##### 清单 1\. 过滤器配置示例

```
<custom-filter before="FORM_LOGIN_FILTER" ref="loginFilter" />
<custom-filter before="LOGOUT_FILTER" ref="logoutFilter" />
```

**AuthenticationManager**

AuthenticationManager 只是一个接口，其实现可以让开发人员灵活选择。在 Spring Security 中的默认实现是 ProviderManager，Spring Security 通过委派一系列配置好的 AuthenticationProvider，遍历 Providers 的过程中调用 authenticate() 方法 , 以保证获取不同来源的身份认证，若某个 Provider 能成功确认当前用户的身份，authenticate() 方法会返回一个完整的包含用户授权信息的 Authentication 对象，否则会抛出一个 AuthenticationException。

**AccessDecisionManager**

当我们使用命名空间配置时，默认的 AccessDecisionManager 实例会自动注册，基于我们设置的 intercept-url 和 protect-pointcut 权限属性内容，来为方法级别调用和 web 请求级别访问提供认证服务。

## 基于 Spring Security 实现认证授权

### Spring Security 的数据模型

多数基于 RBAC 的框架都提供了基础的数据模型，通常，我们需要对其进行扩展来满足企业级应用系统的需求。扩展的方式一般有两种，即在原有数据结构上进行修改，扩展自定义字段；或者，通过表之间的关联将应用系统的数据结构和 RBAC 的数据结构分离。两种方式各有优劣 , 通常需要看应用的复杂程度及对框架的开放程度进行不同的选择。

本文中计费系统因为用户角色权限关系清晰，故采用在原有数据结构基础上进行自定义数据字段的方式，比如，在 Users 表中增加了系统用户的一些属性，如联系方式，电话等等。

### 快速实现

**计费系统认证授权需求**

Spring Security 可以被应用在多种不同的认证环境下，因为它的目标是自管理，即不依赖于容器，所以备受推崇，因为这样可以方便地进行部署和移植。

计费系统中主要包含三类用户，即超级管理员，运营商管理员和普通用户。每种用户可以使用的系统功能模块集合和数据集合是不同的。比如，运营商管理员不能使用网关设备管理模块，并且只能管理属于自己的用户，而超级管理员可以管理网关设备，并且可以管理全部用户。

因为 Spring Security 基于 URL 实现对资源的授权，所以在开发初期，我们需要规划好资源的路径，以便于进行授权配置，即建立 admin，provider，customer 目录，网关设备的管理目录放在 admin 目录下，而超级管理员和运营商管理员都具有的功能模块放在 provider 目录下。

**引入 Spring Security**

通过上面的需求分析，可以看出，使用 Spring Security 完全可以实现计费系统的认证授权功能，并且可以非常快速地验证。

首先，我们要将需要的 jar 文件引入到工程中，包括：

*   spring-security-acl-3.0.3.RELEASE.jar
*   spring-security-config-3.0.3.RELEASE.jar
*   spring-security-core-3.0.3.RELEASE.jar
*   spring-security-taglibs-3.0.3.RELEASE.jar
*   spring-security-web-3.0.3.RELEASE.jar

其次，我们需要完成以下几个部分的修改：

1.  修改 web.xml 设置过滤器，代码如清单 2 所示。
    
    ##### 清单 2\. Web.XML 配置示例
    
    ```
    <filter>
    <filter-name>springSecurityFilterChain</filter-name>
      <filter-class>org.springframework.web.filter.DelegatingFilterProxy
         </filter-class>
    </filter>
    <filter-mapping>
        <filter-name>springSecurityFilterChain</filter-name>
        <url-pattern>/*</url-pattern>
    </filter-mapping>
    ```
    
2.  修改 applicationContext-Security.xml，这个文件可以根据需要设定，在容器启动时记载，其中设置了实现 HTTP 安全和认证授权相关的服务 Bean 来应用框架的认证授权功能，如清单 3 所示。
    
    ##### 清单 3\. applicationContext-Security.xml 配置示例
    
    ```
    <http entry-point-ref="loginUrlEntryPoint" access-denied-page="/common/403.jsp">
       <intercept-url pattern="/image/**" filters="none" />
       <intercept-url pattern="/common/**" filters="none" />
       <intercept-url pattern="/admin/**" access="ROLE_ADMIN" />
       <intercept-url pattern="/admin_provider/**" access="ROLE_ADMIN" />
       <intercept-url pattern="/admin_provider/**" access="ROLE_PROVIDER" />
    <!-- 登录过滤器 -->
        <custom-filter before="FORM_LOGIN_FILTER" ref="loginFilter" />
        <custom-filter position="FORM_LOGIN_FILTER" ref="adminLoginFilter" />
        <!-- 注销过滤器 -->
        <custom-filter before="LOGOUT_FILTER" ref="logoutFilter" />
        <custom-filter position="LOGOUT_FILTER" ref="adminLogoutFilter" />
    </http>
    <authentication-manager alias="authenticationManager">
        <authentication-provider user-service-ref="usersService">
        </authentication-provider>
    </authentication-manager>
    ```
    
3.  实现自定义的 userDetailsService ——通常我们需要对认证授权相关的数据结构进行其他的操作，这些操作并没有集成在 Spring Security 中，因此多数我们需要实现自己的 userDetailsService，如清单 4 所示。
    
    ##### 清单 4\. userDetailsService Bean 配置示例
    
    ```
    <beans:bean id="usersService" class="com.fengfan.service.impl.UsersServiceImpl">
        <beans:property name="dataSource" ref="dataSource"/>
        <beans:property name="authenticationManager" ref="authenticationManager"/>
        <beans:property name="usersDAO" ref="usersDAO"/>
    </beans:bean>
    ```
    
    通过以上几部分的修改，我们就可以方便地集成 Spring Security，进入企业应用系统的认证授权开发了。接下来，我们将讨论更多的定制化需求的实现方式，以此来说明 Spring Security 在企业级应用系统开发中的可扩展性和灵活性及易用性。
    

### 定制化需求

计费系统中有很多定制化的需求实现，下面，我们将就各个需求点进行说明，Spring Security 的成熟度和灵活性在这里得到了充分的体现。

**基于 URL 的授权实现**

通过上面的系统需求，我们实现了清单 5 所示的基于 URL 的权限约束：

##### 清单 5\. 基于 URL 的权限约束

```
<intercept-url pattern="/admin/**" access="ROLE_ADMIN" />
<intercept-url pattern="/admin_provider/**" access="ROLE_ADMIN" />
<intercept-url pattern="/admin_provider/**" access="ROLE_PROVIDER" />
```

这种资源的授权方式要求在开发初期对目录结构进行较清晰的规划，从而避免相同功能页面的重复拷贝的问题。当然，我们可以将资源及授权操作通过数据结构的进一步扩展都保存在数据库中，这样具有更大的灵活性。

**自定义的 UserDetailsService**

除了认证授权涉及到系统用户外，系统本身需要提供对系统用户的信息维护功能，因此，我们需要自定义 UserDetailsService，这也非常方便，我们只需要继承 JdbcUserDetailsManager，并实现 IUsersService 接口即可。这样，我们就可以在 UsersServiceImpl 中实现定制的和系统用户相关的方法，同时通过继承也得到了和安全认证相关的方法，如清单 6 所示。

##### 清单 6\. UsersServiceImpl 方法声明

```
public class UsersServiceImpl extends JdbcUserDetailsManager implements IusersService
```

**如何使用 Remember-Me**

通常我们在应用系统中如果要实现这个功能，需要增加一定的编码工作才能实现，需要操作 cookies 对象。但是 Spring Security 为 remember-me 实现提供了必要的调用钩子，并提供了两个 remember-me 的具体实现。 其中一个使用散列来保护基于 cookie 标记的安全性，另一个使用了数据库或其他持久化存储机制来保存生成的标记。我们只需要在 <http> 段下面添加 <remember-me> 元素就可以使用 remember-me 认证。

**会话同步控制**

首先，您需要把下面的监听器添加到您的 web.xml 文件里，让 Spring Security 获得 session 生存周期事件： <listener><listener-class> org.springframework.security.web.session.HttpSessionEventPublisher </listener-class> </listener> 。然后可以在 HTTP 安全配置中增加一个 session-management 段的配置，设置其中的 concurrency-control 来控制一个帐号最多允许登录多少次，比如 <concurrency-control max-sessions="1" error-if-maximum-exceeded="true"/>，这样，当重复登录时就会出现错误提示。

**不同的登录页面**

在上面的 HTTP 安全的设置部分，我们已经看到为不同的用户的登录和退出设置了不同的自定义过滤器，下面我们通过超级管理的 loginFilter 的配置来说明如何实现不同的用户登录之后到不同的主页，如清单 7 所示。

##### 清单 7\. 超级管理员的登录配置

```
<!-- 超级管理员登录 -->
<beans:bean id="adminLoginFilter"
class="
org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter
">
    <beans:property name="authenticationManager" ref="authenticationManager" />
    <beans:property name="authenticationFailureHandler"
            ref="adminFailureHandler" />
    <beans:property name="authenticationSuccessHandler"
            ref="adminSuccessHandler" />
    <beans:property name="filterProcessesUrl" value="/login_admin" />
</beans:bean>
```

从上面的配置我们看到当登录成功后，使用 authenticationSuccessHandler 来处理后续动作，我们来看一下如下的这个 bean 的配置，就可以明白如何通过 defaultTargetUrl 属性来设置其登录成功之后跳转的页面了，我们只需要在配置另外一个 bean，设置不同的属性值，就可以实现不同用户登录之后到达不同的主页面的需求，如清单 8 所示。

##### 清单 8\. 不同主页面跳转配置

```
<beans:bean id="adminSuccessHandler"
class="com.fengfan.security.AppAuthenticationSuccessHandler">
    <beans:property name="alwaysUseDefaultTargetUrl" value="true" />
    <beans:property name="defaultTargetUrl" value="/admin/index.jsp" />
    <beans:property name="usersDAO" ref="usersDAO"/>
</beans:bean>
```

同样的，我们可以设置不同的 logoutFilter，这样不同角色的用户选择退出系统之后可以拥有不同的退出成功的页面或者跳转的相应的重新登录的页面。

**修改认证信息后不需要重新登录**

很多时候，用户在登录之后可能对自身的信息进行修改，但是，我们不需要用户来重新登录，而是希望修改的信息在当前的会话中立即生效，Spring Security 提供了相应的接口方便我们实现这种需求，比如我们在用户修改密码之后，将主体中的信息也同时更新，如清单 9 所示。

##### 清单 9\. 修改密码代码示范

```
userCache.removeUserFromCache(username);
SecurityContextHolder.getContext().setAuthentication(
   createNewAuthentication(currentUser, newPassword));
```

## 总结

本文从计费系统的实际应用出发，通过分析系统的认证授权需求，研究 RBAC 的基础模型和 Spring Security 框架的核心组件及服务，充分发挥 Spring Security 的成熟度和灵活性的优势，快速完善地实现了计费管理中的认证授权系统，取得了很好的效果。

* * *

#### 相关主题

*   查看文章“[Role Based Access Control （RBAC) and Role Based Security](http://csrc.nist.gov/groups/SNS/rbac/)”，了解 RBAC 模型的基本原理。
*   查看文章“[An Introduction to Role-based Access Control](http://csrc.nist.gov/groups/SNS/rbac/documents/design_implementation/Intro_role_based_access.htm)”，了解常见 RBAC 模型及应用。
*   查看文章“[Spring Security](http://static.springsource.org/spring-security/site/)”，了解 Spring Security 的设计和使用。
*   查看文章“[Introduction to Membership](http://msdn.microsoft.com/en-us/library/yh26yfzy.aspx)”，了解微软身份认证管理框架。
*   [developerWorks Java 技术专区](http://www.ibm.com/developerworks/cn/java/)：这里有数百篇关于 Java 编程各个方面的文章。
