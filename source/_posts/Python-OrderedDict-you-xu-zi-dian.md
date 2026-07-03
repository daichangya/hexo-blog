---
title: Python OrderedDict –有序字典
id: 1373
date: 2024-10-31 22:01:52
author: daichangya
excerpt: 一个OrderedDict维护插入顺序添加到字典中的项目。项目的顺序在迭代或序列化时也会保留。1.PythonOrderedDict示例OrderedDict是pythoncollections模块的一部分。要轻松构建OrderedDict，可以OrderedDict在collections模块中使
permalink: /archives/Python-OrderedDict-you-xu-zi-dian/
categories:
- python基础教程
---

一个**OrderedDict** **维护插入顺序**添加到字典中的项目。项目的顺序在迭代或序列化时也会保留。

1\. Python OrderedDict示例
------------------------

OrderedDict 是python collections模块的一部分。

要轻松构建OrderedDict，可以OrderedDict在collections模块中使用。
```
OrderedDictExample.py
from collections import OrderedDict
d = OrderedDict()
d['how'] = 1
d['to'] = 2
d['do'] = 3
d['in'] = 4
d['java'] = 5
for key in d:
	print(key, d[key])

('how', 1)
('to', 2)
('do', 3)
('in', 4)
('java', 5)
```
2.将OrderedDict转换为JSON
---------------------

项目的顺序在序列化为JSON时也会保留。

OrderedDict JSON示例
```
from collections import OrderedDict
import json

d = OrderedDict()
d['how'] = 1
d['to'] = 2
d['do'] = 3
d['in'] = 4
d['java'] = 5
json.dumps(d)

'{"how": 1, "to": 2, "do": 3, "in": 4, "java": 5}'
```
学习愉快！

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
