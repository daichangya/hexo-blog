---
title: Python读写CSV文件
id: 1368
date: 2024-10-31 22:01:52
author: daichangya
excerpt: 学习在Python中使用CSV文件。CSV（逗号分隔值）格式是电子表格和数据库中非常流行的导入和导出格式。Python语言包含该模块，该模块具有用于读取和写入CSV格式的数据的类。csv目录使用csv.reader（）读取CSV文件使用csv.DictReader读取CSV文件使用csv.write
permalink: /archives/Python-du-xie-CSV-wen-jian/
categories:
- python基础教程
---

1. [Python基础教程](https://blog.jsdiff.com/archives/python基础教程)
2. [在SublimeEditor中配置Python环境](https://blog.jsdiff.com/archives/在sublimeeditor中配置python环境)
3. [Python代码中添加注释](https://blog.jsdiff.com/archives/python代码中添加注释)
4. [Python中的变量的使用](https://blog.jsdiff.com/archives/python中的变量的使用)
5. [Python中的数据类型](https://blog.jsdiff.com/archives/python中的数据类型)
6. [Python中的关键字](https://blog.jsdiff.com/archives/python中的关键字)
7. [Python字符串操作](https://blog.jsdiff.com/archives/python字符串操作)
8. [Python中的list操作](https://blog.jsdiff.com/archives/python中的list操作)
9. [Python中的Tuple操作](https://blog.jsdiff.com/archives/python中的tuple操作)
10. [Pythonmax（）和min（）–在列表或数组中查找最大值和最小值](https://blog.jsdiff.com/archives/pythonmax和min在列表或数组中查找最大值和最小值)
11. [Python找到最大的N个（前N个）或最小的N个项目](https://blog.jsdiff.com/archives/python找到最大的n个前n个或最小的n个项目)
12. [Python读写CSV文件](https://blog.jsdiff.com/archives/python读写csv文件)
13. [Python中使用httplib2–HTTPGET和POST示例](https://blog.jsdiff.com/archives/python中使用httplib2httpget和post示例)
14. [Python将tuple开箱为变量或参数](https://blog.jsdiff.com/archives/python将tuple开箱为变量或参数)
15. [Python开箱Tuple–太多值无法解压](https://blog.jsdiff.com/archives/python开箱tuple太多值无法解压)
16. [Pythonmultidict示例–将单个键映射到字典中的多个值](https://blog.jsdiff.com/archives/pythonmultidict示例将单个键映射到字典中的多个值)
17. [PythonOrderedDict–有序字典](https://blog.jsdiff.com/archives/pythonordereddict有序字典)
18. [Python字典交集–比较两个字典](https://blog.jsdiff.com/archives/python字典交集比较两个字典)
19. [Python优先级队列示例](https://blog.jsdiff.com/archives/python优先级队列示例)


学习在[Python中](https://www.python.org/)使用**CSV**文件。CSV（逗号分隔值）格式是电子表格和数据库中非常流行的导入和导出格式。Python语言包含该模块，该模块具有用于**读取和写入CSV格式的数据的**类。[](https://www.python.org/)csv

目录
[使用csv.reader（）](#csv-reader)
[读取CSV文件使用csv.DictReader读取CSV](#csv-dictreader) 
[文件使用csv.writer（）写入CSV文件](#csv-writer)
[引用](#quoting)
[CSV方言](#dialects)
[自定义CSV方言](#custom-dilects)


Reading CSV file with csv.reader()
----------------------------------

该[csv.reader()](https://docs.python.org/3/library/csv.html#csv.reader)方法返回一个reader对象，该对象将遍历给定CSV文件中的行。

假设我们有以下numbers.csv包含数字的文件：

6,5,3,9,8,6,7 

以下python脚本从此CSV文件读取数据。
```
#!/usr/bin/python3

import csv
f = open('numbers.csv', 'r')
with f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
```
在上面的代码示例中，我们打开了numbers.csv以读取并使用csv.reader()方法加载数据。


现在，假设CSV文件将使用**其他定界符**。（严格来说，这不是CSV文件，但是这种做法很常见。）例如，我们有以下items.csv文件，其中的元素由竖线字符（|）分隔：

```
pen|table|keyboard
```

以下脚本从items.csv文件读取数据。
```
#!/usr/bin/python3

import csv
f = open('items.csv', 'r')
with f:
	reader = csv.reader(f, delimiter="|")
	for row in reader:
		for e in row:
			print(e)
```
我们delimiter在csv.reader()方法中使用参数指定新的分隔字符。

Reading CSV file with csv.DictReader
------------------------------------

该[csv.DictReader](https://docs.python.org/3/library/csv.html#csv.DictReader)班的运作就像**一个普通的读者，但读入字典中的信息映射**。

字典的键可以与fieldnames参数一起传递，也可以从CSV文件的第一行推断出来。

我们有以下values.csv文件：

```
min, avg, max
1, 5.5, 10
```
第一行代表字典的键，第二行代表值。
```
#!/usr/bin/python3

import csv
f = open('values.csv', 'r')
with f:
	reader = csv.DictReader(f)
	for row in reader:
		print(row)
```
上面的python脚本使用读取values.csv文件中的值csv.DictReader。

这是示例的输出。
```
$ ./read_csv3.py 
{' max': ' 10', 'min': '1', ' avg': ' 5.5'}
```
Writing CSV file using csv.writer()
-----------------------------------

该[csv.writer()](https://docs.python.org/3/library/csv.html#csv.writer)方法返回一个writer对象，该对象负责将用户数据转换为给定文件状对象上的定界字符串。
```
#!/usr/bin/python3

import csv
nms = [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]
f = open('numbers2.csv', 'w')
with f:
	writer = csv.writer(f)
	for row in nms:
		writer.writerow(row)
```
该脚本将数字写入numbers2.csv文件。该writerow()方法将一行数据写入指定的文件。

该脚本将产生以下文件（numbers2.csv）：

1,2,3,4,5,6 7,8,9,10,11,12

可以一次写入所有数据。该writerows()方法将所有给定的行写入CSV文件。

下一个代码示例将Python列表写入numbers3.csv文件。该脚本将三行数字写入文件。
```
#!/usr/bin/python3

import csv
nms = [[1, 2, 3], [7, 8, 9], [10, 11, 12]]
f = open('numbers3.csv', 'w')
with f:
	writer = csv.writer(f)
	writer.writerows(nms)
```
运行上述程序时，以下输出将写入numbers3.csv文件：

1,2,3 7,8,9 10,11,12

Quoting
-------

可以在CSV文件中引用单词。Python CSV模块中有**四种不同的引用模式**：

*   QUOTE\_ALL —引用所有字段
*   QUOTE\_MINIMAL-仅引用那些包含特殊字符的字段
*   QUOTE\_NONNUMERIC —引用所有非数字字段
*   QUOTE\_NONE —不引用字段

在下一个示例中，我们向items2.csv文件写入三行。所有非数字字段都用引号引起来。
```
#!/usr/bin/python3

import csv
f = open('items2.csv', 'w')
with f:
	writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
	writer.writerows((["coins", 3], ["pens", 2], ["bottles", 7]))
```
该程序将创建以下items2.csv文件。引用项目名称，不引用数字表示的数量。
```
"coins",3
"pens",2
"bottles",7
```
CSV Dialects
------------

尽管CSV格式是一种非常简单的格式，但还是有许多差异，例如不同的定界符，换行或引号字符。因此，有不同的CSV方言可用。

下一个代码示例将打印可用的方言及其特征。
```
#!/usr/bin/python3

import csv
names = csv.list_dialects()
for name in names:
	print(name)
	dialect = csv.get_dialect(name)
	print(repr(dialect.delimiter), end=" ")
	print(dialect.doublequote, end=" ")
	print(dialect.escapechar, end=" ")
	print(repr(dialect.lineterminator), end=" ")
	print(dialect.quotechar, end=" ")
	print(dialect.quoting, end=" ")
	print(dialect.skipinitialspace, end=" ")
	print(dialect.strict)
```
在csv.list_dialects()返回方言名称的列表和csv.get_dialect()方法返回与方言名称相关联的方言。

```
$ ./dialects.py 
excel
',' 1 None '\r\n' " 0 0 0
excel-tab
'\t' 1 None '\r\n' " 0 0 0
unix
',' 1 None '\n' " 1 0 0
```
程序将打印此输出。有三个内置的方言excel，excel-tab和unix。

Custom CSV Dialect
------------------

在本教程的最后一个示例中，我们将创建一个自定义方言。使用该csv.register_dialect()方法创建自定义方言。
```
#!/usr/bin/python3

import csv
csv.register_dialect("hashes", delimiter="#")
f = open('items3.csv', 'w')
with f:
	writer = csv.writer(f, dialect="hashes")
	writer.writerow(("pencils", 2))
	writer.writerow(("plates", 1))
	writer.writerow(("books", 4))
```
该程序使用（＃）字符作为分隔符。使用方法中的dialect选项指定方言csv.writer()。

该程序将产生以下文件（items3.csv）：
```
pencils#2
plates#1
books#4
```

在本教程中，我们探索了Python csv模块，并介绍了一些**在python中读写CSV文件的**示例。

学习愉快！
