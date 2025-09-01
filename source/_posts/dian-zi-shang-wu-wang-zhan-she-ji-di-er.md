---
title: 电子商务网站设计（第二部分）
id: 1418
date: 2024-10-31 22:01:54
author: daichangya
excerpt: 这是“设计电子商务网站”系列文章的第二篇。如果您还没有阅读第一篇文章，那么最好先检查一下，因为我们将在这里继续我们的讨论。为了简短地提醒您我们在上一篇文章中讨论的内容，我们从电子商务网站的数据模型设计开始。尽管关系数据库是最常用的方法，但是我们注意到，像MongoDB这样的NoSQL数据库在构建电子
permalink: /archives/dian-zi-shang-wu-wang-zhan-she-ji-di-er/
categories:
- 系统架构
---

这是“设计电子商务网站”系列文章的第二篇。如果您还没有阅读[第一篇文章](https://blog.jsdiff.com/design-ecommerce-website-part/)，那么最好先检查一下，因为我们将在这里继续我们的讨论。

为了简短地提醒您我们在上一篇文章中讨论的内容，我们从电子商务网站的数据模型设计开始。尽管关系数据库是最常用的方法，但是我们注意到，像MongoDB这样的NoSQL数据库在构建电子商务网站时具有许多优势和灵活性。为了扩展系统，并发是要考虑的关键因素之一。

 在这篇文章中，我将主要关注电子商务网站的可扩展性。构建单个机器系统可能很简单，但是当我们决定扩展网站以通过多个服务器支持数百万甚至数十亿个请求时，就需要考虑大量的可扩展性问题。

![](https://lh3.googleusercontent.com/bSCLjv6k0CCspNanJjddnTndmV31STNGROR1ImE2pxb_eQsd1ea3ZGW7Cw_7kw4xjUSeoE9UKjd3aBVa_LAApiCSjzXWCcX4Syc0UsT1Ae2dEFb07yj1gJPFoQvyFh73oYcZ7RdmH0lMC9vBubymOHVFpIM_DkWikRZhhq7rfu12yBug-EI_Ct493XZio9yOCrbM1zhX3wXM4LhKleIJBmYmgrOwDKxttlRoAShzOgexO7UuLyjZCvPObW-xLJVeqZ_YSvJihqnpEnHj0yWJzl74CF11ZALiidqfyGq2gzU_7Tont-kzAfdtqptO1BdQOoF4fA6xyrzP51SsYXFpC1pqQAOg97r_n8Es2qUKpYxFZ53UzhpkGVV-pC0hHwrsnYfHX_ruB_zp0gTfdeFY746oq_GMsxucPawELth5mHCJw087Iadl4RfepxsVJwJpDe2i1b1qo2T42Bdx0MRZRFt0226OgctLBUcObS88tYOrlCw6FSR5ozuS8yrqSo-kq8PpJvomttsChJutIKQTaKYZt7in1b7HOtQv-aYxTCHXqUODQOo6Na6ZjeCPPv5rpKIjW8fIjfK8m1XeTMlmKEOuCdEYXhbGDYCJOKA-dKgDosKK=w640-h498-no)

并发（续）
-----

一种常见的情况是，商店中只剩下一本书，而两个人同时购买。如果没有任何并发​​机制，那么两个人都有可能成功购买它。

在我们以前的文章中，我们知道一种方法是每当有人访问资源（书）时在行上放置一个锁，以便最多一个人一次可以读/写数据。该解决方案称为[悲观并发控制](https://en.wikipedia.org/wiki/Concurrency_control#Concurrency_control_mechanisms)。尽管这种方法可以防止两个人同时访问相同的数据，但是放置锁的成本很高。您将如何更有效地解决这个问题？

[乐观并发控制](https://en.wikipedia.org/wiki/Optimistic_concurrency_control)是支持并发的另一种方法。这个想法非常简单–每个进程/线程都可以自由访问数据，而不必使用锁。但是，在提交更改之前，每个事务都应检查数据是否具有与上次读取时相同的状态。换句话说，您在事务开始时检查数据，并在提交之前再次检查数据是否仍然相同。

如果尚未修改数据，则可以安全地提交它。否则，请回滚并重试直到没有冲突。在这里比较两种方法很重要。对于OCC（开放式并发控制），除非有冲突，否则读写数据显然更为有效。考虑到这一点，对于不太可能发生冲突的系统，OCC是更好的选择。但是，当多个客户端频繁访问资源时，在OCC中重新启动事务变得很昂贵，最好在每个事务（PCC）中放置锁。

在像Amazon这样的应用程序中，有太多的产品，以至于多个人同时访问同一产品的频率并不高。因此，OCC是更好的选择。

电子商务中的可用性
---------

如果亚马逊网站宕机1分钟，那将是一个巨大的损失。为了在分布式系统中实现高可用性，最好的方法是拥有数百或数千个副本，以便您可以容忍许多故障。但是，这里需要注意的是可用性和一致性是并存的。

如果您有许多副本，那么绝对很难保证每个副本都具有相同的数据。另一方面，如果要实现高一致性，则最好具有较少的副本，这样系统很容易出现故障。

这里的想法不是试图实现两者。相反，根据产品的性质，您应该能够进行权衡。对于电子商务网站，延迟和停机时间通常意味着收入损失，有时这可能是一个很大的数字。结果，我们可能更关心可用性而不是一致性。后者可以通过其他方法进行改进。  
![](https://lh3.googleusercontent.com/gPBLRqDoLot33L2A63Snw3SfweE2WL1jnaG_ox1_-tjmU1Lcf0gFqPVtiAGyz43sy6QkHAf3WPGJnbjHQvTpt-w7Kt61sIA1nZZkwJ9NEYfTgSZ4ufhzAqBAJblAlTTATYcjIpRIJZbCpdb6InMDct68uyl8r4lrmAP0Mm_obJ3Lth4g0S7V7h3nPuvjDQI-nMn0_AYL-0qUWqH5cxaxIa4HtWusXDZn-KyOMFn7DC5h8M8tOvFRo2MCMok1yJI4WJnnFFg9XD5nbixVZbmFol9skV7PL3HKduF19p6_WOpl9uaca6lu0DdpAEj_30VcprSLHxIbqzql0UfMvcCjGGfznxWsMDT77EmxGu49S3-fD7hR3KpuZ9LEWt40vF8ToNMn41QbR4efXfCxvS4IuMQUfZ3m9vwvzH8ArmoLrZiLZTPtTskfvuHTREDG7j-i_AJBGF0E-j6v9guiOcdChFT0etV1wTk0viGdoQbsyGGWD0Hb8dcElEJoW03YIX10WY5Zu-e1hp5xhCWv3XnC4hAWkDvXzzOsH1CfFDJAlydZhBvAiD9WaDvfv3Y2CTS40I5gYA2pf6TrbRgYYY_bl9wlariWGJUHtjSHvu2lDUDuc6R6=w2172-h1450-no)

电子商务中的一致性
---------

假设我们有成百上千个副本，您如何保证每个副本都保留相同的数据？为了详细解释该问题，假设数据D被复制到多个服务器中。当某个进程试图将D更新为D1时，它从一台服务器启动，并按照特定的顺序传播更改。同时，另一个进程正在尝试将D更新为D2，并且它可能从其他服务器启动。结果，一些服务器具有数据D1和一些D2。

强一致性
----

一种方法是强制所有更新原子地以相同顺序进行。更具体地说，当某人正在更新资源时，该资源将在所有服务器上锁定，直到它们共享相同的值（更新后）为止。结果，如果应用程序建立在具有高度一致性的系统上，则与在单台计算机上工作完全相同。显然，这是最昂贵的方法，因为不仅增加了昂贵的锁，而且每次更新都会阻塞系统。

弱一致性
----

另一个极端情况是我们可以提供最少的策展。每个副本将看到每个更新，但是它们的顺序可能不同。结果，这种方法使更新操作极为轻巧，但缺点是一致性的保证最低。

注意：我们没有解释[一致性模型](https://en.wikipedia.org/wiki/Consistency_model)的准确定义。相反，我们想通过示例来说明想法，这些示例对于准备系统设计面试更为有用。

最终一致性
-----

可以想象，一种更实用的方法介于两者之间。简而言之，系统仅保证每个副本最终将具有相同的值。在特定时间段内，数据可能会不一致。但是从长远来看，该系统将解决冲突。

让我们以[亚马逊的Dynamo](https://en.wikipedia.org/wiki/Dynamo_(storage_system))为例。基本上，每个副本都有可能在特定时间保存不同版本的数据。因此，当客户端读取数据时，它可能会获得多个版本。此时，客户端（而不是数据库）负责解决所有冲突并将其更新回服务器。

您可能想知道客户端如何解决这些冲突。这主要是产品决定。以购物车为例，不丢失任何附加件非常重要，因为丢失附加件意味着损失收入。因此，当面对不同的价值时，客户可以选择包含最多商品的商品。

摘要
--

如您所见，在分布式系统中，这里有很多技术是通用的。重要的是要了解彼此之间的权衡并选择最适合产品的方法。
