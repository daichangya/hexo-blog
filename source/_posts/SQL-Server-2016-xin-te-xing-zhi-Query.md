---
title: SQL Server 2016新特性之 Query Store
id: 1589
date: 2024-10-31 22:02:02
author: daichangya
permalink: /archives/SQL-Server-2016-xin-te-xing-zhi-Query/
tags:
- 数据库
---

Query Store可帮助您跟踪执行计划（含历史记录）、运行时统计信息。可以快速查找包含多个计划的新查询，识别无效计划并强制制定更好的计划。所有示例使用的是SQL Server 2016 CTP 2.2版。

## 一、 启用及配置Query Store

### 1\. 启用

数据库属性 -\> Query Store -> Enable

![新数据库属性](https://img-blog.csdnimg.cn/img_convert/bde8d4c02072787ea8695f6704bbf8c8.gif)

也可以使用T-SQL启用：

```html
ALTER DATABASE [DEMO_1] SET QUERY_STORE = ON;

```

### 2\. 配置

单击每个属性以查看其描述。可以在官方文档找到有关每个选项的详细信息

[https://docs.microsoft.com/en-us/sql/relational-databases/performance/monitoring-performance-by-using-the-query-store?view=sql-server-2017#Options](https://docs.microsoft.com/en-us/sql/relational-databases/performance/monitoring-performance-by-using-the-query-store?view=sql-server-2017#Options)

![查询存储配置](https://img-blog.csdnimg.cn/img_convert/a51855dfdd1a58a4eb168905b8d47140.gif)

还可以使用T-SQL更改Query Store配置：

```vbnet
ALTER DATABASE [DEMO_1] 
SET QUERY_STORE (OPERATION_MODE = READ_ONLY, 
				CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 367), 
				DATA_FLUSH_INTERVAL_SECONDS = 900, 
				INTERVAL_LENGTH_MINUTES = 60, 
				MAX_STORAGE_SIZE_MB = 100, 
				QUERY_CAPTURE_MODE = AUTO, 
				SIZE_BASED_CLEANUP_MODE = AUTO)
GO
```

## 3\. 查看当前磁盘使用情况

左侧为数据库大小和Query Store占比，右侧为Query Store可用和已用大小：

![数据库属性 - 查询存储磁盘使用情况](https://img-blog.csdnimg.cn/img_convert/c482ad1fb063adcc0c714f708b43bc92.gif)

右下方有 Purge Query Data 按钮，可以删除Query Store的内容，或使用以下语句之一：

```sql
ALTER DATABASE [DEMO_1] SET QUERY_STORE CLEAR ALL
或
EXEC sys.sp_query_store_flush_db
```

## 二、Query Store相关系统对象和扩展事件

2016 CTP 2.2中有6个新的系统存储过程和7个相关目录视图，可以通过运行此查询找到：

```sql
SELECT name, type_desc FROM sys.all_objects 
WHERE name LIKE '%query_store%' or name= 'query_context_settings'
```

![系统对象](https://img-blog.csdnimg.cn/img_convert/89ff8bbd60f685e82c4b1aaa9d810a0d.gif)

*   存储过程参考[ https](https://msdn.microsoft.com/en-us/library/dn818153.aspx):[//msdn.microsoft.com/en-us/library/dn818153.aspx](https://msdn.microsoft.com/en-us/library/dn818153.aspx)
*   目录视图参考 [https](https://msdn.microsoft.com/en-us/library/dn818149.aspx):[//msdn.microsoft.com/en-us /library/dn818149.aspx](https://msdn.microsoft.com/en-us/library/dn818149.aspx)

此外，还有19个新的扩展事件：

*   query\_store\_background\_task\_persist_started - Query Store数据持久化后台任务开始执行，则触发
*   query\_store\_background\_task\_persist_finished - Query Store数据持久化后台任务成功完成，则触发
*   query\_store\_load_started - Query Store load时触发
*   query\_store\_db\_data\_structs\_not\_released - 在关闭功能时未释放Query Store数据结构，则触发
*   query\_store\_db_diagnostics - 在数据库级别上使用Query Store诊断时定期触发
*   query\_store\_db\_settings\_changed - 更改Query Store设置时触发。
*   query\_store\_db\_whitelisting\_changed - 更改Query Store数据库白名单状态时触发。
*   query\_store\_global\_mem\_obj\_size\_kb - 使用Query Store全局内存对象大小定期触发。
*   query\_store\_size\_retention\_cleanup_started - 启动size保留策略清除任务时触发。
*   query\_store\_size\_retention\_cleanup_finished - 完成size保留策略清除任务时触发。
*   query\_store\_size\_retention\_cleanup_skipped - 基于size保留策略的清除任务被跳过（不需清除）时触发
*   query\_store\_size\_retention\_query_deleted - 基于size保留策略从Query Store删除查询时触发。
*   query\_store\_size\_retention\_plan_cost - 计算计划的驱逐成本时触发
*   query\_store\_size\_retention\_query_cost - 计算查询逐出成本时触发
*   query\_store\_generate\_showplan\_failure - 因为showplan生成失败，Query Store无法存储执行计划时触发
*   query\_store\_capture\_policy\_evaluate - 在为查询计算捕获策略时触发
*   query\_store\_capture\_policy\_start_capture -当UNDECIDED查询转换捕捉到的触发
*   query\_store\_capture\_policy\_abort_capture -当UNDECIDED查询失败过渡被俘触发
*   query\_store\_schema\_consistency\_check_failure - 在Query Store架构一致性检查失败时触发

## 三、 SSMS查看Query Store功能

### 1. Query Store目录

启用Query Store后，数据库中将新增Query Store目录

![SSMS中的新数据库容器](https://img-blog.csdnimg.cn/img_convert/24f7521e03addf4cc8d8e56e08be7cd4.gif)

右键查看信息

![SSMS查询存储容器](https://img-blog.csdnimg.cn/img_convert/552786f84eaf3bd3ae905e306e4243cb.gif)

展开目录

![SSMS查询存储窗格](https://img-blog.csdnimg.cn/img_convert/61a11650adc7127f2f3dc0748fa72254.gif)

以下为2017

![](https://img-blog.csdnimg.cn/20190704162416542.png)

### 2\. top 资源消耗sql

点开“总体资源消耗”查看详细信息

![https://www.mssqltips.com/tipimages2/4009_ChartViewAll.gif](https://img-blog.csdnimg.cn/img_convert/a73bfbcb0fadfd1817282c6ad14fe2a9.gif)

左图中选中的sql有几个执行计划，右图中就会以不同颜色显示每个计划，气泡的大小取决于总执行次数。可以将鼠标悬停在左侧或右侧图表的对象上，并查看特定query\_id或plan\_id的详细统计信息。

当您单击不同的计划（3）或（4）时，窗格（5）的底部将显示此特定plan_id的执行计划。

根据左侧所选的指标，细节会有所不同：

![TOP资源消费者 - 计划摘要 - 图表视图](https://img-blog.csdnimg.cn/img_convert/e3ad6d9fe5b3a5f38d32759a19740a4a.gif)

再来具体看下面这张图

![Pane Dropdowns概述](https://img-blog.csdnimg.cn/img_convert/5947175d8ba3aa0ebde6bb608f670570.gif)

**1）top 可选指标包括：**

CPU时间、查询时间（默认）、执行计数、逻辑读、逻辑写、内存消耗、物理读

**​​​​​​​2）左图 - 垂直轴（点小箭头）：**

*   执行次数
*   num plans - 执行计划数量
*   平均逻辑读次数

**3）统计项包括：**

*   平均（默认）、最大、最小、标准差、总计

**4）左图 - 水平轴：**

*   查询ID（默认）
*   执行次数
*   平均逻辑读次数

**5）右图（计划摘要）垂直轴根据左侧图表中选择的“统计项”变化：**

*   平均（默认）、最大、最小、标准差

**6）如果屏幕分辨率较小，会隐藏一些按钮。**

点击右侧图表上的“网格”和标题旁边的“垂直视图”，查看可用的按钮：

![窗格概述 - 续](https://img-blog.csdnimg.cn/img_convert/9fdf4c03d349796fecc37106a8ec4d7d.gif)

可以将“计划摘要”从图表改为表格格式

*   “Track Query”（1）按钮将打开“Tracked Queries”窗口。
*   “View Query”（2）将使用查询的T-SQL脚本打开新的SSMS窗口。

![配置窗格](https://img-blog.csdnimg.cn/img_convert/5e921e0b4a47f49176bc19b31553bb4f.gif)

“详细网格”按钮（3）将显示包含所有统计信息的top查询列表（显示更多列）：

![详细的网格视图](https://img-blog.csdnimg.cn/img_convert/4776cff8bcbaea416065ea641b796b1c.gif)

“网格”按钮（4）显示top查询列表，但列数将受到限制，显示的列将取决于所选的统计信息和指标：

![网格视图](https://img-blog.csdnimg.cn/img_convert/f4b6adb7e64f7d08688accbc59dc7b87.gif)

“配置”按钮（5）允许您在一个位置配置窗格：

![配置窗格](https://img-blog.csdnimg.cn/img_convert/851b817e946229b33427b610342291fa.gif)![配置时间间隔](https://img-blog.csdnimg.cn/img_convert/38415fff1243352a9563ca2996e23cd6.gif)

如果查询有多个执行计划，可以单击左侧图表上的“比较计划”按钮，并排查看计划：

![多个计划](https://img-blog.csdnimg.cn/img_convert/f27ae7c4e9caaa2e24060d5aea0e739a.gif)

可以点击“强制计划”按钮，绑定执行计划

![比较计划](https://img-blog.csdnimg.cn/img_convert/d90591543b7b1174b7e543c0e2f0185f.gif)

## **四、查询Query Store视图**

查询Query Store的已用大小和最大大小

```sql
SELECT current_storage_size_mb, max_storage_size_mb FROM sys.database_query_store_options;
```

在Query Store中找查询的ID

```sql
SELECT q.query_id, t.query_sql_text, object_name(q.object_id) AS parent_object 
  FROM sys.query_store_query_text t JOIN sys.query_store_query q
   ON t.query_text_id = q.query_text_id 
  WHERE t.query_sql_text LIKE  N'%insert %db_store%'
        OR object_name(q.object_id) = 'proc_1';
```

根据查询ID、部分查询文本或对象名称（视图，[存储过程](https://so.csdn.net/so/search?q=%E5%AD%98%E5%82%A8%E8%BF%87%E7%A8%8B&spm=1001.2101.3001.7020)等）查找计划ID

```sql
SELECT  t.query_sql_text, q.query_id, p.plan_id, object_name(q.object_id) AS parent_object 
	FROM sys.query_store_query_text t JOIN sys.query_store_query q
		ON t.query_text_id = q.query_text_id 
	JOIN sys.query_store_plan p ON q.query_id = p.query_id 
WHERE q.query_id = 1 
	-- OR t.query_sql_text LIKE  N'%SELECT c1, c2 FROM  dbo.db_store%'
	-- OR object_name(q.object_id) = 'proc_1';
```

找执行计划最多的TOP 10查询

```sql
SELECT TOP 10 t.query_sql_text, q.query_id, 
	object_name(q.object_id) AS parent_object, 
	COUNT(DISTINCT p.plan_id) AS num_of_plans 
   FROM sys.query_store_query_text t JOIN sys.query_store_query q
		ON t.query_text_id = q.query_text_id 
	JOIN sys.query_store_plan p ON q.query_id = p.query_id 
GROUP BY t.query_sql_text, q.query_id, object_name(q.object_id)
HAVING  COUNT(DISTINCT p.plan_id) > 1
ORDER BY COUNT(DISTINCT p.plan_id) DESC
```

找执行次数最多的TOP 10查询

```sql
SELECT TOP 10 t.query_sql_text, q.query_id, 
	object_name(q.object_id) AS parent_object, 
	SUM(s.count_executions) total_executions
 FROM sys.query_store_query_text t JOIN sys.query_store_query q
   ON t.query_text_id = q.query_text_id 
   JOIN sys.query_store_plan p ON q.query_id = p.query_id 
   JOIN sys.query_store_runtime_stats s ON p.plan_id = s.plan_id
 WHERE s.count_executions > 1 -- used to make the query faster
GROUP BY  t.query_sql_text, q.query_id, object_name(q.object_id)
ORDER BY SUM(s.count_executions) DESC
```

找受影响的行数最多的TOP 10查询，这可能有助于检查是否有返回大量行的查询

```sql
SELECT  top 10 t.query_sql_text, q.query_id, 
	object_name(q.object_id) AS parent_object, 
	s.plan_id, s.avg_rowcount
 FROM sys.query_store_query_text t JOIN sys.query_store_query q
  ON t.query_text_id = q.query_text_id 
  JOIN sys.query_store_plan p ON q.query_id = p.query_id 
  JOIN sys.query_store_runtime_stats s ON p.plan_id = s.plan_id
WHERE s.avg_rowcount > 100
ORDER BY s.avg_rowcount DESC
```

找每次执行时编译比例最大的TOP 10查询

有时查询性能可能会受到过度重新编译的影响，使用它来查找具有大量编译的前10个查询：

```sql
WITH Query_Stats 
AS 
(
 SELECT plan_id,
 SUM(count_executions) AS total_executions
 FROM sys.query_store_runtime_stats
 GROUP BY plan_id
)
SELECT TOP 10 t.query_sql_text, q.query_id, p.plan_id,
	s.total_executions/p.count_compiles avg_compiles_per_plan
  FROM sys.query_store_query_text t JOIN sys.query_store_query q
    ON t.query_text_id = q.query_text_id 
    JOIN sys.query_store_plan p ON q.query_id = p.query_id 
    JOIN Query_Stats s ON p.plan_id = s.plan_id
ORDER BY s.total_executions/p.count_compiles DESC
```

其他一些有用的查询可以在MSDN网站上 [找到](https://msdn.microsoft.com/en-us/library/dn817826.aspx#Scenarios)：

*   最后*n次*在数据库上执行的查询
*   每个查询的执行次数
*   过去一小时内平均执行时间最长的查询数
*   在过去24小时内具有最大平均物理IO读数的查询数，具有相应的平均行数和执行计数
*   最近在性能上退化的查询（比较不同的时间点）
*   最近在性能上退化的查询（比较最近与历史执行）
*   删除即席查询。

您可能会发现以下列对自己的查询很有用：

*   sys.query\_store\_plan目录视图中的*is\_parallel\_plan*列
*   sys.query\_store\_runtime_stats目录视图中的*avg_dop*列
*   sys.query\_store\_query目录视图中的*query\_parameterization\_type*列
*   *sys.query\_store\_query*目录视图中的*is\_internal\_query*列。

## 五、 清理Query Store数据

[sp\_query\_store\_remove\_plan](https://msdn.microsoft.com/en-us/library/dn818152.aspx) 从Query Store中删除特定执行计划（执行计划的运行时统计信息也将被清除）：

```html
EXEC sp_query_store_remove_plan @plan_id = 1

```

[sp\_query\_store\_reset\_exec_stats](https://msdn.microsoft.com/en-us/library/dn911020.aspx) 可以删除特定执行计划的运行时统计信息，但将执行计划本身保留在Query Store：

```html
EXEC sp_query_store_reset_exec_stats @plan_id = 1

```

[sp\_query\_store\_remove\_query](https://msdn.microsoft.com/en-us/library/dn818157.aspx) 从Query Store中删除整个查询（包括所有执行计划和统计信息）：

```html
EXEC sp_query_store_remove_query @query_id = 1
```

参考

[https://www.mssqltips.com/sqlservertip/4009/sql-server-2016-query-store-introduction/](https://www.mssqltips.com/sqlservertip/4009/sql-server-2016-query-store-introduction/)

[https://www.mssqltips.com/sqlservertip/4047/sql-server-2016-query-store-queries/](https://www.mssqltips.com/sqlservertip/4047/sql-server-2016-query-store-queries/)

文章知识点与官方知识档案匹配，可进一步学习相关知识

[MySQL入门技能树](https://edu.csdn.net/skill/mysql/mysql-753300de6ef94af7be40fb91a05421a6)[SQL高级技巧](https://edu.csdn.net/skill/mysql/mysql-753300de6ef94af7be40fb91a05421a6)[CTE和递归查询](https://edu.csdn.net/skill/mysql/mysql-753300de6ef94af7be40fb91a05421a6)6860 人正在系统学习中