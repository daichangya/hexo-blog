---
title: 如何用Redis实现分布式锁以及可用性
id: 1498
date: 2024-10-31 22:01:58
author: daichangya
permalink: /archives/ru-he-yong-Redis-shi-xian-fen-bu-shi/
categories:
- redis
---


> 　　在实际的开发场景中，我们可能会遇到不同客户端需要互斥地访问某个共享资源，也就是同一时刻只允许一个客户端操作这个共享资源，为了达到这个目的，一般会采用分布式锁来解决，目前流行的分布式锁实现方式有数据库、Memcached、Redis、文件系统、ZooKeeper，因Redis高性能、部署简单被广泛采用，那么今天我就给大家分享下，如何用Redis实现分布式锁。

**一、一个可靠的、高可用的分布式锁需要满足以下几点**

互斥性：任意时刻只能有一个客户端拥有锁，不能被多个客户端获取

安全性：锁只能被持有该锁的客户端删除，不能被其它客户端删除

死锁：获取锁的客户端因为某些原因而宕机，而未能释放锁，其它客户端也就无法获取该锁，需要有机制来避免该类问题的发生

高可用：当部分节点宕机，客户端仍能获取锁或者释放锁

**二、利用单节点Redis实现分布式锁**

利用单节点Redis实现分布式锁是最常用的一种方式，虽然没有考虑高可用，但是实现简单、成本低廉而被很多中小型企业所采用。

　　网上很多文章说采用setnx实现分布式锁，但是setnx命令无法原子性的设置锁的自身过期时间，也就是说执行setnx命令时我们无法同时设置其过期时间，那么就会出现死锁，例如：客户端A刚执行完setnx，这时候客户端A挂掉了，没有完成给锁设置过期时间，此时就产生了死锁，所有的客户端再也无法获得该锁，这种情况一般采用Lua脚本来实现（因为Redis执行Lua脚本是原子性的），其实从 Redis 2.6.12 版本开始set命令完全可以替代setnx命令，我们看官网的set命令参数

SET key value \[EX seconds\] \[PX milliseconds\] \[NX|XX\]

参数说明：

EX second ：设置键的过期时间为 second 秒。 SET key value EX second 效果等同于 SETEX key second value 。

PX millisecond ：设置键的过期时间为 millisecond 毫秒。 SET key value PX millisecond 效果等同于 PSETEX key millisecond value 。

NX ：只在键不存在时，才对键进行设置操作。 SET key value NX 效果等同于 SETNX key value 。

XX ：只在键已经存在时，才对键进行设置操作。

例如：SET key value NX PX 30000 这个命令的作用是在只有这个key不存在的时候才会设置这个key的值（NX选项的作用），超时时间设为30000毫秒（PX选项的作用）

那么我们用set命令带上EX或者PX、以及NX参数就满足了上面提到的互斥性（加锁）、死锁（自动过期）两个要求。

那么如何满足安全性这个要求呢？

比如：客户端A拿到锁并设置了锁的过期时间为10S，但是由于某种原因客户端A执行时间超过了10S，此时锁自动过期，那么客户端B拿到了锁，然后客户端A此时正好执行完毕删除锁，但是此时删除的是客户端B加的锁，如何防止这种不安全的情况发生呢？

方案一：

我们可以让获得锁的线程开启一个守护线程，用来给自己的锁“续期”。

当过去了9S，客户端A还没执行完，这时候守护线程会执行expire指令，把锁再“续期”10S,守护线程从第9S开始执行，每9秒执行一次。

当客户端A执行完任务，会显式关掉守护线程。

如果客户端A忽然宕机，由于A线程和守护线程在同一个进程，守护线程也会停下。这把锁到了超时的时候，没人给它续期，也就自动释放了。

方案二：

我们也可以在加锁的时候把set的value值设置成一个唯一标识，标识这个锁是谁加的锁，在删除锁的时候判断是不是自己加的那把锁，如果不是则不删除。

注意：这里隐含了一个新的问题，判断是不是自己加的锁和释放锁是两个独立操作，不是原子性，所以我们需要使用Lua脚本执行判断和释放锁。

三、提高Redis分布式锁的高可用性

