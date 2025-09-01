---
title: 如何在Redis中管理Sets
id: 1343
date: 2024-10-31 22:01:51
author: daichangya
excerpt: 介绍Redis是一个开源的内存中键值数据存储。设置在Redis的是储存在一个给定的钥匙串的Sets。当保存在一组中时，单个记录值称为_成员_。与列表不同，Sets是无序的，并且不允许重复的值。本教程说明了如何创建Sets，检索和删除成员以及比较不同Sets的成员。如何使用本指南本指南以备有完整示例的
permalink: /archives/ru-he-zai-Redis-zhong-guan-li-Sets/
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

[Redis](https://redis.io/)是一个开源的内存中键值数据存储。[_设置_](https://redis.io/topics/data-types#sets)在Redis的是储存在一个给定的钥匙串的Sets。当保存在一组中时，单个记录值称为_成员_。与列表不同，Sets是无序的，并且不允许重复的值。

本教程说明了如何创建Sets，检索和删除成员以及比较不同Sets的成员。

#### 如何使用本指南

本指南以备有完整示例的备忘单形式编写。我们鼓励您跳至与您要完成的任务相关的任何部分。

本指南中显示的命令已在运行Redis版本4.0.9的Ubuntu 18.04服务器上进行了测试。要设置类似的环境，您可以按照我们的指南[如何在Ubuntu 18.04上安装和保护Redis的](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis)**步骤1**进行操作。我们将通过使用Redis命令行界面运行它们来演示这些命令的行为。请注意，如果您使用其他Redis界面（例如[Redli）](https://github.com/IBM-Cloud/redli)，则某些命令的确切输出可能会有所不同。[](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis)`redis-cli`[](https://github.com/IBM-Cloud/redli)

另外，您可以提供一个托管的Redis数据库实例来测试这些命令，但是请注意，根据数据库提供者所允许的控制级别，本指南中的某些命令可能无法按所述方式工作。要配置DigitalOcean托管数据库，请遵循我们的[托管数据库产品文档](https://www.digitalocean.com/docs/databases/redis/quickstart/)。然后，**您必须** [**安装Redli**](https://www.digitalocean.com/community/tutorials/how-to-connect-to-managed-database-ubuntu-18-04#connecting-to-a-managed-redis-database) **或** [**设置TLS隧道**](https://www.digitalocean.com/community/tutorials/how-to-connect-to-managed-redis-over-tls-with-stunnel-and-redis-cli)才能通过TLS连接到托管数据库。

创建Sets
----

该`sadd`命令允许您创建一个Sets并向其中添加一个或多个成员。下面的例子将创建一组在一个名为键`key_horror`与成员`"Frankenstein"`和`"Godzilla"`：

    sadd key_horror "Frankenstein" "Godzilla"
    

如果成功，`sadd`将返回一个整数，显示它添加到Sets中的成员数量：

    (integer) 2
    

如果您尝试将Sets的成员添加到已经持有非Sets值的键中，它将返回错误。在此块中的第一个命令创建一个[列表](https://www.digitalocean.com/community/cheatsheets/how-to-manage-lists-in-redis?status=moved_permanently)命名的`key_action`一个元素，`"Shaft"`。下一条命令尝试将set成员添加`"Shane"`到列表中，但是由于数据类型冲突而产生错误：

    rpush key_action "Shaft"
    sadd key_action "Shane"
    

    (error) WRONGTYPE Operation against a key holding the wrong kind of value
    

请注意，Sets不允许同一成员出现多次：

    sadd key_comedy "It's" "A" "Mad" "Mad" "Mad" "Mad" "Mad" "World"
    

    (integer) 4
    

即使此`sadd`命令指定了八个成员，它也会丢弃四个重复的`"Mad"`成员，从而将大小设置为4。

从Sets中检索成员
--------

在本节中，我们将介绍一些Redis命令，这些命令返回有关Sets中持有的成员的信息。要练习此处概述的命令，请运行以下命令，这将创建一个由六个成员组成的Sets，该Sets的键为`key_stooges`：

    sadd key_stooges "Moe" "Larry" "Curly" "Shemp" "Joe" "Curly Joe"
    

要从Sets中返回每个成员，请运行`smembers`命令，然后输入要检查的密钥：

    smembers key_stooges
    

    1) "Curly"
    2) "Moe"
    3) "Larry"
    4) "Shemp"
    5) "Curly Joe"
    6) "Joe"
    

要检查特定值是否是Sets的成员，请使用以下`sismember`命令：

    sismember key_stooges "Harpo"
    

如果元素`"Harpo"`是`key_stooges`Sets的成员，`sismember`则将返回`1`。否则，它将返回`0`：

    (integer) 0
    

要查看给定Sets中有多少成员（换句话说，找到给定Sets的_基数_），请运行`scard`：

    scard key_stooges
    

    (integer) 6
    

要从Sets中返回随机元素，请运行`srandmember`：

    srandmember key_stooges
    

    "Larry"
    

要从Sets中返回多个随机，不同的元素，可以在`srandmember`命令后加上要检索的元素数量：

    srandmember key_stooges 3
    

    1) "Larry"
    2) "Moe"
    3) "Curly Joe"
    

