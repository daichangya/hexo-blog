---
title: HashMap vs ConcurrentHashMap — 示例及Iterator探秘
id: 1037
date: 2024-10-31 22:01:48
author: daichangya
excerpt: "如果你是一名Java开发人员，我能够确定你肯定知道ConcurrentModificationException，它是在使用迭代器遍历集合对象时修改集合对象造成的（并发修改）异常。实际上，Java的集合框架是[迭代器设计模式](http//www.journaldev.com/1716/iterator-design-pattern-in-java-example-tutorial)的一个很好的实现。"
permalink: /archives/18564841/
categories:
 - java并发教程
---

如果你是一名Java开发人员，我能够确定你肯定知道ConcurrentModificationException，它是在使用迭代器遍历集合对象时修改集合对象造成的（并发修改）异常。实际上，Java的集合框架是[迭代器设计模式](http://www.journaldev.com/1716/iterator-design-pattern-in-java-example-tutorial)的一个很好的实现。

Java 1.5引入了_java.util.concurrent_包，其中[Collection类](http://www.journaldev.com/1260/java-collections-framework-tutorial)的实现允许在运行过程中修改集合对象。

_ConcurrentHashMap_是一个与HashMap很相似的类，但是它支持在运行时修改集合对象。

让我们通过一个简单的程序来帮助理解：

**ConcurrentHashMapExample.java**
```
package com.journaldev.util;

import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class ConcurrentHashMapExample {

    public static void main(String\[\] args) {

        //ConcurrentHashMap
        Map<String,String\> myMap= new ConcurrentHashMap<String,String\>();
        myMap.put("1", "1");
        myMap.put("2", "1");
        myMap.put("3", "1");
        myMap.put("4", "1");
        myMap.put("5", "1");
        myMap.put("6", "1");
        System.out.println("ConcurrentHashMap before iterator: "+myMap);
        Iterator<String\> it= myMap.keySet().iterator();

        while(it.hasNext()){
            String key= it.next();
            if(key.equals("3")) myMap.put(key+"new", "new3");
        }
        System.out.println("ConcurrentHashMap after iterator: "+myMap);

        //HashMap
        myMap= new HashMap<String,String\>();
        myMap.put("1", "1");
        myMap.put("2", "1");
        myMap.put("3", "1");
        myMap.put("4", "1");
        myMap.put("5", "1");
        myMap.put("6", "1");
        System.out.println("HashMap before iterator: "+myMap);
        Iterator<String\> it1= myMap.keySet().iterator();

        while(it1.hasNext()){
            String key= it1.next();
            if(key.equals("3")) myMap.put(key+"new", "new3");
        }
        System.out.println("HashMap after iterator: "+myMap);
    }

}
```
当我们试着运行上面的程序，输出如下：
```
ConcurrentHashMap before iterator: {1=1, 5=1, 6=1, 3=1, 4=1, 2=1}
ConcurrentHashMap after iterator: {1=1, 3new=new3, 5=1, 6=1, 3=1, 4=1, 2=1}
HashMap before iterator: {3=1, 2=1, 1=1, 6=1, 5=1, 4=1}
Exception in thread "main" java.util.ConcurrentModificationException
    at java.util.HashMap$HashIterator.nextEntry(HashMap.java:793)
    at java.util.HashMap$KeyIterator.next(HashMap.java:828)
    at com.test.ConcurrentHashMapExample.main(ConcurrentHashMapExample.java:44)
```
查看输出，很明显ConcurrentHashMap可以支持向map中添加新元素，而HashMap则抛出了ConcurrentModificationException。

查看异常堆栈记录，可以发现是下面这条语句抛出异常：
```
String key= it1.next();
```
这就意味着新的元素在HashMap中已经插入了，但是在迭代器执行时出现错误。事实上，集合对象的迭代器提供快速失败（Fail-Fast）的机制，即修改集合对象结构或者元素数量都会使迭代器触发这个异常。

但是迭代器是怎么知道HashMap被修改了呢，我们可以一次取出HashMap的所有Key然后进行遍历。

HashMap包含一个修改计数器，当你调用它的next()方法来获取下一个元素时，迭代器将会用到这个计数器。

**HashMap.java**
```
/**
 * HashMap结构的修改次数
 * 结构修改是指：改变了HashMap中mapping的个数或者其中的内部结构（比如，重新计算hash值）
 * 这个字段在通过Collection操作Hashmap时提供快速失败（Fail-fast）功能。
 * （参见 ConcurrentModificationException）。
 */
transient volatile int modCount;
```
现在为了证明上面的观点，我们对原来的代码做一点修改，使迭代器在插入新的元素后跳出循环。只要在调用put方法后增加一个break：
```
if(key.equals("3")){
    myMap.put(key+"new", "new3");
    break;
}
```
再执行修改后的代码，会得到下面的输出结果：
```
ConcurrentHashMap before iterator: {1=1, 5=1, 6=1, 3=1, 4=1, 2=1}
ConcurrentHashMap after iterator: {1=1, 3new=new3, 5=1, 6=1, 3=1, 4=1, 2=1}
HashMap before iterator: {3=1, 2=1, 1=1, 6=1, 5=1, 4=1}
HashMap after iterator: {3=1, 2=1, 1=1, 3new=new3, 6=1, 5=1, 4=1}
```
最后，如果我们不添加新的元素而是修改已经存在的键值对会不会抛出异常呢？

修改原来的程序并且自己验证一下：
```
//myMap.put(key+"new", "new3");
myMap.put(key, "new3");
```
如果你对于输出结果感觉困惑或者震惊，在下面评论。我会很乐意给出进一步解释。

你有没有注意到那些我们在创建集合和迭代器时的尖括号，在Java中这叫做泛型，当涉及到编译时的类型检查和去除运行时的ClassCastException的时候会很有帮助。点击[这里](http://www.journaldev.com/1663/java-generics-tutorial-example-class-interface-methods-wildcards-and-much-more)可以了解更多泛型教程。

原文链接： [journaldev](http://www.journaldev.com/122/hashmap-vs-concurrenthashmap-%E2%80%93-example-and-exploring-iterator#comment-27448) 