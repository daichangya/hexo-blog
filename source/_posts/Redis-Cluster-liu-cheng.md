---
title: Redis Cluster 流程
id: 1543
date: 2024-10-31 22:02:00
author: daichangya
permalink: /archives/Redis-Cluster-liu-cheng/
categories:
- redis
---



## 启动节点
## 通过命令配置集群（a. 加入节点  b. 分派slot  c. 添加slave)
## 接受命令处理
- 根据key，转发到不同的节点
- 特殊的标记{…}，可以分派key到相同的节点，{} 不能在key的结尾。如果有{…} ,hash算法则使用{与}中间的字符串来计算，所以一定要在{}中间有字符，不然所有的key将会分配到一个节点。
- 命令中有多个key，如果这些key不在相同的slot（即使在相同的节点也不行），则返回错误（getNodeByQuery）
- 根据key获取节点（getNodeByQuery）

```
1. 根据key 计算 slot 值（keyHashSlot）
2. 如果 slot ，没有对应的 node，则返回错误 CLUSTER_REDIR_DOWN_UNBOUND，对应返回消息：-CLUSTERDOWN
3. 如果多个key，对应不同的slot，则返回错误 CLUSTER_REDIR_CROSS_SLOT，对应的返回消息：-CROSSSLOT。exec 命令命令中的多条子命令包含的所有 key 也需要是在同一个slot中。
4. 如果命令中没有key，则返回当前节点。
5. 如果集群不是 OK 状态，则返回错误 CLUSTER_REDIR_DOWN_STATE，对应返回消息：-CLUSTERDOWN
6. 如果是迁移命令（cmd->proc == migrateCommand），也将返回当前节点。
7. 如果对应slot正往别的节点迁移数据，当前节点没有包含所有命令中需要的key，则返回 ASK（CLUSTER_REDIR_ASK），对应返回消息：-ASK hashslot ip port，对应的节点是迁移的目标节点。
8. 如果对应的slot正从别的节点导入到当前节点，如果包含所有命令中需要的key，则返回当前节点，否则返回错误 CLUSTER_REDIR_UNSTABLE，对应返回消息： -TRYAGAIN
9. 如果客户端设置 CLIENT_READONLY 标记，命令也是只读的，当前是slot 对应的 slave 节点，也将返回当前节点。（如果命令是 eval / evalSha 也与只读命令是同样的处理）
10. 如果slot 对应的节点不是当前节点，则返回 CLUSTER_REDIR_MOVED，对应的消息是：-MOVED hashslot ip port，对应其节点，否则返回当前节点。
11. 总结，如果是对应slot在迁移中，可能返回 ASK，去访问新的节点；如果是导入中，可能返回 TRYAGAIN ,等会重试连接当前节点。ASK 中有调整 ip/port ，而 TRYAGAIN 却没有，注意这个区别。MOVED 消息也是跳转，但是这个是正常的slot节点不是当前节点情况，而ASK 是代表迁移中的slot的情况。
```

##  通过cron定时来检测内部变量状态，发送各种消息（这里面将包含非常重要的高可用实现、自动故障转移）

1.  每秒执行10次，100ms 执行一次
2.  更新内核变量

```
1.  myself->ip = server.cluster\_announce\_ip（因为cluster-announce-ip可以在运行时配置，一旦有更新，及时同步）
2.  handshake\_timeout = server.cluster\_node\_timeout;(同理，cluster\_node_timeout 也是可以在运行时配置，及时同步，如果小于1s，则强制设置为1s，也就是节点超时重试间隔大于1s)
3.  myself->flags , 根据 server.cluster\_slave\_no_failover 的状态情况更新，也就是更新当前节点的failover状态
```

3.  遍历所有节点 server.cluster->nodes
```

1.  统计 pfail 节点 （server.cluster->stats_pfail_nodes++;）
2.  移除 HANDSHAKE 状态，并且超过 handshake_timeout  的节点
3.  如果连接为NULL，则建立连接，发送 MEET / PING 消息，连接成功则去掉CLUSTER\_NODE\_MEET标记
	如果是之前为活动的连接，但是没有成功收到pong消息，则这里将继续保持 ping_send  为之前的值
```

4.  发送消息给最早响应的一个节点

```
1.  大约1s执行一次
2.  在节点列表中随机取5次，每次取一个节点，然后取 pong_received 最小的节点
3.  对最小的节点发送 PING 消息
```
5.  遍历所有节点 server.cluster->nodes
```
1.  统计孤立的master节点个数（有分派slot，无slave节点）。
2.  统计最大的单个master对应的slave节点个数，这一步与上一步执行时机相同，都是在当前节点为slave节点，此次遍历的节点为master。如果达到条件将会执行 4.h.iii 中提到的 slave迁移，这就是为什么只在slave节点执行这个判断的原因。
3.  对于超时未收到节点的pong消息，关闭连接 (now - node->ping\_sent > server.cluster\_node_timeout/2)。后续可能有2种情况，第一，走 4.c.iii，给几次重试连接机会；第二，走 vi，如果重试几次还是不正常，标记为可能失败状态（possible failure ）
4.  对于正常的连接，如果长时间未发送ping消息的节点，则发送（node->ping\_sent == 0 &&(now - node->pong\_received) > server.cluster\_node\_timeout/2）
5.  如果在执行手动故障转移（manual failover），当前节点是master节点，此次遍历的节点是 mf_slave 节点，则发送ping消息
6.  对于超时过长的节点，标记为可能失败状态 
	now - node->ping_sent  > server.cluster_node_timeout
	node->flags |= CLUSTER_NODE_PFAIL
```

6.  如果当前节点是slalve 节点，其对应的 master 从故障中恢复正常，重新设置为master信息，开启复制。
7.  手动故障转移超时间检测，如果超时，则重置相关变量
7.  如果当前节点是salve节点，