如果您向传递一个负数`srandmember`，则该命令可以多次返回相同的元素：

    srandmember key_stooges -3
    

    1) "Shemp"
    2) "Curly Joe"
    3) "Curly Joe"
    

`srandmember`尽管所使用的随机元素函数的性能在较大的数据集中有所改善，但它并不是完全随机的。有关更多详细信息，请参见[命令的官方文档](https://redis.io/commands/srandmember#distribution-of-returned-elements)。

从Sets中删除成员
--------

Redis的带有用于从一组删除成员三个命令：`spop`，`srem`，和`smove`。

`spop`从中随机选择指定数量的成员并返回它们，类似于`srandmember`，但是从Sets中删除它们。它接受包含Sets的键名和要从Sets中删除的成员数作为参数。如果您未指定数字，`spop`则默认为返回并删除单个值。

以下示例命令将从`key_stooges`上一节创建的Sets中删除并返回两个随机选择的元素：

    spop key_stooges 2
    

    1) "Shemp"
    2) "Larry"
    

`srem` 允许您从Sets中删除一个或多个特定成员，而不是随机成员：

    srem key_stooges "Joe" "Curly Joe"
    

而不是返回从Sets中删除的成员，而是`srem`返回一个整数，显示已删除的成员数：

    (integer) 2
    

使用`smove`一个成员从一组移动到另一个。此命令以该顺序接受源集，目标集和要移动的成员作为参数。请注意，一次`smove`只能移动一位成员：

    smove key_stooges key_jambands "Moe"
    

如果命令成功移动了成员，它将返回`(integer) 1`：

    (integer) 1
    

如果`smove`失败，它将返回`(integer) 0`。请注意，如果目标键尚不存在，请`smove`在将成员移入之前创建它。

比较集
---

Redis还提供了许多命令，可以找到Sets之间的差异和相似性。为了演示如何工作的，这部分将引用一个名为三套`presidents`，`kings`和`beatles`。如果您想亲自尝试本节中的命令，请创建这些Sets并使用以下`sadd`命令填充它们：

    sadd presidents "George" "John" "Thomas" "James"
    sadd kings "Edward" "Henry" "John" "James" "George"
    sadd beatles "John" "George" "Paul" "Ringo"
    

`sinter`比较不同的Sets并返回_Sets相交_或出现在每个Sets中的值：

    sinter presidents kings beatles
    

    1) "John"
    2) "George"
    

`sinterstore`执行类似的功能，但不是返回相交成员，而是在包含这些相交成员的指定目的地创建了一个新Sets。请注意，如果目的地已经存在，`sinterstore`将覆盖其内容：

    sinterstore new_set presidents kings beatles
    smembers new_set
    

    1) "John"
    2) "George"
    

`sdiff`返回_Sets差异_ —由以下每个Sets的第一个指定Sets的​​差异得出的成员：

    sdiff presidents kings beatles
    

    1) "Thomas"
    

换句话说，`sdiff`查看第一个给定Sets中的每个成员，然后将其与每个连续Sets中的成员进行比较。第一组中也出现在以下组中的任何成员都将被删除，并`sdiff`返回其余成员。可以将其视为从第一组中删除后续组的成员。

`sdiffstore`执行与相似的功能`sdiff`，但不返回Sets差，而是在给定的目的地创建一个包含Sets差的新Sets：

    sdiffstore new_set beatles kings presidents
    smembers new_set
    

    1) "Paul"
    2) "Ringo"
    

像一样`sinterstore`，`sdiffstore`将覆盖目标键（如果已存在）。

`sunion`返回_Setsunion_或包含您指定的每个Sets的每个成员的Sets：

    sunion presidents kings beatles
    

    1) "Thomas"
    2) "George"
    3) "Paul"
    4) "Henry"
    5) "James"
    6) "Edward"
    7) "John"
    8) "Ringo"
    

`sunion` 将结果视为新集，因为它只允许出现任何给定成员。

`sunionstore` 执行类似的功能，但是在给定的目的地创建一个包含Sets并集的新Sets，而不仅仅是返回结果：

    sunionstore new_set presidents kings beatles
    

    (integer) 8
    

与`sinterstore`和一样`sdiffstore`，`sunionstore`如果目标键已经存在，它将覆盖目标键。

结论
--

本指南详细介绍了用于在Redis中创建和管理集的许多命令。如果您想在本指南中概述其他相关的命令，参数或过程，请在下面的评论中提出疑问或提出建议。

有关Redis命令的更多信息，请参阅关于[如何管理Redis数据库的](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8redis%E6%95%B0%E6%8D%AE%E5%BA%93)系列教程。

作者：[分布式编程](https://blog.jsdiff.com/)
出处：[https://blog.jsdiff.com/](https://blog.jsdiff.com/)
如果你喜欢本文,请长按二维码，关注 **分布式编程**
.![分布式编程](https://images.jsdiff.com/%E5%88%86%E5%B8%83%E5%BC%8F%E7%BC%96%E7%A8%8B%E5%B0%8F%E7%A8%8B%E5%BA%8F_1588414366441.jpg)