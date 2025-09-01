---
title: Java设计模式——中介者模式：优化复杂对象交互的利器
id: e9f58e15-94af-4643-a3fd-c731b378135b
date: 2024-11-25 10:21:52
author: daichangya
cover: https://images.jsdiff.com/design02.jpg
excerpt: 一、中介者模式概述 （一）生活场景引出中介者模式 在大学班级场景中，如果没有类似QQ这样的通讯工具，班长或团支书传达消息以及同学之间交流就会呈现出一种复杂的网状结构。随着同学数量增多，这种网状结构会变得更加混乱，对象之间存在大量联系，耦合性极高，不利于复用和系统扩展。例如，新转来一个学生，可能需要改
permalink: /archives/Java-she-ji-mo-shi-zhong-jie-zhe-mo-shi/
categories:
- 设计模式
---

## 一、中介者模式概述
### （一）生活场景引出中介者模式
在大学班级场景中，如果没有类似QQ这样的通讯工具，班长或团支书传达消息以及同学之间交流就会呈现出一种复杂的网状结构。随着同学数量增多，这种网状结构会变得更加混乱，对象之间存在大量联系，耦合性极高，不利于复用和系统扩展。例如，新转来一个学生，可能需要改动很多地方来适应这种复杂的联系。

### （二）中介者模式的定义与作用
中介者模式（Mediator Pattern）定义一个中介对象来封装系列对象之间的交互。中介者使各个对象不需要显式地相互引用，从而使其耦合性松散，而且可以独立地改变它们之间的交互。就像引入QQ群后，班级同学之间的交流变为星形结构，每个学生对象不再直接耦合，而是通过QQ群（中介者）进行交流。（配图：展示班级同学交流从网状结构变为星形结构的示意图，突出QQ群作为中介者的作用）

### （三）中介者模式的结构
1. **角色构成**
   - **抽象中介者（Mediator）**：定义了同事对象到中介者对象的接口，一般包含添加同事对象、通知同事对象等方法。例如，在代码中抽象中介者类有`add_student`（添加学生）、`notify`（通知）和`chart`（交流）等方法，为具体中介者类提供了统一的接口规范。
   - **具体中介者（ConcreteMediator）**：实现抽象中介者的接口，协调各个同事对象之间的交互。如代码中的`QQMediator`类，通过实现`notify`方法来通知所有学生（同事对象），实现`chart`方法来处理两个学生之间的私下交流。
   - **抽象同事类（Colleague）**：定义同事类的接口，声明同事对象的相关方法，通常包含设置和获取自身信息以及与中介者交互的方法。在代码中，抽象同事类`Colleage`有设置和获取姓名、内容的方法，以及虚函数`talk`用于同事对象表达自己的内容。
   - **具体同事类（ConcreteColleague）**：实现抽象同事类的接口，每个具体同事类代表系统中的一个具体对象，它们与中介者协作来完成自身的行为。如班长（`Monitor`）、团支书（`TuanZhiShu`）、同学A（`StudentA`）和同学B（`StudentB`）等具体同事类，分别实现了`talk`方法来输出自己要说的话。

