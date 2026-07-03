---
title: 变量(Shell基础教程2)
id: 1427
date: 2024-10-31 22:01:55
author: daichangya
permalink: /archives/bian-liang-Shell-ji-chu-jiao-cheng-2/
categories:
- shell-tutorial
---

Tutorial
--------
一旦为Shell变量分配了值,便会创建它们。变量可以包含数字,字符或字符串。变量名区分大小写,可以由字母和下划线“ _”组成。
值分配使用“ =”符号完成。请注意,初始化变量时,=符号的两侧均不允许有空格。

    PRICE_PER_APPLE=5
    MyFirstLetters=ABC
    greeting='Hello        world!'

引用变量

反斜杠“ \\”用于转义特殊字符的含义

    PRICE_PER_APPLE=5
    echo "The price of an Apple today is: \$HK $PRICE_PER_APPLE"

使用$ {}封装变量名可避免歧义

    MyFirstLetters=ABC
    echo "The first 10 letters in the alphabet are: ${MyFirstLetters}DEFGHIJ"

用“”封装变量名将保留所有空格值
   
    greeting='Hello        world!'
    echo $greeting" now with spaces: $greeting"

可以使用命令输出的值来分配变量。这称为替代。可以通过用``(称为反引号)或$()封装命令来完成替换

    FILELIST=`ls`
    FileWithTimeStamp=/tmp/my-dir/file_$(/bin/date +%Y-%m-%d).txt

请注意,脚本运行时,它将在$()括号内运行命令并捕获其输出。

Exercise
--------
本练习的目标是使用命令替换来创建字符串,整数和复杂变量。该字符串应命名为BIRTHDATE,并且应包含文本“ 2000年1月1日”。该整数应命名为Presents,并应包含数字10。复杂变量应命名为BIRTHDAY,并且应包含与变量BIRTHDATE中的日期匹配的日期的星期几,例如星期六。请注意,“ date”命令可用于将日期格式转换为其他日期格式。例如,要将日期值$ date1转换为date1的星期几,请使用:

    date -d "$date1" +%A

Tutorial Code
-------------
    #!/bin/bash
    # Change this code
    BIRTHDATE=
    Presents=
    BIRTHDAY=
    
    
    # Testing code - do not change it
    
    if [ "$BIRTHDATE" == "Jan 1, 2000" ] ; then
        echo "BIRTHDATE is correct, it is $BIRTHDATE"
    else
        echo "BIRTHDATE is incorrect - please retry"
    fi
    if [ $Presents == 10 ] ; then
        echo "I have received $Presents presents"
    else
        echo "Presents is incorrect - please retry"
    fi
    if [ "$BIRTHDAY" == "Saturday" ] ; then
        echo "I was born on a $BIRTHDAY"
    else
        echo "BIRTHDAY is incorrect - please retry"
    fi

Expected Output
---------------
    BIRTHDATE is correct, it is Jan 1, 2000
    I have received 10 presents
    I was born on a Saturday

Solution
--------
    #!/bin/bash
    # Change this code
    BIRTHDATE="Jan 1, 2000"
    Presents=10
    BIRTHDAY=`date -d "$BIRTHDATE" +%A`
    
    
    # Testing code - do not change it
    
    if [ "$BIRTHDATE" == "Jan 1, 2000" ] ; then
        echo "BIRTHDATE is correct, it is $BIRTHDATE"
    else
        echo "BIRTHDATE is incorrect - please retry"
    fi
    if [ $Presents == 10 ] ; then
        echo "I have received $Presents presents"
    else
        echo "Presents is incorrect - please retry"
    fi
    if [ "$BIRTHDAY" == "Saturday" ] ; then
        echo "I was born on a $BIRTHDAY"
    else
        echo "BIRTHDAY is incorrect - please retry"
    fi


*   [Hello, World!(Shell基础教程1)](https://www.tushu.info/archives/Hello-World-Shell-ji-chu-jiao-cheng-1)
*   [变量(Shell基础教程2)](https://www.tushu.info/archives/bian-liang-Shell-ji-chu-jiao-cheng-2)
*   [将参数传递给脚本(Shell基础教程3)](https://www.tushu.info/archives/jiang-can-shu-chuan-di-gei-jiao-ben)
*   [数组(Shell基础教程4)](https://www.tushu.info/archives/shu-zu-Shell-ji-chu-jiao-cheng-4)
*   [数组比较(Shell基础教程5)](https://www.tushu.info/archives/shu-zu-bi-jiao-Shell-ji-chu-jiao-cheng-5)
*   [基本运算符(Shell基础教程6)](https://www.tushu.info/archives/bian-liang-Shell-ji-chu-jiao-cheng-2)
*   [基本字符串操作(Shell基础教程7)](https://www.tushu.info/archives/bian-liang-Shell-ji-chu-jiao-cheng-2)
*   [逻辑表达式(Shell基础教程8)](https://www.tushu.info/archives/xun-huan-Shell-ji-chu-jiao-cheng-9)
*   [循环(Shell基础教程9)](https://www.tushu.info/archives/xun-huan-Shell-ji-chu-jiao-cheng-9)
*   [shell函数(Shell基础教程10)](https://www.tushu.info/archives/guan-dao-Shell-ji-chu-jiao-cheng-16)
*   [特殊变量(Shell基础教程11)](https://www.tushu.info/archives/bian-liang-Shell-ji-chu-jiao-cheng-2)
*   [字符串操作(Shell基础教程12)](https://www.tushu.info/archives/bian-liang-Shell-ji-chu-jiao-cheng-2)
*   [捕捉信号命令(Shell基础教程13)](https://www.tushu.info/archives/guan-dao-Shell-ji-chu-jiao-cheng-16)
*   [文件测试(Shell基础教程14)](https://www.tushu.info/archives/bian-liang-Shell-ji-chu-jiao-cheng-2)
*   [输入参数解析(Shell基础教程15)](https://www.tushu.info/archives/jiang-can-shu-chuan-di-gei-jiao-ben)
*   [管道(Shell基础教程16)](https://www.tushu.info/archives/shu-ru-shu-chu-Shell-ji-chu-jiao-cheng)
*   [输入输出(Shell基础教程17)](https://www.tushu.info/archives/shu-ru-shu-chu-Shell-ji-chu-jiao-cheng)
*   [常用表达(Shell基础教程18)](https://www.tushu.info/archives/bian-liang-Shell-ji-chu-jiao-cheng-2)
*   [特殊命令sed(Shell基础教程19)](https://www.tushu.info/archives/chao-xiang-xi-SED-liu-bian-ji-qi-cong)