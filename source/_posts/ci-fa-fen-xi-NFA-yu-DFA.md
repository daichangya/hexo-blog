---
title: 词法分析(NFA与DFA)
id: 1124
date: 2024-10-31 22:01:49
author: daichangya
excerpt: '词法分析(1)---词法分析的有关概念以及转换图 词法分析是编译的第一个阶段，前面简介中也谈到过词法分析器的任务就是： 字符流------>词法记号流

  这里词法分析和语法分析会交错进行，也就是说，词法分析器不会读取所有的词法记号再使用语法分析器来处理，通常情况下，每取一个词法记号，就送入语法分析器进行分析，图解：



  词法分析器是编译器中与源程序直接接触的部分，因此词法分析器可'
permalink: /archives/ci-fa-fen-xi-NFA-yu-DFA/
tags:
- 编译原理
---

**词法分析(1)---词法分析的有关概念以及转换图**

词法分析是编译的第一个阶段，前面简介中也谈到过词法分析器的任务就是：  
字符流------>词法记号流  
  
这里词法分析和语法分析会交错进行，也就是说，词法分析器不会读取所有的词法记号再使用语法分析器来处理，通常情况下，每取一个词法记号，就送入语法分析器进行分析，图解：  
  
[![clip_image001](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image001_thumb.jpg "按此在新窗口打开图片")](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image001_2.jpg)  
  
词法分析器是编译器中与源程序直接接触的部分，因此词法分析器可以做诸如  
1). 去掉注释，自动生成文档(c#中的///注释)  
2). 提供错误位置(可以通过记录行号来提供)，当字符流变成词法记号流以后，就没有了行的概念  
3). 完成预处理，比如宏定义  
  
  
1. 词法记号，词法单元(lexeme)，模式  
模式是一种规则  
每个词法单元都有一个特定记号  
  
比如 int a=3，这里 int，a，＝，3都是词法单元，每个词法单元都属于某个词法记号，比如3就是"num"这个词法记号的一个词法单元，而模式规定了什么样的字符串的词法记号是什么样的(模式是一种规则)  
  
某一特定模式规定了某个词法记号下的一类词法单元，比如：  
模式：用字母开头的包含字母和数字的串  
上面模式的词法记号：id(所有符合上面模式的字符串的记号都是id)  
词法单元：a123 或者 aabc 等  
  
词法记号举例(简称为记号)：  
1) 每个的关键字都有属于自己的一个记号，比如关键字for，它可以使用记号for；关键字int，可以使用记号int  
2) 所有的关系运算符只有一个记号，比如 >=,<=都用记号relation  
3) 所有的标识符只有一个记号，比如a123,aab使用记号id  
4) 所有的常数只有一个记号，比如123,22,32.3,23E10使用记号num  
5) 所有的字符串只有一个记号，比如"123","ab1"使用记号literal  
在实际的编译器设计中，词法记号，一般用一个整形数字表示  
  
词法记号的属性：  
我们喜欢用<词法记号, 属性>这个二元组来描述一个词法单元，比如，对于源代码：position := initial + rate \* 60  
对于词法单元 +，我们可以使用 <add\_op, '+'> 来表示。  
有些情况，更加复杂一点，比如对于 position，我们表示是这样的，<id, 指向符号表中的position元素的指针>，详细来说应该是这样的，假定属性是一个字符串，那么id将指向这样一个字符串"position\\0"，我们把存放这个字符串的地方叫做符号表。有些时候，属性是不必要的，比如 := ，表示赋值，我们可以使用 <assign\_op,257> 这样的表示这个词法单元，不过这个显得有些多于，因为assign\_op和词法单元是一对一的，也就是assign\_op只对应了:=，所以额外信息(属性)就显得多余的了  
  
词法错误：  
词法分析器是很难(有些错误还是可以检测)检测错误的，因为词法分析器的目的是产生词法记号流，它没有能力去分析程序结构，因此无法检测到和程序结构有关的错误，比如：  
fi(a == b)  
词法分析器不会找到这个错误，它认为 fi 是一个标识符，而不是一个关键字，只有在后面的阶段中，这个错误才会被发现，这是一个与程序结构有关的错误  
词法分析器，只能检测到词法单元上的问题，比如 12.ab ，作为一个词法单元，却不没有对应的模式，那么就是产生一个错误。  
  
2. 正规式：  
前面说过模式是一种规则，为了使用，我们需要一种规范的方式来表达模式，这就是正规式  
1) 串和语言  
字符类(又叫字母表)：关于字符的有限集合  
串：字符类上字符的有穷序列，串这个概念，具体来说是，某个字符类上的串  
串的长度：串中字符的个数，比如串 s = abc ，那么串的长度为3，用|s|表示串的长度  
空串：用 ε 表示  
语言：某字符类上的串的集合，属于语言的串，成为语言的句子或字  
  
