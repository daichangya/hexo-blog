---
title: java object多大 java对象内存模型 数组有多长
id: 1551
date: 2024-10-31 22:02:01
author: daichangya
excerpt: "对象结构在HotSpot虚拟机中，对象在内存中存储的布局可以分为3块区域：对象头（Header）、实例数据（InstanceData）和对齐填充（Padding）。下图是普通对象实例与数组对象实例的数据结构：1对象头HotSpot虚拟机的对象头包括两部分信息：markword 第一部分markwor"
permalink: /archives/javaobject%E5%A4%9A%E5%A4%A7java%E5%AF%B9%E8%B1%A1%E5%86%85%E5%AD%98%E6%A8%A1%E5%9E%8B%E6%95%B0%E7%BB%84%E6%9C%89%E5%A4%9A%E9%95%BF/
categories:
 - jvm
---



# 对象结构

在HotSpot虚拟机中，对象在内存中存储的布局可以分为3块区域：**对象头（Header）、实例数据（Instance Data）和对齐填充（Padding）**。下图是普通对象实例与数组对象实例的数据结构：


![20170419212953720.png](https://images.jsdiff.com/20170419212953720_1609210802980.png)

### 1 对象头

HotSpot虚拟机的对象头包括两部分信息：

1.  markword   
    第一部分markword,用于存储对象自身的运行时数据，如**哈希码（HashCode）、GC分代年龄、锁状态标志、线程持有的锁、偏向线程ID、偏向时间戳等，这部分数据的长度****在32位和64位的虚拟机（未开启压缩指针）中分别为32bit和64bit，官方称它为“MarkWord”。**
2.  klass   
    对象头的另外一部分是klass类型指针，即对象指向它的类元数据的指针，虚拟机通过这个指针来确定这个对象是哪个类的实例. **32位4字节，64位开启指针压缩或最大堆内存<32g时 4字节，否则8字节**
3.  **数组长度（只有数组对象有） 4字节**  
    如果对象是一个数组, 那在对象头中还必须有一块数据用于记录数组长度.**int最大值2g，2^31，java数组（包含字符串）最长2g**

### 2 实例数据

实例数据部分是对象真正存储的有效信息，也是在程序代码中所定义的各种类型的字段内容。无论是从父类继承下来的，还是在子类中定义的，都需要记录起来。

| Primitive Type | Memory Required(bytes) |
| --- | --- |
| boolean | 1 |
| byte | 1 |
| short | 2 |
| char | 2 |
| int | 4 |
| float | 4 |
| long | 8 |
| double | 8 |

**此外，引用类型在32位系统上每个占用4B, 在64位系统上每个占用8B，开启（默认）指针压缩占用4B**

### 3 对齐填充

第三部分对齐填充并不是必然存在的，也没有特别的含义，它仅仅起着占位符的作用。**由于HotSpot VM的自动内存管理系统要求对象起始地址必须是8字节的整数倍**，换句话说，就是对象的大小必须是8字节的整数倍。而对象头部分正好是8字节的倍数（1倍或者2倍），因此，当对象实例数据部分没有对齐时，就需要通过对齐填充来补全。

### 对象大小计算

要点   
1\. **在32位系统下，存放Class指针的空间大小是4字节**，MarkWord是4字节，对象头为8字节。   
2\. **在64位系统下，存放Class指针的空间大小是8字节**，MarkWord是8字节，对象头为16字节。   
3\. 64位开启指针压缩**或者 JVM 堆的最大值小于 32G**的情况下，**存放Class指针的空间大小是4字节**，MarkWord是8字节，对象头为12字节。

4 如果是数组对象，对象头的大小为：数组对象头8字节+数组长度4字节+对齐4字节=16字节。其中对象引用占4字节（未开启指针压缩的64位为8字节），数组`MarkWord`为4字节（64位未开启指针压缩的为8字节）;

**markword始终为8字节，class pointer及object ref pointer压缩4字节，不压缩8字节，**数组对象的Shallow Size=数组对象头（12/16）+数组长度4字节+length * 引用指针大小（4/8）+填充****

5\. 静态属性不算在对象大小内。

**JDK 1.8，默认启用指针压缩参数就是开启的。**

## 补充：

### HotSpot对象模型

HotSpot中采用了OOP-Klass模型，它是描述Java对象实例的模型，它分为两部分：

*   类被加载到内存时，就被封装成了klass，klass包含类的元数据信息，像类的方法、常量池这些信息都是存在klass里的，你可以认为它是java里面的java.lang.Class对象，记录了类的全部信息；
*   OOP（Ordinary Object Pointer）指的是普通对象指针，它包含MarkWord 和元数据指针，MarkWord用来存储当前指针指向的对象运行时的一些状态数据；元数据指针则指向klass,用来告诉你当前指针指向的对象是什么类型，也就是使用哪个类来创建出来的；
*     
    那么为何要设计这样一个一分为二的对象模型呢？**这是因为HotSopt JVM的设计者不想让每个对象中都含有一个vtable（虚函数表），所以就把对象模型拆成klass和oop，其中oop中不含有任何虚函数，而klass就含有虚函数表，**可以进行method dispatch。

**实践结果：**

```
package com.daicy.jvm;

import org.openjdk.jol.info.ClassLayout;

/**
 * @author: create by daichangya
 * @version: v1.0
 * @description: com.daicy.jvm
 * @date:12/28/20
 */
public class MarkdownMain {
    // 关闭指针压缩-XX:-UseCompressedOops
    public static void main(String []f) {
        System.out.println(ClassLayout.parseInstance(new Integer(2)).toPrintable());
        System.out.println(ClassLayout.parseInstance(new Long(2)).toPrintable());
        System.out.println(ClassLayout.parseInstance(new MyIntArray()).toPrintable());
        System.out.println(ClassLayout.parseInstance(new MyLong()).toPrintable());
        System.out.println(ClassLayout.parseInstance(new MyLong[]{new MyLong(), new MyLong(), new MyLong()}).toPrintable());
    }

    private static class MyIntArray {
        public int[] intArray;
    }


    private static class MyLong {
        public volatile long usefulVal;
        public volatile Long anotherVal;
        public MyRef myRef;
    }

    private static class MyRef {
        Integer integer = new Integer(15);
    }
}

<dependency>
  <groupId>org.openjdk.jol</groupId>
  <artifactId>jol-core</artifactId>
  <version>0.9</version>
</dependency>
```

1）1.8默认：开启指针压缩

```
java.lang.Integer object internals:
 OFFSET  SIZE   TYPE DESCRIPTION                               VALUE
      0     4        (object header)                           01 00 00 00 (00000001 00000000 00000000 00000000) (1)
      4     4        (object header)                           00 00 00 00 (00000000 00000000 00000000 00000000) (0)
      8     4        (object header)                           ae 22 00 f8 (10101110 00100010 00000000 11111000) (-134208850)
     12     4    int Integer.value                             2
Instance size: 16 bytes
Space losses: 0 bytes internal + 0 bytes external = 0 bytes total

java.lang.Long object internals:
 OFFSET  SIZE   TYPE DESCRIPTION                               VALUE
      0     4        (object header)                           01 00 00 00 (00000001 00000000 00000000 00000000) (1)
      4     4        (object header)                           00 00 00 00 (00000000 00000000 00000000 00000000) (0)
      8     4        (object header)                           f5 22 00 f8 (11110101 00100010 00000000 11111000) (-134208779)
     12     4        (alignment/padding gap)                  
     16     8   long Long.value                                2
Instance size: 24 bytes
Space losses: 4 bytes internal + 0 bytes external = 4 bytes total

com.daicy.jvm.MarkdownMain$MyIntArray object internals:
 OFFSET  SIZE    TYPE DESCRIPTION                               VALUE
      0     4         (object header)                           01 00 00 00 (00000001 00000000 00000000 00000000) (1)
      4     4         (object header)                           00 00 00 00 (00000000 00000000 00000000 00000000) (0)
      8     4         (object header)                           5a f3 00 f8 (01011010 11110011 00000000 11111000) (-134155430)
     12     4   int[] MyIntArray.intArray                       null
Instance size: 16 bytes
Space losses: 0 bytes internal + 0 bytes external = 0 bytes total

com.daicy.jvm.MarkdownMain$MyLong object internals:
 OFFSET  SIZE                               TYPE DESCRIPTION                               VALUE
      0     4                                    (object header)                           01 00 00 00 (00000001 00000000 00000000 00000000) (1)
      4     4                                    (object header)                           00 00 00 00 (00000000 00000000 00000000 00000000) (0)
      8     4                                    (object header)                           d8 f3 00 f8 (11011000 11110011 00000000 11111000) (-134155304)
     12     4                     java.lang.Long MyLong.anotherVal                         null
     16     8                               long MyLong.usefulVal                          0
     24     4   com.daicy.jvm.MarkdownMain.MyRef MyLong.myRef                              null
     28     4                                    (loss due to the next object alignment)
Instance size: 32 bytes
Space losses: 0 bytes internal + 4 bytes external = 4 bytes total

[Lcom.daicy.jvm.MarkdownMain$MyLong; object internals:
 OFFSET  SIZE                                TYPE DESCRIPTION                               VALUE
      0     4                                     (object header)                           01 00 00 00 (00000001 00000000 00000000 00000000) (1)
      4     4                                     (object header)                           00 00 00 00 (00000000 00000000 00000000 00000000) (0)
      8     4                                     (object header)                           18 f4 00 f8 (00011000 11110100 00000000 11111000) (-134155240)
     12     4                                     (object header)                           03 00 00 00 (00000011 00000000 00000000 00000000) (3)
     16    12   com.daicy.jvm.MarkdownMain$MyLong MarkdownMain$MyLong;.<elements>           N/A
     28     4                                     (loss due to the next object alignment)
Instance size: 32 bytes
Space losses: 0 bytes internal + 4 bytes external = 4 bytes total


```

**整个对象要是8的倍数，否则补全**

**markdown8字节，class pointer 4字节**

**引用类型4字节**

**数组类型的val中，存在【数组长度】个引用类型+数组长度int4**

2）关闭指针压缩

-XX:-UseCompressedOops

```

# WARNING: Unable to attach Serviceability Agent. You can try again with escalated privileges. Two options: a) use -Djol.tryWithSudo=true to try with sudo; b) echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope
java.lang.Integer object internals:
 OFFSET  SIZE   TYPE DESCRIPTION                               VALUE
      0     4        (object header)                           01 00 00 00 (00000001 00000000 00000000 00000000) (1)
      4     4        (object header)                           00 00 00 00 (00000000 00000000 00000000 00000000) (0)
      8     4        (object header)                           e0 a9 7e 15 (11100000 10101001 01111110 00010101) (360622560)
     12     4        (object header)                           ea 7f 00 00 (11101010 01111111 00000000 00000000) (32746)
     16     4    int Integer.value                             2
     20     4        (loss due to the next object alignment)
Instance size: 24 bytes
Space losses: 0 bytes internal + 4 bytes external = 4 bytes total

java.lang.Long object internals:
 OFFSET  SIZE   TYPE DESCRIPTION                               VALUE
      0     4        (object header)                           01 00 00 00 (00000001 00000000 00000000 00000000) (1)
      4     4        (object header)                           00 00 00 00 (00000000 00000000 00000000 00000000) (0)
      8     4        (object header)                           18 e5 7e 15 (00011000 11100101 01111110 00010101) (360637720)
     12     4        (object header)                           ea 7f 00 00 (11101010 01111111 00000000 00000000) (32746)
     16     8   long Long.value                                2
Instance size: 24 bytes
Space losses: 0 bytes internal + 0 bytes external = 0 bytes total

com.daicy.jvm.MarkdownMain$MyIntArray object internals:
 OFFSET  SIZE    TYPE DESCRIPTION                               VALUE
      0     4         (object header)                           01 00 00 00 (00000001 00000000 00000000 00000000) (1)
      4     4         (object header)                           00 00 00 00 (00000000 00000000 00000000 00000000) (0)
      8     4         (object header)                           60 d1 84 0d (01100000 11010001 10000100 00001101) (226808160)
     12     4         (object header)                           ea 7f 00 00 (11101010 01111111 00000000 00000000) (32746)
     16     8   int[] MyIntArray.intArray                       null
Instance size: 24 bytes
Space losses: 0 bytes internal + 0 bytes external = 0 bytes total

com.daicy.jvm.MarkdownMain$MyLong object internals:
 OFFSET  SIZE                               TYPE DESCRIPTION                               VALUE
      0     4                                    (object header)                           01 00 00 00 (00000001 00000000 00000000 00000000) (1)
      4     4                                    (object header)                           00 00 00 00 (00000000 00000000 00000000 00000000) (0)
      8     4                                    (object header)                           90 db 84 0d (10010000 11011011 10000100 00001101) (226810768)
     12     4                                    (object header)                           ea 7f 00 00 (11101010 01111111 00000000 00000000) (32746)
     16     8                               long MyLong.usefulVal                          0
     24     8                     java.lang.Long MyLong.anotherVal                         null
     32     8   com.daicy.jvm.MarkdownMain.MyRef MyLong.myRef                              null
Instance size: 40 bytes
Space losses: 0 bytes internal + 0 bytes external = 0 bytes total

[Lcom.daicy.jvm.MarkdownMain$MyLong; object internals:
 OFFSET  SIZE                                TYPE DESCRIPTION                               VALUE
      0     4                                     (object header)                           01 00 00 00 (00000001 00000000 00000000 00000000) (1)
      4     4                                     (object header)                           00 00 00 00 (00000000 00000000 00000000 00000000) (0)
      8     4            Shallow Size=对象头大小16字节+int类型大小4字节+数组引用大小8字节+padding4字节=32字节；
Retained Size=Shallow Size+char数组的Retained Size。                         (object header)                           18 de 84 0d (00011000 11011110 10000100 00001101) (226811416)
     12     4                                     (object header)                           ea 7f 00 00 (11101010 01111111 00000000 00000000) (32746)
     16     4                                     (object header)                           03 00 00 00 (00000011 00000000 00000000 00000000) (3)
     20     4                                     (alignment/padding gap)                  
     24    24   com.daicy.jvm.MarkdownMain$MyLong MarkdownMain$MyLong;.<elements>           N/A
Instance size: 48 bytes
Space losses: 4 bytes internal + 0 bytes external = 4 bytes total

```

**markdown8字节，class pointer 8字节**

**引用类型8字节**

**https://www.jianshu.com/p/91e398d5d17c** 中介绍了另一种看对象模型的方式，还可以看Shallow Size和Retained Size

64位系统中，数组对象的对象头占用24 bytes，启用压缩后占用16字节。比普通对象占用内存多是因为需要额外的空间存储数组的长度。基础数据类型数组占用的空间包括数组对象头以及基础数据类型数据占用的内存空间。由于对象数组中存放的是对象的引用，所以数组对象的Shallow Size=数组对象头（含**数组长度4字节）**+length * 引用指针大小（4/8字节）+填充，Retained Size=Shallow Size+length*每个元素的Retained Size。

因此，在关闭指针压缩时，一个String对象的大小为：

- Shallow Size=对象头大小16字节+int类型大小4字节+数组引用大小8字节+padding4字节=32字节；
- Retained Size=Shallow Size+char数组的Retained Size。

在开启指针压缩时，一个String对象的大小为：

- Shallow Size=对象头大小12字节+int类型大小4字节+数组引用大小4字节+padding4字节=24字节；

- Retained Size=Shallow Size+char数组的Retained Size。


有关Shallow Size和Retained Size请参考

 [使用MAT时的Shallow Size和 Retained Size的区别](https://blog.jsdiff.com/archives/%E4%BD%BF%E7%94%A8mat%E6%97%B6%E7%9A%84shallowsize%E5%92%8Cretainedsize%E7%9A%84%E5%8C%BA%E5%88%AB)
