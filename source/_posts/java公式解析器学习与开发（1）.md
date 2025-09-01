---
title: java公式解析器学习与开发（1）
id: 587
date: 2024-10-31 22:01:44
author: daichangya
excerpt: ""
permalink: /archives/12915313/
categories:
 - 解释器
---

 

```java
public class Evaluate {
    public static void main(String[] args) { 
        Stack<String> ops  = new Stack<String>();
        Stack<Double> vals = new Stack<Double>();
        String[] strs = "( 1 + ( ( 2 + 3 ) * ( 4 * 5 ) ) )".split(" ");
        int i = 0;
        while (i<strs.length) {
            String s = strs[i];
            if      (s.equals("("))               ;
            else if (s.equals("+"))    ops.push(s);
            else if (s.equals("-"))    ops.push(s);
            else if (s.equals("*"))    ops.push(s);
            else if (s.equals("/"))    ops.push(s);
            else if (s.equals("sqrt")) ops.push(s);
            else if (s.equals(")")) {
                String op = ops.pop();
                double v = vals.pop();
                if      (op.equals("+"))    v = vals.pop() + v;
                else if (op.equals("-"))    v = vals.pop() - v;
                else if (op.equals("*"))    v = vals.pop() * v;
                else if (op.equals("/"))    v = vals.pop() / v;
                else if (op.equals("sqrt")) v = Math.sqrt(v);
                vals.push(v);
            }
            else vals.push(Double.parseDouble(s));
            i++;
        }
        System.out.println(vals.pop());
    }
}
```

简单的算术表达式计算，上面的程序必须添加括号，而且各个分词之间必须有空格，这样才能区分出计算结构。

中缀表达式是人们常用的算术表示方法，中缀记法中括号是必需的。计算过程中必须用括号将操作符和对应的操作数括起来，用于指示运算的次序。