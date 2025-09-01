---
title: 有经验的Java开发者和架构师容易犯的10个错误
id: 295
date: 2024-10-31 22:01:42
author: daichangya
excerpt: "首先允许我们问一个严肃的问题？为什么Java初学者能够方便的从网上找到相对应的开发建议呢？每当我去网上搜索想要的建议的时候，我总是能发现一大堆是关于基本入门的教程、书籍以及资源。同样也发现网上到处充斥着从宽泛的角度描述一个大型的企业级项目：如何扩展你的架构，即使是经验丰富的Java开发人员和架构师也会犯错。今天，我们讨论了如果您不密切注意，您可能会犯的Java开发人员常见错误！"
permalink: /archives/19085033/
categories:
 - 软件设计
---

即使是经验丰富的Java开发人员和架构师也会犯错。今天，我们讨论了如果您不密切注意，您可能会犯的Java开发人员常见错误！我根据烦恼将它们按降序排列-＃1最让我困扰，但是根据其他因素，所有这10个人都会给您带来相同的伤害;-)

常见Java错误＃10：滥用或误解依赖注入
---------------------

[依赖注入](http://en.wikipedia.org/wiki/Dependency_injection)通常被认为是企业项目中的“一件好事”。使用它不会出错。但这是真的吗？

DI的基本思想之一是，您无需以对象查找其依赖关系，而是在以定义良好的方式（使用DI框架）创建对象之前初始化依赖关系，而在实际创建对象时，只需将其传递给对象即可。构造函数中的预配置对象（constructor-injection）或使用方法（方法注入）。

但是，最重要的是，您通过了对象的需求，仅此而已。但是，即使在全新项目中，我仍然可以找到这样的代码：

```
    public class CustomerBill {
            	
            //Injected by the DI framework
            private ServerContext serverContext;
            	
            	
            public CustomerBill(ServerContext serverContext)
            {
                        this.serverContext = serverContext;
            }
            	
            public void chargeCustomer(Customer customer)
            {
                        CreditCardProcessor creditCardProcessor = serverContext.getServiceLocator().getCreditCardProcessor();
                        Discount discount  = serverContext.getServiceLocator().getActiveDiscounts().findDiscountFor(customer);
                        	
                        creditCardProcessor.bill(customer,discount);
            }
    }
```

  
当然，这不是真正的DI。该对象仍然自行进行初始化。排队的“火车代码”的存在`serverContext.getServiceLocator().getCreditCardProcessor()`是在这里出问题的另一种指示。

当然，正确的方法是像这样直接传递最终对象：

    
```
    public class CustomerBillCorrected {
            	
            //Injected by the DI framework
            private ActiveDiscounts activeDiscounts;
            	
            //Injected by the DI framework
            private CreditCardProcessor creditCardProcessor;
            	
            	
            public CustomerBillCorrected(ActiveDiscounts activeDiscounts,CreditCardProcessor creditCardProcessor)
            {
                        this.activeDiscounts = activeDiscounts;
                        this.creditCardProcessor = creditCardProcessor;
            }
            	
            public void chargeCustomer(Customer customer)
            {
                        Discount discount  = activeDiscounts.findDiscountFor(customer);
                        	
                        creditCardProcessor.bill(customer,discount);
            }
    }
```

常见的Java错误＃9：伪装Java更像Perl
------------------------

与其他语言相比，Java的优点之一是其类型安全性方法。在您是唯一开发人员的小型项目中，几乎可以采用任何喜欢的编码样式。但是，在大型Java代码库和复杂的系统上，出现问题时需要早期警告。大多数编程错误应在编译时而不是在运行时捕获。

Java提供了许多便利来促进这些编译时警告。但是，当您像这样编写代码时，用脚射击自己并没有什么能做的：

    
```
    public class AnimalFactory {
            	
            public static Animal createAnimal(String type)
            {
                        switch(type)
                        {
                        case "cat":
                                    return new Cat();
                        case "cow":
                                    return new Cow();
                        case "dog":
                                    return new Dog();
                        default:
                                    return new Cat();
                        }
            }
     
    }
```

  
该代码非常危险，因为没有任何编译时检查可以节省您的时间。开发人员可能会使用拼写错误的字符串来呼叫您的工厂，例如`createAnimal(“dig”)`期待狗（而不是猫）。该代码将正常编译，并且该错误将仅在以后的运行时出现。根据应用程序的不同，错误的出现可能会在应用程序正式投入生产后一个月！哎哟。

请帮自己一个忙，并使用Java提供的所有功能来保证编译时的安全。这是一种更正确的方法（还有其他可能的解决方案），仅在正确时才进行编译。

```
    public class AnimalFactoryCorrected {
            public enum AnimalType { DOG, CAT,COW,ANY};
            	
            public static Animal createAnimal(AnimalType type)
            {
                        switch(type)
                        {
                        case CAT:
                                    return new Cat();
            	    case COW:
                                    return new Cow();
                        case DOG:
                                    return new Dog();
                        case ANY:
                        default:
                                    return new Cat();
                        }
            }
     
    }
```

常见的Java错误＃8：假装Java更像C（即不了解OOP）
------------------------------

早在C时代，建议的编写代码的[方法就是过程方法](http://en.wikipedia.org/wiki/Procedural_programming)。您的数据存在于[结构中，](http://en.wikipedia.org/wiki/Struct_(C_programming_language))并且通过函数对数据进行操作。数据很愚蠢，方法很聪明。

但是，Java是一种[面向对象的语言](https://en.wikipedia.org/wiki/Object-oriented_programming)，与这种方法相反。数据和函数绑定在一起（创建类），这些函数和函数应该自己聪明。

但是，许多Java开发人员要么不了解它们之间的区别，要么就不费心去编写OOP代码，即使他们内心深处知道他们的过程方法似乎不合适。

Java应用程序中过程代码的最佳指示之一是**instanceof**操作的使用以及跟在_其后_的相应上_下游_代码段。该**的instanceof**运算符当然有它的有效用途，但在平时的企业代码这是一个巨大[的反模式](http://www.javapractices.com/topic/TopicAction.do?Id=31)。

这是一个不涉及动物的示例：

```
    public void bill(Customer customer, Amount amount) {
    
                        Discount discount = null;
                        if(customer instanceof VipCustomer)
                        {
                                    VipCustomer vip = (VipCustomer)customer;
                                    discount = vip.getVipDiscount();
                        }
                        else if(customer instanceof BonusCustomer)
                        {
                                    BonusCustomer vip = (BonusCustomer)customer;
                                    discount = vip.getBonusDiscount();
                        }
                        else if(customer instanceof LoyalCustomer)
                        {
                                    LoyalCustomer vip = (LoyalCustomer)customer;
                                    discount = vip.getLoyalDiscount();
                        }
    
                        paymentGateway.charge(customer, amount);
    
            }
```
  
可以按[以下OOP方式重构](http://www.artima.com/interfacedesign/PreferPoly.html)此代码：

```
    public void bill(Customer customer, Amount amount) {
    
                       Discount discount = customer.getAppropriateDiscount();
    
                        paymentGateway.charge(customer, amount);
    
            }
```
扩展_Customer_（或实现_Customer_接口）的每个类都定义了一个折扣方法。这样做的好处是您可以添加新类型的客户，而无需接触客户管理系统。对于**instanceof**变体，添加新客户意味着您将必须搜索客户打印代码，客户账单代码，客户联系代码等，并为新类型添加新的if语句。

您还应该查看有关[富域](http://en.wikipedia.org/wiki/Anemic_domain_model)模型[和贫流域](http://en.wikipedia.org/wiki/Anemic_domain_model)模型的讨论。

常见的Java错误7：使用过多的延迟加载（即，不了解对象生命周期）
---------------------------------

我更经常发现以下代码：

```
    public class CreditCardProcessor {
            private PaymentGateway paymentGateway = null;
    
            public void bill(Customer customer, Amount amount) {
    
            	//Billing a customer always needs a payment gateway anyway
              	getPaymentGateway().charge(customer.getCreditCart(),amount);
    
            }
    
            private PaymentGateway getPaymentGateway()
            {
                        if(paymentGateway == null)
                        {
                                    paymentGateway = new PaymentGateway();
                                    paymentGateway.init(); //Network side Effects  here
                        }
                        return paymentGateway;
            }
    
    }
```
延迟加载的最初想法是正确的：如果您有一个昂贵的对象，则仅在需要时才创建它。但是，在应用此技术之前，您必须真正确保：

*   该对象确实是“昂贵的”（您如何定义它？）
*   在某些情况下，不使用对象（因此不需要创建对象） 

**如果**对象中的结构不是真正的“沉重”或运行时始终创建的对象，我将越来越多地看到这种结构-那么有什么好处呢？

过度使用此技术的主要问题是它隐藏了组件的生命周期。一个构建良好的应用程序具有其主要结构的明确生命周期。应该清楚何时创建，使用和销毁对象。几个DI框架可以帮助您实现对象生命周期。

但是，当对象创建产生副作用时，这种技术真正可怕的用途就来自图片。这意味着您的应用程序的状态取决于对象创建的顺序（进入的请求类型的顺序）。由于涉及的案例太多，因此突然调试应用程序几乎是不可能的。复制生产中发生的问题是一项艰巨的任务，因为您必须知道if语句的运行顺序。

无需使用此方法，只需定义应用程序启动期间所需的所有对象。这还有一个额外的优势，那就是您可以在应用程序部署期间发现任何致命问题。

常见的Java错误＃6：取决于“四人帮”（GOF）书作为您的圣经（又名GOF宗教）
-----------------------------------------

我真的很羡慕《[设计模式》这本书的作者](http://en.wikipedia.org/wiki/Design_Patterns)。单一出版物以一种其他书籍无法胜过的方式影响了整个IT行业。设计模式甚至已经进入了工作面试过程，而且有时候，如果您不阅读本书并记住几种设计模式的名称和公式，您有时将无法获得IT职位。希望那个时代正在慢慢消失。

现在不要误会我的意思；这本书本身还不错。就像整个历史一样，问题出在人们如何使用和解释它。这是通常的情况：

1.  马克（Mark）是建筑师，他把手放在GOF书上并阅读。他认为这太酷了！
2.  Mark查看他正在研究的当前代码库。
3.  马克选择了他喜欢的设计模式，并将其应用到当时的代码中
4.  马克将本书传递给高级开发人员，这些高级开发人员从步骤1开始相同的周期。

结果代码一团糟。

本书的简介中清楚地描述了正确使用该书的方式（适用于那些确实不愿阅读的人）。您遇到的问题是，您一遍又一遍地绊脚石，而本书为您提供了过去曾解决过类似问题的解决方案。注意事件的正确顺序。我有一个问题，我看书，然后找到解决问题的方法。

不要陷入看书，寻找喜欢的解决方案，然后尝试将其应用到代码中的某个随机位置的陷阱中，尤其是因为书中提到的某些模式不再有效（请参阅＃5）下面）…。

常见的Java错误＃5：使用Singletons（这是一种反模式！）
----------------------------------

我已经在前面提到了设计模式。但是，[单身人士](http://en.wikipedia.org/wiki/Singleton_pattern)需要一个观点。我请大家重复我100次;-)

*   单例是反模式
*   单例是反模式
*   单例是反模式
*   单例是反模式
*   单例是反模式... 

单例在某个时间点使用它们。但是，**借助现代的依赖注入框架，可以完全消除单例。**当您使用单例时，实际上是在代码中引入了一组新问题。为什么？因为：

1.  单例在类中创建隐藏的依赖项
2.  单例使代码不可测试（即使带有嘲笑）
3.  单例将资源创建与资源获取混合在一起
4.  单例允许对全局状态产生副作用
5.  单例可能是并发问题的根源

如果您仍然不相信我，那么有很多文档说明为什么单例现在是反模式。搜索，您将找到它。

常见Java错误＃4：忽略方法可见性
------------------

当我遇到经验丰富的Java开发人员时，我总是感到惊讶，他们认为Java只有三个保护修饰符。好吧，它有四个（！），并且还有**包private**（也称为**default**）。不，我不会在这里解释它的作用。去查一下

我要解释的是，您应该注意**公开的**方法。应用程序中的公共方法是应用程序的可见API。这应该尽可能的小巧紧凑，尤其是在编写可重用的库时（另请参见[SOLID](https://jrebel.com/rebellabs/solid-object-oriented-design-principles/)原理）。

我真的很讨厌看到应该**私有的**公共方法。不仅因为它们公开了类的内部实现细节，而且还因为几乎根本不应该在此类之外使用它们。

结果是，您始终对类的公共方法使用[单元测试](/blog/unit-testing-cloud-applications-in-java)。我见过所谓的架构师，他们相信将私有方法转换为公共方法以使他们可以对它们进行单元测试是可以接受的。

测试私有方法是完全错误的。只需测试调用私有方法的公共方法。请记住：决不要因为单元测试而用更多的公共方法扩展API。

常见的Java错误＃3：遭受项目特定的StringUtils（即或更一般的NIH综合征）的折磨
-----------------------------------------------

在过去，每个足够大的Java项目都包含StringUtils，DateUtils，FileUtils等文件。现在，当我在旧版代码中看到它时，我就明白了。相信我，我感到您的痛苦！我知道这些文件为使它们成熟和稳定所做的一切努力，因为太多的代码依赖于它们。

但是，当我在全新的代码上看到像这样的文件而又没有任何依赖关系时，我的一部分就会陷入困境。架构师和高级开发人员的职责之一是跟踪经过测试的现有解决方案，这些解决方案更容易集成到您的应用程序中。

如果您的职称中包含“建筑师”一词，那么您就不会因为不了解[Apache Commons](http://commons.apache.org/)，[Guava库](https://code.google.com/p/guava-libraries/)或[Joda Date库而](http://www.joda.org/joda-time/)找借口。

在不熟悉的区域编写代码之前，还应该进行一些研究。例如，在编写用于创建PDF文件的REST服务之前，请花一些时间来了解存在于Java的REST框架以及创建PDF文件的建议方法。（不建议运行unix命令行应用程序。Java可以通过[itext](http://itextpdf.com/)自己创建PDF文件）。

常见的Java错误＃2：依赖于环境的构建
--------------------

我已经与Java开发团队合作了10年，现在，我告诉您一个秘密：**这只是构建企业应用程序的一种可接受的方法。**这是您的操作方式：

1.  我有一天会在您的软件公司中崭露头角。
2.  我将注意力集中在工作站上，并安装Java和我最喜欢的IDE /工具。
3.  我从公司存储库（svn，git或其他）中签出代码。
4.  我最多花5分钟来了解您所拥有的构建系统（例如Maven，Gradle甚至是Ant）。
5.  我运行一个命令来构建应用程序，并且成功。

这不仅是最佳方案，而且如果您已关注应用程序的构建方式，则这是唯一有效的方案。

如果您的企业应用程序依赖于特定的IDE，特定版本的IDE插件，PC上的本地文件，额外的，未记录的环境设置，网络资源或任何非标准的东西，那么该是重新考虑构建系统的时候了。

另外一个相关的事实是构建应该一步完成（请参阅[Joel测试](http://www.joelonsoftware.com/articles/fog0000000043.html)）。

现在不要误会我-集成测试，自检版本或额外的部署/文档步骤可以具有额外的设置或使用外部数据库（应在公司Wiki中进行记录）。

但是，获取可执行文件的简单编译方案最多应该花费一个小时的时间。我见过一些项目，新员工的第一次编译需要2天的时间（以设置环境）。

常见的Java错误＃1：使用反射/自省
-------------------

新闻快讯：如果您正在编写[ORM](http://en.wikipedia.org/wiki/Object-relational_mapping)框架，Java代理，元编译器，IDE或其他奇特的东西，则可以根据需要使用Java反射。但是，对于大多数企业应用程序而言，它们实际上只是数据存储上的美化的[CRUD](http://en.wikipedia.org/wiki/Create,_read,_update_and_delete)接口，Java [反射](http://docs.oracle.com/javase/tutorial/reflect/)实在是太过分了。

我经常看到以性能，向后兼容甚至向前兼容的名义使用反射。几乎总是错误地使用它。反思总是基于一些假设（例如方法名称约定），这些假设在今天可能会成立，但明天可能会成立。

反射问题很难理解，很难调试，很难解决。

而且我什至不打算研究[自我修改的代码](http://en.wikipedia.org/wiki/Self-modifying_code)。在企业Java应用程序中使用反射就像在建筑物的基础上插入定时炸弹。该建筑物现在可能已经稳定了，但是一旦计时器启动，一切都会崩溃。

令我感到困惑的是，引入反射的建筑师总是将反射视为“基本”，而实际上，您可以通过精心构建的对象层次结构和明确的插件体系结构/文档清晰地解决相同的问题。

因此，让我为您在那里的所有“建筑师”提供说明。它**IS**可以创建一个稳定，快速和易于维护的企业级Java应用程序**无**使用反射。如果您的香草型企业应用程序使用反射，那么您只是在自找麻烦。

奖励部分：只有在了解实际瓶颈后，才尝试进行优化
-----------------------

我见过在以下方面花费大量精力的建筑师：

*   微调日志记录语句
*   在旧版代码中替换向量
*   在循环中用StringBuffers替换+运算符
*   为了“性能”而重构现有的，稳定的，成熟的且无错误的代码
*   …和其他奇特的东西\[/ list\]

可悲的是，这样做并没有实际衡量这些努力可能产生的影响。即使应用程序运行速度更快，大多数情况下，还有其他更严重的问题（例如数据库锁定，内存泄漏，永远不会关闭/刷新的流）没有人关注。

修复SQL查询将使速度提高200％时，花费时间来修复日志记录并获得3％的速度并不是很有帮助。

因此，请务必记住，由于性能原因而发生的任何更改实际上都是一个四个步骤的过程：

1.  测量当前系统（有效的基准测试本身就是一项艰巨的任务）
2.  套用变更
3.  再次测量
4.  评估付出的努力和绩效获得的比率。 

记住优化的口头禅- **测量，不要猜测。**

结论
--

如果我看起来有些脾气暴躁，那是因为我除了清理经验丰富的编码员留下的混乱之外，还承担了其他许多工作。从某种程度上说，它比解决n00bs所犯的错误还要糟糕-高级开发人员应该更了解！;-)

希望这份由高级开发人员提出的10个常见陷阱的清单可以帮助您发现应该在解决问题中使用您的专业知识的一些领域。即使是最优秀的编码人员，也应该记住，总有一些东西需要重新学习并付诸实践。

寻找其他提高性能的方法吗？我们的电子书[Java的“隐藏的生产力杀手](https://www.jrebel.com/resources/javas-hidden-productivity-killer) ”概述了Java开发过程中最严重的生产力中断之一。

是否想避免微服务应用程序中的性能瓶颈？请务必检查XRebel。它可以帮助开发人员在开发过程中识别和修复潜在的性能问题。

单击下面的按钮，在我们即将发布的演示中了解XRebel在实时编码环境中的工作方式。

[参见XRebel的实际应用](https://www.jrebel.com/java-toolkit-demo)