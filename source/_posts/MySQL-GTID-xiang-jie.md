---
title: MySQL GTID详解
id: 1479
date: 2024-10-31 22:01:57
author: daichangya
excerpt: MySQL在5.6版本推出了GTID复制，相比传统的复制，GTID复制对于运维更加友好，这个事物是谁产生，产生多少事物，非常直接的标识出来。今天将讨论一下关于从库showslavestatus中的Retrieved_Gtid_Set和Executed_Gtid_Set.Retrieved_Gtid_
permalink: /archives/MySQL-GTID-xiang-jie/
tags:
- mysql
---

MySQL在5.6版本推出了GTID复制，相比传统的复制，GTID复制对于运维更加友好，这个事物是谁产生，产生多少事物，非常直接的标识出来。

今天将讨论一下 关于从库show slave status 中的Retrieved_Gtid_Set 和 Executed_Gtid_Set.

Retrieved_Gtid_Set : 从库已经接收到主库的事务编号

Executed_Gtid_Set : 从库自身已经执行的事务编号

下面将解释这两列的含义：

首先看看master和slave的server-uuid

	 Master:

	[root@localhost][db1]> show variables like '%uuid%';       
	+---------------+--------------------------------------+
	| Variable_name | Value                                |
	+---------------+--------------------------------------+
	| server_uuid   | 2a09ee6e-645d-11e7-a96c-000c2953a1cb |
	+---------------+--------------------------------------+
	1 row in set (0.00 sec)

	Slave

	[root@localhost][(none)]> show variables like '%uuid%';
	+---------------+--------------------------------------+
	| Variable_name | Value                                |
	+---------------+--------------------------------------+
	| server_uuid   | 8ce853fc-6f8a-11e7-8940-000c29e3f5ab |
	+---------------+--------------------------------------+
	1 row in set (0.01 sec)

其中主库的server-id是10,从库的server-id是20.

搭建好主从以后，如果没有数据写入，那么show slave status是下面这样的:

	Replicate_Ignore_Server_Ids: 
		    ** Master_Server_Id: 10
		          Master_UUID: 2a09ee6e-645d-11e7-a96c-000c2953a1cb**
		     Master_Info_File: mysql.slave_master_info
		            SQL_Delay: 0
		  SQL_Remaining_Delay: NULL
	      Slave_SQL_Running_State: **Slave has read all relay log; waiting for more updates**
		   Master_Retry_Count: 86400
		          Master_Bind: 
	      Last_IO_Error_Timestamp: 
	     Last_SQL_Error_Timestamp: 
		       Master_SSL_Crl: 
		   Master_SSL_Crlpath: 
	 **Retrieved_Gtid_Set: 
		    Executed_Gtid_Set:** 
		        Auto_Position: 1
		 Replicate_Rewrite_DB: 
		         Channel_Name: 
		   Master_TLS_Version: 

如果在主库创建表，并且写入2条数据，是下面这样的:

	[root@localhost][db1]> **create table t2 ( id int);**
	Query OK, 0 rows affected (0.07 sec)

	[root@localhost][db1]> **insert into t2 select 1;**
	Query OK, 1 row affected (0.07 sec)
	Records: 1  Duplicates: 0  Warnings: 0

	[root@localhost][db1]> **insert into t2 select 2;**
	Query OK, 1 row affected (0.02 sec)
	Records: 1  Duplicates: 0  Warnings: 0

这里auto_commit=1,可以看到创建表加插入2条数据，一共执行了3个事务.

从库：show slave status\\G

	Replicate_Ignore_Server_Ids: 
		     Master_Server_Id: 10
		          Master_UUID: 2a09ee6e-645d-11e7-a96c-000c2953a1cb
		     Master_Info_File: mysql.slave_master_info
		            SQL_Delay: 0
		  SQL_Remaining_Delay: NULL
	      Slave_SQL_Running_State: Slave has read all relay log; waiting for more updates
		   Master_Retry_Count: 86400
		          Master_Bind: 
	      Last_IO_Error_Timestamp: 
	     Last_SQL_Error_Timestamp: 
		       Master_SSL_Crl: 
		   Master_SSL_Crlpath: 
		   **Retrieved_Gtid_Set**: **2a09ee6e-645d-11e7-a96c-000c2953a1cb**:**1-3**
		    **Executed_Gtid_Set**: **2a09ee6e-645d-11e7-a96c-000c2953a1cb**:**1-3**
		        Auto_Position: 1

