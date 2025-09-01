---
title: Java设计模式——职责链模式：解锁高效灵活的请求处理之道
id: 6dd97f4b-5471-44ce-9364-2d9783d2a8f6
date: 2024-11-25 10:42:02
author: daichangya
cover: https://images.jsdiff.com/design02.jpg
excerpt: "🔥《Java 设计模式之职责链模式：解锁高效灵活的请求处理之道》🚀 嘿，各位 Java 编程大神和爱好者们！今天咱们要一同深入探索一种超厉害的设计模式——职责链模式。它就像一条神奇的“处理链”，能让请求在多个对象之间有条不紊地传递，直到找到最合适的“处理者”。准备好跟我一起揭开它神秘的面纱，看看"
permalink: /archives/javashe-ji-mo-shi--xing-wei-mo-shi/
categories:
 - 设计模式
---

# 🔥《Java 设计模式之职责链模式：解锁高效灵活的请求处理之道》🚀

嘿，各位 Java 编程大神和爱好者们！今天咱们要一同深入探索一种超厉害的设计模式——职责链模式。它就像一条神奇的“处理链”，能让请求在多个对象之间有条不紊地传递，直到找到最合适的“处理者”。准备好跟我一起揭开它神秘的面纱，看看如何用代码实现这种强大的模式，让我们的程序变得更加智能和灵活吧！💥

## 一、职责链模式：请求处理的“智能传送带”🎯

### （一）模式定义与神奇特点
职责链模式可是对象行为模式家族里的“明星成员”哦！想象一下，有一群对象像链条上的环一样紧密相连，每个对象都知道下一个对象是谁（持有下家的引用）。当一个请求像小包裹一样在这条链上传递时，它会逐个经过这些对象。而发出请求的客户端呢，就像把包裹送到快递公司后就安心等待结果一样，完全不用操心到底是哪个对象最终会处理这个请求。这种模式最大的魅力在于它赋予了系统超级强大的灵活性。比如说，我们可以随时调整这条链的结构，添加、删除或者重新排列处理者，而客户端那边却感觉不到任何变化，就像魔法一样！🧙‍♂️

用一个超形象的比喻来理解，职责链模式就像是一场接力赛跑，每个选手（处理者）都有自己的能力范围（处理条件）。当接力棒（请求）传来时，如果这个选手有能力完成接下来的路程（处理请求），那就全力冲刺；如果觉得自己力不从心，就迅速把接力棒交给下一个选手，直到找到那个能冲过终点线（处理请求）的“大神”选手。

再举个生活中的例子，就拿击鼓传花来说吧。一群小伙伴围成一个圈（形成责任链），鼓声响起时开始传花（请求传递）。每个小伙伴就像是链上的一个处理者，当花传到自己手上时，如果鼓声停止（满足某种条件），那这个小伙伴就要表演节目（处理请求）；如果鼓声还在响，就赶紧把花传给下一个小伙伴。这里的小伙伴们可以站成直线、围成环形或者组成树状结构的一部分，具体怎么站完全取决于大家想怎么玩这个游戏（业务逻辑和需求）。🎊
<separator></separator>
### （二）模式结构大揭秘
1. **抽象处理者（Handler）：链的“基石”与“规则制定者”**
   - 抽象处理者就像是整个职责链的“总设计师”，它定义了处理请求的统一接口，就像给所有处理者制定了一套必须遵守的“游戏规则”。在某些情况下，它还会规定怎么设置和获取下一个处理者（下家）的方法。一般来说，它会以抽象类或者接口的形式存在，为具体的处理者提供了一个清晰的行为框架和接口规范，确保所有处理者都能“按章办事”。就好比建筑蓝图，规定了房子该怎么盖，每个房间的布局和功能一样。🏠
2. **具体处理者（ConcreteHandler）：请求的“接收者”与“传递者”**
   - 具体处理者可是链上的“实干家”，当请求送到它面前时，它有两种选择。一种是根据自己的能力和判断，决定是否亲自处理这个请求。如果它觉得自己能行，就会按照自己的方式处理请求，就像厨师根据订单（请求）烹饪美食（处理逻辑）；另一种情况是，如果它觉得自己搞不定，或者根据业务规则应该让更厉害的人来处理，它就会毫不犹豫地把请求转交给下家。因为它知道下家是谁（持有下家引用），所以能轻松地把请求传递下去，让请求继续在链上“旅行”。就像快递员，如果发现包裹的目的地不在自己的配送范围内，就会转交给下一个区域的快递员。🚚

