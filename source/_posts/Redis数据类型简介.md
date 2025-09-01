---
title: Redis数据类型简介
id: 1345
date: 2024-10-31 22:01:51
author: daichangya
excerpt: "Redis数据类型和抽象简介Redis不是_简单的_键值存储，它实际上是一个_数据结构服务器_，支持不同类型的值。这意味着在传统键值存储中，您将字符串键与字符串值相关联，而在Redis中，该值不仅限于简单的字符串，还可以容纳更复杂的数据结构。以下是Redis支持的所有数据结构的列表，本教程将分别进行"
permalink: /archives/redis%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B%E7%AE%80%E4%BB%8B/
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

Redis数据类型简介
=========================================================================

Redis不是_简单的_键值存储，它实际上是一个_数据结构服务器_，支持不同类型的值。这意味着在传统键值存储中，您将字符串键与字符串值相关联，而在Redis中，该值不仅限于简单的字符串，还可以容纳更复杂的数据结构。以下是Redis支持的所有数据结构的列表，本教程将分别进行介绍：

*   二进制安全字符串。
*   列表：根据插入顺序排序的字符串元素的集合。它们基本上是_链表_。
*   集：唯一，未排序的字符串元素的集合。
*   类似于Sets的排序集合，但每个字符串元素都与一个称为_score_的浮点值相关联。元素总是按它们的分数排序，因此与Sets不同，可以检索一系列元素（例如，您可能会问：给我前10名或后10名）。
*   哈希，是由与值关联的字段组成的映射。字段和值都是字符串。这与Ruby或Python哈希非常相似。
*   位数组（或简称为位图）：可以使用特殊命令像位数组一样处理字符串值：您可以设置和清除单个位，计数所有设置为1的位，找到第一个设置或未设置的位，等等。
*   HyperLogLogs：这是一个概率数据结构，用于估计集合的基数。别害怕，它比看起来更简单...请参阅本教程的HyperLogLog部分。
*   流：提供抽象日志数据类型的类地图项的仅追加集合。在“ [Redis流简介”中对](/topics/streams-intro)它们进行了深入 [介绍](/topics/streams-intro)。

从[命令参考中](/commands)掌握这些数据类型的工作方式以及使用什么来解决给定问题并不总是那么容易，因此，本文档是有关Redis数据类型及其最常见模式的速成课程。

对于所有示例，我们将使用该`redis-cli`实用程序（一个简单但方便的命令行实用程序）对Redis服务器发出命令。

[\*](#redis-keys)Redis keys
---------------------------

Redis密钥是二进制安全的，这意味着您可以使用任何二进制序列作为密钥，从“ foo”之类的字符串到JPEG文件的内容。空字符串也是有效的键。

有关密钥的其他一些规则：

*   太长的键不是一个好主意。例如，1024字节的密钥不仅是内存方面的问题，也是一个坏主意，而且因为在数据集中查找密钥可能需要进行一些代价高昂的密钥比较。即使手头的任务是匹配一个大值的存在，对它进行散列（例如使用SHA1）也是一个更好的主意，尤其是从内存和带宽的角度来看。
*   非常短的键通常不是一个好主意。如果您可以改写“ user：1000：followers”，那么将“ u1000flw”写为密钥毫无意义。与键对象本身和值对象使用的空间相比，后者更具可读性，并且添加的空间较小。虽然短键显然会消耗更少的内存，但您的工作是找到合适的平衡。
*   尝试坚持使用架构。例如，“ object-type：id”是一个好主意，例如“ user：1000”。点或破折号通常用于多字字段，例如“ comment：1234：reply.to”或“ comment：1234：reply-to”中。
*   允许的最大密钥大小为512 MB。

[\*](#redis-strings)Redis Strings
---------------------------------

Redis字符串类型是您可以与Redis键关联的最简单的值类型。它是Memcached中唯一的数据类型，因此对于新手来说，在Redis中使用它也是很自然的。

由于Redis键是字符串，因此当我们也使用字符串类型作为值时，我们会将一个字符串映射到另一个字符串。字符串数据类型对于许多用例很有用，例如缓存HTML片段或页面。

让我们使用来处理字符串类型`redis-cli`（所有示例将`redis-cli`在本教程中通过来执行）。

    > set mykey somevalue
    OK
    > get mykey
    "somevalue"
    

如您所见，使用[SET](/commands/set)和[GET](/commands/get)命令是我们设置和检索字符串值的方式。请注意，即使键已与非字符串值相关联，[SET](/commands/set)仍将替换已存储在键中的任何现有值。因此[SET](/commands/set)执行分配。

值可以是每种类型的字符串（包括二进制数据），例如，您可以在值内存储jpeg图像。值不能大于512 MB。

该[SET](/commands/set)命令有有趣的选项，这是作为附加参数。例如，如果密钥已经存在，我可能会要求[SET](/commands/set)失败，或者相反，只有密钥已经存在时，它才会成功：

    > set mykey newval nx
    (nil)
    > set mykey newval xx
    OK
    

即使字符串是Redis的基本值，您也可以使用它们执行一些有趣的操作。例如，一个是原子增量：

    > set counter 100
    OK
    > incr counter
    (integer) 101
    > incr counter
    (integer) 102
    > incrby counter 50
    (integer) 152
    

的[INCR](/commands/incr)命令由一个解析字符串值作为一个整数，它的增量，并最终将获得的值作为新的值。还有其他类似的命令，例如[INCRBY](/commands/incrby)， [DECR](/commands/decr)和[DECRBY](/commands/decrby)。在内部，它始终是相同的命令，其执行方式略有不同。

INCR是原子的意味着什么？即使使用相同密钥发出INCR的多个客户也永远不会进入竞争状态。例如，客户端1不会同时读取“ 10”，客户端2会同时读取“ 10”，都递增为11，并将新值设置为11。最终值将始终为12，而在所有其他客户端未同时执行命令时执行增量设置操作。

有许多用于操作字符串的命令。例如，[GETSET](/commands/getset)命令将键设置为新值，并返回旧值作为结果。例如，如果您的系统在 每次网站接收新访客时使用[INCR](/commands/incr)递增Redis密钥，则可以使用此命令。您可能希望每小时收集一次此信息，而又不会丢失任何增量。您可以[GETSET](/commands/getset)键，[为其](/commands/getset)分配新值“ 0”，然后回读旧值。

在单个命令中设置或检索多个键的值的功能对于减少延迟也很有用。因此，有[MSET](/commands/mset)和[MGET](/commands/mget)命令：

    > mset a 10 b 20 c 30
    OK
    > mget a b c
    1) "10"
    2) "20"
    3) "30"
    

