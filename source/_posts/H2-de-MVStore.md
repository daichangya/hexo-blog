---
title: H2的MVStore
id: 1522
date: 2024-10-31 22:01:59
author: daichangya
permalink: /archives/H2-de-MVStore/
categories:
- 数据结构
---

翻译自[http://www.h2database.com/html/mvstore.html](http://www.h2database.com/html/mvstore.html "http://www.h2database.com/html/mvstore.html")

转载请著名出处，及译者信息。

第一次翻译，诸多不妥请谅解，谢谢。

# 概述

MVStore是一个持久化的、日志结构式的kv存储。本计划用它作为H2的下一代存储子系统，但你也可以在一个不涉及JDBC或者SQL的应用中直接使用它。

*   MVStore代表多版本存储。
*   每一个store包含大量的map，这些map可以用java.util.Map接口存取。
*   支持基于文件存储和基于内存的操作。
*   它希望更快，更简单的使用，更小。
*   支持并发读写操作。
*   支持事务(包括并发事务与两阶段提交(2-phase commit))
*   模块化的工具，支持插拔式的数据类型定义、序列化实现，支持插拔式的存储载体(存到文件里、存到堆外内存)，插拔式的映射实现(B-tree,R-tree,当前用的concurrent B-tree),BLOB存储，文件系统层的抽象以使其支持文件的加密与压缩

# 示例代码

```
import org.h2.mvstore.*;

// open the store (in-memory if fileName is null)
MVStore s = MVStore.open(fileName);

// create/get the map named "data"
MVMap<Integer, String> map = s.openMap("data");

// add and read some data
map.put(1, "Hello World");
System.out.println(map.get(1));

// close the store (this will persist changes)
s.close();
```

下面的代码展示了如何使用这些工具

# Store Builder

MVStore.Builder提供了一个流畅优美的用可选配置项构造store的接口

示例用法：

```
MVStore s = new MVStore.Builder().
    fileName(fileName).
    encryptionKey("007".toCharArray()).
    compress().
    open();
```

可用选项的列表如下：

*   autoCommitBufferSize: 写buffer的大小.
*   autoCommitDisabled: 禁用自动commit.
*   backgroundExceptionHandler: 用于处理后台写入时产生的异常的处理器.
*   cacheSize: 缓存大小，以MB为单位.
*   compress: 是否采用LZF算法进行快速压缩.
*   compressHigh: 是否采用Deflate算法进慢速速压缩.
*   encryptionKey: 文件加密的key.
*   fileName: 基于文件存储时，用于存储的文件名.
*   fileStore: 存储实现.
*   pageSplitSize: pages的分割点.
*   readOnly: 是否以只读形式打开存储文件.

# R-Tree

MVRTreeMap是一个用于快速的R-Tree实现，使用示例如下：

```
// create an in-memory store
MVStore s = MVStore.open(null);

// open an R-tree map
MVRTreeMap<String> r = s.openMap("data",
        new MVRTreeMap.Builder<String>());

// add two key-value pairs
// the first value is the key id (to make the key unique)
// then the min x, max x, min y, max y
r.add(new SpatialKey(0, -3f, -2f, 2f, 3f), "left");
r.add(new SpatialKey(1, 3f, 4f, 4f, 5f), "right");

// iterate over the intersecting keys
Iterator<SpatialKey> it =
        r.findIntersectingKeys(new SpatialKey(0, 0f, 9f, 3f, 6f));
for (SpatialKey k; it.hasNext();) {
    k = it.next();
    System.out.println(k + ": " + r.get(k));
}
s.close();
```

默认维度是2，new MVRTreeMap.Builder<String>().dimensions(3)这样可以设置一个不同的维度数，维度的取值最大值是32，最小值是1.

# 特性

## Maps

每一个store含有一组命名map。每个map按key存储，支持通用查找操作，比如查找第一个，查找最后一个，迭代部分或者全部的key等等等。

也支持一些不太通用的操作：快速的按索引查找、高效的根据key算出其索引(位置、index)。也就是意味着取中间的两个key也是非常快的，也能快速统计某个范围内的key。The iterator supports fast skipping. This is possible because internally, each map is organized in the form of a counted B+-tree.

在数据库侧，一个map能被一张表一样使用，map的key就是表的主键，map的值就是表的行。map也能代表索引，map的key相当于索引的key，map的值相当于表的主键(针对那种非联合索引，map的key需含有主键字段)

## 版本

版本是指在 指定时间的所有map中所有数据的一个快照。创建快照的速度很快：仅仅复制上一个快照后发生改变的page。这种行为通常也叫作COW(copy on write)。旧版本变成只读的。支持回滚到一个旧版本。

下面的示例代码展示了如何创建一个store，打开一个map，增加一些数据和存取当前的以及旧版本的数据：

```
// create/get the map named "data"
MVMap<Integer, String> map = s.openMap("data");

// add some data
map.put(1, "Hello");
map.put(2, "World");

// get the current version, for later use
long oldVersion = s.getCurrentVersion();

// from now on, the old version is read-only
s.commit();

// more changes, in the new version
// changes can be rolled back if required
// changes always go into "head" (the newest version)
map.put(1, "Hi");
map.remove(2);

// access the old data (before the commit)
MVMap<Integer, String> oldMap =
        map.openVersion(oldVersion);

// print the old version (can be done
// concurrently with further modifications)
// this will print "Hello" and "World":
System.out.println(oldMap.get(1));
System.out.println(oldMap.get(2));

// print the newest version ("Hi")
System.out.println(map.get(1));
```

# 事务

支持多路并发开启事务，TransactionStore实现了事务功能,其支持PostgreSQL的带savepoints的事务隔离级别得读提交(read committed),两阶段提交，其他数据的一些经典特性。事务的大小没有限制(针对大的或者长时间运行的事务，其日志被写到磁盘上)

# 基于内存形式的性能和用量

基于内存操作的性能约比java.util.TreeMap慢50%。

The memory overhead for large maps is slightly better than for the regular map implementations, but there is a higher overhead per map. For maps with less than about 25 entries, the regular map implementations need less memory.

如果没有指定文件名，存储的操作将是纯内存形式的，这种模式下支持除持久化之外的所有操作(多版本，索引查找，R-Tree等等)。如果自定义了文件名，在数据持久化之前的所有操作都发生在内存中。

正如所有的map实现一样，所有的key是不可变的，这意味着实体被加入map之后就不允许改变key对象了。如果指定了文件名，在实体加入map之后其value对象也是允许被修改的，因为value或许已经被序列化了（当打开自动commit时序列化会随时发生）。

# 可插拔的数据类型

序列化方式是可插拔的。目前的默认的序列化方式支持许多普通的数据类型，针对其他的对象类型使用了java的序列化机制。下面这些类型是可以直接被支持的：Boolean, Byte, Short, Character, Integer, Long, Float, Double, BigInteger, BigDecimal, String, UUID, Date和数组(基本类型数组和对象数组)。For serialized objects, the size estimate is adjusted using an exponential moving average.

支持泛型数据类型。

存储引擎自身没有任何长度限制，所以key，value，page和chunk可以很大很大，而且针对map和chunk的数量也没有固定的限制。因为使用了日志结构存储，所以针对大的key和page也无需特殊的处理。

# BLOB支持

支持大的二进制对象存储，方式是将其分隔成更小的块。这样就能存储内存里放不下的对象。Streaming as well as random access reads on such objects are supported. This tool is written on top of the store, using only the map interface.

# R-Tree和可插拔的map实现

map的具体实现是可插拔的，目前默认实现是MVMap，here is a multi-version R-tree map implementation for spatial operations.

并发操作和缓存

支持并发读写。所有的读操作可以并行发生。支持与从文件系统中并发读一样的从page cache中 并发读。写操作首先将关联的page从磁盘读取到内存（这个可以并发执行），然后再修改数据，内存部分的写操作是同步的。将变化写入文件和将变化写入快照一样都可以并发的修改数据。

在page级别做了缓存，是一个并发的LIRS 缓存(LIRS 可以减少扫描)

For fully scalable concurrent write operations to a map (in-memory and to disk), the map could be split into multiple maps in different stores ('sharding'). The plan is to add such a mechanism later when needed.

# 日志结构化存储

在内部，变更被缓存在内存。一旦变更累积到一定程度，这些变更将被一组连续的写操作写入磁盘。与传统的数据库存储引擎相比，这对不支持高性能随机写的文件系统和存储系统像SSD一样提升了写入性能According to a test, write throughput of a common SSD increases with write block size, until a block size of 2 MB, and then does not further increase.)默认情况下，当大量pages被修改时，这些修改会被自动写入，一个后台线程每秒写一次。也可以通过调用commit方法直接出发写操作。

