---
title: JDK源码分析之Set类详解——适配器模式的应用
id: 706
date: 2024-10-31 22:01:45
author: daichangya
excerpt: JDK源码中Set类是我们开发过程中经常用到的，那么本文将会向你介绍JDK源码中Set类的一些构造，使我们在编程中高效的应用。JDK源码分析Set类，因为Set类是经常要用到的，那我们知道JDK源码中Set类在其中不可以有相同的元素，那么判断这个元素是否相同是如何实现的呢，我们看下下面这张图：对JDK源码分析之Set类在这张类图上，
permalink: /archives/JDK-yuan-ma-fen-xi-zhi-Set-lei-xiang/
categories:
- java源码分析
tags:
- 设计模式
---

 

JDK源码中Set类是我们开发过程中经常用到的，那么本文将会向你介绍JDK源码中Set类的一些构造，使我们在编程中高效的应用。

JDK源码分析Set类，因为Set类是经常要用到的，那我们知道JDK源码中Set类在其中不可以有相同的元素，那么判断这个元素是否相同是如何实现的呢，我们看下下面这张图：

[](http://images.51cto.com/files/uploadimg/20090708/1352150.png)[![JDK源码分析之Set类图](http://images.51cto.com/files/uploadimg/20090708/140400334lit.png)](http://images.51cto.com/files/uploadimg/20090708/140400334.png)  

对JDK源码分析之Set类在这张类图上，首先我们看见一个经典模式的应用，那就是适配器模式，我们把map接口的对象，包装成为了Set的接口；在代码中，我们来分析一下；

首先，我们看一下HashSet

    private transient HashMap map;  

    // Dummy value to associate with an Object in the backing Map 
    private staticfinal Object PRESENT = new Object(); 

可见，他适配了HashMap，那么他的功能是如何委托给HashMap结构的呢？

    public boolean add(E e) {  
		return map.put(e, PRESENT)==null;  
    } 

在HashMap中，我们大多数时候是用value，但是在set的时候，却很好的利用了已有类HashMap，他利用了HashMap的key的唯一性来保证存储在Set中的元素的唯一性；

private static final Object PRESENT = new Object();

是这个HashMap所有key的value，他只是一个形式，而我们真正的数据是存在在key中的资源；

我们最后拿到的迭代器也是:

    public Iterator iterator() {  
		return map.keySet().iterator();  
    } 

Map的keySet的迭代器；

同理，我们看看LinkedhashMap;

    public LinkedHashSet(int initialCapacity, float loadFactor) {  
		super(initialCapacity, loadFactor, true);  
    }  

    /**  
    * Constructs a new, empty linked hash set with the specified initial  
    * capacity and the default load factor (0.75).  
    *  
    * @param   initialCapacity   the initial capacity of the LinkedHashSet  
    * @throws  IllegalArgumentException if the initial capacity is less  
    *              than zero  
    */
    public LinkedHashSet(int initialCapacity) {  
		super(initialCapacity, .75f, true);  
    }  

    /**  
    * Constructs a new, empty linked hash set with the default initial  
    * capacity (16) and load factor (0.75).  
        */
    public LinkedHashSet() {  
		super(16, .75f, true);  
    } 

调用了父类的构造函数；构造函数如下：

    HashSet(int initialCapacity, float loadFactor, boolean dummy) {  
     	map = new LinkedHashMap(initialCapacity, loadFactor);  
    } 

生出了LinkedHashMap；

同理，我们一样可见到TreeMap的实现：

    private transient NavigableMap m;  

    // Dummy value to associate with an Object in the backing Map 
    private static final Object PRESENT = new Object(); 

更多的，我们也可以理解他是一种桥接模式的一种变形，不过我想从意义上，我更愿意相信其是适配器的应用；

对JDK源码分析之Set类到这里，希望对你有帮助。