```
1.  处理手动故障转移 clusterHandleManualFailover

	如果无手动故障转移(server.cluster->mf_end == 0)，则直接返回。如		果有手动故障转移，这个值是一个结束超时时间，因此在多处都使用这个值来判断是否在执行手动故障转移
如果手动故障转移开始标记已设置，则直接返回。
如果当前节点的 offset 与 master上的 offset 一致，则标记开始故障转移 server.cluster->mf_can_start = 1;（server.cluster->mf_master_offset == replicationGetSlaveOffset()）（offset = server.master->reploff）（offset = server.cached_master->reploff）

2.  处理Slave故障转移 clusterHandleSlaveFailover。这个主题比较长，转移到6
3.  如果有孤立的master节点，slave 个数>=2，当前slave节点属于其中，则执行slave 迁移 clusterHandleSlaveMigration。这个主题同样，转移到7
```

9.  更新集群状态 clusterUpdateState

```
当重启节点后，如果一切状态看上去都正常也不会立即恢复节点状态，留一段时间让其重新配置这个节点，也就是重新与其他节点通讯确认真的可用了  （CLUSTER_WRITABLE_DELAY 2000）
如果要求全部slot覆盖时节点才可用，则检查 slot 是否已经全部分派，并且 slot 对应的节点也需要是可用状态，不能是 CLUSTER_NODE_FAIL（配置项为server.cluster_require_full_coverage）。如果不是全部可用，则标记当前节点状态为不可用（CLUSTER_FAIL）
计算集群节点总数 server.cluster->size（负责slot的Master节点，这里不包括slave节点）与可用节点数（不能是这2种状态 CLUSTER_NODE_FAIL|CLUSTER_NODE_PFAIL）
如果可用节点数 小于总节点数的一半，则认为当前节点与其他节点隔离，属于少数派，标记当前节点状态为不可用（CLUSTER_FAIL）
如果节点从不可用中恢复到正常状态，并且之前是属于少数派，则延时恢复，延时时间为 server.cluster_node_timeout（如不在这个范围，则调整到边界值 CLUSTER_MIN_REJOIN_DELAY <= t <= CLUSTER_MAX_REJOIN_DELAY），这项限制也是为了使其节点持续稳定后在加入集群，以免数据在节点间不停的迁移。
```

## 处理集群消息（包括发送、接收）

1.  截止到目前为止，消息类型总共有10种。

```
#define CLUSTERMSG_TYPE_PING 0          /* Ping */
#define CLUSTERMSG_TYPE_PONG 1          /* Pong (reply to Ping) */
#define CLUSTERMSG_TYPE_MEET 2          /* Meet "let's join" message */
#define CLUSTERMSG_TYPE_FAIL 3          /* Mark node xxx as failing */
#define CLUSTERMSG_TYPE_PUBLISH 4       /* Pub/Sub Publish propagation */
#define CLUSTERMSG_TYPE_FAILOVER_AUTH_REQUEST 5 /* May I failover? */
#define CLUSTERMSG_TYPE_FAILOVER_AUTH_ACK 6     /* Yes, you have my vote */
#define CLUSTERMSG_TYPE_UPDATE 7        /* Another node slots configuration */
#define CLUSTERMSG_TYPE_MFSTART 8       /* Pause clients for manual failover */
#define CLUSTERMSG_TYPE_MODULE 9        /* Module cluster API message. */
#define CLUSTERMSG_TYPE_COUNT 10        /* Total number of message types. */
```
2.  这10种消息中，使用到消息体（clusterMsgData）的又可以分为 PING、FAIL、PUBLISH、UPDATE、MODULE 5种大类，其中MEET/PONG与PING归为同一类，其他消息只使用到了消息头。
3.  消息头的类型为 struct clusterMsg， 消息体的类型为 union clusterMsgData 。 clusterMsgData 中包含不同类型消息的消息数据，clusterMsg 的最后一个字段 data 即是 clusterMsgData 。在源码中称 clusterMsg 为 hdr , clusterMsgData 为 hdr->data ，hdr 也就是header的简写，代表消息头的意思。
4.  只有PING类型（包括PING/MEET/PONG）的消息会携带gossip信息，也就是集群其他节点的信息（ip /port / send\_ping / pong\_received 等），用来传播这些集群节点信息，达到让所有节点都保存了全部节点信息，用于后续的投票选举，故障转移，最终达到高可用。
5.  每个消息都会带有消息头，其中消息头包含：

```
如果当前节点为slave节点，在发送消息时为了更加准确，会使用其对应 master节点的部分信息（slots 槽信息，configEpoch 纪元）
hdr->ver  集群协议版本
hdr->sig[4]  “RCmb” ，标记这个消息是属于redis cluster 消息，其中RCmb是指 Redis Cluster message bus 
hdr->type 消息类型，即上面提到的10种消息中的其中一种
hdr->sender 当前节点的名称 node ID
hdr->myip ，如果有指定 server.cluster_announce_ip 则使用，否则设置为0
hdr->myslots  为 master->slots
hdr->slaveof 如果为salve节点，则为对应master的名称 node ID
hdr->port 如果有设置server.cluster_announce_port，则使用，否则使用 server.port
hdr->cport 如果有设置 server.cluster_announce_bus_port，则使用，否则使用 server.port + 10000
hdr->flags = htons(myself->flags) 当前节点的所有标识
hdr->state = server.cluster->state 集群状态
hdr->currentEpoch = htonu64(server.cluster->currentEpoch)  当前纪元，在发送选举请求时，crruentEpoch 将会在configEpoch的基础上 + 1，标识一个新的纪元开始。纪元也就是周期的意思，也相当于版本号，有变化时递增，反推就是收消息方一旦发现收到的epoch与自己保存的epoch不同，说明发生了变化，进而执行对应的逻辑。也就是通过这种方式来确保集群所有节点间的最终一致性。
hdr->configEpoch = htonu64(master->configEpoch) 节点纪元
hdr->offset 如果是slave节点则为 server.master->reploff，如果是master节点则为 server.master_repl_offset
hdr->mflags  如果是mater节点，并且在手动故障转移，则设置标记 hdr->mflags[0] |= CLUSTERMSG_FLAG0_PAUSED
hdr->totlen 由于部分消息有消息体，并且消息体的长度与其定义的长度可能不同，比如PING类型消息，所以这个消息的总长度将有一个计算的过程。不过当消息中不需要消息体时，这里的totlen将会减去clusterMsgData 的长度，如果需要消息体时，也会减去clusterMsgData，然后再根据不同的消息类型增加上对应消息体的长度。这里消息体使用了union类型，也是为了灵活的控制消息的长度。
以上这些信息都是关于当前节点的信息，而并不是要发送的目标节点的信息，也就是说每个消息中都会携带关于当前节点的信息
```
6.  发送 PING(MEET/PING/PONG)

