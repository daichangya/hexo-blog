---
title: 在Redis中怎么使用Sorted Sets
id: 1346
date: 2024-10-31 22:01:51
author: daichangya
excerpt: 介绍Redis是一个开源的内存中键值数据存储。在Redis的，排序集合类似于一个数据类型集在这两者都是串的非重复的组。不同之处在于，已排序集中的每个成员都与一个分数相关联，从而可以从最小分数到最大分数进行排序。与集合一样，排序集合中的每个成员都必须是唯一的，尽管多个成员可以共享同一分数。本教程说明了
permalink: /archives/zai-Redis-zhong-zen-me-shi-yong-Sorted/
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

[Redis](https://redis.io/)是一个开源的内存中键值数据存储。在Redis的，[_排序集合_](https://redis.io/topics/data-types#sorted-sets)类似于一个数据类型[集](https://redis.io/topics/data-types#sets)在这两者都是串的非重复的组。不同之处在于，已排序集中的每个成员都与一个分数相关联，从而可以从最小分数到最大分数进行排序。与集合一样，排序集合中的每个成员都必须是唯一的，尽管多个成员可以共享同一分数。

本教程说明了如何创建排序集，检索和删除其成员以及如何从现有集合中创建新的排序集。

#### 如何使用本指南

本指南以备有完整示例的备忘单形式编写。我们鼓励您跳至与您要完成的任务相关的任何部分。

本指南中显示的命令已在运行Redis版本4.0.9的Ubuntu 18.04服务器上进行了测试。要设置类似的环境，您可以按照我们的指南[如何在Ubuntu 18.04上安装和保护Redis的](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis)**步骤1**进行操作。我们将通过使用Redis命令行界面运行它们来演示这些命令的行为。请注意，如果您使用其他Redis界面（例如[Redli）](https://github.com/IBM-Cloud/redli)，则某些命令的确切输出可能会有所不同。[](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis)`redis-cli`[](https://github.com/IBM-Cloud/redli)

另外，您可以提供一个托管的Redis数据库实例来测试这些命令，但是请注意，根据数据库提供者所允许的控制级别，本指南中的某些命令可能无法按所述方式工作。要配置DigitalOcean托管数据库，请遵循我们的[托管数据库产品文档](https://www.digitalocean.com/docs/databases/redis/quickstart/)。然后，**您必须** [**安装Redli**](https://www.digitalocean.com/community/tutorials/how-to-connect-to-managed-database-ubuntu-18-04#connecting-to-a-managed-redis-database) **或** [**设置TLS隧道**](https://www.digitalocean.com/community/tutorials/how-to-connect-to-managed-redis-over-tls-with-stunnel-and-redis-cli)才能通过TLS连接到托管数据库。

Creating Sorted Sets and Adding Members
---------------------------------------

要创建排序集，请使用`zadd`命令。`zadd`接受将保留排序后的键集的键的名称作为参数，后跟要添加的成员的分数以及成员本身的值。以下命令将创建一个排序的集合密钥，其名称`faveGuitarists`为一个成员，`"Joe Pass"`得分为`1`：

    zadd faveGuitarists 1 "Joe Pass"
    

`zadd` 将返回一个整数，该整数指示成功创建排序集后将添加到排序集中的成员数。

    Output(integer) 1
    

您可以使用将多个成员添加到排序集中`zadd`。请注意，他们的分数不必是连续的，分数之间可以有间隔，并且同一排序集中的多个成员可以共享同一分数：

    zadd faveGuitarists 4 "Stephen Malkmus" 2 "Rosetta Tharpe" 3 "Bola Sete" 3 "Doug Martsch" 8 "Elizabeth Cotten" 12 "Nancy Wilson" 4 "Memphis Minnie" 12 "Michael Houser"
    

    Output(integer) 8
    

`zadd` 可以接受以下选项，您必须在密钥名称之后和第一个成员评分之前输入以下选项：

*   `NX`或`XX`：这些选项具有相反的效果，因此您在任何`zadd`操作中都只能包括其中之一：
    *   `NX`：告诉`zadd` **不**更新现有成员。使用此选项，`zadd`将仅添加新元素。
    *   `XX`：告诉`zadd`给**只**更新现有的元素。使用此选项，`zadd`将永远不会添加新成员。
*   `CH`：通常，`zadd`仅返回添加到排序集中的新元素的数量。但是，`zadd`如果包含此选项，将返回已_更改_元素的数量。这包括新添加的成员和分数已更改的成员。
*   `INCR`：这会使命令增加成员的得分值。如果该成员还不存在，则该命令会将其添加到已排序的集合中，并将其增量作为分数，就像其原始分数是一样`0`。如果`INCR`包含，则成功`zadd`将返回成员的新分数。请注意，使用此选项时，一次只能包含一个分数/成员对。

无需将`INCR`选项传递给`zadd`，您可以使用`zincrby`行为完全相同的命令。而不是给排序后的集合成员像分数那样由得分值指示的值`zadd`，而是使该成员的得分增加该值。例如，下面的命令增量构件的分数`"Stephen Malkmus"`，这本来`4`，增长`5`到`9`。

    zincrby faveGuitarists 5 "Stephen Malkmus"
    

    Output"9"
    

与`zadd`命令`INCR`选项一样，如果指定的成员不存在，则将`zincrby`使用增量值作为其分数来创建它。

Retrieving Members from Sorted Sets
-----------------------------------

检索排序集中的成员的最基本方法是使用`zrange`命令。此命令接受要检索其成员的键的名称以及其中包含的成员范围作为参数。范围由两个数字定义，这些数字表示[从零开始的](https://en.wikipedia.org/wiki/Zero-based_numbering)索引，`0`表示代表排序集中的第一个成员（或得分最低的成员），`1`代表下一个，依此类推。

下面的示例将返回`faveGuitarists`上一部分中创建的排序集中的前四个成员：

    zrange faveGuitarists 0 3
    

    Output1) "Joe Pass"
    2) "Rosetta Tharpe"
    3) "Bola Sete"
    4) "Doug Martsch"
    

