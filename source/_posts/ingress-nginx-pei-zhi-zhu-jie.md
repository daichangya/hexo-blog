---
title: ingress-nginx配置(注解)
id: 1405
date: 2024-10-31 22:01:54
author: daichangya
excerpt: 注解¶您可以将这些Kubernetes批注添加到特定的Ingress对象，以自定义其行为。小费注释键和值只能是字符串。其他类型，如布尔或数值必须被引用，即&quot;true&quot;，&quot;false&quot;，&quot;100&quot;。注意可以使用--annotations-pr
permalink: /archives/ingress-nginx-pei-zhi-zhu-jie/
categories:
- nginx
---

[](https://github.com/kubernetes/ingress-nginx/edit/master/docs/user-guide/nginx-configuration/annotations.md "编辑这个页面")

注解 
===========================

您可以将这些Kubernetes批注添加到特定的Ingress对象，以自定义其行为。

小费

注释键和值只能是字符串。其他类型，如布尔或数值必须被引用，即`"true"`，`"false"`，`"100"`。

注意

可以使用[`--annotations-prefix`命令行参数](../../cli-arguments/)更改注释前缀 ，但默认值为`nginx.ingress.kubernetes.io`，如下表所述。


|Name                       | type |
|---------------------------|------|
|[nginx.ingress.kubernetes.io/app-root](#rewrite)|string|
|[nginx.ingress.kubernetes.io/affinity](#session-affinity)|cookie|
|[nginx.ingress.kubernetes.io/affinity-mode](#session-affinity)|"balanced" or "persistent"|
|[nginx.ingress.kubernetes.io/auth-realm](#authentication)|string|
|[nginx.ingress.kubernetes.io/auth-secret](#authentication)|string|
|[nginx.ingress.kubernetes.io/auth-secret-type](#authentication)|string|
|[nginx.ingress.kubernetes.io/auth-type](#authentication)|basic or digest|
|[nginx.ingress.kubernetes.io/auth-tls-secret](#client-certificate-authentication)|string|
|[nginx.ingress.kubernetes.io/auth-tls-verify-depth](#client-certificate-authentication)|number|
|[nginx.ingress.kubernetes.io/auth-tls-verify-client](#client-certificate-authentication)|string|
|[nginx.ingress.kubernetes.io/auth-tls-error-page](#client-certificate-authentication)|string|
|[nginx.ingress.kubernetes.io/auth-tls-pass-certificate-to-upstream](#client-certificate-authentication)|"true" or "false"|
|[nginx.ingress.kubernetes.io/auth-url](#external-authentication)|string|
|[nginx.ingress.kubernetes.io/auth-cache-key](#external-authentication)|string|
|[nginx.ingress.kubernetes.io/auth-cache-duration](#external-authentication)|string|
|[nginx.ingress.kubernetes.io/auth-proxy-set-headers](#external-authentication)|string|
|[nginx.ingress.kubernetes.io/auth-snippet](#external-authentication)|string|
|[nginx.ingress.kubernetes.io/enable-global-auth](#external-authentication)|"true" or "false"|
|[nginx.ingress.kubernetes.io/backend-protocol](#backend-protocol)|string|HTTP,HTTPS,GRPC,GRPCS,AJP|
|[nginx.ingress.kubernetes.io/canary](#canary)|"true" or "false"|
|[nginx.ingress.kubernetes.io/canary-by-header](#canary)|string|
|[nginx.ingress.kubernetes.io/canary-by-header-value](#canary)|string|
|[nginx.ingress.kubernetes.io/canary-by-header-pattern](#canary)|string|
|[nginx.ingress.kubernetes.io/canary-by-cookie](#canary)|string|
|[nginx.ingress.kubernetes.io/canary-weight](#canary)|number|
|[nginx.ingress.kubernetes.io/client-body-buffer-size](#client-body-buffer-size)|string|
|[nginx.ingress.kubernetes.io/configuration-snippet](#configuration-snippet)|string|
|[nginx.ingress.kubernetes.io/custom-http-errors](#custom-http-errors)|[]int|
|[nginx.ingress.kubernetes.io/default-backend](#default-backend)|string|
|[nginx.ingress.kubernetes.io/enable-cors](#enable-cors)|"true" or "false"|
|[nginx.ingress.kubernetes.io/cors-allow-origin](#enable-cors)|string|
|[nginx.ingress.kubernetes.io/cors-allow-methods](#enable-cors)|string|
|[nginx.ingress.kubernetes.io/cors-allow-headers](#enable-cors)|string|
|[nginx.ingress.kubernetes.io/cors-allow-credentials](#enable-cors)|"true" or "false"|
|[nginx.ingress.kubernetes.io/cors-max-age](#enable-cors)|number|
|[nginx.ingress.kubernetes.io/force-ssl-redirect](#server-side-https-enforcement-through-redirect)|"true" or "false"|
|[nginx.ingress.kubernetes.io/from-to-www-redirect](#redirect-fromto-www)|"true" or "false"|
|[nginx.ingress.kubernetes.io/http2-push-preload](#http2-push-preload)|"true" or "false"|
|[nginx.ingress.kubernetes.io/limit-connections](#rate-limiting)|number|
|[nginx.ingress.kubernetes.io/limit-rps](#rate-limiting)|number|
|[nginx.ingress.kubernetes.io/permanent-redirect](#permanent-redirect)|string|
|[nginx.ingress.kubernetes.io/permanent-redirect-code](#permanent-redirect-code)|number|
|[nginx.ingress.kubernetes.io/temporal-redirect](#temporal-redirect)|string|
|[nginx.ingress.kubernetes.io/proxy-body-size](#custom-max-body-size)|string|
|[nginx.ingress.kubernetes.io/proxy-cookie-domain](#proxy-cookie-domain)|string|
|[nginx.ingress.kubernetes.io/proxy-cookie-path](#proxy-cookie-path)|string|
|[nginx.ingress.kubernetes.io/proxy-connect-timeout](#custom-timeouts)|number|
|[nginx.ingress.kubernetes.io/proxy-send-timeout](#custom-timeouts)|number|
|[nginx.ingress.kubernetes.io/proxy-read-timeout](#custom-timeouts)|number|
|[nginx.ingress.kubernetes.io/proxy-next-upstream](#custom-timeouts)|string|
|[nginx.ingress.kubernetes.io/proxy-next-upstream-timeout](#custom-timeouts)|number|
|[nginx.ingress.kubernetes.io/proxy-next-upstream-tries](#custom-timeouts)|number|
|[nginx.ingress.kubernetes.io/proxy-request-buffering](#custom-timeouts)|string|
|[nginx.ingress.kubernetes.io/proxy-redirect-from](#proxy-redirect)|string|
|[nginx.ingress.kubernetes.io/proxy-redirect-to](#proxy-redirect)|string|
|[nginx.ingress.kubernetes.io/proxy-http-version](#proxy-http-version)|"1.0" or "1.1"|
|[nginx.ingress.kubernetes.io/proxy-ssl-secret](#backend-certificate-authentication)|string|
|[nginx.ingress.kubernetes.io/proxy-ssl-ciphers](#backend-certificate-authentication)|string|
|[nginx.ingress.kubernetes.io/proxy-ssl-name](#backend-certificate-authentication)|string|
|[nginx.ingress.kubernetes.io/proxy-ssl-protocols](#backend-certificate-authentication)|string|
|[nginx.ingress.kubernetes.io/proxy-ssl-verify](#backend-certificate-authentication)|string|
|[nginx.ingress.kubernetes.io/proxy-ssl-verify-depth](#backend-certificate-authentication)|number|
|[nginx.ingress.kubernetes.io/enable-rewrite-log](#enable-rewrite-log)|"true" or "false"|
|[nginx.ingress.kubernetes.io/rewrite-target](#rewrite)|URI|
|[nginx.ingress.kubernetes.io/satisfy](#satisfy)|string|
|[nginx.ingress.kubernetes.io/server-alias](#server-alias)|string|
|[nginx.ingress.kubernetes.io/server-snippet](#server-snippet)|string|
|[nginx.ingress.kubernetes.io/service-upstream](#service-upstream)|"true" or "false"|
|[nginx.ingress.kubernetes.io/session-cookie-name](#cookie-affinity)|string|
|[nginx.ingress.kubernetes.io/session-cookie-path](#cookie-affinity)|string|
|[nginx.ingress.kubernetes.io/session-cookie-change-on-failure](#cookie-affinity)|"true" or "false"|
|[nginx.ingress.kubernetes.io/session-cookie-samesite](#cookie-affinity)|string|
|[nginx.ingress.kubernetes.io/session-cookie-conditional-samesite-none](#cookie-affinity)|"true" or "false"|
|[nginx.ingress.kubernetes.io/ssl-redirect](#server-side-https-enforcement-through-redirect)|"true" or "false"|
|[nginx.ingress.kubernetes.io/ssl-passthrough](#ssl-passthrough)|"true" or "false"|
|[nginx.ingress.kubernetes.io/upstream-hash-by](#custom-nginx-upstream-hashing)|string|
|[nginx.ingress.kubernetes.io/x-forwarded-prefix](#x-forwarded-prefix-header)|string|
|[nginx.ingress.kubernetes.io/load-balance](#custom-nginx-load-balancing)|string|
|[nginx.ingress.kubernetes.io/upstream-vhost](#custom-nginx-upstream-vhost)|string|
|[nginx.ingress.kubernetes.io/whitelist-source-range](#whitelist-source-range)|CIDR|
|[nginx.ingress.kubernetes.io/proxy-buffering](#proxy-buffering)|string|
|[nginx.ingress.kubernetes.io/proxy-buffers-number](#proxy-buffers-number)|number|
|[nginx.ingress.kubernetes.io/proxy-buffer-size](#proxy-buffer-size)|string|
|[nginx.ingress.kubernetes.io/proxy-max-temp-file-size](#proxy-max-temp-file-size)|string|
|[nginx.ingress.kubernetes.io/ssl-ciphers](#ssl-ciphers)|string|
|[nginx.ingress.kubernetes.io/connection-proxy-header](#connection-proxy-header)|string|
|[nginx.ingress.kubernetes.io/enable-access-log](#enable-access-log)|"true" or "false"|
|[nginx.ingress.kubernetes.io/enable-opentracing](#enable-opentracing)|"true" or "false"|
|[nginx.ingress.kubernetes.io/enable-influxdb](#influxdb)|"true" or "false"|
|[nginx.ingress.kubernetes.io/influxdb-measurement](#influxdb)|string|
|[nginx.ingress.kubernetes.io/influxdb-port](#influxdb)|string|
|[nginx.ingress.kubernetes.io/influxdb-host](#influxdb)|string|
|[nginx.ingress.kubernetes.io/influxdb-server-name](#influxdb)|string|
|[nginx.ingress.kubernetes.io/use-regex](#use-regex)|bool|
|[nginx.ingress.kubernetes.io/enable-modsecurity](#modsecurity)|bool|
|[nginx.ingress.kubernetes.io/enable-owasp-core-rules](#modsecurity)|bool|
|[nginx.ingress.kubernetes.io/modsecurity-transaction-id](#modsecurity)|string|
|[nginx.ingress.kubernetes.io/modsecurity-snippet](#modsecurity)|string|
|[nginx.ingress.kubernetes.io/mirror-request-body](#mirror)|string|
|[nginx.ingress.kubernetes.io/mirror-target](#mirror)|string|

### 金丝雀 

在某些情况下，您可能希望通过向少量与生产服务不同的服务发送少量请求来“取消”一组新的更改。Canary注释使Ingress规范可以充当路由请求的替代服务，具体取决于所应用的规则。`nginx.ingress.kubernetes.io/canary: "true"`设置后，可以启用以下用于配置金丝雀的注释：

*   `nginx.ingress.kubernetes.io/canary-by-header`：用于通知Ingress将请求路由到Canary Ingress中指定的服务的标头。当请求标头设置`always`为时，它将被路由到Canary。当标头设置`never`为时，它将永远不会路由到金丝雀。对于任何其他值，标头将被忽略，并且按优先级将请求与其他金丝雀规则进行比较。
    
*   `nginx.ingress.kubernetes.io/canary-by-header-value`：匹配的报头值，用于通知Ingress将请求路由到Canary Ingress中指定的服务。当请求标头设置为此值时，它将被路由到Canary。对于任何其他标头值，标头将被忽略，并按优先级将请求与其他金丝雀规则进行比较。此注释必须与一起使用。注释是的扩展，`nginx.ingress.kubernetes.io/canary-by-header`允许自定义标头值，而不使用硬编码值。如果`nginx.ingress.kubernetes.io/canary-by-header`未定义注释，则没有任何作用。
    
*   `nginx.ingress.kubernetes.io/canary-by-header-pattern`：这与`canary-by-header-value`PCRE Regex匹配相同。请注意，`canary-by-header-value`设置时，此注释将被忽略。当给定的正则表达式在请求处理期间导致错误时，该请求将被视为不匹配。
    
*   `nginx.ingress.kubernetes.io/canary-by-cookie`：用于通知Ingress将请求路由到Canary Ingress中指定的服务的cookie。当cookie值设置`always`为时，它将被路由到canary。当cookie设置`never`为时，它将永远不会路由到Canary。对于任何其他值，将忽略cookie，并按优先级将请求与其他canary规则进行比较。
    
*   `nginx.ingress.kubernetes.io/canary-weight`：随机请求的整数百分比（0-100），应将其路由到canary Ingress中指定的服务。权重0表示此Canary规则不会在Canary入口中将任何请求发送到服务。权重为100表示​​所有请求都将发送到Ingress中指定的替代服务。
    

金丝雀规则按优先级进行评估。优先级如下： `canary-by-header -> canary-by-cookie -> canary-weight`

**请注意**，当您将某个入口标记为canary时，除`nginx.ingress.kubernetes.io/load-balance`和之外，所有其他非canary注释将被忽略（从相应的主要入口继承）`nginx.ingress.kubernetes.io/upstream-hash-by`。

**已知局限性**

目前，每个Ingress规则最多可以应用一个Canary Ingress。

### Rewrite 

在某些情况下，后端服务中公开的URL与Ingress规则中指定的路径不同。如果没有重写，则任何请求都将返回404。将注释设置`nginx.ingress.kubernetes.io/rewrite-target`为服务所需的路径。

如果应用程序根目录暴露在其他路径中，并且需要重定向，请设置注释`nginx.ingress.kubernetes.io/app-root`以重定向的请求`/`。

例

请检查[重写](../../../examples/rewrite/)示例。

### Session Affinity 

注释`nginx.ingress.kubernetes.io/affinity`在Ingress的所有上游中启用和设置相似性类型。这样，请求将始终定向到同一上游服务器。NGINX唯一可用的相似性类型是`cookie`。

注释`nginx.ingress.kubernetes.io/affinity-mode`定义了会话的粘性。`balanced`如果将部署规模扩大，则将此选项设置为（默认）将重新分配一些会话，从而重新平衡服务器上的负载。将此设置为`persistent`不会重新平衡与新服务器的会话，因此提供了最大的粘性。

注意

如果为一个主机定义了多个Ingress `nginx.ingress.kubernetes.io/affinity: cookie`，并且至少一个Ingress使用，则只有Ingress使用的路径`nginx.ingress.kubernetes.io/affinity`将使用会话Cookie相似性。通过随机选择后端服务器，可以在主机的其他入口定义的所有路径进行负载均衡。

例

请检查[相似性](../../../examples/affinity/cookie/)示例。

#### Cookie Affinity

如果使用`cookie`亲缘关系类型，则还可以指定将用于通过注释路由请求的cookie的名称`nginx.ingress.kubernetes.io/session-cookie-name`。默认是创建一个名为“ INGRESSCOOKIE”的cookie。

NGINX批注`nginx.ingress.kubernetes.io/session-cookie-path`定义将在cookie上设置的路径。除非注释`nginx.ingress.kubernetes.io/use-regex`设置为true，否则这是可选的。会话Cookie路径不支持正则表达式。

使用`nginx.ingress.kubernetes.io/session-cookie-samesite`的应用`SameSite`属性粘饼干。浏览器接受的值是`None`，`Lax`和`Strict`。某些浏览器会拒绝带有的cookie `SameSite=None`，包括在`SameSite=None`规范之前创建的cookie （例如Chrome 5X）。其他浏览器错误地将`SameSite=None`cookie视为`SameSite=Strict`（例如，在OSX 14上运行的Safari）。要从`SameSite=None`浏览器中忽略这些不兼容的内容，请添加注释`nginx.ingress.kubernetes.io/session-cookie-conditional-samesite-none: "true"`。

### 认证方式 

可以添加身份验证，并在Ingress规则中添加其他注释。身份验证的来源是包含用户名和密码的机密。

注释是：

`nginx.ingress.kubernetes.io/auth-type: [basic|digest]` 

指示[HTTP身份验证类型：基本或摘要访问身份验证](https://tools.ietf.org/html/rfc2617)。

`nginx.ingress.kubernetes.io/auth-secret: secretName` 

Secret的名称，其中包含用户名和密码，这些用户名和密码被授予`path`对Ingress规则中定义的的访问权限。此注释还接受替代形式“名称空间/ secretName”，在这种情况下，秘密查找在引用的名称空间而不是Ingress名称空间中执行。

`nginx.ingress.kubernetes.io/auth-secret-type: [auth-file|auth-map]` 

本`auth-secret`可以有两种形式：

*   `auth-file`\-默认情况下，密钥`auth`内的htpasswd文件为秘密
*   `auth-map` -机密密钥是用户名，值是哈希密码

`nginx.ingress.kubernetes.io/auth-realm: "realm string"` 

例

请检查[身份验证](../../../examples/auth/basic/)示例。

### 自定义NGINX上游哈希 

NGINX支持客户端-服务器映射的负载平衡，该映射基于给定密钥的[一致哈希](http://nginx.org/en/docs/http/ngx_http_upstream_module.html#hash)值。键可以包含文本，变量或其任何组合。此功能允许请求粘性而不是客户端IP或cookie。将使用[ketama](http://www.last.fm/user/RJ/journal/2007/04/10/392555/)一致的哈希方法，该方法确保在上游组更改时仅将少数密钥重新映射到不同的服务器。

上游哈希的一种特殊模式称为子集。在这种模式下，上游服务器被分组为子集，粘性通过将密钥映射到子集而不是单个上游服务器来工作。从选定的粘性子集中随机选择特定的服务器。它提供了粘性和负载分配之间的平衡。

要为后端启用一致的哈希：

`nginx.ingress.kubernetes.io/upstream-hash-by`：nginx变量，文本值或它们的任意组合，以用于一致的哈希。例如`nginx.ingress.kubernetes.io/upstream-hash-by: "$request_uri"`，通过当前请求URI一致地哈希上游请求。

可以启用“子集”散列设置`nginx.ingress.kubernetes.io/upstream-hash-by-subset`：“ true”。这会将请求映射到节点的子集，而不是单个请求。`upstream-hash-by-subset-size`确定每个子集的大小（默认为3）。

请检查[chashsubset](../../../examples/chashsubset/deployment.yaml)示例。

### 自定义NGINX负载平衡 

这与[`load-balance`ConfigMap中的](../configmap/#load-balance)类似，但是每个入口配置负载平衡算法。

> 请注意，`nginx.ingress.kubernetes.io/upstream-hash-by`优先于此。如果`nginx.ingress.kubernetes.io/upstream-hash-by`未设置，则我们将退回到使用全局配置的负载平衡算法。

### 自定义NGINX上游虚拟主机 

通过此配置设置，您可以在以下语句中控制host的值：`proxy_set_header Host $host`，它是位置块的一部分。如果您需要通过以外的方式调用上游服务器，这将非常有用`$host`。

### 客户端证书认证 

可以使用“入口规则”中的附加注释来启用“客户端证书认证”。

注释是：

*   `nginx.ingress.kubernetes.io/auth-tls-secret: secretName`：包含完整的证书颁发机构链的密钥的名称，该链`ca.crt`可以针对此Ingress进行身份验证。此注释还接受替代形式“名称空间/ secretName”，在这种情况下，秘密查找在引用的名称空间而不是Ingress名称空间中执行。
*   `nginx.ingress.kubernetes.io/auth-tls-verify-depth`：提供的客户证书和证书颁发机构链之间的验证深度。
*   `nginx.ingress.kubernetes.io/auth-tls-verify-client`：启用客户端证书的验证。
*   `nginx.ingress.kubernetes.io/auth-tls-error-page`：如果发生证书身份验证错误，应重定向用户的URL /页面
*   `nginx.ingress.kubernetes.io/auth-tls-pass-certificate-to-upstream`：指示是否应将收到的证书传递给上游服务器。默认情况下是禁用的。

例

请检查[客户端证书](../../../examples/auth/client-certs/)示例。

注意

Cloudflare中**无法**使用带有客户端身份验证的TLS，**这**可能会导致意外行为。

Cloudflare仅允许使用Authenticated Origin Pulls，并且需要使用其自己的证书：[https](https://blog.cloudflare.com/protecting-the-origin-with-tls-authenticated-origin-pulls/) : [//blog.cloudflare.com/protecting-the-origin-with-tls-authenticated-origin-pulls/](https://blog.cloudflare.com/protecting-the-origin-with-tls-authenticated-origin-pulls/)

仅允许通过身份验证的原产拉取，并且可以按照其教程进行配置：[https](https://support.cloudflare.com/hc/en-us/articles/204494148-Setting-up-NGINX-to-use-TLS-Authenticated-Origin-Pulls) : [//support.cloudflare.com/hc/en-us/articles/204494148-Setting-up-NGINX-to-use-TLS-Authenticated-Origin -拉](https://support.cloudflare.com/hc/en-us/articles/204494148-Setting-up-NGINX-to-use-TLS-Authenticated-Origin-Pulls)

### 后端证书认证 

使用入口规则中的附加注释，可以使用证书对代理的HTTPS后端进行身份验证。

*   `nginx.ingress.kubernetes.io/proxy-ssl-secret: secretName`：使用证书`tls.crt`（`tls.key`PEM格式的密钥）指定用于对代理HTTPS服务器进行身份验证的密钥。它还应包含`ca.crt`PEM格式的受信任CA证书，该证书用于验证代理HTTPS服务器的证书。此注释还接受替代形式“名称空间/ secretName”，在这种情况下，秘密查找在引用的名称空间而不是Ingress名称空间中执行。
*   `nginx.ingress.kubernetes.io/proxy-ssl-verify`：启用或禁用对代理HTTPS服务器证书的验证。（默认值：关闭）
*   `nginx.ingress.kubernetes.io/proxy-ssl-verify-depth`：设置代理HTTPS服务器证书链中的验证深度。（默认值：1）
*   `nginx.ingress.kubernetes.io/proxy-ssl-ciphers`：指定对代理HTTPS服务器的请求的启用[密码](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_ssl_ciphers)。密码以OpenSSL库可以理解的格式指定。
*   `nginx.ingress.kubernetes.io/proxy-ssl-name`：允许设置[proxy\_ssl\_name](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_ssl_name)。这允许覆盖用于验证代理HTTPS服务器的证书的服务器名称。建立与代理HTTPS服务器的连接时，也会通过SNI传递此值。
*   `nginx.ingress.kubernetes.io/proxy-ssl-protocols`：启用对代理HTTPS服务器的请求的指定[协议](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_ssl_protocols)。

### 配置片段 

使用此注释，您可以将其他配置添加到NGINX位置。例如：

`nginx.ingress.kubernetes.io/configuration-snippet: |
  more_set_headers "Request-Id: $req_id";` 

### 自定义HTTP错误 

就像[`custom-http-errors`](../configmap/#custom-http-errors)ConfigMap中的值一样，此批注将设置NGINX `proxy-intercept-errors`，但仅针对与此入口相关联的NGINX位置。如果在入口上指定了[默认后端注释](#default-backend)，则错误将路由到该注释的默认后端服务（而不是全局默认后端）。不同的入口可以指定不同的错误代码集。即使多个入口对象共享相同的主机名，此注释也可以用于为每个入口截取不同的错误代码（例如，如果每个路径在不同的入口上，则对于同一主机名上的不同路径将截取不同的错误代码） 。如果`custom-http-errors` 也是全局指定的，在此批注中指定的错误值将覆盖给定入口的主机名和路径的全局值。

用法示例：

`nginx.ingress.kubernetes.io/custom-http-errors: "404,415"` 

### 默认后端 

此批注具有`nginx.ingress.kubernetes.io/default-backend: <svc name>`指定自定义默认后端的形式。这`<svc name>`是对您在其中应用此批注的相同名称空间中的服务的引用。此注释将覆盖全局默认后端。

当Ingress规则中的服务没有活动的端点时，将处理该服务的响应。如果同时设置了此注释和[custom-http-errors注释，](#custom-http-errors)它还将处理错误响应。

### 启用CORS 

要在Ingress规则中启用跨域资源共享（CORS），请添加注释 `nginx.ingress.kubernetes.io/enable-cors: "true"`。这将在服务器位置中添加一个部分以启用此功能。

可以使用以下注释来控制CORS：

*   `nginx.ingress.kubernetes.io/cors-allow-methods` 控制接受哪些方法。这是一个多值字段，以“，”分隔，仅接受字母（大写和小写）。
*   默认： `GET, PUT, POST, DELETE, PATCH, OPTIONS`
*   例： `nginx.ingress.kubernetes.io/cors-allow-methods: "PUT, GET, POST, OPTIONS"`
    
*   `nginx.ingress.kubernetes.io/cors-allow-headers` 控制接受哪些标题。这是一个多值字段，以“，”分隔，并接受字母，数字，\_和-。
    
*   默认： `DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization`
*   例： `nginx.ingress.kubernetes.io/cors-allow-headers: "X-Forwarded-For, X-app123-XPTO"`
    
*   `nginx.ingress.kubernetes.io/cors-allow-origin` 控制CORS接受的原产地。这是一个单字段值，格式如下：`http(s)://origin-site.com`或`http(s)://origin-site.com:port`
    
*   默认： `*`
*   例： `nginx.ingress.kubernetes.io/cors-allow-origin: "https://origin-site.com:4443"`
    
*   `nginx.ingress.kubernetes.io/cors-allow-credentials` 控制在CORS操作期间是否可以传递凭据。
    
*   默认： `true`
*   例： `nginx.ingress.kubernetes.io/cors-allow-credentials: "false"`
    
*   `nginx.ingress.kubernetes.io/cors-max-age` 控制可以将预检请求缓存多长时间。默认值：`1728000` 示例：`nginx.ingress.kubernetes.io/cors-max-age: 600`
    

注意

有关更多信息，请参见[https://enable-cors.org](https://enable-cors.org/server_nginx.html)

### HTTP2推送预加载。 

启用将“链接”响应标题字段中指定的预加载链接自动转换为推送请求的功能。

例

*   `nginx.ingress.kubernetes.io/http2-push-preload: "true"`

### 服务器别名 

允许使用注解在NGINX配置的服务器定义中定义一个或多个别名`nginx.ingress.kubernetes.io/server-alias: "<alias 1>,<alias 2>"`。这将创建具有相同配置的服务器，但是会向`server_name`指令添加新值。

注意

服务器别名不能与现有服务器的主机名冲突。如果是这样，服务器别名注释将被忽略。如果创建了服务器别名，然后又创建了具有相同主机名的新服务器，则新服务器配置将取代别名配置。

欲了解更多信息，请参阅[该`server_name`文档](http://nginx.org/en/docs/http/ngx_http_core_module.html#server_name)。

### Server Snippet段 

使用注释`nginx.ingress.kubernetes.io/server-snippet`，可以在服务器配置块中添加自定义配置。

`apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/server-snippet: |
        set $agentflag 0;

        if ($http_user_agent ~* "(Mobile)" ){
          set $agentflag 1;
        }

        if ( $agentflag = 1 ) {
          return 301 https://m.example.com;
        }` 

注意

每个主机只能使用一次此注释。

### 客户端主体缓冲区大小 

设置缓冲区大小，以读取每个位置的客户端请求正文。如果请求主体大于缓冲区，则将整个主体或仅将其一部分写入临时文件。默认情况下，缓冲区大小等于两个内存页。在x86，其他32位平台和x86-64上为8K。在其他64位平台上，通常为16K。此注释将应用于入口规则中提供的每个位置。

注意

注释值必须以Nginx可以理解的格式给出。

例

*   `nginx.ingress.kubernetes.io/client-body-buffer-size: "1000"` ＃1000字节
*   `nginx.ingress.kubernetes.io/client-body-buffer-size: 1k` ＃1千字节
*   `nginx.ingress.kubernetes.io/client-body-buffer-size: 1K` ＃1千字节
*   `nginx.ingress.kubernetes.io/client-body-buffer-size: 1m` ＃1兆字节
*   `nginx.ingress.kubernetes.io/client-body-buffer-size: 1M` ＃1兆字节

有关更多信息，请参见[http://nginx.org](http://nginx.org/en/docs/http/ngx_http_core_module.html#client_body_buffer_size)

### 外部认证 

要使用提供身份验证的现有服务，可以对Ingress规则进行注释，`nginx.ingress.kubernetes.io/auth-url`以指示应将HTTP请求发送到的URL。

`nginx.ingress.kubernetes.io/auth-url: "URL  to  the  authentication  service"` 

另外，可以设置：

*   `nginx.ingress.kubernetes.io/auth-method`： `<Method>`指定要使用的HTTP方法。
*   `nginx.ingress.kubernetes.io/auth-signin`： `<SignIn_URL>`指定错误页面的位置。
*   `nginx.ingress.kubernetes.io/auth-response-headers`： `<Response_Header_1, ..., Response_Header_n>`指定在身份验证请求完成后传递给后端的标头。
*   `nginx.ingress.kubernetes.io/auth-proxy-set-headers`： `<ConfigMap>`ConfigMap的名称，该名称指定要传递给身份验证服务的标头
*   `nginx.ingress.kubernetes.io/auth-request-redirect`： `<Request_Redirect_URL>` 指定X-Auth-Request-Redirect标头值。
*   `nginx.ingress.kubernetes.io/auth-cache-key`： `<Cache_Key>`这将启用对身份验证请求的缓存。指定身份验证响应的查找键。例如`$remote_user$http_authorization`。每个服务器和位置都有其自己的密钥空间。因此，缓存的响应仅在按服务器和按位置的基础上有效。
*   `nginx.ingress.kubernetes.io/auth-cache-duration`： `<Cache_duration>`根据身份验证响应的响应代码（例如）指定身份验证响应的缓存时间`200 202 30m`。有关详细信息，请参见[proxy\_cache\_valid](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_valid)。您可以指定多个逗号分隔的值：`200 202 10m, 401 5m`。默认为`200 202 401 5m`。
*   `nginx.ingress.kubernetes.io/auth-snippet`： `<Auth_Snippet>`指定用于外部身份验证的自定义代码段，例如

`nginx.ingress.kubernetes.io/auth-url: http://foo.com/external-auth
nginx.ingress.kubernetes.io/auth-snippet: |
    proxy_set_header Foo-Header 42;` 

> 注意：`nginx.ingress.kubernetes.io/auth-snippet`是可选注释。但是，它只能与结合使用`nginx.ingress.kubernetes.io/auth-url`，如果`nginx.ingress.kubernetes.io/auth-url`未设置，则将被忽略

例

请检查[external-auth](../../../examples/auth/external-auth/)示例。

#### 全局外部认证 

默认情况下，如果`global-auth-url`在NGINX ConfigMap中设置，则控制器会将所有请求重定向到提供身份验证的现有服务。如果您想为该入口禁用此行为，则可以`enable-global-auth: "false"`在NGINX ConfigMap中使用。 `nginx.ingress.kubernetes.io/enable-global-auth`：指示是否应将GlobalExternalAuth配置应用于此Ingress规则。默认值设置为`"true"`。

注意

有关更多信息，请参见[global-auth-url](../configmap/#global-auth-url)。

### 限速 

这些注释定义了对连接和传输速率的限制。这些可以用来减轻[DDoS攻击](https://www.nginx.com/blog/mitigating-ddos-attacks-with-nginx-and-nginx-plus)。

*   `nginx.ingress.kubernetes.io/limit-connections`：单个IP地址允许的并发连接数。超出此限制时，将返回503错误。
*   `nginx.ingress.kubernetes.io/limit-rps`：每秒从给定IP接受的请求数。突发限制设置为限制的5倍。当客户端超过此限制时， [将](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/configmap/#limit-req-status-code) 返回[limit-req-status-code](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/configmap/#limit-req-status-code) **_默认值：_** 503。
*   `nginx.ingress.kubernetes.io/limit-rpm`：每分钟从给定IP接受的请求数。突发限制设置为限制的5倍。当客户端超过此限制时， [将](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/configmap/#limit-req-status-code) 返回[limit-req-status-code](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/configmap/#limit-req-status-code) **_默认值：_** 503。
*   `nginx.ingress.kubernetes.io/limit-rate-after`：初始千字节数，之后将进一步限制对给定连接的响应的进一步传输。必须在启用[代理缓冲的情况](#proxy-buffering)下使用此功能。
*   `nginx.ingress.kubernetes.io/limit-rate`：每秒允许发送到给定连接的千字节数。零值禁用速率限制。必须在启用[代理缓冲的情况](#proxy-buffering)下使用此功能。
*   `nginx.ingress.kubernetes.io/limit-whitelist`：客户端IP源范围要从速率限制中排除。该值是逗号分隔的CIDR列表。

如果你在一个单一的入口规则指定多个注释，限制在顺序应用`limit-connections`，`limit-rpm`，`limit-rps`。

要为所有Ingress规则全局配置设置，可以在[NGINX ConfigMap中](../configmap/#limit-rate)设置`limit-rate-after`和`limit-rate`值。在Ingress注释中设置的值将覆盖全局设置。[](../configmap/#limit-rate)

当启用[use-forwarded-header](../configmap/#use-forwarded-headers)时，将基于[PROXY协议](../configmap/#use-proxy-protocol)的使用或从`X-Forwarded-For`标头值设置客户端IP地址。[](../configmap/#use-forwarded-headers)

### 永久重定向 

此注释允许返回永久重定向，而不是向上游发送数据。例如`nginx.ingress.kubernetes.io/permanent-redirect: https://www.google.com`，将所有内容重定向到Google。

### 永久重定向码 

此注释使您可以修改用于永久重定向的状态代码。例如，`nginx.ingress.kubernetes.io/permanent-redirect-code: '308'`将以308返回您的永久重定向。

### Temporal Redirect 

此注释使您可以返回时间重定向（返回代码302），而不是将数据发送到上游。例如`nginx.ingress.kubernetes.io/temporal-redirect: https://www.google.com`，将所有内容重定向到Google，返回码为302（临时移动）

### SSL直通 

注释`nginx.ingress.kubernetes.io/ssl-passthrough`指示控制器将TLS连接直接发送到后端，而不是让NGINX解密通信。另请参阅《用户指南》中的[TLS / HTTPS](../../tls/#ssl-passthrough)。

注意

SSL直通**默认情况下**处于**禁用状态，**并且需要使用该[`--enable-ssl-passthrough`](../../cli-arguments/)标志启动控制器 。

注意

由于SSL Passthrough在OSI模型（TCP）的第4层而不是第7层（HTTP）上起作用，因此使用SSL Passthrough会使在Ingress对象上设置的所有其他注释无效。

### Service Upstream

默认情况下，NGINX入口控制器使用NGINX上游配置中所有端点（Pod IP /端口）的列表。

该`nginx.ingress.kubernetes.io/service-upstream`注释禁用该行为，而是使用在NGINX，该服务的群集IP和端口的单一上游。

这对于零停机时间部署之类的事情可能是理想的，因为它减少了Pod上下时重新加载NGINX配置的需求。参见问题[＃257](https://github.com/kubernetes/ingress-nginx/issues/257)。

#### 已知的问题 

如果`service-upstream`指定了注释，则应考虑以下事项：

*   粘性会话将不起作用，因为仅支持循环负载平衡。
*   该`proxy_next_upstream`指令不会有任何影响，因为如果出错，该请求将不会分派到另一个上游。

### 通过重定向执行服务器端HTTPS 

默认情况下，如果为该入口启用了TLS，则控制器将重定向（308）到HTTPS。如果要全局禁用此行为，可以`ssl-redirect: "false"`在NGINX [ConfigMap中使用](../configmap/#ssl-redirect)。

要为特定的入口资源配置此功能，可以`nginx.ingress.kubernetes.io/ssl-redirect: "false"` 在特定资源中使用注释。

在群集外部（例如AWS ELB）上使用SSL卸载时，即使没有可用的TLS证书，强制执行到HTTPS的重定向也可能很有用。这可以通过使用`nginx.ingress.kubernetes.io/force-ssl-redirect: "true"`特定资源中的注释来实现。

### 从/重定向到www 

在某些情况下，需要从重定向`www.domain.com`到`domain.com`，反之亦然。要启用此功能，请使用注释`nginx.ingress.kubernetes.io/from-to-www-redirect: "true"`

注意

如果在某个时候创建​​了一个新的Ingress，且其宿主等于选项之一（如`domain.com`），则注释将被省略。

注意

对于从HTTPS到HTTPS的重定向是强制性的，位于Ingress TLS部分中的Secret中定义的SSL证书包含两个通用名称的FQDN。

### 白名单来源范围 

您可以通过`nginx.ingress.kubernetes.io/whitelist-source-range`注释指定允许的客户端IP源范围。该值是逗号分隔的[CIDR](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing)列表，例如 `10.0.0.0/24,172.10.0.1`。

要为所有Ingress规则全局配置此设置，`whitelist-source-range`可以在[NGINX ConfigMap中](../configmap/#whitelist-source-range)设置该值。

注意

向Ingress规则添加注释会覆盖所有全局限制。

### 自定义超时 

使用配置configmap可以为与上游服务器的连接设置默认的全局超时。在某些情况下，要求具有不同的值。为此，我们提供了允许进行此自定义的注释：

*   `nginx.ingress.kubernetes.io/proxy-connect-timeout`
*   `nginx.ingress.kubernetes.io/proxy-send-timeout`
*   `nginx.ingress.kubernetes.io/proxy-read-timeout`
*   `nginx.ingress.kubernetes.io/proxy-next-upstream`
*   `nginx.ingress.kubernetes.io/proxy-next-upstream-timeout`
*   `nginx.ingress.kubernetes.io/proxy-next-upstream-tries`
*   `nginx.ingress.kubernetes.io/proxy-request-buffering`

### 代理重定向 

使用注释`nginx.ingress.kubernetes.io/proxy-redirect-from`，`nginx.ingress.kubernetes.io/proxy-redirect-to`可以在[代理服务器响应](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_redirect)的`Location`和`Refresh`标头字段中设置应更改的文本[](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_redirect)

在注释中设置为“ off”或“ default” `nginx.ingress.kubernetes.io/proxy-redirect-from`会禁用`nginx.ingress.kubernetes.io/proxy-redirect-to`，否则，必须同时使用两个注释。请注意，每个注释必须是不带空格的字符串。

默认情况下，每个注释的值为“ off”。

### Custom max body size 

对于NGINX，当请求中的大小超过客户端请求正文的最大允许大小时，将向客户端返回413错误。该大小可以通过参数来配置[`client_max_body_size`](http://nginx.org/en/docs/http/ngx_http_core_module.html#client_max_body_size)。

要为所有Ingress规则全局配置此设置，`proxy-body-size`可以在[NGINX ConfigMap中](../configmap/#proxy-body-size)设置该值。要在Ingress规则中使用自定义值，请定义以下注释：

`nginx.ingress.kubernetes.io/proxy-body-size: 8m` 

### 代理Cookie域 

设置[应在](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cookie_domain)代理服务器响应的“ Set-Cookie”标头字段[的domain属性](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cookie_domain)中[更改](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cookie_domain)的文本。

要为所有Ingress规则全局配置此设置，`proxy-cookie-domain`可以在[NGINX ConfigMap中](../configmap/#proxy-cookie-domain)设置该值。

### 代理Cookie路径 

设置[应在](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cookie_path)代理服务器响应的“ Set-Cookie”标头字段[的path属性](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cookie_path)中[更改](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cookie_path)的文本。

要为所有Ingress规则全局配置此设置，`proxy-cookie-path`可以在[NGINX ConfigMap中](../configmap/#proxy-cookie-path)设置该值。

### 代理缓冲 

启用或禁用代理缓冲[`proxy_buffering`](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_buffering)。默认情况下，NGINX配置中禁用代理缓冲。

要为所有Ingress规则全局配置此设置，`proxy-buffering`可以在[NGINX ConfigMap中](../configmap/#proxy-buffering)设置该值。要在Ingress规则中使用自定义值，请定义以下注释：

`nginx.ingress.kubernetes.io/proxy-buffering: "on"` 

### 代理缓冲区数 

设置[`proxy_buffers`](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_buffers)用于读取从代理服务器接收到的响应的第一部分的缓冲区数。默认情况下，代理缓冲区数设置为4

要全局配置此设置，请`proxy-buffers-number`在[NGINX ConfigMap中进行](../configmap/#proxy-buffers-number)设置。要在Ingress规则中使用自定义值，请定义以下注释：

`nginx.ingress.kubernetes.io/proxy-buffers-number: "4"` 

### 代理缓冲区大小 

设置[`proxy_buffer_size`](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_buffer_size)用于读取从代理服务器接收到的响应的第一部分的缓冲区的大小。默认情况下，代理缓冲区大小设置为“ 4k”

要全局配置此设置，请`proxy-buffer-size`在[NGINX ConfigMap中进行](../configmap/#proxy-buffer-size)设置。要在Ingress规则中使用自定义值，请定义以下注释：

`nginx.ingress.kubernetes.io/proxy-buffer-size: "8k"` 

### 代理最大临时文件大小 

如果[`buffering`](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_buffering)启用了来自代理服务器的响应，并且整个响应不适合通过[`proxy_buffer_size`](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_buffer_size)和[`proxy_buffers`](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_buffers)指令设置的缓冲区，则可以将响应的一部分保存到临时文件中。此伪指令设置`size`临时文件的最大值，设置为[`proxy_max_temp_file_size`](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_max_temp_file_size)。一次写入临时文件的数据大小由[`proxy_temp_file_write_size`](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_temp_file_write_size)指令设置。

零值禁用对临时文件的响应的缓冲。

要在Ingress规则中使用自定义值，请定义以下注释：

`nginx.ingress.kubernetes.io/proxy-max-temp-file-size: "1024m"` 

### 代理HTTP版本 

使用此注释设置[`proxy_http_version`](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_http_version)Nginx反向代理将用于与后端通信的。默认情况下，它设置为“ 1.1”。

`nginx.ingress.kubernetes.io/proxy-http-version: "1.0"` 

### SSL密码 

指定[启用的密码](http://nginx.org/en/docs/http/ngx_http_ssl_module.html#ssl_ciphers)。

使用此注释将`ssl_ciphers`在服务器级别设置指令。该配置对主机中的所有路径均有效。

`nginx.ingress.kubernetes.io/ssl-ciphers: "ALL:!aNULL:!EXPORT56:RC4+RSA:+HIGH:+MEDIUM:+LOW:+SSLv2:+EXP"` 

### 连接代理头 

使用此注释将覆盖NGINX设置的默认连接头。要在Ingress规则中使用自定义值，请定义注释：

`nginx.ingress.kubernetes.io/connection-proxy-header: "keep-alive"` 

### 启用访问日志 

默认情况下，访问日志处于启用状态，但在某些情况下，可能需要针对给定的入口禁用访问日志。为此，请使用注释：

`nginx.ingress.kubernetes.io/enable-access-log: "false"` 

### 启用重写日志 

默认情况下，未启用重写日志。在某些情况下，可能需要启用NGINX重写日志。请注意，重写日志将在通知级别发送到error\_log文件。要启用此功能，请使用注释：

`nginx.ingress.kubernetes.io/enable-rewrite-log: "true"` 

### 启用开放追踪 

可以通过ConfigMap在全局范围内启用或禁用Opentracing，但是有时需要重写它才能启用它或针对特定入口禁用它（例如，关闭对外部运行状况检查端点的跟踪）

`nginx.ingress.kubernetes.io/enable-opentracing: "true"` 

### X转发前缀报头 

要`X-Forwarded-Prefix`使用字符串值将非标准标头添加到上游请求中，可以使用以下注释：

`nginx.ingress.kubernetes.io/x-forwarded-prefix: "/path"` 

### ModSecurity 

[ModSecurity](http://modsecurity.org/)是一个开源Web应用程序防火墙。可以为一组特定的入口位置启用它。首先必须通过在[ConfigMap中](../configmap/#enable-modsecurity)启用ModSecurity来启用ModSecurity模块 。请注意，这将为所有路径启用ModSecurity，并且必须手动禁用每个路径。

可以使用以下注释启用它：

`nginx.ingress.kubernetes.io/enable-modsecurity: "true"` 

ModSecurity将使用[推荐的配置](https://github.com/SpiderLabs/ModSecurity/blob/v3/master/modsecurity.conf-recommended)以“仅检测”模式[运行](https://github.com/SpiderLabs/ModSecurity/blob/v3/master/modsecurity.conf-recommended)。

您可以通过设置以下注释来启用[OWASP核心规则集](https://www.modsecurity.org/CRS/Documentation/)：

`nginx.ingress.kubernetes.io/enable-owasp-core-rules: "true"` 

您可以通过设置以下内容从nginx传递transactionID：

`nginx.ingress.kubernetes.io/modsecurity-transaction-id: "$request_id"` 

您还可以通过代码段添加自己的modsecurity规则集：

`nginx.ingress.kubernetes.io/modsecurity-snippet: |
SecRuleEngine On
SecDebugLog /tmp/modsec_debug.log` 

注意：如果同时使用`enable-owasp-core-rules`和和`modsecurity-snippet`批注，则只有 `modsecurity-snippet`会生效。如果要包括[OWASP核心规则集](https://www.modsecurity.org/CRS/Documentation/)或 [建议的配置，](https://github.com/SpiderLabs/ModSecurity/blob/v3/master/modsecurity.conf-recommended)只需使用include语句：

nginx 0.24.1及以下

`nginx.ingress.kubernetes.io/modsecurity-snippet: |
Include /etc/nginx/owasp-modsecurity-crs/nginx-modsecurity.conf
Include /etc/nginx/modsecurity/modsecurity.conf` 

nginx 0.25.0及更高版本

`nginx.ingress.kubernetes.io/modsecurity-snippet: |
Include /etc/nginx/owasp-modsecurity-crs/nginx-modsecurity.conf` 

### InfluxDB 

使用`influxdb-*`批注，我们可以使用[nginx-influxdb-module](https://github.com/influxdata/nginx-influxdb-module/)将请求发送到暴露UDP套接字的InfluxDB后端，从而监视通过位置的请求。

`nginx.ingress.kubernetes.io/enable-influxdb: "true"
nginx.ingress.kubernetes.io/influxdb-measurement: "nginx-reqs"
nginx.ingress.kubernetes.io/influxdb-port: "8089"
nginx.ingress.kubernetes.io/influxdb-host: "127.0.0.1"
nginx.ingress.kubernetes.io/influxdb-server-name: "nginx-ingress"` 

对于`influxdb-host`参数，您有两个选择：

*   使用配置为启用[UDP协议](https://docs.influxdata.com/influxdb/v1.5/supported_protocols/udp/)的InfluxDB服务器 。
*   将Telegraf作为Sidecar代理部署到Ingress控制器，该控制器配置为使用[套接字侦听器输入](https://github.com/influxdata/telegraf/tree/release-1.6/plugins/inputs/socket_listener)侦听UDP，并使用任何[输出插件（](https://github.com/influxdata/telegraf/tree/release-1.7/plugins/outputs)例如InfluxDB，Apache Kafka，Prometheus等）进行写入。（推荐）

重要的是要记住，此阶段没有DNS解析器，因此您必须将IP地址配置为`nginx.ingress.kubernetes.io/influxdb-host`。如果将Influx或Telegraf部署为Sidecar（同一吊舱中的另一个容器），这将变得很简单，因为您可以直接使用`127.0.0.1`。

### 后端协议 

使用`backend-protocol`注释可以指示NGINX应如何与后端服务通信。（`secure-backends`在旧版本中替换）有效值：HTTP，HTTPS，GRPC，GRPCS和AJP

默认情况下，NGINX使用`HTTP`。

例：

`nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"` 

### 使用正则表达式 

注意

当将此注释与`nginx.ingress.kubernetes.io/affinity`类型为NGINX的注释一起使用时`cookie`， `nginx.ingress.kubernetes.io/session-cookie-path`还必须设置；会话Cookie路径不支持正则表达式。

使用`nginx.ingress.kubernetes.io/use-regex`注释将指示Ingress上定义的路径是否使用正则表达式。默认值为`false`。

下面将指示正在使用正则表达式路径：

`nginx.ingress.kubernetes.io/use-regex: "true"` 

以下内容将指示**未**使用正则表达式路径：

`nginx.ingress.kubernetes.io/use-regex: "false"` 

当此批注设置为时`true`，不区分大小写的正则表达式[位置修饰符](https://nginx.org/en/docs/http/ngx_http_core_module.html#location)将在给定主机的所有路径上强制执行，无论它们定义在什么Ingress上。

此外，如果在给定主机的任何Ingress上使用了[`rewrite-target`注释](#rewrite)，则不区分大小写的正则表达式[位置修饰符](https://nginx.org/en/docs/http/ngx_http_core_module.html#location)将在给定主机的所有路径上强制执行，无论它们定义在什么Ingress上。

在使用此修饰符之前，请阅读有关[入口路径匹配的信息](../../ingress-path-matching/)。

### Satisfy 

默认情况下，请求将需要满足所有身份验证要求才能被允许。通过使用此批注，基于配置值，允许满足任何或所有身份验证要求的请求。

`nginx.ingress.kubernetes.io/satisfy: "any"` 

### Mirror 

允许将请求镜像到镜像后端。镜像后端的响应将被忽略。此功能很有用，可以查看请求在“测试”后端中的反应。

可以通过以下方式设置镜像后端：

`nginx.ingress.kubernetes.io/mirror-target: https://test.env.com/$request_uri` 

默认情况下，请求正文发送到镜像后端，但可以通过应用以下命令将其关闭：

`nginx.ingress.kubernetes.io/mirror-request-body: "off"` 

**注意：** mirror指令将应用于入口资源内的所有路径。

发送到镜像的请求链接到原始请求。如果您的镜像后端速度较慢，则原始请求将受到限制。

有关镜像模块的更多信息，请参见[ngx\_http\_mirror\_module](https://nginx.org/en/docs/http/ngx_http_mirror_module.html)