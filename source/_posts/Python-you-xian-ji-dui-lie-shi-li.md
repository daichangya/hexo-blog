---
title: Python优先级队列示例
id: 1375
date: 2024-10-31 22:01:52
author: daichangya
excerpt: 1.什么是优先队列优先级队列是一种抽象数据类型，类似于常规队列或堆栈数据结构，但每个元素还具有与之关联的“优先级”。在优先级队列中，优先级高的元素先于优先级低的元素提供。如果两个元素具有相同的优先级，则将根据其在队列中的顺序为其提供服务。2.Python中的优先级队列实现以下python程序使用该h
permalink: /archives/Python-you-xian-ji-dui-lie-shi-li/
categories:
- python基础教程
---

1. [Python基础教程](https://www.tushu.info/archives/Python-ji-chu-jiao-cheng)
2. [在SublimeEditor中配置Python环境](https://www.tushu.info/archives/zai-Sublime-Editor-zhong-pei-zhi-Python)
3. [Python代码中添加注释](https://www.tushu.info/archives/Python-dai-ma-zhong-tian-jia-zhu-shi)
4. [Python中的变量的使用](https://www.tushu.info/archives/Python-zhong-de-bian-liang-de-shi-yong)
5. [Python中的数据类型](https://www.tushu.info/archives/Python-zhong-de-shu-ju-lei-xing)
6. [Python中的关键字](https://www.tushu.info/archives/Python-zhong-de-guan-jian-zi)
7. [Python字符串操作](https://www.tushu.info/archives/Python-zi-fu-chuan-cao-zuo)
8. [Python中的list操作](https://www.tushu.info/archives/Python-zhong-de-list-cao-zuo)
9. [Python中的Tuple操作](https://www.tushu.info/archives/Python-zhong-de-Tuple-cao-zuo)
10. [Pythonmax（）和min（）–在列表或数组中查找最大值和最小值](https://www.tushu.info/archives/Python-max-he-min-zai-lie-biao-huo-shu)
11. [Python找到最大的N个（前N个）或最小的N个项目](https://www.tushu.info/archives/Python-zhao-dao-zui-da-de-N-ge-qian-N)
12. [Python读写CSV文件](https://www.tushu.info/archives/Python-du-xie-CSV-wen-jian)
13. [Python中使用httplib2–HTTPGET和POST示例](https://www.tushu.info/archives/Python-zhong-shi-yong-httplib2-HTTP-GET)
14. [Python将tuple开箱为变量或参数](https://www.tushu.info/archives/Python-jiang-tuple-kai-xiang-wei-bian)
15. [Python开箱Tuple–太多值无法解压](https://www.tushu.info/archives/Python-kai-xiang-Tuple-tai-duo-zhi-wu)
16. [Pythonmultidict示例–将单个键映射到字典中的多个值](https://www.tushu.info/archives/Python-multidict-shi-li-jiang-dan-ge)
17. [PythonOrderedDict–有序字典](https://www.tushu.info/archives/Python-OrderedDict-you-xu-zi-dian)
18. [Python字典交集–比较两个字典](https://www.tushu.info/archives/Python-zi-dian-jiao-ji-bi-jiao-liang-ge)
19. [Python优先级队列示例](https://www.tushu.info/archives/Python-you-xian-ji-dui-lie-shi-li)
20. [python中如何格式化日期](https://www.tushu.info/archives/Python-zhong-ru-he-ge-shi-hua-ri-qi)
21. [30 分钟 Python 爬虫教程](https://www.tushu.info/archives/30-fen-zhong-Python-pa-chong-jiao-cheng)

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
