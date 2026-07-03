---
title: Python max（）和min（）–在列表或数组中查找最大值和最小值
id: 1366
date: 2024-10-31 22:01:52
author: daichangya
excerpt: 使用**max（）和min（）**方法在可比较元素的集合（例如列表，集合或数组）中查找最大（或最小）项的Python示例。1.Pythonmax()functionmax()该功能用于–计算在其参数中传递的最大值。如果字符串作为参数传递，则在字典上的最大值。1.1.Findlargestintege
permalink: /archives/Python-max-he-min-zai-lie-biao-huo-shu/
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


使用**max（）**和**min（）**方法在可比较元素的集合（例如列表，集合或数组）中查找最大（或最小）项的Python示例。

1\. Python max() function
-------------------------

`max()` 该功能用于–


1.  计算在其参数中传递的最大值。
2.  如果字符串作为参数传递，则在字典上的最大值。

#### 1.1. Find largest integer in array
```
>>> nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
>>> max( nums )
42		#Max value in array
```

#### 1.2. Find largest string in array
```
>>> blogName = ["how","to","do","in","java"]

>>> max( blogName )

'to'		#Largest value in array
```
#### 1.3. Find max key or value

有点复杂的结构。
```
>>> prices = {
   'how': 45.23,
   'to': 612.78,
   'do': 205.55,
   'in': 37.20,
   'java': 10.75
}

>>> max( prices.values() )
612.78

>>> max( prices.keys() ) 	#or max( prices ). Default is keys().
'to'
```
2\. Python min() function
-------------------------

此功能用于–

1.  计算在其参数中传递的最小值。
2.  如果字符串作为参数传递，则在字典上的最小值。

#### 2.1. Find lowest integer in array
```
>>> nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]

>>> min( nums )

-4		#Min value in array
```
#### 2.2. Find smallest string in array
```
>>> blogName = ["how","to","do","in","java"]

>>> min( blogName )

'do'		#Smallest value in array
```
#### 2.3. Find min key or value

有点复杂的结构。
```
>>> prices = {
   'how': 45.23,
   'to': 612.78,
   'do': 205.55,
   'in': 37.20,
   'java': 10.75
}

>>> min( prices.values() )
10.75

>>> min( prices.keys() ) 	#or min( prices ). Default is keys().
'do'
```
学习愉快！