比如：{abc, a}这就是一个语言，abc和a就是句子。另外空集也是属于语言  
  
连接：x是串，y是串，x和y连接，结果就是 xy 这个串。假如 x 是串，x^3为 xxx。对于 x^n (n>=0),x^0 = ε  
语言的运算(假定L和M是语言)：  
1\. L U M = {s|s属于L或者M}，例如：  
L={1,2} M={3,4} 那么 L U M = {1,2,3,4}  
  
2\. LM = {st|s属于L且t属于M}，例如：  
L={a,b} M={1,2} 那么 LM = {a1,a2,b1,b2}  ML={1a,1b,2a,2b}  
  
3\. L^n = LLL...LLL (n个L)，例如：  
L={a,b} 那么 L^3 = {aaa,aab,aba,abb,baa,bab,bbb,bba}

注意 n 可以为0，L^0 = {ε}  
  
4\. L\* = L^0 U L^1 U L^2 U L^3 U ...  
L\*表示，语言L中，所有的句子(串)以任意数目任意顺序组成的句子的集合，包括 ε，例如：  
{a,b}\* = {ε,a,b,ab,ba,aab,aba,baa,bba,bab,abb,aaa,bbb...}  
L\*叫做L的闭包  
  
5\. L+ = L^1 U L^2 U L^3 U...  
L+表示，语言L中，所有的句子(串)以任意数目任意顺序组成的句子的集合，但是不包括 ε  
L+中的句子和 L\*中的句子相比少一个 ε  
  
那么，我们通过上面的知识就可以表示一个标识符了，我们知道一般语言规定标识符是由字母开头，后接若干个字母或数字，我们可以这样来表示： L={a-z A-Z} N={0-9}，那么标识符就是 L(L U N)\*  
  
  
2) 正规式  
正规式又叫正规表达式，正规式是模式得一种规范的表达形式，正规式描述了一个集合，这个集合是由串组成的，其实这个集合就是我们前面说过的语言，不过这里大家喜欢使用正规集这个术语。正规式 r 表示正规集L(r)

正规式的运算：

1. 闭包运算，运算优先级最高，(r)\* 表示 (L(r))\*

2. 连接运算，运算优先集合低于闭包，(r)(s) 表示 (L(r))(L(s))

3. 或运算，运算优先集合最低，(r) | (s) 表示 (L(r)) U (L(s))

例如：

a | b 表示集合(语言，正规集) {a,b}

(a | b)(a | b) 表示集合(语言，正规集) {aa,ab,ba,bb}

a\* 表示由一切a字符组成的集合(语言，正规集)，包括 ε

(a | b) 表示由a,b组成的集合(语言，正规集)，包括 ε

等价的正规式：(a | b) = (b | a)

正规式的代数性质：

1\. r|s = s|r

2\. r|(s|t) = (r|s)|t

3\. (rs)t = r(st)

4\. r(s|t) = rs|rt

5\. εr = r

6\. r\*\* = r\*

7\. r\* = (r|ε)\*

注意，rs != sr 因为连接运算是有顺序的，记住并理解2个最基本的运算：a|b表示{a,b}，ab表示{ab}

3. 正规定义

我们可以使用 名字 -> 正规式这种表示，来说明一个等价的代替，比如：

dight -> 0|1|2|3|4|5|6|7|8|9

这里，我们就可以使用名字 digit 来代替后面的正规表达式

我们可以对某个串集进行正规定义，比如我们对标识符集合进行正规定义：

letter -> A|B|...|Z|a|b|...|z

dight -> 0|1|2|3|4|5|6|7|8|9

id -> letter(letter|dight)\*

请通过上面的例子理解正规定义。

在我们表达正规表达式的时候，可以使用一些符号使得表达简化

1) + ，表示一个或者多个实力，比如，a+ 表示 {a,aa,aaa,aaaa,...}。区别一下\*,他们的关系是这里 r+ = r\* | ε

2) 字符组，\[abc\]表示a|b|c，还可以这样表示\[a-zA-Z\]表示字母表中的字符

4. 状态转换图

状态转换图是对词法分析器进行分析过程的描述，我们看一个判断关系运算的状态转化图：

[![clip_image002](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image002_thumb_1.jpg "按此在新窗口打开图片")](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image002_4.jpg)

1) 图中圆圈表示状态

