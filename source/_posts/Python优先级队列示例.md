---
title: Python优先级队列示例
id: 1375
date: 2024-10-31 22:01:52
author: daichangya
excerpt: "1.什么是优先队列优先级队列是一种抽象数据类型，类似于常规队列或堆栈数据结构，但每个元素还具有与之关联的“优先级”。在优先级队列中，优先级高的元素先于优先级低的元素提供。如果两个元素具有相同的优先级，则将根据其在队列中的顺序为其提供服务。2.Python中的优先级队列实现以下python程序使用该h"
permalink: /archives/python%E4%BC%98%E5%85%88%E7%BA%A7%E9%98%9F%E5%88%97%E7%A4%BA%E4%BE%8B/
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
20. [python中如何格式化日期](https://blog.jsdiff.com/archives/python%E4%B8%AD%E5%A6%82%E4%BD%95%E6%A0%BC%E5%BC%8F%E5%8C%96%E6%97%A5%E6%9C%9F)
21. [30 分钟 Python 爬虫教程](https://blog.jsdiff.com/archives/30%E5%88%86%E9%92%9Fpython%E7%88%AC%E8%99%AB%E6%95%99%E7%A8%8B)

1.什么是优先队列
---------

*   [优先级队列](https://en.wikipedia.org/wiki/Priority_queue)是一种抽象数据类型，类似于常规队列或堆栈数据结构，但每个元素还具有与之关联的“优先级”。
*   在优先级队列中，优先级高的元素先于优先级低的元素提供。
*   如果两个元素具有相同的优先级，则将根据其在队列中的顺序为其提供服务。

2\. Python中的优先级队列实现
-------------------

以下python程序使用该heapq模块实现简单的优先级队列：
```
PriorityQueue.py

import heapq

class PriorityQueue:
	def __init__(self):
		self._queue = []
		self._index = 0

	def push(self, item, priority):
		heapq.heappush(self._queue, (-priority, self._index, item))
		self._index += 1

	def pop(self):
		return heapq.heappop(self._queue)[-1]
```
3\. Python优先级队列示例
-----------------

让我们看一个如何使用上面创建的优先级队列的例子。

```
example.py

class Item:
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return 'Item({!r})'.format(self.name)

>>> q = PriorityQueue()

>>> q.push(Item('how'), 1)

>>> q.push(Item('to'), 5)

>>> q.push(Item('do'), 4)

>>> q.push(Item('in'), 2)

>>> q.push(Item('java'), 1)

>>> q.pop()

Item('to') #5

>>> q.pop()

Item('do') #4

>>> q.pop()

Item('in') #2

>>> q.pop()

Item('how') #1

>>> q.pop()

Item('java') #1
```
学习愉快！
