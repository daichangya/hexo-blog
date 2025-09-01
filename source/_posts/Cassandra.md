---
title: Cassandra
id: 1334
date: 2024-10-31 22:01:51
author: daichangya
cover: https://images.jsdiff.com/unnamed_1587857226708.jpg
excerpt: "ApacheCassandra目录1历史1.1主要版本和主要改进[10]2数据模型3存储模型4分布式架构5支持的操作5.1轻量级事务6数据类型7与类似开源系统的比较7.1ApacheHBase8参考文献9相关阅读历史[编辑]Cassandra的名称来源于希腊神话，是特洛伊的一位悲剧性的女先知的名字，"
permalink: /archives/cassandra/
tags: 
 - nosql
---

**Apache Cassandra**

目录
--

*   [1 历史](#历史)
    *   [1.1 主要版本和主要改进\[10\]](#主要版本和主要改进[10])
*   [2 数据模型](#数据模型)
*   [3 存储模型](#存储模型)
*   [4 分布式架构](#分布式架构)
*   [5 支持的操作](#支持的操作)
    *   [5.1 轻量级事务](#轻量级事务)
*   [6 数据类型](#数据类型)
*   [7 与类似开源系统的比较](#与类似开源系统的比较)
    *   [7.1 Apache HBase](#Apache_HBase)
*   [8 参考文献](#参考文献)
*   [9 相关阅读](#相关阅读)

历史\[[编辑](/w/index.php?title=Cassandra&action=edit&section=1 "编辑章节：历史")\]
------------------------------------------------------------------------

Cassandra 的名称来源于[希腊神话](/wiki/%E5%B8%8C%E8%85%8A%E7%A5%9E%E8%AF%9D "希腊神话")，是[特洛伊](/wiki/%E7%89%B9%E6%B4%9B%E4%BC%8A "特洛伊")的一位悲剧性的女先知的名字，因此项目的[Logo](/wiki/Logo "Logo")是一只放光的眼睛。

这个项目由就职于[Facebook](/wiki/Facebook "Facebook")的Avinash Lakshman（也是[Amazon](/wiki/Amazon "Amazon") [Dynamo](/w/index.php?title=Amazon_DynamoDB&action=edit&redlink=1)（英语：[Amazon\_DynamoDB](https://en.wikipedia.org/wiki/Amazon_DynamoDB "en:Amazon DynamoDB")）的作者之一）和Prashant Malik在为[Facebook](/wiki/Facebook "Facebook")的Inbox编写。2008年，[Facebook](/wiki/Facebook "Facebook")将项目开源，Cassandra在2009年成为了[Apache软件基金会](/wiki/Apache%E8%BD%AF%E4%BB%B6%E5%9F%BA%E9%87%91%E4%BC%9A "Apache软件基金会")的Incubator项目，并在2010年2月走出孵化器，成为正式的基金会项目。当前这个项目主要由专门进行Cassandra商业化运作的[DataStax](http://www.datastax.com/)公司来开发，也有一些来自其他公司或独立的开发者[\[9\]](#cite_note-9)。

### 主要版本和主要改进[\[10\]](#cite_note-10)\[[编辑](/w/index.php?title=Cassandra&action=edit&section=2 "编辑章节：主要版本和主要改进[10]")\]

*   0.6，2010年4月发布，支持内置的缓存。
*   0.7，2011年1月发布，支持按列建二级索引(secondary indexes)及在线修改表的结构定义
*   0.8，2011年6月发布，支持CQL语言和零停机的在线升级
*   1.0，2011年10月发布，支持数据压缩，level compaction和提高读取性能
*   1.1，2012年4月发布，支持ssd和机械硬盘混合使用
*   1.2，2013年1月发布，支持虚拟节点(一个机器在一致性哈希环中拥有多个节点)、原子性的批处理
*   2.0，2013年9月发布，支持轻量级事务、触发器、改进compaction性能，强制使用[Java7](/w/index.php?title=Java7&action=edit&redlink=1 "Java7（页面不存在）")
*   2.1，2014年9月10日发布
*   2.2 , 2015年7月20日发布
*   3.0 , 2015年11月11日发布
*   3.1 , 同样 3.10版本，使用类tick-tock发布模式，每月发布一次 , 偶数编号版本提供新功能和错误修正，而奇数编号版本只包括错误修正。
*   3.11 ，2017年6月23日发布，作为稳定的3.11版本系列，修复了上一个tick-tock功能版本的错误。

数据模型
----------------------------------------------------------------------------

Cassandra使用了[Google](/wiki/Google "Google") 设计的 [BigTable](/wiki/BigTable "BigTable")的数据模型，与面向行(row)的传统的[关系型数据库](/wiki/%E5%85%B3%E7%B3%BB%E5%9E%8B%E6%95%B0%E6%8D%AE%E5%BA%93 "关系型数据库")或[键值存储](/wiki/%E9%8D%B5%E5%80%BC%E5%AD%98%E5%84%B2 "键值存储")的key-value数据库不同，Cassandra使用的是[宽列存储模型](/w/index.php?title=%E5%AE%BD%E5%88%97%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B&action=edit&redlink=1 "宽列存储模型（页面不存在）")(Wide Column Stores)[\[8\]](#cite_note-db-rank-8)，每行数据由row key唯一标识之后，可以有最多20亿个列[\[11\]](#cite_note-11)，每个列有一个column key标识，每个column key下对应若干value。这种模型可以理解为是一个二维的key-value存储，即整个数据模型被定义成一个类似map<key1, map<key2,value>>的类型。

旧版的Cassandra与客户端交互的方法是通过[thrift](/wiki/Thrift "Thrift")，而当前新版本的Cassandra采用与SQL语言类似的CQL语言[\[12\]](#cite_note-12)来实现数据模型的定义和数据的读写。其中BigTable中的列族(Column Family)在Cassandra中被称作类似关系型数据库中的称呼——表(table)，而Cassandra/BigTable中的row key和column key并称为主键(primary key)。[\[13\]](#cite_note-cqldoc-13)

Cassandra的row key决定了该行数据存储在哪些节点中，因此row key需要按哈希来存储，不能顺序的扫描或读取，而一个row内的column key是顺序存储的，可以进行有序的扫描或范围查找[\[13\]](#cite_note-cqldoc-13)。

存储模型
----------------------------------------------------------------------------

与BigTable和其模仿者[HBase](/wiki/HBase "HBase")不同，Cassandra的数据并不存储在分布式文件系统如[GFS](/wiki/GFS "GFS")或[HDFS](/wiki/HDFS "HDFS")中，而是直接存于本地。与BigTable一样，Cassandra也是日志型数据库，即把新写入的数据存储在内存的Memtable中并通过磁盘中的CommitLog来做持久化，内存填满后将数据按照key的顺序写进一个只读文件SSTable中，每次读取数据时将所有SSTable和内存中的数据进行查找和合并[\[14\]](#cite_note-14)[\[15\]](#cite_note-15)。这种系统的特点是写入比读取更快[\[16\]](#cite_note-benchmark-16)，因为写入一条数据是顺序计入commit log中，不需要随机读取磁盘以及搜索。

分布式架构
------------------------------------------------------------------------------

Cassandra的系统架构与[Dynamo](/w/index.php?title=Dynamo&action=edit&redlink=1 "Dynamo（页面不存在）")类似，是基于[一致性哈希](/wiki/%E4%B8%80%E8%87%B4%E6%80%A7%E5%93%88%E5%B8%8C "一致性哈希")的完全[P2P](/wiki/P2P "P2P")架构，每行数据通过哈希来决定应该存在哪个或哪些节点中[\[17\]](#cite_note-17)。集群没有master的概念，所有节点都是同样的角色，彻底避免了整个系统的单点问题导致的不稳定性，集群间的状态同步通过[Gossip协议](/w/index.php?title=Gossip%E5%8D%8F%E8%AE%AE&action=edit&redlink=1 "Gossip协议（页面不存在）")来进行P2P的通信。每个节点都把数据存储在本地，每个节点都接受来自客户端的请求。每次客户端随机选择集群中的一个节点来请求数据，对应接受请求的节点将对应的key在一致性哈希的环上定位是哪些节点应该存储这个数据，将请求转发到对应的节点上，并将对应若干节点的查询反馈返回给客户端。

在一致性、可用性和分区耐受能力（[CAP](/wiki/CAP "CAP")）的折衷问题上，Cassandra和Dynamo一样比较灵活。Cassandra的每个keyspace可配置一行数据会写入多少个节点(设这个数为N)，来保证数据不因为机器宕机或磁盘损坏而丢失数据，即保证了CAP中的P。用户在读写数据时可以指定要求成功写到多少个节点才算写入成功(设为W)，以及成功从多少个节点读取到了数据才算成功(设为R)。可推理得出，当W+R>N时，读到的数据一定是上一次写入的，即维护了[强一致性](/w/index.php?title=%E5%BC%BA%E4%B8%80%E8%87%B4%E6%80%A7&action=edit&redlink=1 "强一致性（页面不存在）")，确保了CAP中的C。当W+R<=N时，数据是[最终一致性](/w/index.php?title=%E6%9C%80%E7%BB%88%E4%B8%80%E8%87%B4%E6%80%A7&action=edit&redlink=1 "最终一致性（页面不存在）")因为存在一段时间可能读到的并不是最新版的数据。当W=N或R=N时，意味着系统只要有一个节点无响应或宕机，就有一部分数据无法成功写或者读，即失去了CAP中的可用性A。因此，大多数系统中，都将N设为3，W和R设为QUORUM，即“过半数”——在N为3时QUORUM是2。

支持的操作
------------------------------------------------------------------------------

Cassandra支持对一列数据进行insert、update、或delete操作。其中insert和update虽然语法略有区别，但语义上等价，即可以针对已经存在的行进行update或insert一个不存在的行。

### 轻量级事务
从2.0版开始，Cassandra支持轻量级事务。这种事务被称为“compare-and-set”，简称CAS。通过[paxos算法](/wiki/Paxos%E7%AE%97%E6%B3%95 "Paxos算法")实现在满足某条件后才修改数据否则不修改。当前支持"insert if not exist"、"update if col=value"、"delete if exist"等几种操作。

数据类型
----------------------------------------------------------------------------

Cassandra在CQL语言层面支持多种数据类型[\[18\]](#cite_note-18)。
| CQL类型     | 对应Java类型            | 描述|
|-----------|---------------------|-----------------------|
| ascii     | String              | ascii字符串|
| bigint    | long                | 64位整数|
| blob      | ByteBuffer/byte\[\] | 二进制数组|
| boolean   | boolean             | 布尔|
| counter   | long                | 计数器，支持原子性的增减，不支持直接赋值|
| decimal   | BigDecimal          | 高精度小数|
| double    | double              | 64位浮点数|
| float     | float               | 32位浮点数|
| inet      | InetAddress         | ipv4或ipv6协议的ip地址|
| int       | int                 | 32位整数|
| list      | List                | 有序的列表|
| map       | Map                 | 键值对|
| set       | Set                 | 集合|
| text      | String              | utf\-8编码的字符串|
| timestamp | Date                | 日期|
| uuid      | UUID                | UUID类型|
| timeuuid  | UUID                | 时间相关的UUID|
| varchar   | string              | text的别名|
| varint    | BigInteger          | 高精度整型|


与类似开源系统的比较
----------------------------------------------------------------------------------------

### Apache HBase

[HBase](/wiki/HBase "HBase")是Apache Hadoop项目的一个子项目，是[Google](/wiki/Google "Google") BigTable的一个克隆，与Cassandra一样，它们都使用了BigTable的列族式的数据模型，但是：

*   Cassandra只有一种节点，而HBase有多种不同角色，除了处理读写请求的region server之外，其架构在一套完整的[HDFS](/wiki/HDFS "HDFS")分布式文件系统之上，并需要[ZooKeeper](/wiki/ZooKeeper "ZooKeeper")来同步集群状态，部署上Cassandra更简单。
*   Cassandra的数据一致性策略是可配置的，可选择是强一致性还是性能更高的最终一致性；而HBase总是强一致性的。
*   Cassandra通过一致性哈希来决定一行数据存储在哪些节点，靠概率上的平均来实现负载均衡；而HBase每段数据(region)只有一个节点负责处理，由master来动态分配一个region是否大到需要拆分成两个，同时会将过热的节点上的一些region动态的分配给负载较低的节点，因此实现动态的负载均衡。
*   因为每个region同时只能有一个节点处理，一旦这个节点无响应，在系统将这个节点的所有region转移到其他节点之前这些数据便无法读写，加上master也只有一个节点，备用master的恢复也需要时间，因此HBase在一定程度上有单点问题；而Cassandra无单点问题。
*   Cassandra的读写性能优于HBase[\[16\]](#cite_note-benchmark-16)。

参考文献
-----------------------------------------------------------------------------

1.  **[^](#cite_ref-1 "跳转")** PlanetCassandra, [Apple Inc.: Cassandra at Apple for Massive Scale](https://www.youtube.com/watch?v=Bc4ql9TDzyg), 2015-03-03 \[2016-06-27\]
2.  **[^](#cite_ref-2 "跳转")** [Comcast messaging infrastructure chooses linearly scaling Apache Cassandra as NoSQL solution](http://www.planetcassandra.org/blog/interview/comcast-messaging-infrastructure-chooses-linearly-scaling-apache-cassandra-as-nosql-solution/). www.planetcassandra.org. \[2016-06-27\].
3.  **[^](#cite_ref-3 "跳转")** [Facebook’s Instagram: Making the Switch to Cassandra from Redis, a 75% ‘Insta’ Savings](http://planetcassandra.org/blog/interview/facebooks-instagram-making-the-switch-to-cassandra-from-redis-a-75-insta-savings/). planetcassandra.org. \[2016-06-27\].
4.  **[^](#cite_ref-4 "跳转")** [Spotify scales to the top of the charts with Apache Cassandra at 40k requests/second](http://planetcassandra.org/blog/interview/spotify-scales-to-the-top-of-the-charts-with-apache-cassandra-at-40k-requestssecond/). planetcassandra.org. \[2016-06-27\].
5.  **[^](#cite_ref-5 "跳转")** PlanetCassandra, [eBay: Apache Cassandra Best Practices at Ebay](https://www.youtube.com/watch?v=gn4MDRmrfKo), 2014-10-10 \[2016-06-27\]
6.  **[^](#cite_ref-6 "跳转")** [Rackspace Monitors the Cloud with Cassandra: 35 Million Writes, 180 Million Samples per Hour](http://planetcassandra.org/blog/post/rackspace-monitors-the-cloud-with-cassandra-35-million-writes-180-million-samples-per-hour). 2013-10-08 \[2016-06-27\].
7.  **[^](#cite_ref-7 "跳转")** [Case Study: Netflix](http://www.datastax.com/resources/casestudies/netflix). DataStax. \[2016-06-27\].
8.  ^ [跳转至： **8.0**](#cite_ref-db-rank_8-0) [**8.1**](#cite_ref-db-rank_8-1) [DB-Engines Ranking](http://db-engines.com/en/ranking). 2016-06-27.
9.  **[^](#cite_ref-9 "跳转")** [Cassandra Committers](https://web.archive.org/web/20140819085223/http://wiki.apache.org/cassandra/Committers). \[2014-08-17\]. （[原始内容](http://wiki.apache.org/cassandra/Committers)存档于2014-08-19）.
10.  **[^](#cite_ref-10 "跳转")** [Cassandra Changes](https://github.com/apache/cassandra/blob/trunk/CHANGES.txt).
11.  **[^](#cite_ref-11 "跳转")** [CassandraLimitations](https://web.archive.org/web/20140818132625/http://wiki.apache.org/cassandra/CassandraLimitations). \[2014-08-17\]. （[原始内容](http://wiki.apache.org/cassandra/CassandraLimitations)存档于2014-08-18）.
12.  **[^](#cite_ref-12 "跳转")** [Cassandra Query Language (CQL) v2.0](https://web.archive.org/web/20140815040820/http://cassandra.apache.org/doc/cql/CQL.html). 2014-08-18. （[原始内容](https://cassandra.apache.org/doc/cql/CQL.html)存档于2014-08-15）.
13.  ^ [跳转至： **13.0**](#cite_ref-cqldoc_13-0) [**13.1**](#cite_ref-cqldoc_13-1) [cql document](https://web.archive.org/web/20140819084919/http://www.datastax.com/documentation/cql/3.1/cql/ddl/ddl_intro_c.html). \[2014-08-17\]. （[原始内容](http://www.datastax.com/documentation/cql/3.1/cql/ddl/ddl_intro_c.html)存档于2014-08-19）.
14.  **[^](#cite_ref-14 "跳转")** [Bigtable: A Distributed Storage System for Structured Data](http://static.googleusercontent.com/media/research.google.com/en//archive/bigtable-osdi06.pdf) (PDF).
15.  **[^](#cite_ref-15 "跳转")** [MemtableSSTable](https://web.archive.org/web/20140819085851/http://wiki.apache.org/cassandra/MemtableSSTable). \[2014-08-17\]. （[原始内容](http://wiki.apache.org/cassandra/MemtableSSTable)存档于2014-08-19）.
16.  ^ [跳转至： **16.0**](#cite_ref-benchmark_16-0) [**16.1**](#cite_ref-benchmark_16-1) [nosql-performance-benchmarks](http://planetcassandra.org/nosql-performance-benchmarks/).
17.  **[^](#cite_ref-17 "跳转")** Amazon. [Dynamo: Amazon’s Highly Available Key-value Store](http://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf) (PDF).
18.  **[^](#cite_ref-18 "跳转")** [cql data types](https://web.archive.org/web/20140929225604/http://www.datastax.com/documentation/cql/3.1/cql/cql_reference/cql_data_types_c.html). \[2014-08-18\]. （[原始内容](http://www.datastax.com/documentation/cql/3.1/cql/cql_reference/cql_data_types_c.html)存档于2014-09-29）.
