---
title: Java并发之synchronized关键字深度解析
id: 1552
date: 2024-10-31 22:02:01
author: daichangya
excerpt: "前言  本文继续【Java并发之synchronized关键字深度解析（一）】一文而来，着重介绍synchronized几种锁的特性。一、对象头结构及锁状态标识  synchronized关键字是如何实现的给对象加锁？首先我们要了解一下java中对象的组成。java中的对象由3部分组成，第一部分是对"
permalink: /archives/java%E5%B9%B6%E5%8F%91%E4%B9%8Bsynchronized%E5%85%B3%E9%94%AE%E5%AD%97%E6%B7%B1%E5%BA%A6%E8%A7%A3%E6%9E%90/
categories:
 - jvm
tags: 
 - 面试
---



**前言**

    本文继续【Java并发之synchronized关键字深度解析（一）】一文而来，着重介绍synchronized几种锁的特性。

**一、对象头结构及锁状态标识**

    synchronized关键字是如何实现的给对象加锁？首先我们要了解一下java中对象的组成。java中的对象由3部分组成，第一部分是对象头，第二部分是实例数据，第三部分是对齐填充。

    **对齐填充**：jvm规定对象的起始内存地址必须是8字节的整数倍，如果不够的话就用占位符来填充，此部分占位符就是对齐填充；

    **实例数据**：实例数据是对象存储的真正有效的信息-对象的成员变量信息（包括继承自父类的）；

    **对象头**：对象头由两部分组成，第一部分是对象的运行时数据（Mark Word），包括哈希吗、锁偏向标识、锁类型、GC分代年龄、偏向线程id等；第二部分是对象的类型指针(Kclass Word)，用于去堆中定位对象的实例数据和方法区中的类型数据。java对象的公共特性都在对象头中存放。

对象头存储内容如下所示（以64位操作系统为例）：

```
|--------------------------------------------------------------------------------------------------------------|
|                                              Object Header (128 bits)                                        |
|--------------------------------------------------------------------------------------------------------------|
|                        Mark Word (64 bits)                                    |      Klass Word (64 bits)    |       
|--------------------------------------------------------------------------------------------------------------|
|  unused:25 | identity_hashcode:31 | unused:1 | age:4 | biased_lock:1 | lock:2 |     OOP to metadata object   |  无锁
|----------------------------------------------------------------------|--------|------------------------------|
|  thread:54 |         epoch:2      | unused:1 | age:4 | biased_lock:1 | lock:2 |     OOP to metadata object   |  偏向锁
|----------------------------------------------------------------------|--------|------------------------------|
|                     ptr_to_lock_record:62                            | lock:2 |     OOP to metadata object   |  轻量锁
|----------------------------------------------------------------------|--------|------------------------------|
|                     ptr_to_heavyweight_monitor:62                    | lock:2 |     OOP to metadata object   |  重量锁
|----------------------------------------------------------------------|--------|------------------------------|
|                                                                      | lock:2 |     OOP to metadata object   |    GC
|--------------------------------------------------------------------------------------------------------------|
```

其中lock:2表示有2bit控制锁类型，biased_lock:1表示1bit控制偏向锁状态，对应关系如下所示：

01：无锁（前面偏向锁状态为0时表示未锁定）

01：可偏向（前面偏向锁状态为1时表示可偏向）

00：轻量级锁

10：重量级锁

11：GC标记

    看到前两种状态时可能道友们会有些迷糊，先别着急，此处只要记住JVM的设计者们想用01状态来表示两种情况（无锁和可偏向），但是地球人都知道一个字符是无法做到标识两种状态的，所以他们就把前面一位暂时用不到的bit纳入进来，用前一位的值是0还是1来区分是无锁还是可偏向。

**二、锁的信息打印**

    下面我们先用代码验证一下这几种锁的存在（JVM默认开启偏向锁，默认的偏向锁启动时间为4-5秒后，所以先让主线程睡5秒再加锁能保证对象处于偏向锁的状态，此处也可以在VM Options中添加参数 【-XX:BiasedLockingStartupDelay=0】来让JVM取消延迟启动偏向锁（本文的示例均未设置此参数），其效果跟不改变VM Options只在main方法中让主线程先睡眠5秒是一样的）

