---
title: Python中的数据类型
id: 1361
date: 2024-10-31 22:01:52
author: daichangya
excerpt: "数据类型定义变量的类型。由于所有内容都是Python中的对象，因此数据类型实际上是类。变量是类的实例。在任何编程语言中，可以对不同类型的数据类型执行不同的操作，其中某些数据类型与其他数据类型相同，而某些数据类型非常特定于该特定数据类型。1.Python中的内置数据类型Python默认具有以下内置数据"
permalink: /archives/python%E4%B8%AD%E7%9A%84%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B/
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


数据类型定义变量的类型。由于所有内容都是[Python中](https://blog.jsdiff.com/archives/python基础教程)的对象，因此**数据类型**实际上是类。变量是类的实例。

在任何编程语言中，可以对不同类型的数据类型执行不同的操作，其中某些数据类型与其他数据类型相同，而某些数据类型非常特定于该特定数据类型。


1\. Python中的内置数据类型
------------------

Python默认具有以下内置数据类型。

| Category    | Data types / Class names     |
|-------------|------------------------------|
| Text/String | str                          |
| Numeric     | int, float, complex          |
| List        | list, tuple, range           |
| Map         | dict                         |
| Set         | set, frozenset               |
| Boolean     | bool                         |
| Binary      | bytes, bytearray, memoryview |


2.详细的数据类型
---------

#### 2.1。字符串

字符串可以定义为用单引号，双引号或三引号引起来的字符序列。三引号（“””）可用于编写多行字符串。

```
x = 'A'

y = "B"

z = """

C

"""

print(x) # prints A

print(y) # prints B

print(z) # prints C

print(x + y) # prints AB - concatenation

print(x*2) # prints AA - repeatition operator

name = str('john') # Constructor

sumOfItems = str(100) # type conversion from int to string
```
#### 2.2。整数，浮点数，复数

这些是数字类型。

*   int 保留长度不受限制的带符号整数。
*   float 保留浮点精度数字，并且它们的精度最高为15个小数位。
*   complex –复数包含实部和虚部。

```
x = 2                   # int

x = int(2) # int  

x = 2.5                 # float

x = float(2.5) # float

x = 100+3j              # complex

x = complex(100+3j) # complex
```
#### 2.3。list，tuple

在Python中，**list**是一些数据的**有序序列**。列表可以**包含不同类型的数据**。

**[:]运算符**可用于访问列表中的数据。

list可以使用 **(+)** 和 **(*)** 运算符 。

**tuple**是类似list的-除了tuple是一个只读的数据结构，我们不能修改一个tuple的中的数据。另外，项目用括号括起来(, )。

```
randomList = [1, "one", 2, "two"]

print (randomList); # prints [1, 'one', 2, 'two']

print (randomList + randomList); # prints [1, 'one', 2, 'two', 1, 'one', 2, 'two']

print (randomList * 2); # prints [1, 'one', 2, 'two', 1, 'one', 2, 'two']

alphabets = ["a", "b", "c", "d", "e", "f", "g", "h"] 

print (alphabets[3:]); # range - prints ['d', 'e', 'f', 'g', 'h']

print (alphabets[0:2]); # range - prints ['a', 'b']

randomTuple = (1, "one", 2, "two")

print (randomTuple[0:2]); # range - prints (1, 'one')

randomTuple[0] = 0      # TypeError: 'tuple' object does not support item assignment
```
#### 2.4。dict

**dict**是**键值对**的**有序集合**。键可以保存任何原始数据类型，而值是任意的Python对象。

字典中的条目用逗号分隔并括在花括号中{, }。

```
charsMap = {1:'a', 2:'b', 3:'c', 4:'d'};  

print (charsMap); # prints {1: 'a', 2: 'b', 3: 'c', 4: 'd'}

print("1st entry is " + charsMap[1]); # prints 1st entry is a

print (charsMap.keys()); # prints dict_keys([1, 2, 3, 4])

print (charsMap.values()); # prints dict_values(['a', 'b', 'c', 'd'])
```
#### 2.5。set，frozenset

python中的**set**可以定义为花括号中包含的各种项目的**无序集合**{, }。

集合中的元素**不能重复**。python set的元素**必须是不可变的**。

不同于list，没有index。这意味着我们只能循环访问的元素set。

**frozen sets**是set的不变形式。这意味着我们无法删除任何项目或将其添加到冻结集中。

```
digits = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}  

print(digits) # prints {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

print(type(digits)) # prints <class 'set'>

print("looping through the set elements ... ") 

for i in digits: 

print(i) # prints 0 1 2 3 4 5 6 7 8 9 in new lines

digits.remove(0) # allowed in normal set

print(digits) # {1, 2, 3, 4, 5, 6, 7, 8, 9}

frozenSetOfDigits = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9})  

frozenSetOfDigits.remove(0) # AttributeError: 'frozenset' object has no attribute 'remove'
```
#### 2.6。bool

**bool**值是两个恒定的对象False和True。在数字上下文中，它们的行为分别类似于整数0和1。
```
x = True

y = False

print(x) #True

print(y) #False

print(bool(1)) #True

print(bool(0)) #False
```
#### 2.7。bytes, bytearray, memoryview

**bytes**和**bytearray**用于处理二进制数据。所述**memoryview**使用缓冲协议来访问其他二进制对象的存储器，而无需进行复制。

字节对象是单个字节的**不可变**序列。仅在处理与ASCII兼容的数据时，才应使用它们。

bytes文字的语法与string的语法相同，只是'b'添加了前缀。

bytearray对象总是通过调用构造函数来创建的bytearray()。这些是**可变的**对象。

```
x = b'char_data'

y = bytearray(5)

z = memoryview(bytes(5))

print(x) # b'char_data'

print(y) # bytearray(b'\x00\x00\x00\x00\x00')

print(z) # <memory at 0x014CE328>
```
3\. type（）函数
------------

该type()函数可用于获取任何对象的数据类型。

获取类型
```
x = 5

print(type(x)) # <class 'int'>

y = 'howtodoinjava.com'

print(type(y)) # <class 'str'>
```
将您的问题留在我的评论中。

学习愉快！

参考：[Python文档](https://docs.python.org/3/library/stdtypes.html)