主库：show master status

	+------------------+----------+--------------+------------------+------------------------------------------+
	| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set                        |
	+------------------+----------+--------------+------------------+------------------------------------------+
	| mysql-bin.000001 |      912 |              |                  | **2a09ee6e-645d-11e7-a96c-000c2953a1cb**:**1-3** |
	+------------------+----------+--------------+------------------+------------------------------------------+
	1 row in set (0.00 sec)

其中主库的 Executed_Gtid_Set为：**2a09ee6e-645d-11e7-a96c-000c2953a1cb**:**1-3**

看到从库的Retrieved_Gtid_Set为:   **2a09ee6e-645d-11e7-a96c-000c2953a1cb**:**1-3**

Executed_Gtid_Set为： **2a09ee6e-645d-11e7-a96c-000c2953a1cb**:**1-3**

也就是说主库产生了3个事务，从库接收到了主库的3个事务，且都已全部执行。

 其中 **2a09ee6e-645d-11e7-a96c-000c2953a1cb** 是主库的server-uuid. 可以从从库解析binlog看出:

	\# at 154
	#170823  0:38:38 **server id 10**  end_log_pos 219 CRC32 0x6268641f         GTID    last_committed=0        **sequence_number=1**
	SET @@SESSION.GTID_NEXT= '**2a09ee6e-645d-11e7-a96c-000c2953a1cb**:**1**'/*!*/;
	\# at 219
	#170823  0:38:38 server id 10  end_log_pos 316 CRC32 0x6c837618         Query   thread_id=103   exec_time=0     error_code=0
	use \`db1\`/*!*/;
	SET TIMESTAMP=1503419918/*!*/;
	SET @@session.pseudo_thread_id=103/*!*/;
	SET @@session.foreign_key_checks=1, @@session.sql_auto_is_null=0, @@session.unique_checks=1, @@session.autocommit=1/*!*/;
	SET @@session.sql_mode=1436549152/*!*/;
	SET @@session.auto_increment_increment=1, @@session.auto_increment_offset=1/*!*/;
	/*!\\C utf8 *//*!*/;
	SET @@session.character_set_client=33,@@session.collation_connection=33,@@session.collation_server=33/*!*/;
	SET @@session.lc_time_names=0/*!*/;
	SET @@session.collation_database=DEFAULT/*!*/;
	**create table t2 ( id int)**
	/*!*/;

可以看见server-id为10，gtid-next为**2a09ee6e-645d-11e7-a96c-000c2953a1cb**:**1**，执行了建表，剩下的

**2a09ee6e-645d-11e7-a96c-000c2953a1cb**:**2 与 ****2a09ee6e-645d-11e7-a96c-000c2953a1cb**:**3** 执行的查询我没有写出来。

**这里也体现了文章开始提到的：这个事物由谁产生，产生多少事物，非常直接的标识了出来。**

那么对于文章开头那个诡异的gtid是怎么出来的呢？先说说已经执行的事务：

**Executed_Gtid_Set: 2a09ee6e-645d-11e7-a96c-000c2953a1cb:1-33,**  
**8ce853fc-6f8a-11e7-8940-000c29e3f5ab:1**

这里的**2a09ee6e-645d-11e7-a96c-000c2953a1cb:1-33**好理解，就是已经执行主库的1-33的事务，那么**8ce853fc-6f8a-11e7-8940-000c29e3f5ab:1**呢?其实也简单，有两种情况：

### NO.1  从库有数据写入（即从库插入数据）

	[root@localhost][db1]> **insert into t2 select 1;**
	Query OK, 1 row affected (0.03 sec)
	Records: 1  Duplicates: 0  Warnings: 0

	**show slave status\\G;**

	Replicate_Ignore_Server_Ids: 
		     Master_Server_Id: 10
		          Master_UUID: 2a09ee6e-645d-11e7-a96c-000c2953a1cb
		     Master_Info_File: mysql.slave_master_info
		            SQL_Delay: 0
		  SQL_Remaining_Delay: NULL
	      Slave_SQL_Running_State: Slave has read all relay log; waiting for more updates
		   Master_Retry_Count: 86400
		          Master_Bind: 
	      Last_IO_Error_Timestamp: 
	     Last_SQL_Error_Timestamp: 
		       Master_SSL_Crl: 
		   Master_SSL_Crlpath: 
		   **Retrieved_Gtid_Set**: **2a09ee6e-645d-11e7-a96c-000c2953a1cb**:**1-3**
		    **Executed_Gtid_Set**: **2a09ee6e-645d-11e7-a96c-000c2953a1cb**:**1-3**,
	**8ce853fc-6f8a-11e7-8940-000c29e3f5ab**:**1**
		        Auto_Position: 1
		 Replicate_Rewrite_DB:

可以看到已经执行的事务有来自主库的**2a09ee6e-645d-11e7-a96c-000c2953a1cb**:**1-3**,也有从库自己写入的数据：**8ce853fc-6f8a-11e7-8940-000c29e3f5ab**:**1**。我们可以解析binlog看看

	**mysqlbinlog -vv mysql-bin.000001 --include-gtids='8ce853fc-6f8a-11e7-8940-000c29e3f5ab:1'**

	\# at 896
	#170823  0:59:19 **server id 20 ** end_log_pos 961 CRC32 0x0492528a         GTID    last_committed=3        **sequence_number=4**
	SET @@SESSION.GTID_NEXT= '**8ce853fc-6f8a-11e7-8940-000c29e3f5ab**:**1**'/*!*/;
	\# at 961
	#170823  0:59:19 server id 20  end_log_pos 1032 CRC32 0xbf545cca        Query   thread_id=25    exec_time=0     error_code=0
	SET TIMESTAMP=1503421159/*!*/;
	SET @@session.pseudo_thread_id=25/*!*/;
	SET @@session.foreign_key_checks=1, @@session.sql_auto_is_null=0, @@session.unique_checks=1, @@session.autocommit=1/*!*/;
	SET @@session.sql_mode=1436549152/*!*/;
	SET @@session.auto_increment_increment=1, @@session.auto_increment_offset=1/*!*/;
	/*!\\C utf8 *//*!*/;
	SET @@session.character_set_client=33,@@session.collation_connection=33,@@session.collation_server=33/*!*/;
	SET @@session.lc_time_names=0/*!*/;
	SET @@session.collation_database=DEFAULT/*!*/;
	BEGIN
	/*!*/;
	\# at 1032
	#170823  0:59:19 server id 20  end_log_pos 1079 CRC32 0x2f2de3ec        Rows_query
	\# insert into t2 select 1
	\# at 1079
	#170823  0:59:19 server id 20  end_log_pos 1123 CRC32 0x18fe1c5c        Table_map: \`db1\`.\`t2\` mapped to number 109
	\# at 1123
	#170823  0:59:19 server id 20  end_log_pos 1163 CRC32 0x163a708e        Write_rows: table id 109 flags: STMT_END_F

	BINLOG '
	52KcWR0UAAAALwAAADcEAACAABdpbnNlcnQgaW50byB0MiBzZWxlY3QgMezjLS8=
	52KcWRMUAAAALAAAAGMEAAAAAG0AAAAAAAEAA2RiMQACdDIAAQMAAVwc/hg=
	52KcWR4UAAAAKAAAAIsEAAAAAG0AAAAAAAEAAgAB//4BAAAAjnA6Fg==
	'/*!*/;
	\### **INSERT INTO \`db1\`.\`t2\`**
	\### **SET**
	\###  ** @1=1 /* INT meta=0 nullable=1 is_null=0 */**
	\# at 1163
	#170823  0:59:19 server id 20  end_log_pos 1194 CRC32 0xe3347ac1        Xid = 68
	COMMIT/*!*/;
	SET @@SESSION.GTID_NEXT= 'AUTOMATIC' /* added by mysqlbinlog */ /*!*/;

从binlog中可以清楚看到是从库进行了写入。

### NO.2 主从切换(这里使用的是MHA切换主从)

		     Master_Server_Id: 20
		          Master_UUID: 8ce853fc-6f8a-11e7-8940-000c29e3f5ab
		     Master_Info_File: mysql.slave_master_info
		            SQL_Delay: 0
		  SQL_Remaining_Delay: NULL
	      Slave_SQL_Running_State: Slave has read all relay log; waiting for more updates
		   Master_Retry_Count: 86400
		          Master_Bind: 
	      Last_IO_Error_Timestamp: 
	     Last_SQL_Error_Timestamp: 
		       Master_SSL_Crl: 
		   Master_SSL_Crlpath: 
		   **Retrieved_Gtid_Set**: **8ce853fc-6f8a-11e7-8940-000c29e3f5ab**:**1**
		    **Executed_Gtid_Set**: **2a09ee6e-645d-11e7-a96c-000c2953a1cb**:**1-3**,
	**8ce853fc-6f8a-11e7-8940-000c29e3f5ab**:**1**
		        Auto_Position: 1

可以看到主从切换以后主库的server-id是20。这里的意思是接收到主库**8ce853fc-6f8a-11e7-8940-000c29e3f5ab**:**1**,并已经执行了这个事物，这个事物其实就是之前从库写入的那条数据。对于**2a09ee6e-645d-11e7-a96c-000c2953a1cb**:**1-3**就是之前主库执行的3个事务，如果此时在主库再插入一条数据，那么变化如下：

	** Retrieved_Gtid_Set**: **8ce853fc-6f8a-11e7-8940-000c29e3f5ab**:**1-2**  
	  **Executed_Gtid_Set**: **2a09ee6e-645d-11e7-a96c-000c2953a1cb**:**1-3**,  
	**8ce853fc-6f8a-11e7-8940-000c29e3f5ab**:**1-2**

**下面说说GTID不连续问题，类似 ****2a09ee6e-645d-11e7-a96c-000c2953a1cb**:**37-45** **，这个是由于binlog被清理后导致的，我们可以测试一下，然后查看gtid_purge变量。**

binlog不可能永远驻留在服务上，需要定期进行清理(通过**expire_logs_days**可以控制定期清理间隔)，否则迟早它会把磁盘用尽。**gtid_purged**用于记录已经被清除了的binlog事务集合，它是**gtid_executed**的子集。只有**gtid_executed**为空时才能手动设置该变量，此时会同时更新**gtid_executed**为和**gtid_purged**相同的值。**gtid_executed**为空意味着要么之前没有启动过基于GTID的复制，要么执行过**RESET MASTER**。执行**RESET MASTER**时同样也会把**gtid_purged**置空，即始终保持**gtid_purged**是**gtid_executed**的子集。

	[root@localhost][db1]> **show master logs;**
	+------------------+-----------+
	| Log_name         | File_size |
	+------------------+-----------+
	| mysql-bin.000001 |      3530 |
	+------------------+-----------+
	1 row in set (0.00 sec)

	[root@localhost][db1]> **flush logs;**
	Query OK, 0 rows affected (0.05 sec)

	[root@localhost][db1]> **show master logs;**
	+------------------+-----------+
	| Log_name         | File_size |
	+------------------+-----------+
	| mysql-bin.000001 |      3577 |
	| mysql-bin.000002 |       234 |
	+------------------+-----------+
	2 rows in set (0.00 sec)

	[root@localhost][db1]> **PURGE BINARY LOGS TO 'mysql-bin.000002';**
	Query OK, 0 rows affected (0.01 sec)

	[root@localhost][db1]> **show master logs;**
	+------------------+-----------+
	| Log_name         | File_size |
	+------------------+-----------+
	| mysql-bin.000002 |       234 |
	+------------------+-----------+
	1 row in set (0.00 sec)

然后只要从库有重新启动，才会读取。MySQL服务器启动时，通过读binlog文件，初始化gtid_executed和gtid_purged,使它们的值能和上次MySQL运行时一致。

**gtid_executed 本机被执行并写入日志的gtid**  
**gtid_purged      该变量中记录的是本机上已经执行过，但是已经被purge binary logs to命令清理的gtid_set**

**没启动前：**

	 **Retrieved_Gtid_Set**: **8ce853fc-6f8a-11e7-8940-000c29e3f5ab**:**1-9**
	  **Executed_Gtid_Set**: **2a09ee6e-645d-11e7-a96c-000c2953a1cb**:**1-3**,
	**8ce853fc-6f8a-11e7-8940-000c29e3f5ab**:**1-9**

重启并插入数据：

		    Master_Server_Id: 20
		          Master_UUID: 8ce853fc-6f8a-11e7-8940-000c29e3f5ab
		     Master_Info_File: mysql.slave_master_info
		            SQL_Delay: 0
		  SQL_Remaining_Delay: NULL
	      Slave_SQL_Running_State: Slave has read all relay log; waiting for more updates
		   Master_Retry_Count: 86400
		          Master_Bind: 
	      Last_IO_Error_Timestamp: 
	     Last_SQL_Error_Timestamp: 
		       Master_SSL_Crl: 
		   Master_SSL_Crlpath: 
		   **Retrieved_Gtid_Set**: **8ce853fc-6f8a-11e7-8940-000c29e3f5ab**:**10**
		    **Executed_Gtid_Set**: **2a09ee6e-645d-11e7-a96c-000c2953a1cb**:**1-3**,
	**8ce853fc-6f8a-11e7-8940-000c29e3f5ab**:**1-10**
		        Auto_Position: 1

	[root@localhost][(none)]> **show variables like 'gtid_purged';** 
	+---------------+------------------------------------------------------------------------------------+
	| Variable_name | Value                                                                              |
	+---------------+------------------------------------------------------------------------------------+
	| gtid_purged   | **2a09ee6e-645d-11e7-a96c-000c2953a1cb**:**1-3**,
	**8ce853fc-6f8a-11e7-8940-000c29e3f5ab**:**1-9** |
	+---------------+------------------------------------------------------------------------------------+
	1 row in set (0.01 sec)

可以看到 **2a09ee6e-645d-11e7-a96c-000c2953a1cb**:**1-3 与 ****8ce853fc-6f8a-11e7-8940-000c29e3f5ab**:**1-9** 都在mysql-bin.000001里，已经被清除了。

### **下面的两个实验，将会告诉我们如果主日志被清除，但从还没获得这些日志，该怎么处理：**

## 实验一：如果slave所需要事务对应的GTID在master上已经被purge了

根据`show global variables like '%gtid%'`的命令结果我们可以看到，和GTID相关的变量中有一个`gtid_purged`。从字面意思以及 [官方文档](http://dev.mysql.com/doc/refman/5.6/en/replication-options-gtids.html#sysvar_gtid_purged)可以知道该变量中记录的是本机上已经执行过，但是已经被`purge binary logs to`命令清理的`gtid_set`。  
本节中我们就要试验下，如果master上把某些slave还没有fetch到的gtid event purge后会有什么样的结果。

以下指令在master上执行

```
master [localhost] {msandbox} (test) > show global variables like '%gtid%';
+---------------------------------+----------------------------------------+
| Variable_name                   | Value                                  |
+---------------------------------+----------------------------------------+
| binlog_gtid_simple_recovery     | OFF                                    |
| enforce_gtid_consistency        | ON                                     |
| gtid_executed                   | 24024e52-bd95-11e4-9c6d-926853670d0b:1 |
| gtid_mode                       | ON                                     |
| gtid_owned                      |                                        |
| gtid_purged                     |                                        |
| simplified_binlog_gtid_recovery | OFF                                    |
+---------------------------------+----------------------------------------+
7 rows in set (0.01 sec)
 
