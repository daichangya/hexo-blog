---
title: 事务隔离性与隔离级别
id: 1568
date: 2024-10-31 22:02:01
author: daichangya
permalink: /archives/shi-wu-ge-li-xing-yu-ge-li-ji-bie/
tags:
- mysql
---


## 前言

我们在上一章节中介绍过数据库的[带你了解数据库中事务的ACID特性](https://mp.weixin.qq.com/s?__biz=MzIwMTg3NzYyOA==&mid=2247483722&idx=1&sn=e8bc8bd82c559e0cfe7f35cf46100af3&chksm=96e67059a191f94fe8948e5b5e4ef177b77fa7707d86d945b153f67e7f2e76b83ed0c768ef27&token=1701970188&lang=zh_CN#rd) 的相关用法。本章节主要来介绍下数据库中一个非常重要的知识点`事务的隔离级别`。如有错误还请大家及时指出~

问题：

*   事务的隔离级别有哪些？
*   如果并发事务没有进行隔离，会出现什么问题？

> 以下都是采用mysql数据库

在多个事务并发做数据库操作的时候，如果没有有效的避免机制，就会出现种种问题。大体上有以下问题：

## 一、引发的问题

在并发事务没有进行隔离的情况下，会发生如下问题。

### 问题一：脏读

`脏读`指一个事务读取了另外一个事务未提交的数据。

`具体看后文案例介绍`

### 问题二：不可重复读

`不可重复读`指在一个事务内读取表中的某一行数据，多次读取结果不同。 不可重复读和脏读的区别是，脏读是读取前一事务未提交的脏数据，不可重复读是重新读取了前一事务已提交的数据。

`具体看后文案例介绍`

### 问题三：幻读(虚读)

`幻读(虚读)`指在一个事务内读取到了别的事务插入的数据，导致前后读取不一致。

`具体看后文案例介绍`

## 二、概念

### 2.1 事务的隔离级别分为：

*   Read uncommitted(读未提交)
*   Read Committed(读已提交)
*   Repeatable Reads(可重复读)
*   Serializable(串行化)

#### Read uncommitted

`读未提交`：隔离级别最低的一种事务级别。在这种隔离级别下，会引发脏读、不可重复读和幻读。

#### Read Committed

`读已提交`读到的都是别人提交后的值。这种隔离级别下，会引发不可重复读和幻读，但避免了脏读。

#### Repeatable Reads

`可重复读`这种隔离级别下，会引发幻读，但避免了脏读、不可重复读。

#### Serializable

`串行化`是最严格的隔离级别。在Serializable隔离级别下，所有事务按照次序依次执行。脏读、不可重复读、幻读都不会出现。

![隔离级别](https://user-gold-cdn.xitu.io/2019/4/11/16a0d183bbd062be?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

## 三、操作

### 3.1 查看事务隔离级别

`SHOW VARIABLES LIKE 'tx_isolation';`

查看全局的事务隔离级别

`SHOW GLOBAL VARIABLES LIKE 'tx_isolation';`

使用系统变量查询

`SELECT @@global.tx_isolation;` `SELECT @@session.tx_isolation;` `SELECT @@tx_isolation;`

### 3.2 设置MysQL的事务隔离级别

#### 语法

```
SET [GLOBAL | SESSION] TRANSACTION ISOLATION LEVEL
  {
       REPEATABLE READ
     | READ COMMITTED
     | READ UNCOMMITTED
     | SERIALIZABLE
   }
复制代码
```

`GLOBAL`：设置全局的事务隔离级别 `SESSION`：设置当前session的事务隔离级别，如果语句没有指定GLOBAL或SESSION，默认值为SESSION

#### 使用系统变量设置事务隔离级别

`SET GLOBAL tx_isolation='REPEATABLE-READ';` `SET SESSION tx_isolation='SERIALIZABLE';`

## 四、案例分析

下面实际操作中使用到的一些并发控制语句，可看上面的**操作**介绍

作为演示：product表

| productId | productName | productPrice | productCount |
| --- | --- | --- | --- |
| 1 | xiaomi | 1999 | 100 |

带着上面的我们来看一下，事务在没有隔离性的情况下，会引发哪些问题？

同时打开两个窗口模拟2个用户并发访问数据库

### 4.1 事务隔离级别设置为read uncommitted

查询事务隔离级别

```
SELECT @@tx_isolation;
复制代码
```

设置隔离级别为**未提交读**：

```
SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
复制代码
```

> 注意：需要同时修改两个窗口的事务隔离级别

以下我们以两位用户抢小米手机为例

| 时间轴 | 事务A | 事务B |
| --- | --- | --- |
| T1 | start transaction； |  |
| T2 | select p.productName,p.productCount from product p where p.productId=1;(productCount =100) |  |
| T3 |  | start transaction； |
| T4 |  | select p.productName,p.productCount from product p where p.productId=1;(productCount =100) |
| T5 |  | update product set productCount = 99 where productId = 1; |
| T6 | select p.productName,p.productCount from product p where p.productId=1;(productCount =99) |  |
| T7 |  | ROLLBACK; |
| T8 | select p.productName,p.productCount from product p where p.productId=1;(productCount =100) |  |

* * *

T1—— A用户开启事务，start transaction； T2—— A用户查询当前小米手机剩余数量，select p.productName,p.productCount from product p where p.productId=1;此时数量显示为100。 T3——B用户开启事务，start transaction； T4——B用户查询当前小米手机剩余数量，select p.productName,p.productCount from product p where p.productId=1;此时数量显示为100。 T5—— B用户购买了一台小米手机，update product set productCount = 99 where productId = 1; 此时只修改数据并未提交事务。 T6—— A用户刷新页面，select p.productName,p.productCount from product p where p.productId=1;此时数量显示为99。 T7—— B用户购买失败，回滚事务。 T8—— A用户查询当前小米手机剩余数量，select p.productName,p.productCount from product p where p.productId=1;此时数量显示为100。

* * *

#### 小结：

事务A读取了未提交的数据，事务B的回滚，导致了事务A的数据不一致，导致了事务A的`脏读` ！

### 4.2 事务隔离级别设置为Read Committed

查询事务隔离级别

```
SELECT @@tx_isolation;
复制代码
```

更改数据库隔离级别，设置隔离级别为**提交读**：

```
SET SESSION  TRANSACTION ISOLATION LEVEL READ COMMITTED;
复制代码
```

> 注意：需要同时修改两个窗口的事务隔离级别

| 时间轴 | 事务A | 事务B |
| --- | --- | --- |
| T1 | start transaction； |  |
| T2 | select p.productName,p.productCount from product p where p.productId=1;(productCount =100) |  |
| T3 |  | start transaction； |
| T4 |  | select p.productName,p.productCount from product p where p.productId=1;(productCount =100) |
| T5 |  | update product set productCount = 99 where productId = 1; |
| T7 | select p.productName,p.productCount from product p where p.productId=1;(productCount =100) |  |
| T6 |  | commit; |
| T8 | select p.productName,p.productCount from product p where p.productId=1;(productCount =99) |  |

* * *

这里就不再对流程做过多赘述。

##### 小结：

可以看到避免了`脏读`现象，但是却出现了，一个事务还没有结束，就发生了不可重复读问题，即事务A来说 productCount从 100->100->99。但这个过程中事务并未提交结束。

### 4.3 事务隔离级别设置为Repeatable Read（mysql默认级别）

查询事务隔离级别

```
SELECT @@tx_isolation;
复制代码
```

更改数据库隔离级别，设置隔离级别为**可重复读**：

```
SET SESSION  TRANSACTION ISOLATION LEVEL REPEATABLE READ;
复制代码
```

> 注意：需要同时修改两个窗口的事务隔离级别

| 时间轴 | 事务A | 事务B |
| --- | --- | --- |
| T1 | start transaction； |  |
| T2 | select p.productName,p.productCount from product p where p.productId=1;(productCount =100) |  |
| T3 |  | start transaction； |
| T4 |  | select p.productName,p.productCount from product p where p.productId=1;(productCount =100) |
| T5 |  | update product set productCount = 99 where productId = 1; |
| T7 | select p.productName,p.productCount from product p where p.productId=1;(productCount =100) |  |
| T6 |  | commit; |
| T8 | select p.productName,p.productCount from product p where p.productId=1;(productCount =100) |  |

* * *

这里就不再对流程做过多赘述。

##### 小结：

可以看到`可重复读`隔离级别避免了`脏读`，`不可重复读`的问题，但是出现了`幻读`现象。事务A查询到的小米数量等于100，但是事务B修改了数量为99，但是事务A读取到的值还是100。当事务A去减1等于99时，是错误的，此时应该是99-1=98才对。接下来我们再提高一个事务隔离级别。

### 4.4 事务隔离级别设置为Serializable

查询事务隔离级别

```
SELECT @@tx_isolation;
复制代码
```

更改数据库隔离级别，设置隔离级别为**串行化**：

```
SET SESSION  TRANSACTION ISOLATION LEVEL REPEATABLE READ;
复制代码
```

| 时间轴 | 事务A | 事务B |
| --- | --- | --- |
| \-\-\- | \-\-\- | \-\-\- |
| T1 | start transaction； |  |
| T2 |  | start transaction； |
| T2 | select p.productName,p.productCount from product p where p.productId=1;(productCount =100); |  |
| T4 |  | update product set productCount = 99 where productId = 1;（等待中..） |

* * *

这里就不再对流程做过多赘述。

##### 小结：

在我们Serializable隔离级别中，我们可以看到事务B去做修改动作时卡主了，不能向下执行。这是因为：给事务A的select操作上了锁，所以事务B去修改值的话，就会被卡主。只有当事务A操作执行完毕，才会执行事务B的操作。这样就避免了上述三个问题了。

## 问题本身

*   回到问题的本身，其实我们并不需要将事务提到这么高。
    
*   问题的本身就是，当我们读完了的时候，就要在上面加锁。我们不希望别人能够去读它。因为别人读到了count,就会修改count的值，并写进去。所以我们在select 操作的时候，加上for update。这时候就会把这行操作给锁掉了。那么另外一个人也进行相同的操作，也表示select 出来的count需要进行update，需要锁住。
    

```
select p.productName,p.productCount from product p where p.productId=1 for update;
复制代码
```