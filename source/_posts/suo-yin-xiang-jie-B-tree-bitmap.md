---
title: 索引详解（B-tree、bitmap）
id: 1446
date: 2024-10-31 22:01:56
author: daichangya
permalink: /archives/suo-yin-xiang-jie-B-tree-bitmap/
tags:
- mysql
---


# 索引概述

索引是一种可选创建的数据库对象，建立在表的一列或多列的辅助对象。可以将索引比喻成一本书的目录，通过目录我们能快速的找到我们所需的内容。而数据库索引的主要功能也就是用来提高查询速度以及完整性检查。书的目录将书的名称和页码作为目录，同样的，数据库的索引通常将列值连同ROWID存储在一起，ROWID包含了存储列值的表在磁盘中的物理位置（这里涉及到磁盘的存储方式等内容，学习后记得补上），通过ROWID，Oracle可以以最小的代价快速的检索到相应的内容。如果没有索引，数据库就必须进行全表扫描来查看是否包含数据。但是创建索引也有一定代价，一方面，列值修改的同时也要修改索引以确保索引与列值的相同，另一方面，索引也消耗了磁盘空间以及系统资源。因此创建索引时要保障其合理性。

# B树索引

通常创建的索引一般都是B-TREE（B树）索引，一般有聚集索引和非聚集索引。

网上有一结构图很形象的表示了B树的原理，参考如下：

        ![](https://images0.cnblogs.com/blog/596298/201402/121509264715918.png)

索引有键值和逻辑指针构成。更节点中的0、500、1000指的是所链接的键值的最小值，B1、B2、B3只分支节点块的地址。

聚集索引和非聚集索引的区别在于表记录的排列顺序是否和索引的排列顺序一致，实际的原理就在于聚集索引的叶子节点就是数据节点，而非聚集索引的叶子节点为每一真正数据行存储的“键值对”，并且还包含一个指针偏移量，根据页指针及指针偏移量，就能定位到具体的数据行。

通过以上原理可以知道，聚集索引查询速度较快，但因为要保证表记录的排列顺序与索引意志，在修改表记录的同时也要更新索引数据，因此进行修改的速度较慢。把记录插入到相应的位置必须在索引的数据也中全部重排，也降低了执行速度。非聚集索引指定了索引中的逻辑顺序，但记录的物理顺序和索引顺序不一致。Oracle默认是非聚集索引，sqlServer则默认为每一个主键创建聚集索引。由于表的物理顺序只有一种，因此每张表也只能有一种聚集索引。

# 位图索引

Bitmap索引即位图索引，位图索引是适用于候选值较少却又广泛出现，但不频繁更新的列，比如性别等。

以下有一张表：

<table style="width: 452px;" border="1" cellspacing="0" cellpadding="0"><tbody><tr><td valign="top" width="151"><p>编号</p></td><td valign="top" width="151"><p>婚否</p></td><td valign="top" width="151"><p>性别</p></td></tr><tr><td valign="top" width="151"><p>张三</p></td><td valign="top" width="151"><p>未</p></td><td valign="top" width="151"><p>女</p></td></tr><tr><td valign="top" width="151"><p>李四</p></td><td valign="top" width="151"><p>已</p></td><td valign="top" width="151"><p>男</p></td></tr><tr><td valign="top" width="151"><p>钱五</p></td><td valign="top" width="151"><p>未</p></td><td valign="top" width="151"><p>男</p></td></tr></tbody></table>

转为位图则是：

<table style="width: 301px;" border="1" cellspacing="0" cellpadding="0"><tbody><tr><td valign="top" width="151"><p>女</p></td><td valign="top" width="151"><p>男</p></td></tr><tr><td valign="top" width="151"><p>1</p></td><td valign="top" width="151"><p>0</p></td></tr><tr><td valign="top" width="151"><p>0</p></td><td valign="top" width="151"><p>1</p></td></tr><tr><td valign="top" width="151"><p>0</p></td><td valign="top" width="151"><p>1</p></td></tr></tbody></table>

<table style="width: 301px;" border="1" cellspacing="0" cellpadding="0"><tbody><tr><td valign="top" width="151"><p>已婚</p></td><td valign="top" width="151"><p>未婚</p></td></tr><tr><td valign="top" width="151"><p>0</p></td><td valign="top" width="151"><p>1</p></td></tr><tr><td valign="top" width="151"><p>1</p></td><td valign="top" width="151"><p>0</p></td></tr><tr><td valign="top" width="151"><p>0</p></td><td valign="top" width="151"><p>1</p></td></tr></tbody></table>

即性别为男的向量为：011，性别为女的向量为100，已婚向量为010，未婚向量为101。则通过向量之间的位运算（异或：相同为0，不同为1）获得结果集为：

<table border="1" cellspacing="0" cellpadding="0"><tbody><tr><td valign="top" width="160"><p align="center">女</p></td><td valign="top" width="160"><p align="center">已婚111</p></td><td valign="top" width="160"><p align="center">未婚110</p></td></tr><tr><td valign="top" width="160"><p align="center">男</p></td><td valign="top" width="160"><p align="center">已婚101</p></td><td valign="top" width="160"><p align="center">未婚001</p></td></tr></tbody></table>

执行sql语句：select * from t where 性别 like ’女’ and 婚否like ‘未’获得的向量对着结果集就是结果。位图索引的操作实际上是通过位运算获得最符合的叶子节点，然后不断向上扫描的到的，而B树索引则是通过从根节点开始不断往下扫描得到。

#### 另：关于复合索引　

创建索引：

Create index on t (name,id,sex);

执行查询操作：

Select * from t where name =’zhang’ and sex like ‘male’;

这时查询不再扫描全表，而是直接从索引中拿数据。这就是覆盖式索引。通常根据where

后的条件建里复合索引。

有一点要注意：

Select * from t where name =’zhang’ ;

Select * from t where sex like ‘male’;

执行这两个sql语句时，虽然where后的条件列值建立了复合索引，但只对起始列有效，非起始列则无用。

#### 索引的限制条件：

1.  使用不等于（<>）操作符，数据库仍然执行全表扫描。可用or替代。
2.  使用null、not null关键字，因为数据库对null并没有定义，所以建索引时需要将索引的列设为非空值
3.  使用函数，如果没有基于函数本身的索引，则索引无法执行。但是将函数应用在索引上则可以执行。比如：select * from t where  date =to_date(’1998-3-27’, ‘yyyy-mm-dd’);
4.  比较类型不匹配数据类型，比如一个varchar2类型和integer类型
5.  使用like‘%X%’进行模糊查询

 参考：[http://www.cnblogs.com/kissknife/archive/2009/03/30/1425534.html](http://www.cnblogs.com/kissknife/archive/2009/03/30/1425534.html)

　　　 [http://blog.itpub.net/17203031/viewspace-695055/](http://blog.itpub.net/17203031/viewspace-695055/)
