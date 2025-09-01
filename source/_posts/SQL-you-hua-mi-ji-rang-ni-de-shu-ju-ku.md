---
title: SQL优化秘籍：让你的数据库查询飞起来
id: 29c75895-4f94-4419-a8d9-f61dcdda62c9
date: 2024-12-10 13:52:48
author: daichangya
cover: https://images.jsdiff.com/sql01.jpg
excerpt: 一、SQL优化：开启高效数据库之旅 在当今数据爆炸的时代，数据库的性能至关重要。而SQL作为与数据库交互的关键语言，其优化程度直接影响着数据处理的速度和效率。想象一下，在一个大型电商平台的促销活动中，数据库需要快速处理海量的订单查询、库存更新等操作。如果SQL语句没有经过优化，可能会导致页面加载缓慢
permalink: /archives/SQL-you-hua-mi-ji-rang-ni-de-shu-ju-ku/
categories:
- 数据库
---

## 一、SQL优化：开启高效数据库之旅
在当今数据爆炸的时代，数据库的性能至关重要。而SQL作为与数据库交互的关键语言，其优化程度直接影响着数据处理的速度和效率。想象一下，在一个大型电商平台的促销活动中，数据库需要快速处理海量的订单查询、库存更新等操作。如果SQL语句没有经过优化，可能会导致页面加载缓慢、用户体验差，甚至系统崩溃。接下来，就让我们一起深入探索SQL优化的奥秘，让你的数据库查询如闪电般快速。

## 二、优化SQL的关键步骤

### （一）了解SQL执行频率
1. **使用SHOW STATUS命令**
   - 可以通过`SHOW STATUS`获取服务器状态信息，它能提供session级别和global级别的统计结果。例如，要查看当前session的执行情况，可以使用`SHOW STATUS like "Com_%"`；若要查看全局级别，则使用`show global status`。
   - 对于Myisam和Innodb存储引擎都计数的参数有：
     - `Com_select`：执行select操作的次数，一次查询只累加1。
     - `Com_insert`：执行insert操作的次数，批量插入也只累加一次。
     - `Com_update`：执行update操作的次数。
     - `Com_delete`：执行delete操作的次数。
   - 针对Innodb存储引擎计数且累加算法不同的参数包括：
     - `Innodb_rows_read`：select查询返回的行数。
     - `Innodb_rows_inserted`：执行Insert操作插入的行数。
     - `Innodb_rows_updated`：执行update操作更新的行数。
     - `Innodb_rows_deleted`：执行delete操作删除的行数。
   - 对于事务型应用，`Com_commit`和`Com_rollback`可以帮助了解事务提交和回滚的情况。频繁回滚可能意味着应用编写存在问题。
   - 此外，`Connections`（试图连接Mysql服务器的次数）、`Uptime`（服务器工作时间）、`Slow_queries`（慢查询的次数）等参数也有助于了解数据库的基本情况。

### （二）定位低效SQL语句
1. **利用慢查询日志**
   - 可以通过`--log-slow-queries[=file_name]`选项启动mysqld，它会写一个包含所有执行时间超过`long_query_time`秒的SQL语句的日志文件。但需要注意的是，慢查询日志在查询结束后才记录，所以在应用反映执行效率问题时查询慢查询日志可能无法及时定位问题。
2. **使用SHOW PROCESSLIST命令**
   - 可以实时查看当前MySQL正在进行的线程，包括线程的状态、是否锁表等信息，从而对SQL执行情况进行实时监控，同时对锁表操作进行优化。
<separator></separator>
### （三）分析低效SQL的执行计划
通过`EXPLAIN`或者`DESC`获取MySQL如何执行SELECT语句的信息，包括表的连接方式和连接次序等，以便针对性地进行优化。

## 三、MySQL索引的深度剖析

### （一）索引的使用规则
1. **索引的基本原理**
   - 索引用于快速定位在某个列中有特定值的行，对相关列使用索引是提高SELECT操作性能的最佳途径。但查询要使用索引，需要满足一定条件，例如查询条件中需要使用索引关键字。