2) 箭头叫做边。X状态的边，一般指的是由X状态出发，指向其他状态的边

3) 边上的符号叫做标记

如何来使用这个图？假定输入字符串是 <= ，那么识别开始时，发现 < 和状态0与状态1间的边上的标记一样，那么就进入1状态，下一个输入字符为=，将进入2状态，识别结束，返回二元组<relop,LE>

上图中2，3，4，5，7，8状态，他们表示识别了一个关系运算符，这个状态叫做接受状态

状态4上面有一个\*，表示说，输入指针需要回移。所谓的输入指针，就是指向输入字符串中现在被读入的字符的位置，4状态会多读取一个字符，所以需要回移，也就是要注意的是，识别完成之后，输入指针指向的是被识别对象的最后一个字符，而不是待识别对象的第一个字符，这样的规定在实现词法分析器时，是有一定的意义，举例说明：

输入字符串为： a>b

识别的时候，从>开始，读入下一个字符b时，进入4状态，这个时候，输入指针指向b，这时候需要回移

我们在需要回移的状态上加一个\*

每个状态后面有一个return(relop,XX)这个是状态的行为，这里具体来说就是返回一个二元组的行为，词法分析器分析的结果就是得到二元组(词法记号和属性的二元组)，这个二元组可以表示一个特定的字符串。其实上面的\*，也是表示行为，也就是输入指针回移的行为，我们可以看见，只有在接受状态才会有行为出现

对一门典型的语言来说状态可能有几百个

5. 如何编写一个词法分析器

1) 根据需要写出正规定义

2) 根据正规定义画出转换图

3) 根据转换图写出词法分析器

这里详细讨论面向过程的语言来实现一个词法分析器(比如c语言)，并且主要讨论的是第3步  
  
1) 我们需要一个 nextchar() 函数，取得缓存中下一个等待分析的字符，这个函数完成年2个任务

1.       让输入指针向前移动一位

2.       返回输入指针指向的字符

2) 定义一个变量 token\_beginning，在每个状态转换图开始的时候，记录输入指针的位置，定义forward变量作为输入指针  
  
3) 状态转换图被实现成为代码之后，每个状态都有属于自己的一块代码，这些代码按顺序完成以下工作：

1.       读取一个字符，通过nextchar()函数

2.       读取的字符(标志)，如果它和当前状态的边上的标记相同，那么状态将转换到边所指向的状态，具体实现只需要一个语句就是 state = xxx(xxx为目标状态)；如果当前状态的所有边的标记和这个读取字符不一样，那么表示没有找到token(词法记号)，这时候需要调用 fail() 函数

3.       fail() 函数完成这样的功能：a.指针回移，完成 forward ＝ token\_beginning 的操作 b.找到适当的开始状态(也就是寻找另外一个转换图的开始状态)。假定所有的转换图都被尝试过，并且无法匹配，这时候会调用一个发现错误的小程序，来报告错误

4.       请不要随意添加行为到各个状态所持有的代码中，应该以转换图中表示的行为为准

4) 定义一个全局变量 lexical\_value，用于保存一个指针，这个指针由 install\_id() 和 install\_num() 两个函数中的一个返回  
  
5) 定义两个整形变量 start,state，分别表示一个转换图的开始状态和当前的状态  
  
6) nexttoken()，这是词法分析器的主程序，可以说，我们通过调用nexttoken()就完成了词法分析，这个函数一定是这样的格式：  
while(1){  
   switch(state){  
   case xx:  
      ...  
   case yy:  
      ...  
   default:  
      ...  
   }  
}  
  
关于详细的设计这里就不说了，举例说明一个转换图如何转换成为程序：  
[![clip_image003](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image003_thumb_1.jpg "按此在新窗口打开图片")](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image003_4.jpg)  
  