```
新加入节点时，将发送MEET消息，对方节点回复PONG；建立连接后定期的心跳检测是通过发送PING消息，对方节点回复PONG消息来实现。
计算 freshnodes 个数，即总节点数 - 2 （这2个是指自己与要发送消息的目标节点），也就说，消息中包含的节点数最多也不会超过这个数，否则就是有重复了。
携带的节点分为2种，一种是正常节点，一种是pfail 状态的节点（可能失败的节点，即当前节点没有在超时时间内收到PONG回复）。正常节点数（wanted）的计算方式是总节点数的 1/10，pfail 节点数（pfail_wanted）是全部的pfail节点，这2种节点最后在消息体中是一个列表，每次在添加时检测是否已经存在其列表来保证最终这个列表中的节点是不重复的。wantd 最小值为 3，最大值为 freshnodes
如果是PING类型消息，保存ping消息发送时间，用于验证之后收到的PONG消息是否会超时。（link->node->ping_sent = mstime();）
循环N次，取 1/10 个正常节点，因此每次都会随机在列表中取一个，循环最大次数N = wanted*3
正常节点列表不包括这几种节点：mysql(自己)、CLUSTER_NODE_PFAIL 状态的节点、CLUSTER_NODE_HANDSHAKE 状态的节点、CLUSTER_NODE_NOADDR状态的节点、连接为空且slot数为0的节点（this->link == NULL && this->numslots == 0）
可能失败的节点（pfail）列表不包括这几种节点：CLUSTER_NODE_HANDSHAKE状态的节点、CLUSTER_NODE_NOADDR状态的节点。并且必须有 CLUSTER_NODE_PFAIL 标记。
有2个计算消息总长度的过程，一个是预分配的，一个是实际发送的消息长度。消息头是固定的长度，消息体根据消息类型及携带的集群节点个数不同而不同。预分配是提前根据 wanted+pfail_wanted 乘以单个gossip的长度计算，但是实际可能没有取到这么多节点，所以长度可能不同，所以在实际发送消息时将根据实际的节点数再进行计算一次。
在初始结构中 gossip 数组长度为1（clusterMsgDataGossip gossip[1]） ，所以在上一步计算总长度时，需要把这个长度减掉，然后再加上节点个数乘以gossip占用的长度。这里也有一些技巧，定义为数组长度为1，可以使用它的首地址为指针的特性，再者这个长度在定义时是确定的，后续的计算过程方便运算。
在消息中包括携带的节点个数与消息总长度。
关于为什么选择 1/10 个节点，这个单独另行讨论。
```

7.  发送 FAIL 消息

```
1.  当在A节点的中设置B节点为FAIL状态时，将发送消息给其他所有节点。只有在设置FAIL状态时会发送，如果状态未改变时，不会再次重复发送。
2.  FAIL 消息，在消息体中包含有 FAIL 节点的名称。
```

8.  发送 PUBLISH 消息

```
1.  当客户端发送 PUBLISH 命令时，接收消息的节点要把这个消息发送到其他所有节点（调用函数 clusterBroadcastMessage）。
2.  消息体将会包含这么几个信息：

	uint32_t channel_len
	uint32_t message_len
	unsigned char bulk_data[8]

3.  channel 与 message  的实际内容会拼接在 bulk_data 中。
```

9.  发送 FAILOVER\_AUTH\_REQUEST

```
1.  发送选举请求，请求其他节点选举自己执行故障转移
2.  currentEpoch 将会自增1 
3.  这个请求会发送给所有可用的节点，包括master与slave节点，但是只master会回复，所以参与投票的节点只有master。
4.  这个消息只有消息头，没有对应的消息体
5.  如果在手动故障转移，将携带 dr->mflags[0] |= CLUSTERMSG_FLAG0_FORCEACK
```

10.  发送 FAILOVER\_AUTH\_ACK 消息
```
1.  回复选举请求，同意、或者不同意
2.  这消息只有消息头，没有对应的消息体
```
11.  发送 UPDATE 消息
```
1.  UPDATE 消息，用力发送更新消息。比如：B节点收到A节点发送的PING/PONG时，如果B中保存的slot关系与收到的消息中的slot（A负责的slot）不同，进而将展开不同情况的处理。如果B节点保存的某个slot对应的configEpoch大于消息中携带的A节点的configEpoch，则认为A的slot消息过旧，给A发送UPDATE消息，其中包含对应这个slot的节点信息；如果认为A的slot消息较新，则更新B节点对应的slot信息（通过调用函数clusterUpdateSlotsConfigWith）
2.  消息体格式

	uint64_t configEpoch; /* Config epoch of the specified instance. */
	char nodename[CLUSTER_NAMELEN] /* Name of the slots owner. */
	unsigned char slots[CLUSTER_SLOTS/8]; /* Slots bitmap. 
```
12.  发送 MFSTART 消息
```
1.  MFSTART 即 mamual start ，代表 手动故障转移。
2.  是在执行了命令 CLUSTER FAILOVER 命令，并且不太任何参数的情况下，由当前的slave节点发送给其master节点。
3.  这个消息也是只要消息头，没有对应的消息体。
```
13.  发送 MODULE 消息
	模块集群消息api