master [localhost] {msandbox} (test) > flush logs;create table gtid_test2 (ID int) engine=innodb;
Query OK, 0 rows affected (0.04 sec)
 
Query OK, 0 rows affected (0.02 sec)
 
master [localhost] {msandbox} (test) > flush logs;create table gtid_test3 (ID int) engine=innodb;
Query OK, 0 rows affected (0.04 sec)
 
Query OK, 0 rows affected (0.04 sec)
 
master [localhost] {msandbox} (test) > show master status;
+------------------+----------+--------------+------------------+------------------------------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set                        |
+------------------+----------+--------------+------------------+------------------------------------------+
| mysql-bin.000005 |      359 |              |                  | 24024e52-bd95-11e4-9c6d-926853670d0b:1-3 |
+------------------+----------+--------------+------------------+------------------------------------------+
1 row in set (0.00 sec)
 
master [localhost] {msandbox} (test) > purge binary logs to 'mysql-bin.000004';
Query OK, 0 rows affected (0.03 sec)
 
master [localhost] {msandbox} (test) > show global variables like '%gtid%';
+---------------------------------+------------------------------------------+
| Variable_name                   | Value                                    |
+---------------------------------+------------------------------------------+
| binlog_gtid_simple_recovery     | OFF                                      |
| enforce_gtid_consistency        | ON                                       |
| gtid_executed                   | 24024e52-bd95-11e4-9c6d-926853670d0b:1-3 |
| gtid_mode                       | ON                                       |
| gtid_owned                      |                                          |
| gtid_purged                     | 24024e52-bd95-11e4-9c6d-926853670d0b:1   |
| simplified_binlog_gtid_recovery | OFF                                      |
+---------------------------------+------------------------------------------+
7 rows in set (0.00 sec)
```

在slave2上重新做一次主从，以下命令在slave2上执行

```
slave2 [localhost] {msandbox} ((none)) > change master to master_host='127.0.0.1',master_port =21288,master_user='rsandbox',master_password='rsandbox',master_auto_position=1;
Query OK, 0 rows affected, 2 warnings (0.04 sec)
 