这是一个识别浮点数的例子，看下面的代码：  
```
#include <stdio.h>  
#include <ctype.h>  
#include <string.h>  
  
char \*nexttoken();  
char nextchar();  
void next();  
void back();  
char\* gettoken();  
  
char cbuf\[\]="12.3\*\*\*\*\*\*\*\*\*klj12.2e2jj778";  
int forward = -1;  
  
  
  
int main(){  
    while(1){  
        printf("%s\\n",nexttoken());  
        if(forward >= strlen(cbuf)-1){  
            getchar();  
            return 0;  
        }  
    }  
}  
  
int state;  
int start;  
  
char\* nexttoken(){  
    char c;  
    state = 12;  
    while(1){  
        switch(state){  
        case 12:  
            c = nextchar();  
            start = forward;  
            if(isdigit(c)){  
                state = 13;  
            }else{  
                next();  
            }  
            break;  
        case 13:  
            c = nextchar();  
            if(isdigit(c))  
                state = 13;  
            else if(c == 'e'||c == 'E')    
                state = 16;  
            else if(c == '.')  
                state = 14;  
            else  
                state = 19;  
            break;  
        case 14:  
            c = nextchar();  
            if(isdigit(c))  
                state = 15;  
            break;  
        case 15:  
            c = nextchar();  
            if(isdigit(c))  
                state = 15;  
            else if(c == 'e'|| c == 'E')  
                state = 16;  
            else  
                state = 19;  
            break;  
        case 16:  
            c = nextchar();  
            if(isdigit(c))  
                state = 18;  
            else if(c == '+' || c == '-')  
                state = 17;  
            break;  
        case 17:  
            c = nextchar();  
            if(isdigit(c))  
                state = 18;  
            break;  
        case 18:  
            c = nextchar();  
            if(isdigit(c))  
                state = 18;  
            else  
                state = 19;  
            break;  
        case 19:  
            back();  
            return gettoken();  
        }  
    }  
}  
  
char nextchar(){  
    forward ++;  
    return cbuf\[forward\];  
}  
  
void back(){  
    forward --;  
}  
  
void next(){  
    forward ++;  
}  
  
char token\_buf\[128\];  
char\* gettoken(){  
    int i,j=0;  
    for(i = start; i <= forward; i ++){  
        token\_buf\[j++\] = cbuf\[i\];  
    }  
    token\_buf\[j\] = '\\0';  
    return token\_buf;  
}
```
**词法分析(2)---NFA**

假定一个输入符号(symbol)，可以得到2个或者2个以上的可能状态，那么这个finite automaton就是不确定的，反之就是确定的。例如：  
[![clip_image004](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image004_thumb_1.jpg "按此在新窗口打开图片")](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image004_4.jpg)  
这就是一个不确定的无限自动机，在symbol a输入的时候，无法确定状态应该转向0，还是1  
  
不论是确定的finite automaton还是非确定的finite automaton，它们都可以精确的描述正规集(regular sets)  
我们可以很方便的把正规表达式(regular expressions)转换成为不确定 finite automaton  
  
2\. NFA(Nondeterministic Finite Automaton)  
非确定的无限自动机，我们用NFA这个术语表示，它是一个数学模型(model)：

1.       一个关于状态的集合S

2.       一个关于输入符号(input symbols)的集合**Σ**

3.       函数 move : (状态, 符号) -> P(S) 

4.       一个开始状态s0，是一个唯一的状态

5.       一个结束(接受)状态集合F

注意，P(S)，表示S的幂集。在NFA中，input symbol可以为 ε  
转换函数(transition function)的含义就是，一个确定的状态已经从这个状态出发的一条边的标签(符号symbol)，可以确定它的下一个状态组成的集合，比如上图(这个转换图就是NFA的一种表示方式)，0状态，a符号，确定了一个状态的集合{0,1}  
  
3. 转换图(transition graph)的表示  
我们知道，计算机是无法直接表示一个图，我们应该如何来表示一个转换图？使用表格就是一个最简单的方法，每行表示一个状态，每列表示一个input symbol，这种表格被叫做 transtion table(转换表)  
[![clip_image005](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image005_thumb.jpg "按此在新窗口打开图片")](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image005_2.jpg)  
可以说使用表格是最简单的表示方式，但是我们可以注意到在这个图中状态1和input symbol a，是没有下一个状态的(空集合)，也就是，对于一个大的状态图，我们可能花费大量的空间，而其中空集合会消耗不少空间，但是这种消耗又不是必须的，所以，作为最简单的一种实现方式，却不是最优的  
  
语言(language)被NFA定义成为一个input string的集合，而这个集合中的元素则是被NFA受接受的所有的字符串(那些可以从开始状态到某接受状态的input string)  
  
至于存储的方式，可以试试邻接表。注意，使用什么样的数据结构来保存NFA按情况不同而不同，在一些特殊情况下，某些数据结构会变得很方便使用，而换入其他情况，则不可以使用了。

**词法分析(3)---DFA**

1\. DFA(Deterministic Finite automaton)  
DFA就是确定的有限自动机，因为DFA和NFA关系密切，我们经常需要把他们拿到一起来讲，NFA可以转化成为一个DFA，DFA依然是一个数学model，它和NFA有以下区别

1.       不存在ε-transition，也就是说，不存在ε为input symbol的边

2.       对于move函数，move : (state, symbol) -> S，具体来说就是，一个状态和一个特定的input symbol，不会映射到2个不同的状态。这样的结果是，每个状态，关于每个特定的input symbol，只有一条出边