2. **索引不被使用的情况**
   - 如果mysql估计使用索引比全表扫描更慢，则不使用索引。例如，对于均匀分布在1和100之间的`key_part1`，查询`SELECT * FROM table_name where key_part1 > 1 and key_part1 < 90`使用索引可能不是最佳选择。
   - 使用heap表并且where条件中不用`＝`索引列（其他`>`、`<`、`>=`、`<=`均不使用索引，MyISAM和innodb表除外）。
   - 使用or分割的条件，如果or前的条件中的列有索引，后面的列中没有索引，那么涉及到的索引都不会使用。
   - 创建复合索引时，如果条件中使用的列不是索引列的第一部分（不是前缀索引）。
   - 如果`like`是以`％`开始。
   - 对where后边条件为字符串的一定要加引号，否则即使字符串为数字，mysql会自动转为字符串，但不使用索引。

### （二）查看索引使用情况
1. **通过Handler_read_key和Handler_read_rnd_next判断**
   - 如果`Handler_read_key`的值很高，说明索引经常被使用；如果很低，则表明增加索引得到的性能改善不高。
   - `Handler_read_rnd_next`的值高则意味着查询运行低效，可能需要建立索引补救。例如，如果进行大量的表扫描，该值会较高，通常说明表索引不正确或写入的查询没有利用索引。
   - 语法：`mysql> show status like 'Handler_read%';`

### （三）索引优化案例
假设我们有一个员工表（employees），包含员工ID（employee_id）、姓名（name）、年龄（age）和入职日期（hire_date）等字段，并且在员工ID上建立了主键索引，在姓名和年龄上建立了复合索引（name_age_index）。
```sql
-- 创建员工表
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    name VARCHAR(50),
    age INT,
    hire_date DATE
);

-- 创建复合索引
CREATE INDEX name_age_index ON employees (name, age);
```
现在有一个查询，要查找年龄在30到40岁之间且姓名以“J”开头的员工：
```sql
SELECT * FROM employees WHERE age BETWEEN 30 AND 40 AND name LIKE 'J%';
```
在这个查询中，由于使用了复合索引的前缀（name列）并且`like`操作不是以`%`开头，所以可以利用索引快速定位符合条件的员工记录，大大提高查询效率。

## 四、具体查询语句优化技巧大揭秘

### （一）避免全表扫描
1. **合理创建索引**
   - 应优先在where及order by涉及的列上建立索引。例如，在一个订单表（orders）中，如果经常根据订单日期（order_date）进行查询和排序，那么在订单日期列上建立索引可以显著提高查询速度。
```sql
-- 创建订单表
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10, 2)
);

-- 在订单日期列上建立索引
CREATE INDEX idx_order_date ON orders (order_date);
```
2. **使用相关技巧引导优化器**
   - 使用`ANALYZE TABLE tbl_name`为扫描的表更新关键字分布，帮助优化器更好地选择执行计划。
   - 对扫描的表使用`FORCE INDEX`告知MySQL使用特定索引，例如`SELECT * FROM t1, t2 FORCE INDEX (index_for_column) WHERE t1.col_name = t2.col_name`。
   - 用`--max-seeks-for-key=1000`选项启动mysqld或使用`SET max_seeks_for-key=1000`告知优化器假设关键字扫描不会超过1,000次关键字搜索。

### （二）避免在where子句中的不当操作
1. **避免null值判断**
   - 否则将导致引擎放弃使用索引而进行全表扫描。例如，`select id from t where num is null`应尽量避免。可以在num列上设置默认值（如0），然后查询`select id from t where num = 0`。
2. **避免使用!=或<>操作符**
   - 应尽量使用其他合适的操作符，如`<`、`<=`、`=`、`>`、`>=`、`BETWEEN`、`IN`等。例如，`SELECT id FROM t WHERE col LIKE 'Mich%'`会使用索引，而`SELECT id FROM t WHERE col LIKE '%ike'`不会使用索引。
