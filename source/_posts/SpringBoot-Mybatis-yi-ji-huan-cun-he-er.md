---
title: SpringBoot+Mybatis一级缓存和二级缓存详解
id: 1573
date: 2024-10-31 22:02:02
author: daichangya
permalink: /archives/SpringBoot-Mybatis-yi-ji-huan-cun-he-er/
tags:
- mybatis
---

本文主要介绍在SpringBoot项目中如何使用Mybatis的一级、二级缓存,为了演示方便，本文的数据库采用H2内存数据库，数据库连接池默认使用SpringBoot2.X自带的hikariCP。  
正确的使用Mybatis缓存可以有效减少多余的数据库查询操作，节约IO。  
接下来我们从实践出发，看一看mybatis的一级，二级缓存如何使用，相关代码请查阅：[https://github.com/zhengxl5566/springboot-demo.git](https://github.com/zhengxl5566/springboot-demo.git)

## 1、概念介绍

*   什么是一级缓存  
    在日常开发过程中，经常会有相同的sql执行多次查询的情况，mybatis提供了一级缓存来优化这些查询，避免多次请求数据库。  
    一级缓存在mybatis中默认是开启的并且是session级别，它的作用域为一次sqlSession会话。
*   什么是二级缓存  
    相对于一级缓存，二级缓存的作用域更广泛，它不止局限于一个sqlSession，可以在多个sqlSession之间共享，事实上，它的作用域是namespace。  
    mybatis的二级缓存默认也是开启的，但由于他的作用域是namespace，所以还需要在mapper.xml中开启才能生效
*   缓存的优先级  
    通过mybatis发起的查询，作用顺序为：二级缓存->一级缓存->数据库 ，其中任何一个环节查到不为空的数据，都将直接返回结果
*   缓存失效  
    当在一个缓存作用域中发生了update、insert、delete 动作后，将会触发缓存失效，下一次查询将命中数据库，从而保证不会查到脏数据。

## 2、代码演示

### 一级缓存

默认情况下，mybatis开启并使用了一级缓存。  
单元测试用例：

```
    /**
     * 开启事务，测试一级缓存效果
     * 缓存命中顺序：二级缓存---> 一级缓存---> 数据库
     **/
    @Test
    @Transactional(rollbackFor = Throwable.class)
    public void testFistCache(){
        // 第一次查询，缓存到一级缓存
        userMapper.selectById(1);
        // 第二次查询，直接读取一级缓存
        userMapper.selectById(1);

    }

```

执行结果：  
![](https://img2018.cnblogs.com/blog/1181064/201911/1181064-20191116235612319-87021059.png)

可以看到，虽然进行了两次查询，但最终只请求了一次数据库，第二次查询命中了一级缓存，直接返回了数据。  
这里有两点需要说明一下：  
1、为什么开启事务  
由于使用了数据库连接池，默认每次查询完之后自动commite，这就导致两次查询使用的不是同一个sqlSessioin，根据一级缓存的原理，它将永远不会生效。  
当我们开启了事务，两次查询都在同一个sqlSession中，从而让第二次查询命中了一级缓存。读者可以自行关闭事务验证此结论。  
2、两种一级缓存模式  
一级缓存的作用域有两种：session（默认）和statment，可通过设置local-cache-scope 的值来切换，默认为session。  
二者的区别在于session会将缓存作用于同一个sqlSesson，而statment仅针对一次查询，所以，local-cache-scope: statment可以理解为关闭一级缓存。

### 二级缓存

默认情况下，mybatis打开了二级缓存，但它并未生效，因为二级缓存的作用域是namespace，所以还需要在Mapper.xml文件中配置一下才能使二级缓存生效

*   单表二级缓存  
    下面对userMapper.xml配置一下，让其二级缓存生效,只需加入cache标签即可

```
<cache></cache>

```

单元测试用例：

```
    /**
     * 测试二级缓存效果
     * 需要*Mapper.xml开启二级缓存
     **/
    @Test
    public void testSecondCache(){
        userMapper.selectById(1);
        userMapper.selectById(1);
    }

```

执行结果：  
![](https://img2018.cnblogs.com/blog/1181064/201911/1181064-20191117002019625-2001025521.png)  
这里可以看到，第二次查询直接命中了缓存，日志还打印了该缓存的命中率。读者可以自行关闭二级缓存查看效果，通过注掉对应mapper.xml的cache标签，或者 cache-enabled: false 均可

*   多表联查二级缓存  
    接下来演示多表联查的二级缓存，user表left join user\_order表 on user.id = user\_order.user_id  
    我们考虑这样一种情况，该联查执行两次，第二次联查前更新user\_order表，如果只使用cache配置，将会查不到更新的user\_orderxi，因为两个mapper.xml的作用域不同，要想合到一个作用域，就需要用到cache-ref  
    userOrderMapper.xml

```
<cache></cache>

```

userMapper.xml

```
<cache-ref namespace="com.zhengxl.mybatiscache.mapper.UserOrderMapper"/>

```

单元测试用例：

```
    /**
     * 测试多表联查的二级缓存效果
     * 需要*Mapper.xml设定引用空间
     **/
    @Test
    public void testJoin(){
        System.out.println(userMapper.selectJoin());
        System.out.println(userMapper.selectJoin());
        UserOrder userOrder = new UserOrder();
        userOrder.setGoodName("myGoods");
        userOrder.setUserId(1);
        userOrderMapper.saveOrder(userOrder);
        System.out.println(userMapper.selectJoin());

    }

```

执行结果：  
![](https://img2018.cnblogs.com/blog/1181064/201911/1181064-20191117144858434-99423009.png)

首先查询了两次user表，第二次命中二级缓存，然后更新user_order表，使缓存失效，第三次查询时命中数据库。

#### 综上，mybatis的单机缓存就介绍完了，读者可以自行下载样例工程验证。

### 总结：

mybatis默认的session级别一级缓存，由于springboot中默认使用了hikariCP，所以基本没用，需要开启事务才有用。但一级缓存作用域仅限同一sqlSession内，无法感知到其他sqlSession的增删改，所以极易产生脏数据  
二级缓存可通过cache-ref让多个mapper.xml共享同一namespace，从而实现缓存共享，但多表联查时配置略微繁琐。  
所以生产环境建议将一级缓存设置为statment级别（即关闭一级缓存），如果有必要，可以开启二级缓存

### 注意：如果应用是分布式部署，由于二级缓存存储在本地，必然导致查询出脏数据，所以，分布式部署的应用不建议开启。

参考资料：

*   [聊聊MyBatis缓存机制](https://tech.meituan.com/2018/01/19/mybatis-cache.html)

* * *