使用[MGET时](/commands/mget)，Redis返回一个值数组。

[\*](#altering-and-querying-the-key-space)Altering and querying the key space
-----------------------------------------------------------------------------

有些命令未在特定类型上定义，但是在与键的空间进行交互时很有用，因此可以与任何类型的键一起使用。

例如，[EXISTS](/commands/exists)命令返回1或0表示数据库中是否存在给定的键，而[DEL](/commands/del)命令则删除键和关联的值（无论该值是什么）。

    > set mykey hello
    OK
    > exists mykey
    (integer) 1
    > del mykey
    (integer) 1
    > exists mykey
    (integer) 0
    

从示例中，您还可以看到[DEL](/commands/del)本身如何返回1或0，具体取决于密钥是否已删除（存在）（不存在具有该名称的此类密钥）。

有许多与密钥空间相关的命令，但是以上两个命令与[TYPE](/commands/type)命令一起是必不可少的，[TYPE](/commands/type)命令返回存储在指定密钥处的值的类型：

    > set mykey x
    OK
    > type mykey
    string
    > del mykey
    (integer) 1
    > type mykey
    none
    

[\*](#redis-expires-keys-with-limited-time-to-live)Redis expires: keys with limited time to live
------------------------------------------------------------------------------------------------

在继续使用更复杂的数据结构之前，我们需要讨论另一个功能，该功能不管值类型如何都可以工作，并且称为**Redis expires**。基本上，您可以为密钥设置一个超时时间，这是有限的生存时间。生存时间过去后，该密钥将自动销毁，就像用户使用该密钥调用[DEL](/commands/del)命令一样。

有关Redis的一些快速信息将过期：

*   可以使用秒或毫秒精度进行设置。
*   但是，到期时间分辨率始终为1毫秒。
*   有关过期的信息被复制并保留在磁盘上，实际上Redis服务器保持停止状态的时间已经过去（这意味着Redis保存了密钥过期的日期）。

设置过期时间很简单：

    > set key some-value
    OK
    > expire key 5
    (integer) 1
    > get key (immediately)
    "some-value"
    > get key (after some time)
    (nil)
    

由于第二次呼叫延迟了5秒钟以上，因此在两次[GET](/commands/get)呼叫之间密钥消失了。在上面的示例中，我们使用[EXPIRE](/commands/expire)来设置过期时间（也可以使用它来为已经具有密钥的密钥设置不同的过期时间，例如可以使用[PERSIST](/commands/persist)来删除过期并使密钥永久持久化）。但是，我们也可以使用其他Redis命令来创建具有过期密钥。例如，使用[SET](/commands/set)选项：

    > set key 100 ex 10
    OK
    > ttl key
    (integer) 9
    

上面的示例使用一个字符串值设置一个密钥，该密钥`100`的到期时间为十秒钟。稍后调用[TTL](/commands/ttl)命令以检查密钥的剩余生存时间。

为了设置和检查以毫秒为单位到期，检查[PEXPIRE](/commands/pexpire)和[热释光](/commands/pttl)的命令，以及完整列表[SET](/commands/set)选项。

[\*](#redis-lists)Redis Lists
-----------------------------

为了解释List数据类型，最好从理论上入手，因为_List_一词经常被信息技术人员以不正当的方式使用。例如，“ Python列表”并不是名称（链接列表）所建议的，而是数组（在Ruby中，相同的数据类型实际上称为数组）。

从非常普遍的角度来看，列表只是一系列有序元素：10,20,1,2,3是一个列表。但是，使用Array实现的List的属性与使用_Linked List_实现的List的属性非常不同 。

Redis列表是通过链接列表实现的。这意味着即使您在列表中有数百万个元素，在列表的开头或结尾添加新元素的操作也会_在固定时间内_执行。使用[LPUSH](/commands/lpush)命令将新元素添加到具有10个元素的列表的开头的速度与将元素添加到具有1000万个元素的列表的开头的速度相同。

缺点是什么？在使用Array实现的列表中，_按索引_访问元素_的_速度非常快（恒定时间索引访问），而在通过链接列表实现的列表中访问速度不是那么快（其中操作需要的工作量与所访问元素的索引成比例）。

Redis列表是通过链接列表实现的，因为对于数据库系统而言，至关重要的是能够以非常快的方式将元素添加到很长的列表中。稍后您将看到，另一个强大的优势是Redis列表可以在恒定的时间内以恒定的长度获取。

当快速访问大量元素的中间位置很重要时，可以使用另一种称为排序集的数据结构。排序的集将在本教程的后面部分介绍。

[\*](#first-steps-with-redis-lists)First steps with Redis Lists
---------------------------------------------------------------

所述[LPUSH](/commands/lpush)命令将一个新元素到一个列表，在左侧（在头部），而[RPUSH](/commands/rpush)命令将一个新元素到一个列表，在右侧（在尾部）。最后， [LRANGE](/commands/lrange)命令从列表中提取元素范围：

    > rpush mylist A
    (integer) 1
    > rpush mylist B
    (integer) 2
    > lpush mylist first
    (integer) 3
    > lrange mylist 0 -1
    1) "first"
    2) "A"
    3) "B"
    

请注意，[LRANGE](/commands/lrange)需要两个索引，要返回的范围的第一个和最后一个元素。两个索引都可以为负，告诉Redis从末尾开始计数：因此-1是列表的最后一个元素，-2是列表的倒数第二个元素，依此类推。

如您所见，[RPUSH](/commands/rpush)在列表的右侧附加了元素，而最后的[LPUSH](/commands/lpush)在列表的左侧附加了元素。

这两个命令都是_可变参数命令_，这意味着您可以在单个调用中随意将多个元素推入列表中：

    > rpush mylist 1 2 3 4 5 "foo bar"
    (integer) 9
    > lrange mylist 0 -1
    1) "first"
    2) "A"
    3) "B"
    4) "1"
    5) "2"
    6) "3"
    7) "4"
    8) "5"
    9) "foo bar"
    

