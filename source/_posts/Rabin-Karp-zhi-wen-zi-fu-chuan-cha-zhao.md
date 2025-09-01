---
title: Rabin-Karp指纹字符串查找算法
id: 1502
date: 2024-10-31 22:01:58
author: daichangya
permalink: /archives/Rabin-Karp-zhi-wen-zi-fu-chuan-cha-zhao/
tags:
- 算法
---


首先计算模式字符串的散列函数, 如果找到一个和模式字符串散列值相同的子字符串, 那么继续验证两者是否匹配.

这个过程等价于将模式保存在一个散列表中, 然后在文本中的所有子字符串查找. 但不需要为散列表预留任何空间, 因为它只有一个元素.

**基本思想**

长度为M的字符串对应着一个R进制的M位数, 为了用一张大小为Q的散列表来保存这种类型的键, 需要一个能够将R进制的M位数转化为一个0到Q-1之间的int值散列函数, 这里可以用除留取余法.

举个例子, 需要在文本 3 1 4 1 5 9 2 6 5 3 5 8 9 7 9 3 查找模式 2 6 5 3 5， 这里R=10， 取Q=997, 则散列值为

2 6 5 3 6 % 997 = 613

然后计算文本中所有长度为5的子字符串并寻找匹配

3 1 4 1 5 % 997 = 508

1 4 1 5 9 % 997 = 201

......

2 6 5 3 6 % 997 = 613 (匹配)

**计算散列函数**

对于5位的数值, 只需要使用int就可以完成所有需要的计算, 但是当模式长度太大时, 我们使用Horner方法计算模式字符串的散列值

2 % 997 = 2

2 6 % 997 = (2*10 + 6) % 997 = 26

2 6 5 % 997 = (26*10 + 5) % 997 = 265

2 6 5 3 % 997 = (265*10 + 3) % 997 = 659

2 6 5 3 5 % 997 = (659*10 + 5) % 997 = 613

这里关键的一点就是在于不需要保存这些数的值, 只需保存它们除以Q之后的余数.

取余操作的一个基本性质是如果每次算术操作之后都将结果除以Q并取余, 这等价于在完成所有算术操作之后再将最后的结果除以Q并取余.

**算法实现**

3 1 4 1 5 9 2 6 5 3 5 8 9 7 9 3

3 % 997 = 3

3 1 % 997 = (3*10 + 1) %997 = 31

3 1 4 % 997 = (31*10 + 4) % 997 = 314

3 1 4 1 % 997 = (314*10 + 1) % 997 = 150

3 1 4 1 5 % 997 = (150*10 + 5) % 997 = 508

   1 4 1 5 9 % 997 = ( (508 + 3*(997 - 30) ) *10 + 9) % 997 = 201

      4 1 5 9 2 % 997 = ( (201 + 1*(997 - 30) ) *10 + 2) % 997 = 715

　　　　......

　　           2 6 5 3 6 % 997 =  ( (929 + 9*(997 - 30) ) *10 + 5) % 997 = 613

构造函数为模式字符串计算了散列值patHash并在变量中保存了R^(M-1) mod Q的值, hashSearch()计算了文本前M个字母的散列值并和模式字符串的散列值比较, 如果没有匹配, 文本指针继续下移一位, 计算新的散列值再次比较,知道成功或结束.

```
import java.math.BigInteger;
import java.util.Random;

import edu.princeton.cs.algs4.StdOut;

public class RabinKarp {
    private String pat;    //模式字符串
    private long patHash;    //模式字符串散列值
    private int M;     //模式字符串的长度
    private long Q;    //很大的素数
    private int R;    //字母表的大小
    private long RM;    //R^(M-1) % Q

    public RabinKarp(char[] pat, int R){
        this.pat = String.valueOf(pat);
        this.R = R;
    }
    
    public RabinKarp(String pat){
        this.pat = pat;
        R = 256;
        M = pat.length();
        Q = longRandomPrime();
        
        RM = 1;
        for(int i=1; i<=M-1; i++){
            RM = (R * RM) % Q;
        }
        patHash = hash(pat, M);
    }
    
    private long hash(String str, int M){
        long h = 0;
        for(int i=0; i < M; i++){
            h = (R * h + str.charAt(i)) % Q;
        }
        return h;
    }
    
    public boolean check(String txt,int i){
        for(int j = 0; j < M; j++){
            if(pat.charAt(j) != txt.charAt(i+j))
            return false;
        }
        return true;
    }
    
    private static long longRandomPrime() {
        BigInteger prime = BigInteger.probablePrime(31, new Random());
        return prime.longValue();
    }
    
    private int search(String txt){
        int N = txt.length();
        if(N < M) return N;
        long txtHash = hash(txt,M);
        
        if((txtHash == patHash) && check(txt, 0)) return 0;
        for(int i = M; i < N; i++){
            txtHash = (txtHash + Q - RM*txt.charAt(i-M) % Q) % Q;
            txtHash = (txtHash*R + txt.charAt(i)) % Q;
            int offset = i-M+1;
            if((patHash == txtHash) && check(txt, offset))
                return offset;
        }
        return N;
    }
    
    public static void main(String[] args) {
        String pat = args[0];
        String txt = args[1];

        RabinKarp searcher = new RabinKarp(pat);
        int offset = searcher.search(txt);
        // print results
        StdOut.println("text:    " + txt);

        // from brute force search method 1
        StdOut.print("pattern: ");
        for (int i = 0; i < offset; i++)
            StdOut.print(" ");
        StdOut.println(pat);
    }
}
```

上面代码中的求模运算的方法可以参考初数论里面的同模定理.

