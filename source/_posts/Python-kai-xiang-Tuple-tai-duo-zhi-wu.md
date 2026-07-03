---
title: Python开箱Tuple–太多值无法解压
id: 1371
date: 2024-10-31 22:01:52
author: daichangya
excerpt: Python示例，用于unpack元组或序列或可迭代，以便该元组可能长于N个元素，从而导致“太多的值无法unpack”异常。1.打开任意长度的元组Python“starexpressions”可用于unpack任意长度的元组。example1.py&gt;&gt;&gt;employee=('Lok
permalink: /archives/Python-kai-xiang-Tuple-tai-duo-zhi-wu/
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


Python示例，用于unpack元组或序列或可迭代，以便该元组可能长于N个元素，从而导致“ **太多的值无法unpack** ”异常。

1.打开任意长度的元组
-----------

**Python“ star expressions”可用于unpack任意长度的元组。**

```
example1.py

>>> employee = ('Lokesh', 'email@example.com', '111-222-333', '444-555-666')

>>> name, email, *phone_numbers = employee

>>> name

'Lokesh'

>>> email

'email@example.com'

>>> phone_numbers

['111-222-333', '444-555-666']

example2.py

>>> *elements, end = [1,2,3,4,5,6,7,8]

>>> elements

[1,2,3,4,5,6,7]

>>> end

8
```
2.unpack元组并丢弃不想要的值
--------------

If there is a mismatch in the number of elements, you’ll get an error.
```
example3.py

>>> record = ('Lokesh', 37, 72.45, (1, 1, 1981))

>>> name, *_, (*_, year) = record #Only read name and year

>>> name

'Lokesh'

>>> year

1981
```
学习愉快！
