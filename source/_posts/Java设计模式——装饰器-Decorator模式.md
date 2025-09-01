---
title: Java设计模式——装饰器(Decorator)模式
id: 1087
date: 2024-10-31 22:01:49
author: daichangya
cover: https://images.jsdiff.com/design02.jpg
excerpt: "一、装饰器模式概述 Decorator设计模式属于典型的结构型模式（在GOF的模式分类中，模式分为创建型模式、结构型模式、行为模式三种）。其核心目的在于动态地为对象添加额外功能，这也是理解装饰器模式的关键所在。正如GOF在《Element of reusable Object - Oriented "
permalink: /archives/javashe-ji-mo-shi----zhuang-shi-qi-decorator-mo-shi/
categories:
 - 设计模式
tags: 
 - 设计模式
---

## 一、装饰器模式概述
Decorator设计模式属于典型的结构型模式（在GOF的模式分类中，模式分为创建型模式、结构型模式、行为模式三种）。其核心目的在于动态地为对象添加额外功能，这也是理解装饰器模式的关键所在。正如GOF在《Element of reusable Object - Oriented Software》中所概述的：“Decorator Pattern――Attaches additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality.”

### （一）何时需要使用装饰器模式
在GOF的相关书籍中，以文本组件与边框的例子阐述装饰器模式，但这里将以一个更具说服力的“三明治”例子来说明。假设要为三明治小店构建程序，设计各种三明治对象。若采用传统继承方式，从简单的Sandwich对象开始，如要创建带蔬菜的三明治就继承原有Sandwich并添加蔬菜成员变量，后续若要添加咸肉、奶油等多种成分，且考虑各种成分的任意组合，那么继承方式将导致类的数量急剧膨胀。例如，若有n种成分，根据组合数学知识，不同组合方案数为\(C_{n}^0 + C_{n}^1 + \cdots + C_{n}^{n - 1} + C_{n}^n = 2^n\)种。这意味着每增加一种成分，工作量可能成倍增加，同时类库也会变得极为庞大。而装饰器模式则能有效解决此类问题。

### （二）装饰器模式的设计与实现
1. **类的设计**
   - **Ingredient（成分）**：所有类的父类，一般为抽象类且方法有默认实现，也可为接口，包含所有成分共有的方法，如描述自身的`getDescription`方法和获取价格的`getCost`方法，以及打印自身描述和价格的`printDescription`方法（构成模板方法）。以下是其Java代码实现：
```java
// Ingredient.java
public abstract class Ingredient {
    public abstract String getDescription();
    public abstract double getCost();

    public void printDescription() {
        System.out.println(" Name      " + this.getDescription());
        System.out.println(" Price RMB " + this.getCost());
    }
}
```
   - **Bread（面包）**：三明治中必需的两片面包，是系统中最基本元素，也是被装饰的元素，类似IO中的媒质流（原始流）。它是具体成分，需实现父类抽象方法，描述可通过构造器传入，价格简单返回固定值。示例代码如下：
```java
// Bread.java
public class Bread extends Ingredient {
    private String description;

    public Bread(String desc) {
        this.description = desc;
    }

    public String getDescription() {
        return description;
    }

    public double getCost() {
        return 2.48;
    }
}
```
   - **Decorator（装饰器）**：所有其他成分（如猪肉、羊肉、青菜、芹菜等具有装饰功能成分）的父类，是一个实际不存在仅表示概念的类。其特征为必须有一个父类（Ingredient）作为成员变量且必须继承公共父类（Ingredient）。代码如下：
```java
// Decorator.java
public abstract class Decorator extends Ingredient {
    Ingredient ingredient;

    public Decorator(Ingredient igd) {
        this.ingredient = igd;
    }

    public abstract String getDescription();
    public abstract double getCost();
}
```
   - **Pork（猪肉）、Mutton（羊肉）、Celery（芹菜）、GreenGrocery（青菜）**：这些都是具体的成分，同时也是具体的装饰器，继承自Decorator类。通过构造器传入Ingredient实例，在实现`getDescription`和`getCost`方法时，不仅包含自身的描述和价格，还会加上被装饰成分的描述和价格，从而增强了被装饰成分的功能。以Pork类为例：
