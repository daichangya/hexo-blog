---
title: Python OrderedDict –有序字典
id: 1373
date: 2024-10-31 22:01:52
author: daichangya
excerpt: "一个OrderedDict维护插入顺序添加到字典中的项目。项目的顺序在迭代或序列化时也会保留。1.PythonOrderedDict示例OrderedDict是pythoncollections模块的一部分。要轻松构建OrderedDict，可以OrderedDict在collections模块中使"
permalink: /archives/pythonordereddict%E6%9C%89%E5%BA%8F%E5%AD%97%E5%85%B8/
categories:
 - python基础教程
---

一个**OrderedDict** **维护插入顺序**添加到字典中的项目。项目的顺序在迭代或序列化时也会保留。

1\. Python OrderedDict示例
------------------------

OrderedDict 是python collections模块的一部分。

要轻松构建OrderedDict，可以OrderedDict在collections模块中使用。
```
OrderedDictExample.py
from collections import OrderedDict
d = OrderedDict()
d['how'] = 1
d['to'] = 2
d['do'] = 3
d['in'] = 4
d['java'] = 5
for key in d:
	print(key, d[key])

('how', 1)
('to', 2)
('do', 3)
('in', 4)
('java', 5)
```
2.将OrderedDict转换为JSON
---------------------

项目的顺序在序列化为JSON时也会保留。

OrderedDict JSON示例
```
from collections import OrderedDict
import json

d = OrderedDict()
d['how'] = 1
d['to'] = 2
d['do'] = 3
d['in'] = 4
d['java'] = 5
json.dumps(d)

'{"how": 1, "to": 2, "do": 3, "in": 4, "java": 5}'
```
学习愉快！

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
