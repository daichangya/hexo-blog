---
title: 数组(Shell基础教程4)
id: 1429
date: 2024-10-31 22:01:55
author: daichangya
permalink: /archives/arrays/
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

+   [Hello, World!(Shell基础教程1)](https://blog.jsdiff.com/archives/Hello-World)
+   [变量(Shell基础教程2)](https://blog.jsdiff.com/archives/Variables)
+   [将参数传递给脚本(Shell基础教程3)](https://blog.jsdiff.com/archives/Passing-Arguments-to-the-Script)
+   [数组(Shell基础教程4)](https://blog.jsdiff.com/archives/Arrays)
+   [数组比较(Shell基础教程5)](https://blog.jsdiff.com/archives/Array-Comparison)
+   [基本运算符(Shell基础教程6)](https://blog.jsdiff.com/archives/Basic-Operators)
+   [基本字符串操作(Shell基础教程7)](https://blog.jsdiff.com/archives/Basic-String-Operations)
+   [逻辑表达式(Shell基础教程8)](https://blog.jsdiff.com/archives/Decision-Making)
+   [循环(Shell基础教程9)](https://blog.jsdiff.com/archives/Loops)
+   [shell函数(Shell基础教程10)](https://blog.jsdiff.com/archives/Shell-Functions)
+   [特殊变量(Shell基础教程11)](https://blog.jsdiff.com/archives/Special-Variables)
+   [字符串操作(Shell基础教程12)](https://blog.jsdiff.com/archives/String-Operations)
+   [捕捉信号命令(Shell基础教程13)](https://blog.jsdiff.com/archives/Bash-trap-command)
+   [文件测试(Shell基础教程14)](https://blog.jsdiff.com/archives/File-Testing)
+   [输入参数解析(Shell基础教程15)](https://blog.jsdiff.com/archives/Input-Parameter-Parsing)
+   [管道(Shell基础教程16)](https://blog.jsdiff.com/archives/Pipelines)
+   [输入输出(Shell基础教程17)](https://blog.jsdiff.com/archives/Process-Substitution)
+   [常用表达(Shell基础教程18)](https://blog.jsdiff.com/archives/Regular-Expressions)
+   [特殊命令sed(Shell基础教程19)](https://blog.jsdiff.com/archives/Basic-Sed-Operators)
