---
title: ElasticSearch:master,data,client三类节点区别及节点分配简单例举
id: 1541
date: 2024-10-31 22:02:00
author: daichangya
permalink: /archives/ElasticSearch-master-data-client-san/
tags:
- elasticsearch
---



## 简述

*   默认情况下，ES集群节点都是混合节点，即在`elasticsearch.yml`中默认`node.master: true`和`node.data: true`。
*   当ES集群规模达到一定程度以后，就需要注意对集群节点进行角色划分。
*   ES集群节点可以划分为三种：主节点、数据节点和客户端节点。
*   这是一种`分而治之`的思想，也是一种`术业专攻`的体现。

## 三类节点说明

*   **`master - 主节点`**：
    *   `elasticsearch.yml` :
        
        ```yml
        node.master: true
        node.data: false
        
        ```
        
    *   主要功能：维护元数据，管理集群节点状态；不负责数据写入和查询。
    *   配置要点：内存可以相对小一些，但是机器一定要稳定，最好是独占的机器。
*   **`data - 数据节点`**：
    *   `elasticsearch.yml` :
        
        ```yml
        node.master: false
        node.data: true
        
        ```
        
    *   主要功能：负责数据的写入与查询，压力大。
    *   配置要点：大内存，最好是独占的机器。
*   **`client - 客户端节点`**：
    *   `elasticsearch.yml` :
        
        ```yml
        node.master: false
        node.data: false
        
        ```
        
    *   主要功能：负责任务分发和结果汇聚，分担数据节点压力。
    *   配置要点：大内存，最好是独占的机器
*   **`mixed- 混合节点（不建议）`**：
    *   `elasticsearch.yml` :
        
        ```yml
        node.master: true
        node.data: true
        
        ```
        
    *   主要功能：综合上述三个节点的功能。
    *   配置要点：大内存，最好是独占的机器。
    *   `特别说明：不建议这种配置，节点容易挂掉`。

## 其他说明

*   虽然上面章节中，未对单个服务器的磁盘大小进行要求，但是整体ES集群的总磁盘大小要保证足够。

## 简单举例

假定共计`20`台机器，则可以按照如下配置：

| 节点类型 | 机器数量 | 内存大小 | 其他 |
| :-: | :-: | :-: | :-: |
| master | 3 | 16GB | 机器必须稳定 |
| data | 12 | 31GB | 无 |
| client | 5 | 31GB | 无 |

以上，只是简单的举例，可根据实际情况调节。