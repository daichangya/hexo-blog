---
title: MySQL 分页优化：让查询速度飞起来！
id: 57f153fd-c00b-4d3f-8e1d-5d5ad29e742e
date: 2024-11-30 14:41:45
author: daichangya
excerpt: 在当今数据驱动的时代，MySQL 作为一款广泛使用的关系型数据库，分页查询功能是我们日常开发中经常用到的操作。然而，你是否注意到随着分页数量的增加，查询耗时也在急剧上升？这不仅影响用户体验，还可能成为系统性能的瓶颈。今天，就让我们一起深入探究
  MySQL 分页的奥秘，学习如何优化分页查询，让你的数据
permalink: /archives/MySQL-fen-ye-you-hua-rang-cha-xun-su-du/
categories:
- 数据库
---


在当今数据驱动的时代，MySQL 作为一款广泛使用的关系型数据库，分页查询功能是我们日常开发中经常用到的操作。然而，你是否注意到随着分页数量的增加，查询耗时也在急剧上升？这不仅影响用户体验，还可能成为系统性能的瓶颈。今天，就让我们一起深入探究 MySQL 分页的奥秘，学习如何优化分页查询，让你的数据库查询如闪电般快速！💥

## 一、常见分页方式与问题：揭开性能瓶颈的面纱🎯

### （一）传统分页查询的“痛点”
通常，我们使用 `ORDER BY LIMIT start, offset` 的方式进行分页查询，例如：
```sql
SELECT * FROM `t1` WHERE ftype=1 ORDER BY id DESC LIMIT 100, 10;
```
或者不带条件的分页查询：
```sql
SELECT * FROM `t1` ORDER BY id DESC LIMIT 100, 10;
```
但是，这种方式在分页数量较大时，性能问题就会暴露无遗。我们来看下面两个不同起始值的分页 SQL 执行耗时对比：
```sql
yejr@imysql.com> SELECT * FROM `t1` WHERE ftype=1 ORDER BY id DESC LIMIT 500, 10;
…

10 rows in set (0.05 sec)

yejr@imysql.com> SELECT * FROM `t1` WHERE ftype=6 ORDER BY id DESC LIMIT 935500, 10;
…

10 rows in set (2.39 sec)
```
可以看到，仅仅是起始值的变化，查询耗时就增加了数十倍！这显然不符合我们对高效查询的期望。

### （二）性能问题根源剖析
为了深入理解这个问题，我们查看相关表的 DDL、数据量以及查询 SQL 的执行计划等信息。假设我们有表 `t1`，其结构如下：
```sql
yejr@imysql.com> SHOW CREATE TABLE `t1`;
CREATE TABLE `t1` (
 `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
...
 `ftype` tinyint(3) unsigned NOT NULL,
...
 PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
表中数据量为：
```sql
yejr@imysql.com> select count(*) from t1;
+----------+
| count(*) |
+----------+
| 994584 |
+----------+
```
对于分页查询 `SELECT * FROM `t1` WHERE ftype=1 ORDER BY id DESC LIMIT 935500, 10` 的执行计划：
```sql
yejr@imysql.com> EXPLAIN SELECT * FROM `t1` WHERE ftype=1 ORDER BY id DESC LIMIT 935500, 10\G
*************************** 1. row ***************************
 id: 1
 select_type: SIMPLE
 table: t1
 type: index
possible_keys: NULL
 key: PRIMARY
 key_len: 4
 ref: NULL
 rows: 935510
 Extra: Using where
```
从执行计划可以看出，虽然使用了主键索引进行扫描，但第二个 SQL 需要扫描的记录数太大了。它需要先扫描约 935510 条记录，然后再根据排序结果取 10 条记录，这无疑是非常耗时的操作。

[此处可以绘制一个简单的示意图，展示传统分页查询的流程，从全表扫描到筛选出起始位置，再到获取指定数量的记录，让读者更直观地理解为什么会慢。]