## 二、中介者模式代码实现
### （一）抽象同事类（Colleague）
```cpp
// 抽象的同事类
class Colleage {
private:
    string name;
    string content;
public:
    Colleage(string n = "") : name(n) {};
    void set_name(string name) {
        this->name = name;
    }
    string get_name() {
        return this->name;
    }
    void set_content(string content) {
        this->content = content;
    }
    string get_content() {
        return content;
    }
    virtual void talk() {};
};
```
### （二）具体同事类
1. **班长（Monitor）**
```cpp
// 具体的同事类:班长
class Monitor : public Colleage {
public:
    Monitor(string n = "") : Colleage(n) {};
    virtual void talk() {
        cout << "大班长说：" << get_content() << endl;
    }
};
```
2. **团支书（TuanZhiShu）**
```cpp
// 具体的同事类:团支书
class TuanZhiShu : public Colleage {
public:
    TuanZhiShu(string n = "") : Colleage(n) {};
    virtual void talk() {
        cout << "团支书说：" << get_content() << endl;
    }
};
```
3. **同学A（StudentA）**
```cpp
// 具体的同事类:同学A
class StudentA : public Colleage {
public:
    StudentA(string n = "") : Colleage(n) {};
    virtual void talk() {
        cout << "学生A说：" << get_content() << endl;
    }
};
```
4. **同学B（StudentB）**
```cpp
// 具体的同事类:同学B
class StudentB : public Colleage {
public:
    StudentB(string n = "") : Colleage(n) {};
    virtual void talk() {
        cout << "学生B说：" << get_content() << endl;
    }
};
```
### （三）抽象中介者（Mediator）
```cpp
// 抽象中介者
class Mediator {
public:
    vector<Colleage*> studentList;
    virtual void add_student(Colleage *student) {
        studentList.push_back(student);
    };
    virtual void notify(Colleage *student) {};
    virtual void chart(Colleage *student1, Colleage *student2) {};
};
```
### （四）具体中介者（QQMediator）
```cpp
// 具体中介者qq通讯平台
class QQMediator : public Mediator {
public:
    virtual void notify(Colleage *student) {
        student->talk();
        for (int i = 0; i < studentList.size(); ++i) {
            // 不是说话者
            if (student!= studentList[i]) {
                studentList[i]->talk();
            }
        }
    };
    virtual void chart(Colleage *student1, Colleage *student2) {
        student1->talk();
        student2->talk();
    }
};
```
### （五）主函数（main）
```cpp
int main() {
    QQMediator qq;
    Monitor studentMonitor("Vincent");
    TuanZhiShu studentTuanZhiShu("Robort");
    StudentA studentA("Sam");
    StudentB studentB("Tom");
    /* ----------------------班长发通知----------------------------- */
    cout << "下面的班长发布一个通知的场景：" << endl;
    // 将同学们加入到qq群中
    qq.add_student(&studentMonitor);
    qq.add_student(&studentTuanZhiShu);
    qq.add_student(&studentA);
    qq.add_student(&studentB);
    // 设置大家的回复信息
    studentMonitor.set_content("明天下午2点开年级会，收到回复^^。");
    studentTuanZhiShu.set_content("知道了，肯定到!!");
    studentA.set_content("收到了，但是可能晚点到!!");
    studentB.set_content("收到了，但是明天要去面试!!");
    // 开始发通知
    qq.notify(&studentMonitor);
    /* --------------------两个同学私下交流-------------------------- */
    cout << endl << "下面是两个同学的私下交流：" << endl;
    studentMonitor.set_content("你觉得咱们“软件项目管理老师”讲的怎么样？");
    studentA.set_content("我觉得讲的不够生动，还点名，不太好!!!");
    qq.chart(&studentMonitor, &studentA);
    return 0;
}
```

## 三、中介者模式的应用场景与优缺点
### （一）应用场景
1. 当一组对象之间需要进行复杂的通信时，例如在一个多人在线游戏中，玩家之间、玩家与游戏系统之间的交互非常复杂，使用中介者模式可以将这些交互封装在中介者对象中，使游戏对象之间的耦合降低，便于管理和维护。（配图：展示多人在线游戏中玩家与各种游戏系统组件通过中介者交互的示意图）
2. 当需要定制一个分布在多个类中的行为，而又不想生成太多的子类时。比如在一个企业级应用中，多个部门的业务逻辑相互关联，通过中介者模式可以在不创建大量子类的情况下协调这些部门之间的行为。

### （二）优点
1. 降低系统对象之间的耦合性，使得对象易于独立复用。由于对象之间不再直接相互引用，而是通过中介者进行通信，当某个对象需要改变时，对其他对象的影响较小，提高了系统的可维护性。例如，在上述班级场景中，如果要修改班长通知的方式，只需在中介者（QQMediator）中进行调整，而不会影响到其他同学类。
2. 提高系统的灵活性，易于扩展。如在代码中，如果要添加新的通讯平台（如飞信），只需创建一个继承自抽象中介者的飞信中介者类即可；如果要增加新同学，创建一个继承自抽象同事类的新同学类就行，方便了系统的扩展。