存储的时候，所有的变更将被序列化，LZF压缩算法是可选的，然后顺序的写入到文件的空闲区域。**每一次的变更集合被称之为chunk。**修改过的B-tree的所有父page也是用chunk存储，以使得每一个chunk也含有每一个修改过的map的root page(指读取这个版本数据的入口点) 。这里没有区分开索引：所有的数据被当做一个页列表存储。每次存储, 有一个额外的包含了元数据的map ( 每个map的root page,和chunk列表在哪里).

针对每个chunk通常有两次写操作：一次存储chunk数据(pages)，另一个是更新文件header（它指向最近的chunk）。如果chunk被合并到文件的末尾，文件header仅会被写在chunk的末尾。这里没有事务日志，没有undo日志，也没有in-place updates ???，（然而，未被使用的chunk默认将被写覆盖）。

老的数据将被保持45s(可以配置)，以至于没有显式的需要同步操作去保证数据一致。在需要的时候也可以显式的同步操作。为了重新使用磁盘空间，具有最少活动数据量的chunk将被压缩(compacted )（活动数据被再一次存储在下一个chunk中）。为了改善数据locality (定位？？)和磁盘使用率，计划将消除数据碎片并压缩数据。

相对于传统的存储引擎(使用事务日志，undo日志和主存储区域)，日志结构化存储是简单的，更灵活，而且每次修改需要更少的磁盘操作，因为数据仅仅被写一次，不像传统的存储引擎要写2次或者3次，再有，B-tree页通常是紧凑的(他们相互挨着存储)所以很容易被压缩。但是，目前临时地，磁盘使用率实际会比常规的数据库高一点，磁盘空间不会立即被重复使用(因为没有in-place updates)。

