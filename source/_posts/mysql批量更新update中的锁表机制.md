---
title: mysql批量更新update中的锁表机制
id: 1497
date: 2024-10-31 22:01:58
author: daichangya
permalink: /archives/mysql%E6%89%B9%E9%87%8F%E6%9B%B4%E6%96%B0update%E4%B8%AD%E7%9A%84%E9%94%81%E8%A1%A8%E6%9C%BA%E5%88%B6/
tags: 
 - mysql
---

mysql的行锁是通过索引加载的，即行锁是加在索引响应的行上的，要是对应的SQL语句没有走索引，则会全表扫描，行锁则无法实现，取而代之的是表锁。

```
CREATE TABLE SIMPLE_USER(
    ID BIGINT (20) NOT NULL AUTO_INCREMENT,
    NAME VARCHAR (32) DEFAULT NULL,
    PHONE VARCHAR (11) DEFAULT NULL,
    ADDRESS VARCHAR (32) DEFAULT NULL,
    PRIMARY KEY (id)
) ENGINE = INNODB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8;
```

如上面的建表语句，当执行如下update语句时，数据库对该表施加的是表锁。即在该update执行完之前，所有对该表的update是不允许的。

```
UPDATE SIMPLE_USER SET ADDRESS='David Road' WHERE NAME='David';
```

当对 WHERE 条件的字段添加索引，如本例中的NAME字段，

```
ALTER TABLE SIMPLE_USER ADD INDEX idx_name(NAME);
```

再执行上面update语句时，数据库对该表施加的是行锁，此时仅对NAME='David'的行的update是不允许的，对 NAME<>'David' 的行的update不受影响。
