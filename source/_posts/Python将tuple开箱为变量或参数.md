---
title: Python将tuple开箱为变量或参数
id: 1370
date: 2024-10-31 22:01:52
author: daichangya
excerpt: "Python示例将N元素元组或序列开箱缩为N个变量的集合。将元组开箱缩为变量的Python示例。1.Python开箱元组示例可以使用简单的赋值操作将任何序列（或可迭代）开箱缩为变量。唯一的要求是变量的数量和结构与序列匹配。.beloposttitle300250{text-aligncenter;"
permalink: /archives/python%E5%B0%86tuple%E5%BC%80%E7%AE%B1%E4%B8%BA%E5%8F%98%E9%87%8F%E6%88%96%E5%8F%82%E6%95%B0/
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


Python示例将N元素元组或序列开箱缩为N个变量的集合。将**元组开箱缩为变量的** Python示例。

1\. Python开箱元组示例
----------------

可以使用简单的赋值操作将任何序列（或可迭代）开箱缩为变量。唯一的要求是**变量**的**数量和结构与序列匹配**。

.beloposttitle300250 { text-align: center; margin-top: 20px; margin-bottom: 20px;} @media (min-width:960px) { .beloposttitle300250 { display: none !important; } }

#### 1.1。开箱示例– 1
```
example1.py

>>> data = (1, 2, 3)

>>> x, y, z = data

>>> x

1

>>> y

2

>>> z

3
```
#### 1.2。开箱示例– 2
```
example2.py

>>> data = [ 'Lokesh', 37, 73.5, (1981, 1, 1) ]

>>> name, age, weight, dob = data

>>> name

'Lokesh'

>>> dob

(1981, 1, 1)

# Another Variation

>>> name, age, weight, (year, mon, day) = data

>>> name

'Lokesh'

>>> year

1981

>>> mon

1

>>> day

1
```
#### 1.3。开箱示例– 3
```
example3.py

>>> greeting = 'Hello'

>>> a, b, c, d, e = greeting

>>> a

'H'

>>> b

'e'

>>> c

'o'
```
2.开箱时可能出现的错误
------------

如果**元素数量不匹配**，则会出现错误。
```
example4.py

>>> p = (4, 5)

>>> x, y, z = p

Traceback (most recent call last):

File "<stdin>", line 1, in <module>

ValueError: need more than 2 values to unpack
```
学习愉快！
