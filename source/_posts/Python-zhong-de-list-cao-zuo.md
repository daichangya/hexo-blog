---
title: Python中的list操作
id: 1364
date: 2024-10-31 22:01:52
author: daichangya
excerpt: 在Python中，列表为：有序索引（索引从0开始）易变的异构的（列表中的项目不必是同一类型）写为方括号之间的逗号分隔值列表listOfSubjects=['physics','chemistry',&quot;mathematics&quot;]listOfIds=[0,1,2,3,4]miscLi
permalink: /archives/Python-zhong-de-list-cao-zuo/
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


在[Python中](https://blog.jsdiff.com/archives/python基础教程)，列表为：

*   有序
*   索引（索引从0开始）
*   易变的
*   异构的（列表中的项目不必是同一类型）
*   写为方括号之间的逗号分隔值列表
```
listOfSubjects = ['physics', 'chemistry', "mathematics"]
listOfIds = [0, 1, 2, 3, 4]
miscList = [0, 'one', 2, 'three']
```
1\. Access list items
---------------------

要访问列表中的值，请使用切片语法或数组索引形式的方括号来获取单个项目或项目范围。


传递的索引值可以是正数或负数。如果索引是负数则从列表的末尾开始计数。

`list [m : n]`表示子列表从索引`m`（包括）开始，到索引`n`（不包括）结束。

*   如果`m`未提供，则假定其值为零。
*   如果`n`未提供，则选择范围直到列表的最后。
```
ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print( ids[0] )			# 0
print( ids[1:5] )		# [1, 2, 3, 4]
print( ids[ : 3] )		# [0, 1, 2]
print( ids[7 : ] )		# [7, 8, 9]\
print( ids[-8:-5] )		# [2, 3, 4]
```
2\. Modily list
---------------

要更改列表中的特定项目，请使用其索引引用该项目并分配一个新值。
```
charList =  ["a", "b", "c"]
charList [2] = "d"
print (charList)	# ['a', 'b', 'd']
```
3\. Iterate a list
------------------

我们可以使用来遍历列表项`for loop`。

```
charList =  ["a", "b", "c"]

for x in charList:
	print(x)

# a
# b
# c
```

4\. Check if a item exists in the list
--------------------------------------

使用`'in'`关键字确定列表中是否存在指定的项目。
```
charList =  ["a", "b", "c"]
if "a" in charList:
	print("a is present")	# a is present

if "d" in charList:
	print("d is present")
else:
	print("d is NOT present")	# d is NOT present
```
5\. Finding length of the list
------------------------------

使用该`len()`函数查找给定列表的长度。
```
charList =  ["a", "b", "c"]
x = len (charList)
print (x)	# 3
```
6\. Adding items
----------------

*   要将项目添加到列表的末尾，请使用`append(item)`方法。
*   要在特定索引位置添加项目，请使用`insert(index, item)`方法。如果`index`大于索引长度，则将项目添加到列表的末尾。
```
charList =  ["a", "b", "c"]
charList.append("d")	
charList.append("e")
print (charList)		# ['a', 'b', 'c', 'd', 'e']
charList.insert(5, "f")

print (charList)		# ['a', 'b', 'c', 'd', 'e', 'f']

charList.insert(10, "h")	# No error 

print (charList)	# ['a', 'b', 'c', 'd', 'e', 'f', 'h']
```

7\. Removing items
------------------

若要从列表中删除项目，四个途径使用一个，即`remove()`，`pop()`，`clear()`或`del`关键字。

#### 7.1. remove()

它通过其值删除指定的项目。
```
charList =  ["a", "b", "c"]
charList.remove("c")	
print (charList)		# ['a', 'b']
```
#### 7.2. pop()

它通过索引删除指定的项目。如果未提供index，它将从列表中删除最后一项。
```
charList =  ["a", "b", "c", "d"]
charList.pop()			# removes 'd' - last item
print (charList)		# ['a', 'b', 'c']
charList.pop(1)			# removes 'b'
print (charList)		# ['a', 'c']
```
#### 7.3. clear()

它清空列表。
```
charList =  ["a", "b", "c", "d"]
charList.clear()	
print (charList)		# []
```
#### 7.4. del keyword

它可以用来**从列表的索引中删除项目**。我们也可以使用它**删除整个列表**。
```
charList =  ["a", "b", "c", "d"]
del charList[0]	

print (charList)		# ['b', 'c', 'd']

del charList

print (charList)		# NameError: name 'charList' is not defined
```
8\. Join two lists
------------------

我们可以使用`"+"`运算符或`extend()`函数将两个给定的列表加入Python 。
```
charList = ["a", "b", "c"]
numList	= [1, 2, 3]

list1 = charList + numList

print (list1)	# ['a', 'b', 'c', 1, 2, 3]

charList.extend(numList)

print (charList)	# ['a', 'b', 'c', 1, 2, 3]
```
9\. Python list methods
-----------------------

#### 9.1. append()

在列表的末尾添加一个元素。
```
charList =  ["a", "b", "c"]

charList.append("d")

print (charList)	# ["a", "b", "c", "d"]
```
#### 9.2. clear()

从列表中删除所有元素。
```
charList =  ["a", "b", "c"]

charList.clear()

print (charList)	# []
```
#### 9.3. copy()

返回列表的副本。
```
charList =  ["a", "b", "c"]

newList = charList.copy()

print (newList)	# ["a", "b", "c"]
```
#### 9.4. count()

返回具有指定值的元素数。
```
charList =  ["a", "b", "c"]

x = charList.count('a')

print (x)	# 1
```
#### 9.5. extend()

将列表的元素添加到当前列表的末尾。
```
charList = ["a", "b", "c"]
numList	= [1, 2, 3]

charList.extend(numList)

print (charList)	# ['a', 'b', 'c', 1, 2, 3]
```
#### 9.6. index()

返回具有指定值的第一个元素的索引。
```
charList =  ["a", "b", "c"]

x = charList.index('a')

print (x)	# 0
```
#### 9.7. insert()

在指定位置添加元素。
```
charList =  ["a", "b", "c"]

charList.insert(3, 'd')

print (charList)	# ['a', 'b', 'c', 'd']
```
#### 9.8. pop()

删除指定位置或列表末尾的元素。
```
charList =  ["a", "b", "c", "d"]

charList.pop()			# removes 'd' - last item

print (charList)		# ['a', 'b', 'c']

charList.pop(1)			# removes 'b'

print (charList)		# ['a', 'c']
```
#### 9.9. remove()

删除具有指定值的项目。
```
charList =  ["a", "b", "c", "d"]

charList.remove('d')

print (charList)		# ['a', 'b', 'c']
```
#### 9.10. reverse()

颠倒列表中项目的顺序。
```
charList =  ["a", "b", "c", "d"]

charList.reverse()

print (charList)		# ['d', 'c', 'b', 'a']
```
#### 9.11. sort()

默认情况下，以升序对给定列表进行排序。
```
charList =  ["a", "c", "b", "d"]

charList.sort()

print (charList)		# ["a", "b", "c", "d"]
```
学习愉快！