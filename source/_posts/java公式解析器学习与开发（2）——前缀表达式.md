---
title: java公式解析器学习与开发（2）——前缀表达式
id: 428
date: 2024-10-31 22:01:43
author: daichangya
excerpt: "前缀表达式就是前序表达式。前缀表达式就是不含括号的算术表达式，而且它是将运算符写在前面，操作数写在后面的表达式，为纪念其发明者波兰数学家Jan Lukasiewicz也称为“波兰式”。例如，- 1 + 2 3，它等价于1-(2+3)。2求值方法对于一个前缀表达式的求值而言，首先要从右至左扫描表达式，从右边第一个字符开始判断，如果当前字符是数字则一直到数字串的"
permalink: /archives/12917145/
categories:
 - 解释器
---

 

释义  

前缀表达式就是[前序表达式](http://baike.baidu.com/view/6302645.htm)。

前缀表达式就是不含括号的[算术表达式](http://baike.baidu.com/view/3524050.htm)，而且它是将[运算符](http://baike.baidu.com/view/425996.htm)写在前面，[操作数](http://baike.baidu.com/view/420846.htm)写在后面的表达式，为纪念其发明者波兰数学家Jan Lukasiewicz也称为“波兰式”。例如，- 1 + 2 3，它等价于1-(2+3)。

## 2求值方法

对于一个前缀表达式的求值而言，首先要从右至左扫描表达式，从右边第一个字符开始判断，如果当前字符是数字则一直到数字串的末尾再记录下来，如果是[运算符](http://baike.baidu.com/view/425996.htm)，则将右边离得最近的两个“数字串”作相应的运算，以此作为一个新的“数字串”并记录下来。一直扫描到表达式的最左端时，最后运算的值也就是表达式的值。例如，前缀表达式“\- 1 + 2 3“的求值，扫描到3时，记录下这个数字串，扫描到2时，记录下这个数字串，当扫描到+时，将+右移做相邻两数字串的[运算符](http://baike.baidu.com/view/425996.htm)，记为2+3，结果为5，记录下这个新数字串，并继续向左扫描，扫描到1时，记录下这个数字串，扫描到-时，将-右移做相邻两数字串的运算符，记为1-5，结果为-4，所以表达式的值为-4。

## 3公式用法

前缀表达式是一种十分有用的表达式，它将中缀表达式转换为可以依靠简单的操作就能得到运算结果的表达式。例如，(a+b)*(c+d)转换为*,+,a,b,+,c,d。它的优势在于只用两种简单的操作，入栈和[出栈](http://baike.baidu.com/view/346791.htm)就可以解决任何中缀表达式的运算。其运算方式为：如果当前字符(或字符串)为数字或[变量](http://baike.baidu.com/view/296689.htm)，则压入栈内；如果是[运算符](http://baike.baidu.com/view/425996.htm)，则将栈顶两个元素弹出栈外并作相应运算，再将结果压入栈内。当前缀表达式扫描结束时，栈里的就是中缀表达式运算的最终结果。

## 4相关例子

a+b ---> +,a,b

a+(b-c) ---> +,a,-,b,c

a+(b-c)\*d ---> +,a,\*,-,b,c,d

a=1+3 ---> =,a,+,1,3

## 5转换算法

(1) 首先构造一个运算符栈(也可放置括号)，运算符(以括号分界点)在栈内遵循越往栈顶优先级不降低的原则进行排列。

(2)从右至左扫描中缀表达式，从右边第一个字符开始判断：

如果当前[字符](http://baike.baidu.com/view/263416.htm)是数字，则分析到数字串的结尾并将数字串直接输出。

如果是运算符，则比较优先级。如果当前运算符的优先级大于等于栈顶运算符的优先级(当栈顶是括号时，直接入栈)，则将运算符直接入栈；否则将栈顶运算符[出栈](http://baike.baidu.com/view/346791.htm)并输出，直到当前运算符的优先级大于等于栈顶运算符的优先级(当栈顶是括号时，直接入栈)，再将当前运算符入栈。

如果是括号，则根据括号的方向进行处理。如果是右括号，则直接入栈；否则，遇左括号前将所有的运算符全部[出栈](http://baike.baidu.com/view/346791.htm)并输出，遇左括号后将左右的两括号一起删除。

(3) 重复上述操作(2)直至扫描结束，将栈内剩余运算符全部[出栈](http://baike.baidu.com/view/346791.htm)并输出，再逆缀输出字符串。中缀表达式也就转换为前缀表达式了。

## 6实例分析

将中缀表达式“1+((2+3)*4)-5”转换为前缀表达式。

<table class="table-view log-set-param" width="99%" style="border-collapse:collapse;border-spacing:0px;font-size:12px;line-height:22px;color:rgb(0,0,0);font-family:arial, '宋体', sans-serif;"><tbody><tr><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">中缀表达式</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">前缀表达式</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">（栈顶）运算符栈（栈尾）</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">说明</div></td></tr><tr><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">5</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">5</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">空</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">5，是数字串直接输出</div></td></tr><tr><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">-</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">5</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">-</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">-，栈内无运算符，直接入栈</div></td></tr><tr><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">）</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">5</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">-）</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">)，直接入栈</div></td></tr><tr><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">4</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">5 4</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">-）</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">4，是数字串直接输出</div></td></tr><tr><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">*</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">5 4</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">-）*</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">*，栈顶是括号，直接入栈</div></td></tr><tr><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">)</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">5 4</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">- ) * )</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">)，直接入栈</div></td></tr><tr><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">3</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">5 4 3</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">- ) * )</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">3，是数字串直接输出</div></td></tr><tr><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">+</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">5 4 3</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">- ) * ) +</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">+，栈顶是括号，直接入栈</div></td></tr><tr><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">2</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">5 4 3 2</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">- ) * )+</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">2，是数字串直接输出</div></td></tr><tr><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">(</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">5 4 3 2+</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">- ) *</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">(，参考①</div></td></tr><tr><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">(</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">5 4 3 2+*</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">-</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">(，参考①</div></td></tr><tr><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">+</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">5 4 3 2+*</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">-+</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">+，优先级大于等于栈顶运算符，直接入栈</div></td></tr><tr><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">1</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">5 4 3 2+*1</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">-+</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">1，是数字串直接输出</div></td></tr><tr><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">空</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">5 4 3 2+*1+-</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">空</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">扫描结束，将栈内剩余运算符全部出栈并输出</div></td></tr><tr><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">空</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">- + 1 * + 2 3 4 5</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">空</div></td><td style="border:1px solid rgb(230,230,230);"><div class="para" style="color:rgb(51,51,51);line-height:25px;">逆缀输出字符串</div></td></tr></tbody></table>

## 7运算符

)：直接入栈

(：遇)前，将运算符全部出栈并输出；遇)后，将两括号一起删除①

+、-：1

*、/、%：2

^：3