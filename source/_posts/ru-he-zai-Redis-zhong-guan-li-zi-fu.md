---
title: 如何在Redis中管理字符串
id: 1342
date: 2024-10-31 22:01:51
author: daichangya
excerpt: 介绍Redis是一个开源的内存中键值数据存储。在Redis中，字符串是您可以创建和管理的最基本的值类型。本教程概述了如何创建和检索字符串以及如何操作字符串键所保存的值。如何使用本指南本指南以备有完整示例的备忘单形式编写。我们鼓励您跳至与您要完成的任务相关的任何部分。本指南中显示的命令已在运行Redi
permalink: /archives/ru-he-zai-Redis-zhong-guan-li-zi-fu/
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

[Redis](https://redis.io/)是一个开源的内存中键值数据存储。在Redis中，[_字符串_](https://redis.io/topics/data-types#strings)是您可以创建和管理的最基本的值类型。本教程概述了如何创建和检索字符串以及如何操作字符串键所保存的值。

#### 如何使用本指南

本指南以备有完整示例的备忘单形式编写。我们鼓励您跳至与您要完成的任务相关的任何部分。

本指南中显示的命令已在运行Redis版本4.0.9的Ubuntu 18.04服务器上进行了测试。要设置类似的环境，您可以按照我们的指南[如何在Ubuntu 18.04上安装和保护Redis的](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis)**步骤1**进行操作。我们将通过使用Redis命令行界面运行它们来演示这些命令的行为。请注意，如果您使用其他Redis界面（例如[Redli）](https://github.com/IBM-Cloud/redli)，则某些命令的确切输出可能会有所不同。 [](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis)`redis-cli`[](https://github.com/IBM-Cloud/redli)

另外，您可以提供一个托管的Redis数据库实例来测试这些命令，但是请注意，根据数据库提供者所允许的控制级别，本指南中的某些命令可能无法按所述方式工作。要配置DigitalOcean托管数据库，请遵循我们的[托管数据库产品文档](https://www.digitalocean.com/docs/databases/redis/quickstart/)。然后，**您必须** [**安装Redli**](https://www.digitalocean.com/community/tutorials/how-to-connect-to-managed-database-ubuntu-18-04#connecting-to-a-managed-redis-database) **或** [**设置TLS隧道**](https://www.digitalocean.com/community/tutorials/how-to-connect-to-managed-redis-over-tls-with-stunnel-and-redis-cli)才能通过TLS连接到托管数据库。

创建和管理字符串
--------

包含字符串的键只能包含一个值。您不能在一个键中存储多个字符串。但是，Redis中的字符串是二进制安全的，这意味着Redis字符串可以保存任何类型的数据，从字母数字字符到JPEG图像。唯一的限制是字符串的长度必须小于或等于512 MB。

要创建一个字符串，请使用`set`命令。例如，以下`set`命令创建一个名为key的键`key_Welcome1`，该键包含字符串`"Howdy"`：

    set key_Welcome1 "Howdy"
    

    OK
    

要在一个命令中设置多个字符串，请使用`mset`：

    mset key_Welcome2 "there" key_Welcome3 "partners,"
    

您还可以使用以下`append`命令创建字符串：

    append key_Welcome4 "welcome to Texas"
    

如果成功创建了字符串，`append`将输出一个整数，该整数等于该字符串包含的字符数：

    16
    

注意，`append`也可以用来更改字符串的内容。有关详细信息，请参见有关[处理字符串](https://www.digitalocean.com/community/cheatsheets/how-to-manage-strings-in-redis#manipulating-strings)的部分。

检索字符串
-----

要检索字符串，请使用以下`get`命令：

    get key_Welcome1
    

    Howdy
    

要使用一个命令检索多个字符串，请使用`mget`：

    mget key_Welcome1 key_Welcome2 key_Welcome3 key_Welcome4
    

    1) "Howdy"
    2) "there"
    3) "partners,"
    4) "welcome to Texas"
    

对于传递给`mget`它的每个键都不包含字符串值或根本不存在，该命令将返回`nil`。

操作字符串(Manipulating Strings)
---

如果字符串由整数组成，则可以运行`incr`命令将其增加一：

    set key_1 3
    incr key_1
    

    4
    

同样，您可以使用以下`incrby`命令将数字字符串的值增加特定的增量：

    incrby key_1 16
    

    20
    

该`decr`和`decrby`命令的工作方式相同，但他们减少存储在数字字符串的整数：

    decr key_1
    

    19
    

    decrby key_1 16
    

    3
    

如果字母字符串已经存在，`append`则将值附加到现有值的末尾，并返回字符串的新长度。为了说明这一点，以下命令将附加`", y'all"`到key所保存的字符串上`key_Welcome4`，因此现在该字符串将显示为`"welcome to Texas, y'all"`：

    append key_Welcome4 ", y'all"
    

    15
    

您也可以将整数附加到包含数字值的字符串中。以下示例附加`45`到`3`，其中包含整数`key_1`，因此它将保持`345`。在这种情况下，`append`还将返回字符串的新长度，而不是其新值：

    append key_1 45
    

    3
    

由于此键仍仅保留数字值，因此可以对其执行`incr`和`decr`操作。您也可以在整数字符串后附加字母字符，但是如果这样做，则在字符串上运行`incr`和运行`decr`将产生错误，因为字符串值不再是整数。

结论
--

本指南详细介绍了许多用于在Redis中创建和管理字符串的命令。如果您想在本指南中概述其他相关的命令，参数或过程，请在下面的评论中提出疑问或提出建议。

有关Redis命令的更多信息，请参阅关于[如何管理Redis数据库的](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8redis%E6%95%B0%E6%8D%AE%E5%BA%93)系列教程。