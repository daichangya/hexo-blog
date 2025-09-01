---
title: 漫谈Gossip协议与其在Redis Cluster中的实现
id: 1528
date: 2024-10-31 22:02:00
author: daichangya
permalink: /archives/%E6%BC%AB%E8%B0%88gossip%E5%8D%8F%E8%AE%AE%E4%B8%8E%E5%85%B6%E5%9C%A8rediscluster%E4%B8%AD%E7%9A%84%E5%AE%9E%E7%8E%B0/
tags: 
 - 算法
---

### 前言

之前给小伙伴们科普ClickHouse集群的时候，我曾经提到ClickHouse集群几乎是去中心化的（decentralized），亦即集群中各个CK实例是对等的，没有主从之分。集群上的复制表、分布式表机制只是靠外部ZooKeeper做分布式协调工作。想了想，又补了一句：

> “其实单纯靠P2P互相通信就能维护完整的集群状态，实现集群自治，比如Redis Cluster。”

当然限于时间没有展开说。这个周末休息够了，难得有空，来随便讲两句吧。

在官方Redis Cluster出现之前，要实现集群化Redis都是依靠Sharding+Proxy技术，如Twemproxy和Codis（笔者之前也写过[Codis集群](https://www.jianshu.com/p/5ccfffa37d45)的事儿）。而官方Redis Cluster走了去中心化的路，其通信基础就是Gossip协议，同时该协议还能保证一致性和可用性。本文先来介绍一下它。

### Gossip协议

简介

最近几个月一直在看《Friends》下饭。认为自己从不gossip的Rachel一语道破了gossip的本质。

![](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91cGxvYWQtaW1hZ2VzLmppYW5zaHUuaW8vdXBsb2FkX2ltYWdlcy8xOTUyMzAtMzg3MGJhOGU1MjdkOGZkMy5wbmc?x-oss-process=image/format,png)

现实生活中的流言八卦传播的机制就是“I hear something and I pass that information on”，并且其传播速度非常快。而Gossip协议就是借鉴了这个特点产生的，在P2P网络和分布式系统中应用广泛，它的方法论也特别简单：

> 在一个处于有界网络的集群里，如果每个节点都随机与其他节点交换特定信息，经过足够长的时间后，集群各个节点对该份信息的认知终将收敛到一致。

这里的“特定信息”一般就是指集群状态、各节点的状态以及其他元数据等。可见，Gossip协议是完全符合BASE理论精神的，所以它基本可以用于任何只要求最终一致性的领域，典型的例子就是区块链，以及部分分布式存储。另外，它可以很方便地实现弹性集群（即节点可以随时上下线），如失败检测与动态负载均衡等。

以下GIF图示出Gossip协议下一种可能的消息传播过程。蓝色节点表示对消息无感知，红色节点表示有感知。

![](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91cGxvYWQtaW1hZ2VzLmppYW5zaHUuaW8vdXBsb2FkX2ltYWdlcy8xOTUyMzAtNTliYzY0MDg4MDA1NDkwYS5naWY)

Source: https://managementfromscratch.wordpress.com/2016/04/01/introduction-to-gossip/

为了使Gossip协议更易于表达和分析，一般都会借用流行病学（epidemiology）中的SIR模型进行描述，因为大流行病（pandemic，比如这次新冠肺炎）的传播与流言八卦的传播具有相似性，并且已经由前人总结出一套成熟的数学模型了。

流行病学SIR模型

SIR模型早在1927年就由Kermack与McKendrick提出。该模型将传染病流行范围内的人群分为3类：

*   **S（易感者/susceptible）**，指未患病的人，但缺乏免疫能力，与感染者接触之后容易受到感染。
*   **I（感染者/infective）**，指已患病的人，并且可以将病原体传播给易感者人群；
*   **R（隔离者/removed）**，指被隔离在无传染环境，或者因病愈获得免疫力而不再易感的人。

如果不考虑人口的增长和减少，即s(t)+i(t)+r(t)始终为一常量的话，那么SIR模型就可以用如下的微分方程组来表示。

![](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91cGxvYWQtaW1hZ2VzLmppYW5zaHUuaW8vdXBsb2FkX2ltYWdlcy8xOTUyMzAtNjVkMjZlZWJiZDhkM2E4My5wbmc?x-oss-process=image/format,png)

其中，系数β是感染率，γ则是治愈率。为了阻止以至消灭传染病的流行，医学界会努力降低感染率，提高治愈率。但是在Gossip协议的语境下，计算机科学家要做的恰恰相反，即尽量高效地让集群内所有节点都“感染”（对信息有感知）。由SIR模型推演出的Gossip协议传播模型主要有两种，即反熵（Anti-entropy）和谣言传播（Rumor-mongering），下面分别介绍之。

反熵（Anti-entropy）

熵是物理学中体系混乱程度的度量，而反熵就是通过看似杂乱无章的通信达到最终一致。反熵只用到SIR模型中的S和I状态，S状态表示节点尚未感知到数据，I状态表示节点已感知到数据，并且正在传播给其他节点。具体来讲，反熵Gossip协议有3种实现方式：

*   推模式（push）：处于I状态的节点周期性地随机选择其他节点，并将自己持有的数据发送出去；
*   拉模式（pull）：处于S状态的节点周期性地随机选择其他节点，并请求接收其他节点持有的数据；
*   推-拉模式（push-pull）：即以上两者的综合。

下图示出在有界集群P中，以周期Δ执行反熵Gossip协议的伪代码描述。

![](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91cGxvYWQtaW1hZ2VzLmppYW5zaHUuaW8vdXBsb2FkX2ltYWdlcy8xOTUyMzAtN2I3MGE4ZjlkMDRmODMzYy5wbmc?x-oss-process=image/format,png)

如何分析其效率呢？为了简化问题，提出以下约束：

*   每一轮周期每个节点都只随机选择一个其他节点进行通信；
*   起始时，只有一个节点处于I状态，其他节点都处于S状态。

令s(t)表示在时刻t时，S状态的节点占总节点数n的比例（注意是比例），那么显然有s(0) = 1 - 1/n，可以计算出s(t)的期望为：

*   推模式

![](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91cGxvYWQtaW1hZ2VzLmppYW5zaHUuaW8vdXBsb2FkX2ltYWdlcy8xOTUyMzAtMGFmZGU5NjRiZTc1ZTc5MC5wbmc?x-oss-process=image/format,png)

*   拉模式

![](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91cGxvYWQtaW1hZ2VzLmppYW5zaHUuaW8vdXBsb2FkX2ltYWdlcy8xOTUyMzAtNmVmZTBmNWRkMGY1MGYyZC5wbmc?x-oss-process=image/format,png)

由下图可见，拉模式的信息传播效率比推模式高，达到了真正的指数级收敛速度。综合了两者的推-拉模式效率则比拉模式更高。

![](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91cGxvYWQtaW1hZ2VzLmppYW5zaHUuaW8vdXBsb2FkX2ltYWdlcy8xOTUyMzAtNzVkZGJlMmY1ZTAzY2M4YS5wbmc?x-oss-process=image/format,png)

但是，推模式每轮只需要1次信息交换，拉模式需要2次，推-拉模式需要3次。由于反熵Gossip协议每次都交换全量消息，数据量可能会比较大，因此具体选择哪种模式，还是需要考虑网络资源的开销再决定。

谣言传播（Rumor-mongering）

谣言传播与反熵不同的一点是，它采用完整的SIR模型。处于R状态的结点表示已经获取到了信息，但是不会将这个信息分享给其他节点，就像“谣言止于智者”一样。另一个不同点是，谣言传播机制每次只会交换发生变化的信息，而不是全量信息，所以它对网络资源的开销会比反熵机制要小很多。

下图示出在有界集群P中，以周期Δ执行谣言传播Gossip协议的伪代码描述。

![](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91cGxvYWQtaW1hZ2VzLmppYW5zaHUuaW8vdXBsb2FkX2ltYWdlcy8xOTUyMzAtZDIyNTExMTExYTc5OWY1Ni5wbmc?x-oss-process=image/format,png)

图中的blind/feedback和coin/counter是怎么一回事呢？它们表示节点从I状态转移到R状态的条件。

*   coin：在每轮传播中，节点以1/k的概率从I转移到R状态。
*   counter：在参与k轮传播之后（即发送k次信息）之后，节点从I状态转移到R状态。
*   feedback：在发出信息后，对位节点有反馈才可以进入R状态。
*   blind：在发出信息后，不必等待对位节点有反馈，随时都可以进入R状态。

由上可见，谣言传播模式的结束条件是所有节点都对谣言“免疫”，但是又有可能造成部分节点始终无法对消息有感知（即保持S状态）。以coin条件为例，可以写出如下的微分方程组。其中s和i仍然表示S状态和I状态的节点占总节点数的比例。

![](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91cGxvYWQtaW1hZ2VzLmppYW5zaHUuaW8vdXBsb2FkX2ltYWdlcy8xOTUyMzAtMjlhNWIwOTBkZTU1NmViYi5wbmc?x-oss-process=image/format,png)

消去t，可得：

![](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91cGxvYWQtaW1hZ2VzLmppYW5zaHUuaW8vdXBsb2FkX2ltYWdlcy8xOTUyMzAtMDhlYTU4NmEwZTdkMWI1YS5wbmc?x-oss-process=image/format,png)

根据初始条件：i(1 - 1/n) = 1，可以推导出：

![](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91cGxvYWQtaW1hZ2VzLmppYW5zaHUuaW8vdXBsb2FkX2ltYWdlcy8xOTUyMzAtZTEyZjE1MDJlMzM1ZTZlMy5wbmc?x-oss-process=image/format,png)

如果我们要让i(s*) = 0的话：

![](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91cGxvYWQtaW1hZ2VzLmppYW5zaHUuaW8vdXBsb2FkX2ltYWdlcy8xOTUyMzAtYmQxM2ZiMzlkYTRiNTQ3Yy5wbmc?x-oss-process=image/format,png)

可见，s*会随着k值的增高而指数级下降。当k = 1时，s*约为20%，而当k = 5时，s*就只有约0.24%了。也就是说，如果节点每轮以1/5的概率从I转换为R状态，就已经比较安全了。

在实际应用中，反熵和谣言传播的各种方式往往结合在一起使用，因此Gossip协议非常灵活，没有完全统一的标准。以下就看一看Redis Cluster的实现。

### Redis Cluster的Gossip方案

Redis Cluster是在3.0版本加入的feature，故我们就选择3.0版本的源码来简单解说。下图是主从架构的Redis Cluster示意图，其中虚线表示各个节点之间的Gossip通信。

![](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91cGxvYWQtaW1hZ2VzLmppYW5zaHUuaW8vdXBsb2FkX2ltYWdlcy8xOTUyMzAtYWY5MDgxZjEwOTMwNjhhMC5wbmc?x-oss-process=image/format,png)

消息类型

Gossip协议是个松散的协议，没有对数据交换的格式做特别的约束，各框架可以自由设定自己的implementation。Redis Cluster有以下9种消息类型的定义，详情可见注释（注释非我所写，而是来自[redis-3.0-annotated](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fhuangz1990%2Fredis-3.0-annotated)项目，致敬）。

```
/* Note that the PING, PONG and MEET messages are actually the same exact
 * kind of packet. PONG is the reply to ping, in the exact format as a PING,
 * while MEET is a special PING that forces the receiver to add the sender
 * as a node (if it is not already in the list). */
// 注意，PING 、 PONG 和 MEET 实际上是同一种消息。
// PONG 是对 PING 的回复，它的实际格式也为 PING 消息，
// 而 MEET 则是一种特殊的 PING 消息，用于强制消息的接收者将消息的发送者添加到集群中
// （如果节点尚未在节点列表中的话）
// PING
#define CLUSTERMSG_TYPE_PING 0          /* Ping */
// PONG （回复 PING）
#define CLUSTERMSG_TYPE_PONG 1          /* Pong (reply to Ping) */
// 请求将某个节点添加到集群中
#define CLUSTERMSG_TYPE_MEET 2          /* Meet "let's join" message */
// 将某个节点标记为 FAIL
#define CLUSTERMSG_TYPE_FAIL 3          /* Mark node xxx as failing */
// 通过发布与订阅功能广播消息
#define CLUSTERMSG_TYPE_PUBLISH 4       /* Pub/Sub Publish propagation */
// 请求进行故障转移操作，要求消息的接收者通过投票来支持消息的发送者
#define CLUSTERMSG_TYPE_FAILOVER_AUTH_REQUEST 5 /* May I failover? */
// 消息的接收者同意向消息的发送者投票
#define CLUSTERMSG_TYPE_FAILOVER_AUTH_ACK 6     /* Yes, you have my vote */
// 槽布局已经发生变化，消息发送者要求消息接收者进行相应的更新
#define CLUSTERMSG_TYPE_UPDATE 7        /* Another node slots configuration */
// 为了进行手动故障转移，暂停各个客户端
#define CLUSTERMSG_TYPE_MFSTART 8       /* Pause clients for manual failover */
```

可见，Redis Gossip除了负责信息交换之外，还会负责节点的上下线及failover。

消息格式

Redis Gossip消息分为消息头和消息体，消息体一共有4类，其中MEET、PING和PONG消息都用clusterMsgDataGossip结构来表示。

```
typedef struct {
    // 节点的名字
    // 在刚开始的时候，节点的名字会是随机的
    // 当 MEET 信息发送并得到回复之后，集群就会为节点设置正式的名字
    char nodename[REDIS_CLUSTER_NAMELEN];
    // 最后一次向该节点发送 PING 消息的时间戳
    uint32_t ping_sent;
    // 最后一次从该节点接收到 PONG 消息的时间戳
    uint32_t pong_received;
    // 节点的 IP 地址
    char ip[REDIS_IP_STR_LEN];    /* IP address last time it was seen */
    // 节点的端口号
    uint16_t port;  /* port last time it was seen */
    // 节点的标识值
    uint16_t flags;
    // 对齐字节，不使用
    uint32_t notused; /* for 64 bit alignment */
} clusterMsgDataGossip;
 
typedef struct {
    // 下线节点的名字
    char nodename[REDIS_CLUSTER_NAMELEN];
} clusterMsgDataFail;
 
typedef struct {
    // 频道名长度
    uint32_t channel_len;
    // 消息长度
    uint32_t message_len;
    // 消息内容，格式为 频道名+消息
    // bulk_data[0:channel_len-1] 为频道名
    // bulk_data[channel_len:channel_len+message_len-1] 为消息
    unsigned char bulk_data[8]; /* defined as 8 just for alignment concerns. */
} clusterMsgDataPublish;
 
typedef struct {
    // 节点的配置纪元
    uint64_t configEpoch; /* Config epoch of the specified instance. */
    // 节点的名字
    char nodename[REDIS_CLUSTER_NAMELEN]; /* Name of the slots owner. */
    // 节点的槽布局
    unsigned char slots[REDIS_CLUSTER_SLOTS/8]; /* Slots bitmap. */
} clusterMsgDataUpdate;
 
union clusterMsgData {
    /* PING, MEET and PONG */
    struct {
        /* Array of N clusterMsgDataGossip structures */
        clusterMsgDataGossip gossip[1];
    } ping;
    /* FAIL */
    struct {
        clusterMsgDataFail about;
    } fail;
    /* PUBLISH */
    struct {
        clusterMsgDataPublish msg;
    } publish;
    /* UPDATE */
    struct {
        clusterMsgDataUpdate nodecfg;
    } update;
};
```

调度Gossip通信

在redis.c中，有一个负责调度执行Redis server内周期性任务的函数，名为serverCron()。其中，与集群相关的代码段如下。

```
/* Run the Redis Cluster cron. */
// 如果服务器运行在集群模式下，那么执行集群操作
run_with_period(100) {
    if (server.cluster_enabled)     clusterCron();
}
```

可见，在启用集群时，每个节点都会每隔100毫秒执行关于集群的周期性任务clusterCron()，该函数中与Gossip有关的代码有多处，以下是部分节选。注释写得非常清楚，笔者就不再献丑了。

节点加入集群

```
// 为未创建连接的节点创建连接
if (node->link == NULL) {
    // .....
    /* Queue a PING in the new connection ASAP: this is crucial
     * to avoid false positives in failure detection.
     *
     * If the node is flagged as MEET, we send a MEET message instead
     * of a PING one, to force the receiver to add us in its node
     * table. */
    // 向新连接的节点发送 PING 命令，防止节点被识进入下线
    // 如果节点被标记为 MEET ，那么发送 MEET 命令，否则发送 PING 命令
    old_ping_sent = node->ping_sent;
    clusterSendPing(link, node->flags & REDIS_NODE_MEET ?
            CLUSTERMSG_TYPE_MEET : CLUSTERMSG_TYPE_PING);
    // 这不是第一次发送 PING 信息，所以可以还原这个时间
    // 等 clusterSendPing() 函数来更新它
    if (old_ping_sent) {
        /* If there was an active ping before the link was
         * disconnected, we want to restore the ping time, otherwise
         * replaced by the clusterSendPing() call. */
        node->ping_sent = old_ping_sent;
    }
    /* We can clear the flag after the first packet is sent.
     *
     * 在发送 MEET 信息之后，清除节点的 MEET 标识。
     *
     * If we'll never receive a PONG, we'll never send new packets
     * to this node. Instead after the PONG is received and we
     * are no longer in meet/handshake status, we want to send
     * normal PING packets. 
     *
     * 如果当前节点（发送者）没能收到 MEET 信息的回复，
     * 那么它将不再向目标节点发送命令。
     *
     * 如果接收到回复的话，那么节点将不再处于 HANDSHAKE 状态，
     * 并继续向目标节点发送普通 PING 命令。
     */
    node->flags &= ~REDIS_NODE_MEET;
    redisLog(REDIS_DEBUG,"Connecting with Node %.40s at %s:%d",
            node->name, node->ip, node->port+REDIS_CLUSTER_PORT_INCR);
}
```

随机周期性发送PING消息

```
/* Ping some random node 1 time every 10 iterations, so that we usually ping
 * one random node every second. */
// clusterCron() 每执行 10 次（至少间隔一秒钟），就向一个随机节点发送 gossip 信息
if (!(iteration % 10)) {
    int j;
    /* Check a few random nodes and ping the one with the oldest
     * pong_received time. */
    // 随机 5 个节点，选出其中一个
    for (j = 0; j < 5; j++) {
        // 随机在集群中挑选节点
        de = dictGetRandomKey(server.cluster->nodes);
        clusterNode *this = dictGetVal(de);
        /* Don't ping nodes disconnected or with a ping currently active. */
        // 不要 PING 连接断开的节点，也不要 PING 最近已经 PING 过的节点
        if (this->link == NULL || this->ping_sent != 0) continue;
        if (this->flags & (REDIS_NODE_MYSELF|REDIS_NODE_HANDSHAKE))
            continue;
        // 选出 5 个随机节点中最近一次接收 PONG 回复距离现在最旧的节点
        if (min_pong_node == NULL || min_pong > this->pong_received) {
            min_pong_node = this;
            min_pong = this->pong_received;
        }
    }
    // 向最久没有收到 PONG 回复的节点发送 PING 命令
    if (min_pong_node) {
        redisLog(REDIS_DEBUG,"Pinging node %.40s", min_pong_node->name);
        clusterSendPing(min_pong_node->link, CLUSTERMSG_TYPE_PING);
    }
}
```

防止节点假超时及状态过期

```
/* If we are waiting for the PONG more than half the cluster
 * timeout, reconnect the link: maybe there is a connection
 * issue even if the node is alive. */
// 如果等到 PONG 到达的时间超过了 node timeout 一半的连接
// 因为尽管节点依然正常，但连接可能已经出问题了
if (node->link && /* is connected */
    now - node->link->ctime >
    server.cluster_node_timeout && /* was not already reconnected */
    node->ping_sent && /* we already sent a ping */
    node->pong_received < node->ping_sent && /* still waiting pong */
    /* and we are waiting for the pong more than timeout/2 */
    now - node->ping_sent > server.cluster_node_timeout/2)
{
    /* Disconnect the link, it will be reconnected automatically. */
    // 释放连接，下次 clusterCron() 会自动重连
    freeClusterLink(node->link);
}
/* If we have currently no active ping in this instance, and the
 * received PONG is older than half the cluster timeout, send
 * a new ping now, to ensure all the nodes are pinged without
 * a too big delay. */
// 如果目前没有在 PING 节点
// 并且已经有 node timeout 一半的时间没有从节点那里收到 PONG 回复
// 那么向节点发送一个 PING ，确保节点的信息不会太旧
// （因为一部分节点可能一直没有被随机中）
if (node->link &&
    node->ping_sent == 0 &&
    (now - node->pong_received) > server.cluster_node_timeout/2)
{
    clusterSendPing(node->link, CLUSTERMSG_TYPE_PING);
    continue;
}
```

处理failover和标记疑似下线

```
/* If we are a master and one of the slaves requested a manual
 * failover, ping it continuously. */
// 如果这是一个主节点，并且有一个从服务器请求进行手动故障转移
// 那么向从服务器发送 PING 。
if (server.cluster->mf_end &&
    nodeIsMaster(myself) &&
    server.cluster->mf_slave == node &&
    node->link)
{
    clusterSendPing(node->link, CLUSTERMSG_TYPE_PING);
    continue;
}
/* Check only if we have an active ping for this instance. */
// 以下代码只在节点发送了 PING 命令的情况下执行
if (node->ping_sent == 0) continue;
/* Compute the delay of the PONG. Note that if we already received
 * the PONG, then node->ping_sent is zero, so can't reach this
 * code at all. */
// 计算等待 PONG 回复的时长
delay = now - node->ping_sent;
// 等待 PONG 回复的时长超过了限制值，将目标节点标记为 PFAIL （疑似下线）
if (delay > server.cluster_node_timeout) {
    /* Timeout reached. Set the node as possibly failing if it is
     * not already in this state. */
    if (!(node->flags & (REDIS_NODE_PFAIL|REDIS_NODE_FAIL))) {
        redisLog(REDIS_DEBUG,"*** NODE %.40s possibly failing",
            node->name);
        // 打开疑似下线标记
        node->flags |= REDIS_NODE_PFAIL;
        update_state = 1;
    }
}
```

由上可知，`server.cluster_node_timeout`是判断节点状态过期及疑似下线的标准，所以对于不同网络状态和规模的集群，要视实际情况设定。

实际发送Gossip消息

以下是前方多次调用过的clusterSendPing()方法的源码，不难理解。

```
/* Send a PING or PONG packet to the specified node, making sure to add enough
 * gossip informations. */
// 向指定节点发送一条 MEET 、 PING 或者 PONG 消息
void clusterSendPing(clusterLink *link, int type) {
    unsigned char buf[sizeof(clusterMsg)];
    clusterMsg *hdr = (clusterMsg*) buf;
    int gossipcount = 0, totlen;
    /* freshnodes is the number of nodes we can still use to populate the
     * gossip section of the ping packet. Basically we start with the nodes
     * we have in memory minus two (ourself and the node we are sending the
     * message to). Every time we add a node we decrement the counter, so when
     * it will drop to <= zero we know there is no more gossip info we can
     * send. */
    // freshnodes 是用于发送 gossip 信息的计数器
    // 每次发送一条信息时，程序将 freshnodes 的值减一
    // 当 freshnodes 的数值小于等于 0 时，程序停止发送 gossip 信息
    // freshnodes 的数量是节点目前的 nodes 表中的节点数量减去 2 
    // 这里的 2 指两个节点，一个是 myself 节点（也即是发送信息的这个节点）
    // 另一个是接受 gossip 信息的节点
    int freshnodes = dictSize(server.cluster->nodes)-2;
 
    // 如果发送的信息是 PING ，那么更新最后一次发送 PING 命令的时间戳
    if (link->node && type == CLUSTERMSG_TYPE_PING)
        link->node->ping_sent = mstime();
 
    // 将当前节点的信息（比如名字、地址、端口号、负责处理的槽）记录到消息里面
    clusterBuildMessageHdr(hdr,type);
 
    /* Populate the gossip fields */
    // 从当前节点已知的节点中随机选出两个节点
    // 并通过这条消息捎带给目标节点，从而实现 gossip 协议
 
    // 每个节点有 freshnodes 次发送 gossip 信息的机会
    // 每次向目标节点发送 2 个被选中节点的 gossip 信息（gossipcount 计数）
    while(freshnodes > 0 && gossipcount < 3) {
        // 从 nodes 字典中随机选出一个节点（被选中节点）
        dictEntry *de = dictGetRandomKey(server.cluster->nodes);
        clusterNode *this = dictGetVal(de);
 
        clusterMsgDataGossip *gossip;
        int j;
 
        /* In the gossip section don't include:
         * 以下节点不能作为被选中节点：
         * 1) Myself.
         *    节点本身。
         * 2) Nodes in HANDSHAKE state.
         *    处于 HANDSHAKE 状态的节点。
         * 3) Nodes with the NOADDR flag set.
         *    带有 NOADDR 标识的节点
         * 4) Disconnected nodes if they don't have configured slots.
         *    因为不处理任何槽而被断开连接的节点 
         */
        if (this == myself ||
            this->flags & (REDIS_NODE_HANDSHAKE|REDIS_NODE_NOADDR) ||
            (this->link == NULL && this->numslots == 0))
        {
                freshnodes--; /* otherwise we may loop forever. */
                continue;
        }
 
        /* Check if we already added this node */
        // 检查被选中节点是否已经在 hdr->data.ping.gossip 数组里面
        // 如果是的话说明这个节点之前已经被选中了
        // 不要再选中它（否则就会出现重复）
        for (j = 0; j < gossipcount; j++) {
            if (memcmp(hdr->data.ping.gossip[j].nodename,this->name,
                    REDIS_CLUSTER_NAMELEN) == 0) break;
        }
        if (j != gossipcount) continue;
 
        /* Add it */
 
        // 这个被选中节点有效，计数器减一
        freshnodes--;
 
        // 指向 gossip 信息结构
        gossip = &(hdr->data.ping.gossip[gossipcount]);
 
        // 将被选中节点的名字记录到 gossip 信息
        memcpy(gossip->nodename,this->name,REDIS_CLUSTER_NAMELEN);
        // 将被选中节点的 PING 命令发送时间戳记录到 gossip 信息
        gossip->ping_sent = htonl(this->ping_sent);
        // 将被选中节点的 PING 命令回复的时间戳记录到 gossip 信息
        gossip->pong_received = htonl(this->pong_received);
        // 将被选中节点的 IP 记录到 gossip 信息
        memcpy(gossip->ip,this->ip,sizeof(this->ip));
        // 将被选中节点的端口号记录到 gossip 信息
        gossip->port = htons(this->port);
        // 将被选中节点的标识值记录到 gossip 信息
        gossip->flags = htons(this->flags);
 
        // 这个被选中节点有效，计数器增一
        gossipcount++;
    }
 
    // 计算信息长度
    totlen = sizeof(clusterMsg)-sizeof(union clusterMsgData);
    totlen += (sizeof(clusterMsgDataGossip)*gossipcount);
    // 将被选中节点的数量（gossip 信息中包含了多少个节点的信息）
    // 记录在 count 属性里面
    hdr->count = htons(gossipcount);
    // 将信息的长度记录到信息里面
    hdr->totlen = htonl(totlen);
 
    // 发送信息
    clusterSendMessage(link,buf,totlen);
}
```

### The End

贴的源码有点多了，自己看着都略头疼。

明天还要搬砖，晚安吧各位。