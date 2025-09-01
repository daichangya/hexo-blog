---
title: MapDB实现分析
id: 1555
date: 2024-10-31 22:02:01
author: daichangya
permalink: /archives/mapdb%E5%AE%9E%E7%8E%B0%E5%88%86%E6%9E%90/
tags: 
 - db
---

**MapDB****特性**

mapdb是一个内嵌的纯java的数据库，提供了并发的HashMap、TreeMap、Queue，可以基于堆外或者磁盘来存储数据。用户可以通过配置选择不同的机制来提高性能，比如可以配置多种不同的cache来减少反序列化的开销，提高读取性能；可以开启异步写引擎，使用后台线程来进行序列化和存储更新，来提高插入性能，减少rt。它支持ACID事务、MVCC隔离。它的代码精简，只有一个jar包，无其他依赖，总共才200kb。并且高度模块化，用户可以很容易的扩展，添加新特性。

**MapDB****架构**

从下面的类图，可以看出MapDB的整体脉络，它采用分层的设计，针对接口编程。上层只依赖下层的接口，具体实现可替换。顶层是针对用户的接口，也就是各种数据结构的接口。中间层是存储引擎Engine， 提供简单的key value接口，是MapDB的核心模块，管理对象为记录，通过记录id操作，用户不能直接使用。底层的是Volume，是对原始存储媒介的抽象，MapDB提供堆内、堆外、磁盘等存储媒介。这样的分层设计，使得MapDB的模块清晰，每一层都可以很容易的扩展，只需要实现接口即可。

  
![](http://dl2.iteye.com/upload/attachment/0094/9088/3401c751-cba9-39f6-8fb5-f12ccb522166.png)  
 

**MapDB****的实现原理**

以BTreeMap(Map)+StoreDirect(Engine)+FileChannelVol(Volume)为例，我们来分析MapDB的存储实现。

BTreeMap是B+树的一个实现，非叶子节点存储key，叶子节点存储实际的value。

B+树的核心操作为，从根节点开始，通过key找到对应的叶子节点，把节点读出，然后对节点中的Value进行增删改查操作。在单节点元素个数达到某个阈值后进行节点分裂或者合并。

在BTreeMap的实现中，每个节点作为一条记录在Engine中维护，引擎对外提供根据recid访问记录的接口，例如读接口Engine.get(long recid, Serializer<A> serializer)。BTreeMap只需要维护根节点recid就可以访问到整棵树。

StoreDirect通过维护一个索引Volume和一个物理Volume来实现基于recid的记录管理。

索引Volume用来维护索引项序列（每个索引项为8字节long），通过物理Volume来存储实际数据。每个索引项维护一个物理指针，信息包括记录所在的物理Volume的偏移量和记录大小。通过recid*8+IO\_USER\_START可以找到索引项，再通过索引项就可以找到记录所在物理Volume的位置和大小，这样就实现了通过recid访问记录的功能。

索引Volume（每个slot为8字节的long）物理Volume（每个格子为一个物理页，16*N byte，最大为64kb）

索引Volume还有一个功能是维护空闲的索引项列表和空闲的物理页列表（都是FIFO列表），这些空闲列表被称为Long stack，维护在索引Volume的第15到4111的slot中。当某个recid被删除，那么recid对应的索引项就成了空闲索引项，被加到空闲索引项列表里，对应的物理Volume空间也被释放，加入空闲的物理页列表。由于每个索引项的大小是固定的，所以只需要一个列表就可以维护所有的空闲项，索引Volume第15个slot用来维护空闲索引项列表。 

而每个物理页最小为16byte，最大为64kb（必须是16的倍数），不同的记录使用不同大小的物理页。每个记录删除之后，所释放的物理页大小可能都不一样。所以需要16-4111个slot来维护不同尺寸（4096种）的物理页空闲列表，每个slot指向对应尺寸的物理空闲页列表。

当要添加一条新记录的时候，会先查找空闲索引列表拿到recid，如果空闲索引列表不为空，那么复用该recid的索引项，否则在索引Volume append新的索引项，返回新的recid。拿到索引项之后，还要申请物理页空间，根据记录的大小找到对应的空闲物理页列表，如果有则复用，否则在物理Volume append，得到新的物理页，更新索引项，然后写入数据。物理页的分配方式，类似伙伴系统算法，可以减少外部碎片，充分利用空间。

当一条记录大于64kb的时候，需要通过链接法，链接多个物理页来存储记录。

在这个例子里我们使用的是FileChannelVol，所以索引Volume和物理Volume都是存储在文件中的，就是一个基于磁盘的B+树实现。

如果我们把FileChannelVol替换为MemoryVol，并启用useDirectBuffer，那么就是一个堆外的BTreeMap。

MapDB在Engine模块中还使用了装饰者模式，为引擎添加更多的特性。比如HashTable，为引擎添加Hash缓存；AsyncWriteEngine添加了异步写特性，如果使用堆外存储或者磁盘存储，启用异步写可以减小rt，提高性能。

对事务的支持，则是通过StoreWAL来实现，它继承StoreDirect，通过增加预写日志的特性来实现事务。

MapDB提供了丰富的功能，并且具有很强的扩展性，需要用到内嵌数据库或者堆外内存的场景，可以优先考虑哦。