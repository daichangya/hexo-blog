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

[Python](https://www.tushu.info/archives/Python-ji-chu-jiao-cheng)支持编写简单的单行注释以及多行注释。


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