请注意，如果传递给的排序集`zrange`具有两个或多个共享相同分数的元素，它将按照_字典顺序_或字母顺序对这些元素进行排序。

开始索引和停止索引也可以是负数，`-1`代表最后一个成员，`-2`代表倒数第二个，依此类推：

    zrange faveGuitarists -5 -2
    

    Output1) "Memphis Minnie"
    2) "Elizabeth Cotten"
    3) "Stephen Malkmus"
    4) "Michael Houser"
    

`zrange`可以接受`WITHSCORES`参数，当包含该参数时，该参数还将返回成员的分数：

    zrange faveGuitarists 5 6 WITHSCORES
    

    Output1) "Elizabeth Cotten"
    2) "8"
    3) "Stephen Malkmus"
    4) "9"
    

`zrange`只能以数字升序返回一系列成员。要反转它并以降序返回范围，必须使用`zrevrange`命令。可以将此命令视为暂时反转给定排序集的顺序，然后返回属于指定范围内的成员。因此，使用`zrevrange`，`0`将代表密钥中持有的**最后一个**成员，`1`将代表**倒数第二个**，等等：

    zrevrange faveGuitarists 0 5
    

    Output1) "Nancy Wilson"
    2) "Michael Houser"
    3) "Stephen Malkmus"
    4) "Elizabeth Cotten"
    5) "Memphis Minnie"
    6) "Doug Martsch"
    

`zrevrange`也可以接受该`WITHSCORES`选项。

您可以使用`zrangebyscore`命令根据其分数返回一系列成员。在下面的示例中，该命令将返回`faveGuitarists`键中分数为2、3或4的任何成员：

    zrangebyscore faveGuitarists 2 4
    

    Output1) "Rosetta Tharpe"
    2) "Bola Sete"
    3) "Doug Martsch"
    4) "Memphis Minnie"
    