# 堆外存储和可插拔存储

存储是可插拔的。除了被用到的纯内存操作, 默认的存储是一个文件。

目前有一个可用的堆外存储实现。 这个存储将数据保存在堆外内存中， 意味着脱离了正常的堆的垃圾收集能力。这样就可以允许在不增加jvm堆的不增加GC回收停顿的情况下使用大量的内存存储。使用了ByteBuffer.allocateDirect来分配内存。一次分配一个chunk，一个chunk通常是数兆MB大小, 以使得分配的成本很低。若使用堆外存储，调用：

```
OffHeapStore offHeap = new OffHeapStore();
MVStore s = new MVStore.Builder().
 fileStore(offHeap).open();
```

# 文件系统抽象，文件锁和在线备份

文件系统是可插拔的。同样的文件系统抽象被用在H2中。文件能使用加密的文件系统加密。其他的文件系统实现支持从压缩的zip或者jar file中读取。文件系统的抽象紧密匹配了Java7文件系统操作的API。

每一个存储在一个JVM中仅会被打开一次。当打开一个存储时，文件以排他形式被锁定，以至于文件仅能被一个进程修改。文件若以只读模式打开，那么共享锁将被使用。

被持久化的数据时刻会被备份，甚至在写操作的时候(在线备份)。为了这么做，磁盘空间自动重用将被禁用，以使得新的数据一致被拼接在文件的末尾。然后，文件将被拷贝。文件句柄对应用可用。 推荐使用FileChannelInputStream 做这事。针对加密数据库，加密的文件一样能被备份。

# Encrypted Files

文件加密确保仅通过正确的密码才能读取数据。数据能被以如下方式加密：

```
MVStore s = new MVStore.Builder().
    fileName(fileName).
    encryptionKey("007".toCharArray()).
    open();
```