14.  接收消息后的处理（这个视角与之前说到的视角不同，这个是接收者的视角，所以其中“当前节点”所指的对象是不同的）

```
1.  这么多种消息类型的接收处理都放到了一个统一的函数中 clusterProcessPacket
2.  这个函数的主要实现流程分为了这么几部分，第一，处理 MEET/PING/PONG 消息，这也是代码量最大的逻辑块，第二，CLUSTERMSG\_TYPE\_FAIL 类型的消息，第三，CLUSTERMSG\_TYPE\_PUBLISH 类型的消息，第四，CLUSTERMSG\_TYPE\_FAILOVER\_AUTH\_REQUEST 类型的消息，第五，CLUSTERMSG\_TYPE\_FAILOVER\_AUTH\_ACK 类型的消息，第六，CLUSTERMSG\_TYPE\_MFSTART 类型的消息，第七，CLUSTERMSG\_TYPE\_UPDATE 类型的消息，第八，CLUSTERMSG\_TYPE\_MODULE 类型的消息。
3.  这里先记录下函数开始通用的一些处理，然后单独分节说明每一部分消息。
4.  把接收到的数据通过强制类型转换，直接转换为clusterMsg类型 ( clusterMsg \*hdr = (clusterMsg\*) link->rcvbuf ) ，这样后续的逻辑就直接操作 hdr指针，非常方便，同时也易于理解。
5.  通过 type < CLUSTERMSG\_TYPE\_COUNT  来验证接收的消息类型是否属于正确的类型，如果是，server.cluster->stats\_bus\_messages_received\[type\]++
6.  消息完整性检测，totlen 小于 16 或者大于实际接收到的buf长度 sdslen(link->rcvbuf) 均认为有问题，直接返回。  
7.  通讯协议版本检测，如果不同，直接返回。不能处理不同版本间的消息。
8.  然后根据不同类型的消息计算期望的消息长度，如果与实际发送的totlen的值不同，则也认为消息有问题，直接返回。
9.  根据 hdr->sender 为发送者的 node ID，在当前节点已知的节点列表（server.cluster->nodes）中查找，如果找到则认为这个节点已经是集群中的已知节点，则信任其发送过来的数据。当然也是允许新加入节点的，也就是这里会找不到。
10.  如果是已知节点，握手已经完成，则：

	判断epoch，如果发送者携带的epoch 大于当前节点的 epoch，则把当前节点的 epoch 值更新为最新的值。currentEpoch 与 configEpoch 都是。
	如果当前节点是slave 节点，正在执行手动故障转移，发送者为对应的master节点，消息mflag包含 CLUSTERMSG_FLAG0_PAUSED 标记，server.cluster->mf_master_offset == 0，这时更新 mf_master_offset 的值为sender->repl_offset 。（在手动故障转移的过程中其中有一个过程是 master 会暂停接收客户端请求，等待正在故障转移的slave节点同步完自己的所有数据，这个变量 mf_master_offset 就是用来记录这个偏移量，在手动故障转移逻辑中会根据这个偏移量与当前实际同步的偏移量server.master-> reploff 比较，来验证是否已经完成数据同步）

11.  如果当前节点 server.cluster\_announce\_ip  未设定，并且 myself->ip 为空时，则通过getsockname函数来获取当前节点的ip，如果获取到的值与myself->ip不同，则更新 myself->ip 为新值。
12.  如果是MEET消息，并且发送者未找到，则创建新节点，并添加到 server.cluster->nodes 列表中。其中flag为CLUSTER\_NODE\_HANDSHAKE，也就是设置为握手阶段。
13.  如果是MEET消息，并且发送者未找到，则执行clusterProcessGossipSection，处理 gossip 部分 。这是由于消息MEET消息的特殊性。（这部分将单独展开）
14.  如果是PING/MEET消息，则回复PONG消息
```

