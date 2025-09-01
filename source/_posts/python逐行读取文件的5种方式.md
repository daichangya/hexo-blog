---
title: Python | 逐行读取文件的5种方式
id: 1354
date: 2024-10-31 22:01:52
author: daichangya
excerpt: "在本文中，我们将讨论在Python中逐行读取文件的不同方法。假设我们在与python脚本相同的目录中有一个data.txt文件。让我们看看如何逐行阅读其内容。小型文件的解决方案：使用readlines（）获取文件中所有行的列表第一个基本且效率低下的解决方案是使用**readlines（）**函数。如"
permalink: /archives/python%E9%80%90%E8%A1%8C%E8%AF%BB%E5%8F%96%E6%96%87%E4%BB%B6%E7%9A%845%E7%A7%8D%E6%96%B9%E5%BC%8F/
categories:
 - python基础教程
---

在本文中,我们将讨论在Python中逐行读取文件的不同方法。

假设我们在与python脚本相同的目录中有一个**data.txt**文件。让我们看看如何逐行阅读其内容。

小型文件的解决方案:使用readlines()获取文件中所有行的列表
----------------------------------

第一个基本且**效率低下的解决方案**是使用**readlines()** 函数。


如果我们有一个小文件,则可以在文件处理程序上调用readlines(),它将整个文件内容读取到内存中,然后将其拆分为单独的行,并返回文件中所有行的列表。除最后一行外,列表中的所有行将在末尾包含换行符。  
例如,

```

# Open file    
fileHandler  =  open  ("data.txt",  "r")
# Get list of all lines in file
listOfLines  =  fileHandler.readlines()
# Close file
fileHandler.close()
```

它将返回文件中的行列表。我们可以遍历该列表,并剥离()新行字符,然后打印该行,即
```
# Iterate over the lines
for  line in  listOfLines:
	print(line.strip())
```

**输出:**
```
Hello
This is  a  sample
file that contains is
some text
is
like  123
```
但是,如果文件很大,则会消耗大量内存,因此,如果文件很大,最好避免使用此解决方案。

**让我们看一些有效的解决方案,**

使用readline()逐行读取文件
------------------

读取大文件时,有效的方法是逐行读取文件,而不是一次性读取所有数据。  
让我们将readline()函数与文件处理程序一起使用,即

```

lineStr  =  fileHandler.readline()
```
readline()返回文件中的下一行,该行的末尾将包含换行符。另外,如果到达文件末尾,则它将返回一个空字符串。  
现在让我们看看如何使用readline()逐行读取文件内容
```
# Open file        

fileHandler  =  open  ("data.txt",  "r")
while  True:
    # Get next line from file
    line  =  fileHandler.readline()
    # If line is empty then end of file reached
    if  not  line  :
        break;
    print(line.strip())
    # Close Close    
fileHandler.close()
```
**输出:**
```
Hello
This is  a  sample
file that contains is
some text
is
like  123
```
使用上下文管理器逐行读取文件(带块)
------------------

当我们打开文件时,我们也需要关闭它。如果我们忘记关闭,那么它将在例如对函数结尾处的文件引用的最后一个引用被破坏时自动关闭。但是,即使文件相关的工作已经完成,如果我们有一个大型功能不会很快结束该怎么办。在这种情况下,我们可以使用上下文管理器自动清除诸如文件关闭之类的内容。  
例如,
```

Hello
This is  a  sample
file that contains is
some text
is
like  123
```

在这种情况下,当控制脱离块时,文件将自动关闭。即使由于某些异常而出现阻塞。

使用上下文管理器(带块)获取文件中的行列表
---------------------

让我们遍历文件中的所有行并创建行列表,即
```
# Get the all the lines in file in a list

listOfLines  =  list()
with  open  ("data.txt",  "r")  as  myfile:
    for  line in  myfile:
        listOfLines.append(line.strip())
```

listOfLines列表的内容为
```

['Hello',  'This is a sample',  'file that contains is',  'some text',  'is',  '',  'like 123']
```

使用上下文管理器和while循环逐行读取文件的内容
-------------------------

让我们使用上下文管理器和while循环遍历文件中的各行,即
```
# Open file

with  open("data.txt",  "r")  as  fileHandler:
    # Read next line
    line  =  fileHandler.readline()
    # check line is not empty
    while  line:
         print(line.strip())
         line  =  fileHandler.readline()
```

列表的内容将是
```

Hello
This is  a  sample
file that contains is
some text
is
like  123
```
**完整的示例如下,**
```
def main():
    print("****Read all lines in file using readlines() *****")
    # Open file
    fileHandler = open("data.txt", "r")
    # Get list of all lines in file
    listOfLines = fileHandler.readlines()
    # Close file
    fileHandler.close()
    # Iterate over the lines
    for line in listOfLines:
        print(line.strip())
    print("****Read file line by line and then close it manualy *****")
    # Open file
    fileHandler = open("data.txt", "r")
    while True:
    # Get next line from file
        line = fileHandler.readline()
        # If line is empty then end of file reached
        if not line:
            break;
        print(line.strip())
    # Close Close
    fileHandler.close()
    print("****Read file line by line using with open() *****")
    # Open file
    with open("data.txt", "r") as fileHandler:
        # Read each line in loop
        for line in fileHandler:
            # As each line (except last one) will contain new line character, so strip that
            print(line.strip())
    print("****Read file line by line using with open *****")
    # Get the all the lines in file in a list
    listOfLines = list()
    with open("data.txt", "r") as myfile:
        for line in myfile:
            listOfLines.append(line.strip())
    print(listOfLines)
    print("****Read file line by line using with open() and while loop *****")
    # Open file
    with open("data.txt", "r") as fileHandler:
        # Read next line
        line = fileHandler.readline()
        # check line is not empty
        while line:
            print(line.strip())
            line = fileHandler.readline()


if __name__ == '__main__':
    main()

```
**输出:**
```
****Read all lines in file using readlines() *****
Hello
This is a sample
file that contains is
some text
is
 
like 123
****Read file line by line and then close it manualy *****
Hello
This is a sample
file that contains is
some text
is
 
like 123
****Read file line by line using with open() *****
Hello
This is a sample
file that contains is
some text
is
 
like 123
****Read file line by line using with open *****
['Hello', 'This is a sample', 'file that contains is', 'some text', 'is', '', 'like 123']
****Read file line by line using with open() and while loop *****
Hello
This is a sample
file that contains is
some text
is
 
like 123
```
