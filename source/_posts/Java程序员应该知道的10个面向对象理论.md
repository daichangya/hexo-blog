---
title: Java程序员应该知道的10个面向对象理论
id: 1099
date: 2024-10-31 22:01:49
author: daichangya
excerpt: "面向对象理论是面向对象编程的核心，但是我发现大部分Java程序员热衷于像单例模式、装饰者模式或观察者模式这样的设计模式，而并没有十分注意学习面向对象的分析和设计。学习面向编程的基础(如抽象，封装，多态，继承等)是非常重要的，而运用它们来设计干净的模块也同样重要。我也认识很"
permalink: /archives/18567911/
categories:
 - java
---

 

### 一、题前话

本人一直崇尚一个原则，“我思，故我在！”。一直以来忙于编码，但是不甚如人意（写了较多重复性、耦合性太强的代码）。行有行规，面向对象编程的Java语言也不例外，遵循其相关原则，才能高效快速的编写高性能的代码。那么期间过程学习很重要，从一开始的基础知识学习，到大量的编写代码，回过头来再将学习的理论和实践相结合，每一个环节都很重要，这样才能成为高手，特别是最后一环（将理论与实践相结合——重构之前不符合理论原则的代码，反过来加深理论的理解）。

### 二、正题

一般对Java面向对象编程的高度概括是——三大基本特性（封装、继承、多态）和五大基本原则（SOLID）

#### 1）三大特性是：封装,继承,多态  

所谓封装，也就是把客观事物封装成抽象的类，并且类可以把自己的数据和方法只让可信的类或者对象操作，对不可信的进行信息隐藏。封装是面向对象的特征之一，是对象和类概念的主要特性。 简单的说，一个类就是一个封装了数据以及操作这些数据的代码的逻辑实体。在一个对象内部，某些代码或某些数据可以是私有的，不能被外界访问。通过这种方式，对象对内部数据提供了不同级别的保护，以防止程序中无关的部分意外的改变或错误的使用了对象的私有部分。

  
所谓继承是指可以让某个类型的对象获得另一个类型的对象的属性的方法。它支持按级分类的概念。继承是指这样一种能力：它可以使用现有类的所有功能，并在无需重新编写原来的类的情况下对这些功能进行扩展。 通过继承创建的新类称为“子类”或“派生类”，被继承的类称为“基类”、“父类”或“超类”。继承的过程，就是从一般到特殊的过程。要实现继承，可以通过“继承”（Inheritance）和“组合”（Composition）来实现。继承概念的实现方式有二类：实现继承与接口继承。实现继承是指直接使用基类的属性和方法而无需额外编码的能力；接口继承是指仅使用属性和方法的名称、但是子类必须提供实现的能力；

所谓多态就是指一个类实例的相同方法在不同情形有不同表现形式。多态机制使具有不同内部结构的对象可以共享相同的外部接口。这意味着，虽然针对不同对象的具体操作不同，但通过一个公共的类，它们（那些操作）可以通过相同的方式予以调用。

  

#### 2）五大基本原则 

单一职责原则SRP(Single Responsibility Principle)  
是指一个类的功能要单一，不能包罗万象。如同一个人一样，分配的工作不能太多，否则一天到晚虽然忙忙碌碌的，但效率却高不起来。  
  
开放封闭原则OCP(Open－Close Principle)   
一个模块在扩展性方面应该是开放的而在更改性方面应该是封闭的。比如：一个网络模块，原来只服务端功能，而现在要加入客户端功能，  
那么应当在不用修改服务端功能代码的前提下，就能够增加客户端功能的实现代码，这要求在设计之初，就应当将服务端和客户端分开，公共部分抽象出来。  
  
替换原则(the Liskov Substitution Principle LSP)   
子类应当可以替换父类并出现在父类能够出现的任何地方。比如：公司搞年度晚会，所有员工可以参加抽奖，那么不管是老员工还是新员工，  
也不管是总部员工还是外派员工，都应当可以参加抽奖，否则这公司就不和谐了。  
  
依赖原则(the Dependency Inversion Principle DIP) 具体依赖抽象，上层依赖下层抽象接口。假设B是较A低的模块，但B需要使用到A的功能，  
这个时候，B不应当直接使用A中的具体类： 而应当由B定义一抽象接口，并由A来实现这个抽象接口，B只使用这个抽象接口：这样就达到  
了依赖倒置的目的，B也解除了对A的依赖，反过来是A依赖于B定义的抽象接口。通过上层模块难以避免依赖下层模块，假如B也直接依赖A的实现，那么就可能造成循环依赖。

