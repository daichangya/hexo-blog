---
title: 管道(Shell基础教程16)
id: 1463
date: 2024-10-31 22:01:56
author: daichangya
excerpt: ''
categories:
- shell-tutorial
permalink: /archives/guan-dao-Shell-ji-chu-jiao-cheng-16/
---

Tutorial
---------
管道(通常称为管道)是一种链接命令并将命令的输出连接到命令的输入的方法。
管道由管道字符``|``表示。当命令需要复杂或长输入时,它特别方便。

    command1 | command2

默认情况下,管道仅重定向标准输出,如果要包括标准错误,则需要使用格式``|&``,这是``2>&1 |``的简写形式。

### 示例:
想象一下,您很快想知道目录中的条目数,可以使用管道使用选项``-l``将``ls``命令的输出重定向到``wc``命令。

    ls / | wc -l

然后,您只想查看前10个结果

    ls / | head
    
 *注意:head默认情况下输出前10行,请使用选项-n更改此行为*

Exercise
--------
在本练习中,您将需要根据cpuinfo文件(/proc/cpuinfo)中的信息打印处理器数量。

*提示:每个处理器都有一个唯一的编号,例如第一个处理器将包含行``processor: 0``*

Tutorial Code
-------------
    cat /proc/cpuinfo # | some command

Expected Output
---------------
    4

Solution
--------
    #!/bin/bash
    cat /proc/cpuinfo | grep processor | wc -l



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