下面的算法和设置将被使用:

密码字符数组在使用后将被清理，是为了减少被窃取的风险甚至被攻击后存取主内存。

密码使用SHA-256 算法 使用PBKDF2标准hash编码。

salt 的长度是64位，使得攻击者不能使用预计算密码hash表的方式。他通过一个安全的随机数生成器生成。  
为了提升在android上打开加密存储的速度，PBKDF2 迭代数量是10.这个值越高，对暴力密码攻击的保护越好，但是打开文件就越慢。

文件自身加密使用标准的磁盘加密形式XTS-AES。 Only little more than one AES-128 round per block is needed.  

# Tools工具

有一个MVStoreTool,用来dump 文件contents。

# 异常处理

工具不会抛出受检异常。取而代之的是，若需要的话会跑出未受检异常。如下异常可能发生:

**IllegalStateException** if a map was already closed or an IO exception occurred, for example if the file was locked, is already closed, could not be opened or closed, if reading or writing failed, if the file is corrupt, or if there is an internal error in the tool. For such exceptions, an error code is added so that the application can distinguish between different error cases.  
**IllegalArgumentException** if a method was called with an illegal argument.  
**UnsupportedOperationException** if a method was called that is not supported, for example trying to modify a read-only map.  
ConcurrentModificationException if a map is modified concurrently.  

# H2的存储引擎

H2 1.4之后的版本(含1.4)默认使用MVStore作为存储引擎 (支持 SQL, JDBC, transactions, MVCC等等).针对老版本, 将;MV_STORE=TRUE拼接到database URL后面. Even though it can be used with the default table level locking, by default the MVCC mode is enabled when using the MVStore.

# 文件格式

  
数据被存储到文件里. 文件有两个(出于安全起见)文件头和大量的chunk. 每个文件头是一个4096 bytes的块.每个chunk至少一个块，但是通常是 200个或者更多个块. 数据已日志结构存储的形式存储在chunk中. 每个版本都有一个chunk。.

```
[ file header 1 ] [ file header 2 ] [ chunk ] [ chunk ] ... [ chunk ]
```

  
每一个chunk含有大量的B-Tree page，示例代码如下：

```
MVStore s = MVStore.open(fileName);
MVMap<Integer, String> map = s.openMap("data");
for (int i = 0; i < 400; i++) {
    map.put(i, "Hello");
}
s.commit();
for (int i = 0; i < 100; i++) {
    map.put(0, "Hi");
}
s.commit();
s.close();
```

  
结果是两个chunks (不包含metadata):

Chunk 1:  
\- Page 1: (root) node with 2 entries pointing to page 2 and 3  
\- Page 2: leaf with 140 entries (keys 0 - 139)  
\- Page 3: leaf with 260 entries (keys 140 - 399)  
Chunk 2:  
\- Page 4: (root) node with 2 entries pointing to page 3 and 5  
\- Page 5: leaf with 140 entries (keys 0 - 139)  
这意味着每个chunk含有一个版本的变更: 新版本的变更page和它的父page, 递归直至根page. 后来的page指向被早期的page引用。

# 文件header

这两有两个文件头，通常含有相同的数据. 但在某个文件头被更新的某一片刻, 写操作可能部分失败. 这就是为什么有第二个文件头的原因.(???) 文件头采用in-place update更新方式。文件头包含如下数据:

```
H:2,block:2,blockSize:1000,chunk:7,created:1441235ef73,format:1,version:7,fletcher:3044e6cc
```

  
这些数据被以键值对的形式存储. 其值都是以十六进制形式存储。

这些字段是:

