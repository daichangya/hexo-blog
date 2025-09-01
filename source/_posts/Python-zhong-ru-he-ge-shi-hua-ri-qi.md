---
title: Python 中如何格式化日期
id: 1395
date: 2024-10-31 22:01:53
author: daichangya
excerpt: Python中如何格式化日期介绍Python附带了各种有用的对象，可以直接使用。例如日期对象就是一个例子。由于日期和时间的复杂性，日期类型很难从头开始操作。所幸，Python日期对象将日期转换成所需的字符串格式变得相当容易。日期格式化是作为程序员的你最重要的任务之一。不同地区表示日期/时间的方法各不
permalink: /archives/Python-zhong-ru-he-ge-shi-hua-ri-qi/
categories:
- python基础教程
---

## 介绍

Python 附带了各种有用的对象，可以直接使用。例如日期对象就是一个例子。由于日期和时间的复杂性，日期类型很难从头开始操作。所幸，Python 日期对象将日期转换成所需的字符串格式变得相当容易。

日期格式化是作为程序员的你最重要的任务之一。不同地区表示日期/时间的方法各不相同，因此你作为程序员的一大目标是以用户可读的方式显示日期值。

例如，你可能需要用数字格式表示日期值，如 “02-23-2018”。另一方面，你可能需要以更长的文本格式（如 “Feb 23,2018”）表示相同的日期。在另一种情况下，你可能希望从数字格式的日期值中提取出字符串格式的月份。

在本文中，我们将研究不同类型的日期对象及其功能。

### datetime 模块

正如你猜到的， Python 的 `datetime` 模块包含可用于处理日期和时间值的方法。要使用这个模块，我们得先通过以下 `import` 语句将其导入：

```
import datetime
```

我们可以使用 `time` 类表示时间值。时间类的属性包括小时、分钟、秒和微秒。

`time` 类的参数是可选的。尽管不指定任何参数，你将获得 0 的时间（对象），但这大多数时候不太可能是你需要的。

例如，要初始化值为 1 小时、10 分种、20 秒、13 微秒的时间对象，我们可以运行以下命令：

```
t = datetime.time(1, 10, 20, 13)
```

让我们使用 print 功能来查看时间：

```
print(t)
```

**输出：**

```
01:10:20.000013
```

你可能只需要查看小时、分钟、秒或者微秒，您可以像下边这么做：

```
print('hour:', t.hour)
```

**输出：**

```
hour: 1
```

可以按照如下方式检索上述时间（对象）的分钟、秒或者微秒:

```
print('Minutes:', t.minute)
print('Seconds:', t.second)
print('Microsecond:', t.microsecond)
```

**输出：**

```
Minutes: 10
Seconds: 20
Microseconds: 13
```

日历日期指可以通过 `date` 类表示。示例具有的属性有年、月和日。

让我们来调用 `today` 方法来查看今天的日期：

```
import datetime

today = datetime.date.today()
print(today)
```

**输出：**

```
2018-09-15
```

代码将返回今天的日期，因此你看到的输出取决于你运行脚本的日期。

现在我们调用 `ctime` 方法以另一种格式打印日期：

```
print('ctime:', today.ctime())
```

**输出：**

```
ctime: Sat Sep 15 00:00:00 2018
```

`ctime` 方法会使用比我们之前看到的示例更长的日期时间格式。此方法主要用于将 Unix 时间（从 1970 年 1 月 1 日以来的秒数）转换为字符串格式。

以下是我们如何使用 `date` 类显示年份，月份和日期：

```
print('Year:', today.year)
print('Month:', today.month)
print('Day :', today.day)
```

**输出**

```
Year: 2018

Month: 9
Day : 15
```

### 使用 strftime 将日期转换为字符串

既然你已经知道如何创建时间和日期对象，那么让我们学习如何将它们格式化为更易读的字符串。

为此，我们将使用 `strftime` 方法。这个方法可以帮助我们将日期对象转换为可读字符串。它需要两个参数，语法如下所示：

```
time.strftime(format, t)
```

