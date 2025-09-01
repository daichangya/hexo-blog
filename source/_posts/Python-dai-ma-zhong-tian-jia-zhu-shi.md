---
title: Python代码中添加注释
id: 1359
date: 2024-10-31 22:01:52
author: daichangya
excerpt: 在Python（或任何其他编程语言）中，注释用于解释源代码。注释描述了代码，这有助于将来维护应用程序。python中的注释#prints4print(2+2)print(2+3)#prints5&quot;&quot;&quot;printsthesumoftwonumberswhichare2an
permalink: /archives/Python-dai-ma-zhong-tian-jia-zhu-shi/
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


在Python（或任何其他编程语言）中，注释用于解释源代码。注释描述了代码，这有助于将来维护应用程序。

python中的注释
```
# prints 4

print(2 + 2)

print(2 + 3) # prints 5

"""

prints the sum of

two numbers which are 2 and 2

"""

print(2 + 2)
```
Python中的注释类型
------------

[Python](https://blog.jsdiff.com/archives/python基础教程)支持编写简单的单行注释以及多行注释。


#### 单行注释

一个简单的单行注释将以井号（#）字符开头。Python运行时会忽略#字符后写的任何文本，并将其视为注释。

单行注释
```
# This is a simple comment

print(2 + 2)

print(2 + 3) # prints 5
```
#### 多行注释

Python没有什么特别的东西可以写多行注释。要编写它，我们可以编写**多个单行注释**。

我推荐这种形式的评论。

多行注释
```
# This statement

# prints the sum of

# two numbers which are 2 and 2

print(2 + 2)
```
我们可以利用未分配给变量的**多行字符串文字**（使用_三引号_）。Python会忽略未分配给任何变量的字符串文字，因此它不会影响程序执行。


Un-assigned string literal
```
"""

This statement

prints the sum of

two numbers which are 2 and 2

"""

print(2 + 2)
```
将有关在python中编写注释的问题交给我。

学习愉快！