15.  接收 MEET/PING/PONG 消息的处理
```
1.  link->node 是什么？我目前能理解到的是主动建立连接的一方才会正确设置这个值，监听接收消息的一方这个值为NULL。也许是用来区分这2种情况的吧。
2.  如果 link->node 有值（主动建立连接方），则：

	 如果在握手状态（nodeInHandshake(link->node)），并且发送者是已知的节点，先会更新已知节点的信息（如果ip/port 有变化，link 相同认为无变化），然后则删除 link->node 这个节点的所有相关的信息，包括节点自身的信息。（包括slot / importing\_slots\_from/ migrating\_slots\_to/ node->fail_reports 等等）。清理完之后，此函数就返回，不执行后续逻辑。这里面有一个很关键的点，sender 是根据收到的消息头中的hdr->sender（node ID）在 server.cluster->nodes 列表中查找到的节点，而 link->node 是与当前连接关联的节点，可能在大多数情况是相同的，但是在最初节点A向节点B发送MEET消息时，并不知道节点B的node ID 所以会随机生成一个，在A收到B的回复PONG时，B会携带自己真实的node ID，这时这2个值就不同了。如果相同就表明，这个节点B已经在节点A的已知列表，相当于实际上的一个节点，存在了2份，重复了，就执行删除正在链接的节点。这里可能又会有疑问了，已经在A的已知列表，为啥还要再向B发送MEET消息？这个就要说起 CLUSTER MEET命令，带有相同ip /port 的 MEET 命令可以多次执行，但是如果上一个MEET命令已经与对应节点建立连接完成，这个MEET消息就会重复发送，就是这里的情况，如果上一个MEET命令与对应的节点还在握手状态，则会立即返回，忽略这条MEET命令，这种情况MEET消息就不会重复发送。还有一种情况也可能会出现这样的问题，在执行了CLUSTER MEET 命令后，与实际发送MEET消息给对应节点这中间是有时间间隔的，在这个时间窗口，当前节点可能会收到其他节点已经把这个节点携带过来了，这时也就重复了，所以这里的这个排重逻辑还是少不了。
	如果在握手状态，发送者是未知节点，这应该就是正常的收到PONG回复的情况了。重命名节点的名称（node->name 也就是 Node ID ）。移除 CLUSTER\_NODE\_HANDSHAKE 标记。增加 CLUSTER\_NODE\_MASTER 、 CLUSTER\_NODE\_SLAVE 标记。因为不知道是 slave 还是master，所以都加上，后续再移除。
	如果不是握手状态，那么就比较连接的节点名称与消息中包含的节点名称是否相同，如果不同，则断开这个连接，link->node->ip / link->node->port / link->node->cport 设置为 0 值，link->node->flags 增加 CLUSTER\_NODE\_NOADDR 标记。然后函数就立即返回了。

3.  如果发送者是已知节点（sender 有值），同步消息中的 CLUSTER\_NODE\_NOFAILOVER  标记。
4.  如果发送者是已知节点（sender 有值），不是握手状态，并且是PING消息，则 如果有必要的话更新节点信息（ip/ port /c port）
5.  如果 link->node 有值，并且是 PONG消息时，这是一个正常的 ping <-> pong 流程的回复。

	 设置pong接收时间 link->node->pong_received = mstime() ，将会根据这个时间，时间越小，会优先再次发送 ping 消息来检测节点状态。
	 设置ping发送时间 link->node->ping\_sent = 0  , 设置为0 表明之前发送的ping已经收到pong回复，说明节点正常，否则将会根据这个ping\_send 的时间来判断是否超时。
	收到pong回复，说明节点正常。如果之前有标记PFAIL（可能失败），则移除。 link->node->flags &= ~CLUSTER\_NODE\_PFAIL。如果之前有标记FAIL（失败），满足一定条件则移除这个标记，并不总是直接移除，Slave节点与Master节点的处理逻辑不同。

6.  如果是已知节点（sender 有值），接下来将处理 slave -> master 或者 master -> slave 角色转换的情况

	根据 hdr->slaveof 来判断发送者角色是master还是 slave，如果为空，则认为是master节点。如果当前节点已经保存的角色与发送者最新的角色不同，则认为是发生了角色变化。如果同样是slave，但是对应的master节点不同的话也同样需要更新。因此分为了4种情况：a. slave -> master, b. master->slave, c.一直是slave，但是对应的master节点不同，d. 无变化。但是在这里代码结构稍有不同，是按照最新的状态的不同而分开处理。如下：
	 最新是master角色

		slave -> master 需要把原来master的slave列表中删除这个节点，添加 CLUSTER_NODE_MIGRATE_TO 标记
		清除 CLUSTER_NODE_SLAVE 标记
		添加 CLUSTER_NODE_MASTER 标记
		清除 slaveof ，n->slaveof = NULL

	最新是slave角色

		master -> slave 删除 server.cluster->slots 中对应的这个节点。移除CLUSTER_NODE_MASTER  CLUSTER_NODE_MIGRATE_TO 标记。添加 CLUSTER_NODE_SLAVE 标记。
		对应的master节点不同。需要把原来master的slave列表中删除这个节点，然后配置新的主从关系。

	通过上面 2、3 的 CLUSTER\_NODE\_SLAVE  、CLUSTER\_NODE\_MASTER 标记的处理，最后只保留了其中一个标记，也就是要么是slave、要么是master。

7.  更新关于slot的信息

	当然这一步也需要发送者是已知节点，并且是在设置 master / slave 状态之后。这是因为这一步会使用到 master / slave 状态，如果在这之前发送者消息中声称的状态与当前节点已经保存的状态不同，则无法正确处理。
	发送者消息中声称的slot信息与当前节点已经保存的这个发送者负责的slot不是完全相同。可能是发送者消息中声称的更新，也可能是当前节点已知的更新。两种情况分别处理。
	如果发送者是master，则使用其下保存的slot信息，如果是slave则使用其对于master的slot信息，这样为的是取到最新的slot信息。
	如果消息中包含的slot信息与当前保存的slot信息不同，并且这个slot对应的节点版本更大，则更新当前保存的slot信息（clusterUpdateSlotsConfigWith）。这里只考虑发送者是master的情况，那么slave保存的slot 何时更新呢？？？
	如果与上面的情况相反，则发送消息给发送者（UPDATE类型的消息）
	clusterUpdateSlotsConfigWith  函数执行逻辑在其他小节中有提到，这里不再重复。

8.  解决epoch相同的情况

	只有发送者与当前节点都为 master ，并且configEpoch相同时才执行此项处理（senderConfigEpoch == myself->configEpoch）
	 比较节点名称，节点名称比较大的节点不执行任何处理。因此只有在当前节点的名称小于发送者的名称时才会更新server.cluster->currentEpoch++ 与 myself->configEpoch = server.cluster->currentEpoch

9.  如果发送者已知，则执行clusterProcessGossipSection，处理 gossip部分。（这部分将单独展开）
```
16.  接收 FAIL 消息的处理
```
1.  发送者未知时，直接返回。
2.  FAIL 消息中会携带一个 FAIL 状态的节点的节点名称，是在消息体中发送过来的。如果这个FAIL节点不是已知节点，也将直接返回。
3.  如果FAIL节点不是自己，并且不是CLUSTER\_NODE\_FAIL状态，则：

	设置这个节点为失败状态（failing->flags |= CLUSTER_NODE_FAIL）
	设置这个节点的失败时间（failing->fail_time = mstime()）
	删除PFAIL 状态，因为FAIL 是真正代表失败，（failing->flags &= ~CLUSTER_NODE_PFAIL）
```
17.  接收 PUBLISH 消息的处理
```
1.  接收到PUBLISH 消息后，解析 channel  、 message 字符串，然后使用与普通的pub/sub方式相同的处理（调用函数 pubsubPublishMessage），向订阅消息的客户端发送这个最新的消息。
2.  借此将展开下 pubsubPublishMessage 函数的实现细节：

	  有2个订阅列表，第一个是字典型的 server.pubsub\_channels，key 是 channel 名称，values 是订阅这个channel 的客户端列表。第二个是列表型的 server.pubsub\_patterns , 每一个条目中包含订阅的channel模式及客户端信息。
	 对于 server.pubsub_channels ，先根据 key 找到 对于的 客户端列表，然后循环发送消息给客户端。
	 对于 server.pubsub_patterns，只能依次循环遍历，如果模式匹配将发送消息给对应的客户端。
	 最后返回接收消息的客户端个数。
```
18.  接收 FAILOVER\_AUTH\_REQUEST 消息的处理
```
1.  如果发送者未知，直接返回（即sender为NULL时）
2.  如果当前节点是slave，或者不负责任何slot ，则不参与投票，直接返回。
3.  如果发送者当前的Epoch 小于 当前的 Epoch 则认为消息不是最新的，直接拒绝，返回。
4.  如果最后投票的Epoch 等于当前的Epoch，则认为这个Epoch（纪元、周期）已经投过票，不再重复投票，直接返回。
5.  提出故障转移的节点必须是slave节点，并且当前节点认为其对应的master节点已经不可用 ，否则也将直接返回。还有一种是手动故障转移，这时对应的master节点可能还是可用的，所以会通过消息中的mflag标记来验证是否是这种情况（force\_ack = request->mflags\[0\] & CLUSTERMSG\_FLAG0_FORCEACK），这种情况下也将接着下面的流程，不会直接返回。
6.  在2个集群超时时间范围内，不重复投票。否则直接返回。
7.  发送者负责的slot 要比当前节点保存的这些slot 对应的 configEpoch 要大，否则认为消息不是最新的，直接返回。
8.  然后设置最后投票的Epoch （server.cluster->lastVoteEpoch = server.cluster->currentEpoch）
9.  设置投票时间 node->slaveof->voted_time = mstime()
10.  最后就是发送 FAILOVER\_AUTH\_ACK 类型的消息了。发送ACK类型消息之前已经有介绍，这里不再重复。
```
19.  接收 FAILOVER\_AUTH\_ACK 消息的处理
```
	依然验证发送者是否已知，如果sender未知（sender = NULL ）则直接返回
	接着验证发送者是否是master，并且有负责slot（sender->numslots > 0），并且当前的Epoch 大于等于auth_epoch（senderCurrentEpoch >= server.cluster->failover_auth_epoch），如果同时符合这3个条件，则增加票数（server.cluster->failover_auth_count++;）
	总结，slave 不参与投票，只有负责的slot数大于0的master才参与投票。
```
20.  接收 MFSTART 消息的处理
```
1.  MFSTART 消息只有自己的slave才发送消息给其对应的master，所有只有master才会接受到这类消息。
2.  如果发送者不是已知节点（sender = NULL），或者发送者不是自己的slave节点，直接返回。
3.  重置MF相关变量
4.  设置MF 结束时间 （server.cluster->mf_end = mstime() + CLUSTER_MF_TIMEOUT）
5.  设置MF Slave（server.cluster->mf_slave = sender）
6.  暂停客户端请求 ，并设置暂停时间（server.clients_paused = 1）
```
21.  接收 UPDATE 消息的处理
```
1.  UPDATE消息除了统一消息头，还包含UPDATE消息体，其中包含一个update节点的概要信息（configEpoch 纪元、nodename 节点名称、slots 节点负责的槽信息），消息体中携带的这个节点与发送者是不同的节点，要注意区分。发送时机在之前有提到，这里不再重复了。
2.  涉及到当前节点更新操作，所以发送者必须要是已知节点（sender不为空，否则直接返回，不执行后续逻辑）
3.  根据消息体中携带的nodename 在当前server.cluster->nodes 下查找，如果找不到则认为update节点还是未知节点，直接返回，不执行后续逻辑
4.  再验证这个update节点的epoch，消息体中携带的configEpoch 与当前已经保存的这个update节点的confgEpoch比较，如果当前保存的configEpoch较大，则认为发送的消息中的update节点已经不是最新的，不处理后续逻辑，直接返回。
5.  上面的3步检查完之后，我们认为当前节点的信息不是最新的，如果需要就更新。
6.  消息体中的发送的update节点与其对应的slot信息，说明其是master节点。所以如果当前节点保存的是slave状态，则重新设置为master状态
7.  更新slot相关信息（clusterUpdateSlotsConfigWith），在这个函数内部 sender 变量就是指 update节点，这个函数有2处被调用，其他一处是发送update消息的相反情况被调用，上面有提到过，在这种情况下sender变量就是消息发送者节点。下面将简单描述下这个过程：

	 其实涉及到更新slot的情况，就只有2种可能：第一，执行过故障转移，有slave提升到master，slot信息势必要变更，第二，执行过集群slot迁移动作，即 CLUSTER SETSLOT <slot> (IMPORTING | MIGRATION <node ID>) 命令。
	 获取到当前的master节点，如果当前是slave节点，则取其对应的master节点（curmaster = nodeIsMaster(myself) ? myself : myself->slaveof） 
	关于自己负责的slot信息，只有自己有最终发言权，所以对于这个update节点等于myself节点的情况，统统不理会，也就是说我负责哪些slot 自己知道，不需要别人传递给我。
	 然后就是循环所有的update节点负责的slot，如果slot对应的节点是update节点，则说明没有变化，继续下一个slot；如果这个slot正在从别的节点导入，也将继续下一个slot。
	 剩下的情况就是 slot 对应的节点不同的情况了。如果当前节点保存的这个 slot为NULL，或者当前节点保存的这个slot 对应的节点的纪元（configEpoch）比较早，即小于这个update节点的纪元，则更新，否则不做任何处理。更新操作包含：删除当前 slot 信息，把update节点设置为当前slot 对应的节点。
	 在上一步的条件之下，我们认为当前节点的slot信息不是最新的，所以对应有别的逻辑处理。第一，当前slot对应的节点是 myself，也就是自己，并且slot下还有key存在，则认为这个slot是 dirty_slot （有脏数据存在） ，并且清理其对应的key数据。第二，当前slot对应的节点是 curmaster（在本小节2中有提到），并且 curmaster负责的slot数为0时，修改当前节点的master为update节点。
	 6中的第二点，就会处理故障转移中没有完成的步骤，比如，原来的master（A节点）故障，这个master节点下可能有几个slave（B节点、C节点、D节点），但是由其下的slave（B节点）晋升为了新的master节点，新的master（B节点）将拥有更大的纪元（configEpoch），当B节点发送PING/PONG 给 A/C/D节点时，接收到B节点的消息是，这些节点会执行此函数，进而执行此处逻辑，把A/C/D节点都设置为B节点的Slave。如果原来的master（A节点）一直没有恢复，也就不会处理它，但是C/D节点可能是正常的，然后通过 5 中把关于A节点的相关slot信息删掉，这时 curmaster 负责的slot数就为0，这样就顺利的执行了这个过程。这时完整的故障转移将才算是真正完成。
```
22.  接收 MODULE 消息的处理