slave2 [localhost] {msandbox} ((none)) > start slave;
Query OK, 0 rows affected (0.01 sec)
 
slave2 [localhost] {msandbox} ((none)) > show slave status\G
*************************** 1. row ***************************
                          ......
             Slave_IO_Running: No
            Slave_SQL_Running: Yes
                          ......
                   Last_Errno: 0
                   Last_Error:
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 0
              Relay_Log_Space: 151
                          ......
                Last_IO_Errno: 1236
                Last_IO_Error: Got fatal error 1236 from master when reading data from binary log: 'The slave is connecting using CHANGE MASTER TO MASTER_AUTO_POSITION = 1, but the master has purged binary logs containing GTIDs that the slave requires.'
               Last_SQL_Errno: 0
               Last_SQL_Error:
                          ......
                Auto_Position: 1
1 row in set (0.00 sec)
```

## 实验二：忽略purged的部分，强行同步

那么实际生产应用当中，偶尔会遇到这样的情况：某个slave从备份恢复后（或者load data infile）后，DBA可以人为保证该slave数据和master一致；或者即使不一致，这些差异也不会导致今后的主从异常（例如：所有master上只有insert没有update）。这样的前提下，我们又想使slave通过replication从master进行数据复制。此时我们就需要跳过master已经被purge的部分，那么实际该如何操作呢？  
我们还是以实验一的情况为例：

先确认master上已经purge的部分。从下面的命令结果可以知道master上已经缺失`24024e52-bd95-11e4-9c6d-926853670d0b:1`这一条事务的相关日志

```
master [localhost] {msandbox} (test) > show global variables like '%gtid%';
+---------------------------------+------------------------------------------+
| Variable_name                   | Value                                    |
+---------------------------------+------------------------------------------+
| binlog_gtid_simple_recovery     | OFF                                      |
| enforce_gtid_consistency        | ON                                       |
| gtid_executed                   | 24024e52-bd95-11e4-9c6d-926853670d0b:1-3 |
| gtid_mode                       | ON                                       |
| gtid_owned                      |                                          |
| gtid_purged                     | 24024e52-bd95-11e4-9c6d-926853670d0b:1   |
| simplified_binlog_gtid_recovery | OFF                                      |
+---------------------------------+------------------------------------------+
7 rows in set (0.00 sec)
```

在slave上通过`set global gtid_purged='xxxx'`的方式，跳过已经purge的部分

```
slave2 [localhost] {msandbox} ((none)) > stop slave;
Query OK, 0 rows affected (0.04 sec)
 