```java
// Pork.java
public class Pork extends Decorator {
    public Pork(Ingredient igd) {
        super(igd);
    }

    public String getDescription() {
        String base = ingredient.getDescription();
        return base + "\n" + "Decorated with Pork!";
    }

    public double getCost() {
        double basePrice = ingredient.getCost();
        double porkPrice = 1.8;
        return basePrice + porkPrice;
    }
}
```
其他羊肉、芹菜、青菜装饰器类的实现类似，只是在描述和价格的具体数值上有所不同。
2. **测试类展示装饰器模式的威力**
   - 以下是测试类`DecoratorTest`，通过创建不同组合的三明治来展示装饰器模式的动态组合功能：
```java
public class DecoratorTest {
    public static void main(String[] args) {
        // 夹羊肉的三明治
        Ingredient compound = new Mutton(new Celery(new Bread("Master24's Bread")));
        compound.printDescription();

        // 全蔬菜的三明治
        compound = new Celery(new GreenGrocery(new Bread("Bread with milk")));
        compound.printDescription();

        // 全荤的三明治
        compound = new Mutton(new Pork(new Bread("Bread with cheese")));
        compound.printDescription();
    }
}
```

### （三）装饰器模式的结构剖析
1. **通用结构**
   - 在软件设计中，常使用UML图来表示结构。装饰器模式的通用结构图包含以下几个关键部分：
     - **Component**：位于装饰器模式结构图的顶层，是定义装饰器模式中公共方法的类。
     - **ConcreateComponent**：是具体被装饰的类，类似于IO包中的媒体流，在“三明治”例子中就是Bread类。
     - **Decorator**：装饰器模式的核心对象，是所有具体装饰器对象的父类，完成装饰器的部分职能，如上述例子中的Decorator类。它继承自Component，同时包含一个Component作为其成员变量，通过这种方式实现动态地增加功能。
     - **ConcreteDecoratorA和ConcreteDecoratorB**：是两个具体的装饰器对象，完成具体的装饰功能。装饰功能的实现是通过调用被装饰对象对应的方法，再加上装饰对象自身的方法，这是实现添加额外功能的关键。在实际情况中，存在“透明装饰器”和“不透明装饰器”之分。“透明装饰器”要求整个Decorator结构中的所有类保持相同的“接口”（即共同方法），但现实中大多数装饰器是“不透明装饰器”，其“接口”在某些子类中会得到增强，具体取决于该类与顶层抽象类或接口是否有相同的公共方法。例如IO中的ByteArrayInputStream比InputStream抽象类多一些方法，所以IO中的装饰器是“不透明装饰器”。
2. **IO包中的装饰器模式实例**
   - 以IO中输入字节流部分的装饰器为例，其结构如下：
     - **InputStream**：是装饰器的顶层类，为抽象类，包含一些共有的方法，如读方法（read，有3个不同参数的重载形式）、关闭流的方法（close）、mark相关的方法（mark、reset和markSupport）、跳跃方法（skip）、查询是否还有元素方法（available）。
     - **FileInputStream、PipedInputStream等**：是具体的被装饰对象，它们的“接口”中一般有额外的方法。
     - **FilterInputStream**：是装饰器中的核心，即Decorator对象。
     - **DataInputStream、BufferedInputStream等**：是具体的装饰器，它们保持了和InputStream同样的接口。
     - **ObjectInputStream**：是IO字节输入流中特殊的装饰器，它不是FilterInputStream的子类，但和其他FilterInputStream的子类功能相似，都可以装饰其他对象。IO包中的输出字节流、输入字符流和输出字符流也都采用了装饰器模式。

### （四）总结与启示
装饰器模式为我们提供了一种灵活且高效的方式来扩展对象功能，避免了因大量使用继承而导致的类爆炸问题。通过动态组合装饰器对象，可以根据需求在运行时为对象添加各种功能，提高了代码的可维护性和扩展性。在实际软件开发中，当遇到需要为对象添加多种可选功能且不希望通过复杂的继承层次来实现时，装饰器模式是一个值得考虑的优秀设计模式。它能够让我们的代码结构更加清晰，同时也便于应对不断变化的功能需求。