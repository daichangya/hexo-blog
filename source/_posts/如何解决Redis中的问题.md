---
title: 如何解决Redis中的问题
id: 1349
date: 2024-10-31 22:01:51
author: daichangya
excerpt: "介绍Redis是一个开源的内存中键值数据存储。它带有几个命令，可以帮助您进行故障排除和调试。由于Redis具有内存中的键值存储的性质，因此其中许多命令都集中在内存管理上，但是还有一些其他命令对于概述Redis服务器的状态很有用。本教程将提供有关如何使用其中一些命令来帮助诊断和解决使用Redis时可能"
permalink: /archives/%E5%A6%82%E4%BD%95%E8%A7%A3%E5%86%B3redis%E4%B8%AD%E7%9A%84%E9%97%AE%E9%A2%98/
categories:
 - redis
---

1. [如何在ubuntu18.04上安装和保护redis](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis)
2. [如何连接到Redis数据库](https://blog.jsdiff.com/archives/howtoconnecttoaredisdatabase)
3. [如何管理Redis数据库和Keys](https://blog.jsdiff.com/archives/howtomanageredisdatabasesandkeys)
4. [如何在Redis中管理副本和客户端](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8redis%E4%B8%AD%E7%AE%A1%E7%90%86%E5%89%AF%E6%9C%AC%E5%92%8C%E5%AE%A2%E6%88%B7%E7%AB%AF)
5. [如何在Redis中管理字符串](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8redis%E4%B8%AD%E7%AE%A1%E7%90%86%E5%AD%97%E7%AC%A6%E4%B8%B2)
6. [如何在Redis中管理list](https://blog.jsdiff.com/archives/listsinredis)
7. [如何在Redis中管理Hashes](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8redis%E4%B8%AD%E7%AE%A1%E7%90%86hashes)
8. [如何在Redis中管理Sets](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8redis%E4%B8%AD%E7%AE%A1%E7%90%86sets)
9. [如何在Redis中管理Sorted Sets](https://blog.jsdiff.com/archives/howtomanagesortedsetsinredis)
10. [如何在Redis中运行事务](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8redis%E4%B8%AD%E8%BF%90%E8%A1%8C%E4%BA%8B%E5%8A%A1)
11. [如何使Redis中的Key失效](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E4%BD%BFredis%E4%B8%AD%E7%9A%84keys%E5%A4%B1%E6%95%88)
12. [如何解决Redis中的故障](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E8%A7%A3%E5%86%B3redis%E4%B8%AD%E7%9A%84%E9%97%AE%E9%A2%98)
13. [如何从命令行更改Redis的配置](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E4%BB%8E%E5%91%BD%E4%BB%A4%E8%A1%8C%E6%9B%B4%E6%94%B9redis%E7%9A%84%E9%85%8D%E7%BD%AE)
14. [Redis数据类型简介](https://blog.jsdiff.com/archives/redis%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B%E7%AE%80%E4%BB%8B)
 

### 介绍

[Redis](https://redis.io/)是一个开源的内存中键值数据存储。它带有几个命令，可以帮助您进行故障排除和调试。由于Redis具有[内存中的键值存储](https://en.wikipedia.org/wiki/In-memory_database)的性质，因此其中许多命令都集中在内存管理上，但是还有一些其他命令对于概述Redis服务器的状态很有用。本教程将提供有关如何使用其中一些命令来帮助诊断和解决使用Redis时可能遇到的问题的详细信息。

#### 如何使用本指南

本指南以备有完整示例的备忘单形式编写。我们鼓励您跳至与您要完成的任务相关的任何部分。

本指南中显示的命令已在运行Redis版本4.0.9的Ubuntu 18.04服务器上进行了测试。要设置类似的环境，您可以按照我们的指南[如何在Ubuntu 18.04上安装和保护Redis的](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis)**步骤1**进行操作。我们将通过使用Redis命令行界面运行它们来演示这些命令的行为。请注意，如果您使用其他Redis界面（例如[Redli）](https://github.com/IBM-Cloud/redli)，则某些命令的确切输出可能会有所不同。[](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis)`redis-cli`[](https://github.com/IBM-Cloud/redli)

另外，您可以提供一个托管的Redis数据库实例来测试这些命令，但是请注意，根据数据库提供者所允许的控制级别，本指南中的某些命令可能无法按所述方式工作。要配置DigitalOcean托管数据库，请遵循我们的[托管数据库产品文档](https://www.digitalocean.com/docs/databases/redis/quickstart/)。然后，**您必须** [**安装Redli**](https://www.digitalocean.com/community/tutorials/how-to-connect-to-managed-database-ubuntu-18-04#connecting-to-a-managed-redis-database) **或** [**设置TLS隧道**](https://www.digitalocean.com/community/tutorials/how-to-connect-to-managed-redis-over-tls-with-stunnel-and-redis-cli)才能通过TLS连接到托管数据库。

对内存相关问题进行故障排除
-------------

`memory usage`告诉您单个键当前正在使用多少内存。它以键的名称作为参数，并输出其使用的字节数：

    memory usage key_meaningOfLife
    

    (integer) 42
    

为了更全面地了解您的Redis服务器如何使用内存，可以运行以下`memory stats`命令：

    memory stats
    

此命令输出与内存相关的指标及其值的数组。以下是报告的指标`memory stats`：

*   `peak.allocated`：Redis消耗的最大字节数
*   `total.allocated`：Redis分配的总字节数
*   `startup.allocated`：Redis在启动时消耗的初始字节数
*   `replication.backlog`：复制积压的大小，以字节为单位
*   `clients.slaves`：所有副本_开销_的总大小（输出和查询缓冲区以及连接上下文）
*   `clients.normal`：所有客户端开销的总大小
*   `aof.buffer`：当前和重写[的仅附加文件](https://en.wikipedia.org/wiki/Redis#Persistence)缓冲区的总大小
*   `db.0`：服务器上正在使用的每个数据库的主要和到期字典的开销，以字节为单位报告
*   `overhead.total`：用于管理Redis密钥空间的所有开销的总和
*   `keys.count`：服务器上所有数据库中存储的密钥总数
*   `keys.bytes-per-key`：服务器的净内存使用率与 `keys.count`
*   `dataset.bytes`：数据集的大小，以字节为单位
*   `dataset.percentage`：Redis占用的Redis净内存使用量的百分比 `dataset.bytes`
*   `peak.percentage`：`peak.allocated`取出的百分比`total.allocated`
*   `fragmentation`：当前正在使用的内存量除以Redis实际使用的物理内存之比

`memory malloc-stats`提供了来自[jemalloc](http://jemalloc.net/)的内部统计报告，该报告是Linux系统上Redis使用的内存分配器：

    memory malloc-stats
    

如果您似乎遇到了与内存有关的问题，但是解析前面命令的输出证明是无济于事的，则可以尝试运行`memory doctor`：

    memory doctor
    

此功能将输出它可以找到的所有内存消耗问题，并提出潜在的解决方案。

获取有关Redis实例的常规信息
----------------

与内存管理没有直接关系的调试命令是`monitor`。此命令使您可以查看Redis服务器处理的每个命令的恒定流：

    monitor
    

    OK
    1566157213.896437 [0 127.0.0.1:47740] "auth" "foobared"
    1566157215.870306 [0 127.0.0.1:47740] "set" "key_1" "878"
    

另一个对调试有用的命令是`info`，它返回有关服务器的多个信息和统计信息块：

    info
    

    # Server
    redis_version:4.0.9
    redis_git_sha1:00000000
    redis_git_dirty:0
    redis_build_id:9435c3c2879311f3
    redis_mode:standalone
    os:Linux 4.15.0-52-generic x86_64
    . . .
    

此命令返回很多信息。如果您只想查看一个信息块，则可以将其指定为`info`：

    info CPU
    

    # CPU
    used_cpu_sys:173.16
    used_cpu_user:70.89
    used_cpu_sys_children:0.01
    used_cpu_user_children:0.04
    

请注意，该`info`命令返回的信息将取决于您所使用的Redis版本。

使用`keys`命令
----------

`keys`如果您忘记了某个键的名称，或者您已经创建了一个键，但又意外误拼了它的名称，则该命令很有用。`keys`查找与模式匹配的键：

    keys pattern
    

支持以下glob样式的变量

*   `?`是通配符站在任何单个字符，这样`s?mmy`的比赛`sammy`，`sommy`和`sqmmy`
*   `*`是一个通配符，用来代表任何数量的字符，包括没有任何字符，所以`sa*y`比赛`sammy`，`say`，`sammmmmmy`，和`salmony`
*   您可以通过将模式将其括在方括号中来指定模式可以包含的两个或多个字符，以`s[ai]mmy`匹配`sammy`和`simmy`，但不能匹配`summy`
*   要设置一个忽略一个或多个字母的通配符，请将其括在方括号中，并在其前面加上一个胡萝卜（`^`），这样`s[^oi]mmy`可以匹配`sammy`和`sxmmy`，但不能匹配`sommy`或`simmy`
*   要设置一个通配符，其中包括一系列的字母，范围的开头和结尾分开连字符和括号包起来，这样`s[a-o]mmy`将匹配`sammy`，`skmmy`和`sommy`，但不`srmmy`

**警告：**本[Redis的文件](https://redis.io/commands/keys)警告说，`keys`应该几乎从来没有在生产环境中使用，因为它可能会对性能产生重大的负面影响。  

结论
--

本指南详细介绍了许多命令，这些命令可用于故障排除和解决与Redis一起使用时可能遇到的问题。如果您想在本指南中概述其他相关的命令，参数或过程，请在下面的评论中提出疑问或提出建议。

有关Redis命令的更多信息，请参阅关于[如何管理Redis数据库的](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8redis%E6%95%B0%E6%8D%AE%E5%BA%93)系列教程。