在大型的应用中，一般Redis服务都是集群形式，主从复制、Cluster等，由于Slave同步Master是异步的，所以会出现客户端A在Master上加锁，此时Master宕机，Slave没有完成锁的同步，Slave变为Master，客户端B此时可以完成加锁操作，如何解决该问题呢？

官方给出了Redlock算法，大致意思如下：

在分布式版本的算法里我们假设我们有N个Redis Master节点，这些节点都是完全独立的，我们不用任何复制或者其他隐含的分布式协调算法（如果您采用的是Redis Cluster集群此方案可能不适用，因为Redis Cluster是按哈希槽 (hash slot)的方式来分配到不同节点上的，明显存在分布式协调算法）。

我们把N设成5，因此我们需要在不同的计算机或者虚拟机上运行5个master节点来保证他们大多数情况下都不会同时宕机。一个客户端需要做如下操作来获取锁：

1、获取当前时间（单位是毫秒）。

2、轮流用相同的key和随机值（客户端的唯一标识）在N个节点上请求锁，在这一步里，客户端在每个master上请求锁时，会有一个和总的锁释放时间相比小的多的超时时间。比如如果锁自动释放时间是10秒钟，那每个节点锁请求的超时时间可能是5-50毫秒的范围，这个可以防止一个客户端在某个宕掉的master节点上阻塞过长时间，如果一个master节点不可用了，我们应该尽快尝试下一个master节点。

3、客户端计算第二步中获取锁所花的时间，只有当客户端在大多数master节点上成功获取了锁（在这里是3个），而且总共消耗的时间不超过锁释放时间，这个锁就认为是获取成功了。

4、如果锁获取成功了，那现在锁自动释放时间就是最初的锁释放时间减去之前获取锁所消耗的时间。

5、如果锁获取失败了，不管是因为获取成功的锁不超过一半（N/2+1)还是因为总消耗时间超过了锁释放时间，客户端都会到每个master节点上释放锁，即便是那些他认为没有获取成功的锁。

虽然说RedLock算法可以解决单点Redis分布式锁的高可用问题，但如果集群中有节点发生崩溃重启，还是会出现锁的安全性问题。具体出现问题的场景如下：

假设一共有A, B, C, D, E，5个Redis节点，设想发生了如下的事件序列：

1、客户端1成功锁住了A, B, C，获取锁成功（但D和E没有锁住）

2、节点C崩溃重启了，但客户端1在C上加的锁没有持久化下来，丢失了

3、节点C重启后，客户端2锁住了C, D, E，获取锁成功

这样，客户端1和客户端2同时获得了锁（针对同一资源）。针对这样场景，解决方式也很简单，也就是让Redis崩溃后延迟重启，并且这个延迟时间大于锁的过期时间就好。这样等节点重启后，所有节点上的锁都已经失效了。也不存在以上出现2个客户端获取同一个资源的情况了。

总之用Redis集群实现分布式锁要考虑的特殊情况比较多，尤其是服务器比较多的情况下，需要多测试。

最后给出各种语言实现Redlock算法的代码，感兴趣的朋友可以深入学习下：

Redlock-py (Python 实现)：

https://github.com/SPSCommerce/redlock-py

Redlock-php (PHP 实现)：

https://github.com/ronnylt/redlock-php

PHPRedisMutex (PHP 更完整的实现)：

https://github.com/php-lock/lock#phpredismutex

Redsync.go (Go 实现)：

https://github.com/hjr265/redsync.go

Redisson (Java 实现)：

https://github.com/redisson/redisson

Redis::DistLock (Perl 实现)：

https://github.com/sbertrang/redis-distlock

Redlock-cpp (C++ 实现)：

https://github.com/jacket-code/redlock-cpp

Redlock-cs (C#/.NET 实现)：

https://github.com/kidfashion/redlock-cs

node-redlock (NodeJS 实现). Includes support for lock extension：

https://github.com/mike-marcacci/node-redlock

总结：对于Redis分布式锁需要根据自己的实际情况进行选择是单机还是高可用的集群形式

**三、实际上redis分布式锁的可用性**

　　以上的方案是针对redis分布式锁专门搭建的集群redis，实际上我们的redis可能只是一个黑盒链接，里面关于主从的切换以及主从库节点的获取对于程序而言都是不存在的，程序只管业务。

所以如果要实现以上分布式锁，还需要dba的配合支持。
