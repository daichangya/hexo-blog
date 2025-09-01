---
title: 在Sublime Editor中配置Python环境
id: 1358
date: 2024-10-31 22:01:52
author: daichangya
excerpt: "了解如何在sublime编辑器中安装python软件包，以实现自动完成等功能，并在sublime编辑器本身中运行build。目录安装Sublime软件包控件安装软件包Python3验证Python自动完成和构建安装Sublime软件包控制首先下载用于sublime编辑器的程序包控件。转到URL：ht"
permalink: /archives/%E5%9C%A8sublimeeditor%E4%B8%AD%E9%85%8D%E7%BD%AEpython%E7%8E%AF%E5%A2%83/
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


了解如何**在sublime编辑器中安装python软件包，以**实现自动完成等功能，并在sublime编辑器本身中运行build。

目录
[安装Sublime软件包控件](#install-package-control)
[安装软件包Python 3](#install-python-package) 
[验证Python自动完成和构建](#demo)


安装Sublime软件包控制
--------------

首先下载用于sublime编辑器的程序包控件。

1.  转到URL：[https](https://packagecontrol.io/installation#st3) : [//packagecontrol.io/installation#st3](https://packagecontrol.io/installation#st3)
    
![Sublime-package-control](https://images.jsdiff.com/Sublime-package-control_1588339184724.png)
    
    崇高包装控制
    
2.  现在记下Sublime Editor中安装软件包的文件夹的位置。您可以通过单击**首选项>浏览包**来找到位置。
    
![Browse-Packages](https://images.jsdiff.com/Browse-Packages_1588339184654.png)
    
    浏览套餐
    
3.  单击“ Package Control.sublime-package”链接，**保存**从包控制网站**下载的文件**，并将其**放在第二步的文件夹中**。
4.  现在**，**通过关闭**升华编辑器**来**重新启动**它，然后再次将其打开。
5.  要验证是否正确安装了程序包控件，请单击“ **首选项”>“程序包控件”**菜单项。它应该打开程序包控制窗口。
    
 ![Package-Control-Menu](https://images.jsdiff.com/Package-Control-Menu_1588339182318.png)
    
    包装控制菜单
    

安装软件包Python 3
-------------

1.  现在要安装任何软件包支持，包括Python软件包，请转到**“偏好设置”>“软件包控制”，**然后选择“ **安装软件包”**。
    
![Install-Package-Window](https://images.jsdiff.com/Install-Package-Window_1588339182317.png)
    
    安装软件包窗口
    
2.  在打开的窗口中，**键入“ python”以仅过滤**与python相关**的软件包列表**。
    
   ![Select-Python-Package-to-Install](https://images.jsdiff.com/Select-Python-Package-to-Install_1588339182451.png)
    
    选择要安装的Python软件包
    

等待几秒钟，Python包将安装到编辑器中。


验证Python自动完成和构建
---------------

要验证python支持，请再次**重新启动IDE**。创建一个名为name的文件`demo.py`。输入一些简单的命令，例如`print`。它**应该打开自动完成**窗口。

现在输入简单的hello world code，然后输入`CTRL + B`keyborad。它将在底部窗格中打开输出输出窗口，并将在文件中**显示命令**的生成**输出**`demo.py`。

![Sublime-Build-Output](https://images.jsdiff.com/Sublime-Build-Output_1588339184651.png)

崇高的构建输出

现在，您可以使用sublime编辑器创建和构建python程序了。

学习愉快！