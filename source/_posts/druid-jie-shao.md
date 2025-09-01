---
title: druid 介绍
id: 1588
date: 2024-10-31 22:02:02
author: daichangya
excerpt: 目录一、项目介绍二、快速概览DruidDataSource数据结构三、DruidDataSource入口概览回到顶部一、项目介绍　　1、Druid简介　　Druid连接池是阿里巴巴开源的数据库连接池项目。Druid连接池为监控而生，内置强大的监控功能，监控特性不影响性能。功能强大，能防SQL注入，内
permalink: /archives/druid-jie-shao/
tags:
- mysql
---

**目录**

*   [一、项目介绍](#_label0)
*   [二、快速概览DruidDataSource数据结构](#_label1)
*   [三、DruidDataSource入口概览](#_label2)

* * *

[回到顶部](#_labelTop)

## 一、项目介绍

　　1、Druid简介

　　Druid连接池是阿里巴巴开源的数据库连接池项目。Druid连接池为监控而生，内置强大的监控功能，监控特性不影响性能。功能强大，能防SQL注入，内置Loging能诊断Hack应用行为。

　　　　Github项目地址 https://github.com/alibaba/druid

　　　　文档 https://github.com/alibaba/druid/wiki

　　　　监控 http://x.x.x.x/druid/index.html

　　2、模块划分

　　源码里模块描述：

　　　　filter：增加自定义的扩展能力

　　　　mock：测试模块，可以使用mock模块做一些模拟测试

　　　　pool：核心，入口是DruidDataSource；

　　　　proxy：代理层

　　　　sql：负责sql解析的工作

　　　　stat：扩展能力实现，例如基于filter的监控，真正的实现在stat文件夹

　　　　support：一些附加功能，比如Json解析等

　　　　util：工具类

　　　　wall：防火墙相关，防止sql注入等操作，但是实际上对于现在的项目，对于sql注入都在网关层做了处理，不会真正到数据库连接池层面在做处理。

　　![druid.png](https://images.jsdiff.com/druid_1653530294892.png)

## 二、快速概览DruidDataSource数据结构

　　pool是Druid中最核心的目录，而DruidDataSource是pool中最关键的类之一，其承载了连接池的启动、关闭、以及连接的获取和管理等功能。

　　DruidDataSource继承了DruidAbstractDataSource，两个类内部有大量的变量，用来设置连接池的各种参数。

https://github.com/alibaba/druid/wiki/DruidDataSource%E9%85%8D%E7%BD%AE%E5%B1%9E%E6%80%A7%E5%88%97%E8%A1%A8

## 三、DruidDataSource入口概览

　　连接池在使用时最主要就是获取连接，然后使用连接查询操作数据库，那么获取连接基本上就可以作为连接池的一个入口。

　　DruidConnectionHolder是连接池中物理连接的载体，在DruidDataSource中，获取连接的getConnection方法，拿到的是DruidPooledConnection。

```
    @Override
    public DruidPooledConnection getConnection() throws SQLException {
        return getConnection(maxWait);
    }

    public DruidPooledConnection getConnection(long maxWaitMillis) throws SQLException {
        init();

        if (filters.size() > 0) {
            FilterChainImpl filterChain = new FilterChainImpl(this);
            return filterChain.dataSource_connect(this, maxWaitMillis);
        } else {
            return getConnectionDirect(maxWaitMillis);
        }
    }
```

　　从上述代码可以看到，其首先调用了 init() 方法对连接池做了初始化，然后从连接池中获取连接，获取连接实际调用的是 getConnectionDirect() 方法，在该方法中调用了 getConnectionInternal() 方法获取的连接

## 四、常见问题
https://github.com/alibaba/druid/wiki/%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98

## 五、监控及日志
在META-INF/druid-filter.properties文件中配置Filter的别名。

<table><tbody><tr><td>Filter类名</td><td>别名</td></tr><tr><td>default</td><td>com.alibaba.druid.filter.stat.StatFilter</td></tr><tr><td>stat</td><td>com.alibaba.druid.filter.stat.StatFilter</td></tr><tr><td>mergeStat</td><td>com.alibaba.druid.filter.stat.MergeStatFilter</td></tr><tr><td>encoding</td><td>com.alibaba.druid.filter.encoding.EncodingConvertFilter</td></tr><tr><td>log4j</td><td>com.alibaba.druid.filter.logging.Log4jFilter</td></tr><tr><td>log4j2</td><td>com.alibaba.druid.filter.logging.Log4j2Filter</td></tr><tr><td>slf4j</td><td>com.alibaba.druid.filter.logging.Slf4jLogFilter</td></tr><tr><td>commonlogging</td><td>com.alibaba.druid.filter.logging.CommonsLogFilter</td></tr><tr><td>wall</td><td>com.alibaba.druid.wall.WallFilter</td></tr></tbody></table>

#### 实现的基础组件
![filterList.png](https://images.jsdiff.com/filterList_1653533894434.png)
- 接口：Filter
- 抽象类：FilterEventAdapter

#### 思考
数据库加密
![企业微信截图_90161d420edf44e2b289b8cbdfdfe161.png](https://images.jsdiff.com/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_90161d42-0edf-44e2-b289-b8cbdfdfe161_1653537692365.png)


## 六、sql 抽象语法树 AST （Abstract Syntax Tree）
![sql语法解析树.png](https://images.jsdiff.com/sql%E8%AF%AD%E6%B3%95%E8%A7%A3%E6%9E%90%E6%A0%91_1653534421352.png)
https://github.com/alibaba/druid/wiki/Druid_SQL_AST

https://github.com/alibaba/druid/wiki/SQL-Parser

### 重要接口
SQLASTVisitor

### 实例讲解
#### 动态修改sql
sqlserver 查询添加 nolock
![image.png](https://images.jsdiff.com/image_1653535015668.png)
修改表名称分表
```
        Map<String, String> mapping = Collections.singletonMap("user", "user_01");
        String sql2 = "select * from user";
        String result2 = SQLUtils.refactor(sql2, JdbcConstants.MYSQL, mapping);
```
添加分页
```
String result = PagerUtils.limit(sql, JdbcConstants.SQL_SERVER, 5, 10);
//        Assert.assertEquals("SELECT TOP 10 *"
//                + "\nFROM test t WITH (nolock)", result);

```
添加权限，where添加用户ID
```
    SQLUtils.addCondition("select * from t", "userId = 8", null);
```
添加加密函数sql加密
```
AES_ENCRYPT(#{driverName}
```