##  处理slave故障转移 clusterHandleSlaveFailover

1.  故障转移是由slave接管其已经产生故障的master节点，这时在这个master下可能有多个可用的slave节点，因此就需要选出其中一个slave来执行这个操作，这个选择的过程就是选举的过程，也就是通过投票来选出。
2.  需要赢得选举，至少需要一半以上的节点同意（负责slot的Master节点，这里不包括slave节点），即 needed_quorum = (server.cluster->size / 2) + 1
3.  在发送选举请求，等待投票结果时，有2个时间，超时时间 auth\_timeout = server.cluster\_node\_timeout\*2 ，超时重试时间 auth\_retry\_time = auth\_timeout \* 2 ，也就是说在一次选举超时后，不会立即开始下一次，中间会再间隔一个超时时间。
4.  对于master没有故障，或者次slave异常的节点将不执行这个操作，认为没有理由执行failover。在手动故障模式下，即使master没有故障也会执行故障转移，相当于把管控权交给了集群管理员，方便在特殊场景下使用。
5.  如果有设置 server.cluster\_slave\_validity_factor，则对最后同步时间验证，如果太久，则也认为 不能执行failover 。手动故障转移则没有这个限制。默认值是 10.
6.  当一个master节点故障，很可能在短时间其对应的好多slave都发起选举请求，因此在初始化一个选举请求发起时间，会先给每个slave节点算出一个不同的开始时间。大致算法是，按照复制偏移量reploffset 排名，然后乘以 failover\_auth\_time，再加一个 500ms的随机时间，最后加一个固定的 500ms。最终结果，与master数据最接近的节点将最先开始发起选举请求，相同的偏移量的情况下，根据随机数的情况，避免了同一时间有多个slave节点同时发起。手动故障转移没有这个限制，会立即开始。
7.  如果上诉条件满足，将开始一次选举请求，在一次选举结束前，同一个节点不会发出第二次，如果时间太长，到达auth_timeout ，则返回，等待重试，不执行后续逻辑。
8.  如果 server.cluster->failover\_auth\_sent == 0，也代表没有在执行的选举请求，则发送。

