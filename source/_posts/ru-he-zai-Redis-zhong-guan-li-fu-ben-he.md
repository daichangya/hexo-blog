---
title: 如何在Redis中管理副本和客户端
id: 1341
date: 2024-10-31 22:01:51
author: daichangya
excerpt: 介绍Redis是一个开源的内存中键值数据存储。它最受追捧的功能之一是对复制的支持：任何Redis服务器都可以将其数据复制到任意数量的副本中，从而实现高读取可伸缩性和强大的数据冗余性。此外，Redis旨在允许许多客户端（默认情况下最多10000个）连接数据并与之交互，因此对于许多用户需要访问同一数据集
permalink: /archives/ru-he-zai-Redis-zhong-guan-li-fu-ben-he/
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

[Redis](https://redis.io/)是一个开源的内存中键值数据存储。它最受追捧的功能之一是对复制的支持：任何Redis服务器都可以将其数据复制到任意数量的副本中，从而实现高读取可伸缩性和强大的数据冗余性。此外，Redis旨在允许许多客户端（默认情况下最多10000个）连接数据并与之交互，因此对于许多用户需要访问同一数据集的情况而言，它是一个不错的选择。

本教程介绍了用于管理Redis客户端和副本的命令。

#### 如何使用本指南

本指南以备有完整示例的备忘单形式编写。我们鼓励您跳至与您要完成的任务相关的任何部分。

本指南中显示的命令已在运行Redis版本4.0.9的Ubuntu 18.04服务器上进行了测试。要设置类似的环境，您可以按照我们的指南[如何在Ubuntu 18.04上安装和保护Redis的](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis)**步骤1**进行操作。我们将通过使用Redis命令行界面运行它们来演示这些命令的行为。请注意，如果您使用其他Redis界面（例如[Redli）](https://github.com/IBM-Cloud/redli)，则某些命令的确切输出可能会有所不同。[](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis)`redis-cli`[](https://github.com/IBM-Cloud/redli)

另外，您可以提供一个托管的Redis数据库实例来测试这些命令，但是请注意，根据数据库提供者所允许的控制级别，本指南中的某些命令可能无法按所述方式工作。要配置DigitalOcean托管数据库，请遵循我们的[托管数据库产品文档](https://www.digitalocean.com/docs/databases/redis/quickstart/)。然后，**您必须** [**安装Redli**](https://www.digitalocean.com/community/tutorials/how-to-connect-to-managed-database-ubuntu-18-04#connecting-to-a-managed-redis-database) **或** [**设置TLS隧道**](https://www.digitalocean.com/community/tutorials/how-to-connect-to-managed-redis-over-tls-with-stunnel-and-redis-cli)才能通过TLS连接到托管数据库。

**注意：** Redis项目在其文档和各种命令中使用术语“主”和“从”来标识复制中的不同角色，尽管该项目的参与者[正在采取措施](https://github.com/antirez/redis/issues/5335)在不引起兼容性问题的情况下[更改此语言](https://github.com/antirez/redis/issues/5335)。 。DigitalOcean通常更喜欢使用替代术语“主要”和“副本”。

本指南将在可能的情况下默认设置为“主要”和“副本”，但请注意，在某些情况下不可避免地会出现“主”和“从”这两个术语。  

管理副本
----

Redis最具特色的功能之一是其[内置的复制功能](https://redis.io/topics/replication)。使用复制时，Redis创建主实例的精确副本。这些辅助实例在其连接断开时会随时重新连接至主要实例，并且始终旨在保持主要实例的精确副本。

如果不确定当前连接的Redis实例是主实例还是副本，则可以通过运行以下`role`命令进行检查：

    role
    

如果您使用[Redis Sentinel](https://redis.io/topics/sentinel)，则此命令将返回`master`或`slave`，或者可能返回。`sentinel`[](https://redis.io/topics/sentinel)

要将Redis实例动态指定为另一个实例的副本，请运行`replicaof`命令。此命令将预期的主服务器的主机名或IP地址和端口作为参数：

    replicaof hostname_or_IP port
    

如果服务器已经是另一台主服务器的副本，它将停止复制旧服务器，并立即开始与新服务器同步。它还将丢弃旧数据集。

要将副本提升为主副本，请运行以下`replicaof`命令：

    replicaof no one
    

这将阻止实例复制主服务器，但不会丢弃已复制的数据集。在原始主数据库失败的情况下，此语法很有用。在`replicaof no one`发生故障的主数据库的副本上运行之后，以前的副本可以用作新的主数据库，并拥有自己的副本作为故障保护。

**注意：**在5.0.0之前的版本中，Redis包含了此命令的一个名为的版本`slaveof`。  

管理客户
----

一个[_客户_](https://en.wikipedia.org/wiki/Client_(computing))是任何机器或软件连接到服务器才能访问服务。Redis附带了一些命令，可帮助跟踪和管理客户端连接。

该`client list`命令返回一组有关当前客户端连接的可读信息：

    client list
    

    Output"id=18165 addr=[2001:db8:0:0::12]:47460 fd=7 name=jerry age=72756 idle=0 flags=N db=0 sub=0 psub=0 multi=-1 qbuf=0 qbuf-free=0 obl=0 oll=0 omem=0 events=r cmd=ping
    id=18166 addr=[2001:db8:0:1::12]:47466 fd=8 name= age=72755 idle=5 flags=N db=0 sub=0 psub=0 multi=-1 qbuf=0 qbuf-free=0 obl=0 oll=0 omem=0 events=r cmd=info
    id=19381 addr=[2001:db8:0:2::12]:54910 fd=9 name= age=9 idle=0 flags=N db=0 sub=0 psub=0 multi=-1 qbuf=26 qbuf-free=32742 obl=0 oll=0 omem=0 events=r cmd=client
    "
    

以下是每个字段的含义：

*   `id`：唯一的64位客户端ID
*   `name`：客户端连接的名称，由先前的`client setname`命令定义
*   `addr`：客户端连接的地址和端口
*   `fd`：与客户端所连接的套接字相对应的[文件描述符](https://en.wikipedia.org/wiki/File_descriptor)
*   `age`：客户端连接的总时长，以秒为单位
*   `flags`：一组一个或多个单字符标志，可提供有关客户端的更详细的信息；有关更多详细信息，请参见[`client list`命令文档](https://redis.io/commands/client-list)
*   `db`：客户端连接到的当前数据库ID号（可以从`0`到`15`）
*   `sub`：客户端订阅的频道数
*   `psub`：客户端的模式匹配订阅数
*   `mutli`：客户端已在[事务中](https://www.digitalocean.com/community/cheatsheets/how-to-run-transactions-in-redis)排队的命令数（将显示`-1`客户端是否尚未开始事务或`0`是否仅已开始事务且未排队任何命令）
*   `qbuf`：客户端的查询缓冲区长度，`0`这意味着它没有待处理的查询
*   `qbuf-free`：客户端查询缓冲区中的可用空间量，`0`表示查询缓冲区已满
*   `obl`：客户端的输出缓冲区长度
*   `oll`：客户端的输出列表的长度，当客户端的缓冲区已满时，将在其中排队答复
*   `omem`：客户端的输出缓冲区使用的内存
*   `events`：客户端的文件描述符事件，可以是`r`“可读”，`w`“可写”或两者兼有
*   `cmd`：客户端运行的最后一条命令

设置客户端名称对于调试使用Redis的任何应用程序中的连接泄漏都很有用。每个新连接都将在开始时没有分配的名称，但`client setname`可用于为当前客户端连接创建一个新连接。尽管Redis通常将字符串长度限制为512 MB，但是对客户端名称的长度没有限制。但是请注意，客户端名称不能包含空格：

    client setname elaine
    

要检索客户端连接的名称，请使用以下`client getname`命令：

    client getname
    

    Output"elaine"
    

要获取客户端的连接ID，请使用以下`client id`命令：

    client id
    

    "19492"
    

Redis客户端ID永远不会重复，并且会单调递增。这意味着，如果一个客户端的ID大于另一个客户端，则它是在以后的时间建立的。

阻止客户端并关闭客户端连接
-------------

复制系统通常被描述为_同步_或_异步_。在同步复制中，每当客户端添加或更改数据时，客户端都必须从一定数量的副本中收到某种确认，以使更改注册为已提交。这有助于防止节点发生数据冲突，但是这会增加延迟，因为客户端必须等待执行另一项操作，直到从一定数量的副本中收到回音为止。

另一方面，在异步复制中，一旦将数据写入本地存储，客户端就会看到确认操作已完成的确认。但是，这与副本实际写入数据的时间之间可能会有滞后。如果其中一个副本在写入更改之前失败，则该写入将永远丢失。因此，尽管异步复制允许客户端继续执行操作而没有等待副本引起的延迟，但它可能导致节点之间的数据冲突，并且可能需要数据库管理员方面的额外工作来解决这些冲突。

由于注重性能和低延迟，Redis默认情况下实现异步复制。但是，您可以使用该`wait`命令模拟同步复制。`wait`在指定的时间（以毫秒为单位）内阻止当前客户端连接，直到所有先前的写命令成功传输并被指定数量的副本接受为止。此命令使用以下语法：

    wait number_of_replicas number_of_milliseconds
    

例如，如果要在30毫秒的超时时间内至少3个副本注册所有先前的写入操作之前阻止客户端连接，则`wait`语法应如下所示：

    wait 3 30
    

该`wait`命令返回一个整数，该整数表示已确认写入命令的副本数，即使并非每个副本都这样做：

    2
    

要解除阻止以前通过`wait`（`brpop`，或）`xread`命令阻止的客户端连接，可以`client unblock`使用以下语法运行命令：

    client unblock client_id
    

要暂时挂起当前连接到Redis服务器的每个客户端，可以使用以下`client pause`命令。这在需要以受控方式更改Redis设置的情况下很有用。例如，如果要将一个副本提升为主实例，则可以事先暂停每个客户端，以便升级副本并使客户端作为新的主实例连接到该副本，而不会丢失任何写操作。

该`client pause`命令要求您指定要挂起客户端的时间（以毫秒为单位）。下面的示例将所有客户端暂停一秒钟：

    client pause 1000
    

该`client kill`语法允许您基于许多不同的过滤器关闭单个连接或一组特定的连接。语法如下所示：

    client kill filter_1 value_1 ... filter_n value_n
    

在Redis 2.8.12和更高版本中，可以使用以下过滤器：

*   `addr`：允许您从指定的IP地址和端口关闭客户端连接
*   `client-id`：允许您根据其唯一ID字段关闭客户端连接
*   `type`：关闭一个给定类型，它可以是每一个客户端`normal`，`master`，`slave`，或`pubsub`
*   `skipme`：此过滤器的值选项为`yes`和`no`：
    *   如果`no`指定了if ，则调用该`client kill`命令的客户端不会被跳过，并且如果其他过滤器应用到该客户端，它将被杀死
    *   如果`yes`指定，则将跳过运行该命令的客户端，而kill命令将对该客户端无效。`skipme`始终`yes`默认为

结论
--

本指南详细介绍了用于管理Redis客户端和副本的许多命令。如果您想在本指南中概述其他相关的命令，参数或过程，请在下面的评论中提出疑问或提出建议。

有关Redis命令的更多信息，请参阅关于[如何管理Redis数据库的](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8redis%E6%95%B0%E6%8D%AE%E5%BA%93)系列教程。