在Redis列表上定义的一项重要操作是_弹出元素_的能力。弹出元素是同时从列表中检索元素并将其从列表中删除的操作。您可以从左侧和右侧弹出元素，类似于在列表两边推送元素的方式：

    > rpush mylist a b c
    (integer) 3
    > rpop mylist
    "c"
    > rpop mylist
    "b"
    > rpop mylist
    "a"
    

我们添加了三个元素并弹出了三个元素，因此在此命令序列的末尾，列表为空，没有其他要弹出的元素。如果我们尝试弹出另一个元素，则会得到以下结果：

    > rpop mylist
    (nil)
    

Redis返回NULL值，以指示列表中没有元素。

[\*](#common-use-cases-for-lists)Common use cases for lists
-----------------------------------------------------------

列表对于许多任务很有用，以下是两个非常有代表性的用例：

*   记住用户发布到社交网络上的最新更新。
*   使用生产者将项目推送到列表中的消费者与生产者模式进行流程之间的通信，而消费者（通常是_worker_）消耗这些项目和已执行的动作。Redis具有特殊的列表命令，以使此用例更加可靠和高效。

例如，流行的Ruby库[resque](https://github.com/resque/resque)和 [sidekiq](https://github.com/mperham/sidekiq)都在[后台](https://github.com/mperham/sidekiq)使用Redis列表，以实现后台作业。

流行的Twitter社交网络[将](http://www.infoq.com/presentations/Real-Time-Delivery-Twitter) 用户发布[的最新推文](http://www.infoq.com/presentations/Real-Time-Delivery-Twitter)放入Redis列表中。

为了逐步描述一个常见的用例，假设您的主页显示了在照片共享社交网络中发布的最新照片，并且您想加快访问速度。

*   每次用户发布新照片时，我们都会使用[LPUSH](/commands/lpush)将其ID添加到列表中。
*   当用户访问主页时，我们`LRANGE 0 9`为了获取最新发布的10个项目。

[\*](#capped-lists)Capped lists
-------------------------------

在许多用例中，我们只想使用列表来存储_最新项目_，无论它们是什么：社交网络更新，日志或其他任何内容。

Redis允许我们使用列表作为上限集合，仅使用[LTRIM](/commands/ltrim)命令记住最新的N个项目并丢弃所有最旧的项目。

的[LTRIM](/commands/ltrim)命令类似于[LRANGE](/commands/lrange)，但是**，而不是显示元件的规定的范围内**将其设置在该范围作为新的列表值。给定范围之外的所有元素都将被删除。

一个例子将使其更加清楚：

    > rpush mylist 1 2 3 4 5
    (integer) 5
    > ltrim mylist 0 2
    OK
    > lrange mylist 0 -1
    1) "1"
    2) "2"
    3) "3"
    

上面的[LTRIM](/commands/ltrim)命令告诉Redis仅从索引0到2列出列表元素，其他所有内容都将被丢弃。这允许一个非常简单但有用的模式：一起执行List推操作+ List修剪操作，以便添加新元素并丢弃超出限制的元素：

    LPUSH mylist <some element>
    LTRIM mylist 0 999
    

上面的组合添加了一个新元素，并且仅将1000个最新元素纳入列表。使用[LRANGE，](/commands/lrange)您可以访问最重要的项目，而无需记住非常旧的数据。

注意：虽然[LRANGE](/commands/lrange)从技术上讲是O（N）命令，但朝列表的开头或[结尾](/commands/lrange)访问较小范围是恒定时间操作。

[\*](#blocking-operations-on-lists)Blocking operations on lists
---------------------------------------------------------------

列表具有一项特殊功能，使其适合于实现队列，并且通常用作进程间通信系统的构建块：阻止操作。

想象一下，您想通过一个流程将项目推入列表，然后使用不同的流程来对这些项目进行某种工作。这是通常的生产者/使用者设置，可以通过以下简单方式实现：

*   为了将项目推送到列表中，生产者调用[LPUSH](/commands/lpush)。
*   为了从列表中提取/处理项目，消费者调用[RPOP](/commands/rpop)。

但是，有时列表可能为空，没有任何要处理的内容，因此[RPOP](/commands/rpop)仅返回NULL。在这种情况下，消费者被迫等待一段时间，然后使用[RPOP](/commands/rpop)重试。这称为_轮询_，在这种情况下不是一个好主意，因为它有几个缺点：

1.  强制Redis和客户端处理无用的命令（列表为空时的所有请求将无法完成任何实际工作，它们只会返回NULL）。
2.  由于工作人员在收到NULL之后会等待一段时间，因此会增加项目处理的延迟。为了使延迟更小，我们可以在[两次](/commands/rpop)调用[RPOP](/commands/rpop)之间等待的时间更少，从而扩大了问题编号1，即对Redis的调用更加无用。

所以，所谓的Redis命令工具[BRPOP](/commands/brpop)和[BLPOP](/commands/blpop)它们的版本[RPOP](/commands/rpop)和[LPOP](/commands/lpop)能够阻止如果列表是空的：他们将回到只有当新的元素添加到列表中的来电者，或在用户指定的超时到达。

这是我们可以在worker中使用的[BRPOP](/commands/brpop)调用的示例：

    > brpop tasks 5
    1) "tasks"
    2) "do_something"
    