```
server.cluster->currentEpoch++;
server.cluster->failover_auth_epoch = server.cluster->currentEpoch
clusterRequestFailoverAuth()
server.cluster->failover_auth_sent = 1
```
9.  在上一步发送完选举请求后，响应结果不会同步返回，所以这次函数调用就返回了。
10.  到达下一个时间周期，将会验证所得票数是否大于等于需要的票数，如果满足条件则赢得选举，将执行从slave到master角色的切换。如果选票不足，则继续等待（也许别的节点的结果还没有发送回来），直到到达超时时间 auth_timeout。
11.  发送选举请求的详细过程将在5.i中展开，发送选举请求即发送 FAILOVER\_AUTH\_REQUEST 类型的消息，消息接收方接着会发送 CLUSTERMSG\_TYPE\_FAILOVER\_AUTH\_ACK 类型的消息进行回复。等这些参与投票的大多数节点进行了回复之后，就可以执行上面的 j 步骤，计算所支持票数够不够。
12.  slave 到 master 角色切换过程有这么几步：
```
1.  改变角色标记，也就是说从 CLUSTER\_NODE\_SLAVE  到 CLUSTER\_NODE\_MASTER。删除原来master节点下slaves 列表中的当前节点，因为当前节点要变更为master了。
2.  取消与原来master的复制，重置及释放相关资源。
	重置server.replid , 用于 PSYNC  ???
	关闭原来的复制连接，并且设置复制状态为关闭 server.repl_state = REPL_STATE_NONE;
	关闭与slave节点的连接， server.slaves  。 ???
	server.slaveseldb = -1;  防止在master切换后进行全量同步，而是按照预期使用部分同步 ???
	记录无slave的时间 server.repl_no_slaves_since = server.unixtime;（由于一旦slave提升为master，在很短时间是没有对应的slave，用于统计在复制积压时间？？？）
3.  slot 相关的切换，在原来的master 删除、在新的节点增加
4.  更新集群状态，保存配置，并且强制保存到磁盘 fsync
5.  发送PONG消息给所有节点，广播最新状态
6.  重置手动故障转移（manual failover） 相关变量，清除状态
```
7.  处理slave迁移（migration）
```
1.  只有在slave节点执行
2.  不正常的集群状态下，这步将不会执行 （server.cluster->state != CLUSTER_OK），直接返回。
3.  没有对应的master节点时，这步也将不会执行，直接返回。
4.  计算对应的master节点下可用slave节点个数 okslaves。（可用代表不是这2中状态 CLUSTER\_NODE\_FAIL  CLUSTER\_NODE\_PFAIL）
5.  如果okslaves <= server.cluster\_migration\_barrier 时，直接返回。迁移界限 cluster\_migration\_barrier 默认值为1
6.  遍历所有的节点找到孤立的master节点，与候选（candidate）节点

	一个有较多的slave节点的master节点要把超过一定界限的slave节点分派给一些孤立master节点。这时这个master下的多个slave节点可能同时执行这个操作，导致最终自己成了孤立节点。所以会使用一个规则来避免这种情况发生，规则就是这几个slave节点中node ID 最小的那个，成为 candidate j节点。
	 如果有多个孤立master节点，按顺序优先取到时则把他作为目标（target）节点，也就是候选节点接下来要跟随的master节点。
	 如果是孤立master节点就会标记孤立时间 node->orphaned\_time = mstime() ，如果不是将置 orphaned\_time = 0
	 如果能找到 okslaves 个数与之前统计的max_slaves 相同的master节点，则取其slaves 列表中node ID最小的节点作为 candidate 节点。否则，myself节点兜底，也就是当前节点作为 candidate 节点。

7.  如果找到 target 节点，candidate 节点是当前节点，并且target节点的孤立时长超过 5s , 则重新设置当前节点的master为target，即完成了一次slave迁移。
```
8.  处理 gossip 部分
```
1.  在接收到 PING/MEET/PONG 消息时，有2种情况会处理，第一，是MEET消息，发送者未知节点，第二，是PING/MEET/PONG 消息，但是发送者是已知节点。
2.  gossip 中包含有N个节点的部分信息，然后依次遍历处理，这节点我们就以代号G来称呼。
3.  如果G节点不是已知节点时，给这个G节点发送握手消息（HANDSHAKE类型），如果存在继续下面的步骤
4.  如果发送者是已知节点，并且是master，G节点不是当前节点，则：

	如果是gossip 消息中标记的是CLUSTER_NODE_FAIL|CLUSTER_NODE_PFAIL 这2个中的任一状态，那么：
		增加失败汇报记录（clusterNodeAddFailureReport）。
		如果需要则标记G节点为失败节点（markNodeAsFailingIfNeeded）。
	否则，将删除失败汇报记录（clusterNodeDelFailureReport）
5.  如果gossip 消息中的标记并没有 CLUSTER_NODE_FAIL|CLUSTER_NODE_PFAIL 中其中任一，当前节点也按时收到了G节点的pong回复，并且之前没有节点汇报关于G节点的FAIL 、PFAIL 状态，那么：
	 如果gossip 中包含的pongtime 大于 当前节点保存的关于G节点的pong回复时，设置G节点的回复时间为gossip中的pongtime。（也许这是认为既然节点是可用的，就同步最后可用时间，这个在发送PING消息时会有用到，pong_received 越小的节点将优先发送ping消息）

6.  如果当前节点认为是FAIL 、PFAIL ，但是gossip消息中并没有包含FAIL PFAIL 状态，当前节点保存的G节点的ip /port 与 gossip 消息中的不是完全相同时，将断开当前节点与 G节点的连接，并且重新设置G节点的ip/port 为 gossip消息中的 ip/port，同时也取消 CLUSTER\_NODE\_NOADDR 标记 。
7.  在b中发送握手消息时，也会有一些额外的条件，发送者需要时已知节点，gossip中有关于G节点的ip/port信息，G节点不在黑名单中。
8.  clusterNodeAddFailureReport 函数内部实现：

	 在节点列表中的每个节点下都有一个 fail_reports  ，记录哪些节点认为这个节点失败。
	 遍历 fail_reports 列表，如果上报节点已经存在，则重新设置上报时间为当前节点。
	 如果不存在时，添加上报节点与上报时间到 fail_reports 列表中。
	 上面提到的删除失败上报记录与这个函数逻辑正好相反，将不再展开。

9.  markNodeAsFailingIfNeeded 函数内部实现：

	 计算需要的票数 （int needed_quorum = (server.cluster->size / 2) + 1）
	 如果当前节点还没有把G节点标记PFAIL 状态，则直接返回。（说明当前节点还可以连接G节点，不认为是G是失败节点）
	 如果当前节点已经把G节点已经标记为了 FAIL 状态，也将直接返回，认为这个过程已经处理过了，不重复处理。
	 计算对节点G的失败上报次数 failures ，也就是计算 fail_reports 列表的长度。
	 如果当前节点是master，则增加一个失败票数 （failures++）
	如果失败票数 小于 需要的票数，则直接返回。（failures < needed_quorum）
	 到此处时，说明节点是失败节点了，票数也通过，当前节点连接也超时，那么设置这个节点的失败状态：

		node->flags &= ~CLUSTER_NODE_PFAIL
		node->flags |= CLUSTER_NODE_FAIL
		node->fail_time = mstime()

	 如果当前节点是master节点，则发送FAIL类型消息（包含这个失败节点的信息）给其他所有节点。

  
```
  
