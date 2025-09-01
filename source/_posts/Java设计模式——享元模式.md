---
title: Java设计模式——享元模式
id: 4d62cb46-4849-448e-94d2-1dc387716b42
date: 2024-11-25 11:04:26
author: daichangya
cover: https://images.jsdiff.com/design02.jpg
excerpt: "一、引子 在Java中，String类型具有一些独特的特性。其一，String类型的对象一旦被创建就不可改变；其二，当两个String对象所包含的内容相同时，JVM只创建一个String对象对应这两个不同的对象引用。我们可以通过以下代码来验证这两个特性： public class TestPatte"
permalink: /archives/javashe-ji-mo-shi----xiang-yuan-mo-shi/
categories:
 - 设计模式
---

## 一、引子
在Java中，String类型具有一些独特的特性。其一，String类型的对象一旦被创建就不可改变；其二，当两个String对象所包含的内容相同时，JVM只创建一个String对象对应这两个不同的对象引用。我们可以通过以下代码来验证这两个特性：
```java
public class TestPattern {
    public static void main(String[] args) {
        String n = "I Love Java";
        String m = "I Love Java";
        System.out.println(n == m);
    }
}
```
上述代码会输出`true`，这表明在JVM中`n`和`m`两个引用指向了同一个String对象。若在系统输出之前添加一行代码`m = m + "hehe";`，此时`n == m`的结果将变为`false`。这是因为执行添加语句时，`m`指向了一个新创建的String对象，而非修改原来引用的对象。String类型的设计避免了创建大量相同内容的String对象时产生的不必要资源损耗，是享元模式应用的范例，下面让我们深入学习享元模式。

## 二、定义与分类
享元模式英文称为“Flyweight Pattern”。其定义为：采用共享来避免大量拥有相同内容对象的开销，这里最常见、直观的开销就是内存损耗。享元模式以共享的方式高效支持大量细粒度对象。在该模式中，核心概念是共享，为实现共享，区分了内蕴状态和外蕴状态。内蕴状态是共性，存储在享元内部，不会随环境改变而不同，可共享；外蕴状态是个性，随环境改变而改变，由客户端保持，在具体环境下，客户端将外蕴状态传递给享元以创建不同对象。

根据《Java与模式》，享元模式分为单纯享元模式和复合享元模式。

### （一）单纯享元模式
1. **结构**
   - **抽象享元角色**：在Java中可由抽象类、接口担当，为具体享元角色规定必须实现的方法，外蕴状态以参数形式通过此方法传入。
   - **具体享元角色**：实现抽象角色规定的方法，若存在内蕴状态，负责为其提供存储空间。
   - **享元工厂角色**：负责创建和管理享元角色，是实现共享的关键。其实现通常使用Singleton模式，确保工厂对象只产生一个实例。
   - **客户端角色**：维护对所有享元对象的引用，并存储对应的外蕴状态。
   - 单纯享元模式的类图如下：
   [此处可插入单纯享元模式类图，展示Client、Flyweight、FlyweightFactory、ConcreteFlyweight之间的关系]
   - 该模式结构类似简单工厂模式，但重点不同。简单工厂模式主要使系统不依赖于实现细节，而享元模式旨在采用共享技术避免大量相同内容对象的开销。
2. **举例（以咖啡店订单为例）**
   - 假设一家咖啡店有多种口味的咖啡（如拿铁、摩卡、卡布奇诺等），接到大量订单时，咖啡口味可设置为共享，不必为每一杯单独生成对象。
   - 以下是相关代码实现：