这意味着：“等待列表中的元素`tasks`，但如果5秒钟后没有可用元素，则返回”。

请注意，您可以将0用作超时来永远等待元素，还可以指定多个列表，而不仅仅是一个列表，以便同时等待多个列表，并在第一个列表收到一个元素时得到通知。

有关[BRPOP的](/commands/brpop)几点注意[事项](/commands/brpop)：

1.  客户端以有序方式提供服务：第一个阻塞等待列表的客户端，在某个元素被其他客户端推送时首先提供服务，依此类推。
2.  返回值与[RPOP](/commands/rpop)相比有所不同：它是一个包含两个元素的数组，因为它还包含键的名称，因为[BRPOP](/commands/brpop)和[BLPOP](/commands/blpop)能够阻止等待来自多个列表的元素。
3.  如果达到超时，则返回NULL。

关于列表和阻止操作，您应该了解更多信息。我们建议您阅读以下内容：

*   使用[RPOPLPUSH](/commands/rpoplpush)可以构建更安全的队列或轮换队列。
*   该命令还有一个阻塞变体，称为[BRPOPLPUSH](/commands/brpoplpush)。

[\*](#automatic-creation-and-removal-of-keys)Automatic creation and removal of keys
-----------------------------------------------------------------------------------

到目前为止，在我们的示例中，我们无需在推入元素之前创建空列表，也无需在内部不再包含元素时删除空列表。Redis的责任是在列表为空时删除键，或者在键不存在并且我们试图向其添加元素（例如，使用[LPUSH）时](/commands/lpush)创建一个空列表。

这不是特定于列表的，它适用于由多个元素组成的所有Redis数据类型-流，集合，排序集合和哈希。

基本上，我们可以用三个规则来总结行为：

1.  当我们将元素添加到聚合数据类型时，如果目标键不存在，则在添加元素之前会创建一个空的聚合数据类型。
2.  当我们从聚合数据类型中删除元素时，如果该值保持为空，则键将自动销毁。流数据类型是此规则的唯一例外。
3.  调用带有空键的只读命令（例如[LLEN](/commands/llen)（返回列表的长度））或写命令删除元素，总会产生与键保持空的聚合类型相同的结果。命令希望找到。

规则1的示例：

    > del mylist
    (integer) 1
    > lpush mylist 1 2 3
    (integer) 3
    

但是，如果密钥存在，我们将无法对错误的类型执行操作：

    > set foo bar
    OK
    > lpush foo 1 2 3
    (error) WRONGTYPE Operation against a key holding the wrong kind of value
    > type foo
    string
    

规则2的示例：

    > lpush mylist 1 2 3
    (integer) 3
    > exists mylist
    (integer) 1
    > lpop mylist
    "3"
    > lpop mylist
    "2"
    > lpop mylist
    "1"
    > exists mylist
    (integer) 0
    

弹出所有元素后，键不再存在。

规则3的示例：

    > del mylist
    (integer) 0
    > llen mylist
    (integer) 0
    > lpop mylist
    (nil)
    

[\*](#redis-hashes)Redis Hashes
-------------------------------

Redis散列与字段值对看起来完全一样，可能是人们期望的“散列”外观：

    > hmset user:1000 username antirez birthyear 1977 verified 1
    OK
    > hget user:1000 username
    "antirez"
    > hget user:1000 birthyear
    "1977"
    > hgetall user:1000
    1) "username"
    2) "antirez"
    3) "birthyear"
    4) "1977"
    5) "verified"
    6) "1"
    