接口分离原则(the Interface Segregation Principle ISP)   
模块间要通过抽象接口隔离开，而不是通过具体的类强耦合起来

  

### 三、正正题

下面的总结10个面向对象基本原则总结的也不错，记录如下

面向对象设计原则是OOPS（Object-Oriented Programming System，面向对象的程序设计系统）编程的核心，但大多数Java程序员追逐像[Singleton](http://en.wikipedia.org/wiki/Singleton_pattern)、[Decorator](http://en.wikipedia.org/wiki/Decorator_pattern)、[Observer](http://en.wikipedia.org/wiki/Observer_pattern)这样的设计模式，而不重视面向对象的分析和设计。甚至还有经验丰富的Java程序员没有听说过OOPS和[SOLID](http://en.wikipedia.org/wiki/SOLID)设计原则，他们根本不知道设计原则的好处，也不知道如何依照这些原则来进行编程。  
  
众所周知，Java编程最基本的原则就是要追求高内聚和低耦合的解决方案和代码模块设计。查看Apache和Sun的开放源代码能帮助你发现其他Java设计原则在这些代码中的实际运用。Java Development Kit则遵循以下模式：BorderFactory类中的[工厂模式](http://en.wikipedia.org/wiki/Factory_Pattern)、Runtime类中的[单件模式](http://en.wikipedia.org/wiki/Singleton_pattern)。你可以通过Joshua Bloch的[《Effective Java》](http://www.amazon.com/gp/product/0321356683/ref=as_li_ss_tl?ie=UTF8&tag=javamysqlanta-20&linkCode=as2&camp=1789&creative=390957&creativeASIN=0321356683)一书来了解更多信息。我个人偏向的另一种面向对象的设计模式是Kathy Sierra的[Head First Design Pattern](http://www.amazon.com/gp/product/0596007124/ref=as_li_ss_tl?ie=UTF8&tag=javamysqlanta-20&linkCode=as2&camp=1789&creative=390957&creativeASIN=0596007124)以及[Head First Object Oriented Analysis and Design](http://www.amazon.com/gp/product/0596008678/ref=as_li_ss_tl?ie=UTF8&tag=javamysqlanta-20&linkCode=as2&camp=1789&creative=390957&creativeASIN=0596008678)。  
  
虽然实际案例是学习设计原则或模式的最佳途径，但通过本文的介绍，没有接触过这些原则或还在学习阶段的Java程序员也能够了解这10个面向对象的设计原则。其实每条原则都需要大量的篇幅才能讲清楚，但我会尽力做到言简意赅。  
  

#### **原则1：DRY（Don't repeat yourself）**

  
即不要写重复的代码，而是用“abstraction”类来抽象公有的东西。如果你需要多次用到一个硬编码值，那么可以设为公共常量；如果你要在两个以上的地方使用一个代码块，那么可以将它设为一个独立的方法。SOLID设计原则的优点是易于维护，但要注意，不要滥用，duplicate 不是针对代码，而是针对功能。这意味着，即使用公共代码来验证OrderID和SSN，二者也不会是相同的。使用公共代码来实现两个不同的功能，其实就是近似地把这两个功能永远捆绑到了一起，如果OrderID改变了其格式，SSN验证代码也会中断。因此要慎用这种组合，不要随意捆绑类似但不相关的功能。  

####   
**原则2：封装变化**

  
在软件领域中唯一不变的就是“Change”，因此封装你认为或猜测未来将发生变化的代码。OOPS设计模式的优点在于易于测试和维护封装的代码。如果你使用Java编码，可以默认私有化变量和方法，并逐步增加访问权限，比如从private到protected和not public。有几种Java设计模式也使用封装，比如Factory设计模式是封装“对象创建”，其灵活性使得之后引进新代码不会对现有的代码造成影响。  
  

#### **原则3：开闭原则**

  
即对扩展开放，对修改关闭。这是另一种非常棒的设计原则，可以防止其他人更改已经测试好的代码。理论上，可以在不修改原有的模块的基础上，扩展功能。这也是[开闭原则](http://en.wikipedia.org/wiki/Open/closed_principle)的宗旨。  
  

#### **原则4：单一职责原则**

  
类被修改的几率很大，因此应该专注于单一的功能。如果你把多个功能放在同一个类中，功能之间就形成了关联，改变其中一个功能，有可能中止另一个功能，这时就需要新一轮的测试来避免可能出现的问题。  
  

#### **原则5：依赖注入或倒置原则**

  
这个设计原则的亮点在于任何被DI框架注入的类很容易用mock对象进行测试和维护，因为对象创建代码集中在框架中，客户端代码也不混乱。有很多方式可以实现依赖倒置，比如像AspectJ等的AOP（Aspect Oriented programming）框架使用的字节码技术，或Spring框架使用的代理等。  

####   
**原则6：优先利用组合而非继承**

  
如果可能的话，优先利用组合而不是继承。一些人可能会质疑，但我发现，组合比继承灵活得多。组合允许在运行期间通过设置类的属性来改变类的行为，也可以通过使用接口来组合一个类，它提供了更高的灵活性，并可以随时实现。[《Effective Java》](http://www.amazon.com/gp/product/0321356683/ref=as_li_ss_tl?ie=UTF8&tag=javamysqlanta-20&linkCode=as2&camp=1789&creative=390957&creativeASIN=0321356683)也推荐此原则。  
  

#### **原则7：里氏代换原则（LSP）**

  
根据该原则，子类必须能够替换掉它们的基类，也就是说使用基类的方法或函数能够顺利地引用子类对象。LSP原则与单一职责原则和接口分离原则密切相关，如果一个类比子类具备更多功能，很有可能某些功能会失效，这就违反了LSP原则。为了遵循该设计原则，派生类或子类必须增强功能。  
  

#### **原则8：接口分离原则**

  
采用多个与特定客户类有关的接口比采用一个通用的涵盖多个业务方法的接口要好。设计接口很棘手，因为一旦释放接口，你就无法在不中断执行的情况下改变它。在Java中，该原则的另一个优势在于，在任何类使用接口之前，接口不利于实现所有的方法，所以单一的功能意味着更少的实现方法。  
  

#### **原则9：针对接口编程，而不是针对实现编程**

  
该原则可以使代码更加灵活，以便可以在任何接口实现中使用。因此，在Java中最好使用变量接口类型、方法返回类型、方法参数类型等。《Effective Java》 和《head first design pattern》书中也有提到。  
  

#### **原则10：委托原则**

  
该原则最典型的例子是Java中的equals() 和 hashCode() 方法。为了平等地比较两个对象，我们用类本身而不是客户端类来做比较。这个设计原则的好处是没有重复的代码，而且很容易对其进行修改。  
  
总之，希望这些面向对象的设计原则能帮助你写出更灵活更好的代码。理论是第一步，更重要的是需要开发者在实践中去运用和体会。

  

### 四、英文原文

**Object Oriented Design Principles** are core of OOP programming, but I have seen most of the Java programmers chasing design patterns like[Singleton pattern](http://javarevisited.blogspot.sg/2013/03/difference-between-singleton-pattern-vs-static-class-java.html), [Decorator pattern](http://java67.blogspot.sg/2013/07/decorator-design-pattern-in-java-real-life-example-tutorial.html) or Observer pattern, and not putting enough attention on learningObject oriented analysis and design. It's important to learn basics of Object oriented programming like Abstraction, Encapsulation, Polymorphism and Inheritance. But, at the same time, it's equally important to know object oriented design principles, to create clean and modular design. I have regularly seen Java programmers and developers of various experience level, who either doesn't heard about these**OOP** and **SOLID design principle,** or simply doesn't know what**benefits a particular design principle** offers, or how to apply these design principle in coding.   

  

Bottom line is, always strive for highly cohesive and loosely couple solution, code or design. Looking open source code from Apache and Sun are good examples of learning Java and OOPS design principles. They show us,  how design principles should be used in coding and Java programs. Java Development Kit follows several design principle like Factory Pattern inBorderFactory class,  Singleton pattern inRuntime class, Decorator pattern on variousjava.io classes. By the way if you really interested more on Java coding practices then read Effective Java by Joshua Bloch , a gem by the guy who wrote Java Collection API.  
  
 If you are interested in learning object oriented principles and patterns, then you can look at my another personal favorite[Head First Object Oriented Analysis and Design](http://www.amazon.com/dp/0596008678/?tag=javamysqlanta-20). This an excellent book and probably the best material available in object oriented analysis and design, but it often shadowed by its more popular cousin Head First Design Pattern by Eric Freeman. Later is more about how these principle comes together to create pattern you can use directly to solve known problems. These books helps a lot to write better code, taking full advantage of various Object oriented and SOLID design principles.  
  

[![](http://2.bp.blogspot.com/-Obqo1Yl95Gk/VjHR4RqvDVI/AAAAAAAAEC8/JtxxhuWoSuw/s1600/Head%2BFirst%2BObject-Oriented%2BAnalysis%2Band%2BDesign.jpg)](http://www.amazon.com/dp/0596008678/?tag=javamysqlanta-20)

  

[![Object oriented design principles and pattern in Java programming](http://2.bp.blogspot.com/-wrzDeQGAe1I/TWu8pLuLr4I/AAAAAAAAADE/V017G-6Q61w/s1600/java_logo_50_50.jpg)](http://javarevisited.blogspot.com/2011/09/spring-interview-questions-answers-j2ee.html)Though best way of learning any design principle or pattern is real world example and understanding the consequences of violating that design principle, subject of this article is IntroducingObject oriented design principles for Java Programmers, who are either not exposed to it or in learning phase. I personally think each of these OOPS and SOLID design principle need an article to explain them clearly, and I will definitely try to do that here, but for now just get yourself ready for quick bike ride on design principle town :)  
  
  

#### DRY (Don't repeat yourself)

Our first object oriented design principle is DRY, as name suggest**DRY (don't repeat yourself)** means don't write duplicate code, instead use[Abstraction](http://javarevisited.blogspot.com/2010/10/abstraction-in-java.html) to abstract common things in one place. If you have block of code in more than two place consider making it a separate method, or if you use a hard-coded value more than one time make them[public final constant](http://javarevisited.blogspot.com/2011/12/final-variable-method-class-java.html). Benefit of this Object oriented design principle is in maintenance. It's important  not to abuse it, duplication is not for code, but for functionality . It means, if you used common code to validateOrderID and SSN it doesn’t mean they are same or they will remain same in future. By using common code for two different functionality or thing you closely couple them forever and when your OrderID changes its format , your SSN validation code will break. So beware of such coupling and just don’t combine anything which uses similar code but are not related.  
  

#### Encapsulate What Changes

Only one thing is constant in software field and that is "Change", So encapsulate the code you expect or suspect to be changed in future. Benefit of this OOPS Design principle is that Its easy to test and maintain proper encapsulated code. If you are coding in Java then follow principle of making variable and methods private by default and increasing access step by step e.g. from private to protected and not public. Several of**design pattern in Java** uses Encapsulation, [Factory design pattern](http://javarevisited.blogspot.com/2011/12/factory-design-pattern-java-example.html) is one example of Encapsulation which encapsulate object creation code and provides flexibility to introduce new product later with no impact on existing code.  
  

  

#### Open Closed Design Principle

Classes, methods or functions should be Open for extension (new functionality) and Closed for modification. This is another beautiful SOLID design principle, which prevents some-one from changing already tried and tested code. Ideally if you are adding new functionality only than your code should be tested and that's the goal of[Open Closed Design principle](http://javarevisited.blogspot.com/2011/11/great-example-of-open-closed-design.html). By the way, Open Closed principle is "O" from SOLID acronym.

  

####  Single Responsibility Principle (SRP)

Single Responsibility Principle is another SOLID design principle, and represent  "S" on SOLID acronym. As per SRP, there should not be more than one reason for a class to change, or a class should always handle single functionality. If you put more than one functionality in one [Class in Java](http://javarevisited.blogspot.com/2011/10/class-in-java-programming-general.html)  it introduce **coupling** between two functionality and even if you change one functionality there is chance you broke coupled functionality,  which require another round of testing to avoid any surprise on production environment.  

#### Dependency Injection or Inversion principle

Don't ask for dependency it will be provided to you by framework. This has been very well implemented in Spring framework, beauty of this**design principle** is that any class which is injected by DI framework is easy to test with mock object and easier to maintain because object creation code is centralized in framework and client code is not littered with that.There are multiple ways to  implemented **Dependency injection** like using  byte code instrumentation which some AOP (Aspect Oriented programming) framework like AspectJ does or by using proxies just like used in Spring. See this[example of IOC and DI design pattern](http://javarevisited.blogspot.com/2012/12/inversion-of-control-dependency-injection-design-pattern-spring-example-tutorial.html) to learn more about this SOLID design principle. It represent "D" on SOLID acronym.  
  

#### Favor Composition over Inheritance

Always favor composition over inheritance ,if possible. Some of you may argue this, but I found that Composition is lot more flexible than[Inheritance](http://javarevisited.blogspot.sg/2012/10/what-is-inheritance-in-java-and-oops-programming.html). Composition allows to change behavior of a class at run-time by setting property during run-time and by using Interfaces to compose a class we use[polymorphism](http://javarevisited.blogspot.com/2011/08/what-is-polymorphism-in-java-example.html) which provides flexibility of to replace with better implementation any time. Even Effective Java advise to favor composition over inheritance. See[here](http://javarevisited.blogspot.sg/2015/06/difference-between-inheritance-and-Composition-in-Java-OOP.html) to learn more about why you Composition is better than Inheritance for reusing code and functionality. 

  

#### Liskov Substitution Principle (LSP)

According to Liskov Substitution Principle, Subtypes must be substitutable for super type i.e. methods or functions which uses super class type must be able to work with[object](http://javarevisited.blogspot.com/2012/12/what-is-object-in-java-or-oops-example.html) of sub class without any issue". LSP is closely related **to Single responsibility principle** and**Interface Segregation Principle**. If a class has more functionality than subclass might not support some of the functionality ,and does violated LSP. In order to follow**LSP SOLID design principle**, derived class or sub class must enhance functionality, but not reduce them. LSP represent  "L" on SOLID acronym.  

#### Interface Segregation principle (ISP)

Interface Segregation Principle stats that, a client should not implement an[interface](http://javarevisited.blogspot.com/2012/04/10-points-on-interface-in-java-with.html), if it doesn't use that. This happens mostly when one interface contains more than one functionality, and client only need one functionality and not other.Interface design is tricky job because once you release your interface you can not change it without breaking all implementation. Another benefit of this design principle in Java is, interface has disadvantage to implement all method before any class can use it so having single functionality means less method to implement.  

#### Programming for Interface not implementation

Always program for interface and not for implementation this will lead to flexible code which can work with any new implementation of interface. So use interface type on variables, return types of method or argument type of methods in Java. This has been advised by many Java programmer including in Effective Java and Head First design pattern book.  

#### Delegation principle

Don't do all stuff  by yourself,  delegate it to respective class. Classical example of delegation design principle is[equals() and hashCode() method in Java](http://javarevisited.blogspot.com/2011/02/how-to-write-equals-method-in-java.html). In order to compare two object for equality we ask class itself to do comparison instead of Client class doing that check. Benefit of this design principle is no duplication of code and pretty easy to modify behavior.

  
Here is nice summary of all these OOP design principles :  
  

[![Object oriented and SOLID design principle in Java](http://1.bp.blogspot.com/-Od9z4FHN9mA/VbjRcuQAcXI/AAAAAAAADfI/gc6uJdAP7bs/s640/10%2BOOP%2BDesign%2BPRinciples%2Bfor%2BJava%2Bprogrammers.png)](http://1.bp.blogspot.com/-Od9z4FHN9mA/VbjRcuQAcXI/AAAAAAAADfI/gc6uJdAP7bs/s1600/10%2BOOP%2BDesign%2BPRinciples%2Bfor%2BJava%2Bprogrammers.png)

  

All these **object oriented design principle** helps you write flexible and better code by striving high cohesion and low coupling. Theory is first step, but what is most important is todevelop ability to find out when to apply these design principle. Find out, whether we are violating any design principle and compromising flexibility of code, but again as nothing is perfect in this world, don't always try to solve problem with **design patterns and design principle** they are mostly for large enterprise project which has longer maintenance cycle.  
  
  
**Recommended books to learn Object Oriented analysis, design and patterns :**  

*   Head First Design Pattern by Eric Freeman \[[see here](http://www.amazon.com/dp/0596007124/?tag=javamysqlanta-20) \]
*   Head First Object Oriented Analysis and Design by O'Rielly \[[see here](http://www.amazon.com/dp/0596008678/?tag=javamysqlanta-20)\]

  
  
Read more: [http://javarevisited.blogspot.com/2012/03/10-object-oriented-design-principles.html#ixzz4aWzMOH00](http://javarevisited.blogspot.com/2012/03/10-object-oriented-design-principles.html#ixzz4aWzMOH00)  （需要翻墙）

  

参考：[http://www.iteye.com/news/24488](http://www.iteye.com/news/24488)

[http://www.cnblogs.com/hnrainll/archive/2012/09/18/2690846.html](http://www.cnblogs.com/hnrainll/archive/2012/09/18/2690846.html)