### （三）缺点
中介者模式的缺点是中介对象承担了较多责任。一旦中介对象出现问题，整个系统都会受到重大影响。因为所有对象之间的交互都依赖于中介者，如果中介者出现故障或设计不合理，可能导致整个系统无法正常工作或性能下降。例如，如果QQ群（中介者）出现故障，班级同学之间的交流就会受到阻碍。

### （四）中介者模式的使用建议
1. **合理设计中介者接口**
   - 在设计抽象中介者接口时，要充分考虑系统中可能的交互场景，确保接口方法的完整性和通用性。例如，在上述班级通讯的例子中，`notify`方法用于向所有同事广播消息，`chart`方法用于特定同事之间的交流，这些方法覆盖了常见的通讯需求。如果后续可能出现新的交互方式，如群发消息给部分同学，就需要提前规划接口，以便在不修改现有代码的基础上进行扩展。
2. **控制中介者复杂度**
   - 虽然中介者模式可以降低对象之间的耦合，但如果中介者过于复杂，会影响系统的可维护性。因此，在实现具体中介者时，要避免在其中添加过多与业务逻辑无关的代码。可以将一些复杂的计算或处理逻辑提取到其他辅助类中，使中介者专注于协调对象之间的交互。例如，如果在`QQMediator`中需要对消息进行加密处理，可以创建一个专门的加密类，在`notify`或`chart`方法中调用加密类的方法来处理消息，而不是在中介者类中直接实现加密逻辑。
3. **权衡对象职责分配**
   - 确定哪些职责应该放在中介者中，哪些应该留在同事类中是很关键的。一般来说，与对象之间交互协调相关的职责交给中介者，而对象自身的业务逻辑和属性操作留在同事类。例如，同学类（同事类）负责设置自己的姓名和发言内容，而中介者负责将这些发言内容按照合适的方式传递给其他同学。这样可以保持每个类的职责单一，遵循单一职责原则，提高系统的可扩展性和可维护性。

### （五）与其他模式的对比
1. **与观察者模式的对比**
   - 观察者模式中，多个观察者对象关注一个被观察对象的状态变化，当被观察对象状态改变时，会通知所有观察者。而中介者模式中，中介者协调多个同事对象之间的交互，同事对象之间并不直接相互观察。例如，在一个股票价格监控系统中，如果使用观察者模式，多个投资者（观察者）会关注股票价格（被观察对象）的变化；而如果使用中介者模式，可能会有一个中介者对象（如股票交易平台）协调投资者之间的交易行为（同事对象之间的交互），以及与股票市场（外部系统）的交互。
   - 观察者模式强调的是对象之间的一对多依赖关系，侧重于状态变化的通知；中介者模式强调的是对象之间的多对多交互关系，侧重于协调交互过程。
2. **与外观模式的对比**
   - 外观模式为子系统中的一组接口提供一个一致的界面，隐藏了子系统的复杂性，客户端只与外观类交互。中介者模式则是协调多个对象之间的交互，这些对象之间的交互关系相对复杂且平等。例如，在一个计算机硬件系统中，计算机启动过程涉及多个硬件组件（如CPU、内存、硬盘等）的初始化和交互，外观模式可以提供一个简单的启动接口，隐藏这些硬件组件初始化的复杂过程；而在一个多人协作的项目管理系统中，不同角色的人员（如项目经理、开发人员、测试人员等）之间需要频繁交互，中介者模式可以协调他们之间的沟通和协作，确保项目顺利进行。
   - 外观模式主要是简化外部对系统的访问，中介者模式主要是解决系统内部对象之间的交互问题。

### （六）总结
中介者模式在处理多对象之间复杂交互场景中具有重要作用。通过引入中介者对象，有效地降低了对象之间的耦合度，提高了系统的灵活性和可维护性。在实际应用中，需要根据具体的业务需求和系统架构合理选择使用中介者模式，并注意其优缺点，遵循相关的设计原则来优化中介者的设计。同时，要清晰地理解中介者模式与其他相关设计模式的区别，以便在合适的场景中选择最合适的模式来解决问题，构建高效、可扩展和易于维护的软件系统。无论是在社交网络、企业应用还是游戏开发等领域，中介者模式都能为处理复杂的对象交互提供一种有效的解决方案，帮助开发者更好地组织和管理系统中的对象关系，提升软件的质量和用户体验。