尽管哈希可以方便地表示_对象_，但是实际上可以放入哈希中的字段数没有实际限制（可用内存除外），因此您可以在应用程序内部以多种不同方式使用哈希。

[HMSET](/commands/hmset)命令设置哈希的多个字段，而[HGET](/commands/hget)检索单个字段。[HMGET](/commands/hmget)类似于[HGET](/commands/hget)但返回值的数组：

    > hmget user:1000 username birthyear no-such-field
    1) "antirez"
    2) "1977"
    3) (nil)
    

有些命令也可以对单个字段执行操作，例如[HINCRBY](/commands/hincrby)：

    > hincrby user:1000 birthyear 10
    (integer) 1987
    > hincrby user:1000 birthyear 10
    (integer) 1997
    

您可以[在文档中](http://redis.io/commands#hash)找到[哈希命令](http://redis.io/commands#hash)的[完整列表](http://redis.io/commands#hash)。

值得注意的是，小哈希（即，一些具有较小值的元素）以特殊方式在内存中进行编码，从而使它们具有很高的内存效率。

[\*](#redis-sets)Redis Sets
---------------------------

Redis集是字符串的无序集合。该 [SADD](/commands/sadd)命令添加新的元素，一组。还可以对集合进行许多其他操作，例如测试给定元素是否已存在，执行多个集合之间的交集，并集或求差等等。

    > sadd myset 1 2 3
    (integer) 3
    > smembers myset
    1. 3
    2. 1
    3. 2
    

在这里，我在集合中添加了三个元素，并告诉Redis返回所有元素。如您所见，它们没有排序-Redis可以在每次调用时随意以任何顺序返回元素，因为与用户之间没有关于元素顺序的约定。

Redis具有用于测试成员资格的命令。例如，检查元素是否存在：

    > sismember myset 3
    (integer) 1
    > sismember myset 30
    (integer) 0
    

“ 3”是集合的成员，而“ 30”不是集合的成员。

集合非常适合表示对象之间的关系。例如，我们可以轻松地使用集合来实现标签。

对这个问题进行建模的一种简单方法是为我们要标记的每个对象设置一个集合。该集合包含与对象关联的标签的ID。

一个例证是标记新闻文章。如果商品ID 1000带有标签1、2、5和77进行标记，则集合可以将这些标签ID与新闻项相关联：

    > sadd news:1000:tags 1 2 5 77
    (integer) 4
    

我们可能还需要逆关系：用给定标签标记的所有新闻的列表：

    > sadd tag:1:news 1000
    (integer) 1
    > sadd tag:2:news 1000
    (integer) 1
    > sadd tag:5:news 1000
    (integer) 1
    > sadd tag:77:news 1000
    (integer) 1
    

要获取给定对象的所有标签很简单：

    > smembers news:1000:tags
    1. 5
    2. 1
    3. 77
    4. 2
    

注意：在示例中，我们假设您具有另一个数据结构，例如Redis哈希，它将标签ID映射到标签名称。

还有其他一些非常简单的操作，使用正确的Redis命令仍然很容易实现。例如，我们可能需要包含标签1、2、10和27的所有对象的列表。我们可以使用[SINTER](/commands/sinter)命令执行此操作，该命令执行不同集合之间的交集。我们可以用：

    > sinter tag:1:news tag:2:news tag:10:news tag:27:news
    ... results here ...
    

除了交集之外，您还可以执行并集，求差，提取随机元素等等。

提取元素的命令称为[SPOP](/commands/spop)，对于建模某些问题非常方便。例如，为了实现基于Web的扑克游戏，您可能需要用一组来代表您的套牌。假设我们对（C）lubs，（D）钻石，（H）耳钉，（S）垫使用一个单字符前缀：

    >  sadd deck C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 CJ CQ CK
       D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 DJ DQ DK H1 H2 H3
       H4 H5 H6 H7 H8 H9 H10 HJ HQ HK S1 S2 S3 S4 S5 S6
       S7 S8 S9 S10 SJ SQ SK
       (integer) 52
    

现在我们要为每个玩家提供5张卡片。该[SPOP](/commands/spop)命令删除一个随机元素，将其返回到客户端，所以在这种情况下完美运行。

但是，如果我们直接在甲板上对其进行称呼，那么在游戏的下一场比赛中，我们将需要再次填充纸牌，这可能并不理想。因此，首先，我们可以将存储在`deck`密钥中的集合复制到`game:1:deck`密钥中。

这可以使用[SUNIONSTORE](/commands/sunionstore)来完成，[SUNIONSTORE](/commands/sunionstore)通常执行多个集合之间的联合，并将结果存储到另一个集合中。但是，由于单个集合的并集本身，我可以使用以下命令复制我的卡组：

    > sunionstore game:1:deck deck
    (integer) 52
    

现在，我准备为第一位玩家提供五张牌：

    > spop game:1:deck
    "C6"
    > spop game:1:deck
    "CQ"
    > spop game:1:deck
    "D1"
    > spop game:1:deck
    "CJ"
    > spop game:1:deck
    "SJ"
    

一副千斤顶，不是很好...

现在是引入set命令的好时机，该命令提供集合中元素的数量。 在集合理论的上下文中，这通常称为_集合_的_基数_，因此Redis命令称为[SCARD](/commands/scard)。

    > scard game:1:deck
    (integer) 47
    

数学原理：52-5 = 47。

当您只需要获取随机元素而不将其从集合中删除时，可以使用适合该任务的[SRANDMEMBER](/commands/srandmember)命令。它还具有返回重复元素和非重复元素的功能。

[\*](#redis-sorted-sets)Redis Sorted sets
-----------------------------------------

排序集是一种数据类型，类似于集合和哈希之间的混合。像集合一样，排序集合由唯一的，非重复的字符串元素组成，因此从某种意义上说，排序集合也是一个集合。

但是，虽然集内的元素没有排序，但排序后的集合中的每个元素都与一个称为_得分_的浮点值相关联 （这就是为什么该类型也类似于哈希的原因，因为每个元素都映射到一个值）。

此外，已排序集合中的元素是按_顺序进行的_（因此，它们不是应请求而排序的，顺序是用于表示已排序集合的数据结构的特殊性）。它们按照以下规则排序：

*   如果A和B是两个分数不同的元素，则如果A.score是> B.score，则A>B。
*   如果A和B的分数完全相同，那么如果A字符串在字典上大于B字符串，则A>B。A和B字符串不能相等，因为排序集仅具有唯一元素。

让我们从一个简单的示例开始，添加一些选定的黑客名称作为排序的集合元素，并以其出生年份为“得分”。

    > zadd hackers 1940 "Alan Kay"
    (integer) 1
    > zadd hackers 1957 "Sophie Wilson"
    (integer) 1
    > zadd hackers 1953 "Richard Stallman"
    (integer) 1
    > zadd hackers 1949 "Anita Borg"
    (integer) 1
    > zadd hackers 1965 "Yukihiro Matsumoto"
    (integer) 1
    > zadd hackers 1914 "Hedy Lamarr"
    (integer) 1
    > zadd hackers 1916 "Claude Shannon"
    (integer) 1
    > zadd hackers 1969 "Linus Torvalds"
    (integer) 1
    > zadd hackers 1912 "Alan Turing"
    (integer) 1
    

如您所见，[ZADD](/commands/zadd)与[SADD](/commands/sadd)相似，但是使用一个额外的参数（放置在要添加的元素之前）作为得分。 [ZADD](/commands/zadd)也是可变参数，因此即使上面的示例中未使用它，您也可以自由指定多个得分-值对。

使用排序集，返回按其出生年份排序的黑客列表很简单，因为实际上_他们已经被排序了_。

实施说明：排序集是通过包含跳过列表和哈希表的双端口数据结构实现的，因此，每次添加元素时，Redis都会执行O（log（N））操作。很好，但是当我们要求排序元素时，Redis根本不需要做任何工作，它已经全部排序了：

    > zrange hackers 0 -1
    1) "Alan Turing"
    2) "Hedy Lamarr"
    3) "Claude Shannon"
    4) "Alan Kay"
    5) "Anita Borg"
    6) "Richard Stallman"
    7) "Sophie Wilson"
    8) "Yukihiro Matsumoto"
    9) "Linus Torvalds"
    

