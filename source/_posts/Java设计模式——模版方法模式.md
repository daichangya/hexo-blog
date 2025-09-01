---
title: Java设计模式——模版方法模式
id: 3d56360c-13f2-46f7-ab32-6f8da7fff4b1
date: 2024-11-25 10:33:28
author: daichangya
cover: https://images.jsdiff.com/design02.jpg
excerpt: "一、模版方法模式概述 模版方法模式是极为常见的设计模式之一。在实际工作中，你可能已经在不经意间使用了该模式。此模式需要抽象类与具体子类协同工作，抽象类用于勾勒算法的轮廓和骨架，具体子类则负责填充算法中的各个逻辑步骤，不同子类的填充方式各异。汇总这些基本方法的方法被称为模版方法，它在抽象类中以具体方法"
permalink: /archives/javashe-ji-mo-shi----mo-ban-fang-fa-mo-shi/
categories:
 - 设计模式
---

# 一、模版方法模式概述
模版方法模式是极为常见的设计模式之一。在实际工作中，你可能已经在不经意间使用了该模式。此模式需要抽象类与具体子类协同工作，抽象类用于勾勒算法的轮廓和骨架，具体子类则负责填充算法中的各个逻辑步骤，不同子类的填充方式各异。汇总这些基本方法的方法被称为模版方法，它在抽象类中以具体方法的形式定义。

### （一）模板方法模式所涉及的角色
1. **抽象模版角色**
   - 定义一个或多个抽象操作，这些抽象操作是顶级逻辑的组成步骤，被称为基本操作。同时，定义并实现一个模版方法，此模版方法给出顶级逻辑的骨架，而逻辑的具体实现则推迟到子类中完成。
2. **具体模版角色**
   - 实现父类中定义的一个或多个抽象方法，这些方法是顶级逻辑的组成部分。不同的具体模版可以为这些抽象方法提供不同的实现，从而使顶级逻辑的实现各不相同。

### （二）举例说明
以一个有趣但不太恰当的例子来说明，比如《如何说服女生上床》（这里仅为举例，不代表任何不当价值观）这部经典文章（假设存在）中描述的从认识女生到上床有一些不变步骤：巧遇、展开追求、牵手、接吻等（一共八大步骤，这里简化为四个主要步骤进行代码示例）。这八大步骤就像是定义好的模版方法，而每个人针对每个步骤根据自身情况会有不同的方法，这就是具体实现。

以下是相关代码实现：
```java
/**
* 抽象模版角色，定义了一个骨架,模版方法，
* 将要想追到女生，必须遵循的4个步骤抽象成一个顶级逻辑
* @author Administrator
*/
public abstract class 如何说服女生上床 {
    public void 模版方法() {
        巧遇();
        追求();
        牵手();
        接吻();
    }

    public abstract void 巧遇();
    public abstract void 追求();
    public abstract void 牵手();
    public abstract void 接吻();
}

/**
* 读过这本书的读者一展开了自己的行动
* @author Administrator
*/
public class 读者一 extends 如何说服女生上床 {
    @Override
    public void 巧遇() {
        System.out.println("读者一自己的巧遇方法。。。");
    }

    @Override
    public void 追求() {
        System.out.println("读者一自己的追求方法。。。");
    }

    @Override
    public void 牵手() {
        System.out.println("读者一自己的牵手方法。。。");
    }

    @Override
    public void 接吻() {
        System.out.println("读者一自己的接吻方法。。。");
    }
}

/**
* 读过这本书的读者二展开了自己的行动
* @author Administrator
*/
public class 读者二 extends 如何说服女生上床 {
    @Override
    public void 巧遇() {
        System.out.println("读者二自己的巧遇方法。。。");
    }

    @Override
    public void 追求() {
        System.out.println("读者二自己的追求方法。。。");
    }

    @Override
    public void 牵手() {
        System.out.println("读者二自己的牵手方法。。。");
    }

    @Override
    public void 接吻() {
        System.out.println("读者二自己的接吻方法。。。");
    }
}
```
客户端调用代码如下：
```java
public static void main(String[] args) {
    如何说服女生上床第一个读该书的人 = new 读者一();
    第一个读该书的人.模版方法();
    如何说服女生上床第二个读该书的人 = new 读者二();
    第二个读该书的人.模版方法();
}
```

## 二、总结
模版方法模式的核心是准备一个抽象类，在其中将部分逻辑以具体方法实现，同时声明一些抽象方法迫使子类实现剩余逻辑。不同子类可以通过不同方式实现这些抽象方法，从而实现剩余逻辑的多样化。通过这种方式，代码结构更加清晰，具有更好的扩展性和可维护性，能够适应不同场景下的需求变化。继续努力，加油！