![](https://img2018.cnblogs.com/i-beta/1558028/201912/1558028-20191201110649008-723216801.png)

 此外，要打印对象存储空间需要引入openjdk的jar包依赖

```
        <dependency>
            <groupId>org.openjdk.jol</groupId>
            <artifactId>jol-core</artifactId>
            <version>RELEASE</version>
        </dependency>
```

User对象代码：

```
public class LockClient {
    static class User {
        public String name;
        public byte age;
    }
}

```

万事具备，下面开始测试:

**1、无锁状态**

先不睡眠五秒，此时偏向锁未开启，所以对象都是无锁状态（未加synchronized的情况下），打印无锁状态的对象（锁标识001）

```
   @Test
    public void noLock() {
        User user = new User();
        System.out.println(ClassLayout.parseInstance(user).toPrintable());
    }

```

输出结果：

```
com.daicy.jvm.LockClient$User object internals:
 OFFSET  SIZE               TYPE DESCRIPTION                               VALUE
      0     4                    (object header)                           01 00 00 00 (00000001 00000000 00000000 00000000) (1)
      4     4                    (object header)                           00 00 00 00 (00000000 00000000 00000000 00000000) (0)
      8     4                    (object header)                           24 f3 00 f8 (00100100 11110011 00000000 11111000) (-134155484)
     12     1               byte User.age                                  0
     13     3                    (alignment/padding gap)                  
     16     4   java.lang.String User.name                                 null
     20     4                    (loss due to the next object alignment)
Instance size: 24 bytes
Space losses: 3 bytes internal + 4 bytes external = 7 bytes total
```

下面我们来解读一下这个打印结果。

通过TYPE DESCRIPTION可以知道，前三行打印的是对象头（object header），那么后面四行就是对象的实例数据和对其填充了。

先看第一行，VALUE中，标红的001表示当前对象是无锁状态，前面的0对应我们上面讲的可偏向锁状态为非偏向锁（如果是1表示偏向锁）。第三行存放的是对象指针。

第四行和第六行存放的是对象的两个成员变量，第五行空间用于填充age变量；第七行就是我们所说的对齐填充，使对象内存空间凑齐8字节的整数倍。

**2、偏向锁状态**

加上睡眠5秒

```
 @Test
    public void biasedLocking() {
        // 先睡眠5秒，保证开启偏向锁
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) { // -XX:-UseBiasedLocking
            e.printStackTrace(); // -XX:BiasedLockingStartupDelay=0
        }
        User user = new User();
        System.out.println(ClassLayout.parseInstance(user).toPrintable());
    }

```

看看打印结果：

```
com.daicy.jvm.LockClient$User object internals:
 OFFSET  SIZE               TYPE DESCRIPTION                               VALUE
      0     4                    (object header)                           05 00 00 00 (00000101 00000000 00000000 00000000) (5)
      4     4                    (object header)                           00 00 00 00 (00000000 00000000 00000000 00000000) (0)
      8     4                    (object header)                           24 f3 00 f8 (00100100 11110011 00000000 11111000) (-134155484)
     12     1               byte User.age                                  0
     13     3                    (alignment/padding gap)                  
     16     4   java.lang.String User.name                                 null
     20     4                    (loss due to the next object alignment)
Instance size: 24 bytes
Space losses: 3 bytes internal + 4 bytes external = 7 bytes total
```

可以看到，锁状态为101可偏向锁状态了，只是由于未用synchronized加锁，所以线程id是空的。其余数据跟上述无锁状态一样。

偏向锁带线程id情况，代码如下：

```
    @Test
    public void synchronizedLocking() {
        // 先睡眠5秒，保证开启偏向锁
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) { // -XX:-UseBiasedLocking
            e.printStackTrace(); // -XX:BiasedLockingStartupDelay=0
        }
        System.out.println(Thread.currentThread().getId());
//        System.out.println(Integer.toBinaryString(System.identityHashCode(Thread.currentThread())));
        User user = new User();
        synchronized (user) {
            System.out.println(ClassLayout.parseInstance(user).toPrintable());
        }
    }
```

输出结果：

```
com.daicy.jvm.LockClient$User object internals:
 OFFSET  SIZE               TYPE DESCRIPTION                               VALUE
      0     4                    (object header)                           05 d8 00 fc (00000101 11011000 00000000 11111100) (-67053563)
      4     4                    (object header)                           0e 7f 00 00 (00001110 01111111 00000000 00000000) (32526)
      8     4                    (object header)                           24 f3 00 f8 (00100100 11110011 00000000 11111000) (-134155484)
     12     1               byte User.age                                  0
     13     3                    (alignment/padding gap)                  
     16     4   java.lang.String User.name                                 null
     20     4                    (loss due to the next object alignment)
Instance size: 24 bytes
Space losses: 3 bytes internal + 4 bytes external = 7 bytes total
```

可见第一行中后面不再是0了，有了线程id的值。

**3、轻量级锁状态**

再看看轻量锁，不睡眠5秒，直接用synchronized给对象加锁，此时触发的就是轻量锁。代码如下：

```
   @Test
    public void lightWeightLock() {
        System.out.println(Integer.toBinaryString(System.identityHashCode(Thread.currentThread())));
        User user = new User();
        synchronized (user) {
            System.out.println(ClassLayout.parseInstance(user).toPrintable());
        }
    }
```

打印结果：

```
com.daicy.jvm.LockClient$User object internals:
 OFFSET  SIZE               TYPE DESCRIPTION                               VALUE
      0     4                    (object header)                           e0 59 8b 34 (11100000 01011001 10001011 00110100) (881547744)
      4     4                    (object header)                           77 7f 00 00 (01110111 01111111 00000000 00000000) (32631)
      8     4                    (object header)                           24 f3 00 f8 (00100100 11110011 00000000 11111000) (-134155484)
     12     1               byte User.age                                  0
     13     3                    (alignment/padding gap)                  
     16     4   java.lang.String User.name                                 null
     20     4                    (loss due to the next object alignment)
Instance size: 24 bytes
Space losses: 3 bytes internal + 4 bytes external = 7 bytes total
```

可以看到锁的标识位为000，轻量级锁

**4、重量级锁状态**

最后看一下重量级锁，只有在锁竞争的时候才会变为重量级锁，代码如下：

```
  @Test
    public void heavyWeightLock() {
        User user = new User();
        System.out.println(ClassLayout.parseInstance(user).toPrintable());
        Thread t1 = new Thread(() -> {
            synchronized (user) {
                try {
                    Thread.sleep(5000);// 睡眠，创造竞争条件
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });
        t1.start();
        Thread t2  = new Thread(() -> {
            synchronized (user) {
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });
        t2.start();
        System.out.println(ClassLayout.parseInstance(user).toPrintable());
    }
```

输出结果为：

```
com.daicy.jvm.LockClient$User object internals:
 OFFSET  SIZE               TYPE DESCRIPTION                               VALUE
      0     4                    (object header)                           01 00 00 00 (00000001 00000000 00000000 00000000) (1)
      4     4                    (object header)                           00 00 00 00 (00000000 00000000 00000000 00000000) (0)
      8     4                    (object header)                           24 f3 00 f8 (00100100 11110011 00000000 11111000) (-134155484)
     12     1               byte User.age                                  0
     13     3                    (alignment/padding gap)                  
     16     4   java.lang.String User.name                                 null
     20     4                    (loss due to the next object alignment)
Instance size: 24 bytes
Space losses: 3 bytes internal + 4 bytes external = 7 bytes total

com.daicy.jvm.LockClient$User object internals:
 OFFSET  SIZE               TYPE DESCRIPTION                               VALUE
      0     4                    (object header)                           6a 62 00 50 (01101010 01100010 00000000 01010000) (1342202474)
      4     4                    (object header)                           74 7f 00 00 (01110100 01111111 00000000 00000000) (32628)
      8     4                    (object header)                           24 f3 00 f8 (00100100 11110011 00000000 11111000) (-134155484)
     12     1               byte User.age                                  0
     13     3                    (alignment/padding gap)                  
     16     4   java.lang.String User.name                                 null
     20     4                    (loss due to the next object alignment)
Instance size: 24 bytes
Space losses: 3 bytes internal + 4 bytes external = 7 bytes total
```

可以看到锁状态为010，重量级锁。

**5、调用hashCode会取消偏向**

此外，如果通过Object对象的本地hashCode方法来获取对象的hashCode值，会使对象取消偏向锁状态

```
   @Test
    public void cancelBiasedLocking() {
        // 先睡眠5秒，保证开启偏向锁
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) { // -XX:-UseBiasedLocking
            e.printStackTrace(); // -XX:BiasedLockingStartupDelay=0
        }
        User user = new User();
        System.out.println(ClassLayout.parseInstance(user).toPrintable());
        System.out.println(user.hashCode());
        System.out.println(ClassLayout.parseInstance(user).toPrintable());
        synchronized (user) {
            System.out.println(ClassLayout.parseInstance(user).toPrintable());
        }
    }
```

打印结果：

```
com.daicy.jvm.LockClient$User object internals:
 OFFSET  SIZE               TYPE DESCRIPTION                               VALUE
      0     4                    (object header)                           05 00 00 00 (00000101 00000000 00000000 00000000) (5)
      4     4                    (object header)                           00 00 00 00 (00000000 00000000 00000000 00000000) (0)
      8     4                    (object header)                           24 f3 00 f8 (00100100 11110011 00000000 11111000) (-134155484)
     12     1               byte User.age                                  0
     13     3                    (alignment/padding gap)                  
     16     4   java.lang.String User.name                                 null
     20     4                    (loss due to the next object alignment)
Instance size: 24 bytes
Space losses: 3 bytes internal + 4 bytes external = 7 bytes total

1644443712
com.daicy.jvm.LockClient$User object internals:
 OFFSET  SIZE               TYPE DESCRIPTION                               VALUE
      0     4                    (object header)                           01 40 38 04 (00000001 01000000 00111000 00000100) (70795265)
      4     4                    (object header)                           62 00 00 00 (01100010 00000000 00000000 00000000) (98)
      8     4                    (object header)                           24 f3 00 f8 (00100100 11110011 00000000 11111000) (-134155484)
     12     1               byte User.age                                  0
     13     3                    (alignment/padding gap)                  
     16     4   java.lang.String User.name                                 null
     20     4                    (loss due to the next object alignment)
Instance size: 24 bytes
Space losses: 3 bytes internal + 4 bytes external = 7 bytes total

com.daicy.jvm.LockClient$User object internals:
 OFFSET  SIZE               TYPE DESCRIPTION                               VALUE
      0     4                    (object header)                           e0 29 99 e8 (11100000 00101001 10011001 11101000) (-392615456)
      4     4                    (object header)                           a8 7f 00 00 (10101000 01111111 00000000 00000000) (32680)
      8     4                    (object header)                           24 f3 00 f8 (00100100 11110011 00000000 11111000) (-134155484)
     12     1               byte User.age                                  0
     13     3                    (alignment/padding gap)                  
     16     4   java.lang.String User.name                                 null
     20     4                    (loss due to the next object alignment)
Instance size: 24 bytes
Space losses: 3 bytes internal + 4 bytes external = 7 bytes total

```

可以看到，计算完对象的hashCode之后，该对象立即从偏向锁状态变为了无锁状态，即使后续给对象加锁，该对象也只会进入轻量级或者重量级锁状态，不会再进入偏向状态了。因为该对象一旦进行Object的hashCode计算，那么对象头中会保存这个hashCode，此时再也无法存放偏向线程的id了（因为对象头的长度无法同时存放hashCode和偏向线程id），所以此后该对象无法再进入偏向锁状态。

**三、锁膨胀过程**

到这里，我们一起看完了synchronized给对象加的各种锁状态以及触发场景，下面我们梳理一下它们之间的关系。

 JVM启动后会默认开启偏向锁（默认4-5秒后开启），开启后，所有新建对象的对象头中都标识为101可偏向状态，且偏向线程id为0，表示处于初始化的偏向锁状态。此后一旦有线程对该对象使用了synchronized加锁，那么就会进入偏向锁状态，偏向线程id记录当前线程id；如果走完同步块之后，有另一个线程对该对象加锁，那么膨胀为轻量级锁，如果未走完同步块就有另一个线程试图给该对象加锁，那么会直接膨胀为（**中间会有一个自旋锁的过程，此处略去**）重量级锁。

**1、开启偏向锁**

![](https://img2018.cnblogs.com/i-beta/1558028/201912/1558028-20191201150648122-953765124.png)

                                                                                                             开启偏向的锁膨胀草图

下面演示一下对象从偏向锁膨胀为轻量级锁的过程：

```
 @Test
    public void biasedLockToLightWeightLock() throws InterruptedException {
        // 先睡眠5秒，保证开启偏向锁
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) { // -XX:-UseBiasedLocking
            e.printStackTrace(); // -XX:BiasedLockingStartupDelay=0
        }
        User user = new User();
        Thread t1 = new Thread(() -> {
            synchronized (user) {
                System.out.println(ClassLayout.parseInstance(user).toPrintable());
            }
        });
        t1.start();
        t1.join(); // 确保t1执行完了再执行当前主线程
        synchronized (user) {
            System.out.println(ClassLayout.parseInstance(user).toPrintable());
        }
        System.out.println(ClassLayout.parseInstance(user).toPrintable());
    }
```

打印结果如下，可以看到user对象先是偏向锁，然后变为轻量级锁，最后走完同步块释放锁变为无锁状态。

```
com.daicy.jvm.LockClient$User object internals:
 OFFSET  SIZE               TYPE DESCRIPTION                               VALUE
      0     4                    (object header)                           05 38 3a 1c (00000101 00111000 00111010 00011100) (473577477)
      4     4                    (object header)                           7d 7f 00 00 (01111101 01111111 00000000 00000000) (32637)
      8     4                    (object header)                           24 f3 00 f8 (00100100 11110011 00000000 11111000) (-134155484)
     12     1               byte User.age                                  0
     13     3                    (alignment/padding gap)                  
     16     4   java.lang.String User.name                                 null
     20     4                    (loss due to the next object alignment)
Instance size: 24 bytes
Space losses: 3 bytes internal + 4 bytes external = 7 bytes total

com.daicy.jvm.LockClient$User object internals:
 OFFSET  SIZE               TYPE DESCRIPTION                               VALUE
      0     4                    (object header)                           d8 a9 de 25 (11011000 10101001 11011110 00100101) (635349464)
      4     4                    (object header)                           7d 7f 00 00 (01111101 01111111 00000000 00000000) (32637)
      8     4                    (object header)                           24 f3 00 f8 (00100100 11110011 00000000 11111000) (-134155484)
     12     1               byte User.age                                  0
     13     3                    (alignment/padding gap)                  
     16     4   java.lang.String User.name                                 null
     20     4                    (loss due to the next object alignment)
Instance size: 24 bytes
Space losses: 3 bytes internal + 4 bytes external = 7 bytes total

com.daicy.jvm.LockClient$User object internals:
 OFFSET  SIZE               TYPE DESCRIPTION                               VALUE
      0     4                    (object header)                           01 00 00 00 (00000001 00000000 00000000 00000000) (1)
      4     4                    (object header)                           00 00 00 00 (00000000 00000000 00000000 00000000) (0)
      8     4                    (object header)                           24 f3 00 f8 (00100100 11110011 00000000 11111000) (-134155484)
     12     1               byte User.age                                  0
     13     3                    (alignment/padding gap)                  
     16     4   java.lang.String User.name                                 null
     20     4                    (loss due to the next object alignment)
Instance size: 24 bytes
Space losses: 3 bytes internal + 4 bytes external = 7 bytes total
```

 **2、关闭偏向锁**

如果通过参数设置JVM不开启偏向锁，那么新创建的对象是001无锁状态，遇到synchronized同步块会变为轻量级锁，遇到锁竞争变为重量级锁。
```
 @Test
    public void lightWeightToheavyWeightLock() {
        //-XX:-UseBiasedLocking 关闭偏向锁
        User user = new User();
        System.out.println(ClassLayout.parseInstance(user).toPrintable());
        Thread t1 = new Thread(() -> {
            synchronized (user) {
                try {
                    Thread.sleep(5000);// 睡眠，创造竞争条件
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });
        t1.start();
        System.out.println(ClassLayout.parseInstance(user).toPrintable());
        Thread t2  = new Thread(() -> {
            synchronized (user) {
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });
        t2.start();
        System.out.println(ClassLayout.parseInstance(user).toPrintable());
    }
```

```
com.daicy.jvm.LockClient$User object internals:
 OFFSET  SIZE               TYPE DESCRIPTION                               VALUE
      0     4                    (object header)                           01 00 00 00 (00000001 00000000 00000000 00000000) (1)
      4     4                    (object header)                           00 00 00 00 (00000000 00000000 00000000 00000000) (0)
      8     4                    (object header)                           24 f3 00 f8 (00100100 11110011 00000000 11111000) (-134155484)
     12     1               byte User.age                                  0
     13     3                    (alignment/padding gap)                  
     16     4   java.lang.String User.name                                 null
     20     4                    (loss due to the next object alignment)
Instance size: 24 bytes
Space losses: 3 bytes internal + 4 bytes external = 7 bytes total

com.daicy.jvm.LockClient$User object internals:
 OFFSET  SIZE               TYPE DESCRIPTION                               VALUE
      0     4                    (object header)                           20 e9 ff 17 (00100000 11101001 11111111 00010111) (402647328)
      4     4                    (object header)                           8e 7f 00 00 (10001110 01111111 00000000 00000000) (32654)
      8     4                    (object header)                           24 f3 00 f8 (00100100 11110011 00000000 11111000) (-134155484)
     12     1               byte User.age                                  0
     13     3                    (alignment/padding gap)                  
     16     4   java.lang.String User.name                                 null
     20     4                    (loss due to the next object alignment)
Instance size: 24 bytes
Space losses: 3 bytes internal + 4 bytes external = 7 bytes total

com.daicy.jvm.LockClient$User object internals:
 OFFSET  SIZE               TYPE DESCRIPTION                               VALUE
      0     4                    (object header)                           1a 63 00 40 (00011010 01100011 00000000 01000000) (1073767194)
      4     4                    (object header)                           8e 7f 00 00 (10001110 01111111 00000000 00000000) (32654)
      8     4                    (object header)                           24 f3 00 f8 (00100100 11110011 00000000 11111000) (-134155484)
     12     1               byte User.age                                  0
     13     3                    (alignment/padding gap)                  
     16     4   java.lang.String User.name                                 null
     20     4                    (loss due to the next object alignment)
Instance size: 24 bytes
Space losses: 3 bytes internal + 4 bytes external = 7 bytes total
```
![](https://img2018.cnblogs.com/i-beta/1558028/201912/1558028-20191201150731291-1189892613.png)

                                                                                      关闭偏向的锁膨胀草图

**四、重量级锁原理**

    Java中synchronized的重量级锁，是基于进入和退出Monitor对象实现的。在编译时会将同步块的开始位置插入monitorenter指令，在结束位置插入monitorexit指令。当线程执行到monitorenter指令时，会尝试获取对象所对应的Monitor所有权，如果获取到了，即获取到了锁，会在Monitor的owner中存放当前线程的id，这样它将处于锁定状态，除非退出同步块，否则其他线程无法获取到这个Monitor。

测试代码:
https://github.com/daichangya/Dtutorials/tree/main/jvm/src/main/java/com/daicy/jvm