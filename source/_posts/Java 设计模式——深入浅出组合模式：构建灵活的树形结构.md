---
title: Java 设计模式——深入浅出组合模式：构建灵活的树形结构
id: 40ebad7e-d8ee-4b1f-a08f-86732d261f01
date: 2024-12-10 11:19:49
author: daichangya
cover: https://images.jsdiff.com/design03.jpg
excerpt: "在软件开发的世界里，设计模式犹如一把把钥匙，帮助我们打开高效、灵活代码架构的大门。今天，我们要深入探讨的是组合模式，它为处理树形结构数据提供了一种巧妙而强大的解决方案。 一、组合模式：概念与核心价值 （一）定义 组合模式，顾名思义，就是将对象组合成树形结构，以此来清晰地表示“部分 - 整体”的层次关"
permalink: /archives/java-she-ji-mo-shi----shen-ru-qian-chu-zu-he-mo-shi/
categories:
 - 设计模式
---

在软件开发的世界里，设计模式犹如一把把钥匙，帮助我们打开高效、灵活代码架构的大门。今天，我们要深入探讨的是组合模式，它为处理树形结构数据提供了一种巧妙而强大的解决方案。

## 一、组合模式：概念与核心价值
### （一）定义
组合模式，顾名思义，就是将对象组合成树形结构，以此来清晰地表示“部分 - 整体”的层次关系。这意味着，无论是单个的对象，还是由多个对象组合而成的复杂对象，在使用方式上对用户来说都是一致的，大大简化了代码的复杂性，提高了代码的可维护性和可扩展性。

### （二）解决的痛点
在许多实际场景中，我们常常需要处理具有层次结构的数据，例如公司的组织结构、文件系统的目录结构等。组合模式的出现，完美解决了如何统一对待整体和部分的问题，使得我们在操作这些结构时无需区分是单个元素还是组合元素，从而降低了代码的理解和维护成本。

### （三）模式结构剖析
1. **Component（组件）抽象类**
这是组合模式中的核心抽象类，它声明了组合对象和叶子对象共有的接口方法，为整个组合结构提供了统一的操作规范。
```java
public abstract class Component {
    protected String name;

    public Component(String name) {
        this.name = name;
    }

    // 添加子组件方法
    public abstract void Add(Component c);

    // 删除子组件方法
    public abstract void Remove(Component c);

    // 显示组件信息方法
    public abstract void Display(int depth);
}
```
2. **Leaf（叶子节点）类**
叶子节点是组合结构中的最底层对象，它没有子节点。虽然叶子节点实现了Component接口，但由于其自身特性，添加和删除子节点的操作对它来说没有实际意义，通常会在这些方法中给出相应提示。
<separator></separator>
```java
public class Leaf extends Component {
    public Leaf(String name) {
        super(name);
    }

    @Override
    public void Add(Component c) {
        System.out.println("不能向叶子节点添加子节点");
    }

    @Override
    public void Remove(Component c) {
        System.out.println("叶子节点没有子节点");
    }

    @Override
    public void Display(int depth) {
        System.out.println(new String('-', depth) + name);
    }
}
```
3. **Composite（组合节点）类**
组合节点可以包含子节点，它实现了Component接口中的方法，用于管理子节点的添加、删除和显示操作。在内部，它通常使用一个集合来存储子节点，以便进行统一管理。
```java
import java.util.ArrayList;
import java.util.List;

public class Composite extends Component {
    private List<Component> children;

    public Composite(String name) {
        super(name);
        children = new ArrayList<>();
    }

    @Override
    public void Add(Component c) {
        children.add(c);
    }

    @Override
    public void Remove(Component c) {
        children.remove(c);
    }

    @Override
    public void Display(int depth) {
        System.out.println(new String('-', depth) + name);
        for (Component component : children) {
            component.Display(depth + 2);
        }
    }
}
```

### （四）示例代码展示
以下是一个简单的示例，展示了如何使用组合模式构建一个简单的树形结构并进行操作：
```java
public class Main {
    public static void main(String[] args) {
        // 创建根节点
        Composite root = new Composite("根节点root");

        // 添加叶子节点到根节点
        root.Add(new Leaf("根上生出的叶子A"));
        root.Add(new Leaf("根上生出的叶子B"));

        // 创建组合节点并添加叶子节点
        Composite comp = new Composite("根上生出的分支CompositeX");
        comp.Add(new Leaf("分支CompositeX生出的叶子LeafXA"));
        comp.Add(new Leaf("分支CompositeX生出的叶子LeafXB"));

        // 将组合节点添加到根节点
        root.Add(comp);

        // 创建更深层次的组合节点并添加叶子节点
        Composite comp2 = new Composite("分支CompositeX生出的分支CompositeXY");
        comp2.Add(new Leaf("分支CompositeXY生出叶子LeafXYA"));
        comp2.Add(new Leaf("分支CompositeXY生出叶子LeafXYB"));

        // 将更深层次的组合节点添加到上一级组合节点
        comp.Add(comp2);

        // 再次添加叶子节点到根节点
        root.Add(new Leaf("根节点生成的叶子LeafC"));

        // 创建一个叶子节点用于测试删除操作
        Leaf leafD = new Leaf("leaf D");
        root.Add(leafD);

        // 删除叶子节点
        root.Remove(leafD);

        // 显示整个树形结构
        root.Display(1);
    }
}
```