### （三）代码实现：构建职责链
下面是一个用 Java 实现的职责链模式的简单示例代码，让我们一起来看看它是如何工作的。

```java
// 抽象处理者（Handler）
abstract class Handler {
    // 持有下一个处理者的引用
    protected Handler successor;

    // 设置下一个处理者的方法
    public void setSuccessor(Handler successor) {
        this.successor = successor;
    }

    // 抽象的处理请求方法，具体处理逻辑由子类实现
    abstract public void handleRequest(int request);
}

// 具体处理者 1（ConcreteHandler1）
class ConcreteHandler1 extends Handler {
    @Override
    public void handleRequest(int request) {
        // 如果请求在 0 到 10 之间（这里只是一个简单的示例条件），则由当前处理者处理
        if (request >= 0 && request < 10) {
            System.out.println(this + " handled request " + request);
        } else if (successor!= null) {
            // 否则，将请求传递给下一个处理者（如果有下家的话）
            successor.handleRequest(request);
        }
    }
}

// 具体处理者 2（ConcreteHandler2）
class ConcreteHandler2 extends Handler {
    @Override
    public void handleRequest(int request) {
        if (request >= 10 && request < 20) {
            System.out.println(this + " handled request " + request);
        } else if (successor!= null) {
            successor.handleRequest(request);
        }
    }
}

// 具体处理者 3（ConcreteHandler3）
class ConcreteHandler3 extends Handler {
    @Override
    public void handleRequest(int request) {
        if (request >= 20 && request < 30) {
            System.out.println(this + " handled request " + request);
        } else if (successor!= null) {
            successor.handleRequest(request);
        }
    }
}

// 客户端测试类
public class Client {
    public static void main(String[] args) {
        // 创建处理者对象
        Handler h1 = new ConcreteHandler1();
        Handler h2 = new ConcreteHandler2();
        Handler h3 = new ConcreteHandler3();

        // 设置处理者之间的链关系，形成 h1 -> h2 -> h3 的链
        h1.setSuccessor(h2);
        h2.setSuccessor(h3);

        // 生成一些请求并处理
        int[] requests = {2, 5, 14, 22, 18, 3, 27, 20};

        for (int request : requests) {
            h1.handleRequest(request);
        }
    }
}
```