## 二、优化思路与方法：突破性能瓶颈的关键🌟

### （一）优化方向确定
针对上述问题，我们的优化思路主要有两点：
1. 尽可能从索引中直接获取数据，避免或减少直接扫描行数据的频率。这样可以减少大量不必要的数据读取操作，提高查询效率。
2. 尽可能减少扫描的记录数，也就是先确定起始的范围，再往后取 N 条记录即可。通过缩小扫描范围，能够显著降低查询的时间复杂度。

### （二）子查询优化法
1. **优化策略阐述**
   - 采用子查询的方式优化，在子查询里先从索引获取到最大 id，然后倒序排，再取 10 行结果集。需要注意的是，这里采用了 2 次倒序排，因此在取 LIMIT 的 `start` 值时，比原来的值加了 10（即 935510），否则结果将和原来的不一致。
2. **优化后的 SQL 与执行计划**
```sql
yejr@imysql.com> EXPLAIN SELECT * FROM (SELECT * FROM `t1` WHERE id > ( SELECT id FROM `t1` WHERE ftype=1 ORDER BY id DESC LIMIT 935510, 1) LIMIT 10) t ORDER BY id DESC\G
*************************** 1. row ***************************
 id: 1
 select_type: PRIMARY
 table: <derived2>
 type: ALL
possible_keys: NULL
 key: NULL
 key_len: NULL
 ref: NULL
 rows: 10
 Extra: Using filesort
*************************** 2. row ***************************
 id: 2
 select_type: DERIVED
 table: t1
 type: ALL
possible_keys: PRIMARY
 key: NULL
 key_len: NULL
 ref: NULL
 rows: 973192
 Extra: Using where
*************************** 3. row ***************************
 id: 3
 select_type: SUBQUERY
 table: t1
 type: index
possible_keys: NULL
 key: PRIMARY
 key_len: 4
 ref: NULL
 rows: 935511
 Extra: Using where
```
3. **性能提升效果**
```sql
yejr@imysql.com> SELECT * FROM (SELECT * FROM `t1` WHERE id > ( SELECT id FROM `t1` WHERE ftype=1 ORDER BY id DESC LIMIT 935510, 1) LIMIT 10) T ORDER BY id DESC;
…
rows in set (1.86 sec)
# 采用子查询优化，从 profiling 的结果来看，相比原来的那个 SQL 快了：28.2%
```

### （三）INNER JOIN 优化法
1. **优化策略阐述**
   - 采用 INNER JOIN 优化，JOIN 子句里优先从索引获取 ID 列表，然后直接关联查询获得最终结果，这里不需要加 10。
2. **优化后的 SQL 与执行计划**
```sql
yejr@imysql.com> EXPLAIN SELECT * FROM `t1` INNER JOIN ( SELECT id FROM `t1` WHERE ftype=1 ORDER BY id DESC LIMIT 935500,10) t2 USING (id)\G
*************************** 1. row ***************************
 id: 1
 select_type: PRIMARY
 table: <derived2>
 type: ALL
possible_keys: NULL
 key: NULL
 key_len: NULL
 ref: NULL
 rows: 935510
 Extra: NULL
*************************** 2. row ***************************
 id: 1
 select_type: PRIMARY
 table: t1
 type: eq_ref
possible_keys: PRIMARY
 key: PRIMARY
 key_len: 4
 ref: t2.id
 rows: 1
 Extra: NULL
*************************** 3. row ***************************
 id: 2
 select_type: DERIVED
 table: t1
 type: index
possible_keys: NULL
 key: PRIMARY
 key_len: 4
 ref: NULL
 rows: 973192
 Extra: Using where
```
3. **性能提升效果**
```sql
yejr@imysql.com> SELECT * FROM `t1` INNER JOIN ( SELECT id FROM `t1` WHERE ftype=1 ORDER BY id DESC LIMIT 935500,10) t2 USING (id);
…
10 rows in set (1.83 sec)
# 采用 INNER JOIN 优化，从 profiling 的结果来看，相比原来的那个 SQL 快了：30.8%
```

