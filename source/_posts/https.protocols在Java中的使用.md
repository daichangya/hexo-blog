---
title: https.protocols在Java中的使用
id: 1530
date: 2024-10-31 22:02:00
author: daichangya
permalink: /archives/httpsprotocols%E5%9C%A8java%E4%B8%AD%E7%9A%84%E4%BD%BF%E7%94%A8/
categories:
 - java
---


## Contents

*   [Caused by: java.io.EOFException: SSL peer shut down incorrectly](#caused-by-java-io-eofexception-ssl-peer-shut-down-incorrectly)
*   [HTTPS 的 protocols](#https-的-protocols)
    *   [TLS 与 SSL](#tls-与-ssl)
*   [发展历史](#发展历史)
    *   [SSL](#ssl)
    *   [TLS](#tls)
*   [JDK中对 HTTPS 版本的支持情况](#jdk中对-https-版本的支持情况)
    *   [JDK 6](#jdk-6)
    *   [JDK 7](#jdk-7)
    *   [JDK 8](#jdk-8)
*   [JSSE](#jsse)
    *   [JSSE 参数调节](#jsse-参数调节)
*   [查看服务器支持的 HTTPS 协议版本](#查看服务器支持的-https-协议版本)
*   [解决办法](#解决办法)
*   [参考资料](#参考资料)

# [](#caused-by-java-io-eofexception-ssl-peer-shut-down-incorrectly)Caused by: java.io.EOFException: SSL peer shut down incorrectly

在服务器上，发现一个微博爬虫系统偶尔会报这种异常。Google 了下，在 [Stackoverflow](http://stackoverflow.com/questions/28908835/ssl-peer-shut-down-incorrectly-in-java) 上看到相关的回答。所以决定详细了解下这原理。

上面说，明确指定HTTPS的协议版本即可。即：`System.setProperty("https.protocols", "TLSv1.1")`

# [](#https-的-protocols)HTTPS 的 protocols

查看维基百科，关于 HTTPS 的介绍可知：

> 严格地讲，HTTPS并不是一个单独的协议，而是对工作在一加密连接（TLS或SSL）上的常规HTTP协议的称呼。

## [](#tls-与-ssl)TLS 与 SSL

*SSL* 是 *TLS* 的前身。*SSL* 是 *Netscape* 公司推出的 *HTTPS* 协议，以 *SSL* 进行加密。

*IETF* 将 *SSL* 进行标准化，公布了第一版的 *TLS* 标准文件。

# [](#发展历史)发展历史

## [](#ssl)SSL

*   1.0 没有公开过
*   2.0 1995年2月发布
*   3.0 1996年发布。2014年10月，Google 发现 SSL 3.0 设计缺陷，建议禁用此一协议。

## [](#tls)TLS

*IETF* 将SSL标准化，并称为 *TLS*. *TLS1.0* 与 *SSL 3.0* 的差异非常小。

*   1.0
*   1.1 2006
*   1.2 2008
*   1.3 2016

# [](#jdk中对-https-版本的支持情况)JDK中对 HTTPS 版本的支持情况

## [](#jdk-6)JDK 6

*   SSL v3
*   TLS v1(默认)
*   TLS v1.1(JDK6 update 111 及以上)

## [](#jdk-7)JDK 7

*   SSLv3
*   TLS v1(默认)
*   TLS v1.1
*   TLS v1.2

## [](#jdk-8)JDK 8

*   SSL v3
*   TLS v1
*   TLS v1.1
*   TLS v1.2(默认)

# [](#jsse)JSSE

JSSE（Java Security Socket Extension），它实现了SSL和TSL（传输层安全）协议。

## [](#jsse-参数调节)JSSE 参数调节

*   `javax.net.debug` ：打印连接的详细信息。例如 `-Djavax.net.debug=all` 或者 `-Djavax.net.debug=ssl🤝verbose`
*   `https.protocols` ：控制使用 Java 客户端通过 `HttpsURLConnection` 或 `URL.openStream()` 操作的协议版本。例如 `-Dhttps.protocols=TLSv1,TLSv1.1,TLSv1.2`. 对于非HTTP协议，可以通过 `SocketFactory's SSLContext` 来控制 。
*   `jdk.tls.client.protocols` ：控制底层平台的TLS实现。例如 `-Djdk.tls.client.protocols=TLSv1.1,TLSv1.2`
*   `http.agent` ：当初始化连接时，Java会使用这个作为 `user-agent` 的字符串。例如: `-Dhttp.agent="known agent"`
*   `java.net.useSystemProxies` ：使用系统本身的代理： `-Djava.net.useSystemProxies=true`
*   `http.proxyHost` 和 `http.proxyPort` : 使用HTTP协议时的代理。例如: `-Dhttp.proxyHost=proxy.example.com -Dhttp.proxyPort=8080`
*   `https.proxyHost` 和 `https.proxyPort` : 和上面一样，区别只是 HTTP 和 HTTPS
*   `http.proxyUser`,`http.proxyPassword`, `https.proxyUser`,`https.proxyPassword` : 认证用户名和密码。

# [](#查看服务器支持的-https-协议版本)查看服务器支持的 HTTPS 协议版本

```
nmap --script ssl-enum-ciphers -p 443 api.weibo.com
```

返回的结果为:

```

Starting Nmap 7.40 ( https://nmap.org ) at 2017-03-02 14:18 CST
Nmap scan report for api.weibo.com (180.149.135.176)
Host is up (0.039s latency).
Other addresses for api.weibo.com (not scanned): 180.149.135.230
PORT    STATE SERVICE
443/tcp open  https
| ssl-enum-ciphers:
|   SSLv3:
|     ciphers:
|       TLS_RSA_WITH_AES_256_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_CAMELLIA_256_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_AES_128_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_SEED_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_CAMELLIA_128_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_IDEA_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_RC4_128_SHA (rsa 2048) - C
|       TLS_RSA_WITH_3DES_EDE_CBC_SHA (rsa 2048) - C
|       TLS_RSA_WITH_DES_CBC_SHA (rsa 2048) - C
|       TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA (secp256r1) - A
|       TLS_DHE_RSA_WITH_AES_256_CBC_SHA (dh 1024) - A
|       TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA (dh 1024) - A
|       TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA (secp256r1) - A
|       TLS_DHE_RSA_WITH_AES_128_CBC_SHA (dh 1024) - A
|       TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA (dh 1024) - A
|       TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA (secp256r1) - C
|       TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA (dh 1024) - D
|     compressors:
|       NULL
|     cipher preference: server
|     warnings:
|       64-bit block cipher 3DES vulnerable to SWEET32 attack
|       64-bit block cipher DES vulnerable to SWEET32 attack
|       64-bit block cipher IDEA vulnerable to SWEET32 attack
|       Broken cipher RC4 is deprecated by RFC 7465
|       CBC-mode cipher in SSLv3 (CVE-2014-3566)
|       Key exchange (dh 1024) of lower strength than certificate key
|   TLSv1.0:
|     ciphers:
|       TLS_RSA_WITH_AES_256_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_CAMELLIA_256_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_AES_128_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_SEED_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_CAMELLIA_128_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_IDEA_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_RC4_128_SHA (rsa 2048) - C
|       TLS_RSA_WITH_3DES_EDE_CBC_SHA (rsa 2048) - C
|       TLS_RSA_WITH_DES_CBC_SHA (rsa 2048) - C
|       TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA (secp256r1) - A
|       TLS_DHE_RSA_WITH_AES_256_CBC_SHA (dh 1024) - A
|       TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA (dh 1024) - A
|       TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA (secp256r1) - A
|       TLS_DHE_RSA_WITH_AES_128_CBC_SHA (dh 1024) - A
|       TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA (dh 1024) - A
|       TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA (secp256r1) - C
|       TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA (dh 1024) - D
|     compressors:
|       NULL
|     cipher preference: server
|     warnings:
|       64-bit block cipher 3DES vulnerable to SWEET32 attack
|       64-bit block cipher DES vulnerable to SWEET32 attack
|       64-bit block cipher IDEA vulnerable to SWEET32 attack
|       Broken cipher RC4 is deprecated by RFC 7465
|       Key exchange (dh 1024) of lower strength than certificate key
|   TLSv1.1:
|     ciphers:
|       TLS_RSA_WITH_AES_256_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_CAMELLIA_256_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_AES_128_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_SEED_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_CAMELLIA_128_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_IDEA_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_RC4_128_SHA (rsa 2048) - C
|       TLS_RSA_WITH_3DES_EDE_CBC_SHA (rsa 2048) - C
|       TLS_RSA_WITH_DES_CBC_SHA (rsa 2048) - C
|       TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA (secp256r1) - A
|       TLS_DHE_RSA_WITH_AES_256_CBC_SHA (dh 1024) - A
|       TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA (dh 1024) - A
|       TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA (secp256r1) - A
|       TLS_DHE_RSA_WITH_AES_128_CBC_SHA (dh 1024) - A
|       TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA (dh 1024) - A
|       TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA (secp256r1) - C
|       TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA (dh 1024) - D
|     compressors:
|       NULL
|     cipher preference: server
|     warnings:
|       64-bit block cipher 3DES vulnerable to SWEET32 attack
|       64-bit block cipher DES vulnerable to SWEET32 attack
|       64-bit block cipher IDEA vulnerable to SWEET32 attack
|       Broken cipher RC4 is deprecated by RFC 7465
|       Key exchange (dh 1024) of lower strength than certificate key
|   TLSv1.2:
|     ciphers:
|       TLS_RSA_WITH_AES_256_GCM_SHA384 (rsa 2048) - A
|       TLS_RSA_WITH_AES_256_CBC_SHA256 (rsa 2048) - A
|       TLS_RSA_WITH_AES_256_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_CAMELLIA_256_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_AES_128_GCM_SHA256 (rsa 2048) - A
|       TLS_RSA_WITH_AES_128_CBC_SHA256 (rsa 2048) - A
|       TLS_RSA_WITH_AES_128_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_SEED_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_CAMELLIA_128_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_IDEA_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_RC4_128_SHA (rsa 2048) - C
|       TLS_RSA_WITH_3DES_EDE_CBC_SHA (rsa 2048) - C
|       TLS_RSA_WITH_DES_CBC_SHA (rsa 2048) - C
|       TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA (secp256r1) - A
|       TLS_DHE_RSA_WITH_AES_256_GCM_SHA384 (dh 1024) - A
|       TLS_DHE_RSA_WITH_AES_256_CBC_SHA256 (dh 1024) - A
|       TLS_DHE_RSA_WITH_AES_256_CBC_SHA (dh 1024) - A
|       TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA (dh 1024) - A
|       TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA (secp256r1) - A
|       TLS_DHE_RSA_WITH_AES_128_GCM_SHA256 (dh 1024) - A
|       TLS_DHE_RSA_WITH_AES_128_CBC_SHA256 (dh 1024) - A
|       TLS_DHE_RSA_WITH_AES_128_CBC_SHA (dh 1024) - A
|       TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA (dh 1024) - A
|       TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA (secp256r1) - C
|       TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA (dh 1024) - D
|     compressors:
|       NULL
|     cipher preference: server
|     warnings:
|       64-bit block cipher 3DES vulnerable to SWEET32 attack
|       64-bit block cipher DES vulnerable to SWEET32 attack
|       64-bit block cipher IDEA vulnerable to SWEET32 attack
|       Broken cipher RC4 is deprecated by RFC 7465
|       Key exchange (dh 1024) of lower strength than certificate key
|_  least strength: D
Nmap done: 1 IP address (1 host up) scanned in 10.99 seconds

```

可知，它支持的协议有:

*   SSLv3
*   TLSv1.0
*   TLSv1.1
*   TLSv1.2

# [](#解决办法)解决办法

服务器为Linux + JDK7 + 64位。添加

```
System.setProperty("https.protocols", "TLSv1.2");
```

在爬虫爬取数据时，就没有报这类似的异常了。

# [](#参考资料)参考资料

*   [Oracle 上关于 https.protocols 的文档](https://blogs.oracle.com/java-platform-group/entry/diagnosing_tls_ssl_and_https)
    
*   [wiki](https://zh.wikipedia.org/wiki/%E5%82%B3%E8%BC%B8%E5%B1%A4%E5%AE%89%E5%85%A8%E5%8D%94%E8%AD%B0)
    