下图就是一个DFA：  
[![clip_image006](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image006_thumb.jpg "按此在新窗口打开图片")](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image006_2.jpg)  
  
接受语言(a|b)\*ab，注意一下，接受语言(a|b)\*ab的DFA我们前面见过，就是这张图：  
  
[![clip_image004](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image004_thumb_2.jpg "按此在新窗口打开图片")](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image004_6.jpg)  
  
2\. DFA的行为  
我们用一个算法来模拟DFA的行为  
s = s0;  
c = nextchar();  
while(c != EOF){  
    s = move(s,c);  
    c = nextchar();  
}  
if(s属于F)  
    return "yes"  
else  
    return "no"

**词法分析(4)---NFA与DFA的转化**

1. 子集构造(Subset Construction)  
这是一个转换NFA到DFA的算法。我们知道NFA和DFA的区别最主要的就是一个状态和一个input symbol是否能够确定一个状态的问题，对于NFA，它将确定一个组状态，而DFA将确定一个状态，因此，我们有一个很好的办法就是把NFA的状态集对应每个DFA的状态，这就是subset construction的思想，不过这只是大概泛泛而论，我们需要更加明确的认识  
  
1) NFA在任何一个input symbol下，映射的状态集(通过move函数，这个集合通常用T字母表示)应该被知道  
2) 必须保证1)中状态集都对应了DFA中的一个状态  
  
具体算法：  
Input : 一个NFA N  
Output : 接受相同语言的DFA D  
Method : 为D构架一个transition table(转换表) Dtran，每个DFA的状态是一个NFA的状态集合(这里一定要注意前面说过的1)2)两点)。我们定义一些操作：  
  
s 表示NFA的状态，T 表示NFA的状态集合，a表示一个input symbol  
ε-transition(ε转换)就是说input symbol为ε时的transition(转换)

操作(operation)

描述(description)

ε-closure(s)

从NFA的状态s出发，只通过ε-transition到达的NFA的状态集合

ε-closure(T)

NFA的集合T中的状态p，只通过ε-transition到达的NFA的状态集合，再求这些集合的交集。用数学表达就是 {p|p 属于 ε-closure(t) , t属于T}

move(T,a)

NFA的集合，这个集合在input symbol为a，状态为T中任意状态情况下，通过一个转换得到的集合

注意一下，所有的操作都是针对NFA的状态或者状态集合，得到的时NFA的状态集合，或者说是DFA看为一个状态  
  
Subset Construction  
初始Dstates，它仅仅含有状态(D的状态)ε-closure(s0)，并且状态未被标记，s0表示开始状态，注意，Dstates放的是D的状态  
while ( Dstates 有未标记的状态 T ) { // T是D中的一个状态，也是N中一个状态集  
    标记 T;  
    for ( input symbol a ){                  // 遍历所有的input symbol  
       U = ε-closure(move(T, a));        // move为NFA的move函数  
       if ( U 不在 Dstates 中 )  
          把U作为尚未标记的状态加入Dstates;  
       Dtran\[T, a\] = U  
    }  
}  
  
注意，状态s，ε-closure(s)一定包含s  
我们先来熟悉上面的操作operation，再来看上面的算法  
[![clip_image008](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image008_thumb.jpg "按此在新窗口打开图片")](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image008_2.jpg)  
  
ε-closure(0) = {0, 1, 2, 4, 7}   // 从0状态出发的，input symbol为ε的所有状态的集合  
ε-closure(3) = {1, 2, 3, 4, 6, 7}  
ε-closure(8) = {8}  
ε-closure( {3, 8} ) = ε-closure(3) U ε-closure(8) = {1, 2, 3, 4, 6, 7, 8}  
move(0,a) = 空  
move(7,a) = {8}  
move(8,b) = {9}  
move( {0, 1, 2, 4, 7}, a) = move(0,a) U move(1,a) U move(2,a) U move(4,a) U move(7,a) = {3, 8}  
  
现在可以回去理解一下算法了。  
  
这里再说说求ε-closure(T)的算法：  
  
把T的所有状态压入stack(栈);  
ε-closure(T)的初始值为 T 中的所有元素 ;  // 也就是一定包含他们本身  
while( 栈非空 ) {  
    弹出栈顶元素 t ;  
    for( 每个属于 move(t, ε) 的状态 u ){  
       if( u 不在 ε-closure(T) 中 ){  
          u 加入 ε-closure(T);  
          把 u 入栈;  
       }  
    }  
}  
  