注意：0和-1表示从元素索引0到最后一个元素（-1的工作方式与[LRANGE](/commands/lrange)命令的情况[相同](/commands/lrange)）。

如果我想按相反的顺序订购（最小到最大）怎么办？使用[ZREVRANGE](/commands/zrevrange)而不是[ZRANGE](/commands/zrange)：

    > zrevrange hackers 0 -1
    1) "Linus Torvalds"
    2) "Yukihiro Matsumoto"
    3) "Sophie Wilson"
    4) "Richard Stallman"
    5) "Anita Borg"
    6) "Alan Kay"
    7) "Claude Shannon"
    8) "Hedy Lamarr"
    9) "Alan Turing"
    

也可以使用以下`WITHSCORES`参数返回分数：

    > zrange hackers 0 -1 withscores
    1) "Alan Turing"
    2) "1912"
    3) "Hedy Lamarr"
    4) "1914"
    5) "Claude Shannon"
    6) "1916"
    7) "Alan Kay"
    8) "1940"
    9) "Anita Borg"
    10) "1949"
    11) "Richard Stallman"
    12) "1953"
    13) "Sophie Wilson"
    14) "1957"
    15) "Yukihiro Matsumoto"
    16) "1965"
    17) "Linus Torvalds"
    18) "1969"
    

