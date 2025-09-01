---
title: ehcache之offheap
id: 1523
date: 2024-10-31 22:02:00
author: daichangya
permalink: /archives/ehcache%E4%B9%8Boffheap/
---

### 一、背景

offheap作为摆脱gc的本地缓存来使用，对于缓存大量数据和提升应用的性能大有裨益。

EHCache的offheap层直接使用了Terracotta-OSS开源的[offheap-store](https://github.com/Terracotta-OSS/offheap-store)作为底层实现。

但是offheap-store包含了一系列的算法和数据结构的设计和使用，很多地方借鉴了操作系统的知识，比如内存分页设计，时钟置换算法，内存分配等等，由此可见涉及到内存管理的都是比较复杂的领域，这里仅仅是简单介绍，为后续深入使用铺垫基础。

想了解offheap-store的原因来自于以下几个问题：

由于堆外内存不能存储对象，只能存储序列化后的二进制数据，那么本质就转换为了数据对于内存的需求：

堆外内存如何分配和管理？  
数据移除后内存如何释放？  
过期和剔除机制是怎样的？  
下面针对上面的问题进行一一说明。

### 二、ehcache offheap put

**put时序图**，由于调用链太长，故分成两部分，第一部分到OffHeapHashMap截止，如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200407141652436.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2E0MTc5MzA0MjI=,size_16,color_FFFFFF,t_70)

此部分调用都是顺序的，调用过程比较简单，这里只介绍一下EhcacheConcurrentOffHeapClockCache类：

*   EhcacheConcurrentOffHeapClockCache
    
    它继承了AbstractConcurrentOffHeapMap，因此有map的特性。其内部持有多个EhcacheSegment(每个Segment是一个OffHeapHashMap)，每个Segment通过锁来实现并发控制。如下图所示：
    

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200407141719443.png)

第二部分时序图如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200407141737464.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2E0MTc5MzA0MjI=,size_16,color_FFFFFF,t_70)

这里来详细介绍一下每一步的调用：

*   第5步，OffHeapHashMap调用PortabilityBasedStorageEngine.writeMapping(k,v)写入key和value。
    
*   第6步，PortabilityBasedStorageEngine调用OffHeapBufferStorageEngine.writeMappingBuffers(kb,vb)写入key和value序列化后转换为ByteBuffer对应的值。
    
*   第7步，存储数据到offheap之前需要先分配内存，这里负责OffHeap内存分配的是OffHeapStorageArea。
    
*   第8步，OffHeapStorageArea调用UpfrontAllocatingPageSource.expand进行内存页的分配，而UpfrontAllocatingPageSource初始化时会先将整体内存进行划分为块（以大小为10G的offheap为例）：
    
    UpfrontAllocatingPageSource初始化时会按照最大为1G大小拆分为块，这里10G/1G=10，即会分为10个大小为1G的内存块，如下图所示：
    

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200407141756996.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2E0MTc5MzA0MjI=,size_16,color_FFFFFF,t_70)

*   第9步，内存页分配借助PowerOfTwoAllocator进行分配，其实现借助于AA树（红黑树的变种）。
    
*   第9步返回分配好的内存页的起始地址。
    
    到这里说一下，内存页分配示例图：
    

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200407141810321.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2E0MTc5MzA0MjI=,size_16,color_FFFFFF,t_70)

上面图示中1G大小的是已经预划分好的内存块，分配内存页时会顺序的在内存块上分配出内存页来，其分配释放由PowerOfTwoAllocator来管理。

*   第8步返回分配好的内存页对象，OffHeapStorageArea会将内存页对象存储在其内部hash表中。
    
