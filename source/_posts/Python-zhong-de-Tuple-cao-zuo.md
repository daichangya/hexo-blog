---
title: Python中的Tuple操作
id: 1365
date: 2024-10-31 22:01:52
author: daichangya
excerpt: 在Pyhton中，元组类似于不变，list但不可变，并带有可选的圆括号。元组是：不可变有序异质索引（从零开始）带圆括号（可选，但建议）在迭代过程中更快，因为它是不可变的元组对于创建通常包含相关信息（例如员工信息）的对象很有用。换句话说，元组可以让我们将相关信息“块”在一起，并将其用作单个事物。1.C
permalink: /archives/Python-zhong-de-Tuple-cao-zuo/
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


在[Pyhton中](https://blog.jsdiff.com/archives/python基础教程)，**元组**类似于**不变**，list但**不可变**，并带有可选的**圆括号**。

元组是：


*   不可变
*   有序
*   异质
*   索引（从零开始）
*   带圆括号（可选，但建议）
*   在迭代过程中更快，因为它是不可变的

元组**对于创建**通常包含相关信息（例如员工信息）的**对象**很有用。换句话说，元组可以让我们将相关信息“块”在一起，并将其用作单个事物。

1\. Creating a Tuple
--------------------

元组中的元素用圆括号括起来，并用逗号分隔。元组可以包含任意数量的不同类型的项。

句法
```
Tuple = (item1, item2, item3)
```
元组的例子
```
tuple1 = () # empty tuple

tuple2 = (1, "2", 3.0)

tuple3 = 1, "2", 3.0
```
#### 1.1. Tuple with one element

如果元组仅包含一个元素，则不将其视为元组。它应该以逗号结尾以指定解释器为元组。

元组的例子
```
tupleWithOneElement = ("hello", ) # Notice trailing comma
```
#### 1.2. Nested Tuple

一个包含另一个元组作为元素的元组，称为嵌套元组。


嵌套元组
```
nestedTuple = ("hello", ("python", "world"))
```
2\. Accessing Tuple Items
-------------------------

我们可以使用方括号内的索引访问元组项。

*   **正索引**从元组的开始开始计数。
*   **负索引**从元组的末尾开始计数。
*   一定**范围的索引**将使用指定的项目创建一个新的元组（称为**Slicing**）。
*   范围[m:n]是指从位置m（_含_）到位置n（_不含_）。
*   使用**双索引**访问嵌套元组的元素。

存取项目
```
Tuple = ("a", "b", "c", "d", "e", "f")

print(Tuple[0]) # a

print(Tuple[1]) # b

print(Tuple[-1]) # f

print(Tuple[-2]) # e

print(Tuple[0:3]) # ('a', 'b', 'c')

print(Tuple[-3:-1]) # ('d', 'e')

Tuple = ("a", "b", "c", ("d", "e", "f"))

print(Tuple[3]) # ('d', 'e', 'f')

print(Tuple[3][0]) # d

print(Tuple[3][0:2]) # ('d', 'e')
```
3\. Loop into tuple
-------------------

使用**for循环**遍历元组项。

对于循环示例
```
Tuple = ("a", "b", "c")

for x in Tuple:

print(x)
```
4\. Check if an item exist in tuple
-----------------------------------

要检查一个元组是否包含给定的元素，我们可以使用'in'关键词和'not in'关键词。

检查项目是否存在于元组中
```
Tuple = ("a", "b", "c", "d", "e", "f")

if "a" in Tuple:

print("Yes, 'a' is present") # Yes, 'a' is present

if "p" not in Tuple:

print("No, 'p' is not present") # No, 'p' is not present
```
5\. Sorting a Tuple
-------------------

使用语言内置sorted()方法对元组内的元素进行排序。

排序元组
```
Tuple = ("a", "c", "b", "d", "f", "e")

sortedTuple = sorted(Tuple)

print (sortedTuple) # ("a", "b", "c", "d", "e", "f")
```
6\. Repetition and Concatenation of Tuples
------------------------------------------

要重复元组的所有元素，请将其乘以所需因子N。

重复
```
Tuple = ("a", "b")

repeatedTuple = Tuple * 3

print (repeatedTuple) # ('a', 'b', 'a', 'b', 'a', 'b')
```
要连接/连接两个或多个元组，我们可以使用+运算符。

级联
```
Tuple1 = ("a", "b", "c")

Tuple2 = ("d", "e", "f")

joinedTuple = Tuple1 + Tuple2

print (joinedTuple) # ("a", "b", "c", "d", "e", "f")
```
7\. Packing and Unpacking the Tuple
-----------------------------------

**打包** 是指我们为变量分配一组值的操作。在打包时，元组中的所有项目都分配给一个元组对象。

在下面的示例中，所有三个值都分配给了variable Tuple。

Packing
```
Tuple = ("a", "b", "c")
```
**拆包** 称为将元组变量分配给另一个元组，并将元组中的各个项目分配给各个变量的操作。

在给定的示例中，元组被解包为新的元组，并且将值"a", "b" and "c"–分配给了变量x, y and z

Unpacking
```
Tuple = ("a", "b", "c") # Packing

(x, y, z) = Tuple

print (x) # a

print (y) # b

print (z) # c
```
在解包期间，分配左侧的元组中的元素数必须等于右侧的数量。

Unpacking errors
```
Tuple = ("a", "b", "c") # Packing

(x, y, z) = Tuple       # ValueError: too many values to unpack (expected 2)

(x, y, z, i) =  Tuple   # ValueError: not enough values to unpack (expected 4, got 3)
```
8\. Named tuples
----------------

Python提供了一种来自模块的特殊类型的函数，名为**namedtuple（）**collection。

命名元组类似于字典，但是支持从值和键进行访问，其中字典仅支持按键访问。

命名元组示例
```
import collections

Record = collections.namedtuple('Record', ['id', 'name', 'date'])

R1 = Record('1', 'My Record', '12/12/2020')

#Accessing using index

print("Record id is:", R1[0]) # Record id is: 1

# Accessing using key  

print("Record name is:", R1.name) # Record name is: My Record
```
9\. Python Tuples Methods
-------------------------

#### 9.1. any()

返回True如果至少一个元素存在于元组，并返回False如果元组是空的。
```
print( any( () ) ) # Empty tuple - False

print( any( (1,) ) ) # One element tuple - True

print( any( (1, 2) ) ) # Regular tuple - True
```
#### 9.2. min()

返回元组的最小元素（整数）。
```
Tuple = (4, 1, 2, 6, 9)

print( min( Tuple ) ) # 1
```
#### 9.3. max()

返回元组的最大元素（整数）。
```
Tuple = (4, 1, 2, 6, 9)

print( max( Tuple ) ) # 9
```
#### 9.4. len()

返回元组的长度。
```
Tuple = (4, 1, 2, 6, 9)

print( len( Tuple ) ) # 5
```
#### 9.5. sum()

返回元组的所有元素（整数）的总和。
```
Tuple = (4, 1, 2, 6, 9)

print( sum( Tuple ) ) # 22
```
10\. Conclusion
---------------

如上所述，元组不可变，有序和索引的异构元素集合。它写有或没有圆括号。

元组对于创建对象类型和实例非常有用。

元组支持类似于[list](https://blog.jsdiff.com/archives/python%E4%B8%AD%E7%9A%84list%E6%93%8D%E4%BD%9C/)类型的操作，只有我们不能更改元组元素。

学习愉快！
