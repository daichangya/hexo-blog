---
title: Python中的变量的使用
id: 1360
date: 2024-10-31 22:01:52
author: daichangya
excerpt: 了解python中的变量，声明局部和全局变量。另外，了解python函数内部使用的全局关键字。1.创建变量1.1。简单分配Python语言没有用于声明变量的关键字。当我们首先为变量赋值时，会立即在适当位置创建一个变量。创建变量i=20blogName=&quot;howtodoinjava&quot
permalink: /archives/Python-zhong-de-bian-liang-de-shi-yong/
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


了解[python中的](https://blog.jsdiff.com/archives/python基础教程)变量，声明局部和全局变量。另外，了解python函数内部使用的全局关键字。

1.创建变量
------

#### 1.1。简单分配

Python语言**没有用于声明变量的关键字**。当我们首先为变量赋值时，会立即在适当位置创建一个变量。

创建变量
```
i = 20

blogName = "howtodoinjava"

print(i) # prints 20

print(blogName) # prints howtodoinjava
```
可以使用单引号和双引号来创建字符串类型的变量。

字符串类型
```
author = 'Lokesh'

blogName = "howtodoinjava"

print(author) # prints Lokesh

print(blogName) # prints howtodoinjava
```
#### 1.2。连续赋值

Python还允许连续赋值，这使得可以将相同的值同时分配给多个变量。

连续赋值
```
i = j = k = 20

print(i) # prints 20

print(j) # prints 20

print(k) # prints 20
```
#### 1.3。单行中的多个赋值

Python允许您在一行中将值分配给多个变量。

同时进行多个赋值
```
x, y, z = "A", "B", 100

print(x) # prints A

print(y) # prints B

print(z) # prints 100
```
#### 1.2。变量重新声明

由于变量不需要数据类型信息，因此我们可以毫无问题地重新分配任何类型的新值。在Python中，可以为变量分配一种类型的值，然后在以后重新分配其他类型的值。


重新赋值
```
index = 10

index = 20

index = "NA"

print(index) # prints NA
```
2.命名约定
------

在Python中创建变量的规则是：

*   变量名必须**以字母或下划线字符开头**。
*   变量名**不能以数字开头**。
*   变量名称**只能包含字母数字字符和下划线** (A-z, 0-9, and _ )。
*   变量**名称区分大小写**。例如，名称，名称和名称是三个不同的变量。

> **注意：** Python 3具有完整的Unicode支持，它也允许在变量名中使用Unicode字符。

3.局部变量与全局变量
-----------

#### 3.1。创建局部变量和全局变量

在函数内部创建的变量称为**局部变量**。

在函数外部创建的变量是**全局变量**。全局变量可以被函数内部和外部的每个人使用。

局部变量和全局变量
```
x = 10      # global variable

def myfunc():

y = 10    # local variable

print("Sum of x and y = " + str(x + y)) # prints Sum of x and y = 20

myfunc()

print("Sum of x and y = " + str(x + y)) # NameError: name 'y' is not defined
```
#### 3.2。局部变量限制在函数范围内

如果在函数内部创建具有相同名称的变量，则此变量将是局部变量，并且只能在函数内部使用。具有相同名称的全局变量将保持原样，并具有原始值。

局部变量在范围内
```
x = 10      # global variable

def myfunc():

x = 20    # local variable

print("x is " + str(x)) # prints x is 20

myfunc()

print("x is " + str(x)) # prints x is 10
```
#### 3.3。'global'关键字

要在函数内部创建全局变量，可以使用global关键字。

函数内部的全局变量
```
x = 10      # global variable

def myfunc():

global y

y = 10    # global variable created inside function

print("Sum of x and y = " + str(x + y)) # prints Sum of x and y = 20

myfunc()

print("Sum of x and y = " + str(x + y)) # prints Sum of x and y = 20
```
将您与python变量有关的问题交给我。

学习愉快！
