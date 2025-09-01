---
title: 在Redis中怎么使用Lists
id: 1335
date: 2024-10-31 22:01:51
author: daichangya
excerpt: "redis list操作指南"
permalink: /archives/listsinredis/
categories:
 - redis
tags: 
 - redis基础教程
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

[Redis](https://redis.io/)是一个开源的内存中键值数据存储。在Redis中，[_列表_](https://redis.io/topics/data-types#lists)是按插入顺序排序的字符串的集合，类似于[链接列表](https://en.wikipedia.org/wiki/Linked_list)。本教程介绍了如何在Redis列表中创建和使用元素。

#### 如何使用本指南

本指南以备有完整示例的备忘单形式编写。我们鼓励您跳至与您要完成的任务相关的任何部分。

本指南中显示的命令已在运行Redis版本4.0.9的Ubuntu 18.04服务器上进行了测试。要设置类似的环境，您可以按照我们的指南[如何在Ubuntu 18.04上安装和保护Redis的](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis)**步骤1**进行操作。我们将通过使用Redis命令行界面运行它们来演示这些命令的行为。请注意，如果您使用其他Redis界面（例如[Redli）](https://github.com/IBM-Cloud/redli)，则某些命令的确切输出可能会有所不同。[](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis)`redis-cli`[](https://github.com/IBM-Cloud/redli)

另外，您可以提供一个托管的Redis数据库实例来测试这些命令，但是请注意，根据数据库提供者所允许的控制级别，本指南中的某些命令可能无法按所述方式工作。要配置DigitalOcean托管数据库，请遵循我们的[托管数据库产品文档](https://www.digitalocean.com/docs/databases/redis/quickstart/)。然后，**您必须** [**安装Redli**](https://blog.jsdiff.com/archives/howtoconnecttoaredisdatabase) **或** [**设置TLS隧道**](https://www.digitalocean.com/community/tutorials/how-to-connect-to-managed-redis-over-tls-with-stunnel-and-redis-cli)才能通过TLS连接到托管数据库。

Creating Lists
----

一个键只能容纳一个列表，尽管任何列表都可以容纳40亿个元素。Redis从左到右读取列表，您可以使用命令将新列表元素添加到列表的开头（“左”端），`lpush`也可以使用尾部（“右”端）添加新元素`rpush`。您还可以使用`lpush`或`rpush`创建新列表：

    lpush key value
    

这两个命令都将输出一个整数，以显示列表中有多少个元素。为了说明，请运行以下命令以创建包含“我认为是我”的​​格言的列表：

    lpush key_philosophy1 "therefore"
    lpush key_philosophy1 "think"
    rpush key_philosophy1 "I"
    lpush key_philosophy1 "I"
    rpush key_philosophy1 "am"
    

最后一条命令的输出将显示为：

    (integer) 5
    

请注意，您可以使用单个`lpush`或`rpush`语句添加多个列表元素：

    rpush key_philosophy1 "-" "Rene" "Decartes"
    

该`lpushx`和`rpushx`命令也用于元素添加到列表中，但如果给定的名单已经存在只会工作。如果任何一个命令失败，它将返回`(integer) 0`：

    rpushx key_philosophy2 "Happiness" "is" "the" "highest" "good" "–" "Aristotle"
    

    (integer) 0
    

要更改列表中的现有元素，请运行`lset`命令，然后输入键名，要更改的元素的索引和新值：

    lset key_philosophy1 5 "sayeth"
    

如果尝试将列表元素添加到不包含列表的现有键中，则会导致数据类型冲突并返回错误。例如，以下`set`命令创建一个保存字符串的键，因此以下尝试向其中添加列表元素的尝试`lpush`将失败：

    set key_philosophy3 "What is love?"
    lpush key_philosophy3 "Baby don't hurt me"
    

    (error) WRONGTYPE Operation against a key holding the wrong kind of value
    

无法将Redis密钥从一种数据类型转换为另一种数据类型，因此要变成`key_philosophy3`列表，您需要删除该密钥并使用`lpush`or `rpush`命令重新开始。

从列表中检索元素(Retrieving Elements from a List)
--------

要检索列表中的项目范围，请使用`lrange`命令，后跟起始[_偏移量_](https://en.wikipedia.org/wiki/Offset_(computer_science))和终止偏移量。每个偏移量都是从零开始的索引，`0`表示代表列表中的第一个元素，`1`代表下一个，依此类推。

以下命令将从上一节创建的示例列表中返回所有元素：

    lrange key_philosophy1 0 7
    

    1) "I"
    2) "think"
    3) "therefore"
    4) "I"
    5) "am"
    6) "sayeth"
    7) "Rene"
    8) "Decartes"
    

传递给的偏移量`lrange`也可以为负数。在这种情况下使用时，`-1`代表列表中的最后一个元素，`-2`代表列表中的倒数第二个元素，依此类推。以下示例返回保存在列表中的最后三个元素`key_philosophy1`：

    lrange key_philosophy1 -3 -1
    

    1) "I"
    2) "am"
    3) "sayeth"
    

要从列表中检索单个元素，可以使用`lindex`命令。但是，此命令要求您提供元素的索引作为参数。与一样`lrange`，索引是从零开始的，这意味着第一个元素在index `0`，第二个元素在index `1`，依此类推：

    lindex key_philosophy1 4
    

    "am"
    

要查找给定列表中有多少个元素，请使用以下`llen`命令，该命令是“ **l** ist **len** gth”的缩写：

    llen key_philosophy1
    

    (integer) 8
    

如果存储在给定键上的值不存在，`llen`将返回错误。

从列表中删除元素
--------

该`lrem`命令将删除与给定值匹配的已定义次数的第一个。要对此进行试验，请创建以下列表：

    rpush key_Bond "Never" "Say" "Never" "Again" "You" "Only" "Live" "Twice" "Live" "and" "Let" "Die" "Tomorrow" "Never" "Dies"
    

以下`lrem`示例将删除该值的第一次出现`"Live"`：

    lrem key_Bond 1 "Live"
    

此命令将输出从列表中删除的元素数量：

    (integer) 1
    

传递给`lrem`命令的数字也可以为负数。以下示例将删除该值的最后两个出现`"Never"`：

    lrem key_Bond -2 "Never"
    

    (integer) 2
    

该`lpop`命令从列表中删除并返回第一个或“最左边”的元素：

    lpop key_Bond
    

    "Never"
    

同样，要从列表中删除并返回最后或“最右边”的元素，请使用`rpop`：

    rpop key_Bond
    

    "Dies"
    

Redis还包括`rpoplpush`命令，该命令从列表中删除最后一个元素并将其推到另一个列表的开头：

    rpoplpush key_Bond key_AfterToday
    

    "Tomorrow"
    

如果传递给`rpoplpush`命令的源键和目标键相同，则它将实质上旋转列表中的元素。

结论
--

本指南详细介绍了可用于在Redis中创建和管理列表的许多命令。如果您想在本指南中概述其他相关的命令，参数或过程，请在下面的评论中提出疑问或提出建议。

有关Redis命令的更多信息，请参阅关于[如何管理Redis数据库的](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8redis%E6%95%B0%E6%8D%AE%E5%BA%93)系列教程。