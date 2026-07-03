---
title: 数组(Shell基础教程4)
id: 1429
date: 2024-10-31 22:01:55
author: daichangya
permalink: /archives/shu-zu-Shell-ji-chu-jiao-cheng-4/
categories:
- shell-tutorial
---
## Tutorial

一个数组可以用一个名称保存多个值。数组命名与变量命名相同。  
通过分配()中包含的以空格分隔的值来初始化数组

```
my_array=(apple banana "Fruit Basket" orange)
new_array[2]=apricot
```

数组成员不必是连续的或连续的。数组的某些成员可以保留为未初始化。

```bash
数组中元素的总数由${#my_array[@]}  引用

my_array=(apple banana "Fruit Basket" orange)
echo  ${#my_array[@]}                   # 4
```

可以使用数字索引访问数组元素。第一个元素的索引为0。

```
my_array=(apple banana "Fruit Basket" orange)
echo ${my_array[3]}                     # orange - note that curly brackets are needed
# adding another array element
my_array[4]="carrot"                    # value assignment without a $ and curly brackets
echo ${#my_array[@]}                    # 5
echo ${my_array[${#my_array[@]}-1]}     # carrot
```

## Exercise

在本练习中,您将需要将数字和字符串添加到正确的数组中。您必须将数字1,2和3添加到“数字”数组中,并将单词“ hello”和“ world”添加到字符串数组中。

您还必须更正变量NumberOfNames和变量second\_name的值。NumberOfNames应该使用$#特殊变量保存NAMES数组中名称的总数。变量second\_name应该使用方括号运算符\[ \]在NAMES数组中保留第二个名称。请注意,索引是从零开始的,因此,如果您要访问列表中的第二项,则其索引将为1。

## Tutorial Code

```
#!/bin/bash
NAMES=( John Eric Jessica )
# write your code here
NUMBERS=()
STRINGS=()
NumberOfNames=0
second_name='Vladimir'
```

## Expected Output

```
1 2 3
hello world
The number of names listed in the NAMES array: 3
The second name on the NAMES list is: Eric
```

## Solution

```
#!/bin/bash
NAMES=( John Eric Jessica )
# write your code here
NUMBERS=( 1 2 3 )
STRINGS=( "hello" "world" )
NumberOfNames=${#NAMES[@]}
second_name=${NAMES[1]}
echo ${NUMBERS[@]}
echo ${STRINGS[@]}
echo "The number of names listed in the NAMES array: $NumberOfNames"
echo "The second name on the NAMES list is:" ${second_name}
```

+   [Hello, World!(Shell基础教程1)](https://www.tushu.info/archives/Hello-World-Shell-ji-chu-jiao-cheng-1)
+   [变量(Shell基础教程2)](https://www.tushu.info/archives/bian-liang-Shell-ji-chu-jiao-cheng-2)
+   [将参数传递给脚本(Shell基础教程3)](https://www.tushu.info/archives/jiang-can-shu-chuan-di-gei-jiao-ben)
+   [数组(Shell基础教程4)](https://www.tushu.info/archives/shu-zu-Shell-ji-chu-jiao-cheng-4)
+   [数组比较(Shell基础教程5)](https://www.tushu.info/archives/shu-zu-bi-jiao-Shell-ji-chu-jiao-cheng-5)
+   [基本运算符(Shell基础教程6)](https://www.tushu.info/archives/bian-liang-Shell-ji-chu-jiao-cheng-2)
+   [基本字符串操作(Shell基础教程7)](https://www.tushu.info/archives/bian-liang-Shell-ji-chu-jiao-cheng-2)
+   [逻辑表达式(Shell基础教程8)](https://www.tushu.info/archives/xun-huan-Shell-ji-chu-jiao-cheng-9)
+   [循环(Shell基础教程9)](https://www.tushu.info/archives/xun-huan-Shell-ji-chu-jiao-cheng-9)
+   [shell函数(Shell基础教程10)](https://www.tushu.info/archives/guan-dao-Shell-ji-chu-jiao-cheng-16)
+   [特殊变量(Shell基础教程11)](https://www.tushu.info/archives/bian-liang-Shell-ji-chu-jiao-cheng-2)
+   [字符串操作(Shell基础教程12)](https://www.tushu.info/archives/bian-liang-Shell-ji-chu-jiao-cheng-2)
+   [捕捉信号命令(Shell基础教程13)](https://www.tushu.info/archives/guan-dao-Shell-ji-chu-jiao-cheng-16)
+   [文件测试(Shell基础教程14)](https://www.tushu.info/archives/bian-liang-Shell-ji-chu-jiao-cheng-2)
+   [输入参数解析(Shell基础教程15)](https://www.tushu.info/archives/jiang-can-shu-chuan-di-gei-jiao-ben)
+   [管道(Shell基础教程16)](https://www.tushu.info/archives/shu-ru-shu-chu-Shell-ji-chu-jiao-cheng)
+   [输入输出(Shell基础教程17)](https://www.tushu.info/archives/shu-ru-shu-chu-Shell-ji-chu-jiao-cheng)
+   [常用表达(Shell基础教程18)](https://www.tushu.info/archives/bian-liang-Shell-ji-chu-jiao-cheng-2)
+   [特殊命令sed(Shell基础教程19)](https://www.tushu.info/archives/chao-xiang-xi-SED-liu-bian-ji-qi-cong)