在此示例中，范围是包含范围的，这意味着它将返回分数为2或4的成员。您可以在范围的任一末端加上一个开放的括号（`(`），以排除该范围的任何一端。以下示例将返回分数大于或等于`2`，但小于的每个成员`4`：

    zrangebyscore faveGuitarists 2 (4
    

    Output1) "Rosetta Tharpe"
    2) "Bola Sete"
    3) "Doug Martsch"
    

与一样`zrange`，`zrangebyscore`可以接受`WITHSCORES`参数。它还接受该`LIMIT`选项，您可以使用该选项仅从`zrangebyscore`输出中检索元素的选择。此选项接受一个[_offset（偏移量）_](https://en.wikipedia.org/wiki/Offset_(computer_science))和一个count（计数），该[_偏移量_](https://en.wikipedia.org/wiki/Offset_(computer_science))标记该命令将返回的范围内的第一个成员，该计数总共定义该命令将返回的成员数。例如，以下命令将查看已`faveGuitarists`排序集合的前六个成员，但仅从该集合中返回3个成员，从该范围内的第二个成员开始，由表示`1`：

    zrangebyscore faveGuitarists 0 5 LIMIT 1 3
    

    Output1) "Rosetta Tharpe"
    2) "Bola Sete"
    3) "Doug Martsch"
    

该`zrevrangebyscore`命令根据成员的得分返回相反的范围。以下命令将返回分数在10到6之间的集合中的每个成员：

    zrevrangebyscore faveGuitarists 10 6
    

    Output1) "Stephen Malkmus"
    2) "Elizabeth Cotten"
    

与一样`zrangebyscore`，`zrevrangebyscore`可以接受`WITHSCORES`和`LIMIT`选项。此外，您可以在范围的两端加上开放括号来排除该范围的任何一端。

有时，排序集中的所有成员都具有相同的分数。在这种情况下，您可以使用命令强制redis返回按_字典顺序_或字母顺序排序的元素范围`zrangebylex`。要尝试此命令，请运行以下`zadd`命令以创建一个排序的集合，其中每个成员具有相同的分数：

    zadd SomervilleSquares 0 Davis 0 Inman 0 Union 0 porter 0 magoun 0 ball 0 assembly
    

`zrangebylex`后面必须跟一个键的名称，一个开始间隔和一个停止间隔。开始和停止间隔必须以圆括号（`(`）或方括号（）开头`[`，如下所示：

    zrangebylex SomervilleSquares [a [z
    

    Output1) "assembly"
    2) "ball"
    3) "magoun"
    4) "porter"
    

请注意，即使该命令查找的范围是从`a`到，该示例也仅返回集合中八个成员中的四个`z`。这是因为Redis值区分大小写，因此以大写字母开头的成员将从其输出中排除。要返回这些值，可以运行以下命令：

    zrangebylex SomervilleSquares [A [z
    

    Output1) "Davis"
    2) "Inman"
    3) "Union"
    4) "assembly"
    5) "ball"
    6) "magoun"
    7) "porter"
    

`zrangebylex`还接受特殊字符`-`，它们代表负无穷大，而`+`代表正无穷大。因此，以下命令语法还将返回排序集中的每个成员：

    zrangebylex SomervilleSquares - +
    

请注意，`zrangebylex`不能以相反的字典顺序（字母升序）返回排序的集合成员。为此，请使用`zrevrangebylex`：

    zrevrangebylex SomervilleSquares + -
    

    Output1) "porter"
    2) "magoun"
    3) "ball"
    4) "assembly"
    5) "Union"
    6) "Inman"
    7) "Davis"
    

因为它适用于每个成员都具有相同分数的排序集，`zrangebylex`所以**不**接受该`WITHSCORES`选项。但是，它确实接受该`LIMIT`选项。

Retrieving Information about Sorted Sets
----------------------------------------