```java
import java.util.*;

// 抽象订单类
public abstract class Order {
    // 执行卖出动作
    public abstract void sell();
}

// 具体口味订单类
public class FlavorOrder extends Order {
    public String flavor;

    // 获取咖啡口味
    public FlavorOrder(String flavor) {
        this.flavor = flavor;
    }

    @Override
    public void sell() {
        System.out.println("卖出一份" + flavor + "的咖啡。");
    }
}

// 口味工厂类
public class FlavorFactory {
    private Map<String, Order> flavorPool = new HashMap<>();
    // 静态工厂，负责生成订单对象
    private static FlavorFactory flavorFactory = new FlavorFactory();

    private FlavorFactory() {
    }

    public static FlavorFactory getInstance() {
        return flavorFactory;
    }

    public Order getOrder(String flavor) {
        Order order = null;
        if (flavorPool.containsKey(flavor)) {
            order = flavorPool.get(flavor);
        } else {
            order = new FlavorOrder(flavor);
            flavorPool.put(flavor, order);
        }
        return order;
    }

    public int getTotalFlavorsMade() {
        return flavorPool.size();
    }
}

// 客户端类
public class Client {
    // 客户下的订单
    private static List<Order> orders = new ArrayList<>();
    // 订单对象生成工厂
    private static FlavorFactory flavorFactory;

    // 增加订单
    private static void takeOrders(String flavor) {
        orders.add(flavorFactory.getOrder(flavor));
    }

    public static void main(String[] args) {
        // 订单生成工厂
        flavorFactory = FlavorFactory.getInstance();
        // 增加订单
        takeOrders("摩卡");
        takeOrders("卡布奇诺");
        takeOrders("香草星冰乐");
        takeOrders("香草星冰乐");
        takeOrders("拿铁");
        takeOrders("卡布奇诺");
        takeOrders("拿铁");
        takeOrders("卡布奇诺");
        takeOrders("摩卡");
        takeOrders("香草星冰乐");
        takeOrders("卡布奇诺");
        takeOrders("摩卡");
        takeOrders("香草星冰乐");
        takeOrders("拿铁");
        takeOrders("拿铁");
        // 卖咖啡
        for (Order order : orders) {
            order.sell();
        }
        // 打印生成的订单java对象数量
        System.out.println("\n客户一共买了 " + orders.size() + " 杯咖啡! ");
        // 打印生成的订单java对象数量
        System.out.println("共生成了 " + flavorFactory.getTotalFlavorsMade() + " 个FlavorOrder java对象! ");
    }
}
```
输出结果显示，通过口味共享极大减少了对象数目，降低了内存消耗。例如，客户一共买了15杯咖啡，但只生成了4个`FlavorOrder` Java对象。

### （二）复合享元模式
1. **结构**
   - **抽象享元角色**：同单纯享元模式，为具体享元角色规定必须实现的方法，外蕴状态以参数形式传入。
   - **具体享元角色**：实现抽象角色规定的方法，负责内蕴状态的存储空间（若有）。
   - **复合享元角色**：所代表对象不可共享，但可分解为多个单纯享元对象的组合。
   - **享元工厂角色**：负责创建和管理享元角色，实现共享的关键。
   - **客户端角色**：维护对所有享元对象的引用，并存储对应的外蕴状态。
   - 复合享元模式的类图如下：
   [此处可插入复合享元模式类图，展示Client、Flyweight、FlyweightFactory、ConcreteFlyweight、ConcreteCompositeFlyweight之间的关系]
   - 该模式左半部类似简单工厂模式，右半部类似合成模式。合成模式用于将具体享元角色和复合享元角色同等对待和处理，确保复合享元中包含的单纯享元具有相同外蕴状态，而单纯享元内蕴状态往往不同。
2. **举例（在餐馆点菜场景下）**
   - 以去餐馆吃饭为例，内蕴状态代表菜肴种类，外蕴状态是点菜人。
   - 首先定义抽象享元角色：
```java
interface Menu {
    // 规定实现类必须实现设置内外关系的方法
    public void setPersonMenu(String person, List list);
    // 规定实现类必须实现查找外蕴状态对应的内蕴状态的方法
    public List findPersonMenu(String person, List list);
}
```
   - 具体享元角色实现：
```java
class PersonMenu implements Menu {
    private String dish;

    // 在构造方法中给内蕴状态赋值
    public PersonMenu(String dish) {
        this.dish = dish;
    }

    public synchronized void setPersonMenu(String person, List list) {
        list.add(person);
        list.add(dish);
    }

    public List findPersonMenu(String person, List list) {
        List dishList = new ArrayList<>();
        Iterator it = list.iterator();
        while (it.hasNext()) {
            if (person.equals((String) it.next())) {
                dishList.add(it.next());
            }
        }
        return dishList;
    }
}
```
   - 享元工厂角色：