第一个参数是格式字符串（以何种格式显示时间日期，感谢 [rocheers](https://github.com/rocheers) 提醒），第二个参数是格式化的时间，可选值。

这个方法也可以在 `datetime` 对象上直接调用。如以下示例所示：

```
import datetime

x = datetime.datetime(2018, 9, 15)

print(x.strftime("%b %d %Y %H:%M:%S"))
```

**输出：**

```
Sep 15 2018 00:00:00
```

我们使用以下字符串来格式化日期:

*   `%b`: 返回月份名称的前三个字符。在我们的例子中，它返回 "Sep"。
*   `%d`: 返回本月的日期，从 1 到 31。在我们的例子中，它返回 "15"。
*   `%Y`: 返回四位数格式的年份。在我们的例子中，它返回 "2018"。
*   `%H`: 返回小时。在我们的例子中，它返回 "00"。
*   `%M`: 返回分钟，从 00 到 59。在我们的例子中，它返回 "00"。
*   `%S`: 返回秒，从 00 到 59。在我们的例子中，它返回 "00"。

我们没有时间（对象），因此时间值都是 "00"。下面的例子显示了如何格式化时间：

```
import datetime

x = datetime.datetime(2018, 9, 15, 12, 45, 35)

print(x.strftime("%b %d %Y %H:%M:%S"))
```

**输出：**

```
Sep 15 2018 12:45:35
```

#### 完整的字符代码列表

除了上面给出的字符串外，`strftime` 方法还使用了其他几个指令来格式化日期值：

*   `%a`: 返回工作日的前三个字符，例如 Wed。
*   `%A`: 返回返回工作日的全名，例如 Wednesday。
*   `%B`: 返回月份的全名，例如 September。
*   `%w`: 返回工作日作为数字，从 0 到 6，周日为 0。
*   `%m`: 将月份作为数字返回，从 01 到 12。
*   `%p`: 返回 AM/PM 标识。
*   `%y`: 返回两位数格式的年份，例如，”18“ 而不是 ”2018“。
*   `%f`: 返回从 000000 到 999999 的微秒。
*   `%Z`: 返回时区。
*   `%z`: 返回 UTC 偏移量。
*   `%j`: 返回当年的日期编号，从 001 到 366。
*   `%W`: 返回年份的周数，从 00 到 53。星期一被记为一周第一天。
*   `%U`: 返回年份的周数，从 00 到 53。星期日被记为一周第一天。
*   `%c`: 返回本地日期和时间版本。
*   `%x`: 返回本地日期版本。
*   `%X`: 返回本地时间版本。

---

**译者备注：原文中的是 weekday，在查了一些资料后翻译成 “工作日”，但是考虑以下示例：**

```python
from datetime import datetime
x  = datetime.now()
x.strftime("%A")
```
**输出：**

```
'Sunday'
```

----

请考虑以下示例：

```
import datetime

x = datetime.datetime(2018, 9, 15)

print(x.strftime('%b/%d/%Y'))
```

**输出：**

```
Sep/15/2018
```

以下是你只获取月份的方法：

```
print(x.strftime('%B'))
```

**输出：**

```
September
```

让我们只展示年份：

```
print(x.strftime('%Y'))
```

**输出：**

```
2018
```

在这个例子中，我们使用了格式化代码 `%Y`。请注意，它的 Y 是大写的，现在使用小写写：

```
print(x.strftime('%y'))
```

**输出：**

```
18 
```

这次省略了年份中前两位数字。如你所见，使用这些格式化代码，你可以用你想要的任何方式表示日期时间。

### 使用 strptime 将字符串转换成日期

`strftime` 方法帮助我们将日期对象转换为可读的字符串，`strptime` 恰恰相反。它作用于字符串，并将它们转换成 Python 可以理解的日期对象。

这是这个方法的语法：

```
datetime.strptime(string, format)
```

`string` 参数是我们转换成日期格式的字符串值。`format` 参数是指定转换后日期采用的格式的指令。

例如，如果我们需要将字符串 “9/15/18” 转换成 `datetime` 对象。

我们先导入 `datetime` 模块，我们将使用 `from` 关键字以便能够在没有点格式的情况下引用模块中特定的函数：

```
from datetime import datetime
```

然后我们可以用字符串形式定义日期：

```
str = '9/15/18'
```

在将字符串转换为实际的 `datetime` 对象之前，Python 无法将上述字符串理解为日期时间。我们可以通过调用 `strptime` 方法成功完成：

执行以下命令转换字符串：

```
date_object = datetime.strptime(str, '%m/%d/%y')
```

现在让我们调用 `print` 函数用 `datetime` 格式显示字符串：

```
print(date_object)
```

**输出：**

```
2018-09-15 00:00:00
```

如你所见，转换成功！

你可以看到正斜杠 “/” 用于分隔字符串的各个元素。这告诉 `strptime` 方法我们的日期是什么格式，我们的例子中是用 "/" 作为分隔符。

但是，如果月/日/年被 "-" 分隔怎么办？你应该这么处理：

```
from datetime import datetime

str = '9-15-18'
date_object = datetime.strptime(str, '%m-%d-%y')

print(date_object)
```

**输出：**

```
2018-09-15 00:00:00
```

再一次，多亏了格式说明符，`strptime` 方法能够解析我们的日期并将其转换为日期对象。

### 结论

在本文中，我们研究了如何在 Python 中格式化日期。我们看到 Python 中的 `datetime` 模块如何操作日期和时间值。该模块包含了许多操作日期时间的类，比如，`time` 类用于表示时间值，而 `date` 类用来表示日历日期值。

学习愉快！

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