要查找给定排序集中有多少个成员（或者换句话说，确定其[_基数_](https://en.wikipedia.org/wiki/Cardinality)），请使用`zcard`命令。以下示例显示了`faveGuitarists`本指南第一部分中密钥中拥有多少成员：

    zcard faveGuitarists
    

    Output(integer) 9
    

`zcount`可以告诉您在给定的排序集中有多少个元素落在分数范围内。键后面的第一个数字是范围的开始，第二个数字是范围的结束：

    zcount faveGuitarists 3 8
    

    Output(integer) 4
    

`zscore` 输出排序集中指定成员的分数：

    zscore faveGuitarists "Bola Sete"
    

    Output"3"
    

如果指定的成员或密钥都不存在，`zscore`将返回`(nil)`。

`zrank`与相似`zscore`，但不返回给定成员的分数，而是返回其排名。在Redis中，_等级_是排序集中成员的从零开始的索引，按其得分排序。例如，`"Joe Pass"`得分为`1`，但是由于这是键中所有成员的最低得分，因此其等级为`0`：

    zrank faveGuitarists "Joe Pass"
    

    Output(integer) 0
    

调用了另一个Redis命令`zrevrank`，该命令执行与相同的功能`zrank`，但取而代之的是反转集合中成员的等级。在以下示例中，该成员`"Joe Pass"`的得分最低，因此其反向排名最高：

    zrevrank faveGuitarists "Joe Pass"
    

    Output(integer) 8
    

成员的分数与其等级之间的唯一关系是其分数相对于其他成员的分数所处的位置。如果两个连续成员之间存在得分差距，则该得分差距不会反映在他们的排名中。请注意，如果两个成员的分数相同，则按字母顺序排在第一位的成员将具有较低的排名。

类似于`zscore`，如果键或成员不存在`zrank`，`zrevrank`将返回`(nil)`。

`zlexcount`可以告诉您在词典范围之间的排序集中有多少个成员。下面的示例使用`SomervilleSquares`上一节中的排序集：

    zlexcount SomervilleSquares [M [t
    

    Output(integer) 5
    

该命令的语法与`zrangebylex`命令相同，因此，请参见上[一节](#retrieving-members-from-sorted-sets)以获取有关如何定义字符串范围的详细信息。

Removing Members from Sorted Sets
---------------------------------

该`zrem`命令可以从排序集中删除一个或多个成员：

    zrem faveGuitarists "Doug Martsch" "Bola Sete"
    

`zrem` 将返回一个整数，指示从排序集中删除了多少个成员：

    Output(integer) 2
    

有三个Redis命令，可让您根据范围删除排序集中的成员。例如，如果排序集中的每个成员都具有相同的分数，则可以使用来根据词典范围删除成员`zremrangebylex`。此命令使用与相同的语法`zrangebylex`。以下示例将从`SomervilleSquares`上一节中创建的密钥中删除所有以大写字母开头的成员：

    zremrangebylex SomervilleSquares [A [Z
    

`zremrangebylex` 将输出一个整数，指示已删除的成员数：

    Output(integer) 3
    

您还可以`zremrangebyscore`使用命令使用与命令相同的语法，根据分数范围删除成员`zrangebyscore`。以下示例将删除`faveGuitarists`得分为4、5或6的每个成员：

    zremrangebyscore faveGuitarists 4 6
    

    Output(integer) 1
    

您可以从基于一系列与队伍的一组删除成员`zremrangebyrank`的命令，它使用相同的语法`zrangebyrank`。以下命令将删除排名最低的排序集中的三个成员，这些成员由一系列从零开始的索引定义：

    zremrangebyrank faveGuitarists 0 2
    

    Output(integer) 3
    

请注意，传递给的数字`remrangebyrank`也可以为负，`-1`代表最高排名，次高排名，`-2`依此类推。

Creating New Sorted Sets from Existing Ones
-------------------------------------------

Redis包含两个命令，它们允许您比较多个排序集的成员并基于这些比较创建新的：`zinterstore`和`zunionstore`。要试验这些命令，请运行以下`zadd`命令以创建一些示例排序集。

    zadd NewKids 1 "Jonathan" 2 "Jordan" 3 "Joey" 4 "Donnie" 5 "Danny"
    zadd Nsync 1 "Justin" 2 "Chris" 3 "Joey" 4 "Lance" 5 "JC"
    

`zinterstore`查找两个或多个排序集（它们的交集）共享的成员，并生成仅包含那些成员的新排序集。此命令必须依次包括相交成员将以排序集存储的目标键的名称，要传递给的键的数量以及`zinterstore`要分析的键的名称：

    zinterstore BoyBands 2 NewKids Nsync
    

`zinterstore`将返回一个整数，该整数显示存储到目标排序集中的元素数。因为`NewKids`和`Nsync`仅共享一个成员`"Joey"`，所以该命令将返回`1`：

    Output(integer) 1
    

请注意，如果目标键已经存在，`zinterstore`将覆盖其内容。

`zunionstore`将创建一个新的排序集，其中包含传递给它的**每个**键成员。此命令使用与相同的语法`zinterstore`，并且需要目标键的名称，传递给该命令的键的数量以及键的名称：

    zunionstore SuperGroup 2 NewKids Nsync
    

像一样`zinterstore`，`zunionstore`将返回一个整数，显示存储在目标键中的元素数。即使两个原始排序集都包含五个成员，但由于排序集不能包含重复成员，并且每个键都有一个名为`"Joey"`的成员，因此所得的整数将为`9`：

    Output(integer) 9
    

与一样`zinterstore`，`zunionstore`如果目标键已经存在，它将覆盖目标键的内容。

为了在使用`zinterstore`和创建新的排序集时更好地控制成员分数`zunionstore`，这两个命令都接受`WEIGHTS`和`AGGREGATE`选项。

对于`WEIGHTS`该命令中包含的每个排序集，此选项后均带有一个数字，该数字_加权_或乘以每个成员的分数。`WEIGHTS`选项后的第一个数字对传递给命令的第一个键的分数加权，第二个数字对第二个键的加权加权，依此类推。

以下示例创建一个新的排序集，其中包含来自`NewKids`和`Nsync`排序集的相交键。它将`NewKids`密钥中的分数加权三倍，并将密钥中的分数加权`Nsync`七倍：

    zinterstore BoyBandsWeighted 2 NewKids Nsync WEIGHTS 3 7
    

如果`WEIGHTS`选项未包括在内，权重默认为`1`两个`zinterstore`和`zunionstore`。

`AGGREGATE`接受三个子选项。其中的第一个，通过添加组合集中匹配成员的得分来`SUM`实现`zinterstore`和`zunionstore`的默认行为。

如果在共享一个成员的两个排序集合上运行`zinterstore`或`zunionstore`运算，但是该成员在每个集合中具有不同的分数，则可以使用`MIN`子选项强制操作在新集合中分配两个分数中的较低者。

    zinterstore BoyBandsWeightedMin 2 NewKids Nsync WEIGHTS 3 7 AGGREGATE MIN
    

由于这两个排序的集合只有一个具有相同分数（`3`）的匹配成员，因此此命令将创建一个新集合，其成员具有两个加权分数中的较低者：

    zscore BoyBandsWeightedMin "Joey"
    

    Output"9"
    

同样，`AGGREGATE`可以使用以下选项强制`zinterstore`或`zunionstore`分配两个分数中的较高者`MAX`：

    zinterstore BoyBandsWeightedMax 2 NewKids Nsync WEIGHTS 3 7 AGGREGATE MAX
    

此命令创建一个新集合，其中有一个成员，`"Joey"`具有两个加权得分中的较高者：

    zscore BoyBandsWeightedMax "Joey"
    

    Output"21"
    

将其`WEIGHTS`视为在分析成员之前临时操纵其分数的一种方式可能会有所帮助。同样，将`AGGREGATE`选项视为在将成员添加到新集中之前决定如何控制其分数的一种方式也很有帮助。

Conclusion
----------

本指南详细介绍了用于在Redis中创建和管理排序集的许多命令。如果您想在本指南中概述其他相关的命令，参数或过程，请在下面的评论中提出疑问或提出建议。

有关Redis命令的更多信息，请参阅关于[如何管理Redis数据库的](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8redis%E6%95%B0%E6%8D%AE%E5%BA%93)系列教程。