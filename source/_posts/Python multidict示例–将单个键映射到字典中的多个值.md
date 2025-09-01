---
title: Python multidict示例–将单个键映射到字典中的多个值
id: 1372
date: 2024-10-31 22:01:52
author: daichangya
excerpt: "1.什么是multidict词典&gt;在python中，“multidict”一词用于指代字典，在字典中可以将单个键映射到多个值。例如多重结构multidictWithList={'key1'[1,2,3],'key2'[4,5]}multidictWithSet={'key1'{1,2,3"
permalink: /archives/pythonmultidict%E7%A4%BA%E4%BE%8B%E5%B0%86%E5%8D%95%E4%B8%AA%E9%94%AE%E6%98%A0%E5%B0%84%E5%88%B0%E5%AD%97%E5%85%B8%E4%B8%AD%E7%9A%84%E5%A4%9A%E4%B8%AA%E5%80%BC/
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


1.什么是multidict词典>
-----------------

在python中，“ **multidict** ”一词用于指代字典，在字典中可以将**单个键**映射**到多个值**。例如

多重结构
```
multidictWithList = {

'key1' : [1, 2, 3],

'key2' : [4, 5]

}

multidictWithSet = {

'key1' : {1, 2, 3},

'key2' : {4, 5}

}
```
1\. list如果要保留项目的插入顺序，请使用。  
2\. set如果要消除重复项（并且不关心顺序），请使用a 。

2\. Multidict词典示例
-----------------

要轻松构建此类词典，可以defaultdict在collections模块中使用。的功能defaultdict是它会自动初始化第一个值，因此您只需关注添加项目即可。

```
multidict.py

from collections import defaultdict

d1 = defaultdict(list) #list backed multidict

d1['key1'].append(1)

d1['key1'].append(2)

d1['key1'].append(3)

d1['key2'].append(4)

d1['key2'].append(5)

d2 = defaultdict(set) #set backed multidict

d2['key1'].add(1)

d2['key1'].add(2)

d2['key1'].add(3)

d2['key2'].add(4)

d2['key2'].add(5)

>>> d1

defaultdict(<type 'list'>, {'key2': [4, 5], 'key1': [1, 2, 3]})

>>> d1['key1']

[1, 2, 3]

>>> d2

defaultdict(<type 'set'>, {'key2': set([4, 5]), 'key1': set([1, 2, 3])})

>>> d2['key1']

set([1, 2, 3])
```
学习愉快！
