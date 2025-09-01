---
title: Python目录和文件管理
id: 1441
date: 2024-10-31 22:01:56
author: daichangya
permalink: /archives/Python-mu-lu-he-wen-jian-guan-li/
categories:
- python基础教程
---

Python目录和文件管理
=============

在本教程中，您将学习Python中的文件和目录管理，即创建目录，重命名，列出所有目录以及使用它们。


Python目录
--------

如果我们的Python程序中有大量文件要处理，我们可以将代码安排在不同的目录中，以使事情更易于管理。

目录或文件夹是文件和子目录的集合。Python的`os` [模块]为我们提供了许多使用目录（和文件）的有用方法。

* * *

获取当前目录
------

我们可以使用模块的`getcwd()`方法来获得当前的工作目录`os`。

此方法以字符串形式返回当前工作目录。我们还可以使用该`getcwdb()`方法将其作为字节对象获取。

    >>> import os
    
    >>> os.getcwd()
    'C:\\Program Files\\PyScripter'
    
    >>> os.getcwdb()
    b'C:\\Program Files\\PyScripter'

多余的反斜杠表示转义序列。该`print()`函数将正确渲染此图像。

    >>> print(os.getcwd())
    C:\Program Files\PyScripter

* * *

变更目录
----

我们可以使用`chdir()`方法更改当前工作目录。

我们要更改为的新路径必须作为字符串提供给此方法。我们可以使用正斜杠`/`或反斜杠`\`来分隔路径元素。

使用反斜杠时，使用转义序列更安全。

    >>> os.chdir('C:\\Python33')
    
    >>> print(os.getcwd())
    C:\Python33

* * *

列出目录和文件
-------

使用该`listdir()`方法可以检索目录中的所有文件和子目录。


此方法采用一个路径，并返回该路径中的子目录和文件的列表。如果未指定路径，它将返回当前工作目录中的子目录和文件列表。

    >>> print(os.getcwd())
    C:\Python33
    
    >>> os.listdir()
    ['DLLs',
    'Doc',
    'include',
    'Lib',
    'libs',
    'LICENSE.txt',
    'NEWS.txt',
    'python.exe',
    'pythonw.exe',
    'README.txt',
    'Scripts',
    'tcl',
    'Tools']
    
    >>> os.listdir('G:\\')
    ['$RECYCLE.BIN',
    'Movies',
    'Music',
    'Photos',
    'Series',
    'System Volume Information']

* * *

制作新目录
-----

我们可以使用该`mkdir()`方法创建一个新目录。

此方法采用新目录的路径。如果未指定完整路径，则会在当前工作目录中创建新目录。

    >>> os.mkdir('test')
    
    >>> os.listdir()
    ['test']

* * *

重命名目录或文件
--------

该`rename()`方法可以重命名目录或文件。

为了重命名任何目录或文件，该`rename()`方法采用两个基本参数：旧名称作为第一个参数，新名称作为第二个参数。

    >>> os.listdir()
    ['test']
    
    >>> os.rename('test','new_one')
    
    >>> os.listdir()
    ['new_one']

* * *

删除目录或文件
-------

可以使用`remove()`方法删除（删除）文件。

同样，该`rmdir()`方法将删除一个空目录。

    >>> os.listdir()
    ['new_one', 'old.txt']
    
    >>> os.remove('old.txt')
    >>> os.listdir()
    ['new_one']
    
    >>> os.rmdir('new_one')
    >>> os.listdir()
    []

**注意**：该`rmdir()`方法只能删除空目录。

为了删除一个非空目录，我们可以`rmtree()`在`shutil`模块内部使用该方法。

    >>> os.listdir()
    ['test']
    
    >>> os.rmdir('test')
    Traceback (most recent call last):
    ...
    OSError: [WinError 145] The directory is not empty: 'test'
    
    >>> import shutil
    
    >>> shutil.rmtree('test')
    >>> os.listdir()
    []
    
变量文件夹下的所有文件
-------

可以使用`walk()`方法遍历所有文件。

该函数返回生成器对象，已从该生成器对象获取给定文件层次结构的每个目录的元组。

每个元组包含三个项目：

1.  当前目录的地址。这是一个字符串。
2.  此目录的第一级子目录的名称。类型是一个列表。
3.  此目录（列表）的文件名。

这是目录树的示例：

![目录树](https://pythoner.name/sites/default/files/inline-images/tree_for_walk.png)

让我们传递os.walk（）函数的“ test”目录：

    >>> for i in os.walk('/home/pl/test'):
    ...     print(i)
    ... 
    ('/home/pl/test', ['cgi-bin'], ['dgs.png', 'index.html'])
    ('/home/pl/test/cgi-bin', ['backup', 'another'], ['hello.py'])
    ('/home/pl/test/cgi-bin/backup', [], [])
    ('/home/pl/test/cgi-bin/another', [], ['data.txt'])