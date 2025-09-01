---
title: Python找到最大的N个（前N个）或最小的N个项目
id: 1367
date: 2024-10-31 22:01:52
author: daichangya
excerpt: Python示例使用heapq库中的**nlargest（）和nsmallest（）**函数从元素集合中找到最大（或最小）的N个元素。1.使用heapq模块的nlargest（）和nsmallest（）Pythonheapq模块可用于从集合中查找N个最大或最小的项目。它有两个功能可帮助–nlarge
permalink: /archives/Python-zhao-dao-zui-da-de-N-ge-qian-N/
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


Python示例使用**heapq**库中的**nlargest（）**和**nsmallest（）**函数从元素集合中找到最大（或最小）的N个元素。

1.使用heapq模块的nlargest（）和nsmallest（）
----------------------------------

Python heapq模块可用于从集合中**查找N个最大或最小的项目**。它有两个功能可帮助–


1.  nlargest()
2.  nsmallest()

#### 1.1。在简单的可迭代对象中查找项目

example1.py
```
>>> import heapq

>>> nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]

print(heapq.nlargest(3, nums)) 

>>> [42, 37, 23]

print(heapq.nsmallest(3, nums))

>>> [-4, 1, 2]
```
#### 1.2。查找复杂的可迭代项

example2.py
```
>>> portfolio =

[

{'name': 'IBM', 'shares': 100, 'price': 91.1},

{'name': 'AAPL', 'shares': 50, 'price': 543.22},

{'name': 'FB', 'shares': 200, 'price': 21.09},

{'name': 'HPQ', 'shares': 35, 'price': 31.75},

{'name': 'YHOO', 'shares': 45, 'price': 16.35},

{'name': 'ACME', 'shares': 75, 'price': 115.65}

]

>>> cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])

>> cheap

>>> [

{'price': 16.35, 'name': 'YHOO', 'shares': 45},

{'price': 21.09, 'name': 'FB', 'shares': 200},

{'price': 31.75, 'name': 'HPQ', 'shares': 35}

]

>>> expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])

>>> expensive

>>> [

{'price': 543.22, 'name': 'AAPL', 'shares': 50},

{'price': 115.65, 'name': 'ACME', 'shares': 75},

{'price': 91.1, 'name': 'IBM', 'shares': 100}

]
```
如果您只是想查找单个最小或最大项（N=1），则[使用min()和max()函数的]速度更快。

学习愉快！