3. **谨慎使用or连接条件**
   - 可以使用`UNION`合并查询来替代，如`select id from t where num = 10 union all select id from t where num = 20`。但在某些情况下，or条件也可以避免全表扫描，例如where语句里面如果带有or条件，myisam表能用到索引，innodb不行，且必须所有的or条件都必须是独立索引。
4. **慎用in和not in**
   - 对于连续的数值，能用`between`就不要用`in`了，如`Select id from t where num between 1 and 3`比`select id from t where num in(1, 2, 3)`效率更高。
5. **避免like '%abc%'或like '%abc'形式的查询**
   - 若要提高效率，可以考虑全文检索。而`select id from t where name like 'abc%'`才用到索引。
6. **避免在where子句中使用参数导致全表扫描**
   - 例如`select id from t where num = @num`会进行全表扫描，可以改为强制查询使用索引：`select id from t with(index(索引名)) where num = @num`。
7. **避免在where子句中对字段进行表达式和函数操作**
   - 如`select id from t where num / 2 = 100`应改为`select id from t where num = 100 * 2`；`select id from t where substring(name, 1, 3) = 'abc'`应改为`select id from t where name like 'abc%'`；`select id from t where datediff(day, createdate, '2005 - 11 - 30') = 0`应改为`select id from t where createdate >= '2005 - 11 - 30' and createdate < '2005 - 12 - 1'`。同时，不要在where子句中的“=”左边进行函数、算术运算或其他表达式运算。
8. **确保索引字段的正确使用**
   - 如果索引是复合索引，必须使用到该索引中的第一个字段作为条件时才能保证系统使用该索引，并且应尽可能让字段顺序与索引顺序相一致。

### （三）其他优化注意事项
1. **避免无意义查询**
   - 如`select col1, col2 into #t from t where 1 = 0`应改成`create table #t(...)`。
2. **用exists代替in（在合适场景）**
   - 例如`select num from a where num in(select num from b)`可以用`select num from a where exists(select 1 from b where num = a.num)`替换。
3. **合理创建索引数量**
   - 索引不是越多越好，一个表的索引数最好不要超过6个，应根据具体情况权衡。
4. **避免更新clustered索引数据列（如果频繁更新）**
   - 因为这会导致整个表记录顺序的调整，耗费大量资源。
5. **尽量使用数字型字段和变长字段**
   - 数字型字段在查询和连接时性能更高，变长字段（如varchar/nvarchar）比定长字段（如char/nchar）存储空间小且搜索效率高。
6. **避免返回不必要字段**
   - 不要使用`select * from t`，而用具体的字段列表代替。
7. **合理使用临时表和游标**
   - 尽量使用表变量代替临时表，避免频繁创建和删除临时表。尽量避免使用游标，优先寻找基于集的解决方案。
8. **优化事务操作**
   - 尽量避免大事务操作，提高系统并发能力。
9. **优化count操作**
   - `count(*)`优于`count(1)`和`count(primary_key)`，且`count(column)`和`count(*)`含义不同。innodb引擎在统计方面和myisam不同，myisam在无查询条件时`count(*)`可直接从计数器取值，innodb则需全表扫描；有查询条件时两者效率一致。同时，主键索引count(*)时较慢，因为InnoDB引擎主键索引与数据文件存储在一起，每次统计都需扫描数据文件，而二级索引统计数据时无需扫描数据文件。
10. **优化order by语句**
   - 可以通过建立合适的复合索引来优化。例如，对于`SELECT * FROM SALES WHERE NAME = "name" ORDER BY SALE_DATE DESC`，可以建立复合索引`ALTER TABLE SALES DROP INDEX NAME, ADD INDEX (NAME, SALE_DATE)`。同时要注意where条件和order by使用相同索引且顺序一致，并且字段升降序相同的情况才能使用索引，否则可能不使用索引。
11. **优化GROUP BY**
   - 可以指定`ORDER BY NULL`禁止排序来避免消耗，如`INSERT INTO foo SELECT a, COUNT(*) FROM bar GROUP BY a ORDER BY NULL`。

## 五、Explain：SQL优化的得力助手

