---
title: Java 设计模式 — 抽象工厂模式
id: 588
date: 2024-10-31 22:01:44
author: daichangya
cover: https://images.jsdiff.com/design02.jpg
excerpt: 简单工厂模式是类的创建模式，又叫静态工厂方法（static factory method）,负责将大量有共同接口的类实例化，可以动态的决定将哪个类实例化，不必事先知道要实例化哪个类。顾名思义，就像是工厂的功能，客户需要什么样的产品，工厂就能生产。但是产品之间应该有某种关联性，即有共同的接口，不能让一个工厂去生产火腿肠。工厂模式中创建是不同类的对象。工厂的老板可以根据客户不同的需要进
permalink: /archives/Java-she-ji-mo-shi-chou-xiang-gong/
categories:
- 设计模式
tags:
- 设计模式
---

# Java设计模式—抽象工厂模式

## 一、抽象工厂模式概述
### （一）定义
抽象工厂模式属于创建型设计模式，它提供了一种创建一系列相关或相互依赖对象的接口，并且无需指定这些对象的具体类。这种模式在创建对象时，将对象的创建和使用分离开来，使得系统在创建对象时具有更高的灵活性和可维护性。

### （二）适用场景
1. 当系统需要创建一系列相关或相互依赖的对象时，例如在一个游戏开发中，需要创建游戏角色、武器、道具等一系列相关对象，并且这些对象的创建过程较为复杂，相互之间存在一定的关联关系，抽象工厂模式可以很好地组织和管理这些对象的创建过程。
2. 当系统希望与具体的产品实现解耦，即不希望系统代码依赖于产品的具体类，而是依赖于抽象产品接口时，抽象工厂模式可以通过抽象工厂和抽象产品接口来实现这种解耦，使得系统更容易进行扩展和维护。

### （三）角色构成
1. **抽象工厂角色（AbstractFactory）**
   - 这是抽象工厂模式的核心角色，它声明了一系列创建产品对象的抽象方法。这些方法通常返回抽象产品类型，例如在一个图形绘制系统中，抽象工厂可能定义创建抽象图形（如抽象圆形、抽象矩形等）的方法。
   - 抽象工厂角色不负责创建具体的产品对象，而是将这个任务交给具体的工厂子类来完成。它为整个系统提供了一个统一的创建对象的接口，使得系统的其他部分可以通过这个接口来获取所需的产品对象，而无需关心对象的具体创建过程。
2. **具体工厂角色（ConcreteFactory）**
   - 具体工厂角色实现了抽象工厂角色声明的抽象方法，负责创建具体的产品对象。例如，在一个游戏开发中，可能有中世纪风格工厂（MedievalFactory）和科幻风格工厂（SciFiFactory）等具体工厂类。
   - 中世纪风格工厂可能会创建中世纪风格的角色（如骑士角色）、武器（如长剑）和道具（如魔法药水）等具体产品对象；科幻风格工厂则会创建科幻风格的角色（如机器人角色）、武器（如激光枪）和道具（如能量护盾）等具体产品对象。每个具体工厂类都对应着一个特定的产品族，它所创建的产品对象之间具有一定的关联性和一致性。
3. **抽象产品角色（AbstractProduct）**
   - 抽象产品角色定义了产品对象的公共接口，这些接口声明了产品对象所具有的基本操作和属性。在一个图形绘制系统中，抽象图形类可能定义了图形的绘制方法（draw）、获取图形面积方法（getArea）等抽象接口。
   - 具体的产品类（如圆形类、矩形类等）实现了这些抽象接口，从而提供了具体的产品功能。抽象产品角色使得系统可以以统一的方式处理不同类型的产品对象，提高了系统的灵活性和可扩展性。
4. **具体产品角色（ConcreteProduct）**
   - 具体产品角色是抽象产品角色的具体实现类，它实现了抽象产品角色定义的接口，提供了具体的产品功能。例如，在游戏开发中，骑士角色类（Knight）实现了抽象角色类（AbstractCharacter）的接口，提供了骑士角色的具体属性（如生命值、攻击力等）和行为（如攻击、防御等）；长剑武器类（LongSword）实现了抽象武器类（AbstractWeapon）的接口，提供了长剑的具体攻击方式和伤害值等。

