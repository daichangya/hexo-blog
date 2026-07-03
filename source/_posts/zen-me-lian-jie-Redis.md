---
title: 怎么链接Redis
id: 1337
date: 2024-10-31 22:01:51
author: daichangya
excerpt: 介绍Redis是一个开源的内存中键值数据存储。无论您是在本地安装Redis还是在使用远程实例，都需要连接到该实例才能执行大多数操作。在本教程中，我们将介绍如何从命令行连接到Redis，如何验证和测试您的连接以及如何关闭Redis连接。如何使用本指南本指南以备有完整示例的备忘单形式编写。我们鼓励您跳至
permalink: /archives/zen-me-lian-jie-Redis/
categories:
- redis
tags:
- redis基础教程
---

1. [如何在ubuntu18.04上安装和保护redis](https://www.tushu.info/archives/ru-he-zai-Ubuntu-18-04-shang-an-zhuang)
2. [如何连接到Redis数据库](https://www.tushu.info/archives/zen-me-lian-jie-Redis)
3. [如何管理Redis数据库和Keys](https://www.tushu.info/archives/ru-he-guan-li-Redis-shu-ju-ku-he-Keys)
4. [如何在Redis中管理副本和客户端](https://www.tushu.info/archives/ru-he-zai-Redis-zhong-guan-li-fu-ben-he)
5. [如何在Redis中管理字符串](https://www.tushu.info/archives/ru-he-zai-Redis-zhong-guan-li-zi-fu)
6. [如何在Redis中管理list](https://www.tushu.info/archives/zai-Redis-zhong-zen-me-shi-yong-Lists)
7. [如何在Redis中管理Hashes](https://www.tushu.info/archives/ru-he-zai-Redis-zhong-guan-li-Hashes)
8. [如何在Redis中管理Sets](https://www.tushu.info/archives/ru-he-zai-Redis-zhong-guan-li-Sets)
9. [如何在Redis中管理Sorted Sets](https://www.tushu.info/archives/zai-Redis-zhong-zen-me-shi-yong-Sorted)
10. [如何在Redis中运行事务](https://www.tushu.info/archives/ru-he-zai-Redis-zhong-yun-xing-shi-wu)
11. [如何使Redis中的Key失效](https://www.tushu.info/archives/ru-he-shi-Redis-zhong-de-Keys-shi-xiao)
12. [如何解决Redis中的故障](https://www.tushu.info/archives/ru-he-jie-jue-Redis-zhong-de-wen-ti)
13. [如何从命令行更改Redis的配置](https://www.tushu.info/archives/ru-he-cong-ming-ling-xing-geng-gai)
14. [Redis数据类型简介](https://www.tushu.info/archives/Redis-shu-ju-lei-xing-jian-jie)

### 介绍

[Redis](https://redis.io/)是一个开源的内存中键值数据存储。无论您是在本地安装Redis还是在使用远程实例，都需要连接到该实例才能执行大多数操作。在本教程中，我们将介绍如何从命令行连接到Redis，如何验证和测试您的连接以及如何关闭Redis连接。

#### 如何使用本指南

本指南以备有完整示例的备忘单形式编写。我们鼓励您跳至与您要完成的任务相关的任何部分。

本指南中显示的命令已在运行Redis版本4.0.9的Ubuntu 18.04服务器上进行了测试。要设置类似的环境，您可以按照我们的指南[如何在Ubuntu 18.04上安装和保护Redis的](https://www.tushu.info/archives/ru-he-zai-Ubuntu-18-04-shang-an-zhuang)**步骤1**进行操作。我们将通过使用Redis命令行界面运行它们来演示这些命令的行为。请注意，如果您使用其他Redis界面（例如[Redli）](https://github.com/IBM-Cloud/redli)，则某些命令的确切输出可能会有所不同。[](https://www.tushu.info/archives/ru-he-zai-Ubuntu-18-04-shang-an-zhuang)`redis-cli`[](https://github.com/IBM-Cloud/redli)

另外，您可以提供一个托管的Redis数据库实例来测试这些命令，但是请注意，根据数据库提供者所允许的控制级别，本指南中的某些命令可能无法按所述方式工作。要配置DigitalOcean托管数据库，请遵循我们的[托管数据库产品文档](https://www.digitalocean.com/docs/databases/redis/quickstart/)。然后，**您必须** [**安装Redli**](https://www.digitalocean.com/community/tutorials/how-to-connect-to-managed-database-ubuntu-18-04#connecting-to-a-managed-redis-database) **或** [**设置TLS隧道**](https://www.digitalocean.com/community/tutorials/how-to-connect-to-managed-redis-over-tls-with-stunnel-and-redis-cli)才能通过TLS连接到托管数据库。

连接到Redis
--------

如果已`redis-server` **在本地安装**，则可以使用以下`redis-cli`命令连接到Redis实例：

    redis-cli
    

这将带您进入`redis-cli`的_交互模式_，该_模式_为您提供一个[_read-eval-print循环_](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop)（REPL），您可以在其中运行Redis的内置命令并接收答复。

在交互模式下，命令行提示符将更改以反映您的连接。在本示例以及本指南中的其他示例中，提示指示与本地托管的Redis实例的连接（`127.0.0.1`），并通过Redis的默认端口（`6379`）进行访问：

在交互模式下运行Redis命令的替代方法是将它们作为`redis-cli`命令的参数运行，如下所示：

    redis-cli redis_command
    

如果要连接到**远程** Redis数据存储，可以分别使用`-h`和`-p`标志指定其主机和端口号。另外，如果您已将Redis数据库配置为要求输入密码，则可以在`-a`其后加上该标志并进行身份验证：

    redis-cli -h host -p port_number -a password
    

如果您设置了Redis密码，则即使客户端未`-a`在`redis-cli`命令中包含该标志，客户端也可以连接到Redis 。但是，他们只有在通过身份验证后才能添加，更改或查询数据。要在连接后进行身份验证，请使用`auth`命令后跟密码：

    auth password
    

如果传递给的密码`auth`有效，则命令将返回`OK`。否则，它将返回错误。

如果您正在使用托管Redis数据库，则云提供商可能会给您提供一个以URI开头`redis://`或`rediss://`可用于访问数据存储的URI 。如果连接字符串以开头`redis://`，则可以将其作为`redis-cli`连接参数。

但是，如果您有一个以开头的连接字符串，则`rediss://`意味着您的托管数据库需要通过[TLS / SSL进行](https://en.wikipedia.org/wiki/Transport_Layer_Security)连接。`redis-cli`不支持TLS连接，因此您需要使用支持`rediss`协议的其他工具才能与URI连接。对于需要通过TLS建立连接的DigitalOcean托管数据库，我们建议使用[Redli](https://github.com/IBM-Cloud/redli)访问Redis实例。

使用以下语法通过Redli连接到数据库。请注意，此示例包括`--tls`选项（该选项指定应通过TLS建立连接）和`-u`标志（该标志声明以下参数将是连接URI）：

    redli --tls -u rediss://connection_URI
    

我尝试连接到不可用的实例，`redis-cli`将进入_断开连接模式_。提示将反映以下内容：

每次在断开连接状态下运行命令时，Redis都会尝试重新建立连接。

测试连接
----

该`ping`命令对于测试与数据库的连接是否有效很有用。请注意，这是Redis特定的命令，与[`ping`网络实用程序](https://en.wikipedia.org/wiki/Ping_(networking_utility))不同。但是，两者共享相似的功能，因为它们都用于检查两台计算机之间的连接。

如果连接建立并且不包含任何参数，则`ping`命令将返回`PONG`：

    ping
    

    PONG
    

如果为`ping`命令提供参数，它将返回该参数，而不是`PONG`连接成功：

    ping "hello Redis!"
    

    "hello Redis!"
    

如果`ping`以断开连接的方式运行或其他任何命令，您将看到类似以下的输出：

    ping
    

    Could not connect to Redis at host:port: Connection refused
    

注意，`ping`Redis在内部也使用它[来测量延迟](https://www.digitalocean.com/community/tutorials/how-to-perform-redis-benchmark-tests#checking-latency-with-redis-cli)。

与Redis断开连接
----------

要与Redis实例断开连接，请使用以下`quit`命令：

    quit
    

运行`exit`也会退出连接：

    exit
    

两者`quit`和`exit`都会关闭连接，但是只有在所有未决答复都已写到客户端后，才可以。

结论
--

本指南详细介绍了用于建立，测试和关闭与Redis服务器的连接的许多命令。如果您想在本指南中看到其他相关的命令，参数或过程，请在下面的评论中提出疑问或提出建议。

有关Redis命令的更多信息，请参阅关于[如何管理Redis数据库的](https://www.tushu.info/archives/ru-he-shi-yong-Redis-shu-ju-ku)系列教程。