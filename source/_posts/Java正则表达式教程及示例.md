---
title: Java正则表达式教程及示例
id: 1046
date: 2024-10-31 22:01:48
author: daichangya
excerpt: "当我开始我的Java职业生涯的时候，对于我来说正则表达式简直是个是梦魇。本教程旨在帮助你驾驭Java正则表达式，同时也帮助我复习正则表达式"
permalink: /archives/19083979/
tags: 
 - 正则表达式
---

 当我开始我的Java职业生涯的时候，对于我来说正则表达式简直是个是梦魇。本教程旨在帮助你驾驭Java正则表达式，同时也帮助我复习正则表达式。

## 什么是正则表达式?

正则表达式定义了字符串的模式。正则表达式可以用来搜索、编辑或处理文本。正则表达式并不仅限于某一种语言，但是在每种语言中有细微的差别。Java正则表达式和Perl的是最为相似的。

Java正则表达式的类在 java.util.regex 包中，包括三个类：Pattern,Matcher 和 PatternSyntaxException。

1.  Pattern对象是正则表达式的已编译版本。他没有任何公共构造器，我们通过传递一个正则表达式参数给公共静态方法 compile 来创建一个pattern对象。
2.  Matcher是用来匹配输入字符串和创建的 pattern 对象的正则引擎对象。这个类没有任何公共构造器，我们用patten对象的matcher方法，使用输入字符串作为参数来获得一个Matcher对象。然后使用matches方法，通过返回的布尔值判断输入字符串是否与正则匹配。
3.  如果正则表达式语法不正确将抛出PatternSyntaxException异常。

让我们在一个简单的例子里看看这些类是怎么用的吧

```java
package com.journaldev.util;
 
import java.util.regex.Matcher;
import java.util.regex.Pattern;
 
public class RegexExamples {
 
    public static void main(String[] args) {
        // using pattern with flags
        Pattern pattern = Pattern.compile("ab", Pattern.CASE_INSENSITIVE);
        Matcher matcher = pattern.matcher("ABcabdAb");
        // using Matcher find(), group(), start() and end() methods
        while (matcher.find()) {
            System.out.println("Found the text \"" + matcher.group()
                    + "\" starting at " + matcher.start()
                    + " index and ending at index " + matcher.end());
        }
 
        // using Pattern split() method
        pattern = Pattern.compile("\\W");
        String[] words = pattern.split("one@two#three:four$five");
        for (String s : words) {
            System.out.println("Split using Pattern.split(): " + s);
        }
 
        // using Matcher.replaceFirst() and replaceAll() methods
        pattern = Pattern.compile("1*2");
        matcher = pattern.matcher("11234512678");
        System.out.println("Using replaceAll: " + matcher.replaceAll("_"));
        System.out.println("Using replaceFirst: " + matcher.replaceFirst("_"));
    }
 
}
```

  
  
  
  

上述程序的输出是：

Input String matches regex - true
Exception in thread "main" java.util.regex.PatternSyntaxException: Dangling meta character '*' near index 0
\*xx\*
^
	at java.util.regex.Pattern.error(Pattern.java:1924)
	at java.util.regex.Pattern.sequence(Pattern.java:2090)
	at java.util.regex.Pattern.expr(Pattern.java:1964)
	at java.util.regex.Pattern.compile(Pattern.java:1665)
	at java.util.regex.Pattern.(Pattern.java:1337)
	at java.util.regex.Pattern.compile(Pattern.java:1022)
	at com.journaldev.util.PatternExample.main(PatternExample.java:13)

既然正则表达式总是和字符串有关， Java 1.4对String类进行了扩展，提供了一个matches方法来匹配pattern。在方法内部使用Pattern和Matcher类来处理这些东西，但显然这样减少了代码的行数。

Pattern类同样有matches方法，可以让正则和作为参数输入的字符串匹配，输出布尔值结果。

下述的代码可以将输入字符串和正则表达式进行匹配。

