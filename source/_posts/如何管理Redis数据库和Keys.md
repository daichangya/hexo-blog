---
title: 如何管理Redis数据库和Keys
id: 1340
date: 2024-10-31 22:01:51
author: daichangya
excerpt: "介绍Redis是一个开源的内存中键值数据存储。甲_键值_数据存储是一种类型的NoSQL数据库，其中_keys_作为其相关联的唯一标识符_值_。任何给定的Redis实例都包含许多_数据库_，每个_数据库_都可以保存许多不同的keys，这些keys具有各种_数据类型_。在本教程中，我们将介绍如何选择数据"
permalink: /archives/howtomanageredisdatabasesandkeys/
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

[Redis](https://redis.io/)是一个开源的内存中键值数据存储。[键值_数据存储](https://www.digitalocean.com/community/tutorials/a-comparison-of-nosql-database-management-systems-and-models#key-value-databases)是一种类型的NoSQL数据库，其中_keys_作为其相关联的唯一标识符_值_。任何给定的Redis实例都包含许多_数据库_，每个_数据库_都可以保存许多不同的keys，这些keys具有各种_数据类型_。在本教程中，我们将介绍如何选择数据库，在数据库之间移动keys以及管理和删除keys。

#### 如何使用本指南

本指南以备有完整示例的备忘单形式编写。我们鼓励您跳至与您要完成的任务相关的任何部分。

本指南中显示的命令已在运行Redis版本4.0.9的Ubuntu 18.04服务器上进行了测试。要设置类似的环境，您可以按照我们的指南[如何在Ubuntu 18.04上安装和保护Redis的](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis)**步骤1**进行操作。我们将通过使用Redis命令行界面运行它们来演示这些命令的行为。请注意，如果您使用其他Redis界面（例如[Redli）](https://github.com/IBM-Cloud/redli)，则某些命令的确切输出可能会有所不同。[](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis)`redis-cli`[](https://github.com/IBM-Cloud/redli)

另外，您可以提供一个托管的Redis数据库实例来测试这些命令，但是请注意，根据数据库提供者所允许的控制级别，本指南中的某些命令可能无法按所述方式工作。要配置DigitalOcean托管数据库，请遵循我们的[托管数据库产品文档](https://www.digitalocean.com/docs/databases/redis/quickstart/)。然后，**您必须** [**安装Redli**](https://www.digitalocean.com/community/tutorials/how-to-connect-to-managed-database-ubuntu-18-04#connecting-to-a-managed-redis-database) **或** [**设置TLS隧道**](https://www.digitalocean.com/community/tutorials/how-to-connect-to-managed-redis-over-tls-with-stunnel-and-redis-cli)才能通过TLS连接到托管数据库。

管理数据库
-----

开箱即用的Redis实例支持16个逻辑数据库。这些数据库实际上是相互隔离的，当您在一个数据库中运行命令时，它不会影响Redis实例中其他数据库中存储的任何数据。

Redis数据库从编号`0`到`15`，默认情况下，`0`当您连接到Redis实例时，您将连接到数据库。但是，您可以`select`在连接后通过以下命令更改正在使用的数据库：

    select 15
    

如果您选择了以外的其他数据库`0`，则会在`redis-cli`提示中反映出来：

要将一个数据库中保存的所有数据与另一个数据库中保存的数据交换，请使用`swapdb`命令。下面的例子将交换数据库中保存的数据`6`与数据库`8`，并连接到任何数据库的任何客户将能够立即看到变化：

    swapdb 6 8
    

`swapdb``OK`如果交换成功，将返回。

如果要将keys移到其他Redis实例，可以运行`migrate`。此命令确保在从源实例删除keys之前，该keys存在于目标实例上。运行时`migrate`，命令必须按以下顺序包含以下元素：

*   目标数据库的主机名或IP地址
*   目标数据库的端口号
*   您要迁移的keys的名称
*   您要在目标实例上存储keys的数据库号
*   超时（以毫秒为单位），该超时定义了两台计算机之间的最大空闲通信时间。请注意，这不是操作的时间限制，只是操作应始终在定义的时间长度内取得一定程度的进展

为了显示：

    migrate 203.0.113.0 6379 key_1 7 8000
    

此外，`migrate`允许您在超时参数后添加以下选项：

*   `COPY`：指定不应从源实例中删除keys
*   `REPLACE`：指定如果目标上已经存在keys，则该`migrate`操作应删除并替换它
*   `KEYS`：您可以输入一个空字符串（`""`），而不是提供要迁移的特定keys，然后使用`keys`命令中的语法迁移与模式匹配的任何keys。有关`keys`工作原理的更多信息，请参见我们的有关[如何在Redis中解决问题的](https://www.digitalocean.com/community/cheatsheets/how-to-troubleshoot-issues-in-redis#using-the-keys-command)教程。

管理Keys
----

有许多Redis命令可用于管理keys，而不管它们所保存的数据类型是什么。在本节中，我们将介绍其中的一些。

`rename`将重命名指定的keys。如果成功，它将返回`OK`：

    rename old_key new_key
    

您可以用来`randomkey`从当前选定的数据库中返回一个随机keys：

    randomkey
    

    "any_key"
    

使用`type`来确定给定keys持有什么类型的数据。这条命令的输出可以是`string`，`list`，`hash`，`set`，`zset`，或`stream`：

    type key_1
    

    "string"
    

如果指定的键不存在，`type`将返回`none`。

您可以使用以下`move`命令将单个keys移动到Redis实例中的另一个数据库。`move`接受键的名称以及要将键移动到的数据库作为参数。例如，要将keys移动`key_1`到database `8`，您将运行以下命令：

    move key_1 8
    

`move``OK`如果成功移动钥匙，将返回。

删除Keys
----

要删除任何数据类型`del`的一个或多个键，请使用命令后跟要删除的一个或多个键：

    del key_1 key_2
    

如果此命令成功删除keys，它将返回`(integer) 1`。否则，它将返回`(integer) 0`。

该`unlink`命令执行的功能`del`与相似，不同之处在于，`del`当服务器回收keys占用的内存时，该块会阻止客户端。如果要删除的keys与一个小对象相关联，则`del`回收内存所花费的时间将非常小，并且阻塞时间甚至可能不会很明显。

但是，例如，如果您要删除的键与许多对象相关联（例如具有数千或数百万个字段的哈希），则可能会带来不便。删除这样的keys可能会花费相当长的时间，并且在将其从服务器内存中完全删除之前，您将无法执行任何其他操作。

`unlink`但是，首先要确定重新分配keys占用的内存的成本。如果太小，则立即`unlink`起到`del`与按键相同的作用，同时也会阻塞客户端。但是，如果为keys分配内存的成本很高，`unlink`则将通过创建另一个线程_异步_删除keys，并在后台递增回收内存而不阻塞客户端：

    unlink key_1
    

由于它是在后台运行的，因此通常建议您使用它`unlink`从服务器上删除keys，以减少客户机上的错误，尽管`del`在许多情况下也足够了。

**警告：**以下两个命令被认为是**危险的**。该`flushdb`和`flushall`命令将不可逆转地删除一个数据库中的所有键和所有键在Redis的服务器上的每个数据库，分别。我们建议仅在绝对确定要删除数据库或服务器中的所有键时才运行这些命令。

您可能希望[将这些命令重命名](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis#step-5-%E2%80%94-renaming-dangerous-commands)为偶然运行的可能性较低的名称。  

要删除所选数据库中的所有keys，请使用以下`flushdb`命令：

    flushdb
    

要删除Redis服务器上每个数据库（包括当前选择的数据库）中的所有keys，请运行`flushall`：

    flushall
    

两者`flushdb`和均`flushall`接受该`async`选项，该选项使您可以异步删除单个数据库或群集中每个数据库上的所有keys。这使它们的功能类似于`unlink`命令，并且它们将创建一个新线程以在后台逐步释放内存。

备份数据库
-----

要创建当前所选数据库的备份，可以使用以下`save`命令：

    save
    

这会将当前数据集的快照导出为`.rdb`文件，这是一个数据库转储文件，以内部压缩的序列化格式保存数据。

`save`同步运行，将阻止连接到数据库的所有其他客户端。因此，[`save`命令文档](https://redis.io/commands/save)建议几乎不要在生产环境中运行此命令。相反，它建议使用`bgsave`命令。这告诉Redis派生数据库：父进程将继续为客户端提供服务，而子进程在退出之前保存数据库：

    bgsave
    

请注意，如果客户端在执行`bgsave`操作时添加或修改数据，则这些更改将不会捕获到快照中。

如果对数据库进行了最少的更改，您还可以编辑Redis配置文件以使Redis 在一定时间后自动保存快照（称为_快照_或_RDB_模式）。这称为_保存点_。默认情况下，`redis.conf`文件中启用了以下保存点设置：

/etc/redis/redis.conf

    . . .
    save 900 1
    save 300 10
    save 60 10000
    . . .
    dbfilename "nextfile.rdb"
    . . .
    

使用这些设置，`dbfilename`如果更改了至少1个键，则Redis将每900秒将数据库的快照导出到该参数定义的文件中；如果更改了至少10个键，则将每300秒将数据库快照导出一次；如果更改了至少10000个键，则将每60秒导出一次数据库快照。被改变了。

您可以使用该`shutdown`命令备份Redis数据，然后关闭连接。`save`如果配置了至少一个保存点，此命令将阻止连接到数据库的每个客户端，然后执行操作，这意味着它将`.rdb`在不阻止客户端进行任何更改的情况下，将当前状态的数据库导出到文件中。

此外，`shutdown`如果启用了_仅附加模式_，该命令将在退出前刷新对Redis的仅附加文件的更改。该[只追加文件模式](https://redis.io/topics/persistence#append-only-file)（AOF）涉及在结尾的文件在服务器上创建一个日志每次写操作的`.aof`每个快照之后。可以在同一服务器上启用AOF和RDB模式，并且使用两种持久性方法都是备份数据的有效方法。

简而言之，该`shutdown`命令本质上是一个阻塞`save`命令，该命令还会刷新对仅附加文件的所有最新更改，并关闭与Redis实例的连接：

**警告：**该`shutdown`命令**被认为是危险的**。通过阻止Redis服务器的客户端，可以使数据对依赖它的用户和应用程序不可用。我们建议仅在测试Redis的行为或绝对确定要阻止所有Redis服务器的客户端时才运行此命令。

实际上，将您的[命令重命名](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis#step-5-%E2%80%94-renaming-dangerous-commands)为不太可能意外运行的[命令](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis#step-5-%E2%80%94-renaming-dangerous-commands)可能符合您的利益。  

    shutdown
    

如果您尚未配置任何保存点，但仍希望Redis执行`save`操作，请将该`save`选项附加到\`shutdown命令：

    shutdown save
    

如果您已经配置了至少一个保存点，但是您想在不执行保存的情况下关闭Redis服务器，则可以将`nosave`参数添加到命令中：

    shutdown nosave
    

请注意，仅附加文件会随着时间的增长而变得很长，但是您可以配置Redis通过编辑文件来基于某些变量重写`redis.conf`文件。您还可以通过运行以下`bgrewriteaof`命令指示Redis重写仅附加文件：

    bgrewriteaof
    

`bgrewriteaof`将创建使数据库恢复到当前状态所需的最短命令集。顾名思义，该命令将在后台运行。但是，如果另一个持久性命令已经在后台进程中运行，则该命令必须在Redis执行之前完成`bgrewriteaof`。

结论
--

本指南详细介绍了许多用于管理数据库和keys的命令。如果您想在本指南中看到其他相关的命令，参数或过程，请在下面的评论中提出疑问或提出建议。

有关Redis命令的更多信息，请参阅关于[如何管理Redis数据库的](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8redis%E6%95%B0%E6%8D%AE%E5%BA%93)系列教程。