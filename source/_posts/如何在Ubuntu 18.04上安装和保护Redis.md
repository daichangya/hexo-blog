---
title: 如何在Ubuntu 18.04上安装和保护Redis
id: 1339
date: 2024-10-31 22:01:51
author: daichangya
excerpt: "介绍Redis是一个内存中键值存储，以其灵活性，性能和广泛的语言支持而闻名。本教程演示了如何在Ubuntu18.04服务器上安装，配置和保护Redis。先决条件要完成本指南，您将需要访问Ubuntu18.04服务器，该服务器具有具有sudo特权的非root用户并配置了基本防火墙。您可以按照我们的初始"
permalink: /archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis/
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

[Redis](https://redis.io/)是一个内存中键值存储，以其灵活性，性能和广泛的语言支持而闻名。本教程演示了如何在Ubuntu 18.04服务器上安装，配置和保护Redis。

先决条件
----

要完成本指南，您将需要访问Ubuntu 18.04服务器，该服务器具有具有`sudo`特权的非root用户并配置了基本防火墙。您可以按照我们的[初始服务器安装指南进行设置](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04)。

准备开始时，以`sudo`用户身份登录到Ubuntu 18.04服务器，然后继续。

第1步-安装和配置Redis
--------------

为了获得最新版本的Redis，我们将使用`apt`从官方Ubuntu存储库进行安装。

`apt`通过键入以下内容来更新本地程序包缓存并安装Redis：
```
    sudo apt update
    sudo apt install redis-server
```    

这将下载并安装Redis及其依赖项。然后，在Redis配置文件中进行一项重要的配置更改，该更改是在安装过程中自动生成的。

使用您喜欢的文本编辑器打开此文件：
```
    sudo nano /etc/redis/redis.conf
```

在文件内部，找到`supervised`指令。该指令允许您声明一个初始化系统来将Redis作为服务进行管理，从而为您提供对其操作的更多控制。该`supervised`指令`no`默认设置为。由于您正在运行使用systemd init系统的Ubuntu，请将其更改为`systemd`：
```
/etc/redis/redis.conf

    
    # If you run Redis from upstart or systemd, Redis can interact with your
    # supervision tree. Options:
    #   supervised no      - no supervision interaction
    #   supervised upstart - signal upstart by putting Redis into SIGSTOP mode
    #   supervised systemd - signal systemd by writing READY=1 to $NOTIFY_SOCKET
    #   supervised auto    - detect upstart or systemd method based on
    #                        UPSTART_JOB or NOTIFY_SOCKET environment variables
    # Note: these supervision methods only signal "process is ready."
    #       They do not enable continuous liveness pings back to your supervisor.
    supervised systemd
```
    

这是您目前唯一需要对Redis配置文件进行的更改，因此请在完成后保存并关闭它。然后，重新启动Redis服务以反映您对配置文件所做的更改：
```
    sudo systemctl restart redis.service
```

这样，您已经安装并配置了Redis，并且它在您的计算机上运行。但是，在开始使用它之前，先检查一下Redis是否运行正常是明智的。

第2步-测试Redis
-----------

与任何新安装的软件一样，在对其配置进行任何进一步更改之前，最好确保Redis能够按预期运行。我们将介绍几种方法来检查Redis在此步骤中是否正常工作。

首先检查Redis服务是否正在运行：
```
    sudo systemctl status redis
```

如果它正在运行而没有任何错误，则此命令将产生类似于以下内容的输出：
```
● redis-server.service - Advanced key-value store
   Loaded: loaded (/lib/systemd/system/redis-server.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2018-06-27 18:48:52 UTC; 12s ago
     Docs: http://redis.io/documentation,
           man:redis-server(1)
  Process: 2421 ExecStop=/bin/kill -s TERM $MAINPID (code=exited, status=0/SUCCESS)
  Process: 2424 ExecStart=/usr/bin/redis-server /etc/redis/redis.conf (code=exited, status=0/SUCCESS)
 Main PID: 2445 (redis-server)
    Tasks: 4 (limit: 4704)
   CGroup: /system.slice/redis-server.service
           └─2445 /usr/bin/redis-server 127.0.0.1:6379
```
    

在这里，您可以看到Redis正在运行并且已经启用，这意味着它被设置为在每次服务器启动时启动。

**注意：**对于Redis的许多常见用例，此设置是理想的。但是，如果您希望每次服务器启动时都手动启动Redis，则可以使用以下命令进行配置：
```
    sudo systemctl disable redis 
```
要测试Redis是否正常运行，请使用命令行客户端连接到服务器：
```
    redis-cli
```
在随后的提示中，使用以下`ping`命令测试连接性：

此输出确认服务器连接仍然有效。接下来，检查是否可以通过运行以下命令设置密钥：
```
    set test "It's working!"
    OK
```
通过键入以下内容来检索值：
```
get test
```
假设一切正常，您将能够检索存储的值：
```
It's working!
```
在确认可以获取该值之后，退出Redis提示符以返回到Shell：
```
    exit
```

作为最终测试，我们将检查Redis即使在停止或重新启动后也能够持久保存数据。为此，请首先重新启动Redis实例：
```
    sudo systemctl restart redis
```

然后再次与命令行客户端连接，并确认您的测试值仍然可用：
```
    redis-cli

    get test
```

您的密钥值仍应可访问：
```
It's working!
```
    
完成后再次退出外壳：
```
    exit
```

这样，您的Redis安装就可以完全运行并可以使用了。但是，其某些默认配置设置是不安全的，并为恶意行为者提供了攻击和获得对服务器及其数据的访问的机会。本教程的其余步骤介绍了[Redis官方网站](http://redis.io/topics/security)所规定的缓解这些漏洞的方法。尽管这些步骤是可选的，并且如果您选择不遵循这些步骤，则Redis仍将起作用，但_强烈_建议您完成这些步骤，以增强系统的安全性。

第3步-绑定到本地主机
-----------

默认情况下，只能从**localhost**访问Redis 。但是，如果您通过遵循与本教程不同的教程来安装和配置Redis，则可能已更新了配置文件以允许从任何地方进行连接。这不如绑定到**localhost**安全。

要更正此问题，请打开Redis配置文件进行编辑：
```
    sudo nano /etc/redis/redis.conf
```
找到此行，并确保其未注释（删除，`#`如果存在）：
```
/etc/redis/redis.conf

    bind 127.0.0.1 ::1
```

保存并关闭完成后的文件（新闻`CTRL + X`，`Y`话`ENTER`）。

然后，重新启动服务以确保systemd读取您的更改：
```
    sudo systemctl restart redis
```

要检查此更改是否已生效，请运行以下`netstat`命令：
```
    sudo netstat -lnp | grep redis

tcp        0      0 127.0.0.1:6379          0.0.0.0:*               LISTEN      14222/redis-server  
    tcp6       0      0 ::1:6379                :::*                    LISTEN      14222/redis-server  
```
此输出显示该`redis-server`程序已绑定到**localhost**（`127.0.0.1`），反映了您刚刚对配置文件进行的更改。如果您在该列中看到另一个IP地址（`0.0.0.0`例如，），则应再次检查您是否取消注释正确的行，然后再次重新启动Redis服务。

现在，您的Redis安装仅在**localhost**上进行侦听，对于恶意行为者来说，发出请求或访问您的服务器将更加困难。但是，Redis当前未设置为要求用户在更改其配置或保存的数据之前对其进行身份验证。为了解决这个问题，Redis允许您要求用户通过密码进行身份验证，然后才能通过Redis客户端（`redis-cli`）进行更改。

步骤4 —配置Redis密码
--------------

配置Redis密码可启用其两个内置安全功能之一-该`auth`命令，该命令要求客户端进行身份验证才能访问数据库。密码是直接在Redis的配置文件中配置的`/etc/redis/redis.conf`，因此请使用您喜欢的编辑器再次打开该文件：
```
    sudo nano /etc/redis/redis.conf
```

滚动到该`SECURITY`部分，然后查找带有以下注释的指令：
```
/etc/redis/redis.conf

    # requirepass foobared
```

通过删除取消注释`#`，然后更改`foobared`为安全密码。

**注意：**`requirepass`在`redis.conf`文件中的指令上方，有一条注释警告：
```
    # Warning: since Redis is pretty fast an outside user can try up to
    # 150k passwords per second against a good box. This means that you should
    # use a very strong password otherwise it will be very easy to break.
    #
```

因此，重要的是要指定一个非常强且很长的值作为密码。您可以使用该`openssl`命令生成一个随机的密码，而不用自己编写密码，如以下示例所示。通过将第一个命令的输出传递到第二个`openssl`命令，如下所示，它将删除由第一个命令产生的任何换行符：
```
    openssl rand 60 | openssl base64 -A
```
您的输出应类似于：

```
RBOJ9cCNoGCKhlEBwQLHri1g+atWgn4Xn4HwNUbtzoVxAYxkiYBi7aufl4MILv1nxBqR4L6NNzI0X6cE
```

将命令的输出复制并粘贴为的新值后`requirepass`，它应显示为：
```
    /etc/redis/redis.conf
requirepass RBOJ9cCNoGCKhlEBwQLHri1g+atWgn4Xn4HwNUbtzoVxAYxkiYBi7aufl4MILv1nxBqR4L6NNzI0X6cE 
```
设置密码后，保存并关闭文件，然后重新启动Redis：
```
    sudo systemctl restart redis.service
```

要测试密码是否有效，请访问Redis命令行：
```
    redis-cli
```

以下显示了用于测试Redis密码是否有效的命令序列。第一条命令尝试在验证之前将密钥设置为一个值：
```
    set key1 10
```

由于您未进行身份验证，因此无法使用，因此Redis返回错误：

```
 NOAUTH Authentication required.
```

下一条命令使用Redis配置文件中指定的密码进行身份验证：
```
    auth your_redis_password
```

Redis承认：
```
OK
```

之后，再次运行前面的命令将成功：
```
    set key1 10
    OK
```

`get key1` 向Redis查询新密钥的值。
```
    get key1
    10
```

确认身份验证后可以在Redis客户端中运行命令后，您可以退出`redis-cli`：
```
    quit
```

接下来，我们将研究重命名Redis命令，如果错误或由恶意参与者输入Redis命令，可能会严重损坏您的计算机。

第5步-重命名危险命令
-----------

Redis内置的另一个安全功能涉及重命名或完全禁用某些被认为是危险的命令。

当由未经授权的用户运行时，此类命令可用于重新配置，破坏或擦除您的数据。与身份验证密码一样`SECURITY`，在`/etc/redis/redis.conf`文件的同一部分中配置重命名或禁用命令。

一些被认为是危险的命令包括：**FLUSHDB**，**FLUSHALL**，**KEYS**，**PEXPIRE**，**DEL**，**CONFIG**，**SHUTDOWN**，**BGREWRITEAOF**，**BGSAVE**，**SAVE**，**SPOP**，**SREM**，**RENAME**和**DEBUG**。这不是一个完整的列表，但是重命名或禁用该列表中的所有命令是增强Redis服务器安全性的一个很好的起点。

是否应禁用或重命名命令取决于您的特定需求或站点的需求。如果您知道永远不会使用可能会被滥用的命令，则可以将其禁用。否则，重命名可能是您的最大利益。

要启用或禁用Redis命令，请再次打开配置文件：

    sudo nano  /etc/redis/redis.conf
    

**警告：**以下显示如何禁用和重命名命令的步骤是示例。您应该只选择禁用或重命名对您有意义的命令。您可以自己查看命令的完整列表，并在[redis.io/commands中](http://redis.io/commands)确定如何滥用[它们](http://redis.io/commands)。  

要禁用命令，只需将其重命名为一个空字符串（由一对引号引起，它们之间没有字符），如下所示：

/etc/redis/redis.conf

    . . .
    # It is also possible to completely kill a command by renaming it into
    # an empty string:
    #
    rename-command FLUSHDB ""
    rename-command FLUSHALL ""
    rename-command DEBUG ""
    . . .
    

要重命名命令，请给其另一个名称，如下面的示例所示。重命名的命令应该使其他人难以猜到，但容易记住：

/etc/redis/redis.conf

    . . .
    # rename-command CONFIG ""
    rename-command SHUTDOWN SHUTDOWN_MENOT
    rename-command CONFIG ASC12_CONFIG
    . . .
    

保存您的更改并关闭文件。

重命名命令后，通过重新启动Redis来应用更改：

    sudo systemctl restart redis.service
    

要测试新命令，请输入Redis命令行：

    redis-cli
    

然后，验证：
```
    auth your_redis_password

OK
```
假设您像前面的示例一样将`CONFIG`命令重命名`ASC12_CONFIG`为。首先，尝试使用原始`CONFIG`命令。它应该失败，因为您已将其重命名：

    config get requirepass
    

    (error) ERR unknown command 'config'
    

但是，调用重命名的命令将成功。它不区分大小写：

    asc12_config get requirepass
    

    1) "requirepass"
    2) "your_redis_password"
    

最后，您可以从退出`redis-cli`：

    exit
    

请注意，如果您已经在使用Redis命令行，然后重新启动Redis，则需要重新进行身份验证。否则，如果键入命令，则会出现此错误：

    NOAUTH Authentication required.
    

关于重命名命令的做法，本`SECURITY`节末尾有一条警告性声明`/etc/redis/redis.conf`，内容为：

> `Please note that changing the name of commands that are logged into the AOF file or transmitted to slaves may cause problems.`

**_注意：_** _Redis项目选择使用术语“主”和“从”，而DigitalOcean通常更喜欢使用“主要”和“次要”替代方案。为了避免混淆，我们选择在此处使用Redis文档中使用的术语。_

这意味着，如果重命名的命令不在AOF文件中，或者如果该重命名的命令尚未将AOF文件传输到从属设备，则应该没有问题。

因此，在尝试重命名命令时，请记住这一点。重命名命令的最佳时间是在不使用AOF持久性时，或者在安装后即刚部署使用Redis的应用程序之前。

当您使用AOF并处理主从安装时，请[从项目的GitHub问题页面中](https://github.com/antirez/redis/issues/2783)考虑[此答案](https://github.com/antirez/redis/issues/2783)。以下是对作者问题的答复：

> 命令将以发送命令的相同方式记录到AOF并复制到从属设备，因此，如果您尝试在没有相同重命名的实例上重播AOF，则可能会遇到不一致的情况，因为命令无法执行（奴隶也一样）

因此，在这种情况下处理重命名的最佳方法是确保将重命名的命令应用于主从安装中的所有实例。  

结论
--

在本教程中，您已安装和配置Redis，验证您的Redis安装是否正常运行，并使用其内置的安全功能使其较不容易受到恶意行为者的攻击。