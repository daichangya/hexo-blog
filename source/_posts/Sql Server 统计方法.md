---
title: Sql Server 统计方法
id: 1625
date: 2024-10-31 22:02:03
author: daichangya
excerpt: "查询表中的某一个字段在那些存储过程和视图中被使用SELECTDISTINCTOBJECT_NAME(sd.id)Dependent_Object,(SELECTxtypeFROMsysobjectssoWHEREso.id=sd.id)Object_TypeFROMsysobjectssoINNER"
permalink: /archives/sqlserver%E7%BB%9F%E8%AE%A1%E6%96%B9%E6%B3%95/
tags: 
 - 数据库
---

#### 查询表中的某一个字段在那些存储过程和视图中被使用
```sql
SELECT DISTINCT
  OBJECT_NAME(sd.id) Dependent_Object,
  (
    SELECT
      xtype
    FROM
      sysobjects so
    WHERE
      so.id = sd.id
  ) Object_Type
FROM
  sysobjects so
  INNER JOIN syscolumns sc ON so.id = sc.id
  INNER JOIN sysdepends sd ON so.id = sd.depid
  and sc.colid = sd.depnumber
WHERE
  so.id = OBJECT_ID('表名称')
  AND sc.name = '字段名称';
```
#### 表列信息查询,包含字段名称,字段类型,字段长度
```sql
SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '表名称'
```
#### 统计存储过程的行数
```sql
SELECT
    OBJECT_NAME(object_id) AS ProcedureName,
    (LEN(definition) - LEN(REPLACE(definition, CHAR(10), ''))) AS LineCount
FROM
    sys.sql_modules
WHERE
    object_id = OBJECT_ID('ProcedureName'); -- 替换ProcedureName为你的存储过程名称
```
#### 统计存储过程被那些存储过程引用了
```sql
SELECT * FROM sys.dm_sql_referencing_entities ('dbo.ProcedureName', 'OBJECT');

```
#### 统计表被那些存储过程引用了
```sql
SELECT * FROM sys.dm_sql_referencing_entities ('dbo.表名称', 'OBJECT');
```
#### 统计存储过程使用了那些 对象及存储过程
```sql

SELECT
        referenced_id,
        referenced_entity_name AS table_name,
        referenced_minor_name  AS referenced_column_name,
        is_all_columns_found
    FROM
        sys.dm_sql_referenced_entities ('dbo.ProcedureName', 'OBJECT');

```
#### 统计某一个字段在那些对象中被使用
```sql
select [name] from [dbo].sysobjects where id in(select id from [dbo].syscolumns Where name='字段名称')
```

#### 统计表被那些存储过程和试图使用
```sql
SELECT OBJECT_SCHEMA_NAME ( referencing_id ) AS referencing_schema_name, 
    OBJECT_NAME(referencing_id) AS referencing_entity_name,  
    o.type_desc AS referencing_desciption,  
    COALESCE(COL_NAME(referencing_id, referencing_minor_id), '(n/a)') AS referencing_minor_id,  
    referencing_class_desc, referenced_class_desc, 
    referenced_server_name, referenced_database_name, referenced_schema_name, 
    referenced_entity_name,  
    COALESCE(COL_NAME(referenced_id, referenced_minor_id), '(n/a)') AS referenced_column_name, 
    is_caller_dependent, is_ambiguous 
FROM sys.sql_expression_dependencies AS sed 
INNER JOIN sys.objects AS o ON sed.referencing_id = o.object_id 
WHERE referenced_id = OBJECT_ID(N'表名称')
```
#### 存储过程使用情况统计
```sql
SELECT top 1000 a.name                AS 存储过程名称,
       a.create_date         AS 创建日期,
       a.modify_date         AS 修改日期,
       b.cached_time         AS 缓存时间,
       b.last_execution_time AS 最后执行日期,
       b.execution_count     AS 执行次数
FROM sys.procedures a
       LEFT JOIN sys.dm_exec_procedure_stats b ON a.object_id = b.object_id AND b.database_id = '6'
WHERE a.is_ms_shipped = 0 and a.name in(SELECT  DISTINCT name
FROM    sysobjects o ,
        syscomments s
WHERE   o.id = s.id
      and a.name not in (SELECT
    d.referenced_entity_name
FROM
    sys.sql_expression_dependencies AS d  INNER JOIN sys.objects AS o ON d.referencing_id = o.object_id
WHERE
    d.referenced_entity_name in(SELECT name from sys.procedures))
        )
ORDER BY b.execution_count desc;
```