```java
class FlyweightFactory {
    private Map menuList = new HashMap();
    private static FlyweightFactory factory = new FlyweightFactory();

    // 单例模式，确保工厂对象唯一
    private FlyweightFactory() {
    }

    public static FlyweightFactory getInstance() {
        return factory;
    }

    // 享元模式关键方法，根据内蕴状态创建或获取对象
    public synchronized Menu factory(String dish) {
        if (menuList.containsKey(dish)) {
            return (Menu) menuList.get(dish);
        } else {
            Menu menu = new PersonMenu(dish);
            menuList.put(dish, menu);
            return menu;
        }
    }

    // 验证生成对象数量
    public int getNumber() {
        return menuList.size();
    }
}
```
   - 复合享元角色：
```java
class PersonMenuMuch implements Menu {
    private Map MenuList = new HashMap<>();

    public PersonMenuMuch() {
    }

    // 增加一个新的单纯享元对象
    public void add(String key, Menu menu) {
        MenuList.put(key, menu);
    }

    // 两个无为的方法（因为复合享元不涉及内外状态对应）
    public synchronized void setPersonMenu(String person, List list) {
    }

    public List findPersonMenu(String person, List list) {
        List nothing = null;
        return nothing;
    }
}
```
   - 在工厂方法中添加重载方法以支持复合享元创建：
```java
public Menu factory(String[] dish) {
    PersonMenuMuch menu = new PersonMenuMuch();
    String key = null;
    for (int i = 0; i < dish.length; i++) {
        key = dish[i];
        menu.add(key, this.factory(key));
    }
    return menu;
}
```
   - 客户端使用示例：
```java
class Client {
    private static FlyweightFactory factory;

    public static void main(String[] args) {
        List list1 = new ArrayList<>();
        factory = FlyweightFactory.getInstance();
        Menu list = factory.factory("尖椒土豆丝");
        list.setPersonMenu("ai92", list1);
        list = factory.factory("红烧肉");
        list.setPersonMenu("ai92", list1);
        list = factory.factory("地三鲜");
        list.setPersonMenu("ai92", list1);
        list = factory.factory("地三鲜");
        list.setPersonMenu("ai92", list1);
        list = factory.factory("红焖鲤鱼");
        list.setPersonMenu("ai92", list1);
        list = factory.factory("红烧肉");
        list.setPersonMenu("ai921", list1);
        list = factory.factory("红焖鲤鱼");
        list.setPersonMenu("ai921", list1);
        list = factory.factory("地三鲜");
        list.setPersonMenu("ai921", list1);
        System.out.println(factory.getNumber());

        List list2 = list.findPersonMenu("ai921", list1);
        Iterator it = list2.iterator();
        while (it.hasNext()) {
            System.out.println(" " + it.next());
        }
    }
}
```

### （三）两种模式对比
1. **复杂度方面**：复合享元模式比单纯享元模式复杂。
2. **共享效果方面**：复合享元模式在共享上未达预期，虽内部单纯享元可共享，但复合享元角色使用两个`Map`保存内蕴状态和对象，未节省空间和对象个数，违背享元模式初衷，应尽量使用单纯享元模式。

## 三、使用优缺点
### （一）优点
享元模式能大幅降低内存中对象数量，提高程序运行速度，例如在处理大量重复字符串或文本系统中字母对象时可节省资源。

### （二）缺点
1. 为实现对象共享，需将一些状态外部化，使程序逻辑复杂化。
2. 读取外部状态会使运行时间稍变长。

### （三）使用条件
1. 系统中有大量对象，影响系统效率。
2. 对象状态可分离为内外两部分，且内外状态划分及对应关系维护很重要，划分不当可能无法减少对象数量，对应关系维护需花费一定空间和时间，享元模式是以时间换空间，可使用B树等优化对应关系查找。

## 四、总结
享元模式较为复杂，实际应用相对较少，但共享思想对系统优化有益，在企业级架构设计中应用广泛，如缓存体系。Java中的String和Integer类是其应用实例。