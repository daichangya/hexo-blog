---
title: 如何从命令行更改Redis的配置
id: 1350
date: 2024-10-31 22:01:51
author: daichangya
excerpt: 介绍Redis是一个开源的内存中键值数据存储。Redis有几个命令，可让您即时更改Redis服务器的配置设置。本教程将介绍其中一些命令，并说明如何使这些配置更改永久生效。如何使用本指南本指南以备有完整示例的备忘单形式编写。我们鼓励您跳至与您要完成的任务相关的任何部分。本指南中显示的命令已在运行Red
permalink: /archives/ru-he-cong-ming-ling-xing-geng-gai/
categories:
- redis
---


1. [如何在ubuntu18.04上安装和保护redis](https://www.tushu.info/archives/ru-he-zai-Ubuntu-18-04-shang-an-zhuang)
2. [如何连接到Redis数据库](https://www.tushu.info/archives/zen-me-lian-jie-Redis)
3. [如何管理Redis数据库和Keys](https://www.tushu.info/archives/ru-he-guan-li-Redis-shu-ju-ku-he-Keys)
4. [如何在Redis中管理副本和客户端](https://www.tushu.info/archives/ru-he-zai-Redis-zhong-guan-li-fu-ben-he)
5. [如何在Redis中管理字符串](https://www.tushu.info/archives/ru-he-zai-Redis-zhong-guan-li-zi-fu)
6. [如何在Redis中管理list](https://www.tushu.info/archives/zai-Redis-zhong-zen-me-shi-yong-Lists)
7. [如何在Redis中管理Hashes](https://www.tushu.info/archives/ru-he-zai-Redis-zhong-guan-li-Hashes)
8. [如何在Redis中管理Sets](https://www.tushu.info/archives/ru-he-zai-Redis-zhong-guan-li-Sets)
9. [如何在Redis中管理Sorted Sets](https://www.tushu.info/archives/zai-Redis-zhong-zen-me-shi-yong-Sorted)
10. [如何在Redis中运行事务](https://www.tushu.info/archives/ru-he-zai-Redis-zhong-yun-xing-shi-wu)
11. [如何使Redis中的Key失效](https://www.tushu.info/archives/ru-he-shi-Redis-zhong-de-Keys-shi-xiao)
12. [如何解决Redis中的故障](https://www.tushu.info/archives/ru-he-jie-jue-Redis-zhong-de-wen-ti)
13. [如何从命令行更改Redis的配置](https://www.tushu.info/archives/ru-he-cong-ming-ling-xing-geng-gai)
14. [Redis数据类型简介](https://www.tushu.info/archives/Redis-shu-ju-lei-xing-jian-jie)

介绍
--

[Redis](https://redis.io/)是一个开源的内存中键值数据存储。Redis有几个命令，可让您即时更改Redis服务器的配置设置。本教程将介绍其中一些命令，并说明如何使这些配置更改永久生效。

#### 如何使用本指南

本指南以备有完整示例的备忘单形式编写。我们鼓励您跳至与您要完成的任务相关的任何部分。

本指南中显示的命令已在运行Redis版本4.0.9的Ubuntu 18.04服务器上进行了测试。要设置类似的环境，您可以按照我们的指南[如何在Ubuntu 18.04上安装和保护Redis的](https://www.tushu.info/archives/ru-he-zai-Ubuntu-18-04-shang-an-zhuang)**步骤1**进行操作。我们将通过使用Redis命令行界面运行它们来演示这些命令的行为。请注意，如果您使用其他Redis界面（例如[Redli）](https://github.com/IBM-Cloud/redli)，则某些命令的确切输出可能会有所不同。[](https://www.tushu.info/archives/ru-he-zai-Ubuntu-18-04-shang-an-zhuang)`redis-cli`[](https://github.com/IBM-Cloud/redli)

请注意，托管Redis数据库通常不允许用户更改配置文件。如果您正在使用DigitalOcean的托管数据库，则本指南中概述的命令将导致错误。

更改Redis的配置
----------

本节中概述的命令将仅在当前会话期间或直到您运行之前更改Redis服务器的行为，`config rewrite`这将使它们永久化。您可以通过使用首选文本编辑器打开和编辑Redis配置文件来直接更改它。例如，您可以`nano`这样做：

    sudo nano /etc/redis/redis.conf
    

**警告：**该`config set`命令**被认为是危险的**。通过更改Redis配置文件，有可能导致Redis服务器以意外或不良方式运行。我们建议仅在`config set`测试命令的行为或绝对确定要对Redis配置进行更改时才运行该命令。

您可能希望[将此命令重命名](https://www.tushu.info/archives/ru-he-zai-Ubuntu-18-04-shang-an-zhuang#step-5-%E2%80%94-renaming-dangerous-commands)为不太可能意外运行的[命令](https://www.tushu.info/archives/ru-he-zai-Ubuntu-18-04-shang-an-zhuang#step-5-%E2%80%94-renaming-dangerous-commands)。  

`config set`允许您在运行时重新配置Redis，而无需重新启动服务。它使用以下语法：

    config set parameter value
    

例如，如果要更改运行`save`命令后Redis将产生的数据库转储文件的名称，则可以运行如下命令：

    config set "dbfilename" "new_file.rdb"
    

如果配置更改有效，则命令将返回`OK`。否则将返回错误。

**注意：**并非`redis.conf`文件中的每个参数都可以通过`config set`操作来更改。例如，您不能更改`requirepass`参数定义的身份验证密码。  

永久进行配置更改
--------

`config set`不会永久更改Redis实例的配置文件；它仅在运行时更改Redis的行为。要`redis.conf`在运行`config-set`命令后进行编辑并使当前会话的配置永久化，请运行`config rewrite`：

    config rewrite
    

此命令将尽最大努力保留原始`redis.conf`文件的注释和整体结构，而只需进行最小的更改即可匹配服务器当前使用的设置。

就像`config set`，如果重写成功`config rewrite`将返回`OK`。

检查Redis的配置
----------

要读取Redis服务器的当前配置参数，请运行`config get`命令。`config get`只有一个参数，其可以是在使用的参数中的任一个完全匹配`redis.conf`或[_水珠图案_](https://en.wikipedia.org/wiki/Glob_(programming))。例如：

    config get repl*
    

根据您的Redis配置，此命令可能返回：

    Output 1) "repl-ping-slave-period"
     2) "10"
     3) "repl-timeout"
     4) "60"
     5) "repl-backlog-size"
     6) "1048576"
     7) "repl-backlog-ttl"
     8) "3600"
     9) "repl-diskless-sync-delay"
    10) "5"
    11) "repl-disable-tcp-nodelay"
    12) "no"
    13) "repl-diskless-sync"
    14) "no"
    

您还可以`config set`通过运行返回所有支持的配置参数`config get *`。

结论
--

本指南详细介绍了`redis-cli`用于动态更改Redis服务器的配置文件的命令。如果您想在本指南中概述其他相关的命令，参数或过程，请在下面的评论中提出疑问或提出建议。

有关Redis命令的更多信息，请参阅关于[如何管理Redis数据库的](https://www.tushu.info/archives/ru-he-shi-yong-Redis-shu-ju-ku)系列教程。