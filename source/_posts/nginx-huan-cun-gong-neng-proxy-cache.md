---
title: nginx 缓存功能(proxy_cache)
id: 1331
date: 2024-10-31 22:01:51
author: daichangya
excerpt: 本节介绍如何启用和配置从代理服务器收到的响应的缓存。总览启用响应缓存缓存涉及的NGINX进程指定要缓存的请求限制或绕过缓存从缓存中清除内容配置缓存清除发送清除命令限制对清除命令的访问从缓存中完全删除文件缓存清除配置示例字节范围缓存组合配置示例总览启用缓存后，NGINXPlus将响应保存在磁盘缓存中，
permalink: /archives/nginx-huan-cun-gong-neng-proxy-cache/
categories:
- nginx
tags:
- 最新文章
---

本节介绍如何启用和配置从代理服务器收到的响应的缓存。

*   [总览](#overview)
*   [启用响应缓存](#enable)
*   [缓存涉及的NGINX进程](#processes)
*   [指定要缓存的请求](#select)
*   [限制或绕过缓存](#bypass)
*   [从缓存中清除内容](#purge)
    *   [配置缓存清除](#purge_configure)
    *   [发送清除命令](#purge_request)
    *   [限制对清除命令的访问](#purge_secure)
    *   [从缓存中完全删除文件](#purge_remove)
    *   [缓存清除配置示例](#purge_example)
*   [字节范围缓存](#slice)
*   [组合配置示例](#example)

总览[](#overview "固定到该标题")
------------------------

启用缓存后，NGINX Plus将响应保存在磁盘缓存中，并使用它们来响应客户端，而不必每次都代理相同内容的请求。

要了解有关NGINX Plus缓存功能的更多信息，请观看[NGINX](https://nginx.com/resources/webinars/content-caching-nginx-plus/)网络研讨会的[内容缓存，](https://nginx.com/resources/webinars/content-caching-nginx-plus/)并深入了解动态[内容缓存](https://nginx.com/products/nginx/caching/)，缓存清除和延迟缓存等功能。

启用响应缓存[](#enabling-the-caching-of-responses "固定到该标题")
-----------------------------------------------------

要启用缓存，请将[`proxy_cache_path`](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_path)指令包含在顶级上下文中。强制性的第一个参数是缓存内容的本地文件系统路径，而强制性参数定义用于存储有关缓存项的元数据的共享内存区的名称和大小：`http {}``keys_zone`
```
http  { 
    ... 
    proxy_cache_path  /data/nginx/cache  keys_zone = one：10m ; 
}
```

然后[`proxy_cache`](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache)在要为其缓存服务器响应的上下文（协议类型，虚拟服务器或位置）中包含该指令，并为该指令指定`keys_zone`参数定义的区域名称`proxy_cache_path`（在本例中为`one`）：
```
http {
    ...
    proxy_cache_path /data/nginx/cache keys_zone=one:10m;
    server {
        proxy_cache mycache;
        location / {
            proxy_pass http://localhost:8000;
        }
    }
}
```
请注意，`keys_zone`参数定义的大小并不限制缓存的响应数据的总量。缓存的响应本身与元数据的副本一起存储在文件系统上的特定文件中。要限制缓存的响应数据量，请`max_size`在[`proxy_cache_path`](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_path)指令中包含参数。（但是请注意，缓存的数据量可能会暂时超过此限制，如下一节所述。）

缓存涉及的NGINX进程[](#nginx-processes-involved-in-caching "固定到该标题")
-------------------------------------------------------------

缓存还涉及另外两个NGINX流程：

*   该**高速缓存管理器**周期性地起动，检查高速缓存的状态。如果高速缓存大小超出了`max_size`参数由[`proxy_cache_path`](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_path)伪指令设置的限制，则高速缓存管理器将删除最近最少访问的数据。如前所述，在缓存管理器激活之间的时间间隔内，缓存的数据量可能会暂时超过限制。
*   该**缓存加载器**只运行一次，NGINX开始之后。它将有关先前缓存的数据的元数据加载到共享内存区域中。在启动后的最初几分钟内，一次加载整个缓存可能会消耗足够的资源，从而降低NGINX的性能。为避免这种情况，请通过在[`proxy_cache_path`](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_path)伪指令中包含以下参数来配置缓存的迭代加载：
    *   `loader_threshold`–迭代持续时间，以毫秒为单位（默认为 `200`）
    *   `loader_files`–一次迭代中加载的最大项目数（默认为 `100`）
    *   `loader_sleeps`–迭代之间的延迟，以毫秒为单位（默认为 `50`）

在下面的示例中，迭代持续`300` 毫秒或直到`200` 加载项为止：

proxy\_cache\_path  / data / nginx / cache  keys\_zone = one：10m  loader\_threshold = 300  loader\_files = 200 ;

指定要缓存的请求[](#specifying-which-requests-to-cache "固定到该标题")
--------------------------------------------------------

默认情况下，NGINX Plus会缓存对使用HTTP发出的请求的所有响应，`GET`并`HEAD`在首次从代理服务器接收到此类响应时使用方法。NGINX Plus使用请求字符串作为请求的键（标识符）。如果请求具有与缓存的响应相同的密钥，则NGINX Plus会将缓存的响应发送到客户端。您可以在不同的指令，或上下文来控制其响应缓存。`http {}``server {}``location {}`

要更改用于计算密钥的请求特征，请包含以下[`proxy_cache_key`](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_key)指令：

proxy\_cache\_key  “ $ host $ request\_uri $ cookie\_user” ;

要定义在缓存响应之前必须发出具有相同密钥的请求的最小次数，请包含以下[`proxy_cache_min_uses`](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_min_uses)指令：

proxy\_cache\_min\_uses  5 ;

要使用`GET`和以外的方法来缓存对请求的响应`HEAD`，请将它们与`GET`和一起`HEAD`作为[`proxy_cache_methods`](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_methods)指令的参数列出：

proxy\_cache\_methods  GET  HEAD  POST ;

限制或禁用缓存[](#limiting-or-disabling-caching "固定到该标题")
--------------------------------------------------

默认情况下，响应会无限期保留在缓存中。仅当高速缓存超过最大配置大小时才将其删除，然后按自上次请求以来的时间长度顺序进行删除。您可以设置多长时间缓存的响应被认为是有效的，甚至他们是否在所有使用，通过在指示，或上下文：`http {}``server {}``location {}`

要限制具有特定状态码的缓存响应被视为有效的时间，请包含以下[`proxy_cache_valid`](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_valid)指令：

```
proxy_cache_valid 200 302 10m;
proxy_cache_valid 404      1m;
```

在此示例中，带有代码`200`或的响应`302`被认为有效10分钟，带有代码的响应被认为有效`404`1分钟。要定义所有状态代码的响应的有效时间，请指定`any`作为第一个参数：

```
proxy_cache_valid any 5m;
```

要定义NGINX Plus不向客户端发送缓存的响应的条件，请包含[`proxy_cache_bypass`](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_bypass)指令。每个参数定义一个条件，并由许多变量组成。如果至少一个参数不为空且不等于“ 0”（零），则NGINX Plus不会在缓存中查找响应，而是立即将请求转发给后端服务器。

proxy\_cache\_bypass  $ cookie\_nocache  $ arg\_nocache $ arg\_comment ;

要定义条件，NGINX Plus根本不缓存响应，请包含[`proxy_no_cache`](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_no_cache)指令，以与`proxy_cache_bypass`指令相同的方式定义参数。

proxy\_no\_cache  $ http\_pragma  $ http\_authorization ;

从缓存中清除内容[](#purging-content-from-the-cache "固定到该标题")
----------------------------------------------------

NGINX可以从缓存中删除过期的缓存文件。这对于删除过时的缓存内容是必要的，以防止同时提供新旧版本的网页。收到包含自定义HTTP标头或HTTP `PURGE`方法的特殊“清除”请求后，将清除缓存。

### 配置缓存清除[](#configuring-cache-purge "固定到该标题")

让我们设置一个配置，该配置标识使用HTTP `PURGE`方法的请求并删除匹配的URL。

1.  在http {}上下文中，创建一个新变量`$purge_method`，该变量取决于该变量：`$request_method`
    
```
http {
    ...
    map $request_method $purge_method {
        PURGE 1;
        default 0;
    }
}
```
    
2.  在配置缓存的位置location{}块中，包含[`proxy_cache_purge`](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_purge)指令，以指定缓存清除请求的条件.在我们的示例中，它是在上一步中配置的$purge_方法：
3. 在location {}中配置了缓存的块中，包括指令以指定用于缓存清除请求的条件。在我们的示例中，它是上一步中配置的：`location {}`[`proxy_cache_purge`](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_purge)`$purge_method`
    
```
server {
    listen      80;
    server_name www.example.com;

    location / {
        proxy_pass  https://localhost:8002;
        proxy_cache mycache;

        proxy_cache_purge $purge_method;
    }
}
```

### 发送清除命令[](#sending-the-purge-command "固定到该标题")

当`proxy_cache_purge`指令配置，你需要发送一个特殊的缓存清除请求清除缓存。您可以使用多种工具发出清除请求，包括`curl`以下示例中的命令：

```
$ curl -X PURGE -D – "https://www.example.com/*"
HTTP/1.1 204 No Content
Server: nginx/1.15.0
Date: Sat, 19 May 2018 16:33:04 GMT
Connection: keep-alive
```

在该示例中，将清除具有公共URL部分（由星号通配符指定）的资源。但是，此类高速缓存条目不会完全从高速缓存中删除：它们保留在磁盘上，直到因不活动（由指令的`inactive`参数确定[`proxy_cache_path`](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_path)）或由高速缓存清除程序（将[`purger`](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#purger)参数启用为`proxy_cache_path`）或客户端而被删除为止。尝试访问它们。

### 限制对清除命令的访问[](#restricting-access-to-the-purge-command "固定到该标题")

我们建议您限制允许发送缓存清除请求的IP地址数量：

```
geo $purge_allowed {
   default         0;  # deny from other
   10.0.0.1        1;  # allow from localhost
   192.168.0.0/24  1;  # allow from 10.0.0.0/24
}

map $request_method $purge_method {
   PURGE   $purge_allowed;
   default 0;
}
```

在此示例中，NGINX检查`PURGE`请求中是否使用了该方法，如果有，则分析客户端IP地址。如果IP地址已列入白名单，则将`$purge_method`设置为`$purge_allowed`：`1`允许清除，并`0`拒绝它。

### 从缓存中完全删除文件[](#completely-removing-files-from-the-cache "固定到该标题")

要完全删除与星号匹配的缓存文件，请激活一个特殊的cache purger进程，该进程将永久迭代所有缓存项并删除与通配符键匹配的项。将[`purger`](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#purger)参数包含到http{}上下文中的[`proxy_cache_path`](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_path)指令中：

```
proxy_cache_path /data/nginx/cache levels=1:2 keys_zone=mycache:10m purger=on;
```

### 缓存清除配置示例[](#cache-purge-configuration-example "固定到该标题")

```
http {
    ...
    proxy_cache_path /data/nginx/cache levels=1:2 keys_zone=mycache:10m purger=on;

    map $request_method $purge_method {
        PURGE 1;
        default 0;
    }

    server {
        listen      80;
        server_name www.example.com;

        location / {
            proxy_pass        https://localhost:8002;
            proxy_cache       mycache;
            proxy_cache_purge $purge_method;
        }
    }

    geo $purge_allowed {
       default         0;
       10.0.0.1        1;
       192.168.0.0/24  1;
    }

    map $request_method $purge_method {
       PURGE   $purge_allowed;
       default 0;
    }
}
```

字节范围缓存[](#byte-range-caching "固定到该标题")
--------------------------------------

初始高速缓存填充操作有时会花费很长时间，尤其是对于大文件。例如，当视频文件开始下载以满足部分文件的初始请求时，后续请求必须等待整个文件被下载并放入缓存中。

NGINX可以缓存此类范围请求，并使用“ [缓存切片”](https://nginx.org/en/docs/http/ngx_http_slice_module.html)模块逐渐填充缓存，该模块将文件分成较小的“切片”。每个范围请求都选择覆盖所请求范围的特定切片，如果仍未缓存该范围，则将其放入缓存。这些切片的所有其他请求都从缓存中获取数据。

要启用字节范围缓存：

1.  确保NGINX是使用“ [缓存切片”](https://nginx.org/en/docs/http/ngx_http_slice_module.html)模块编译的。
    
2.  使用[`slice`](https://nginx.org/en/docs/http/ngx_http_slice_module.html#slice)指令指定切片的大小：
    
```
location / {
    slice  1m;
}
```
    

选择切片大小以使切片下载速度更快。如果大小太小，则内存使用可能会过多，并且在处理请求时会打开大量文件描述符，而太大的大小可能会导致延迟。

1.  将[`$slice_range`](https://nginx.org/en/docs/http/ngx_http_slice_module.html#var_slice_range)变量包括到缓存键中：
    
    proxy\_cache\_key  $ uri $ is\_args $ args $ slice\_range ;
    
2.  使用`206`状态码启用响应缓存：
    
    proxy\_cache\_valid  200  206  1H ;
    
3.  通过[`$slice_range`](https://nginx.org/en/docs/http/ngx_http_slice_module.html#var_slice_range)在`Range`标头字段中设置变量，可以将范围请求传递到代理服务器：
    
```
proxy_set_header  Range $slice_range;
```

这是完整的配置：

```
location / {
    slice             1m;
    proxy_cache       cache;
    proxy_cache_key   $uri$is_args$args$slice_range;
    proxy_set_header  Range $slice_range;
    proxy_cache_valid 200 206 1h;
    proxy_pass        http://localhost:8000;
}
```

请注意，如果启用了切片缓存，则不得更改初始文件。

组合配置示例[](#combined-configuration-example "固定到该标题")
--------------------------------------------------

下面的示例配置结合了上述某些缓存选项。

```
http {
    ...
    proxy_cache_path /data/nginx/cache keys_zone=one:10m loader_threshold=300 
                     loader_files=200 max_size=200m;

    server {
        listen 8080;
        proxy_cache mycache;

        location / {
            proxy_pass http://backend1;
        }

        location /some/path {
            proxy_pass http://backend2;
            proxy_cache_valid any 1m;
            proxy_cache_min_uses 3;
            proxy_cache_bypass $cookie_nocache $arg_nocache$arg_comment;
        }
    }
}
```
在此示例中，两个位置使用相同的缓存，但方式不同。

由于响应`backend1`很少改变，因此不包括缓存控制指令。响应在第一次发出请求时被缓存，并无限期保持有效。

相反，对请求的响应`backend2`通常由更改来服务，因此它们被认为仅有效1分钟，并且直到发出相同请求3次才被缓存。此外，如果请求符合`proxy_cache_bypass`指令定义的条件，则NGINX Plus会立即将请求传递给，`backend2`而无需在缓存中查找相应的响应。