### （五）运行结果解析
当运行上述代码时，控制台将输出以下结果：
```
-根节点root
  -根上生出的叶子A
  -根上生出的叶子B
  -根上生出的分支CompositeX
    -分支CompositeX生出的叶子LeafXA
    -分支CompositeX生出的叶子LeafXB
    -分支CompositeX生出的分支CompositeXY
      -分支CompositeXY生出叶子LeafXYA
      -分支CompositeXY生出叶子LeafXYB
  -根节点生成的叶子LeafC
```
从结果可以清晰地看到，我们成功构建了一个树形结构，并且通过统一的操作方式（添加、删除和显示）对其进行了处理，无论是叶子节点还是组合节点，都按照预期的方式进行了展示。

## 二、组合模式实战：公司组织结构案例
### （一）场景设定
假设我们正在构建一个公司组织结构管理系统，公司的结构如下：
- 总经理
  - 技术部门经理
    - 开发人员A
    - 开发人员B
  - 销售部门经理（目前暂时没有直接下属员工，但随着公司发展可能会新增销售员工）

我们的目标是计算整个组织结构的总工资状况。

### （二）代码实现
1. **IComponent接口**
这个接口定义了公司组织架构中每个角色共有的属性和方法，包括职称、工资待遇以及添加员工到组织团队的方法和计算工资成本的方法。
```java
public interface IComponent {
    String getTitle();
    void setTitle(String title);
    double getSalary();
    void setSalary(double salary);
    void Add(IComponent c);
    void GetCost(ref double salary);
}
```
2. **Component叶子节点类**
叶子节点代表公司中的基层员工，他们没有下属员工，因此添加员工的方法没有实际意义。在计算工资成本时，只需将自身工资累加到总工资中。
```java
public class Component implements IComponent {
    private String title;
    private double salary;

    public Component(String title, double salary) {
        this.title = title;
        this.salary = salary;
    }

    @Override
    public String getTitle() {
        return title;
    }

    @Override
    public void setTitle(String title) {
        this.title = title;
    }

    @Override
    public double getSalary() {
        return salary;
    }

    @Override
    public void setSalary(double salary) {
        this.salary = salary;
    }

    @Override
    public void Add(IComponent c) {
        System.out.println("Cannot add to the leaf!");
    }

    @Override
    public void GetCost(ref double salary) {
        salary += this.salary;
    }
}
```
3. **Composite组合类**
组合类用于表示公司中的经理级别角色，他们可以有下属员工。在内部，使用一个列表来存储下属员工，并实现了添加员工、计算工资成本的方法。计算工资成本时，不仅要加上自身工资，还要递归计算下属员工的工资总和。
```java
import java.util.ArrayList;
import java.util.List;

public class Composite implements IComponent {
    private String title;
    private double salary;
    private List<IComponent> _listEmployees;

    public Composite(String title, double salary) {
        this.title = title;
        this.salary = salary;
        _listEmployees = new ArrayList<>();
    }

    @Override
    public String getTitle() {
        return title;
    }

    @Override
    public void setTitle(String title) {
        this.title = title;
    }

    @Override
    public double getSalary() {
        return salary;
    }

    @Override
    public void setSalary(double salary) {
        this.salary = salary;
    }

    @Override
    public void Add(IComponent comp) {
        _listEmployees.add(comp);
    }

    @Override
    public void GetCost(ref double salary) {
        salary += this.salary;
        for (IComponent component : _listEmployees) {
            component.GetCost(ref salary);
        }
    }
}
```
4. **客户端代码**
在客户端代码中，我们创建了公司的组织结构，并计算了总经理级别和技术部门经理级别的工资成本。
```java
public class Main {
    public static void main(String[] args) {
        double costCEO = 0.0;
        double costVPD = 0.0;

        // 创建总经理节点
        IComponent compCEO = new Composite("CEO", 500000);

        // 创建技术部门经理和开发人员节点
        IComponent compVPDev = new Composite("VP-Development", 250000);
        IComponent compDev1 = new Component("Developer1", 75000);
        IComponent compDev2 = new Component("Developer2", 50000);
        compVPDev.Add(compDev1);
        compVPDev.Add(compDev2);

        // 创建销售部门经理节点（暂时没有下属）
        IComponent compVPSales = new Component("VP-Sales", 300000);

        // 将技术部门经理和销售部门经理添加到总经理下属
        compCEO.Add(compVPDev);
        compCEO.Add(compVPSales);

        // 计算总经理级别的工资成本
        compCEO.GetCost(ref costCEO);
        System.out.println(String.format("The Cost incurred at the CEO level is %.2f ", costCEO));

        // 计算技术部门经理级别的工资成本
        compVPDev.GetCost(ref costVPD);
        System.out.println(String.format("The Cost incurred at the VP-Development level is %.2f ", costVPD));
    }
}
```

### （三）结果分析
运行上述客户端代码，我们将得到以下结果：
```
The Cost incurred at the CEO level is 975000.00 
The Cost incurred at the VP-Development level is 375000.00 
```
这表明我们成功地使用组合模式构建了公司组织结构，并准确计算了不同层级的工资成本。通过组合模式，我们可以轻松地扩展组织结构，例如为销售部门经理添加下属员工，而无需对现有代码进行大规模修改。

## 三、总结与展望
组合模式作为一种强大的设计模式，为处理树形结构数据提供了优雅而高效的解决方案。它通过统一整体和部分的操作方式，简化了复杂结构的处理，提高了代码的灵活性和可维护性。无论是在构建公司组织结构、文件系统，还是其他具有层次结构的场景中，组合模式都能发挥重要作用。

在未来的软件开发中，随着系统复杂度的不断提高，设计模式的应用将更加广泛。希望通过本文的介绍，你能深入理解组合模式的精髓，并将其应用到实际项目中，为打造高质量的软件系统贡献力量。同时，也期待你继续探索其他设计模式，解锁更多编程技巧，提升自己的技术水平。

你对组合模式有什么疑问或者见解吗？欢迎在评论区留言分享！让我们一起在编程的世界里不断进步。