<table border="0" cellpadding="0" cellspacing="0" style="width:622px;border-spacing:1px;border:0px !important;font-size:12px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><tbody style="margin-left:0px !important;border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><tr style="margin-left:0px !important;border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><td class="gutter" style="border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;font-family:Consolas, 'Bitstream Vera Sans Mono', 'Courier New', Courier, monospace !important;min-height: !important;color:rgb(175,175,175) !important;"><div class="line number1 index0 alt2" style="border-width:0px 3px 0px 0px !important;border-right-style:solid !important;border-right-color:rgb(108,226,108) !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;text-align:right !important;min-height: !important;">1</div><div class="line number2 index1 alt1" style="border-width:0px 3px 0px 0px !important;border-right-style:solid !important;border-right-color:rgb(108,226,108) !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;text-align:right !important;min-height: !important;">2</div><div class="line number3 index2 alt2" style="margin-left:0px !important;border-width:0px 3px 0px 0px !important;border-right-style:solid !important;border-right-color:rgb(108,226,108) !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;text-align:right !important;min-height: !important;">3</div></td><td class="code" style="width:591px;margin-left:0px !important;border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;font-family:Consolas, 'Bitstream Vera Sans Mono', 'Courier New', Courier, monospace !important;min-height: !important;"><div style="margin-left:0px !important;border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><div class="line number1 index0 alt2" style="border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><code class="java plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">String str = </code><code class="java string" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:#0000FF !important;">"bbb"</code><code class="java plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">;</code></div><div class="line number2 index1 alt1" style="border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><code class="java plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">System.out.println(</code><code class="java string" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:#0000FF !important;">"Using String matches method: "</code><code class="java plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">+str.matches(</code><code class="java string" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:#0000FF !important;">".bb"</code><code class="java plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">));</code></div><div class="line number3 index2 alt2" style="margin-left:0px !important;border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><code class="java plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">System.out.println(</code><code class="java string" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:#0000FF !important;">"Using Pattern matches method: "</code><code class="java plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">+Pattern.matches(</code><code class="java string" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:#0000FF !important;">".bb"</code><code class="java plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">, str));</code></div></div></td></tr></tbody></table>

所以如果你的需要仅仅是检查输入字符串是否和pattern匹配，你可以通过调用String的matches方法省下时间。只有当你需要操作输入字符串或者重用pattern的时候，你才需要使用Pattern和Matches类。

注意由正则定义的pattern是从左至右应用的，一旦一个原字符在一次匹配中使用过了，将不会再次使用。

例如，正则“121”只会匹配两次字符串“31212142121″，就像这样“\_121\_\_\_\_121″。

## 正则表达式通用匹配符号

<table width="728" border="0" cellspacing="0" cellpadding="0" style="border:0px;font-size:14px;vertical-align:baseline;border-spacing:1px;color:rgb(25,25,25);font-family:'微软雅黑', Verdana, sans-serif, '宋体';line-height:22px;"><thead style="border:0px;vertical-align:baseline;"><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="72" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
正则表达式</p>
</td>
<td valign="bottom" width="144" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
说明</p>
</td>
<td valign="bottom" width="216" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
示例</p>
</td>
</tr></thead><tbody style="border:0px;vertical-align:baseline;"><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="72" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
.</p>
</td>
<td valign="bottom" width="144" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
Matches any single sign, includes everything</p>
<p align="center" style="border:0px;vertical-align:baseline;">
匹配任何单个符号，包括所有字符</p>
</td>
<td valign="bottom" width="216" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
(“..”, “a%”) – true(“..”, “.a”) – true</p>
<p align="center" style="border:0px;vertical-align:baseline;">
(“..”, “a”) – false</p>
</td>
</tr><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="72" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
^xxx</p>
</td>
<td valign="bottom" width="144" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
在开头匹配正则xxx</p>
</td>
<td valign="bottom" width="216" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
(“^a.c.”, “abcd”) – true(“^a”, “a”) – true</p>
<p align="center" style="border:0px;vertical-align:baseline;">
(“^a”, “ac”) – false</p>
</td>
</tr><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="72" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
xxx$</p>
</td>
<td valign="bottom" width="144" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
在结尾匹配正则xxx</p>
</td>
<td valign="bottom" width="216" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
&nbsp;(“..cd$”, “abcd”) – true(“a$”, “a”) – true</p>
<p align="center" style="border:0px;vertical-align:baseline;">
(“a$”, “aca”) – false</p>
</td>
</tr><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="72" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
[abc]</p>
</td>
<td valign="bottom" width="144" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
能够匹配字母a,b或c。[]被称为character classes。</p>
</td>
<td valign="bottom" width="216" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
&nbsp;(“^[abc]d.”, “ad9″) – true(“[ab].d$”, “bad”) – true</p>
<p align="center" style="border:0px;vertical-align:baseline;">
(“[ab]x”, “cx”) – false</p>
</td>
</tr><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="72" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
[abc][12]</p>
</td>
<td valign="bottom" width="144" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
能够匹配由1或2跟着的a,b或c</p>
</td>
<td valign="bottom" width="216" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
(“[ab][12].”, “a2#”) – true(“[ab]..[12]“, “acd2″) – true</p>
<p align="center" style="border:0px;vertical-align:baseline;">
(“[ab][12]“, “c2″) – false</p>
</td>
</tr><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="72" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
[^abc]</p>
</td>
<td valign="bottom" width="144" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
当^是[]中的第一个字符时代表取反，匹配除了a,b或c之外的任意字符。</p>
</td>
<td valign="bottom" width="216" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
(“[^ab][^12].”, “c3#”) – true(“[^ab]..[^12]“, “xcd3″) – true</p>
<p align="center" style="border:0px;vertical-align:baseline;">
(“[^ab][^12]“, “c2″) – false</p>
</td>
</tr><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="72" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
[a-e1-8]</p>
</td>
<td valign="bottom" width="144" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
匹配a到e或者1到8之间的字符</p>
</td>
<td valign="bottom" width="216" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
(“[a-e1-3].”, “d#”) – true(“[a-e1-3]“, “2″) – true</p>
<p align="center" style="border:0px;vertical-align:baseline;">
(“[a-e1-3]“, “f2″) – false</p>
</td>
</tr><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="72" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
xx|yy</p>
</td>
<td valign="bottom" width="144" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
匹配正则xx或者yy</p>
</td>
<td valign="bottom" width="216" style="border:0px;font-size:14px;vertical-align:baseline;">
<p align="center" style="border:0px;vertical-align:baseline;">
(“x.|y”, “xa”) – true(“x.|y”, “y”) – true</p>
<p align="center" style="border:0px;vertical-align:baseline;">
(“x.|y”, “yz”) – false</p>
</td>
</tr></tbody></table>
## Java正则表达式元字符

<table width="728" border="0" cellspacing="0" cellpadding="0" style="border:0px;font-size:14px;vertical-align:baseline;border-spacing:1px;color:rgb(25,25,25);font-family:'微软雅黑', Verdana, sans-serif, '宋体';line-height:22px;"><tbody style="border:0px;vertical-align:baseline;"><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="78" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">正则表达式</p></td><td valign="bottom" width="366" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">说明</p></td></tr><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="78" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">\d</p></td><td valign="bottom" width="366" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">任意数字，等同于[0-9]</p></td></tr><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="78" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">\D</p></td><td valign="bottom" width="366" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">任意非数字，等同于[^0-9]</p></td></tr><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="78" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">\s</p></td><td valign="bottom" width="366" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">任意空白字符，等同于[\t\n\x0B\f\r]</p></td></tr><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="78" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">\S</p></td><td valign="bottom" width="366" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">任意非空白字符，等同于[^\s]</p></td></tr><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="78" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">\w</p></td><td valign="bottom" width="366" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">任意英文字符，等同于[a-zA-Z_0-9]</p></td></tr><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="78" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">\W</p></td><td valign="bottom" width="366" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">任意非英文字符，等同于[^\w]</p></td></tr><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="78" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">\b</p></td><td valign="bottom" width="366" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">单词边界</p></td></tr><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="78" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">\B</p></td><td valign="bottom" width="366" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">非单词边界</p></td></tr></tbody></table>

有两种方法可以在正则表达式中像一般字符一样使用元字符。

1.  在元字符前添加反斜杠(\\)
2.  将元字符置于\\Q(开始引用)和\\E(结束引用)间

## 正则表达式量词

量词指定了字符匹配的发生次数。

<table width="728" border="0" cellspacing="0" cellpadding="0" style="border:0px;font-size:14px;vertical-align:baseline;border-spacing:1px;color:rgb(25,25,25);font-family:'微软雅黑', Verdana, sans-serif, '宋体';line-height:22px;"><tbody style="border:0px;vertical-align:baseline;"><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="77" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">正则表达式</p></td><td valign="bottom" width="365" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">说明</p></td></tr><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="77" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">x?</p></td><td valign="bottom" width="365" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">x没有出现或者只出现一次</p></td></tr><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="77" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">X*</p></td><td valign="bottom" width="365" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">X出现0次或更多</p></td></tr><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="77" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">X+</p></td><td valign="bottom" width="365" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">X出现1次或更多</p></td></tr><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="77" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">X{n}</p></td><td valign="bottom" width="365" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">X正好出现n次</p></td></tr><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="77" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">X{n,}</p></td><td valign="bottom" width="365" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">X出席n次或更多</p></td></tr><tr style="border:0px;vertical-align:baseline;"><td valign="bottom" width="77" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">X{n,m}</p></td><td valign="bottom" width="365" style="border:0px;font-size:14px;vertical-align:baseline;"><p align="center" style="border:0px;vertical-align:baseline;">X出现至少n次但不多于m次</p></td></tr></tbody></table>

量词可以和character classes和capturing group一起使用。

例如，\[abc\]+表示a,b或c出现一次或者多次。

 (abc)+表示capturing group “abc”出现一次或多次。我们即将讨论capturing group。

## 正则表达式capturing group

Capturing group是用来对付作为一个整体出现的多个字符。你可以通过使用()来建立一个group。输入字符串中和capturing group相匹配的部分将保存在内存里，并且可以通过使用Backreference调用。

你可以使用matcher.groupCount方法来获得一个正则pattern中capturing groups的数目。例如((a)(bc))包含3个capturing groups; ((a)(bc)), (a) 和 (bc)。

你可以使用在正则表达式中使用Backreference，一个反斜杠(\\)接要调用的group号码。

Capturing groups和Backreferences可能很令人困惑，所以我们通过一个例子来理解。

<table border="0" cellpadding="0" cellspacing="0" style="width:615px;border-spacing:1px;border:0px !important;font-size:12px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><tbody style="margin-left:0px !important;border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><tr style="margin-left:0px !important;border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><td class="gutter" style="border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;font-family:Consolas, 'Bitstream Vera Sans Mono', 'Courier New', Courier, monospace !important;min-height: !important;color:rgb(175,175,175) !important;"><div class="line number1 index0 alt2" style="border-width:0px 3px 0px 0px !important;border-right-style:solid !important;border-right-color:rgb(108,226,108) !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;text-align:right !important;min-height: !important;">1</div><div class="line number2 index1 alt1" style="border-width:0px 3px 0px 0px !important;border-right-style:solid !important;border-right-color:rgb(108,226,108) !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;text-align:right !important;min-height: !important;">2</div><div class="line number3 index2 alt2" style="border-width:0px 3px 0px 0px !important;border-right-style:solid !important;border-right-color:rgb(108,226,108) !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;text-align:right !important;min-height: !important;">3</div><div class="line number4 index3 alt1" style="margin-left:0px !important;border-width:0px 3px 0px 0px !important;border-right-style:solid !important;border-right-color:rgb(108,226,108) !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;text-align:right !important;min-height: !important;">4</div></td><td class="code" style="width:584px;margin-left:0px !important;border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;font-family:Consolas, 'Bitstream Vera Sans Mono', 'Courier New', Courier, monospace !important;min-height: !important;"><div style="margin-left:0px !important;border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><div class="line number1 index0 alt2" style="border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><code class="java plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">System.out.println(Pattern.matches(</code><code class="java string" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:#0000FF !important;">"(\\w\\d)\\1"</code><code class="java plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">, </code><code class="java string" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:#0000FF !important;">"a2a2"</code><code class="java plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">)); </code><code class="java comments" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:rgb(0,130,0) !important;">//true</code></div><div class="line number2 index1 alt1" style="border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><code class="java spaces" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="java plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">System.out.println(Pattern.matches(</code><code class="java string" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:#0000FF !important;">"(\\w\\d)\\1"</code><code class="java plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">, </code><code class="java string" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:#0000FF !important;">"a2b2"</code><code class="java plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">)); </code><code class="java comments" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:rgb(0,130,0) !important;">//false</code></div><div class="line number3 index2 alt2" style="border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><code class="java spaces" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="java plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">System.out.println(Pattern.matches(</code><code class="java string" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:#0000FF !important;">"(AB)(B\\d)\\2\\1"</code><code class="java plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">, </code><code class="java string" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:#0000FF !important;">"ABB2B2AB"</code><code class="java plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">)); </code><code class="java comments" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:rgb(0,130,0) !important;">//true</code></div><div class="line number4 index3 alt1" style="margin-left:0px !important;border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><code class="java spaces" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="java plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">System.out.println(Pattern.matches(</code><code class="java string" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:#0000FF !important;">"(AB)(B\\d)\\2\\1"</code><code class="java plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">, </code><code class="java string" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:#0000FF !important;">"ABB2B3AB"</code><code class="java plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">)); </code><code class="java comments" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:rgb(0,130,0) !important;">//false</code></div></div></td></tr></tbody></table>

在第一个例子里，运行的时候第一个capturing group是(\\w\\d)，在和输入字符串“a2a2″匹配的时候获取“a2″并保存到内存里。因此\\1是”a2”的引用，并且返回true。基于相同的原因，第二行代码打印false。

试着自己理解第三行和第四行代码。:)

现在我们来看看Pattern和Matcher类中一些重要的方法。

我们可以创建一个带有标志的Pattern对象。例如Pattern.CASE_INSENSITIVE可以进行大小写不敏感的匹配。Pattern类同样提供了和String类相似的split(String) 方法

Pattern类toString()方法返回被编译成这个pattern的正则表达式字符串。

Matcher类有start()和end()索引方法，他们可以显示从输入字符串中匹配到的准确位置。

Matcher类同样提供了字符串操作方法replaceAll(String replacement)和replaceFirst(String replacement)。

现在我们在一个简单的java类中看看这些函数是怎么用的。

```java
package com.journaldev.util;
 
import java.util.regex.Matcher;
import java.util.regex.Pattern;
 
public class RegexExamples {
 
    public static void main(String[] args) {
        // using pattern with flags
        Pattern pattern = Pattern.compile("ab", Pattern.CASE_INSENSITIVE);
        Matcher matcher = pattern.matcher("ABcabdAb");
        // using Matcher find(), group(), start() and end() methods
        while (matcher.find()) {
            System.out.println("Found the text \"" + matcher.group()
                    + "\" starting at " + matcher.start()
                    + " index and ending at index " + matcher.end());
        }
 
        // using Pattern split() method
        pattern = Pattern.compile("\\W");
        String[] words = pattern.split("one@two#three:four$five");
        for (String s : words) {
            System.out.println("Split using Pattern.split(): " + s);
        }
 
        // using Matcher.replaceFirst() and replaceAll() methods
        pattern = Pattern.compile("1*2");
        matcher = pattern.matcher("11234512678");
        System.out.println("Using replaceAll: " + matcher.replaceAll("_"));
        System.out.println("Using replaceFirst: " + matcher.replaceFirst("_"));
    }
 
}
```

  
  

上述程序的输出：

<table border="0" cellpadding="0" cellspacing="0" style="width:570px;border-spacing:1px;border:0px !important;font-size:12px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><tbody style="margin-left:0px !important;border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><tr style="margin-left:0px !important;border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><td class="gutter" style="border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;font-family:Consolas, 'Bitstream Vera Sans Mono', 'Courier New', Courier, monospace !important;min-height: !important;color:rgb(175,175,175) !important;"><div class="line number1 index0 alt2" style="border-width:0px 3px 0px 0px !important;border-right-style:solid !important;border-right-color:rgb(108,226,108) !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;text-align:right !important;min-height: !important;">1</div><div class="line number2 index1 alt1" style="border-width:0px 3px 0px 0px !important;border-right-style:solid !important;border-right-color:rgb(108,226,108) !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;text-align:right !important;min-height: !important;">2</div><div class="line number3 index2 alt2" style="border-width:0px 3px 0px 0px !important;border-right-style:solid !important;border-right-color:rgb(108,226,108) !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;text-align:right !important;min-height: !important;">3</div><div class="line number4 index3 alt1" style="border-width:0px 3px 0px 0px !important;border-right-style:solid !important;border-right-color:rgb(108,226,108) !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;text-align:right !important;min-height: !important;">4</div><div class="line number5 index4 alt2" style="border-width:0px 3px 0px 0px !important;border-right-style:solid !important;border-right-color:rgb(108,226,108) !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;text-align:right !important;min-height: !important;">5</div><div class="line number6 index5 alt1" style="border-width:0px 3px 0px 0px !important;border-right-style:solid !important;border-right-color:rgb(108,226,108) !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;text-align:right !important;min-height: !important;">6</div><div class="line number7 index6 alt2" style="border-width:0px 3px 0px 0px !important;border-right-style:solid !important;border-right-color:rgb(108,226,108) !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;text-align:right !important;min-height: !important;">7</div><div class="line number8 index7 alt1" style="border-width:0px 3px 0px 0px !important;border-right-style:solid !important;border-right-color:rgb(108,226,108) !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;text-align:right !important;min-height: !important;">8</div><div class="line number9 index8 alt2" style="border-width:0px 3px 0px 0px !important;border-right-style:solid !important;border-right-color:rgb(108,226,108) !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;text-align:right !important;min-height: !important;">9</div><div class="line number10 index9 alt1" style="margin-left:0px !important;border-width:0px 3px 0px 0px !important;border-right-style:solid !important;border-right-color:rgb(108,226,108) !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;text-align:right !important;min-height: !important;">10</div></td><td class="code" style="width:532px;margin-left:0px !important;border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;font-family:Consolas, 'Bitstream Vera Sans Mono', 'Courier New', Courier, monospace !important;min-height: !important;"><div style="margin-left:0px !important;border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><div class="line number1 index0 alt2" style="border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><code class="actionscript3 plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">Found the text </code><code class="actionscript3 string" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:#0000FF !important;">"AB"</code> <code class="actionscript3 plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">starting at </code><code class="actionscript3 value" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:rgb(0,153,0) !important;">0</code> <code class="actionscript3 plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">index and ending at index </code><code class="actionscript3 value" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:rgb(0,153,0) !important;">2</code></div><div class="line number2 index1 alt1" style="border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><code class="actionscript3 plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">Found the text </code><code class="actionscript3 string" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:#0000FF !important;">"ab"</code> <code class="actionscript3 plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">starting at </code><code class="actionscript3 value" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:rgb(0,153,0) !important;">3</code> <code class="actionscript3 plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">index and ending at index </code><code class="actionscript3 value" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:rgb(0,153,0) !important;">5</code></div><div class="line number3 index2 alt2" style="border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><code class="actionscript3 plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">Found the text </code><code class="actionscript3 string" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:#0000FF !important;">"Ab"</code> <code class="actionscript3 plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">starting at </code><code class="actionscript3 value" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:rgb(0,153,0) !important;">6</code> <code class="actionscript3 plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">index and ending at index </code><code class="actionscript3 value" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;color:rgb(0,153,0) !important;">8</code></div><div class="line number4 index3 alt1" style="border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><code class="actionscript3 plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">Split using Pattern.split(): one</code></div><div class="line number5 index4 alt2" style="border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><code class="actionscript3 plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">Split using Pattern.split(): two</code></div><div class="line number6 index5 alt1" style="border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><code class="actionscript3 plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">Split using Pattern.split(): three</code></div><div class="line number7 index6 alt2" style="border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><code class="actionscript3 plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">Split using Pattern.split(): four</code></div><div class="line number8 index7 alt1" style="border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><code class="actionscript3 plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">Split using Pattern.split(): five</code></div><div class="line number9 index8 alt2" style="border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><code class="actionscript3 plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">Using replaceAll: _345_678</code></div><div class="line number10 index9 alt1" style="margin-left:0px !important;border:0px !important;vertical-align:baseline !important;line-height:1.1em !important;overflow:visible !important;min-height: !important;"><code class="actionscript3 plain" style="line-height:24px;font-family:'Lucida console';border:0px !important;vertical-align:baseline !important;overflow:visible !important;min-height: !important;">Using replaceFirst: _34512678</code></div></div></td></tr></tbody></table>

原文链接： [journaldev](http://www.journaldev.com/634/java-regular-expression-tutorial-with-examples) 