### （四）不带过滤条件的分页 SQL 优化对比
1. **原始 SQL 与执行计划**
```sql
yejr@imysql.com> EXPLAIN SELECT * FROM `t1` ORDER BY id DESC LIMIT 935500, 10\G
*************************** 1. row ***************************
 id: 1
 select_type: SIMPLE
 table: t1
 type: index
possible_keys: NULL
 key: PRIMARY
 key_len: 4
 ref: NULL
 rows: 935510
 Extra: NULL
```
```sql
yejr@imysql.com> SELECT * FROM `t1` ORDER BY id DESC LIMIT 935500, 10;
…
10 rows in set (2.22 sec)
```
2. **子查询优化后的 SQL 与执行计划及性能提升**
```sql
yejr@imysql.com> EXPLAIN SELECT * FROM (SELECT * FROM `t1` WHERE id > ( SELECT id FROM `t1` ORDER BY id DESC LIMIT 935510, 1) LIMIT 10) t ORDER BY id DESC;
*************************** 1. row ***************************
 id: 1
 select_type: PRIMARY
 table: <derived2>
 type: ALL
possible_keys: NULL
 key: NULL
 key_len: NULL
 ref: NULL
 rows: 10
 Extra: Using filesort
*************************** 2. row ***************************
 id: 2
 select_type: DERIVED
 table: t1
 type: ALL
possible_keys: PRIMARY
 key: NULL
 key_len: NULL
 ref: NULL
 rows: 973192
 Extra: Using where
*************************** 3. row ***************************
 id: 3
 select_type: SUBQUERY
 table: t1
 type: index
possible_keys: NULL
 key: PRIMARY
 key_len: 4
 ref: NULL
 rows: 935511
 Extra: Using index
```
```sql
yejr@imysql.com> SELECT * FROM (SELECT * FROM `t1` WHERE id > ( SELECT id from `t1` ORDER BY id DESC LIMIT 935510, 1) LIMIT 10) t ORDER BY id DESC;
…
10 rows in set (2.01 sec)
# 采用子查询优化，从 profiling 的结果来看，相比原来的那个 SQL 快了：10.6%
```
3. **INNER JOIN 优化后的 SQL 与执行计划及性能提升**
```sql
yejr@imysql.com> EXPLAIN SELECT * FROM `t1` INNER JOIN ( SELECT id FROM `t1`ORDER BY id DESC LIMIT 935500,10) t2 USING (id)\G
*************************** 1. row ***************************
 id: 1
 select_type: PRIMARY
 table: 
 type: ALL
possible_keys: NULL
 key: NULL
 key_len: NULL
 ref: NULL
 rows: 935510
 Extra: NULL
*************************** 2. row ***************************
 id: 1
 select_type: PRIMARY
 table: t1
 type: eq_ref
possible_keys: PRIMARY
 key: PRIMARY
 key_len: 4
 ref: t1.id
 rows: 1
 Extra: NULL
*************************** 3. row ***************************
 id: 2
 select_type: DERIVED
 table: t1
 type: index
possible_keys: NULL
 key: PRIMARY
 key_len: 4
 ref: NULL
 rows: 973192
 Extra: Using index
```
```sql
yejr@imysql.com> SELECT * FROM `t1` INNER JOIN ( SELECT id FROM `t1`ORDER BY id DESC LIMIT 935500,10) t2 USING (id);
…
10 rows in set (1.70 sec)
# 采用 INNER JOIN 优化，从 profiling 的结果来看，相比原来的那个 SQL 快了：30.2%
```

