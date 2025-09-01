---
title: Java设计模式——适配器模式的精妙应用：探秘 JDK 源码中的 Set 类
id: 20fcd8f5-e2d9-4275-bb36-49aba2ea2fc5
date: 2024-11-29 12:24:38
author: daichangya
cover: https://images.jsdiff.com/design06.jpg
excerpt: "在 Java 编程的世界里，JDK 源码犹如一座神秘的宝藏，其中的 Set 类更是我们日常开发中频繁使用的利器。今天，就让我们像勇敢的探险家一样，深入 JDK 源码，揭开 Set 类的神秘面纱，重点剖析适配器模式在其中的巧妙应用，看看它是如何让 Set 类焕发出独特魅力的！💥 一、Set 类：常用"
permalink: /archives/javashe-ji-mo-shi----gua-pei-qi-mo-shi-de-jing-miao/
categories:
 - 设计模式
---

在 Java 编程的世界里，JDK 源码犹如一座神秘的宝藏，其中的 Set 类更是我们日常开发中频繁使用的利器。今天，就让我们像勇敢的探险家一样，深入 JDK 源码，揭开 Set 类的神秘面纱，重点剖析适配器模式在其中的巧妙应用，看看它是如何让 Set 类焕发出独特魅力的！💥

## 一、Set 类：常用数据结构的重要角色🎯

在我们的编程之旅中，Set 类就像一个收纳有序的工具箱，它具有不允许存储重复元素的特性，这使得它在处理数据去重、集合运算等场景中发挥着至关重要的作用。无论是处理用户输入数据、管理系统配置项，还是在复杂算法中进行数据筛选，Set 类都能助我们一臂之力。但你是否曾好奇，Set 类是如何在底层实现元素唯一性判断的呢🧐？

## 二、适配器模式：Set 类背后的隐藏力量🌟

### （一）类图中的秘密
当我们审视 JDK 源码中与 Set 类相关的类图时，会惊喜地发现一个经典设计模式的身影——适配器模式。就像一位神奇的魔法师，它将 Map 接口的对象巧妙地包装成了 Set 接口，实现了两种不同接口之间的无缝转换。

### （二）HashSet：适配器模式的实例展示
1. **底层结构：依赖 HashMap**
<separator></separator>
在 HashSet 的源码中，我们发现它内部持有一个 transient 的 HashMap 实例：
```java
private transient HashMap<E,Object> map;
// 用于与 HashMap 中元素关联的虚拟值
private static final Object PRESENT = new Object();
```
这个 HashMap 就是实现 Set 功能的关键“幕后英雄”。HashSet 巧妙地利用了 HashMap 的特性来实现自己的功能。
2. **添加元素：委托给 HashMap**
当我们调用 HashSet 的 add 方法时，实际上是将元素作为 HashMap 的键，而那个固定的 PRESENT 对象作为值，存入了 HashMap 中：
```java
public boolean add(E e) {
    return map.put(e, PRESENT)==null;
}
```
这样一来，通过 HashMap 键的唯一性，就轻松保证了 Set 中元素的唯一性。当我们向 HashSet 中添加元素时，就如同将物品放入一个经过特殊改造的 HashMap 容器中，它会自动帮我们去重。
3. **迭代器：获取 Map 的键迭代器**
而当我们获取 HashSet 的迭代器时，它直接返回的是 HashMap 的键集合的迭代器：
```java
public Iterator<E> iterator() {
    return map.keySet().iterator();
}
```
这使得我们在遍历 HashSet 时，实际上是在遍历 HashMap 的键，从而获取到 Set 中的所有元素。

### （三）LinkedHashSet：类似的适配逻辑
LinkedHashSet 的实现也别具匠心。它在构造函数中调用了父类的构造函数，最终创建了一个 LinkedHashMap：
```java
public LinkedHashSet(int initialCapacity, float loadFactor) {
    super(initialCapacity, loadFactor, true);
}
// 其他构造函数类似，最终都会调用到父类构造函数创建 LinkedHashMap
```
其构造函数最终会调用到类似这样的父类构造函数：
```java
HashSet(int initialCapacity, float loadFactor, boolean dummy) {
    map = new LinkedHashMap<>(initialCapacity, loadFactor);
}
```
LinkedHashSet 利用 LinkedHashMap 的有序特性，不仅实现了元素的唯一性，还能保持元素插入的顺序，为我们提供了一种有序的 Set 实现。

### （四）TreeSet：适配 NavigableMap
TreeSet 的实现同样依赖于适配器模式，它内部持有一个 transient 的 NavigableMap 实例：
```java
private transient NavigableMap<E,Object> m;
private static final Object PRESENT = new Object();
```
TreeSet 通过将元素存储在 NavigableMap 中，并利用其排序功能，实现了对元素的有序存储和操作，为我们提供了一个有序且不重复的 Set 集合。

## 三、不仅仅是适配器模式：桥接模式的影子🤔

有趣的是，在分析 JDK 源码中 Set 类的实现时，我们还能发现一些类似桥接模式的变形痕迹。虽然从本质上来说，这里的实现更符合适配器模式的定义，但这种相似性也让我们对设计模式的运用有了更深入的思考。它就像一座横跨在不同设计理念之间的桥梁，让我们看到了在实际编程中，设计模式之间可能存在的微妙联系和灵活转换。

## 四、总结与启示：源码学习的价值💡

通过深入剖析 JDK 源码中 Set 类对适配器模式的应用，我们不仅揭开了 Set 类高效实现元素唯一性判断和操作的神秘面纱，更深刻体会到了设计模式在优化代码结构、提高代码复用性和灵活性方面的巨大威力。这就像在黑暗中点亮了一盏明灯，为我们今后的编程实践指明了方向。

在日常编程中，我们不应仅仅满足于使用现成的类和接口，更应该像这样深入源码，学习大师们的设计思路和技巧。只有这样，我们才能不断提升自己的编程水平，打造出更加高效、健壮、优雅的软件系统。希望今天的探索能成为你编程之路上的宝贵财富，让我们一起在源码的海洋中继续畅游，发现更多的智慧结晶！🚀