## 二、抽象工厂模式示例代码
### （一）抽象工厂类
```java
// 抽象工厂类
public abstract class AbstractFactory {
    // 创建角色的抽象方法
    public abstract Character createCharacter();
    // 创建武器的抽象方法
    public abstract Weapon createWeapon();
    // 创建道具的抽象方法
    public abstract Item createItem();
}
```
### （二）具体工厂类
1. **中世纪风格工厂类**
```java
// 中世纪风格工厂类
public class MedievalFactory extends AbstractFactory {
    @Override
    public Character createCharacter() {
        return new Knight();
    }

    @Override
    public Weapon createWeapon() {
        return new LongSword();
    }

    @Override
    public Item createItem() {
        return new MagicPotion();
    }
}
```
2. **科幻风格工厂类**
```java
// 科幻风格工厂类
public class SciFiFactory extends AbstractFactory {
    @Override
    public Character createCharacter() {
        return new Robot();
    }

    @Override
    public Weapon createWeapon() {
        return new LaserGun();
    }

    @Override
    public Item createItem() {
        return new EnergyShield();
    }
}
```
### （三）抽象产品类
1. **抽象角色类**
```java
// 抽象角色类
public abstract class Character {
    public abstract void attack();
    public abstract void defend();
}
```
2. **抽象武器类**
```java
// 抽象武器类
public abstract class Weapon {
    public abstract void use();
}
```
3. **抽象道具类**
```java
// 抽象道具类
public abstract class Item {
    public abstract void use();
}
```
### （四）具体产品类
1. **骑士角色类**
```java
// 骑士角色类
public class Knight extends Character {
    @Override
    public void attack() {
        System.out.println("骑士挥舞长剑攻击！");
    }

    @Override
    public void defend() {
        System.out.println("骑士举起盾牌防御！");
    }
}
```
2. **长剑武器类**
```java
// 长剑武器类
public class LongSword extends Weapon {
    @Override
    public void use() {
        System.out.println("使用长剑进行攻击，造成高额伤害！");
    }
}
```
3. **魔法药水道具类**
```java
// 魔法药水道具类
public class MagicPotion extends Item {
    @Override
    public void use() {
        System.out.println("使用魔法药水，恢复生命值！");
    }
}
```
4. **机器人角色类**
```java
// 机器人角色类
public class Robot extends Character {
    @Override
    public void attack() {
        System.out.println("机器人发射激光攻击！");
    }

    @Override
    public void defend() {
        System.out.println("机器人启动能量护盾防御！");
    }
}
```
5. **激光枪武器类**
```java
// 激光枪武器类
public class LaserGun extends Weapon {
    @Override
    public void use() {
        System.out.println("使用激光枪射击，具有强大的攻击力！");
    }
}
```
6. **能量护盾道具类**
```java
// 能量护盾道具类
public class EnergyShield extends Item {
    @Override
    public void use() {
        System.out.println("启动能量护盾，抵挡攻击！");
    }
}
```
### （五）测试类
```java
// 测试类
public class Test {
    public static void main(String[] args) {
        // 创建中世纪风格工厂
        AbstractFactory medievalFactory = new MedievalFactory();
        // 创建中世纪风格角色
        Character knight = medievalFactory.createCharacter();
        // 创建中世纪风格武器
        Weapon longSword = medievalFactory.createWeapon();
        // 创建中世纪风格道具
        Item magicPotion = medievalFactory.createItem();

        knight.attack();
        longSword.use();
        magicPotion.use();

        // 创建科幻风格工厂
        AbstractFactory sciFiFactory = new SciFiFactory();
        // 创建科幻风格角色
        Character robot = sciFiFactory.createCharacter();
        // 创建科幻风格武器
        Weapon laserGun = sciFiFactory.createWeapon();
        // 创建科幻风格道具
        Item energyShield = sciFiFactory.createItem();

        robot.attack();
        laserGun.use();
        energyShield.use();
    }
}
```

## 三、总结
抽象工厂模式通过抽象工厂、具体工厂、抽象产品和具体产品等角色的协作，实现了创建一系列相关或相互依赖对象的功能。它使得系统在创建对象时更加灵活、可维护，并且能够有效地解耦对象的创建和使用过程。在实际应用中，当面临需要创建多个相关对象且希望保持系统的扩展性和灵活性时，抽象工厂模式是一个非常有效的解决方案。它可以帮助开发人员更好地组织代码结构，提高软件系统的质量和可维护性，同时也便于根据需求的变化快速添加新的产品族或修改现有产品族的实现。