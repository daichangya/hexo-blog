---
title: Redis 主从在线切换
id: 1507
date: 2024-10-31 22:01:59
author: daichangya
permalink: /archives/redis%E4%B8%BB%E4%BB%8E%E5%9C%A8%E7%BA%BF%E5%88%87%E6%8D%A2/
categories:
 - redis
---

Redis 主从在线切换记录

## 背景

Redis master 所在实例主机需要下线维护. 如何切换主从对线上影响最小. 当前架构如下图

![切换前](https://user-gold-cdn.xitu.io/2020/3/6/170adec248f4ffb3?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

## 技术方案

### 方案1

引入 redis sentinel.

#### 步骤:

1.  部署redis sentinel
2.  修改业务配置, 修改业务代码.
3.  kill master.
4.  check
5.  建立新主从逻辑

#### 优点:

1.  切换简单, kill 主库即可, sentinel 可自动提升 slave -> master.

#### 缺点:

1.  需要部署 redis sentinel, 新的中间件.
2.  需要改动业务代码.

### 方案2

直接切换

#### 步骤:

1.  使从库可写, `redis-cli -h redis-slave -p 6379 CONFIG set slave-read-only no`
2.  修改业务侧配置, redis 地址指向可写的 slave 实例, 重启业务应用
3.  确保主从同步完成, 停止主从同步. `redis-cli -h redis-slave -p 6379 slaveof no one`
4.  建立新主从逻辑.

#### 优点:

1.  符合直觉
2.  没有代码改动

#### 缺点:

1.  如果切换过程中有问题, 需要及时回滚配置和业务项目发布. 耗时较长, 会导致数据丢失.

### 方案3

引入4层代理, haproxy

#### 步骤:

1.  部署 haproxy, 作为现 master 的代理.
2.  修改业务侧配置, redis 地址指向 haproxy 代理地址, 重启业务应用.
3.  使从库可写
4.  修改 haproxy 配置, 指向可写的从库, 并 reload 配置.
5.  确保主从同步完成, 停止主从同步.
6.  建立新主从逻辑.

#### 优点

1.  引入中间层haproxy, 因为 haproxy 支持动态reload配置, 并保证优雅关闭之前的连接, 业务侧可无感知 redis 主从切换.
2.  主从切换时间短

#### 缺点

1.  引入了新的中间件

## 确定方案

稳妥起见, 使用方案3.

## 实施

1.  引入 haproxy 后架构
    
![image.png](https://images.jsdiff.com/image_1604061043091.png)
    
2.  执行主从切换
    

```

export redis-slave=REDIS_SLAVE_IP
export redis-master=REDIS_MASTER_IP

# 从库可写
redis-cli -h redis-slave -p 6379 CONFIG set slave-read-only no

# 修改 haproxy 配置
sed -i 's/redis-master/redis-slave/g' haproxy.cfg

# reload haproxy
haproxy -f haproxy.cfg -p /tmp/haproxy.pid -sf `cat /tmp/haproxy.pid`

# 确定主从同步结束
redis-cli -h redis-slave -p 6379 info | grep master_sync_in_progress
# 值需为0

# 停止主从同步
redis-cli -h redis-slave -p 6379 slaveof no one

# 建立新主从
redis-cli -h redis-master -p 6379 slaveof redis-slave 6379

# 确定新主从同步结束
redis-cli -h redis-master -p 6379 info | grep master_sync_in_progress
# 值需为0

# 结束
复制代码
```

3.  切换后架构
    
![image.png](https://images.jsdiff.com/image_1604061094607.png)

## 小结

简单记录了 Redis 主从切换的取舍和操作.