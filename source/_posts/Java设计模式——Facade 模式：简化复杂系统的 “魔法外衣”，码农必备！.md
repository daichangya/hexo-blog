---
title: Java设计模式——Facade 模式：简化复杂系统的 “魔法外衣”，码农必备！
id: 463ee43b-52cd-42e5-bde4-6bc28ad2ca78
date: 2024-11-25 11:07:38
author: daichangya
cover: https://images.jsdiff.com/design02.jpg
excerpt: "🌟Java 设计模式之 Facade 模式：简化复杂系统的“魔法钥匙”🎁 各位 Java 编程爱好者们，今天我们要一起探索一个超厉害的设计模式——Facade 模式。它就像一把神奇的“魔法钥匙”，能够轻松打开复杂系统的简化之门，让你的编程之旅更加顺畅。准备好了吗？让我们一起开启这场精彩的技术之旅"
permalink: /archives/javashe-ji-mo-shi----facademo-shi/
categories:
 - 设计模式
---

# 🌟Java 设计模式之 Facade 模式：简化复杂系统的“魔法钥匙”🎁

各位 Java 编程爱好者们，今天我们要一起探索一个超厉害的设计模式——Facade 模式。它就像一把神奇的“魔法钥匙”，能够轻松打开复杂系统的简化之门，让你的编程之旅更加顺畅。准备好了吗？让我们一起开启这场精彩的技术之旅吧！🚀

## 一、Facade 模式：隐藏复杂，展现简单的“魔法师”🧙‍♂️

### （一）模式简介
Facade 模式，从字面上理解，就是给复杂的子系统穿上一件漂亮的“外衣”，为子系统中的一组接口提供一个统一且一致的界面。它的主要使命就是将系统内部那些让人头疼的复杂性统统隐藏起来，只把一个简洁明了、易于使用和理解的接口暴露给客户端。就好像一个魔法师，把杂乱无章的魔法道具（复杂系统的内部实现）藏在身后，只在前台展示一个神奇的魔法棒（Facade 接口），让观众（客户端）看到精彩绝伦的魔法表演（轻松调用系统功能），而无需关心背后的魔法是如何施展的（系统内部细节）。🌟

### （二）经典案例：数据库 JDBC 操作的华丽变身😎

在 JSP 应用开发中，数据库操作是必不可少的一环，但传统的直接操作数据库的代码就像一团乱麻。让我们来看看这段熟悉又“可怕”的代码：

```java
public class DBCompare {
    Connection conn = null;
    PreparedStatement prep = null;
    ResultSet rset = null;
    try {
        // 加载数据库驱动，这就像是在黑暗中寻找开启宝藏（数据库连接）的神秘钥匙🔑
        Class.forName("<driver>").newInstance();
        // 获取数据库连接，仿佛是打开了通往宝藏库（数据库）的大门🚪
        conn = DriverManager.getConnection("<database>");
        String sql = "SELECT * FROM <table> WHERE <column name> =?";
        // 创建预编译语句对象，就像是准备好一个特殊的工具来挖掘宝藏（执行查询）⛏
        prep = conn.prepareStatement(sql);
        // 设置查询参数，如同在工具上设置精准的挖掘方向🧭
        prep.setString(1, "<column value>");
        // 执行查询并获取结果集，这是终于挖到宝藏（数据）并把它们收集起来的时刻💎
        rset = prep.executeQuery();
        if (rset.next()) {
            // 输出查询结果，展示我们挖到的宝藏（数据）的一部分🧾
            System.out.println(rset.getString("<column name"));
        }
    } catch (SQLException e) {
        e.printStackTrace();
    } finally {
        try {
            // 关闭结果集，就像收拾好挖掘工具，准备下次使用🗑
            if (rset!= null) {
                rset.close();
            }
            // 关闭预编译语句对象，把工具放回原位🗂
            if (prep!= null) {
                prep.close();
            }
            // 关闭数据库连接，再次锁上宝藏库的大门🔒
            if (conn!= null) {
                conn.close();
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

哇哦！每次进行数据库操作都要重复这么多繁琐的步骤，就像每次寻宝都要重新走一遍复杂的迷宫一样。而且，一旦需要更换数据库（比如从 MySQL 切换到 Oracle）或者添加新功能（如使用连接池来提高性能），那就得在每个涉及数据库操作的地方都进行修改，这简直就是一场噩梦，维护成本高得让人望而却步。😫

### （三）Facade 模式的解救之道：打造统一接口🎉

别担心，Facade 模式来拯救我们了！我们引入一个 Facade 外观对象，就像一个聪明的管家，把数据库操作中那些不变的部分（如连接建立、资源管理等）提炼出来，精心打造一个简单易用的接口。这样一来，以后不管是更换数据库驱动还是添加新功能，只需要在这个 Facade 接口上进行修改就可以了，系统的复杂性瞬间降低，灵活性却像火箭一样飙升。🚀

假设我们创建了一个 `Mysql` 类来专门处理与 MySQL 数据库的交互，并提供了一个 Facade 接口，那么之前那段繁琐的代码就可以摇身一变：

```java
public class DBCompare {
    String sql = "SELECT * FROM <table> WHERE <column name> =?";

    try {
        // 创建 Mysql 对象并传入 SQL 语句，就像把寻宝任务交给了专业的管家🧑‍✈️
        Mysql msql = new Mysql(sql);
        msql.setString(1, "<column value>");
        // 执行查询并获取结果集，管家轻松帮我们完成寻宝并带回宝藏（数据）💼
        ResultSet rset = msql.executeQuery();
        if (rset.next()) {
            System.out.println(rset.getString("<column name"));
        }
    } catch (SQLException e) {
        e.printStackTrace();
    } finally {
        // 关闭 Mysql 连接，管家把善后工作处理得妥妥当当🧹
        msql.close();
        msql = null;
    }
}
```

看，在这个新的代码世界里，`Mysql` 类内部把数据库连接、查询等复杂操作都封装得严严实实，客户端代码只需要和 `Mysql` 类提供的简单接口愉快地玩耍，完全不用操心底层那些让人眼花缭乱的数据库操作细节。是不是感觉代码一下子变得清爽又可爱了呢？😘

### （四）Facade 模式的强大力量💪
想象一下，客户端就像一个顾客，它只知道自己想要购买某种商品（调用系统功能）。Facade 接口就像是商店的前台服务员，它提供了一个简单明了的服务界面，顾客只需要告诉服务员自己的需求，不需要知道商品是如何从仓库中取出、如何结账等复杂流程。而子系统则是商店的仓库、收银台等一系列复杂组件，它们负责具体的商品存储、计价等工作。服务员（Facade 接口）在背后协调仓库、收银台等组件（子系统），为顾客（客户端）提供高效、便捷的服务。

![facade01.jpg](https://images.jsdiff.com/facade01.jpg)

## 二、总结与进阶指南📖

Facade 模式无疑是我们编程世界中的一颗璀璨明珠，在梳理系统关系、降低耦合度方面有着非凡的魔力。在实际开发中，你可能已经在不知不觉中运用了类似的简化思想，但现在通过深入理解 Facade 模式，我们能够更加系统、科学地运用这种设计理念，构建出更加灵活、易于维护的软件系统，就像从一个只会搭建简单积木房子的孩子变成了一个能够设计宏伟建筑的大师。🏗