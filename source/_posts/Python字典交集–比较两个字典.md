---
title: Python字典交集–比较两个字典
id: 1374
date: 2024-10-31 22:01:52
author: daichangya
excerpt: "Python示例，用于查找2个或更多词典之间的常见项目，即字典相交项目。1.使用“＆”运算符的字典交集最简单的方法是查找键，值或项的交集，即&amp;在两个字典之间使用运算符。example.pya={'x'1,'y'2,'z'3}b={'u'1,'v'2,'w'3,'x' 1,'y'"
permalink: /archives/python%E5%AD%97%E5%85%B8%E4%BA%A4%E9%9B%86%E6%AF%94%E8%BE%83%E4%B8%A4%E4%B8%AA%E5%AD%97%E5%85%B8/
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


Python示例，用于查找2个或更多词典之间的常见项目，即字典相交项目。

1.使用“＆”运算符的字典交集
---------------

最简单的方法是查找键，值或项的交集，即 & 在两个字典之间使用运算符。

```
example.py

a = { 'x' : 1, 'y' : 2, 'z' : 3 }
b = { 'u' : 1, 'v' : 2, 'w' : 3, 'x'  : 1, 'y': 2 }
set( a.keys() ) & set( b.keys() ) # Output set(['y', 'x'])

set( a.items() ) & set( b.items() ) # Output set([('y', 2), ('x', 1)])
```
2.设置交集（）方法
----------

Set intersection()方法返回一个集合，其中包含集合a和集合b中都存在的项。
```
example.py

a = { 'x' : 1, 'y' : 2, 'z' : 3 }

b = { 'u' : 1, 'v' : 2, 'w' : 3, 'x'  : 1, 'y': 2 }

setA = set( a )

setB = set( b )

setA.intersection( setB ) 

# Output set(['y', 'x'])

for item in setA.intersection(setB):
	print item
	
#x
#y
```
请把与**检查两个字典**在python中**是否具有相同的键或值**有关的问题交给我。

学习愉快！