H: H:2表示是H2数据库  
block: 最新的chunk的block的数量 (but not necessarily the newest???).  
blockSize: 文件的块的大小; 目前常用0x1000=4096, 与现代磁盘sector的大小匹配.  
chunk: chunk的id, 通常与版本相同，没有版本的时候是0  
created: 文件创建时间(从1970年到现在的毫秒数)  
format: 文件格式，当前是1.  
version: chunk的版本  
fletcher: header的[Fletcher-32形式](https://en.wikipedia.org/wiki/Fletcher%27s_checksum#Fletcher-32)的check sum值

  
打开文件时，读取文件头并校验其check sum值. 如果两个头都是合法的，那么新版本的将被使用. 最新版本的chunk被找到，而且从这里读取剩余的metadata 。如果chunk id, block and version没有存储在文件头中,那么从文件中最后一个chunk开始查找最近的chunk。

# Chunk 格式

这里针对单个版本的chunk. 每个chunk由 header, 这个版本中发生修改的pages , 和一个footer组成. page包含map中实际的数据. chunk里的page被存储在header的后面的右侧, next to each other (unaligned). chunk的大小是块大小的倍数. footer被存储在至少128字节的chunk中。

```
[ header ] [ page ] [ page ] ... [ page ] [ footer ]
```

  
footer允许用来验证这个chunk是否完全写完成了， (一个chunk对应一次写操作),同时允许用来找到文件中最后一个chunk的开始位置chunk的header和footer包含如下数据：

```
chunk:1,block:2,len:1,map:6,max:1c0,next:3,pages:2,root:4000004f8c,time:1fc,version:1
chunk:1,block:2,version:1,fletcher:aed9a4f6
```

这些字段解析如下：

chunk: chunk id.  
block: chunk的第一个block (multiply by the block size to get the position in the file).  
len: chunk的size，即block的个数？？.  
map: 最新map的id; 当新map创建时会增加.  
max: 所有的最大的page size的和 (see page format).  
next: 为下一个chunk预估的开始位置.  
pages: 一个chunk中page的个数  
root: metadata根page的位置 (see page format).  
time: 写chunk的时间, 从文件创建到写chunk之间的隔的毫秒数.  
version: chunk体现的版本  
fletcher: footer的check sum.

  
**Chunks 从不取代式更新. 每个chunk含有相应版本的page (如上所说，一个chunk对应一个版本),** plus all the parent nodes of those pages, recursively, up to the root page. **如果有一个entry在map中发生了增加、删除或者修改，然后相应的page将被拷贝、修改，并存储到下一个chunk中, 旧chunk中活(live)page的数量将减少. 这个机制叫作复制后写**, 与Btrfs文件系统工作原理相似. 没有活(live)page的chunk将被打上释放的标志,所以这个空间能被更多的最近的chunk使用. Because not all chunks are of the same size, there can be a number of free blocks in front of a chunk for some time (until a small chunk is written or the chunks are compacted). **There is a delay of 45 seconds (by default) before a free chunk is overwritten, to ensure new versions are persisted first.**

当打开一个store时最新的chunk是如何被定位到的: 文件头含有一个近期的(a recent chunk)chunk,但不总是最新的一个。这将减少文件header更新的次数。在打开一个文件之后， 文件头, 大量的chunk的脚 (处于文件的尾端) 被读取. From those candidates, 最近的chunk的header被读取。它含有下一个指针(参见上面)，这些chunk的头和脚同样会被读取。 those chunk's header and footer are read as well. If it turned out to be a newer valid chunk, this is repeated, until the newest chunk was found. Before writing a chunk, the position of the next chunk is predicted based on the assumption that the next chunk will be of the same size as the current one. When the next chunk is written, and the previous prediction turned out to be incorrect, the file header is updated as well. In any case, the file header is updated if the next chain gets longer than 20 hops.

# Page格式

每一个map是一个B-tree, map的数据被存存储在B-tree pages.：含有map的key-value pairs 的叶子节点，那些仅含有key和指向叶子的内部节点. 树的根节点既是一个叶子也是一个内部节点. 与文件头、chunk头脚不同的是， page的数据是人类不可读的，它是以字节数组形式存储的, 有 long (8 bytes), int (4 bytes), short (2 bytes), and variable size int and long (1 to 5 / 10 bytes)几种类型。

page 格式是:

length (int): page的长度(以bytes为单位)。  
checksum (short): Checksum 值(chunk id  xor  offset within the chunk  xor  page length)。  
mapId (variable size int): 这页所属map的id。  
len (variable size int): 这个页中key的数量。  
type (byte): 页的类型。0 表示左page, 1 表示内部节点; 加2代表键值对采用了LZF算法压缩, 加6代表键值对采用了Deflate 算法压缩。  
children (array of long; internal nodes only): 子节点位置。  
childCounts (array of variable size long; internal nodes only): 已知子页的实体总数。  
keys (byte array): 所有的键， stored depending on the data type.  
values (byte array; leaf pages only): 所有值, stored depending on the data type.

即使这不是文件格式所要求的，页仍以如下顺序存储：

针对每一个map，root page首先被存储，然后是内部节点(如果有的话)，然后是左叶子。这样应该能加速读取的速度，因为顺序读的速度高于随机读。元数据的map被存储在一个chunk的尾端。指向页的指针被当做一个long型存储，使用了一个特殊的格式：26位用于chunk id，32位用于在chunk内的位移，5位用于长度码，1位用于页类型(叶子还是内部节点)。页类型被编码以至于当清除或移除一个map时，叶子节点不必被读取（内部节点需要被读取以使得程序知道所有的页在哪里，而且在一个典型的B-tree结构中，绝大多数page是叶子页）。绝对文件位置没有被包含以至于在不必改变页指针的情况下chunk能在文件里被移除，仅有chunk的元数据需要被修改。长度码是一个从0到31的数字，0表示这个页的最大长度是32bytes,1代表48bytes 2: 64, 3: 96, 4: 128, 5: 192, 以此类推，直至31代表1MB 。如此一来，读取一个页仅仅需要一个读操作(除非是很大的页)。所有页的最大长度的和被存储在chunk元数据的max字段，并且当一个页被标记成“移除了”，活动页最大长度将被调整。这样不仅可以估算空闲页数的个数，还允许估算一个block内的剩余空间。

子页中总实体的数量总保持在有效的允许范围内计数，通过索引查找和跳过一些操作。？？

The total number of entries in child pages are kept to allow efficient range counting, lookup by index, and skip operations.

这个页的形式是一个技数B-tree。

数据压缩：page类型后的数据可以选择LZF压缩算法进行压缩。

# Metadata Map

除用户map之外，还有个元数据map，它含有用户map的名字、位置及其chunk元数据。 chunk的最后一页含有元数据map的root page。 root page的精确位置被存储在chunk的header里。这个page(直接地或间接地)指向所有其他map的root page。一个store的元数据map有一个名字叫data的map,还有一个chunk，包含如下实体：

chunk.1:  chunk 1的元数据. 这是和chunk header相同的数据，活动的page的数量, 和最大的活动长度。  
map.1: map 1的元数据。这个实体是：名字、创建版本和类型。  
name.data: 名字为data的map id。他的值是1.  
root.1: map1的root位置.  
setting.storeVersion: store的版本(一个用户定义的值).  

# 相似的项目以及和其他存储引擎的不同

  
与类似的存储引擎LevelDB和Kyoto Cabinet不同，MVStore使用java编写，能很容易嵌入java或者android程序中。

MVStore与Berkeley DB的Java版本有点相似，因为它也是用java编写的且是日志结构式的存储, 但是H2的许可证更自由.

类似SQLite3MVStore在一个文件上保存所有数据。与SQLite 3不同的是, MVStore 使用日志结构式存储。 该计划使得MVStore比SQLite3更易用更快。在最近一个很简单的测试中, 在android上MVStore速度是SQLite 3的两倍。

MVStore的api与Jan Kotek写的MapDB 相似 (以前称作JDBM) , 部分代码在 MVStore 和 MapDB中共享. 然而, 与MapDB不同的是, MVStore 使用日志结构式存储。 MVStore没有记录的大小限制。

# 目前状态

这个阶段的代码仍处于实验性阶段。API与其行为也可能被部分修改。 特性或将被添加或移除(即使主要特性将保留).

# Requirements需求

  
MVStore被包含在最新的H2 jar文件中.

对于使用它没有什么特别的需要。MVStore 也可以在android的JVM上运行。

若需要仅仅构建MVStore (不含有数据库引擎), 运行:

./build.sh jarMVStore  
这将创建h2mvstore-1.4.191.jar (大约200 KB).

[