下面对上图如何使用Set Construction算法来构建DFA做一个详细的描述：  
1. 初始化Dstates 把集合 ε-closure(s0) = {0, 1, 2, 4, 7}作为第一个状态，设此状态为 A  
2. 现在转化，input symbol {a, b}，因此，求：  
ε-closure(move(A, a));  
ε-closure(move(A, b));  
这里会得到2个状态  
ε-closure(move(A, a)) = {1, 2, 3, 4, 6, 7, 8},设其为 B  
ε-closure(move(A, b)) = {1, 2, 4, 5, 6, 7}, 设其为C  
B，C放入Dstates  
改写 Dtrans  
  
最终得到的 Dtrans 为：  
A = {0, 1, 2, 4, 7}  
B = {1, 2, 3, 4, 6, 7, 8}  
C = {1, 2, 4, 5, 6, 7}  
D = {1, 2, 4, 5, 6, 7, 9}  
[![clip_image009](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image009_thumb.jpg "按此在新窗口打开图片")](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image009_2.jpg)  
  
因此，NFA转化成为DFA：  
[![clip_image010](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image010_thumb.jpg "按此在新窗口打开图片")](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image010_2.jpg)

**词法分析(5)---从正规式到NFA**

在说到这个问题前，先告诉大家，我们可以直接从 Regular expression 到 DFA，不过这里我们先不讨论这个问题  
  
关于RE到DFA的算法有很多，这里学习一个最简单的  
  
Algorithm Thompson's construction：  
Input : 一个字母表(**Σ**)上的 Regular Experssion r  
Output : 一个接受 L(r) 的 NFA N  
Method : 把 r 解析成为子表达式(subexpressions)，然后使用下面的1),2)规则，为 r 中的基本符号(basic symbols,基本符号就是ε和**Σ**中的字符)构建NFA，基本符号符合1),2)关于正规式的定义，注意，假如symbol a 出现多次，那么它每次出现都要构建一个NFA。之后，我们需要通过 r 的语法结构，通过规则3)组合前面构建的NFA，直到得到整个NFA为止。对于中间产生的NFA，它只有一个终态，没有进入开始装状态的边，也没有离开接受状态的边。  
1) 对于 ε 构造如下NFA  
[![clip_image011](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image011_thumb.jpg "按此在新窗口打开图片")](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image011_2.jpg)  
注意，每次构建时，i,f的值都不一样，因此可见构造一个识别 ε 的NFA，会产生2个新的状态  
  
2) 对于Σ中的每个字符a  
[![clip_image012](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image012_thumb.jpg "按此在新窗口打开图片")](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image012_2.jpg)  
同样，对于aaa，第一个a构造的NFA中的i,f不会和第2个a构造的i,f一样，因此可见构造一个识别Σ中的每个字符a 的NFA，会产生2个新的状态  
  
3) 先假定 N(t) N(s) 分别是 t s 的NFA，则：  
    a) 对于表达式 s|t 构建 NFA N(s|t)  
    [![clip_image013](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image013_thumb.jpg "按此在新窗口打开图片")](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image013_2.jpg)  
    这里一样会产生2个新的状态i,j，我们看其中一个N(s)，左边的圆圈，表示N(s)的开始状态，右边的圆圈表示N(s)的接受状态，N(t)同理  
    b) 对于表达式 st ,构建N(st)  
    [![clip_image014](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image014_thumb.jpg "按此在新窗口打开图片")](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image014_2.jpg)  
    这个时候，不产生新的状态，N(s)的开始状态变为N(st)的开始状态，N(t)的接受状态变成N(st)的接受状态，N(s)的接受状态和N(t)开始状态成为一个状态。这里提醒一下，写程序的时候，这里千万要注意，因为没有新的状态产生，必须考虑状态的部分复制，如果不小心就会出错。  
    c) 对于正规式 s\*，构造N(s\*)  
    [![clip_image015](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image015_thumb.jpg "按此在新窗口打开图片")](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image015_2.jpg)  
    这里一样需要产生2个新的状态i,f，注意，产生了一条N(s)接受状态到N(s)开始状态的边，边上的symbol为 ε  
    d) 对于(s)，使用N(s)本身作为它的NFA，也就是不用构造新的NFA  
  
注意一下，以上产生的NFA，有以下性质：  
1) 只有一个接受状态和一个开始状态  
2) 每个状态最多含有2个指向其他状态的边，详细的来说，如果状态只有一条指向其他状态的边，那么边上的symbol为**Σ**中的任意字符或者ε，如果状态有两条指向其他状态的边，那么边上的symbol一定为2个ε  
  
由以上性质，我们可以很好的选择数据结构来表示NFA

