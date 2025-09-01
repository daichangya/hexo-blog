---
title: 如何使Redis中的Keys失效
id: 1348
date: 2024-10-31 22:01:51
author: daichangya
excerpt: "介绍Redis是一个开源的内存中键值数据存储。默认情况下，Redis密钥是_永久性_的，这意味着Redis服务器将继续存储它们，除非手动将其删除。但是，在某些情况下，您已经设置了密钥，但是您知道要在经过一定时间后才将其删除。换句话说，您希望密钥是_可变的_。本教程说明了如何设置密钥的过期时间，如何检"
permalink: /archives/%E5%A6%82%E4%BD%95%E4%BD%BFredis%E4%B8%AD%E7%9A%84keys%E5%A4%B1%E6%95%88/
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

[Redis](https://redis.io/)是一个开源的内存中键值数据存储。默认情况下，Redis密钥是_永久性_的，这意味着Redis服务器将继续存储它们，除非手动将其删除。但是，在某些情况下，您已经设置了密钥，但是您知道要在经过一定时间后才将其删除。换句话说，您希望密钥是_可变的_。本教程说明了如何设置密钥的过期时间，如何检查直到密钥过期的剩余时间以及取消密钥的过期设置。

#### 如何使用本指南

本指南以备有完整示例的备忘单形式编写。我们鼓励您跳至与您要完成的任务相关的任何部分。

本指南中显示的命令已在运行Redis版本4.0.9的Ubuntu 18.04服务器上进行了测试。要设置类似的环境，您可以按照我们的指南[如何在Ubuntu 18.04上安装和保护Redis的](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis)**步骤1**进行操作。我们将通过使用Redis命令行界面运行它们来演示这些命令的行为。请注意，如果您使用其他Redis界面（例如[Redli）](https://github.com/IBM-Cloud/redli)，则某些命令的确切输出可能会有所不同。 [](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis)`redis-cli`[](https://github.com/IBM-Cloud/redli)

另外，您可以提供一个托管的Redis数据库实例来测试这些命令，但是请注意，根据数据库提供者所允许的控制级别，本指南中的某些命令可能无法按所述方式工作。要配置DigitalOcean托管数据库，请遵循我们的[托管数据库产品文档](https://www.digitalocean.com/docs/databases/redis/quickstart/)。然后，**您必须** [**安装Redli**](https://www.digitalocean.com/community/tutorials/how-to-connect-to-managed-database-ubuntu-18-04#connecting-to-a-managed-redis-database) **或** [**设置TLS隧道**](https://www.digitalocean.com/community/tutorials/how-to-connect-to-managed-redis-over-tls-with-stunnel-and-redis-cli)才能通过TLS连接到托管数据库。

Setting Keys to Expire
----------------------

您可以使用`expire`命令设置现有密钥的过期时间，该命令将密钥名称和直到过期的秒数作为参数。为了证明这一点，请运行以下两个命令。第一创建名为字符串键`key_melon`具有值`"cantaloupe"`，而第二组它到450秒之后超时：

    set key_melon "cantaloupe"
    expire key_melon 450
    

如果成功设置了超时，则`expire`命令将返回`(integer) 1`。如果设置超时失败，它将返回`(integer) 0`。

或者，您可以使用该`expireat`命令将密钥设置为在特定的时间点过期。它使用[_Unix时间戳_](https://en.wikipedia.org/wiki/Unix_time)作为参数，而不是到期前的秒数。Unix时间戳是自_Unix纪元_（即1970年1月1日UTC 00:00:00）以来的秒数。可以使用许多在线工具来查找特定日期和时间的Unix时间戳，例如[EpochConverter](https://www.epochconverter.com/)或[UnixTimestamp.com](https://www.unixtimestamp.com/)。

例如，要设置`key_melon`为在2025年5月1日格林尼治标准时间晚上8:30到期（以Unix timestamp表示`1746131400`），可以使用以下命令：

    expireat key_melon 1746131400
    

请注意，如果传递给您的时间戳`expireat`已经发生，它将立即删除密钥。

Checking How Long Until a Key Expires
-------------------------------------

你设置一键到期任何时候，你可以检查剩余到期为止（以秒为单位）的时候`ttl`，它的全称是“ **牛逼** IME **牛逼** Ø **升**香港专业教育学院”：

    ttl key_melon
    

    Output(integer) 433
    

有关更详细的信息，可以运行`pttl`，它将返回直到密钥过期的时间（以毫秒为单位）：

    pttl key_melon
    

    Output(integer) 431506
    

如果密钥尚未设置为过期且密钥不存在，则两者`ttl`和`pttl`都将返回。`(integer) -1``(integer) -2`

Persisting Keys
---------------

如果密钥已设置为过期，则任何覆盖密钥内容的命令（例如`set`或`getset`）都会清除密钥的超时值。要手动清除键的超时，请使用以下`persist`命令：

    persist key_melon
    

如果成功完成，该`persist`命令将返回`(integer) 1`，表明密钥将不再过期。

Conclusion
----------

本指南详细介绍了用于在Redis中操作和检查键持久性的许多命令。如果您想在本指南中概述其他相关的命令，参数或过程，请在下面的评论中提出疑问或提出建议。

有关Redis命令的更多信息，请参阅关于[如何管理Redis数据库的](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8redis%E6%95%B0%E6%8D%AE%E5%BA%93)系列教程。