---
title: 如何在Redis中运行事务
id: 1347
date: 2024-10-31 22:01:51
author: daichangya
excerpt: 介绍Redis是一个开源的内存中键值数据存储。Redis允许您计划一系列命令，然后一个接一个地运行它们，这一过程称为_transaction_。每个事务都被视为不间断且隔离的操作，以确保数据完整性。在执行事务块时，客户端无法运行命令本教程介绍了如何执行和取消交易，还包括一些与交易通常相关的陷阱的信息
permalink: /archives/ru-he-zai-Redis-zhong-yun-xing-shi-wu/
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

[Redis](https://redis.io/)是一个开源的内存中键值数据存储。Redis允许您计划一系列命令，然后一个接一个地运行它们，这一过程称为_transaction_。每个事务都被视为不间断且隔离的操作，以确保数据完整性。在执行事务块时，客户端无法运行命令

本教程介绍了如何执行和取消交易，还包括一些与交易通常相关的陷阱的信息。

#### 如何使用本指南

本指南以备有完整示例的备忘单形式编写。我们鼓励您跳至与您要完成的任务相关的任何部分。

本指南中显示的命令已在运行Redis版本4.0.9的Ubuntu 18.04服务器上进行了测试。要设置类似的环境，您可以按照我们的指南[如何在Ubuntu 18.04上安装和保护Redis的](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis)**步骤1**进行操作。我们将通过使用Redis命令行界面运行它们来演示这些命令的行为。请注意，如果您使用其他Redis界面（例如[Redli）](https://github.com/IBM-Cloud/redli)，则某些命令的确切输出可能会有所不同。[](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis)`redis-cli`[](https://github.com/IBM-Cloud/redli)

另外，您可以提供一个托管的Redis数据库实例来测试这些命令，但是请注意，根据数据库提供者所允许的控制级别，本指南中的某些命令可能无法按所述方式工作。要配置DigitalOcean托管数据库，请遵循我们的[托管数据库产品文档](https://www.digitalocean.com/docs/databases/redis/quickstart/)。然后，**您必须** [**安装Redli**](https://www.digitalocean.com/community/tutorials/how-to-connect-to-managed-database-ubuntu-18-04#connecting-to-a-managed-redis-database) **或** [**设置TLS隧道**](https://www.digitalocean.com/community/tutorials/how-to-connect-to-managed-redis-over-tls-with-stunnel-and-redis-cli)才能通过TLS连接到托管数据库。

Running Transactions
--------------------

该`multi`命令告诉Redis开始事务块。在执行`exec`命令之前，所有后续命令都将排队等待。

以下命令形成一个事务块。第一个命令启动事务，第二个命令设置一个包含值的字符串的键`1`，第三个命令将值增加1，第四个命令将其值增加40，第五个返回字符串的当前值，最后一个返回执行事务块：

    multi
    set key_MeaningOfLife 1
    incr key_MeaningOfLife
    incrby key_MeaningOfLife 40
    get key_MeaningOfLife
    exec
    

运行后`multi`，`redis-cli`将使用响应以下每个命令`QUEUED`。运行`exec`命令后，它将分别显示每个命令的输出：

    Output1) OK
    2) (integer) 2
    3) (integer) 42
    4) "42"
    

事务块中包含的命令按排队顺序依次运行。Redis事务是_原子的_，这意味着要么处理事务块中的每个命令（意味着它被视为有效命令并排队等待执行），要么不执行。但是，即使命令成功排队，执行时它仍然可能产生错误。在这种情况下，事务中的其他命令仍然可以运行，但是Redis将跳过导致错误的命令。有关更多详细信息，请参见[了解事务错误](https://www.digitalocean.com/community/cheatsheets/how-to-run-transactions-in-redis#understanding-transaction-errors)的部分。

Canceling Transactions
----------------------

要取消交易，请运行`discard`命令。这样可以防止任何先前排队的命令运行：

    multi
    set key_A 146
    incrby key_A 10
    discard
    

    OutputOK
    

该`discard`命令将连接恢复到正常状态，该状态告诉Redis像往常一样运行单个命令。您需要`multi`再次运行以告知服务器您正在开始另一笔交易。

Understanding Transaction Errors
--------------------------------

某些命令可能无法排队，例如语法错误的命令。如果尝试对语法错误的命令进行排队，则Redis将返回错误。

下面的事务创建了一个名为的键`key_A`，然后尝试将其增加10。但是，`incrby`命令中的拼写错误导致并导致错误并关闭了该事务：

    multi
    set key_A 146
    incrbuy key_A 10
    

    Output(error) ERR unknown command 'incrbuy'
    

如果`exec`在尝试将命令与类似语法错误的命令放入队列后尝试运行命令，则会收到另一条错误消息，告知您事务已被丢弃：

    exec
    

    Output(error) EXECABORT Transaction discarded because of previous errors.
    

在这种情况下，您需要重新启动事务块并确保正确输入每个命令。

一些不可能命令_是_可能的队列，例如运行`incr`在仅包含字符串的密钥。由于该命令在语法上是正确的，因此，如果您尝试将其包含在事务中，则Redis不会返回错误，也不会阻止您运行`exec`。在这种情况下，将执行队列中的所有其他命令，但不可能的命令将返回错误：

    multi
    set key_A 146
    incrby key_A "ten"
    exec
    

    Output1) OK
    2) (error) ERR value is not an integer or out of range
    

有关Redis如何处理事务内部错误的更多信息，请参阅[关于此主题](https://redis.io/topics/transactions#errors-inside-a-transaction)的[官方文档](https://redis.io/topics/transactions#errors-inside-a-transaction)。

Conclusion
----------

本指南详细介绍了许多用于在Redis中创建，运行和取消事务的命令。如果您想在本指南中概述其他相关的命令，参数或过程，请在下面的评论中提出疑问或提出建议。

有关Redis命令的更多信息，请参阅关于[如何管理Redis数据库的](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8redis%E6%95%B0%E6%8D%AE%E5%BA%93)系列教程。