*   第8.2步，OffHeapStorageArea会调用IntegerBestFitAllocator扩展内存，IntegerBestFitAllocator是内存管理器，其实现采用Doug Lea大神的内存分配器：[dlmalloc](http://gee.cs.oswego.edu/dl/html/malloc.html)。
    
*   第10步，经过第8,9步扩展好内存后，可以正式分配内存了，此时分配的内存大小就是实际需要的大小。
    
*   第10步返回实际需要的内存的起始地址。
    
*   第11步，返回正式的地址后，写入数据，这里需要说明一下，写入的value将会包装额外的元信息，包括：
    
    ```
    long creationTime;
    long lastAccessTime;
    long expirationTime;
    
    ```
    
*   第12步，**上面介绍的步骤都是为了写入key和value的数据**，key的hash值也会写入到offheap中，其实现主要在OffHeapHashMap中，它采用[线性探测](https://www.cnblogs.com/hongshijie/p/9419387.html)解决hash冲突。为了避免大量key导致数据聚集，它在初始化时利用`UpfrontAllocatingPageSource`分配了hash表(堆外内存)来存储key的hash值。
    
    一个key的hash值对应的空间称作slot，共占用16(int+int+long)个字节，并且当使用量大于50%时将进行自动扩容，如下：
    

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200407141856864.png)

每个slot存储的数据结构如下：

```
int status marker;// 状态值：0代表可用，1代表已使用，2代表已移除。
int cached key hashcode;//key的hash值。
long value address;//key对应的value存在offheap的地址。

```

**下面从内存结构层面来描述一下整个映射过程**：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200407141913912.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2E0MTc5MzA0MjI=,size_16,color_FFFFFF,t_70)

*   假设offheap为10个G，会首先划分为10个1个G的内存块，之后所有内存管理都会以内存块为最大单位。
    
*   假设存储的key为字符串a，value为一个对象video。首先介绍**②key和value的内存空间**，因为key的hash值存储中会存储key和value实际存储内存的地址。
    
*   **②key和value的内存空间**:
    
    *   首先需要根据key和value的大小，从内存块上扩展出能存储下此大小的内存页。
        
    *   之后采用dlmalloc进行内存分配
        
    *   分配完毕后，根据分配的内存起始地址写入实际数据，数据结构如下：
        
        ```
        writeInt(address, hash);
        writeInt(address + 4, keyLength);
        writeInt(address + 8, valueLength);
        writeBuffer(address + 12, keyBuffer);
        writeBuffer(address + 12 + keyLength, valueBuffer);
        
        ```
        
*   **①key的hash值空间**：
    
    *   根据key的hash值97进行定位。
    *   获得*key和value实际写入的内存地址*后，结合hash值，写入hash表中。

**根据put流程中的内存结构，很容易能够知道get的流程，故get过程不再赘述**。

### 三、ehcache offheap remove

remove主要涉及到内存的释放，故流程图只从OffHeapHashMap开始，前边的EHCache相关的调用省略，如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200407141935193.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2E0MTc5MzA0MjI=,size_16,color_FFFFFF,t_70)

*   第1步，EhcacheSegment调用OffHeapHashMap.computeIfPresentWithMetadata(k,fun)进行remove操作。
*   第2步，根据key定位hash表，获得到value的内存地址。
*   第3,4,5,6都是顺序调用，不再介绍。
*   第6步返回，IntegerBestFitAllocator之前说过，是采用dlmalloc算法实现的，它能判断出是否需要释放某页。
*   第7步，如果需要释放页，会回调OffHeapStorageArea.free(page)进行内存页的释放。
*   第8步，内存页由PowerOfTwoAllocator管理，调用free释放内存页。

当然，OffHeapHashMap还涉及到将slot(key的存储内存)标记为删除，便于下次利用。

### 四、ehcache offheap evict

剔除发生在内存满了但是还有数据写入的时候，主要发生在如下两种情况：

1.  hash表(存储key的hashcode和value地址)满了，对hash表扩容，但是扩容失败。
2.  存储key和value的空间满了，导致存储失败。

两种剔除方式类似，都使用了[clock eviction algorithm](https://github.com/Terracotta-OSS/offheap-store/blob/81037c9d2a0f14763e6241af29bf454ddac01cad/src/main/java/org/terracotta/offheapstore/AbstractOffHeapClockCache.java#L128)来通过hash表找到能够剔除的slot，之后类似于remove操作，释放映射的内存，并将hash表的slot标记为删除。

**目前对于offheap层，不能选择其他剔除方法，但可以提供[建议](https://www.ehcache.org/documentation/3.8/eviction-advisor.html)供ehcache剔除时使用。**

### 五、ehcache offheap expire

put和get时，均会检测value中的元信息，如果过期，则执行类似remove的操作，释放映射的内存。

### 六、总结

offheap层包含了一系列的算法和数据结构的设计和使用，很多地方借鉴了操作系统的知识，比如内存分页设计，时钟置换算法，内存分配等等，由此可见涉及到内存管理的都是比较复杂的领域，这里仅仅是简单介绍，为后续深入使用铺垫基础。