**词法分析(6)---DFA的化简**

通过NFA转化而成的DFA不一定是最简的，也就是说，有多余的状态可以被删除，对于每一个正规定义，我们一定可以得到一个唯一的最简的DFA

我们回顾一下Move函数，DFA的move函数：

move : (state, symbol) -> S

注意，这里(state, symbol)表示的是一个集合，这里规范的数学表达应该是：

move : { (state, symbol) | 所有属于DFA的state和symbol } -> S 或者

move : S × Σ -> S

假如一个DFA的move函数不是全函数，那么必须引入死状态。假如某个DFA的move函数是全函数，那么每个状态在所有input symbol下都有出边，比如：

[![clip_image016](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image016_thumb.jpg "按此在新窗口打开图片")](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image016_2.jpg)

这个DFA每个状态都可以接受所有的input symbol，这里是a，b。而下面的DFA：

[![clip_image017](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image017_thumb.jpg "按此在新窗口打开图片")](http://www.cppblog.com/images/cppblog_com/woaidongmao/WindowsLiveWriter/NFADFA_10EE6/clip_image017_2.jpg)

先不要看红色部分，那么这个DFA的状态c，d，它们无法通过input symbol b 进入下一个状态，我们可以加上红色的部分，把这个move函数，转化成为一个全函数，并且，经过转化操作之后，新的DFA与原DFA等价。这个红色部分标识的状态，被叫做死状态

死状态：

假如出现DFA的move函数不是全函数，我们可以引入一个死状态S(仅仅引入一个方可)，这个状态包括所有input symbol对自身的转换，所有的其他状态假如不接受某个input symbol a，那么，我们建立这个状态到S且input symbol为 a 的边。

状态的区别：

假如一个状态s，通过input string w，可以转换到某个状态，而某个状态t，通过w，转化到了一个与s通过w转化到的状态不同的状态，那么我们就可以通过w来区别状态s，t，如果这样的w不存在，那么s，t这2个状态是无法区别的。

每个接受状态都可以通过ε和非接受状态进行区别。

化简算法，极小化DFA的思想：

极小化DFA算法，它把状态分成一些不相交的子集，每一个子集中的所有状态都是不可区别的，而不同子集中的每个状态两两都是可区别的，最后我们把每个子集中的所有状态合成一个状态。

1) 划分状态集

首先把所有状态划分成为2个集合，一个集合是接受状态的集合，一个集合是非接受状态的集合，他们通过ε来区别。然后看每个集合中的状态时候还可以区别，例如一个集合通过input symbol a，转换后得到的状态落入当前划分的不同集合，那么说明通过input symbol a，是可以区别这个集合中的状态的(这里要强调的是，对于一个而不是多个input symbol，假如转换到的状态落入不同的划分中那么这些状态就是可以区别的)。我们假定有一个状态集合{s1,s2},s1通过a到达状态集合t1，s2通过a到达状态集合t2，t1,t2分别是当前划分的状态集合，那么，集合{s1,s2}就可以分成2个集合{s1},{s2}

2) 构造最简的DFA

我们可以重复1)的步骤，最后得到一些子集合，我们从每个子集合中取一个状态，通过它们可以得到最简的DFA，但具体需要按一定规则去构建

极小化DFA状态数的算法：

Input : 一个DFA M，它的状态集是S，输入符号集合Σ，move : S × Σ -> S，开始状态为s0，接受状态的集合为F

Output : 一个DFA N，它和DFA M等价，并为最简

Method :

1) 初始化: 假如move函数不是全函数，那么加入死状态，构造划分X：把S分成2个子集合，包括接受状态集合F和非接受状态集合S-F(F集合的补集)

2) Xnew是一个划分

for( X 中的每个集合G ){

    G中状态每次通过Σ中的symbol转化到的状态如果属于X的不同子集，那么把集合G分成子集，每个symbol都可能划分G，划分之后，使用下一个symbol进行操作，一直到遍历完所有的input symbol

    更新Xnew，用G的划分代替G

}

3) 如果Xnew == X，那么定义 Xfinal = X，执行4)，否则进行赋值操作 X = Xnew，进行2)

4) Xfinal中每个子集合中选择一个状态来代表这个状态集合，包含s0的状态集合，就是表示开始状态的集合。通过DFA M来构造DFA N，规则是这样的：假如某状态p通过某input symbol a，通过DFA M的move函数转到另外一个状态q，我们就用q所在的集合的代表状态来表示q，并把这个转换过程的边，input symbol，集合的代表状态，加入DFA N中。我们需要遍历DFA M，然后按规则构建DFA N。化简的DFA中，可能有多个接受状态。

