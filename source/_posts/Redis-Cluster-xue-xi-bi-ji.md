---
title: Redis Cluster 学习笔记
id: 1542
date: 2024-10-31 22:02:00
author: daichangya
permalink: /archives/Redis-Cluster-xue-xi-bi-ji/
categories:
- redis
---



*   redis cluster 是 redis 提供的分布式数据库方案，通过在多个 redis 节点之间分片(sharding)来进行数据共享。并能在部分节点故障的情况下继续运行。
    
*   redis 集群的基本存储单位是槽（slot），一个集群有2^14=16384个槽。每一个槽的key存放在集群中的唯一一个master节点中，每一个槽还有0~N个slave节点。
    

## [](#集群简介 "集群简介")集群简介

[![集群简介](http://ralphbupt.github.io/img/redis-cluster-1.png)](http://ralphbupt.github.io/img/redis-cluster-1.png)

*   redis集群每个节点都和其他节点保持连接，需要两个端口。其中一个数据端口（例如7000用来为客户端提供服务以及同其他服务端交换数据。另外一个总线端口（数据端口号+10000，其中偏移量10000是固定的）用来在节点之间传送控制信息。要让redis集群系统正常运行，需要：
    *   每个节点的数据端口对 Client **以及**其他集群节点可见
    *   每个节点的总线端口对其他节点可见

## [](#redis-cluster-数据分片（sharding） "redis cluster 数据分片（sharding）")redis cluster 数据分片（sharding）

*   redis 集群有16384个哈希槽（hash slot），其中散列算法是简单的取 key 的 CRC16 模 16384
*   集群中的每一个节点负责哈希槽的一个子集
*   slot 可以动态的迁移、删除和分配
*   slot 的设计使得集群中能动态的添加和删除节点，例如：
    *   当添加新的节点 nodeD 时，只需要从节点 nodeA,nodeB,nodeC 中移动一些 slot 到 nodeD去，这样就实现了集群的扩容。
    *   当需要删除节点 nodeA 时，将 nodeA 中的 slot 移动到 nodeB，和nodeC中。当nodeA为空之后，可以从集群中删除nodeA

*   redis cluster 支持多键（MGET MSET 等）操作，但前提是–单次命令执行（command execution）或者整个 transection 中的 key 属于同一个哈希槽。我们可以使用 hash tag 来强制多个key使用同一个哈希槽。
    *   hash tag 的 简单语法是 只有key 中 ***{ }***中的部分才被用来做hash，例如 key ***{user1000}.following*** 和 ***{user1000}.followers*** 会被 hash 到同一个哈希槽中去，因为{}中的内容相同。

## [](#redis-cluster-主从模式 "redis cluster 主从模式")redis cluster 主从模式

*   redis cluster 采用主从模式，其中每一个槽有 1（主节点本身） ~ N(N-1个从节点)
*   当主节点故障之后，系统会从该主节点的从节点中选举出一个从节点作为新的主节点。接管故障主节点负责处理的槽。当故障的节点恢复后，自动变为从节点
*   当一个哈希槽的所有节点，主节点和从节点都故障之后，系统不能正常运行

## [](#redis-cluster-配置参数 "redis cluster 配置参数")redis cluster 配置参数

*   redis集群配置文件中，需要修改的最小配置有
    *   port: 端口
    *   cluster-enabled： 开启 cluster
    *   cluster-config-file: 集群配置文件
    *   cluster-node-timeout： 节点超时时间(ms)

## [](#redis-cluster-搭建 "redis cluster 搭建")redis cluster 搭建

*   redis 的 src 目录下提供了 create-cluster 脚本来创建简单的的 demo
    1.  create-cluster start
        1.  create-cluster create // 命令1和2开启集群
        2.  create-cluster stop // 停止集群
*   redis cluster 手动创建
    
    ```
    mkdir    cluster-test
    cd         cluster-test
    mkdir 7000 7001 7002 7003 7004 7005
    
    ```
    
    在每一个文件夹中创建一个 redis.conf ，替换其中的端口号为7000~7005 ，修改 cluster 相关配置
    
    创建启动脚本
    
    ```
    vim start_cluster.sh
    cd 7000/
    nohup ./redis-server redis.conf &
    cd ../7001
    nohup ./redis-server redis.conf &
    cd ../7002
    nohup ./redis-server redis.conf &
    cd ../7003
    nohup ./redis-server redis.conf &
    cd ../7004
    nohup ./redis-server redis.conf &
    cd ../7005
    nohup ./redis-server redis.conf &
    cd ../
    ps -aux|grep redis
    
    ```
    
    关闭集群，现在重启集群需要kill掉所有进程
    
    ```
    ps -aux| grep redis-server | grep -v grep | cut -c 9-15 | xargs kill -9
    
    ```
    
    创建集群
    
    ```
    ./redis-trib.rb create --replicas 1 127.0.0.1:7000 127.0.0.1:7001 \
    127.0.0.1:7002 127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005
    
    ```
    

## [](#redis-集群管理 "redis 集群管理")redis 集群管理

*   redis-trib.rb 是 redis 作者用 ruby 实现的 redis cluster 管理工具。  
    用此工具，我们能轻松的完成节点的添加、删除、slot的管理等。常用命令如下：
    
    ```
    create          host1:port1 ... hostN:portN        // 创建集群    
    check           host:port                        // 检查集群
    info            host:port                        // 查看集群
    fix             host:port                        // 修复集群
    reshard         host:port                        // 迁移slot
    rebalance       host:port                        // 平衡节点slot数量
    add-node        new_host:new_port existing_host:existing_port    // 添加节点
    del-node        host:port node_id                // 删除节点
    set-timeout     host:port milliseconds            // 设置节点心跳超时使劲按
    
    ```
    
*   此外也能通过 [CLUSTER](https://redis.io/commands#cluster) 相关命令来管理集群，使用这些命令需要登录
    
    ```
    //集群(cluster)  
    CLUSTER INFO 打印集群的信息  
    CLUSTER NODES 列出集群当前已知的所有节点（node），以及这些节点的相关信息。   
    
    //节点(node)  
    CLUSTER MEET <ip> <port> 将 ip 和 port 所指定的节点添加到集群当中，让它成为集群的一份子。  
    CLUSTER FORGET <node_id> 从集群中移除 node_id 指定的节点。  
    CLUSTER REPLICATE <node_id> 将当前节点设置为 node_id 指定的节点的从节点。  
    CLUSTER SAVECONFIG 将节点的配置文件保存到硬盘里面。   
    
    //槽(slot)  
    CLUSTER ADDSLOTS <slot> [slot ...] 将一个或多个槽（slot）指派（assign）给当前节点。  
    CLUSTER DELSLOTS <slot> [slot ...] 移除一个或多个槽对当前节点的指派。  
    CLUSTER FLUSHSLOTS 移除指派给当前节点的所有槽，让当前节点变成一个没有指派任何槽的节点。  
    CLUSTER SETSLOT <slot> NODE <node_id> 将槽 slot 指派给 node_id 指定的节点，如果槽已经指
                                          槽派给另一个节点，那么先让另一个节点删除该槽>，然后再进行指派。  
    CLUSTER SETSLOT <slot> MIGRATING <node_id> 将本节点的槽 slot 迁移到 node_id 指定的节点中。  
    CLUSTER SETSLOT <slot> IMPORTING <node_id> 从 node_id 指定的节点中导入槽 slot 到本节点。  
    CLUSTER SETSLOT <slot> STABLE 取消对槽 slot 的导入（import）或者迁移（migrate）。   
    
    //键 (key)  
    CLUSTER KEYSLOT <key> 计算键 key 应该被放置在哪个槽上。  
    CLUSTER COUNTKEYSINSLOT <slot> 返回槽 slot 目前包含的键值对数量。  
    CLUSTER GETKEYSINSLOT <slot> <count> 返回 count 个 slot 槽中的键。  
    
    ```
    

## [](#redis-cluster-客户端使用原理 "redis cluster 客户端使用原理")redis cluster 客户端使用原理

*   redis cluster 需要客户端能够解析 cluster 协议，主要包括：
    
    1.  MOVE 和 ASK 命令的重定向， 连接超时的处理
    2.  槽、节点缓存的维护。连接的管理等。

[![客户端处理流程](http://ralphbupt.github.io/img/image_2.png)](http://ralphbupt.github.io/img/image_2.png)

*   向 Redis 集群发送的任何含 key 命令 (如 get, set, llen, mget, mset, rename, rpoplpush 等) 时, 先对计算 key 的槽位编号, 将指令发送给对应槽位的master节点. 如果key存在，返回如果指令发送到了错误的节点, 该节点并不会处理请求, 而是会返回重定向(MOVED, ASK)错误信息.

```
const kClusterSlots    = 16384
type Cluster struct {
    slots        [kClusterSlots]*redisNode        // 槽对应的节点信息
    nodes        map[string]*redisNode
    ...
    ...
}

```

*   例如
    
    ```
    MOVED 16384 127.0.0.1：7001
    ASK 16384 127.0.0.1：7001
    
    ```
    
*   MOVED 代表槽 i 的负责权**已经**从节点 A 转移到节点 B。当客户端收到了槽的 MOVED 错误之后，应该将本地缓存的节点和槽的对应信息也更新。即下次遇到槽 i 的命令请求，直接向 SLOT-B 发送命令。
    
*   ACK 代表槽 i **正在**从节点 A转移到节点 B。所以当客户端收到了 ASK 之后，只是这次命令向节点 B 请求，而且必须先发送 ASKING 命令。 接下来槽 i 的命令仍然向节点 A 请求。
*   超时： 超时后随机向新的节点更新槽的信息。

## [](#redis-cluster-的使用 "redis cluster 的使用")redis cluster 的使用

*   当搭建好 redis cluste 后，使用redis cluster 就变得很简单，作者提到了当前 client libraries 实现。以 redis-go-cluster 为例：
*   安装 redis-go-cluster
    
    ```
    go get github.com/chasex/redis-go-cluster
    
    ```
    
*   使用
    
    ```
    import "github.com/chasex/redis-go-cluster"
    
    cluster, err := redis.NewCluster(
    &redis.Options{
    StartNodes: []string{"127.0.0.1:7000", "127.0.0.1:7001", "127.0.0.1:7002"},
    ConnTimeout: 50 * time.Millisecond,
    ReadTimeout: 50 * time.Millisecond,
    WriteTimeout: 50 * time.Millisecond,
    KeepAlive: 16,
    AliveTime: 60 * time.Second,
    })
    
    _, err := cluster.Do("set", key, value)
    value, err := redis.Int(cluster.Do("GET", key))
    ...
    
    ```
    

## [](#参考文档 "参考文档")参考文档

*   [https://redis.io/topics/cluster-tutorial](https://redis.io/topics/cluster-tutorial) 最好的文档永远是官方的文档
*   [http://blog.csdn.net/dc_726/article/details/48552531](http://blog.csdn.net/dc_726/article/details/48552531) 全面剖析Redis Cluster原理和应用
*   [https://github.com/chasex/redis-go-cluster](https://github.com/chasex/redis-go-cluster) redis-go-cluster ,使用redigo
*   [http://weizijun.cn/2016/01/08/redis%20cluster%E7%AE%A1%E7%90%86%E5%B7%A5%E5%85%B7redis-trib-rb%E8%AF%A6%E8%A7%A3/](http://weizijun.cn/2016/01/08/redis%20cluster%E7%AE%A1%E7%90%86%E5%B7%A5%E5%85%B7redis-trib-rb%E8%AF%A6%E8%A7%A3/) redis-trib.rb 的介绍
*   [http://blog.51yip.com/nosql/1726.html](http://blog.51yip.com/nosql/1726.html) redis cluster 节点管理
