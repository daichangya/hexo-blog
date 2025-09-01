---
title: 将参数传递给脚本(Shell基础教程3)
id: 1428
date: 2024-10-31 22:01:55
author: daichangya
excerpt: PassingArgumentstotheScript可以在执行脚本时将参数传递为脚本,方法是在脚本文件名后将其作为空格分隔的列表编写。在脚本内部,$1变量引用命令行中的第一个参数,$2引用第二个参数,依此类推。变量$0引用当前脚本。在以下示例中,脚本名称后跟6个参数。./bin/my_shoppi
permalink: /archives/jiang-can-shu-chuan-di-gei-jiao-ben/
categories:
- shell-tutorial
---

Passing Arguments to the Script
--------
可以在执行脚本时将参数传递为脚本,方法是在脚本文件名后将其作为空格分隔的列表编写。

在脚本内部,$1变量引用命令行中的第一个参数,$2引用第二个参数,依此类推。
变量$0引用当前脚本。在以下示例中,脚本名称后跟6个参数。

	./bin/my_shopping.sh apple 5 banana 8 "Fruit Basket" 15
	echo $3                          --> results with: banana
	BIG=$5
	echo "A $BIG costs just $6"      --> results with: A Fruit Basket costs just 15


变量$#保留传递给脚本的参数数量

**echo $#               --> results with: 6**

变量$@包含一个以空格分隔的字符串,其中包含传递给脚本的所有参数

Exercise
-------------
本节没有练习。您可以继续。

Tutorial Code
-------------
    #!/bin/bash
    # There is no exercise for this section.
    # You may proceed.

Solution
--------
    #!/bin/bash
    # There is no exercise for this section.
    # You may proceed.

Expected Output
---------------
    #!/bin/bash
    # There is no exercise for this section.
    # You may proceed.


*   [Hello, World!(Shell基础教程1)](https://blog.jsdiff.com/archives/Hello-World)
*   [变量(Shell基础教程2)](https://blog.jsdiff.com/archives/Variables)
*   [将参数传递给脚本(Shell基础教程3)](https://blog.jsdiff.com/archives/Passing-Arguments-to-the-Script)
*   [数组(Shell基础教程4)](https://blog.jsdiff.com/archives/Arrays)
*   [数组比较(Shell基础教程5)](https://blog.jsdiff.com/archives/Array-Comparison)
*   [基本运算符(Shell基础教程6)](https://blog.jsdiff.com/archives/Basic-Operators)
*   [基本字符串操作(Shell基础教程7)](https://blog.jsdiff.com/archives/Basic-String-Operations)
*   [逻辑表达式(Shell基础教程8)](https://blog.jsdiff.com/archives/Decision-Making)
*   [循环(Shell基础教程9)](https://blog.jsdiff.com/archives/Loops)
*   [shell函数(Shell基础教程10)](https://blog.jsdiff.com/archives/Shell-Functions)
*   [特殊变量(Shell基础教程11)](https://blog.jsdiff.com/archives/Special-Variables)
*   [字符串操作(Shell基础教程12)](https://blog.jsdiff.com/archives/String-Operations)
*   [捕捉信号命令(Shell基础教程13)](https://blog.jsdiff.com/archives/Bash-trap-command)
*   [文件测试(Shell基础教程14)](https://blog.jsdiff.com/archives/File-Testing)
*   [输入参数解析(Shell基础教程15)](https://blog.jsdiff.com/archives/Input-Parameter-Parsing)
*   [管道(Shell基础教程16)](https://blog.jsdiff.com/archives/Pipelines)
*   [输入输出(Shell基础教程17)](https://blog.jsdiff.com/archives/Process-Substitution)
*   [常用表达(Shell基础教程18)](https://blog.jsdiff.com/archives/Regular-Expressions)
*   [特殊命令sed(Shell基础教程19)](https://blog.jsdiff.com/archives/Basic-Sed-Operators)