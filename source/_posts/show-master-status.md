---
title: show master status
id: 1478
date: 2024-10-31 22:01:57
author: daichangya
permalink: /archives/show-master-status/
tags:
- mysql
---



只有在主库上执行才能有效抵输出：

![136896120191124143732834627226970.png](https://images.jsdiff.com/1368961-20191124143732834-627226970_1602314879544.png)
![1368961201911241439528211926993328.png](https://images.jsdiff.com/1368961-20191124143952821-1926993328_1602314885116.png)
![136896120191124144237619458392195.png](https://images.jsdiff.com/1368961-20191124144237619-458392195_1602314892666.png)

具体文档如下：

```
# 在127.0.0.1:3306主库上执行

tmp@127.0.0.1 ((none))> show variables like '%server%';
+---------------------------------+--------------------------------------+
| Variable_name                   | Value                                |
+---------------------------------+--------------------------------------+
| character_set_server            | utf8mb4                              |
| collation_server                | utf8mb4_general_ci                   |
| innodb_ft_server_stopword_table |                                      |
| server_id                       | 3232266753                           |
| server_id_bits                  | 32                                   |
| server_uuid                     | ceabbacf-0c77-11ea-b49f-2016d8c96b46 |
+---------------------------------+--------------------------------------+
6 rows in set (0.01 sec)
# 根据show variables like '%server_uuid%';
# 可以获得当前mysql实例的server_uuid值

tmp@127.0.0.1 ((none))> show master status\G;
*************************** 1. row ***************************
             File: mysql-bin.000013
         Position: 269728976
     Binlog_Do_DB:
 Binlog_Ignore_DB:
Executed_Gtid_Set: 108cc4a4-0d40-11ea-9598-2016d8c96b66:1-5,
c42216ad-0d37-11ea-b163-2016d8c96b56:1-9,
ceabbacf-0c77-11ea-b49f-2016d8c96b46:1-1662590
1 row in set (0.00 sec)

ERROR:
No query specified

tmp@127.0.0.1 ((none))>

# 根据主库上执行show master status\G;
# Executed_Gtid_Set值表明：每个server_uuid代表一个实例，有多个server_uuid表明这三个实例都曾经当过主库，分别执行的事务个数都确定。在ceabbacf-0c77-11ea-b49f-2016d8c96b46实例上执行了1662590个事务，在c42216ad-0d37-11ea-b163-2016d8c96b56实例上执行了9个事务，在108cc4a4-0d40-11ea-9598-2016d8c96b66实例上执行了5个事务，但是并不知道这些实例之间事务执行的先后顺序，当然同一个实例上的事务肯定是从1开始递增，步长为1.结合该实例上的server_uuid可知道，当前主库实例执行到了ceabbacf-0c77-11ea-b49f-2016d8c96b46:1-1662590这个位置上了。

# 根据File: mysql-bin.000013和Position: 269728976可知：当前写的二进制日志文件名称和位置是mysql-bin.000013:269728976,在文件mysql-bin.000013中有“end_log_pos 269728976”的地方就是这个位置，如下就是截取了mysql-bin.000013日志最后一部分内容：

# at 269728646
#191124 13:00:04 server id 3232266753  end_log_pos 269728707    GTID    last_committed=16       sequence_number=18      rbr_only=yes
/*!50718 SET TRANSACTION ISOLATION LEVEL READ COMMITTED*//*!*/;
SET @@SESSION.GTID_NEXT= 'ceabbacf-0c77-11ea-b49f-2016d8c96b46:1662590'/*!*/;
# at 269728707
#191124 13:00:04 server id 3232266753  end_log_pos 269728776    Query   thread_id=17    exec_time=0     error_code=0
SET TIMESTAMP=1574571604/*!*/;
BEGIN
/*!*/;
# at 269728776
#191124 13:00:04 server id 3232266753  end_log_pos 269728837    Rows_query
# update table_name set name='2' where id=2
# at 269728837
#191124 13:00:04 server id 3232266753  end_log_pos 269728890    Table_map: `apple`.`table_name` mapped to number 108
# at 269728890
#191124 13:00:04 server id 3232266753  end_log_pos 269728949    Update_rows: table id 108 flags: STMT_END_F
### UPDATE `apple`.`table_name`
### WHERE
###   @1=2 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='8888' /* VARSTRING(1020) meta=1020 nullable=1 is_null=0 */
### SET
###   @1=2 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='2' /* VARSTRING(1020) meta=1020 nullable=1 is_null=0 */
# at 269728949
#191124 13:00:04 server id 3232266753  end_log_pos 269728976    Xid = 119
COMMIT/*!*/;
SET @@SESSION.GTID_NEXT= 'AUTOMATIC' /* added by mysqlbinlog */ /*!*/;
DELIMITER ;
# End of log file
/*!50003 SET COMPLETION_TYPE=@OLD_COMPLETION_TYPE*/;
/*!50530 SET @@SESSION.PSEUDO_SLAVE_MODE=0*/;
```

 https://www.cnblogs.com/igoodful/p/11922379.html

在MYSQL的主从复制中 ，通过命令show master status，可以查看master数据库当前正在使用的二进制日志及当前执行二进制日志位置

show master logs,查看所有二进制日志列表 ，和show binary logs 同义。  
  
show master status为空解决办法

默认yum安装了mysql，现在想调试一下主从，结果发现执行show master status为空。

Welcome to the MySQL monitor. Commands end with ; or g.  
Your MySQL connection id is 2  
Server version: 5.0.95 Source distribution

Copyright (c) 2000, 2011, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its  
affiliates. Other names may be trademarks of their respective  
owners.

Type ‘help;’ or ‘h’ for help. Type ‘c’ to clear the current input statement.

mysql>  
mysql> show master status;  
Empty set (0.00 sec)

原来搞错了主要配置文件的路径，yum默认安装mysql在/usr/shara/mysql下

需要执行：

cp /usr/shara/mysql/my-medium.cnf /etc/my.cnf

然后在my.cnf \[mysqld\]下加上主从配置就可以了。

server-id=1   #指定server ID  
log-bin = /home/mysql-bin.log   #开启binlog

重启mysql

mysql> show master status;  
+——————+———-+————–+——————+  
| File | Position | Binlog\_Do\_DB | Binlog\_Ignore\_DB |  
+——————+———-+————–+——————+  
| mysql-bin.000001 | 98 | | |  
+——————+———-+————–+——————+  
1 row in set (0.00 sec)  
http://imkerwin.com/166.html  
