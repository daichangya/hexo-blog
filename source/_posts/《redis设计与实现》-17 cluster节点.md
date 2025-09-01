---
title: 《redis设计与实现》-17 cluster节点
id: 1526
date: 2024-10-31 22:02:00
author: daichangya
permalink: /archives/redis%E8%AE%BE%E8%AE%A1%E4%B8%8E%E5%AE%9E%E7%8E%B0-17cluster%E8%8A%82%E7%82%B9/
categories:
 - redis
---


 关于redis的集群，官网介绍比较全面了。[https://redis.io/topics/cluster-spec](https://redis.io/topics/cluster-spec)  

设计目标：

*   High performance and linear scalability up to 1000 nodes. There are no proxies, asynchronous replication is used, and no merge operations are performed on values.
    *   高达1000个节点的线性**可扩展性**。没有代理，使用异步复制，并且在进行赋值时没有合并操作
*   Acceptable degree of write safety: the system tries (in a best-effort way) to retain all the writes originating from clients connected with the majority of the master nodes. Usually there are small windows where acknowledged writes can be lost. Windows to lose acknowledged writes are larger when clients are in a minority partition.
    *   可接受程度的**写安全**：当客户端与大多数master节点建立连接后，系统努力（使用最优的方式）保持来自客户端的写操作。通常有小窗口，其中确认的写操作可能会丢失。当客户端在一个小的分区中，窗口丢失写操作会更大。
*   Availability: Redis Cluster is able to survive partitions where the majority of the master nodes are reachable and there is at least one reachable slave for every master node that is no longer reachable. Moreover using *replicas migration*, masters no longer replicated by any slave will receive one from a master which is covered by multiple slaves.
    *   **可用性：**Redis集群支持网络分区——其中大部分主节点都可访问，并且不可访问的各master节点对应的从至少一个可访问。而且采用副本迁移，有多个从的主会提供一个从给没有从的主。

正是`Redis Cluster`是`Redis`的分布式解决方案，所以redis才能实现分布式Nosql数据库.有效解决了`Redis`分布式方面的需求。当遇到单机内存、并发、流量等瓶颈时，可以采用`Cluster`架构达到负载均衡的目的。

   背景知识点：**数据分布理论**。分布式数据库首要解决**把整个数据集按照分区规则映射到多个节点**的问题，即把数据集划分到多个节点上，每个节点负责整个数据的一个子集，先简单介绍下分布式数据库的数据分区。所谓的数据分区就是将一个较大的数据集分布在不同的节点上进行储存。常见的数据分区方式：节点取余、一致性哈希、虚拟槽。

**节点取余**：根据key的hash值和节点数取模的方式计算出节点ID，然后向对应的节点提交数据。

             缺点：节点的增删会造成大量的数据迁移。

**一致性哈希**：对于任何的哈希函数，都有其取值范围。我们可以用环形结构来标识范围。通过哈希函数，每个节点都会被分配到环上的一个位置，每个键值也会被映射到环上的一个位置，然后顺时针找到相邻的节点。限于篇幅不再展开，

      缺点：节点调整会造成数据分布不均等的问题。

**虚拟槽**：虚拟槽分区巧妙地使用了哈希空间，使用分散度良好的哈希函数把所有的数据映射到一个固定范围内的整数集合，整数定义为槽（slot）。比如Redis Cluster槽的范围是0 ～ 16383。槽是集群内数据管理和迁移的基本单位。采用大范围的槽的主要目的是为了方便数据的拆分和集群的扩展，每个节点负责一定数量的槽。

## 二 节点 Node

       在单机版的Redis中，每个Master之间是没有任何通信的，要组件一个真正可工作的集群，我们必须将各个独立的节点连接起来，构成一个包含多个节点的集群.

连接各个节点的工作可以使用CLUSTER MEET命令来完成，该命令的格式如下：

CLUSTER MEET <ip> <port>

        向一个节点node发送CLUSTER MEET命令，可以让node节点与ip和port所指定的节点进行握手（handshake），当握手成功时，node节点就会将ip和port所指定的节点添加到当前所在的集群中。

###      2.1 启动节点

      一个节点就是一个运行在集群模式下的Redis服务器，Redis服务器在启动时会根据cluster_enabled配置选项是否为yes来决定是否开启服务器的集群模式。

```cpp
....
    // 集群开启，则初始化cluster
    if (server.cluster_enabled) clusterInit();
...
```

```cpp
// 初始化集群
void clusterInit(void) {
    int saveconf = 0;
	  // 初始化配置
    server.cluster = zmalloc(sizeof(clusterState));
    server.cluster->myself = NULL;
    server.cluster->currentEpoch = 0;
    // 初始为 FAIL 状态
    server.cluster->state = CLUSTER_FAIL;
    // master 节点数
    server.cluster->size = 1;
    server.cluster->todo_before_sleep = 0;
    server.cluster->nodes = dictCreate(&clusterNodesDictType,NULL);
    server.cluster->nodes_black_list =
        dictCreate(&clusterNodesBlackListDictType,NULL);
    server.cluster->failover_auth_time = 0;
    server.cluster->failover_auth_count = 0;
    server.cluster->failover_auth_rank = 0;
    server.cluster->failover_auth_epoch = 0;
    server.cluster->cant_failover_reason = CLUSTER_CANT_FAILOVER_NONE;
    server.cluster->lastVoteEpoch = 0;
    server.cluster->stats_bus_messages_sent = 0;
    server.cluster->stats_bus_messages_received = 0;
    memset(server.cluster->slots,0, sizeof(server.cluster->slots));
    clusterCloseAllSlots();
 
    /* Lock the cluster config file to make sure every node uses
     * its own nodes.conf. */
     // 配置文件上锁 
    if (clusterLockConfig(server.cluster_configfile) == C_ERR)
        exit(1);
 
    /* Load or create a new nodes configuration. */
     // 载入或创建一个新的节点配置文件
    if (clusterLoadConfig(server.cluster_configfile) == C_ERR) {
        /* No configuration found. We will just use the random name provided
         * by the createClusterNode() function. */
        // 没找到配置文件，随机创建一个集群节点 
        myself = server.cluster->myself =
            createClusterNode(NULL,CLUSTER_NODE_MYSELF|CLUSTER_NODE_MASTER);
        serverLog(LL_NOTICE,"No cluster configuration found, I'm %.40s",
            myself->name);
        // 添加到当前集群节点的配置中(// 该 nodes 维护的是一张 nodeName -> node 的 hash 表)    
        clusterAddNode(myself);
        saveconf = 1;
    }
     // 写配置文件
    if (saveconf) clusterSaveConfigOrDie(1);
 
    /* We need a listening TCP port for our cluster messaging needs. */
    server.cfd_count = 0;
 
    /* Port sanity check II
     * The other handshake port check is triggered too late to stop
     * us from trying to use a too-high cluster port number. */
     // 检查端口号是否合法(<=65535) 
    if (server.port > (65535-CLUSTER_PORT_INCR)) {
        serverLog(LL_WARNING, "Redis port number too high. "
                   "Cluster communication port is 10,000 port "
                   "numbers higher than your Redis port. "
                   "Your Redis port number must be "
                   "lower than 55535.");
        exit(1);
    }
      // 将该集群节点的端口和fd绑定( 打开 cluster 通道的 非阻塞监听端口) 
    if (listenToPort(server.port+CLUSTER_PORT_INCR,
        server.cfd,&server.cfd_count) == C_ERR)
    {
        exit(1);
    } else {
        int j;
 
        for (j = 0; j < server.cfd_count; j++) {
        	  // 为所有集群的fd设置可读事件的处理函数clusterAcceptHandler
        	  // 可以根据系统平台选择合适的 事件模型(如：Linux 上的 epoll，具体查看 aeApiAddEvent 源码)
            if (aeCreateFileEvent(server.el, server.cfd[j], AE_READABLE,
                clusterAcceptHandler, NULL) == AE_ERR)
                    serverPanic("Unrecoverable error creating Redis Cluster "
                                "file event.");
        }
    }
 
    /* The slots -> keys map is a sorted set. Init it. */
    // 创建槽映射到键的有序集合
    server.cluster->slots_to_keys = zslCreate();
 
    /* Set myself->port to my listening port, we'll just need to discover
     * the IP address via MEET messages. */
     // 设置集群端口 
    myself->port = server.port;
    // 没有正在进行手动的故障转移
    server.cluster->mf_end = 0;
     // 重置与手动故障转移的状态
    resetManualFailover();
}
```

  从该部分源码可以看出 Redis Cluster 初始化部分的核心主要是 nodes.conf 的加载，以及 cluster bus 通道的监听服务的启动 这两部分.

   节点会继续使用redisServer结构来保存服务器的状态，使用redisClient结构来保存客户端的状态，至于那些只有在集群模式下才会用到的数据，节点将它们保存到了cluster.h/clusterNode结构、cluster.h/clusterLink结构，以及cluster.h/clusterState结构里面。下面分别介绍。

### 2.2 集群数据结构

      clusterNode结构保存了一个节点的当前状态，比如节点的创建时间、节点的名字、节点当前的配置纪元、节点的IP地址和端口号等等。

```objectivec
typedef struct clusterNode {
	  // 创建节点的时间
    mstime_t ctime; /* Node object creation time. */
    // 节点的名字，由 40 个十六进制字符组成
    char name[CLUSTER_NAMELEN]; /* Node name, hex string, sha1-size */
    // 节点标识
    // 使用各种不同的标识值记录节点的角色（比如主节点或者从节点），
    // 以及节点目前所处的状态（比如在线或者下线）。
    int flags;      /* CLUSTER_NODE_... */
     // 节点当前的配置纪元，用于实现故障转移
    uint64_t configEpoch; /* Last configEpoch observed for this node */
    // 由这个节点负责处理的槽
    //(一共有 REDIS_CLUSTER_SLOTS / 8 个字节长,每个字节的每个位记录了一个槽的保存状态位,值为 1 表示槽正由本节点处理，值为 0 则表示槽并非本节点处理)
    unsigned char slots[CLUSTER_SLOTS/8]; /* slots handled by this node */
    // 该节点负责处理的槽数量
    int numslots;   /* Number of slots handled by this node */
     // 如果本节点是主节点，那么用这个属性记录从节点的数量
    int numslaves;  /* Number of slave nodes, if this is a master */
     // 指针数组，指向各个从节点
    struct clusterNode **slaves; /* pointers to slave nodes */
     // 指向主节点，即使是从节点也可以为NULL
    struct clusterNode *slaveof; /* pointer to the master node. Note that it
                                    may be NULL even if the node is a slave
                                    if we don't have the master node in our
                                    tables. */
    // 最后一次发送 PING 命令的时间                                
    mstime_t ping_sent;      /* Unix time we sent latest ping */
    // 接收到PONG的时间
    mstime_t pong_received;  /* Unix time we received the pong */
    // 最后一次被设置为 FAIL 状态的时间
    mstime_t fail_time;      /* Unix time when FAIL flag was set */
     // 最后一次给某个从节点投票的时间
    mstime_t voted_time;     /* Last time we voted for a slave of this master */
     // 最后一次从这个节点接收到复制偏移量的时间
    mstime_t repl_offset_time;  /* Unix time we received offset for this node */
    // 孤立的主节点迁移的时间
    mstime_t orphaned_time;     /* Starting time of orphaned master condition */
    // 该节点已知的复制偏移量
    long long repl_offset;      /* Last known repl offset for this node. */
     // 节点的 IP 地址
    char ip[NET_IP_STR_LEN];  /* Latest known IP address of this node */
     // 节点的端口号
    int port;                   /* Latest known port of this node */
     // 保存连接节点所需的有关信息
    clusterLink *link;          /* TCP/IP link with this node */
     // 保存下线报告的链表
    list *fail_reports;         /* List of nodes signaling this as failing */
} clusterNode;
```

   clusterNode结构的link属性是一个clusterLink结构，该结构保存了连接节点所需的有关信息，比如套接字描述符，输入缓冲区和输出缓存区:    

```cpp
 
/* clusterLink encapsulates everything needed to talk with a remote node. */
// clusterLink 包含了与其他节点进行通讯所需的全部信息
typedef struct clusterLink {
	 // 连接创建的时间
    mstime_t ctime;             /* Link creation time */
    // TCP 套接字描述符
    int fd;                     /* TCP socket file descriptor */
    // 输出缓冲区，保存着等待发送给其他节点的消息（message）。
    sds sndbuf;                 /* Packet send buffer */
    // 输入缓冲区，保存着从其他节点接收到的消息。
    sds rcvbuf;                 /* Packet reception buffer */
     // 与这个连接相关联的节点，如果没有的话就为 NULL
    struct clusterNode *node;   /* Node related to this link if any, or NULL */
} clusterLink;
```

         redisClient结构和clusterLink结构都有自己的套接字描述符和输入、输出缓冲区，这两个结构区别在于，**redisClient结构中的套接字和缓冲区是用于连接客户端的，而clusterLink结构中的套接字和缓冲区则是用于连接节点的。**                                            最后，每个节点都保存着一个clusterState结构，这个结构记录了在当前节点的视角下，集群目前所处的状态。                         

```cpp
typedef struct clusterState {
	   // 指向当前节点的指针
    clusterNode *myself;  /* This node */
    // 集群当前的配置纪元，用于实现故障转移
    uint64_t currentEpoch;
    // 集群当前的状态：是在线还是下线
    int state;            /* CLUSTER_OK, CLUSTER_FAIL, ... */     
     // 集群中至少负责一个槽的主节点个数
    int size;             /* Num of master nodes with at least one slot */
    // 集群节点名单（包括 myself 节点）                     
    // 字典的键为节点的名字，字典的值为 clusterNode 结构
    dict *nodes;          /* Hash table of name -> clusterNode structures */
    // 防止重复添加节点的黑名单
    dict *nodes_black_list; /* Nodes we don't re-add for a few seconds. */
    // 导出槽数据到目标节点，该数组记录这些节点
    clusterNode *migrating_slots_to[CLUSTER_SLOTS];
    // 导入槽数据到目标节点，该数组记录这些节点
    clusterNode *importing_slots_from[CLUSTER_SLOTS];
     // 槽和负责槽节点的映射(负责处理各个槽的节点)                                   
     // 例如 slots[i] = clusterNode_A 表示槽 i 由节点 A 处理
    clusterNode *slots[CLUSTER_SLOTS];
    //槽映射到键的有序集合( 跳表中以槽作为分值，键作为成员，对槽进行有序排序，当有需要对槽进行区间range操作时，会很方便 )
    zskiplist *slots_to_keys;
    /* The following fields are used to take the slave state on elections. */
    // 以下这些域被用于进行故障转移选举
    // 上次执行选举或者下次执行选举的时间
    mstime_t failover_auth_time; /* Time of previous or next election. */
    // 节点获得的投票数量
    int failover_auth_count;    /* Number of votes received so far. */
    // 如果为真，表示本节点已经向其他节点发送了投票请求
    int failover_auth_sent;     /* True if we already asked for votes. */
    // 该从节点在当前请求中的排名
    int failover_auth_rank;     /* This slave rank for current auth request. */
    // 当前选举的纪元
    uint64_t failover_auth_epoch; /* Epoch of the current election. */
     // 从节点不能执行故障转移的原因
    int cant_failover_reason;   /* Why a slave is currently not able to
                                   failover. See the CANT_FAILOVER_* macros. */
    /* Manual failover state in common. */
     /* 共用的手动故障转移状态 */
    // 如果为0，表示没有正在进行手动的故障转移。否则表示手动故障转移的时间限制 
    mstime_t mf_end;            /* Manual failover time limit (ms unixtime).
                                   It is zero if there is no MF in progress. */
    /* Manual failover state of master. */
    /* 主服务器的手动故障转移状态 */ 
    clusterNode *mf_slave;   /* Slave performing the manual failover. */
    /* Manual failover state of slave. */
    // 从节点记录手动故障转移时的主节点偏移量
    long long mf_master_offset; /* Master offset the slave needs to start MF
                                   or zero if stil not received. */
    // 非零值表示手动故障转移能开始                               
    int mf_can_start;           /* If non-zero signal that the manual failover
                                   can start requesting masters vote. */
    /* The followign fields are used by masters to take state on elections. */
    /* 以下这些域由主服务器使用，用于记录选举时的状态 */
    // 集群最近一次投票的纪元
    uint64_t lastVoteEpoch;     /* Epoch of the last vote granted. */     
    // 调用clusterBeforeSleep()所做的一些事，以各个 flag 来记录
    int todo_before_sleep; /* Things to do in clusterBeforeSleep(). */
     // 通过 cluster 连接发送的消息数量
    long long stats_bus_messages_sent;  /* Num of msg sent via cluster bus. */
    // 通过 cluster 接收到的消息数量
    long long stats_bus_messages_received; /* Num of msg rcvd via cluster bus.*/
} clusterState;
```

###  2.3 CLUSTER MEET命令的实现                                                                                                  

   通过向节点A发送CLUSTER MEET命令，客户端可以让接收命令的节点A将另一个节点B添加到节点A当前所在的集群里面：

    CLUSTER MEET <ip> <port>

收到命令的节点A将与节点B进行握手（handshake），以此来确认彼此的存在，并为将来的进一步通信打好基础：

*   节点A会为节点B创建一个clusterNode结构，并将该结构添加到自己的clusterState.nodes字典里面
*   之后，节点A将根据CLUSTER MEET命令给定的IP地址和端口号，向节点B发送一条MEET消息（message）
*   如果一切顺利，节点B将接收到节点A发送的MEET消息，节点B会为节点A创建一个clusterNode结构，并将该结构添加到自己的clusterState.nodes字典里面
*   之后，节点B将向节点A返回一条PONG消息
*   如果一切顺利，节点A将接收到节点B返回的PONG消息，通过这条PONG消息节点A可以知道节点B已经成地接收了自己发送的MEET消息
*   之后，节点A将向节点B返回一条PING消息
*   如果一切顺利，节点B将接收到节点A返回的PING消息，通过这条PING消息节点B可以知道节点A已经成功地接收到了自己返回的PONG消息，握手完成。
*   之后，节点A会将节点B的信息通过Gossip协议传播给集群中的其他节点，让其他节点也与节点B进行握手，最终，经过一段时间之后，节点B会被集群中的所有节点认识。

上面是书上介绍的流程，下面看下源码的实现。

**2.3.1 A 节点发送MEET给B节点**

  由客户端发起命令：`cluster meet <ip> <port>`

当节点接收到客户端的`cluster meet`命令后会调用对应的函数来处理命令，该命令的执行函数是`clusterCommand()`函数，

```cpp
// CLUSTER 命令的实现
void clusterCommand(client *c) {
	   // 不能在非集群模式下使用该命令
    if (server.cluster_enabled == 0) {
        addReplyError(c,"This instance has cluster support disabled");
        return;
    }
    // CLUSTER MEET <ip> <port>命令
    // 与给定地址的节点建立连接
    if (!strcasecmp(c->argv[1]->ptr,"meet") && c->argc == 4) {
        long long port;
        // 获取端口
        if (getLongLongFromObject(c->argv[3], &port) != C_OK) {
            addReplyErrorFormat(c,"Invalid TCP port specified: %s",
                                (char*)c->argv[3]->ptr);
            return;
        }
        // 尝试与给定地址的节点进行连接 
        if (clusterStartHandshake(c->argv[2]->ptr,port) == 0 &&
            errno == EINVAL)
        {
        	  // 连接失败 
            addReplyErrorFormat(c,"Invalid node address specified: %s:%s",
                            (char*)c->argv[2]->ptr, (char*)c->argv[3]->ptr);
        } else {
        	  // 连接成功回复ok
            addReply(c,shared.ok);
        }
....
}
```

该函数先根据`cluster meet <ip> <port>`命令传入的参数，获取要与目标节点建立连接的节点地址，然后根据节点地址执行`clusterStartHandshake()`函数来开始执行握手操作。该函数代码如下：     

```cpp
/* Start an handshake with the specified address if there is not one
 * already in progress. Returns non-zero if the handshake was actually
 * started. On error zero is returned and errno is set to one of the
 * following values:
 * 如果还没有与指定的地址进行过握手，那么进行握手。
 * 返回 1 表示握手已经开始，
 * 返回 0 并将 errno 设置为以下值来表示意外情况：
 * EAGAIN - There is already an handshake in progress for this address.
             已经有握手在进行中了。
 * EINVAL - IP or port are not valid. 
             ip 或者 port 参数不合法。 
 */
int clusterStartHandshake(char *ip, int port) {
    clusterNode *n;
    char norm_ip[NET_IP_STR_LEN];
    struct sockaddr_storage sa;
 
    /* IP sanity check */
     // 检查地址是否非法
    if (inet_pton(AF_INET,ip,
            &(((struct sockaddr_in *)&sa)->sin_addr)))
    {
        sa.ss_family = AF_INET;
    } else if (inet_pton(AF_INET6,ip,
            &(((struct sockaddr_in6 *)&sa)->sin6_addr)))
    {
        sa.ss_family = AF_INET6;
    } else {
        errno = EINVAL;
        return 0;
    }
 
    /* Port sanity check */
    // port 合法性检查
    if (port <= 0 || port > (65535-CLUSTER_PORT_INCR)) {
        errno = EINVAL;
        return 0;
    }
 
    /* Set norm_ip as the normalized string representation of the node
     * IP address. */
    // 设置 norm_ip 作为节点地址的标准字符串表示形式 
    memset(norm_ip,0,NET_IP_STR_LEN);
    if (sa.ss_family == AF_INET)
        inet_ntop(AF_INET,
            (void*)&(((struct sockaddr_in *)&sa)->sin_addr),
            norm_ip,NET_IP_STR_LEN);
    else
        inet_ntop(AF_INET6,
            (void*)&(((struct sockaddr_in6 *)&sa)->sin6_addr),
            norm_ip,NET_IP_STR_LEN);
    // 判断当前地址是否处于握手状态，如果是，则设置errno并返回，该函数被用来避免重复和相同地址的节点进行握手
    if (clusterHandshakeInProgress(norm_ip,port)) {
        errno = EAGAIN;
        return 0;
    }
 
    /* Add the node with a random address (NULL as first argument to
     * createClusterNode()). Everything will be fixed during the
     * handshake. */
    // 为node设置一个随机的名字，当握手完成时会为其设置真正的名字
    // 创建一个随机名字的节点 
    n = createClusterNode(NULL,CLUSTER_NODE_HANDSHAKE|CLUSTER_NODE_MEET);
     // 设置地址
    memcpy(n->ip,norm_ip,sizeof(n->ip));    
    n->port = port;
     // 添加到集群中
    clusterAddNode(n);
    return 1;
}
```

    该函数先判断传入的地址是否非法，如果非法会设置`errno`，然后会调用`clusterHandshakeInProgress()`函数来判断是否要进行握手的节点也处于握手状态，以避免重复和相同地址的目标节点进行握手。然后创建一个随机名字的目标节点，并设置该目标节点的状态.然后调用`clusterAddNode()`函数将该目标节点添加到集群中，也就是`server.cluster->nodes`字典，该字典的键是节点的名字，值是指向`clusterNode()`结构的指针。                                                                                                                                     此时A节点并没有将`meet`消息发送给指定地址的目标节点，而是设置集群中目标节点的状态。而发送`meet`消息则是在`clusterCron()`函数中执行。                                                                                                                                                                

```cpp
 
/* This is executed 10 times every second */
// 集群的周期性执行函数。每秒执行10次，100ms执行一次
void clusterCron(void) {
    dictIterator *di;
    dictEntry *de;
    int update_state = 0;
    // 没有从节点从属的主节点个数
    int orphaned_masters; /* How many masters there are without ok slaves. */
     // 所有主节点附属的最多的从节点数量
    int max_slaves; /* Max number of ok slaves for a single master. */
    // 如果myself是从节点，该从节点对应的主节点下有多少从节点
    int this_slaves; /* Number of ok slaves for our master (if we are slave). */
    mstime_t min_pong = 0, now = mstime();
    clusterNode *min_pong_node = NULL;
     // 静态变量，表示该函数执行的计数器
    static unsigned long long iteration = 0;
    mstime_t handshake_timeout;
 
    // 记录一次迭代
    iteration++; /* Number of times this function was called so far. */
 
    /* The handshake timeout is the time after which a handshake node that was
     * not turned into a normal node is removed from the nodes. Usually it is
     * just the NODE_TIMEOUT value, but when NODE_TIMEOUT is too small we use
     * the value of 1 second. */
    // 获取握手状态超时的时间，最低为1s
    // 如果一个处于握手状态的节点如果没有在该超时时限内变成一个普通的节点，那么该节点从节点字典中被删除 
    handshake_timeout = server.cluster_node_timeout;
    if (handshake_timeout < 1000) handshake_timeout = 1000;
 
    /* Check if we have disconnected nodes and re-establish the connection. */
    // 检查是否当前集群中有断开连接的节点和重新建立连接的节点
    di = dictGetSafeIterator(server.cluster->nodes);
     // 遍历所有集群中的节点，如果有未建立连接的节点，那么发送PING或PONG消息，建立连接
    while((de = dictNext(di)) != NULL) {
        clusterNode *node = dictGetVal(de);
        
        // 跳过当前节点以及没有地址的节点
        if (node->flags & (CLUSTER_NODE_MYSELF|CLUSTER_NODE_NOADDR)) continue;
 
        /* A Node in HANDSHAKE state has a limited lifespan equal to the
         * configured node timeout. */
       // 如果仍然node节点处于握手状态，但是从建立连接开始到现在已经超时  
        if (nodeInHandshake(node) && now - node->ctime > handshake_timeout) {
        	  // 从集群中删除该节点，遍历下一个节点
            clusterDelNode(node);
            continue;
        }
        
        // 为未创建连接的节点创建连接
        if (node->link == NULL) {
            int fd;
            mstime_t old_ping_sent;
            clusterLink *link;
            // myself节点连接这个node节点 
            fd = anetTcpNonBlockBindConnect(server.neterr, node->ip,
                node->port+CLUSTER_PORT_INCR, NET_FIRST_BIND_ADDR);
             // 连接出错，跳过该节点    
            if (fd == -1) {
                /* We got a synchronous error from connect before
                 * clusterSendPing() had a chance to be called.
                 * If node->ping_sent is zero, failure detection can't work,
                 * so we claim we actually sent a ping now (that will
                 * be really sent as soon as the link is obtained). */
                // 如果ping_sent为0，察觉故障无法执行，因此要设置发送PING的时间，当建立连接后会真正的的发送PING命令 
                if (node->ping_sent == 0) node->ping_sent = mstime();
                serverLog(LL_DEBUG, "Unable to connect to "
                    "Cluster Node [%s]:%d -> %s", node->ip,
                    node->port+CLUSTER_PORT_INCR,
                    server.neterr);
                continue;
            }
             // 为node节点创建一个连接对象
            link = createClusterLink(node);
             // 设置连接对象的属性
            link->fd = fd;
             // 为node设置连接对象
            node->link = link;
            // 监听该连接的可读事件，设置可读时间的读处理函数
            aeCreateFileEvent(server.el,link->fd,AE_READABLE,
                    clusterReadHandler,link);
            /* Queue a PING in the new connection ASAP: this is crucial
             * to avoid false positives in failure detection.
             *
             * If the node is flagged as MEET, we send a MEET message instead
             * of a PING one, to force the receiver to add us in its node
             * table. */
             /* 向新连接的节点发送 PING 命令，防止节点被识进入下线*/
             // 备份旧的发送PING的时间
            old_ping_sent = node->ping_sent;
             // 如果node节点指定了MEET标识，那么发送MEET命令，否则发送PING命令
            clusterSendPing(link, node->flags & CLUSTER_NODE_MEET ?
                    CLUSTERMSG_TYPE_MEET : CLUSTERMSG_TYPE_PING);
             // 如果不是第一次发送PING命令，要将发送PING的时间还原，等待被clusterSendPing()更新        	
            if (old_ping_sent) {
                /* If there was an active ping before the link was
                 * disconnected, we want to restore the ping time, otherwise
                 * replaced by the clusterSendPing() call. */
                node->ping_sent = old_ping_sent;
            }
            /* We can clear the flag after the first packet is sent.
             * If we'll never receive a PONG, we'll never send new packets
             * to this node. Instead after the PONG is received and we
             * are no longer in meet/handshake status, we want to send
             * normal PING packets. */
            // 发送MEET消息后，清除MEET标识
            // 如果没有接收到PONG回复，那么不会在向该节点发送消息
            // 如果接收到了PONG回复，取消MEET/HANDSHAKE状态，发送一个正常的PING消息 
            node->flags &= ~CLUSTER_NODE_MEET;
 
            serverLog(LL_DEBUG,"Connecting with Node %.40s at %s:%d",
                    node->name, node->ip, node->port+CLUSTER_PORT_INCR);
        }
    }
    dictReleaseIterator(di);
...
}
```

以A节点举例来解释周期性函数中发送`MEET`消息的代码：遍历集群中所有的节点，跳过操作当前A节点和没有指定地址的节点，然后判断处于握手状态的节点是否在建立连接的过程中超时，如果超时则会删除该节点。如果还没有创建连接，那么A节点会与当前这个目标节点建立TCP连接，并获取套接字fd，根据这个套接字，就可以创建clusterLink结构的连接对象，并将这个连接对象保存到当前这个目标节点。

A节点创建完连接后，首先会监听与目标节点建立的fd的可读事件，并设置对应的处理程序clusterReadHandler()，因为当发送MEET消息给目标节点后，要接收目标节点回复的PING。

接下来，A节点就调用clusterSendPing()函数发送MEET消息给目标节点。MEET消息是特殊的PING消息，只用于通知新节点的加入，而PING消息还需要更改一些时间信息，以便进行故障检测。

最后无论如何都要取消CLUSTER\_NODE\_MEET标识，但是没有取消CLUSTER\_NODE\_HANDSHAKE该标识，表示仍处于握手状态，但是已经发送了MEET消息了。

**2.3.2 目标节点处理MEET消息并回复PONG消息**

      当A节点将MEET消息发送给目标节点B之前，就设置了clusterReadHandler()函数为处理接收的PONG消息。当时目标节点B如何接收到MEET消息，并且回复PONG消息给A节点呢？  在集群模式下，每个节点初始化时调用的clusterInit时，会监听节点的端口等待客户端的连接，并且会将该监听的套接字fd保存到server.cfd数组中，然后创建文件事件，监听该套接字fd的可读事件，并设置可读事件处理函数clusterAcceptHandler()，等待客户端发送数据。

```cpp
// 监听事件处理器(集群的fd所设置可读事件的处理函数)
#define MAX_CLUSTER_ACCEPTS_PER_CALL 1000
void clusterAcceptHandler(aeEventLoop *el, int fd, void *privdata, int mask) {
    int cport, cfd;
    int max = MAX_CLUSTER_ACCEPTS_PER_CALL;
    char cip[NET_IP_STR_LEN];
    clusterLink *link;
    UNUSED(el);
    UNUSED(mask);
    UNUSED(privdata);
 
    /* If the server is starting up, don't accept cluster connections:
     * UPDATE messages may interact with the database content. */
    // 如果当前节点正在载入数据，则直接返回。不接收集群的连接 
    if (server.masterhost == NULL && server.loading) return;
 
    // 最大每次调用接收1000个连接
    while(max--) {
    	  // TCP连接的accept
        cfd = anetTcpAccept(server.neterr, fd, cip, sizeof(cip), &cport);
        if (cfd == ANET_ERR) {
            if (errno != EWOULDBLOCK)
                serverLog(LL_VERBOSE,
                    "Error accepting cluster node: %s", server.neterr);
            return;
        }
        // 设置fd为非阻塞模式
        anetNonBlock(NULL,cfd);
        // 禁用 nagle 算法
        anetEnableTcpNoDelay(NULL,cfd);
 
        /* Use non-blocking I/O for cluster messages. */
        serverLog(LL_VERBOSE,"Accepted cluster node %s:%d", cip, cport);
        /* Create a link object we use to handle the connection.
         * It gets passed to the readable handler when data is available.
         * Initiallly the link->node pointer is set to NULL as we don't know
         * which node is, but the right node is references once we know the
         * node identity. */
          // 当连接成功后，为其创建一个连接对象，但是不关联连接的节点 
        link = createClusterLink(NULL);
        link->fd = cfd;
         // 监听该连接的可读事件，并设置处理函数为clusterReadHandler
        aeCreateFileEvent(server.el,cfd,AE_READABLE,clusterReadHandler,link);
    }
}
```

    clusterAcceptHandler()函数，该函数实际上就是accept()函数，接收A节点的连接，然后监听该连接上的可读事件，设置可读事件的处理函数为clusterReadHandler()，等待A节点发送数据，当A节点发送MEET消息给目标节点时，触发目标节点执行clusterReadHandler()函数来处理消息。clusterReadHandler函数主要工作就是解析 cluster bus 上接收的数据并进行消息分包，然后对消息进行处理，而对于消息的分包首先需要了解一下消息结构，Redis Cluster 节点之间通信的消息结构定义如下: 

```cpp
#define CLUSTER_PROTO_VER 0 /* Cluster bus protocol version. */
// 用来表示集群消息的结构（消息头，header）
typedef struct {
	   // "RCmb"的签名
    char sig[4];        /* Siganture "RCmb" (Redis Cluster message bus). */
    // 消息的总长
    uint32_t totlen;    /* Total length of this message */
    // 协议版本，当前为0
    uint16_t ver;       /* Protocol version, currently set to 0. */
    // 未使用的2字节
    uint16_t notused0;  /* 2 bytes not used. */
    // 消息类型
    uint16_t type;      /* Message type */
    // 只在发送PING、PONG和MEET消息时使用
    // 消息正文包含的节点信息数量
    uint16_t count;     /* Only used for some kind of messages. */
    // 消息发送者的配置纪元
    uint64_t currentEpoch;  /* The epoch accordingly to the sending node. */
    // 如果消息发送者是一个主节点，那么这里记录的是消息发送者的配置纪元
    // 如果消息发送者是一个从节点，那么这里记录的是消息发送者正在复制的主节点的配置纪元
    uint64_t configEpoch;   /* The config epoch if it's a master, or the last
                               epoch advertised by its master if it is a
                               slave. */
    // 节点的复制偏移量                           
    uint64_t offset;    /* Master replication offset if node is a master or
                           processed replication offset if node is a slave. */
    // 发送消息的节点的name（ID）                       
    char sender[CLUSTER_NAMELEN]; /* Name of the sender node */
    // 消息发送者目前的槽指派信息
    unsigned char myslots[CLUSTER_SLOTS/8];
    // 如果消息发送者是一个从节点，那么这里记录的是消息发送者正在复制的主节点的名字
    // 如果消息发送者是一个主节点，那么这里记录的是空( REDIS_NODE_NULL_NAME 一个 40 字节长，值全为 0 的字节数组)
    char slaveof[CLUSTER_NAMELEN];
    // 32字节未使用
    char notused1[32];  /* 32 bytes reserved for future usage. */
     // 发送消息节点的端口
    uint16_t port;      /* Sender TCP base port */
    // 发送消息节点的标识
    uint16_t flags;     /* Sender node flags */
    // 消息发送者所处集群的状态
    unsigned char state; /* Cluster state from the POV of the sender */
    // 消息的标识
    unsigned char mflags[3]; /* Message flags: CLUSTERMSG_FLAG[012]_... */
    // 消息的数据
    union clusterMsgData data;
} clusterMsg;
```

 从上面结构可以看到消息分包，主要解析前 8 个字节，分别为:  
  \- char sig\[4\];      // 消息签名，对于 cluster 消息，固定为字符序列 RCmb  
  \- uint32_t totlen;  // 消息总长度  
其他结构成员都是在处理消息时使用的，后续讲解消息处理流程时进行分析。     

```cpp
/* Read data. Try to read the first field of the header first to check the
 * full length of the packet. When a whole packet is in memory this function
 * will call the function to process the packet. And so forth. */
// 读事件处理器
// 首先读入内容的头，以判断读入内容的长度
// 如果内容是一个 whole packet ，那么调用函数来处理这个 packet 。 
void clusterReadHandler(aeEventLoop *el, int fd, void *privdata, int mask) {
    char buf[sizeof(clusterMsg)];
    ssize_t nread;
    clusterMsg *hdr;
    clusterLink *link = (clusterLink*) privdata;
    unsigned int readlen, rcvbuflen;
    UNUSED(el);
    UNUSED(mask);
 
     // 循环从fd读取数据(尽可能地多读数据)
    while(1) { /* Read as long as there is data to read. */
    	  // 获取连接对象的接收缓冲区的长度，表示一次最多能多大的数据量
        rcvbuflen = sdslen(link->rcvbuf);
         // 如果接收缓冲区的长度小于8字节(头信息)，就无法读入消息的总长
        if (rcvbuflen < 8) {
            /* First, obtain the first 8 bytes to get the full message
             * length. */
            readlen = 8 - rcvbuflen;
        } else {// 能够读入完整数据信息
            /* Finally read the full message. */
            hdr = (clusterMsg*) link->rcvbuf;
             // 如果是8个字节
            if (rcvbuflen == 8) {
                /* Perform some sanity check on the message signature
                 * and length. */
                 // 如果前四个字节不是"RCmb"签名，释放连接 
                if (memcmp(hdr->sig,"RCmb",4) != 0 ||
                    ntohl(hdr->totlen) < CLUSTERMSG_MIN_LEN)
                {
                    serverLog(LL_WARNING,
                        "Bad message length or signature received "
                        "from Cluster bus.");
                    handleLinkIOError(link);
                    return;
                }
            }
            // 记录已经读入的内容长度
            readlen = ntohl(hdr->totlen) - rcvbuflen;
            if (readlen > sizeof(buf)) readlen = sizeof(buf);
        }
        
          // 读入内容
        nread = read(fd,buf,readlen);
        // 没有内容可读
        if (nread == -1 && errno == EAGAIN) return; /* No more data ready. */
        	
         // 读错误，释放连接
        if (nread <= 0) {
            /* I/O error... */
            serverLog(LL_DEBUG,"I/O error reading from node link: %s",
                (nread == 0) ? "connection closed" : strerror(errno));
            handleLinkIOError(link);
            return;
        } else {
            /* Read data and recast the pointer to the new buffer. */
            // 将读到的数据追加到连接对象的接收缓冲区中
            link->rcvbuf = sdscatlen(link->rcvbuf,buf,nread);
            hdr = (clusterMsg*) link->rcvbuf;
            rcvbuflen += nread;
        }
 
        /* Total length obtained? Process this packet. */
         // 检查已读入内容的长度，看是否整条信息已经被读入了
        if (rcvbuflen >= 8 && rcvbuflen == ntohl(hdr->totlen)) {
        	   // 如果读到的数据有效，处理读到接收缓冲区的数据
            if (clusterProcessPacket(link)) {
            	 // 处理成功，则设置新的空的接收缓冲区
                sdsfree(link->rcvbuf);
                link->rcvbuf = sdsempty();
            } else {
                return; /* Link no longer valid. */
            }
        }
    }
}
```

     之前在介绍clusterLink对象时，每个连接对象都有一个link->rcvbuf接收缓冲区和link->sndbuf发送缓冲区，因此这个函数就是从fd将数据读到link的接收缓冲区，然后进行是否读完整的判断，如果完整的读完数据，就调用clusterProcessPacket()函数来处理读到的数据，这里会处理MEET消息。  
    

```cpp
/* When this function is called, there is a packet to process starting
 * at node->rcvbuf. Releasing the buffer is up to the caller, so this
 * function should just handle the higher level stuff of processing the
 * packet, modifying the cluster state if needed.
 *
 * 当这个函数被调用时，说明 node->rcvbuf 中有一条待处理的信息。
 * 信息处理完毕之后的释放工作由调用者处理，所以这个函数只需负责处理信息就可以了。
 *
 * The function returns 1 if the link is still valid after the packet
 * was processed, otherwise 0 if the link was freed since the packet
 * processing lead to some inconsistency error (for instance a PONG
 * received from the wrong sender ID).
 * 如果函数返回 1 ，那么说明处理信息时没有遇到问题，连接依然可用。
 * 如果函数返回 0 ，那么说明信息处理时遇到了不一致问题
 * （比如接收到的 PONG 是发送自不正确的发送者 ID 的），连接已经被释放。
  */
int clusterProcessPacket(clusterLink *link) {
	  // 连接的输入（接收）缓冲区
    clusterMsg *hdr = (clusterMsg*) link->rcvbuf;
     // 消息的总长度
    uint32_t totlen = ntohl(hdr->totlen);
     // 消息的类型
    uint16_t type = ntohs(hdr->type);
    // 通过Cluster接收到的消息数量加1
    server.cluster->stats_bus_messages_received++;
    serverLog(LL_DEBUG,"--- Processing packet of type %d, %lu bytes",
        type, (unsigned long) totlen);
 
    /* Perform sanity checks */
     // 检查消息包的合法性
    // 至少包含一个签名、版本、总长、消息正文包含的节点信息数量
    if (totlen < 16) return 1; /* At least signature, version, totlen, count. */
     // 总长度大于接收缓冲区的大小	
    if (totlen > sdslen(link->rcvbuf)) return 1;
     // 目前版本号为0，不处理其他版本
    if (ntohs(hdr->ver) != CLUSTER_PROTO_VER) {
        /* Can't handle messages of different versions. */
        return 1;
    }
    
	  // 获取发送消息节点的标识
    uint16_t flags = ntohs(hdr->flags);
    uint64_t senderCurrentEpoch = 0, senderConfigEpoch = 0;
    clusterNode *sender;
     // 如果消息是PING、PONG或者MEET
    if (type == CLUSTERMSG_TYPE_PING || type == CLUSTERMSG_TYPE_PONG ||
        type == CLUSTERMSG_TYPE_MEET)
    {
    	  // 消息正文包含的节点信息数量
        uint16_t count = ntohs(hdr->count);
        uint32_t explen; /* expected length of this packet */
         // 计算消息包应该的长度
        explen = sizeof(clusterMsg)-sizeof(union clusterMsgData);        
        explen += (sizeof(clusterMsgDataGossip)*count);
        // 总长度和计算的长度不相同返回1
        if (totlen != explen) return 1;
        // 如果消息是FAIL 	
    } else if (type == CLUSTERMSG_TYPE_FAIL) {
    	 // 计算消息包应该的长度    	 
        uint32_t explen = sizeof(clusterMsg)-sizeof(union clusterMsgData);
 
        explen += sizeof(clusterMsgDataFail);
        // 总长度和计算的长度不相同返回1
        if (totlen != explen) return 1;
     // 如果消息是PUBLISH   	
    } else if (type == CLUSTERMSG_TYPE_PUBLISH) {
        uint32_t explen = sizeof(clusterMsg)-sizeof(union clusterMsgData);
 
        explen += sizeof(clusterMsgDataPublish) -
                8 +
                ntohl(hdr->data.publish.msg.channel_len) +
                ntohl(hdr->data.publish.msg.message_len);
        if (totlen != explen) return 1;
      // 如果消息是故障有关的    	
    } else if (type == CLUSTERMSG_TYPE_FAILOVER_AUTH_REQUEST ||
               type == CLUSTERMSG_TYPE_FAILOVER_AUTH_ACK ||
               type == CLUSTERMSG_TYPE_MFSTART)
    {
        uint32_t explen = sizeof(clusterMsg)-sizeof(union clusterMsgData);
 
        if (totlen != explen) return 1;
     //如果消息是UPDATE的   	
    } else if (type == CLUSTERMSG_TYPE_UPDATE) {
        uint32_t explen = sizeof(clusterMsg)-sizeof(union clusterMsgData);
 
        explen += sizeof(clusterMsgDataUpdate);
        if (totlen != explen) return 1;
    }
 
    /* Check if the sender is a known node. */
    //如果消息是UPDATE的
    // 从集群中查找sender节点
    sender = clusterLookupNode(hdr->sender);
     // 节点存在，并且不是 HANDSHAKE 节点
    // 那么个更新节点的配置纪元信息
    if (sender && !nodeInHandshake(sender)) {
        /* Update our curretEpoch if we see a newer epoch in the cluster. */
        // 如果sender的纪元大于集群的纪元，更新集群的纪元
        senderCurrentEpoch = ntohu64(hdr->currentEpoch);
        senderConfigEpoch = ntohu64(hdr->configEpoch);
        // 更新集群的当前纪元
        if (senderCurrentEpoch > server.cluster->currentEpoch)
            server.cluster->currentEpoch = senderCurrentEpoch;
        /* Update the sender configEpoch if it is publishing a newer one. */   
        // 更新sender的配置纪元
        if (senderConfigEpoch > sender->configEpoch) {
            sender->configEpoch = senderConfigEpoch;
             // 更新配置和状态
            clusterDoBeforeSleep(CLUSTER_TODO_SAVE_CONFIG|
                                 CLUSTER_TODO_FSYNC_CONFIG);
        }
        /* Update the replication offset info for this node. */
        // 更新sender的复制偏移量和更新复制偏移量的时间
        sender->repl_offset = ntohu64(hdr->offset);
        sender->repl_offset_time = mstime();
        /* If we are a slave performing a manual failover and our master
         * sent its offset while already paused, populate the MF state. */
        // 如果当前节点是正在执行手动故障转移的从节点，该当前节点的主节点正是sender节点
        // 并且主节点发送复制偏移量时已经暂停手动故障转移 
        if (server.cluster->mf_end &&
            nodeIsSlave(myself) &&
            myself->slaveof == sender &&
            hdr->mflags[0] & CLUSTERMSG_FLAG0_PAUSED &&
            server.cluster->mf_master_offset == 0)
        {
        	  // 设置当前从节点已经复制的偏移量
            server.cluster->mf_master_offset = sender->repl_offset;
            serverLog(LL_WARNING,
                "Received replication offset for paused "
                "master manual failover: %lld",
                server.cluster->mf_master_offset);
        }
    }
 
    /* Initial processing of PING and MEET requests replying with a PONG. */
    // 初始处理PING和MEET请求，用PONG作为回复
    if (type == CLUSTERMSG_TYPE_PING || type == CLUSTERMSG_TYPE_MEET) {
        serverLog(LL_DEBUG,"Ping packet received: %p", (void*)link->node);
 
        /* We use incoming MEET messages in order to set the address
         * for 'myself', since only other cluster nodes will send us
         * MEET messagses on handshakes, when the cluster joins, or
         * later if we changed address, and those nodes will use our
         * official address to connect to us. So by obtaining this address
         * from the socket is a simple way to discover / update our own
         * address in the cluster without it being hardcoded in the config.
         * 我们使用传入的MEET消息来设置当前myself节点的地址，因为只有其他集群中的节点在握手的时会发送MEET消息，
         * 当有节点加入集群时，或者如果我们改变地址，这些节点将使用我们公开的地址来连接我们，
         * 所以在集群中，通过套接字来获取地址是一个简单的方法去discover / update我们自己的地址，而不是在配置中的硬设置
         *
         * However if we don't have an address at all, we update the address
         * even with a normal PING packet. If it's wrong it will be fixed
         * by MEET later.
         * 但是，如果我们根本没有地址，即使使用正常的PING数据包，我们也会更新该地址。 如果是错误的，那么会被MEET修改
          */
        // 如果是MEET消息 或者是其他消息但是当前集群节点的IP为空  
        if (type == CLUSTERMSG_TYPE_MEET || myself->ip[0] == '\0') {
            char ip[NET_IP_STR_LEN];
             // 可以根据fd来获取ip，并设置myself节点的IP
            if (anetSockName(link->fd,ip,sizeof(ip),NULL) != -1 &&
                strcmp(ip,myself->ip))
            {
                memcpy(myself->ip,ip,NET_IP_STR_LEN);
                serverLog(LL_WARNING,"IP address for this node updated to %s",
                    myself->ip);
                clusterDoBeforeSleep(CLUSTER_TODO_SAVE_CONFIG);
            }
        }
 
        /* Add this node if it is new for us and the msg type is MEET.
         * 如果当前节点是第一次遇见这个节点，并且对方发来的是 MEET 信息，
         * 那么将这个节点添加到集群的节点列表里面。
         * In this stage we don't try to add the node with the right
         * flags, slaveof pointer, and so forth, as this details will be
         * resolved when we'll receive PONGs from the node. 
         *  节点目前的 flag 、 slaveof 等属性的值都是未设置的，
         * 等当前节点向对方发送 PING 命令之后，这些信息可以从对方回复的 PONG 信息中取得。
         */
        if (!sender && type == CLUSTERMSG_TYPE_MEET) {
            clusterNode *node;
             // 创建一个处于握手状态的节点
            node = createClusterNode(NULL,CLUSTER_NODE_HANDSHAKE);
             // 设置 IP 和端口
            nodeIp2String(node->ip,link);
            node->port = ntohs(hdr->port);
             // 添加到集群中
            clusterAddNode(node);
            clusterDoBeforeSleep(CLUSTER_TODO_SAVE_CONFIG);
        }
 
        /* If this is a MEET packet from an unknown node, we still process
         * the gossip section here since we have to trust the sender because
         * of the message type. */
        // 如果是从一个未知的节点发送过来MEET包，处理流言信息 
        if (!sender && type == CLUSTERMSG_TYPE_MEET)
        	   // 处理流言中的 PING or PONG 数据包
            clusterProcessGossipSection(hdr,link);
 
        /* Anyway reply with a PONG */
        // 回复一个PONG消息
        clusterSendPing(link,CLUSTERMSG_TYPE_PONG);
    }
....
}
```

       函数代码较长，处理各种消息，这里只截取到处理meet部分。在该函数中，首先先会对消息中的签名、版本、消息总大小，消息中包含的节点信息数量等等都进行判断，确保该消息是一个合法的消息，然后就计算消息的总长度，来判断接收到的消息和读到的消息是否一致完整。

       接着进入if条件判断，首先目标节点会根据MEET消息来获取自己的地址并更新自己的地址，因为如果通过从配置文件来设置地址，当节点重新上线，地址就有可能改变，但是配置文件中却没有修改，所用通过套接字获取地址来更新节点地址是一种非常好的办法。

     然后继续执行第二个if中的代码，第一次MEET消息，而且sender发送该消息的节点并不存在目标节点视角中的集群，所以会为发送消息的A节点创建一个处于握手状态的节点，并且，将该节点加入到目标节点视角中的集群。这样一来，目标节点就知道了A节点的存在。最后就是调用clusterSendPing()函数，指定回复一个PONG消息给A节点。

  此时 目标节点B 中维护的 A 节点信息的 flag 仍然为 HANDSHAKE 阶段(因为 目标节点B 此时并不确认 A节点 已经接收到 PONG 响应)。

**2.3.3  `A`节点处理 PONG 消息回复 PING 消息**

  `A节点`在发送消息`MEET`消息之前，就已经为监听`fd`的可读消息，当目标节点处理完`MEET`消息并回复`PONG`消息之后，触发`A`节点的可读事件，调用`clusterReadHandler()`函数来处理目标节点发送来的`PONG`消息.所以还是同一个函数，但是处理逻辑不同。

```cpp
    /* PING, PONG, MEET: process config information. */
     // 如果是PING、PONG或MEET消息，处理配置信息
    if (type == CLUSTERMSG_TYPE_PING || type == CLUSTERMSG_TYPE_PONG ||
        type == CLUSTERMSG_TYPE_MEET)
    {
        serverLog(LL_DEBUG,"%s packet received: %p",
            type == CLUSTERMSG_TYPE_PING ? "ping" : "pong",
            (void*)link->node);
        //如果关联该连接的节点存在 
        if (link->node) {
        	   // 如果关联该连接的节点处于 HANDSHAKE 状态
            if (nodeInHandshake(link->node)) {
                /* If we already have this node, try to change the
                 * IP/port of the node with the new one. */
                // sender节点存在，用该新的连接地址更新sender节点的地址
                if (sender) {
                    serverLog(LL_VERBOSE,
                        "Handshake: we already know node %.40s, "
                        "updating the address if needed.", sender->name);
                     // 如果有需要的话，更新节点的地址    
                    if (nodeUpdateAddressIfNeeded(sender,link,ntohs(hdr->port)))
                    {
                        clusterDoBeforeSleep(CLUSTER_TODO_SAVE_CONFIG|
                                             CLUSTER_TODO_UPDATE_STATE);
                    }
                    /* Free this node as we already have it. This will
                     * cause the link to be freed as well. */
                  // 释放关联该连接的节点   
                    clusterDelNode(link->node);
                    return 0;
                }
 
                /* First thing to do is replacing the random name with the
                 * right node name if this was a handshake stage. */
                // 用节点的真名sender替换在 HANDSHAKE 时创建的随机名字
                clusterRenameNode(link->node, hdr->sender);
                serverLog(LL_DEBUG,"Handshake with node %.40s completed.",
                    link->node->name);
                // 取消握手状态，设置节点的角色    
                link->node->flags &= ~CLUSTER_NODE_HANDSHAKE;
                link->node->flags |= flags&(CLUSTER_NODE_MASTER|CLUSTER_NODE_SLAVE);
                clusterDoBeforeSleep(CLUSTER_TODO_SAVE_CONFIG);
                
              // 如果sender的地址和关联该连接的节点的地址不相同   
            } else if (memcmp(link->node->name,hdr->sender,
                        CLUSTER_NAMELEN) != 0)
            {
                /* If the reply has a non matching node ID we
                 * disconnect this node and set it as not having an associated
                 * address. */
                serverLog(LL_DEBUG,"PONG contains mismatching sender ID. About node %.40s added %d ms ago, having flags %d",
                    link->node->name,
                    (int)(mstime()-(link->node->ctime)),
                    link->node->flags);
                 // 设置NOADDR标识，清空关联连接节点的地址    
                link->node->flags |= CLUSTER_NODE_NOADDR;
                link->node->ip[0] = '\0';
                link->node->port = 0;
                 // 断开连接
                freeClusterLink(link);
                clusterDoBeforeSleep(CLUSTER_TODO_SAVE_CONFIG);
                return 0;
            }
        }
 
        /* Update the node address if it changed. */
        // 如果发送的消息为PING类型，sender节点不处于握手状态
        // 那么更新sender节点的IP地址
        if (sender && type == CLUSTERMSG_TYPE_PING &&
            !nodeInHandshake(sender) &&
            nodeUpdateAddressIfNeeded(sender,link,ntohs(hdr->port)))
        {
            clusterDoBeforeSleep(CLUSTER_TODO_SAVE_CONFIG|
                                 CLUSTER_TODO_UPDATE_STATE);
        }
 
        /* Update our info about the node */
         // 如果这是一条 PONG 消息，那么更新我们关于 node 节点的认识
        if (link->node && type == CLUSTERMSG_TYPE_PONG) {
        	  // 更新接收到PONG的时间 
            link->node->pong_received = mstime();
            // 清零最近一次发送PING的时间戳
            link->node->ping_sent = 0;
 
            /* The PFAIL condition can be reversed without external
             * help if it is momentary (that is, if it does not
             * turn into a FAIL state).
             *  接到节点的 PONG 回复，我们可以移除节点的 PFAIL 状态。
             *
             * The FAIL condition is also reversible under specific
             * conditions detected by clearNodeFailureIfNeeded(). 
             *  FAIL标识能否删除，需要clearNodeFailureIfNeeded()来决定
             */
            // 如果关联该连接的节点疑似下线 
            if (nodeTimedOut(link->node)) {
            	   // 取消PFAIL标识
                link->node->flags &= ~CLUSTER_NODE_PFAIL;
                clusterDoBeforeSleep(CLUSTER_TODO_SAVE_CONFIG|
                                     CLUSTER_TODO_UPDATE_STATE);
               // 如果关联该连接的节点已经被判断为下线                       
            } else if (nodeFailed(link->node)) {
            	   // 如果一个节点被标识为FAIL，需要检查是否取消该节点的FAIL标识，因为该节点在一定时间内重新上线了
                clearNodeFailureIfNeeded(link->node);
            }
        }
```

      和之前处理MEET消息一样，首先先会对消息中的签名、版本、消息总大小，消息中包含的节点信息数量等等都进行判断，确保该消息是一个合法的消息，然后就计算消息的总长度，来判断接收到的消息和读到的消息是否一致完整。然后处理上述部分的代码。

      由于A节点已经“认识”目标节点，因此A节点在发送MEET消息时已经为集群（A节点视角）中的目标节点设置了连接对象，因此会执行判断连接对象是否存在的代码if (nodeInHandshake(link->node))，并且在A节点发送完MEET消息后，只取消了目标节点的CLUSTER\_NODE\_MEET标识，保留了CLUSTER\_NODE\_HANDSHAKE标识，因此会执行if (sender)判断。

       目标节点发送过来的PONG消息，在消息包的头部会包含sender发送节点的信息，但是名字对不上号，这是因为A节点创建目标节点加入集群的时候，随机给他起的名字，因为A节点当时也不知道目标节点的名字，所以在集群中找不到sender的名字，因此这个判断会失败，调用clusterRenameNode()函数把它的名字改过来，这样myself节点就真正的认识了目标节点，重新认识。之后会将目标节点的CLUSTER\_NODE\_HANDSHAKE状态取消，并且设置它的角色状态。

      然后就是执行if (link->node && type == CLUSTERMSG\_TYPE\_PONG)判断，更新接收PONG的时间戳，清零发送PING的时间戳，根据接收PONG的时间等信息判断目标节点是否下线，如果下线要进行故障转移等操作。  
      之后`A`节点并不会立即向目标节点发送`PING`消息，而是要等待下一次时间事件的发生，在`clusterCron()`函数中，每次执行都需要对集群中所有节点进行故障检测和主从切换等等操作，因此在遍历节点时，会处理以下一种情况：

```cpp
   /* If we have currently no active ping in this instance, and the
         * received PONG is older than half the cluster timeout, send
         * a new ping now, to ensure all the nodes are pinged without
         * a too big delay. */   
 if (node->link &&
            node->ping_sent == 0 &&
            (now - node->pong_received) > server.cluster_node_timeout/2)
        {
            clusterSendPing(node->link, CLUSTERMSG_TYPE_PING);
            continue;
        }
```

当`A`节点接收到`PONG`就会将目标节点`node->ping_sent`设置为`0`，表示目标节点还没有发送过`PING`消息，因此会发送`PING`消息给目标节点。当发送了这个`PING`消息之后，节点之间的握手操作就完成了。之后每隔`1s`都会发送`PING`包，来进行故障检测等工作。

 ![](https://img-blog.csdnimg.cn/20190114213534371.png)                  

书上关于第一节节点的内容先整理到这里。  搭建`Redis Cluster`时，首先通过`CLUSTER MEET`命令将所有的节点加入到一个集群中， 但是并没有在所有节点两两之间都执行`CLUSTER MEET`命令，那么因为节点之间使用`Gossip`协议进行工作。    这个下一篇整理吧。                                                                                                                                                                                  

参考：

[https://blog.csdn.net/men_wen/article/details/72871618](https://blog.csdn.net/men_wen/article/details/72871618)