[\*](#operating-on-ranges)Operating on ranges
---------------------------------------------

排序集比这更强大。它们可以在范围内操作。让我们获取所有在1950年（含）之前出生的人。我们使用[ZRANGEBYSCORE](/commands/zrangebyscore)命令来做到这一点：

    > zrangebyscore hackers -inf 1950
    1) "Alan Turing"
    2) "Hedy Lamarr"
    3) "Claude Shannon"
    4) "Alan Kay"
    5) "Anita Borg"
    

我们要求Redis返回分数在负无穷大和1950之间的所有元素（包括两个极端）。

也可以删除元素范围。让我们从排序集中删除所有1940年至1960年之间出生的黑客：

    > zremrangebyscore hackers 1940 1960
    (integer) 4
    

[ZREMRANGEBYSCORE](/commands/zremrangebyscore)可能不是最好的命令名称，但是它可能非常有用，并返回已删除元素的数量。

为排序的集合元素定义的另一个极其有用的操作是get-rank操作。可以问一个元素在有序元素集合中的位置是什么。

    > zrank hackers "Anita Borg"
    (integer) 4
    

该[ZREVRANK](/commands/zrevrank)命令也可以为了获得军衔，考虑的要素排序的下降方式。

[\*](#lexicographical-scores)Lexicographical scores
---------------------------------------------------

在最新版本的Redis 2.8中，引入了一项新功能，该功能允许按字典顺序获取范围，假设已排序集中的元素都以相同的相同分数插入（将元素与C `memcmp`函数进行比较 ，因此可以确保没有排序规则） ，并且每个Redis实例将以相同的输出进行回复）。

用于按字典顺序操作的主要命令是[ZRANGEBYLEX](/commands/zrangebylex)， [ZREVRANGEBYLEX](/commands/zrevrangebylex)，[ZREMRANGEBYLEX](/commands/zremrangebylex)和[ZLEXCOUNT](/commands/zlexcount)。

例如，让我们再次添加我们的著名黑客列表，但是这次对所有元素使用零分：

    > zadd hackers 0 "Alan Kay" 0 "Sophie Wilson" 0 "Richard Stallman" 0
      "Anita Borg" 0 "Yukihiro Matsumoto" 0 "Hedy Lamarr" 0 "Claude Shannon"
      0 "Linus Torvalds" 0 "Alan Turing"
    

由于排序集的排序规则，它们已经按字典顺序排序：

    > zrange hackers 0 -1
    1) "Alan Kay"
    2) "Alan Turing"
    3) "Anita Borg"
    4) "Claude Shannon"
    5) "Hedy Lamarr"
    6) "Linus Torvalds"
    7) "Richard Stallman"
    8) "Sophie Wilson"
    9) "Yukihiro Matsumoto"
    

使用[ZRANGEBYLEX](/commands/zrangebylex)我们可以要求词典范围：

    > zrangebylex hackers [B [P
    1) "Claude Shannon"
    2) "Hedy Lamarr"
    3) "Linus Torvalds"
    

范围可以是包含（inclusive）或排除（exclusive）（取决于第一个字符），字符串无限和负无限分别用`+`和`-`字符串指定。有关更多信息，请参见文档。

此功能非常重要，因为它允许我们将排序后的集合用作通用索引。例如，如果要通过128位无符号整数参数索引元素，则只需将元素添加到具有相同分数（例如0）但具有由**128**个字节组成的16字节前缀的排序集中**大尾数中的位数**。由于big endian中的数字实际上按数字顺序也按字典顺序（以原始字节顺序）排序，因此您可以要求128位空间中的范围，并获得丢弃前缀的元素值。