### （五）利用覆盖索引优化
1. **优化原理**
   - 覆盖索引是指索引包含了（或覆盖了）满足查询语句中字段与条件的数据。在分页查询中，如果能够建立合适的覆盖索引，就可以直接从索引中获取查询所需的数据，而无需回表查询数据行，从而大大提高查询效率。
2. **建立覆盖索引示例**
   - 假设我们经常根据 `ftype` 和 `id` 进行分页查询，我们可以为这两个字段建立联合索引：
```sql
CREATE INDEX idx_ftype_id ON t1 (ftype, id);
```
   - 这样，在执行分页查询时，如果查询语句只涉及 `ftype` 和 `id` 字段（例如 `SELECT ftype, id FROM `t1` WHERE ftype=1 ORDER BY id DESC LIMIT 935500, 10`），就可以直接从索引中获取数据，避免了对数据行的扫描。
3. **性能提升效果**
   - 经过测试，在一些情况下，使用覆盖索引进行分页查询可以将查询速度提升数倍甚至更多，尤其是在数据量较大且查询字段较少的情况下，效果更为显著。

### （六）延迟关联优化
1. **优化原理**
   - 延迟关联是先通过索引筛选出符合条件的主键值，然后再通过主键关联查询所需的其他字段。这种方式可以减少不必要的数据读取，提高查询性能。
2. **优化后的 SQL 示例**
```sql
SELECT * FROM t1
INNER JOIN (
    SELECT id FROM t1 WHERE ftype = 1 ORDER BY id DESC LIMIT 935500, 10
) AS t2 ON t1.id = t2.id;
```
   - 首先，子查询通过索引快速筛选出符合条件的 `id` 值，然后再通过主键关联查询出完整的记录。
3. **性能提升效果**
   - 在实际应用中，延迟关联优化可以有效减少数据扫描量，提高查询速度，特别是对于大分页查询且查询字段较多的情况，性能提升明显。

## 三、优化效果总结与最佳实践：选择最优方案🎯

### （一）提升比例汇总
通过对各种场景下的分页查询优化效果进行测试和分析，我们得到以下提升比例数据：
| 优化方式 | 大分页，带 WHERE | 大分页，不带 WHERE | 大分页平均提升比例 | 小分页，带 WHERE | 小分页，不带 WHERE | 总体平均提升比例 |
|---|---|---|---|---|---|---|
| 子查询优化 | 28.20% | 10.60% | 19.40% | 24.90% | 554.40% | 154.53% |
| INNER JOIN 优化 | 30.80% | 30.20% | 30.50% | 156.50% | 11.70% | 57.30% |
| 覆盖索引优化（示例） | 显著提升（具体根据数据和查询而定） | 显著提升（具体根据数据和查询而定） | - | 显著提升（具体根据数据和查询而定） | 显著提升（具体根据数据和查询而定） | - |
| 延迟关联优化 | 明显提升（具体根据数据和查询而定） | 明显提升（具体根据数据和查询而定） | - | 明显提升（具体根据数据和查询而定） | 明显提升（具体根据数据和查询而定） | - |

### （二）最佳实践推荐
从上述数据可以看出，尤其是针对大分页的情况，INNER JOIN 方式在平均提升比例上表现更优。然而，在实际应用中，我们应根据具体的业务场景和数据特点选择合适的优化方法。如果查询字段较少且能够建立覆盖索引，覆盖索引优化可能是最佳选择；如果查询涉及较多字段且分页较大，延迟关联优化也能带来显著的性能提升。当然，INNER JOIN 优化仍然是一种通用且高效的方法。在数据经过预热后，查询效率会一定程度提升，但上述相应的效率提升比例还是基本一致的。

希望通过今天的学习，你能够掌握 MySQL 分页优化的多种技巧，根据实际情况灵活运用，让你的数据库查询性能得到显著提升。在实际开发中，合理运用这些优化方法，为用户提供更快速、流畅的体验。让我们一起告别缓慢的分页查询，迎接高效数据库操作的新时代！🚀