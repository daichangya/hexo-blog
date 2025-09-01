---
title: 使用MAT时的Shallow Size和 Retained Size的区别
id: 1550
date: 2024-10-31 22:02:01
author: daichangya
permalink: /archives/%E4%BD%BF%E7%94%A8mat%E6%97%B6%E7%9A%84shallowsize%E5%92%8Cretainedsize%E7%9A%84%E5%8C%BA%E5%88%AB/
categories:
 - jvm
---

所有包含Heap Profling功能的工具（MAT, Yourkit, JProfiler, TPTP等）都会使用到两个名词，一个是Shallow Size，另一个是 Retained Size.  
这是两个在平时不太常见的名词，本文会对这两个名词做一个详细的解释。

Shallow Size  
对象自身占用的内存大小，不包括它引用的对象。  
针对非数组类型的对象，它的大小就是对象与它所有的成员变量大小的总和。当然这里面还会包括一些java语言特性的数据存储单元。  
针对数组类型的对象，它的大小是数组元素对象的大小总和。

Retained Size  
Retained Size=当前对象大小+当前对象可直接或间接引用到的对象的大小总和。(间接引用的含义：A->B->C, C就是间接引用)  
换句话说，Retained Size就是当前对象被GC后，从Heap上总共能释放掉的内存。  
不过，释放的时候还要排除被GC Roots直接或间接引用的对象。他们暂时不会被被当做Garbage。

看图理解Retained Size  
![Shallow size and retained size](http://pic.yupoo.com/kenwug/AX15U96P/4DEzc.png)  
上图中，GC Roots直接引用了A和B两个对象。

A对象的Retained Size=A对象的Shallow Size  
B对象的Retained Size=B对象的Shallow Size + C对象的Shallow Size

这里不包括D对象，因为D对象被GC Roots直接引用。  
如果GC Roots不引用D对象呢？  
![Shallow Size and retained size](http://pic.yupoo.com/kenwug/AX15V1mt/rgUkr.png)

此时,  
B对象的Retained Size=B对象的Shallow Size + C对象的Shallow Size + D对象的Shallow Size

转载自：[http://kenwublog.com/understand-shallow-and-retained-size-in-hprofling](http://kenwublog.com/understand-shallow-and-retained-size-in-hprofling)