### （一）Explain的作用
`Explain`可以显示mysql如何使用索引来处理select语句以及连接表，帮助我们选择更好的索引和写出更优化的查询语句。

### （二）Explain结果列解读
1. **table列**
   - 显示这一行的数据是关于哪张表的。
2. **type列**
   - 这是重要的列，显示连接使用了何种类型，从最好到最差的连接类型为：system、const、eg_reg、ref、ref_or_null、range、indexhe、ALL。例如，system表示表仅有一行（系统表），const表示表最多有一个匹配行，在查询开始时被读取且列值可被优化器视为常数。
3. **possible_keys列**
   - 显示可能应用在这张表中的索引，如果为空则没有可能的索引，可以据此为相关域从WHERE语句中选择合适的索引。
4. **key列**
   - 实际使用的索引，如果为NULL则没有使用索引，极少数情况下MYSQL会选择优化不足的索引，此时可以使用`USEINDEX（indexname）`强制使用一个索引或`IGNORE INDEX（indexname）`强制MYSQL忽略索引。
5. **key_len列**
   - 使用的索引的长度，在不损失精确性的情况下，长度越短越好。
6. **ref列**
   - 显示索引的哪一列被使用了，如果可能的话，是一个常数。
7. **rows列**
   - MYSQL认为必须检查的用来返回请求数据的行数（扫描行的数量）。
8. **Extra列**
   - 包含MySQL解决查询的详细信息，如`Using temporary`（需要创建临时表来存储结果，通常发生在对不同列集进行ORDER BY时）、`Using filesort`（需要进行额外步骤来排序，查询需要优化）、`Using index`（列数据仅从索引返回，未读取实际行，通常发生在请求列都是同一索引部分时）、`Using where`（使用了WHERE从句限制行匹配或返回）等。

### （三）案例分析
假设有一个学生成绩表（student_scores），包含学生ID（student_id）、课程ID（course_id）、成绩（score）等字段，并且在学生ID和课程ID上建立了复合索引（student_course_index）。
```sql
-- 创建学生成绩表
CREATE TABLE student_scores (
    student_id INT,
    course_id INT,
    score INT,
    PRIMARY KEY (student_id, course_id)
);

-- 创建复合索引
CREATE INDEX student_course_index ON student_scores (student_id, course_id);
```
现在有一个查询，要查找学生ID为1的所有成绩记录：
```sql
EXPLAIN SELECT * FROM student_scores WHERE student_id = 1;
```
在这个例子中，`EXPLAIN`的结果可能显示`table`为`student_scores`，`type`为`ref`（因为使用了索引且可能匹配少量行），`possible_keys`为`student_course_index`，`key`为`student_course_index`，`key_len`为合适的长度（根据索引字段类型计算），`ref`为常数（这里是1），`rows`为估计需要检查的行数，`Extra`可能为`Using index`（因为只从索引返回数据）。通过分析`EXPLAIN`结果，我们可以确定查询是否有效地使用了索引，以及是否需要进一步优化。

## 六、SQL核心语句优化技巧

### （一）插入数据
可以使用批量插入来提高效率，例如：
```sql
INSERT mytable (first_column, second_column, third_column)
VALUES ('some data', 'some more data', 'yet more data'),
       ('some data', 'some more data', 'yet more data'),
       ('some data', 'some more data', 'yet more data');
```

### （二）清空数据表
使用`TRUNCATE TABLE`语句删除表中的所有记录，它比`DELETE`语句快得多，因为记录的删除不作记录。例如：`TRUNCATE TABLE `mytable`;`

### （三）用SELECT创建记录和表
1. **INSERT与SELECT结合插入数据**
   - 可以从一个表拷贝记录到另一个表，例如：
```sql
INSERT mytable(first_column, second_column)
SELECT another_first, another_second FROM anothertable WHERE another_first = 'Copy Me!';
```
2. **SELECT INTO创建新表**
   - 可以创建一个包含原表所有数据的新表，例如：`SELECT * INTO newtable FROM mytable;`也可以指定特定字段和使用WHERE子句限制拷贝的记录。