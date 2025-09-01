---
title: MySQL和Lucene索引对比分析
id: 1548
date: 2024-10-31 22:02:01
author: daichangya
permalink: /archives/MySQL-he-Lucene-suo-yin-dui-bi-fen-xi/
tags:
- mysql
- lucene
---



MySQL和Lucene都可以对数据构建索引并通过索引查询数据，一个是关系型数据库，一个是构建搜索引擎（Solr、ElasticSearch）的核心类库。两者的索引（index）有什么区别呢？以前写过一篇《[Solr与MySQL查询性能对比](http://www.cnblogs.com/luxiaoxun/p/4696477.html)》，只是简单的对比了下查询性能，对于内部原理却没有解释，本文简单分析下两者的索引区别。

**MySQL索引实现**

在MySQL中，索引属于存储引擎级别的概念，不同存储引擎对索引的实现方式是不同的，本文主要讨论MyISAM和InnoDB两个存储引擎的B+Tree索引实现方式（HASH索引不能使用范围查询，只支持等值比较查询，不在此文章讨论）。

**MyISAM索引实现**

MyISAM引擎使用B+Tree作为索引结构，叶节点的data域存放的是数据记录的地址。下图是MyISAM索引的原理图：

![](https://images2015.cnblogs.com/blog/434101/201605/434101-20160502154525763-666682601.png)

图1是一个MyISAM表的主索引（Primary key）示意。可以看出MyISAM的索引文件仅仅保存数据记录的地址。在MyISAM中，主索引和辅助索引（Secondary key）在结构上没有任何区别，只是主索引要求key是唯一的，而辅助索引的key可以重复。B+Tree的所有叶子节点包含所有关键字且是按照升序排列的。

MyISAM表的索引和数据是分离的，索引保存在”表名.MYI”文件内，而数据保存在“表名.MYD”文件内。

MyISAM的索引方式也叫做“非聚集”的，之所以这么称呼是为了与InnoDB的聚集索引区分。

**InnoDB索引实现**

虽然InnoDB也使用B+Tree作为索引结构，但具体实现方式却与MyISAM截然不同。

第一个重大区别是InnoDB的数据文件本身就是索引文件。从上文知道，MyISAM索引文件和数据文件是分离的，索引文件仅保存数据记录的地址。而在InnoDB中，表数据文件本身就是按B+Tree组织的一个索引结构，这棵树的叶节点data域保存了完整的数据记录。这个索引的key是数据表的主键，因此InnoDB表数据文件本身就是主索引。

![](https://images2015.cnblogs.com/blog/434101/201605/434101-20160502154622232-2102383628.png)

图2是InnoDB主索引（同时也是数据文件）的示意图，可以看到叶节点包含了完整的数据记录。这种索引叫做聚集索引。因为InnoDB的数据文件本身要按主键聚集，所以InnoDB要求表必须有主键（MyISAM可以没有），如果没有显式指定，则MySQL系统会自动选择一个可以唯一标识数据记录的列作为主键，如果不存在这种列，则MySQL自动为InnoDB表生成一个隐含字段作为主键，这个字段长度为6个字节，类型为长整形。

第二个与MyISAM索引的不同是InnoDB的辅助索引data域存储相应记录主键的值而不是地址。换句话说，InnoDB的所有辅助索引都引用主键作为data域。例如，图3为定义在Col3上的一个辅助索引：

![](https://images2015.cnblogs.com/blog/434101/201605/434101-20160502154647216-666186254.png)

这里以英文字符的ASCII码作为比较准则。聚集索引这种实现方式使得按主键的搜索十分高效，但是辅助索引搜索需要检索两遍索引：首先检索辅助索引获得主键，然后用主键到主索引中检索获得记录。

了解不同存储引擎的索引实现方式对于正确使用和优化索引都非常有帮助，例如知道了InnoDB的索引实现后，就很容易明白为什么不建议使用过长的字段作为主键，因为所有辅助索引都引用主索引，过长的主索引会令辅助索引变得过大。再例如，用非单调的字段作为主键在InnoDB中不是个好主意，因为InnoDB数据文件本身是一颗B+Tree，非单调的主键会造成在插入新记录时数据文件为了维持B+Tree的特性而频繁的分裂调整，十分低效，而使用自增字段作为主键则是一个很好的选择。

讲MySQL索引的实现的文章很多，以上也是参考了《MySQL索引背后的数据结构及算法原理》，现在来看看Lucene的索引原理。

**Lucene索引实现**

Lucene的索引不是B+Tree组织的，而是倒排索引，Lucene的倒排索引由Term index，Team Dictionary和Posting List组成。

![](https://images2015.cnblogs.com/blog/434101/201605/434101-20160502154740669-1992480149.jpg)

有倒排索引（invertedindex）就有正排索引（forwardindex），正排索引就是文档（Document）和它的字段Fields正向对应的关系：

<table style="width: 553px" border="1" cellspacing="0" cellpadding="0"><tbody><tr><td valign="top" width="138"><p align="left">DocID</p></td><td valign="top" width="138"><p align="left">name</p></td><td valign="top" width="138"><p align="left">sex</p></td><td valign="top" width="138"><p align="left">age</p></td></tr><tr><td valign="top" width="138"><p align="left">1</p></td><td valign="top" width="138"><p align="left">jack</p></td><td valign="top" width="138"><p align="left">男</p></td><td valign="top" width="138"><p align="left">18</p></td></tr><tr><td valign="top" width="138"><p align="left">2</p></td><td valign="top" width="138"><p align="left">lucy</p></td><td valign="top" width="138"><p align="left">女</p></td><td valign="top" width="138"><p align="left">17</p></td></tr><tr><td valign="top" width="138"><p align="left">3</p></td><td valign="top" width="138"><p align="left">peter</p></td><td valign="top" width="138"><p align="left">男</p></td><td valign="top" width="138"><p align="left">17</p></td></tr></tbody></table>

倒排索引是字段Field和拥有这个Field的文档对应的关系:

Sex字段：

<table style="width: 553px" border="1" cellspacing="0" cellpadding="0"><tbody><tr><td valign="top" width="277"><p align="left">男</p></td><td valign="top" width="277"><p align="left">[1,3]</p></td></tr><tr><td valign="top" width="277"><p align="left">女</p></td><td valign="top" width="277"><p align="left">[2]</p></td></tr></tbody></table>

Age字段：

<table style="width: 553px" border="1" cellspacing="0" cellpadding="0"><tbody><tr><td valign="top" width="277"><p align="left">18</p></td><td valign="top" width="277"><p align="left">[1]</p></td></tr><tr><td valign="top" width="277"><p align="left">17</p></td><td valign="top" width="277"><p align="left">[2，3]</p></td></tr></tbody></table>

Jack，lucy或者17,18这些叫做term，而\[1,3\]就是posting list。Posting list就是一个int型的数组，存储了所有符合某个term的文档id。那么什么是Term index和Term dictionary？

如上，假设name字段有很多个term，比如：**Carla,Sara,Elin,Ada,Patty,Kate,Selena**

如果按照这样的顺序排列，找出某个特定的term一定很慢，因为term没有排序，需要全部过滤一遍才能找出特定的term。排序之后就变成了：**Ada,Carla,Elin,Kate,Patty,Sara,Selena**

这样就可以用二分查找的方式，比全遍历更快地找出目标的term。如何组织这些term的方式就是 Term dictionary，意思就是term的字典。有了Term dictionary之后，就可以用比较少的比较次数和磁盘读次数查找目标。但是磁盘的随机读操作仍然是非常昂贵的，所以尽量少的读磁盘，有必要把一些数据缓存到内存里。但是整个Term dictionary本身又太大了，无法完整地放到内存里。于是就有了Term index。Term index有点像一本字典的大的章节表。比如：

A开头的term ……………. Xxx页

C开头的term ……………. Xxx页

E开头的term ……………. Xxx页

如果所有的term都是英文字符的话，可能这个term index就真的是26个英文字符表构成的了。但是实际的情况是，term未必都是英文字符，term可以是任意的byte数组。而且26个英文字符也未必是每一个字符都有均等的term，比如x字符开头的term可能一个都没有，而s开头的term又特别多。实际的term index是一棵trie 树：

![](https://images2015.cnblogs.com/blog/434101/201605/434101-20160502154845794-1895604786.png)

上图例子是一个包含 "A", "to", "tea", "ted", "ten", "i", "in", 和 "inn" 的trie树。这棵树不会包含所有的term，它包含的是term的一些前缀。通过term index可以快速地定位到term dictionary的某个offset，然后从这个位置再往后顺序查找。再加上一些压缩技术（想了解更多，搜索 Lucene Finite State Transducers），Term index的尺寸可以只有所有term的尺寸的几十分之一，使得用内存缓存整个term index变成可能。整体上来说就是这样的效果:

![](https://images2015.cnblogs.com/blog/434101/201605/434101-20160502154907357-189345550.jpg)

由Term index到Term Dictionary，再到Posting List，通过某个字段的关键字去查询结果的过程就比较清楚了，通过多个关键字的Posting List进行AND或者OR进行交集或者并集的查询也简单了。

对比MySQL的B+Tree索引原理，可以发现：

1）Lucene的Term index和Term Dictionary其实对应的就是MySQL的B+Tree的功能，为关键字key提供索引。Lucene的inverted index可以比MySQL的b-tree检索更快。

2）Term index在内存中是以FST（finite state transducers）的形式保存的，其特点是非常节省内存。所以Lucene搜索一个关键字key的速度是非常快的，而MySQL的B+Tree需要读磁盘比较。

3）Term dictionary在磁盘上是以分block的方式保存的，一个block内部利用公共前缀压缩，比如都是Ab开头的单词就可以把Ab省去。这样Term dictionary可以比B-tree更节约磁盘空间。

4）Lucene对不同的数据类型采用了不同的索引方式，上面分析是针对field为字符串的，比如针对int，有TrieIntField类型，针对经纬度，就可以用GeoHash编码。

5）在 Mysql中给两个字段独立建立的索引无法联合起来使用，必须对联合查询的场景建立复合索引，而Lucene可以任何AND或者OR组合使用索引进行检索。

参考：

《MySQL索引背后的数据结构及算法原理》: [http://blog.codinglabs.org/articles/theory-of-mysql-index.html](http://blog.codinglabs.org/articles/theory-of-mysql-index.html)

http://stackoverflow.com/questions/4628571/solr-date-field-tdate-vs-date

http://lucene.apache.org/core/