slave2 [localhost] {msandbox} ((none)) > set global gtid_purged = '24024e52-bd95-11e4-9c6d-926853670d0b:1';
Query OK, 0 rows affected (0.05 sec)
 
slave2 [localhost] {msandbox} ((none)) > start slave;
Query OK, 0 rows affected (0.01 sec)
 
slave2 [localhost] {msandbox} ((none)) > show slave status\G                
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                          ......
              Master_Log_File: mysql-bin.000005
          Read_Master_Log_Pos: 359
               Relay_Log_File: mysql_sandbox21290-relay-bin.000004
                Relay_Log_Pos: 569
        Relay_Master_Log_File: mysql-bin.000005
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
                          ......
          Exec_Master_Log_Pos: 359
              Relay_Log_Space: 873
                          ......
             Master_Server_Id: 1
                  Master_UUID: 24024e52-bd95-11e4-9c6d-926853670d0b
             Master_Info_File: /data/mysql/rsandbox_mysql-5_6_23/node2/data/master.info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
      Slave_SQL_Running_State: Slave has read all relay log; waiting for the slave I/O thread to update it
                          ......
           Retrieved_Gtid_Set: 24024e52-bd95-11e4-9c6d-926853670d0b:2-3
            Executed_Gtid_Set: 24024e52-bd95-11e4-9c6d-926853670d0b:1-3
                Auto_Position: 1
1 row in set (0.00 sec)
```

可以看到此时slave已经可以正常同步，并补齐了`24024e52-bd95-11e4-9c6d-926853670d0b:2-3`范围的binlog日志。