5) 如果N中有死状态(终态不是死状态)，去掉它，有开始状态无法到达的状态，也去掉它。注意，在DFA N中有可能出现死状态，也就是通过所有的input symbol都回到自己的状态，前面说过，添加一个死状态得到的新的DFA与原DFA等价，那么我们这里也自然可以删除它。

在真正的实现上面算法的时候，是灵活的，因为出于时间复杂度的考虑，可能并不需要完全照搬上面的算法，把握主要的思想是很重要的。

1) 每个input symbol都可能划分一次集合

2) 每个集合都中的状态被看成是不可区别的，即使在计算过程中某些集合中的状态是可以区别的

3) 一定要确保每个集合都无法在分

  

[关于正则表达式、正则文法、NFA、LR(1)](http://www.cppblog.com/woaidongmao/archive/2009/09/29/97542.html)
------------------------------------------------------------------------------------------

昨天和Sumtec谈到自动机和语法分析，一下子脑子有点混乱，把一些概念搞混了，看了半天清华的编译书也没有整明白...今天早上起来看了《离散数学及其应用》里的自动机一部分，才厘清了头绪。还是外国人的书讲得清楚一点。

昨天主要是把NFA和语法分析中的LL(1) LR(1)搞混了。事实上LL(1)分析也好LR(1)分析也好，使用的是一个基于下推自动机的计算模型，而不是有限自动机。下推自动机的计算能力要比有限自动机强。

其次就是NFA和DFA的计算能力确实是等价的，也就是对于任意一个NFA都可以找到一个与之等价的DFA(可以使用子集法来构造这样一个DFA)。

为了说明有限自动机与LL(1) LR(1)等分析法的关系，先概述一下文法的分类

文法分为四类：

(1)短语文法(0型文法)

(2)上下文相关文法(1型文法)

(3)上下文无关文法(2型文法)

(4)正规(则)文法(3型文法)

上面四种文法有包含的关系，1型文法是0型文法的一个子集，2型文法是1型文法的一个子集，,3型文法是2型文法的一个子集。

我们主要研究2型和3型方法。

3型文法(正则文法)与正则表达式(Regular Expression)是等价的，任意一个正则文法总是可以转化成一个等价的正则表达式。同时正则表达式与有限自动机是等价的。一个能由有限自动机识别的语言，必然可以用正则表达式来表示，而一个用正则表达式表示的语言一定可以用一个有限自动机来识别。

但是正则文法不足以描述程序设计语言(比如，不能用正则表达式定义带有括号的数学表达式)，现在流行的程序设计语言如C#, java等都是用2型文法，也就是上下文无关文法来定义的。因此有限自动机没有能力来识别程序设计语言(最后我会举个例子)。因此提出来下推自动机的模型。下推自动机具有限自动机的所有部件，如状态、状态转移表等，同时它比有限自动机多一个堆栈，常称为计算栈。下推自动机可以根据情况将终结符或者非终结符压入栈，或者弹出栈。

而LL(1)，LR(1)等分析法就是用来分析上下文无关文法的，基于下推自动机的模型。这也是为什么介绍语法分析时，所有的书都会说一个基于LR(1)分析法的预测分析器，都会有三部分组成：状态转移表、控制器和计算栈。而所谓的移进与归约就是入栈与出栈的问题。

最后，举一个例子(好象大家都睡着了 -\_-b)

先给出一个文法：

S->0S1 | 01

其中0、1是终结符。

这样一个文法描述的语言其实就是n个0加上相等数量的n个1，这里n是某个整数。

这个文法是一个上下文无关文法，但不是一个正则文法。所以说我们没办法写出一个正则表达式来描述这样一个语言。等于一个能识别这个文法中的任意句子的NFA，我们总能找到这样一个句子，它不是由该文法所定义的，却能被这个NFA接受。换句话说，任意NFA都不能用来判断某个句子是不是由以上这个文法所定义。说得实际一点，如果要求写一个着色程序，输入的文件是一串0、1组成的序列，要求把其中n个0加n个1的序列用红色着色，而其它用黑色的话，我们就不能光用正则表达式匹配来完成这一任务了。

如果上面这个例子还比较抽象的话，那么对于“带有括号的数学表达式”这样一个语言，也是没有办法用正则表达式来进行匹配的。因为描述“带有括号的数学表达式”的文法，也不是一个正则文法，因为其中带有类似：

F->(E)

这样的部分。

而正则文法要求所有的产生式都必须是A->aB或者A->a这样的形式的(其中A、B是非终结符，a是终结符)