如果要在更严重的演示环境中查看该功能，请检查[Redis自动完成演示](http://autocomplete.redis.io)。

[\*](#updating-the-score-leader-boards)Updating the score: leader boards
------------------------------------------------------------------------

在切换到下一个主题之前，请只对已排序集做最后的说明。排序集的分数可以随时更新。只需对已包含在排序集中的元素调用[ZADD](/commands/zadd)，将以O（log（N））时间复杂度更新其得分（和位置）。这样，当有大量更新时，排序集是合适的。

由于这种特性，常见的用例是排行榜。典型的应用是Facebook游戏，您可以将按高分对用户进行排序的能力与获得排名的操作结合起来，以显示前N名的用户以及排行榜中的用户排名（例如，“您是这里的＃4932最佳成绩”）。

[\*](#bitmaps)Bitmaps
---------------------

位图不是实际的数据类型，而是在String类型上定义的一组面向位的操作。由于字符串是二进制安全Blob，并且最大长度为512 MB，因此它们适合设置多达2 32个不同的位。

位操作分为两类：固定时间的单个位操作（如将一个位设置为1或0或获取其值），以及对位组的操作，例如计算给定位范围内设置的位的数量（例如，人口计数）。

位图的最大优点之一是，它们在存储信息时通常可以节省大量空间。例如，在以增量用户ID表示不同用户的系统中，仅使用512 MB内存就可以记住40亿用户的一位信息（例如，知道用户是否要接收新闻通讯）。

使用[SETBIT](/commands/setbit)和[GETBIT](/commands/getbit)命令设置和检索位：

    > setbit key 10 1
    (integer) 1
    > getbit key 10
    (integer) 1
    > getbit key 11
    (integer) 0
    

所述[SETBIT](/commands/setbit)命令采用作为第一个参数的比特数，和作为第二个参数的值以设置所述位，其为1或0的命令自动放大字符串，如果寻址位是当前字符串长度之外。

[GETBIT](/commands/getbit)只是返回指定索引处的位的值。超出范围的位（寻址超出存储在目标键中的字符串长度的位）始终被视为零。

在位组上有三个命令：

1.  [BITOP](/commands/bitop)在不同的字符串之间执行按位运算。提供的运算为AND，OR，XOR和NOT。
2.  [BITCOUNT](/commands/bitcount)执行填充计数，报告设置为1的位数。
3.  [BITPOS](/commands/bitpos)查找指定值为0或1的第一位。

无论[BITPOS](/commands/bitpos)和[比特计数](/commands/bitcount)能够与字符串的字节范围进行操作，而不是该字符串的整个长度运行。以下是[BITCOUNT](/commands/bitcount)调用的一个简单示例：

    > setbit key 0 1
    (integer) 0
    > setbit key 100 1
    (integer) 0
    > bitcount key
    (integer) 2
    

位图的常见用例是：

*   各种实时分析。
*   存储与对象ID相关的空间高效但高性能的布尔信息。

例如，假设您想知道网站用户每天访问量最长的时间。您从零开始计算天数，即从您公开网站的那一天开始，并在用户每次访问该网站时对[SETBIT进行](/commands/setbit)设置。作为位索引，您只需花费当前的unix时间，减去初始偏移量，然后除以一天中的秒数（通常为3600 \* 24）。

这样，对于每个用户，您都有一个小的字符串，其中包含每天的访问信息。使用[BITCOUNT](/commands/bitcount)，可以轻松获得给定用户访问网站的天数，而只需几个[BITPOS](/commands/bitpos)调用，或者仅获取和分析客户端的位图，就可以轻松计算最长的连胜记录。

位图很容易分成多个键，例如，为了分片数据集，并且因为通常最好避免使用大键。要在不同的密钥上拆分位图，而不是将所有位都设置为密钥，一个简单的策略就是为每个密钥存储M位，并使用来获取密钥名称，使用来获取`bit-number/M`第N位`bit-number MOD M`。

[\*](#hyperloglogs)HyperLogLogs
-------------------------------

HyperLogLog是一种概率数据结构，用于对唯一事物进行计数（从技术上讲，这是指估计集合的基数）。通常，对唯一项目进行计数需要使用与要计数的项目数量成比例的内存量，因为您需要记住过去已经看到的元素，以避免多次对其进行计数。但是，有一组算法会以内存为代价来交换精度：您最终会得到带有标准误差的估计量度，在Redis实现的情况下，该误差小于1％。这种算法的神奇之处在于，您不再需要使用与所计数项目数量成正比的内存量，而是可以使用恒定数量的内存！在最坏的情况下为12k字节，如果您的HyperLogLog（从现在开始将它们称为HLL）看到的元素很少，则少得多。

Redis中的HLL尽管在技术上是不同的数据结构，但被编码为Redis字符串，因此您可以调用[GET](/commands/get)来序列化HLL，然后调用[SET](/commands/set) 来将其反序列化回服务器。

从概念上讲，HLL API就像使用Set来执行相同的任务。你会 [萨德](/commands/sadd)每个观测元素为一组，并且将使用[SCARD](/commands/scard)检查组中的元素，这是唯一的数量自[SADD](/commands/sadd)不会再添加一个现有的元素。

尽管您并未真正_将项目添加_到HLL中，但由于数据结构仅包含不包含实际元素的状态，因此API相同：

*   每次看到新元素时，都可以使用[PFADD](/commands/pfadd)将其添加到计数中。
*   到目前为止，每次您要检索_添加_到[PFADD](/commands/pfadd)的唯一元素的当前近似值时，都可以使用[PFCOUNT](/commands/pfcount)。
    
        > pfadd hll a b c d
        (integer) 1
        > pfcount hll
        (integer) 4
        
    

该数据结构用例的一个例子是每天计算用户在搜索表单中执行的唯一查询。

Redis也能够执行HLL的合并，请查看 [完整的文档](/commands#hyperloglog)以获取更多信息。

[\*](#other-notable-features)Other notable features
---------------------------------------------------

Redis API中还有其他重要内容，在本文档的上下文中无法探讨，但值得您注意：

*   可以逐步[迭代大型集合的键空间](/commands/scan)。
*   可以在[服务器端](/commands/eval)运行[Lua脚本](/commands/eval)以改善延迟和带宽。
*   Redis还是[Pub-Sub服务器](/topics/pubsub)。

[\*](#learn-more)Learn more
---------------------------

本教程绝不完整，仅涵盖了API的基础知识。阅读[命令参考](/commands)以发现更多内容。

感谢您的阅读，并祝您使用Redis玩得开心！

作者：[分布式编程](https://blog.jsdiff.com/)
出处：[https://blog.jsdiff.com/](https://blog.jsdiff.com/)
如果你喜欢本文,请长按二维码，关注 **分布式编程**
.![分布式编程](https://images.jsdiff.com/qrcode_for_gh_1e2587cc42b1_258_1587996055777.jpg)