---
title: 数组比较(Shell基础教程5)
id: 1430
date: 2024-10-31 22:01:55
author: daichangya
permalink: /archives/shu-zu-bi-jiao-Shell-ji-chu-jiao-cheng-5/
categories:
- shell-tutorial
---

Tutorial
--------

数组比较
Shell可以处理数组
数组是包含多个值的变量。任何变量都可以用作数组。数组的大小没有最大限制,也没有要求成员变量被连续索引或连续分配。
数组从零开始:第一个元素的编号为0。 
   
 # basic construct
	# array=(value1 value2 ... valueN)
	array=(23 45 34 1 2 3)
	#To refer to a particular value (e.g. : to refer 3rd value)
	echo ${array[2]}  
    
	#To refer to all the array values
	echo ${array[@]}
	
	#To evaluate the number of elements in an array
	echo ${#array[@]}
 
Exercise
--------
在本练习中,您将需要比较三个数组列表并编写所有三个数组的公共元素:

`a=(3 5 8 10 6)`,`b=(6 5 4 12)`,`c=(14 7 5 7)`
结果是共同点5。

Tutorial Code
-------------
 #!/bin/bash
	# enter your array comparison code here
        

Expected Output
---------------
 5

Solution
--------

	#!/bin/bash
	# enter your array comparison code here
	# initialize arrays a b c
	a=(3 5 8 10 6) 
	b=(6 5 4 12) 
	c=(14 7 5 7)
	#comparison of first two arrays a and b
	for x in "${a[@]}"; do 
	  in=false 
	  for y in "${b[@]}"; do 
	    if [ $x = $y ];then 
	      # assigning the matching results to new array z
	      z[${#z[@]}]=$x
	    fi
	  done 
	done
	#comparison of third array c with new array z
	for i in "${c[@]}"; do 
	  in=false
	  for k in "${z[@]}"; do
	    if [ $i = $k ];then
	      # assigning the matching results to new array j
	      j[${#j[@]}]=$i
	    fi
	  done 
	done 
	# print content of array j
	echo ${j[@]}


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