![Responsibility.jpg](https://images.jsdiff.com/Responsibility.jpg)


### （四）纯与不纯的职责链模式
1. **纯职责链模式：规则严格的“处理链”**
   - 在纯职责链模式的世界里，规则那是相当严格的。对于每一个具体的处理者来说，当收到请求时，它只能二选一：要么勇敢地承担起处理请求的全部责任，就像独自扛起一座大山；要么毫不犹豫地把责任推给下家，绝不拖泥带水。而且，在这条链上，每个请求就像一个被精心安排的小旅客，必定会被某个处理者收留并妥善处理，绝对不会出现被忽视、流落街头的情况。不过呢，这种模式在现实生活中的例子比较少，因为它的实现和应用场景相对来说有点“挑食”，要求比较高，不够灵活。就像一个只接受特定规格零件的精密仪器，稍微有点不匹配就无法工作。🔍
2. **不纯职责链模式：适应变化的“万能链”**
   - 不纯职责链模式就随和多了，它允许请求在传递过程中，即使经过了所有的处理者，也可能找不到一个愿意收留它的“家”。这种模式在实际开发中可是非常受欢迎的“大众明星”，因为它能更好地应对复杂多变的业务需求。比如说，在某些业务场景中，一个请求可能像一个挑剔的顾客，在经过一系列的服务者（处理者）后，还是没有找到满意的服务（没有合适的处理者）。这时候，系统可以根据预先设定的策略，比如记录下这个“挑剔顾客”的需求（记录日志），或者礼貌地告诉它“不好意思，我们无法满足您的需求”（返回错误信息）。就像一家餐厅，如果遇到顾客点了菜单上没有的菜品，服务员可以记录下来反馈给厨房（记录日志），或者向顾客解释并推荐其他菜品（返回错误信息）。🍽

### （五）实际应用案例：采购审批系统中的职责链
让我们来看一个更贴近实际工作场景的例子——采购审批系统。

```java
// 抽象审批者（Approver）
abstract class Approver {
    // 审批者姓名
    protected String name;
    // 持有下一个审批者的引用
    protected Approver successor;

    // 构造函数，初始化审批者姓名
    public Approver(String name) {
        this.name = name;
    }

    // 设置下一个审批者的方法
    public void setSuccessor(Approver successor) {
        this.successor = successor;
    }

    // 抽象的审批请求方法，具体审批逻辑由子类实现
    abstract public void processRequest(PurchaseRequest request);
}

// 主管审批者（Director）
class Director extends Approver {
    public Director(String name) {
        super(name);
    }

    @Override
    public void processRequest(PurchaseRequest request) {
        if (request.getAmount() < 10000.0) {
            System.out.println(this + " " + name + " approved request# " + request.getNumber());
        } else if (successor!= null) {
            successor.processRequest(request);
        }
    }
}

// 副总裁审批者（VicePresident）
class VicePresident extends Approver {
    public VicePresident(String name) {
        super(name);
    }

    @Override
    public void processRequest(PurchaseRequest request) {
        if (request.getAmount() < 25000.0) {
            System.out.println(this + " " + name + " approved request# " + request.getNumber());
        } else if (successor!= null) {
            successor.processRequest(request);
        }
    }
}

// 总裁审批者（President）
class President extends Approver {
    public President(String name) {
        super(name);
    }

    @Override
    public void processRequest(PurchaseRequest request) {
        if (request.getAmount() < 100000.0) {
            System.out.println(this + " " + name + " approved request# " + request.getNumber());
        } else {
            System.out.println("Request# " + request.getNumber() + " requires an executive meeting!");
        }
    }
}

// 采购请求类（PurchaseRequest）
class PurchaseRequest {
    private double amount;
    private int number;

    public PurchaseRequest(double amount, int number) {
        this.amount = amount;
        this.number = number;
    }

    public double getAmount() {
        return amount;
    }

    public int getNumber() {
        return number;
    }
}
```

在这个采购审批系统中，我们定义了不同级别的审批者，从主管、副总裁到总裁，他们就像一条职责链上的各个环节。当一个采购请求（就像一个任务包裹）被提交后，它会从主管开始，沿着这条审批链依次传递。如果采购金额比较小，比如小于 10000 元，主管就可以直接批准（处理请求）；如果金额超过了主管的审批权限，主管就会把请求交给副总裁。副总裁也会根据金额大小决定是否批准，如果金额超过了副总裁的权限，就继续传递给总裁。这样，不同金额的采购请求就能找到合适的审批者进行处理。而且，如果未来公司的审批流程发生了变化，比如增加了新的审批层级或者修改了审批金额的限制，我们只需要在相应的审批者类中进行修改，就像调整链条上的某个环节一样，不会对整个审批系统的结构造成太大的影响。这就是职责链模式在实际应用中的强大之处，它让系统变得更加灵活和易于维护。💼

## 二、总结与展望：职责链模式的无限潜力💡

通过对职责链模式的深入学习，我们就像获得了一把神奇的钥匙，可以打开高效灵活处理请求的大门。它不仅让我们的代码结构更加清晰，各个处理者之间的职责分明，还让系统能够轻松应对各种变化，无论是业务规则的调整还是处理流程的优化。

在未来的开发中，我们可以继续探索职责链模式的更多应用场景，比如在工作流系统、消息处理系统、异常处理机制等方面都可以发挥它的优势。同时，我们也可以结合其他设计模式，如工厂模式来创建处理者对象，或者结合装饰者模式来增强处理者的功能，让我们的程序更加健壮和强大。相信只要我们善于运用这些设计模式，就能打造出更加优秀、高效的软件系统，在编程的世界里创造更多的精彩！🚀