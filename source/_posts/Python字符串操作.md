---
title: Python字符串操作
id: 1363
date: 2024-10-31 22:01:52
author: daichangya
excerpt: "在Python中，string文字是：代表Unicode字符的字节数组用单引号或双引号引起来无限长度字符串文字str='helloworld'str=&quot;helloworld&quot;一个多行字符串使用三个单引号或三个双引号创建的。多行字符串文字str='''Sayhellotopytho"
permalink: /archives/python%E5%AD%97%E7%AC%A6%E4%B8%B2%E6%93%8D%E4%BD%9C/
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


在[Python中](https://blog.jsdiff.com/archives/python基础教程)，string文字是：

*   代表Unicode字符的字节数组
*   用单引号或双引号引起来
*   无限长度

字符串文字
```
str = 'hello world'

str = "hello world"
```
一个**多行字符串**使用三个单引号或三个双引号创建的。


多行字符串文字
```
str = '''Say hello

to python

programming'''

str = """Say hello

to python

programming"""
```
> Python没有字符数据类型，单个字符就是长度为1的字符串。

2\. Substring or slicing
------------------------

通过使用slice语法，我们可以获得一系列字符。索引从零开始。

str[m:n] 从位置2（包括）到5（不包括）返回字符串。

从索引2到5的子字符串
```
str = 'hello world'

print(str[2:5]) # llo
```
**负切片**将从末尾返回子字符串。


子串从索引-5到-2
```
str = 'hello world'

print(str[-5:-2])   # wor

str[-m:-n] 将字符串从位置-5（不包括）返回到-2（包括）。
```
3\. Strings as arrays
---------------------

在python中，字符串表现为数组。方括号可用于访问字符串的元素。

字符在第n个位置
```
str = 'hello world'

print(str[0])   # h

print(str[1])   # e

print(str[2])   # l

print(str[20])  # IndexError: string index out of range
```
4\. String length
-----------------

len（）函数返回字符串的长度：

字符串长度
```
str = 'hello world'

print(len(str)) # 11
```
5\. String Formatting
---------------------

要在python中格式化s字符串，请{ }在所需位置在字符串中使用占位符。将参数传递给format()函数以使用值格式化字符串。

我们可以在占位符中传递参数位置（从零开始）。

字符串格式（）
```
age = 36

name = 'Lokesh'

txt = "My name is {} and my age is {}"

print(txt.format(name, age))    # My name is Lokesh and my age is 36

txt = "My age is {1} and the name is {0}"

print(txt.format(name, age))    # My age is 36 and the name is Lokesh
```
6\. String Methods
------------------

#### 6.1. capitalize()

它返回一个字符串，其中给定字符串的第一个字符被转换为大写。当第一个字符为非字母时，它将返回相同的字符串。

字符串大写（）
```
name = 'lokesh gupta'

print( name.capitalize() )  # Lokesh gupta

txt = '38 yrs old lokesh gupta'

print( txt.capitalize() )   # 38 yrs old lokesh gupta
```
#### 6.2. casefold()

它返回一个字符串，其中所有字符均为给定字符串的小写字母。

字符串casefold（）
```
txt = 'My Name is Lokesh Gupta'

print( txt.casefold() ) # my name is lokesh gupta
```
#### 6.3. center()

使用指定的字符（默认为空格）作为填充字符，使字符串居中对齐。

在给定的示例中，输出总共需要20个字符，而“ hello world”位于其中。

字符串中心
```
txt = "hello world"

x = txt.center(20)

print(x)    # '    hello world     '
```
#### 6.4. count()

它返回指定值出现在字符串中的次数。它有两种形式：
```
 count(value) - value to search for in the string.  
 count(value, start, end) - value to search for in the string, where search starts from start position till end position.
```
字符串数（）
```
txt = "hello world"

print( txt.count("o") )         # 2

print( txt.count("o", 4, 7) )   # 1
```
#### 6.5. encode()

它使用指定的编码对字符串进行编码。如果未指定编码，UTF-8将使用。

字符串encode（）
```
txt = "My name is åmber"

x = txt.encode()

print(x)    # b'My name is \xc3\xa5mber'
```
#### 6.6. [endswith()](https://howtodoinjava.com/python/string-endswith-method/)

True如果字符串以指定值结尾，则返回，否则返回False。

字符串endswith（）
```
txt = "hello world"

print( txt.endswith("world") )      # True

print( txt.endswith("planet") )     # False
```
#### 6.7. expandtabs()

它将制表符大小设置为指定的空格数。

字符串expandtabs（）
```
txt = "hello\tworld"

print( txt.expandtabs(2) )      # 'hello world'

print( txt.expandtabs(4) )      # 'hello   world'

print( txt.expandtabs(16) )     # 'hello           world'
```
#### 6.8. find()

它查找指定值的第一次出现。-1如果字符串中没有指定的值，它将返回。

find()与index()方法相同，唯一的区别是，index()如果找不到该值，该方法将引发异常。

字符串find（）
```
txt = "My name is Lokesh Gupta"

x = txt.find("e")

print(x)        # 6
```
#### 6.9. format()

它格式化指定的字符串，并在字符串的占位符内插入参数值。

字符串格式（）
```
age = 36

name = 'Lokesh'

txt = "My name is {} and my age is {}"

print( txt.format(name, age) )  # My name is Lokesh and my age is 36
```
#### 6.10. format\_map()

它用于返回字典键的值，以格式化带有命名占位符的字符串。

字符串format\_map（）
```
params = {'name':'Lokesh Gupta', 'age':'38'}

txt = "My name is {name} and age is {age}"

x = txt.format_map(params)

print(x)        # My name is Lokesh Gupta and age is 38
```
#### 6.11. index()

*   它在给定的字符串中查找指定值的第一次出现。
*   如果找不到要搜索的值，则会引发异常。

字符串index（）
```
txt = "My name is Lokesh Gupta"

x = txt.index("e")

print(x)        # 6

x = txt.index("z")  # ValueError: substring not found
```
#### 6.12. isalnum()

它检查字母数字字符串。True如果所有字符都是字母数字，即字母(a-zA-Z)和数字，它将返回(0-9)。

字符串isalnum（）
```
print("LokeshGupta".isalnum())      # True

print("Lokesh Gupta".isalnum())     # False - Contains space
```
#### 6.13. isalpha()

True如果所有字符都是字母，则返回它，即字母(a-zA-Z)。

字符串isalpha（）
```
print("LokeshGupta".isalpha())          # True

print("Lokesh Gupta".isalpha())         # False - Contains space

print("LokeshGupta38".isalpha())        # False - Contains numbers
```
#### 6.14. isdecimal()

如果所有字符均为小数（0-9），则返回代码。否则返回False。

字符串isdecimal（）
```
print("LokeshGupta".isdecimal())    # False

print("12345".isdecimal())          # True

print("123.45".isdecimal())         # False - Contains 'point'

print("1234 5678".isdecimal())      # False - Contains space
```
#### 6.15. isdigit()

True如果所有字符都是数字，则返回，否则返回False。指数也被认为是数字。

字符串isdigit（）
```
print("LokeshGupta".isdigit())      # False

print("12345".isdigit())            # True

print("123.45".isdigit())           # False - contains decimal point

print("1234\u00B2".isdigit())       # True - unicode for square 2
```
#### 6.16. isidentifier()

True如果字符串是有效的标识符，则返回，否则返回False。

有效的标识符仅包含字母数字字母(a-z)和(0-9)或下划线( _ )。它不能以数字开头或包含任何空格。

字符串isidentifier（）
```
print( "Lokesh_Gupta_38".isidentifier() )       # True

print( "38_Lokesh_Gupta".isidentifier() )       # False - Start with number

print( "_Lokesh_Gupta".isidentifier() )         # True

print( "Lokesh Gupta 38".isidentifier() )       # False - Contain spaces
```
#### 6.17. islower()

True如果所有字符均小写，则返回，否则返回False。不检查数字，符号和空格，仅检查字母字符。

字符串islower（）
```
print( "LokeshGupta".islower() )        # False

print( "lokeshgupta".islower() )        # True

print( "lokesh_gupta".islower() )       # True

print( "lokesh_gupta_38".islower() )    # True
```
#### 6.18. isnumeric()

True如果所有字符都是数字（0-9），则it方法返回，否则返回False。指数也被认为是数值。

字符串isnumeric（）
```
print("LokeshGupta".isnumeric())    # False

print("12345".isnumeric())          # True

print("123.45".isnumeric())         # False - contains decimal point

print("1234\u00B2".isnumeric())     # True - unicode for square 2
```
#### 6.19. isprintable()

它返回True，如果所有字符都打印，否则返回False。不可打印字符用于指示某些格式化操作，例如：

*   空白（被视为不可见的图形）
*   回车
*   标签
*   换行
*   分页符
*   空字符

字符串isprintable（）
```
print("LokeshGupta".isprintable())      # True

print("Lokesh Gupta".isprintable())     # True

print("Lokesh\tGupta".isprintable())    # False
```
#### 6.20. isspace()

True如果字符串中的所有字符都是空格，则返回，否则返回False。

#### 6.21. istitle()

它返回True如果文本的所有单词以大写字母开头，字的其余均为小写字母，即标题案例。否则False。

字符串istitle（）
```
print("Lokesh Gupta".istitle())     # True

print("Lokesh gupta".istitle())     # False
```
#### 6.22. isupper()

True如果所有字符均大写，则返回，否则返回False。不检查数字，符号和空格，仅检查字母字符。

字符串isupper（）
```
print("LOKESHGUPTA".isupper())      # True

print("LOKESH GUPTA".isupper())     # True

print("Lokesh Gupta".isupper())     # False
```
#### 6.23. join()

它以可迭代方式获取所有项目，并使用强制性指定的分隔符将它们连接为一个字符串。

字符串join（）
```
myTuple = ("Lokesh", "Gupta", "38")

x = "#".join(myTuple)

print(x)    # Lokesh#Gupta#38
```
#### 6.24. ljust()

此方法将使用指定的字符（默认为空格）作为填充字符使字符串左对齐。

字符串ljust（）
```
txt = "lokesh"

x = txt.ljust(20, "-")

print(x)    # lokesh--------------
```
#### 6.25. lower()

它返回一个字符串，其中所有字符均为小写。符号和数字将被忽略。

字符串lower（）
```
txt = "Lokesh Gupta"

x = txt.lower()

print(x)    # lokesh gupta
```
#### 6.26. lstrip()

它删除所有前导字符（默认为空格）。

字符串lstrip（）
```
txt = "#Lokesh Gupta"

x = txt.lstrip("#_,.")

print(x)    # Lokesh Gupta
```
#### 6.27. maketrans()

它创建一个字符到其转换/替换的一对一映射。当在translate()方法中使用时，此翻译映射随后用于将字符替换为其映射的字符。

字符串maketrans（）
```
dict = {"a": "123", "b": "456", "c": "789"}

string = "abc"

print(string.maketrans(dict))   # {97: '123', 98: '456', 99: '789'}
```
#### 6.28. partition()

它在给定的文本中搜索指定的字符串，并将该字符串拆分为包含三个元素的元组：

*   第一个元素包含指定字符串之前的部分。
*   第二个元素包含指定的字符串。
*   第三个元素包含字符串后面的部分。

字符串partition（）
```
txt = "my name is lokesh gupta"

x = txt.partition("lokesh")

print(x)    # ('my name is ', 'lokesh', ' gupta')

print(x[0]) # my name is

print(x[1]) # lokesh

print(x[2]) #  gupta
```
#### 6.29. replace()

它将指定的短语替换为另一个指定的短语。它有两种形式：

*   string.replace(oldvalue, newvalue)
*   string.replace(oldvalue, newvalue, count)–“计数”指定要替换的出现次数。默认为所有事件。

字符串replace（）
```
txt = "A A A A A"

x = txt.replace("A", "B")

print(x)    # B B B B B

x = txt.replace("A", "B", 2)

print(x)    # B B A A A
```
#### 6.30. rfind()

它查找指定值的最后一次出现。-1如果在给定的文本中找不到该值，则返回该值。

字符串rfind（）
```
txt = "my name is lokesh gupta"

x = txt.rfind("lokesh")    

print(x)        # 11

x = txt.rfind("amit")      

print(x)        # -1
```
#### 6.31. rindex()

它查找指定值的最后一次出现，如果找不到该值，则引发异常。

字符串rindex（）
```
txt = "my name is lokesh gupta"

x = txt.rindex("lokesh")       

print(x)                # 11

x = txt.rindex("amit")  # ValueError: substring not found
```
#### 6.32. rjust()

它将使用指定的字符（默认为空格）作为填充字符来右对齐字符串。

字符串rjust（）
```
txt = "lokesh"

x = txt.rjust(20,"#")

print(x, "is my name")  # ##############lokesh is my name
```
#### 6.33. rpartition()

它搜索指定字符串的最后一次出现，并将该字符串拆分为包含三个元素的元组。

*   第一个元素包含指定字符串之前的部分。
*   第二个元素包含指定的字符串。
*   第三个元素包含字符串后面的部分。

字符串rpartition（）
```
txt = "my name is lokesh gupta"

x = txt.rpartition("lokesh")

print(x)    # ('my name is ', 'lokesh', ' gupta')

print(x[0]) # my name is

print(x[1]) # lokesh

print(x[2]) #  gupta
```
#### 6.34. rsplit()

它将字符串从右开始拆分为一个列表。

字符串rsplit（）
```
txt = "apple, banana, cherry"

x = txt.rsplit(", ")

print(x)    # ['apple', 'banana', 'cherry']
```
#### 6.35. rstrip()

它删除所有结尾字符（字符串末尾的字符），空格是默认的结尾字符。

字符串rstrip（）
```
txt = "     lokesh     "

x = txt.rstrip()

print(x)    # '     lokesh'
```
#### 6.36. [split()](https://howtodoinjava.com/python/split-string/)

它将字符串拆分为列表。您可以指定分隔符。默认分隔符为空格。

字符串split（）
```
txt = "my name is lokesh"

x = txt.split()

print(x)    # ['my', 'name', 'is', 'lokesh']
```
#### 6.37. splitlines()

通过在换行符处进行拆分，它将字符串拆分为列表。

字符串splitlines（）
```
txt = "my name\nis lokesh"

x = txt.splitlines()

print(x)    # ['my name', 'is lokesh']
```
#### 6.38. [startswith()](https://howtodoinjava.com/python/string-startswith/)

True如果字符串以指定值开头，则返回，否则返回False。字符串比较区分大小写。

字符串startswith（）
```
txt = "my name is lokesh"

print( txt.startswith("my") )   # True

print( txt.startswith("My") )   # False
```
#### 6.39. strip()

它将删除所有前导（开头的空格）和结尾（结尾的空格）字符（默认为空格）。

字符串strip（）
```
txt = "   my name is lokesh   "

print( txt.strip() )    # 'my name is lokesh'
```
#### 6.40. swapcase()

它返回一个字符串，其中所有大写字母均为小写字母，反之亦然。

字符串swapcase（）
```
txt = "My Name Is Lokesh Gupta"

print( txt.swapcase() ) # mY nAME iS lOKESH gUPTA
```
#### 6.41. title()

它返回一个字符串，其中每个单词的第一个字符均为大写。如果单词开头包含数字或符号，则其后的第一个字母将转换为大写字母。

字符串标题（）
```
print( "lokesh gupta".title() ) # Lokesh Gupta

print( "38lokesh gupta".title() )   # 38Lokesh Gupta

print( "1. lokesh gupta".title() )  # Lokesh Gupta
```
#### 6.42. translate()

它需要转换表来根据映射表替换/翻译给定字符串中的字符。

字符串translate（）
```
translation = {97: None, 98: None, 99: 105}

string = "abcdef"  

print( string.translate(translation) )  # idef
```
#### 6.43. upper()

它返回一个字符串，其中所有字符均为大写。符号和数字将被忽略。

字符串upper（）
```
txt = "lokesh gupta"

print( txt.upper() )    # LOKESH GUPTA
```
#### 6.44. zfill()

它在字符串的开头添加零（0），直到达到指定的长度。

字符串zfill（）
```
txt = "100"

x = txt.zfill(10)

print( 0000000100 ) # 0000000100
```
学习愉快！
