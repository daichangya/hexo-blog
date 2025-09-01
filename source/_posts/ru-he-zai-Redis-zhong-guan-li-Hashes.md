---
title: 如何在Redis中管理Hashes
id: 1344
date: 2024-10-31 22:01:51
author: daichangya
excerpt: 介绍Redis是一个开源的内存中键值数据存储。RedisHashes是一种数据类型，表示字符串字段和字符串值之间的映射。Hashes可以容纳许多字段-值对，并且设计为不占用太多空间，因此使其非常适合表示数据对象。例如，Hashes可能代表一个客户，以及包括像场name，address，email，或
permalink: /archives/ru-he-zai-Redis-zhong-guan-li-Hashes/
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

[Redis](https://redis.io/)是一个开源的内存中键值数据存储。Redis [_Hashes_](https://redis.io/topics/data-types#hashes)是一种数据类型，表示字符串字段和字符串值之间的映射。Hashes可以容纳许多字段-值对，并且设计为不占用太多空间，因此使其非常适合表示数据对象。例如，Hashes可能代表一个客户，以及包括像场`name`，`address`，`email`，或`customer_id`。

本教程将介绍如何在Redis中管理Hashes，从创建Hashes到检索和删除Hashes中保存的数据。

#### 如何使用本指南

本指南以备有完整示例的备忘单形式编写。我们鼓励您跳至与您要完成的任务相关的任何部分。

本指南中显示的命令已在运行Redis版本4.0.9的Ubuntu 18.04服务器上进行了测试。要设置类似的环境，您可以按照我们的指南[如何在Ubuntu 18.04上安装和保护Redis的](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis)**步骤1**进行操作。我们将通过使用Redis命令行界面运行它们来演示这些命令的行为。请注意，如果您使用其他Redis界面（例如[Redli）](https://github.com/IBM-Cloud/redli)，则某些命令的确切输出可能会有所不同。[](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis)`redis-cli`[](https://github.com/IBM-Cloud/redli)

另外，您可以提供一个托管的Redis数据库实例来测试这些命令，但是请注意，根据数据库提供者所允许的控制级别，本指南中的某些命令可能无法按所述方式工作。要配置DigitalOcean托管数据库，请遵循我们的[托管数据库产品文档](https://www.digitalocean.com/docs/databases/redis/quickstart/)。然后，**您必须** [**安装Redli**](https://www.digitalocean.com/community/tutorials/how-to-connect-to-managed-database-ubuntu-18-04#connecting-to-a-managed-redis-database) **或** [**设置TLS隧道**](https://www.digitalocean.com/community/tutorials/how-to-connect-to-managed-redis-over-tls-with-stunnel-and-redis-cli)才能通过TLS连接到托管数据库。

创建Hashes
----

要创建Hashes，请运行`hset`命令。此命令接受Hashes键的名称，字段字符串和相应的值字符串作为参数：

    hset poet:Verlaine nationality French
    

**注意：**在此示例及以下示例中，`poet:Verlaine`是Hashes键。点，破折号和冒号通常用于使多字键和字段更具可读性。确保您的密钥遵循一致且易于阅读的格式很有帮助。  

`hset`返回`(integer) 1`如果指定的字段是一个新的领域和值设置正确：

    1
    

但是，如果您未能包含Hashes键的值，字段或名称，`hset`将返回错误。

另外，请注意，`hset`如果Hashes值已经存在，它将覆盖其内容：

    hset poet:Verlaine nationality Francais
    

如果该字段已经存在并且其值已成功更新，`hset`将返回`(integer) 0`：

    0
    

您还可以`hsetnx`用于将字段添加到Hashes，但是只有在字段不存在时才起作用。如果指定的字段已经存在，`hsetnx`将不会有任何效果，并将返回`(integer) 0`：

    hsetnx poet:Verlaine nationality French
    

    0
    

要将多个字段/值对设置为给定的集合，请使用`hmset`命令，后跟相应的字段/值字符串：

    hmset poet:Verlaine born 1844 died 1896 genre Decadent
    

`hmset``OK`成功就会返回。

从Hashes中检索信息
--------

您可以使用以下`hexists`命令确定给定Hashes的字段是否存在：

    hexists poet:Verlaine nationality
    

`hexists``(integer) 1`如果该字段确实存在，则返回，如果不存在则返回`(integer) 0`。

要返回一个字段的值，请运行以下`hget`命令，然后依次按Hashes键和要检索其值的字段：

    hget poet:Verlaine nationality
    

    "Francais"
    

`hmget` 使用相同的语法，但可以返回多个字段的值

    hmget poet:Verlaine born died
    

    1) "1844"
    2) "1896"
    

如果您传递给`hget`或`hmget`不存在的Hashes，这两个命令将返回`(nil)`：

    hmget poet:Dickinson born died
    

    1) (nil)
    2) (nil)
    

要获取特定Hashes中包含的所有字段的列表，请运行以下`hkeys`命令：

    hkeys poet:Verlaine
    

    1) "nationality"
    2) "born"
    3) "died"
    4) "genre"
    

相反，运行`hvals`以检索散列中包含的值的列表：

    hvals poet:Verlaine
    

    1) "French"
    2) "1844"
    3) "1896"
    4) "Decadent"
    

要返回Hashes表所包含的每个字段及其关联值的列表，请运行`hgetall`：

    hgetall poet:Verlaine
    

    1) "nationality"
    2) "French"
    3) "born"
    4) "1844"
    5) "died"
    6) "1896"
    7) "genre"
    8) "Decadent"
    

您可以通过运行来查找Hashes中的字段数`hlen`，它代表“ **h** ash **len** gth”：

    hlen poet:Verlaine
    

    4
    

你可以找到一个字段关联的值字符串的长度`hstrlen`，它的全称是“ **^ h**灰**海峡**荷兰国际集团**LEN** GTH”：

    hstrlen poet:Verlaine nationality
    

    8
    

`hlen``(integer) 0`如果Hashes不存在，将返回。

从Hashes中删除字段
--------

要从Hashes表中删除字段，请运行`hdel`命令。`hdel`可以接受多个字段作为参数，并将返回一个整数，该整数指示从Hashes中删除了多少个字段：

    hdel poet:Verlaine born died
    

    2
    

如果您将一个不存在的字段传递给`hdel`，它将忽略该字段，但删除您指定的任何其他现有字段。

结论
--

本指南详细介绍了用于在Redis中创建和管理Hashes的许多命令。如果您想在本指南中概述其他相关的命令，参数或过程，请在下面的评论中提出疑问或提出建议。

有关Redis命令的更多信息，请参阅关于[如何管理Redis数据库的](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8redis%E6%95%B0%E6%8D%AE%E5%BA%93)系列教程。