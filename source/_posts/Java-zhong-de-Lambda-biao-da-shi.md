---
title: Java中的Lambda表达式
id: 1431
date: 2024-10-31 22:01:55
author: daichangya
excerpt: Java中的Lambda表达式介绍Lambda函数是Java8附带的一项功能，它是该语言向函数式编程迈出的第一步，这是实现各种兼容范例的有用功能的普遍趋势。引入lambda函数的动机主要是为了减少传递给类实例以模拟其他语言的匿名函数的繁琐的重复代码。这是一个例子：String[]arr={&quot
permalink: /archives/Java-zhong-de-Lambda-biao-da-shi/
---

## Java中的Lambda表达式

### 介绍

Lambda函数是[Java 8](https://www.oracle.com/technetwork/java/javase/overview/java8-2100321.html)附带的一项功能，它是该语言向[函数式编程](https://en.wikipedia.org/wiki/Functional_programming)迈出的第一步，这是实现各种兼容[范例的](https://en.wikipedia.org/wiki/Programming_paradigm)有用功能的普遍趋势。

引入lambda函数的动机主要是为了减少传递给类实例以模拟其他语言的匿名函数的繁琐的重复代码。

这是一个例子：

```java
String[] arr = { "family", "illegibly", "acquired", "know", "perplexing", "do", "not", "doctors", "where", "handwriting", "I" };

Arrays.sort(arr, new Comparator<String>() {
    @Override public int compare(String s1, String s2) {
        return s1.length() - s2.length();
    }
});

System.out.println(Arrays.toString(arr));

```

如您所见，实例化一个新的Comparator类并覆盖其内容的全部内容是一小段重复的代码，我们也可以不这样做，因为它始终是相同的。

`Arrays.sort()`可以用更短更甜的方法代替整个方法，但是在功能上是等效的：

```java
Arrays.sort(arr, (s1,s2) -> s1.length() - s2.length());

```

这些简短而甜美的代码与冗长的对应代码起到相同的作用，称为[语法糖](https://en.wikipedia.org/wiki/Syntactic_sugar)。这是因为他们没有在语言中添加功能，而是使其更加紧凑和易读。Lambda函数是Java语法糖的一个示例。

尽管我强烈建议您按顺序阅读本文，但是，如果您不熟悉该主题，那么以下是我们将要涵盖的内容的快速列表，以便于参考：

*   [Lambda作为对象](#Lambda作为对象)
    *   [单方法接口匹配](#单方法接口匹配)
*   [Implementation](#implementation)
    *   [Parameters](#parameters)
    *   [Body](#body)
    *   [变量获取](#变量获取)
    *   [方法引用](#方法引用)
        *   [静态方法参考](#静态方法参考)
        *   [参数方法参考](#参数方法参考)
        *   [实例方法参考](#实例方法参考)
        *   [构造方法参考](#构造方法参考)

### Lambda作为对象

在了解lambda语法本身的本质之前，我们应该先看看*什么是* lambda函数以及*如何使用它们*。

如前所述，它们只是语法糖，但是它们是专门针对实现单个方法接口的对象的语法糖。

在这些对象中，lambda实现被视为所述方法的实现。如果lambda和接口匹配，则可以将lambda函数分配给该接口类型的变量。

#### 单方法接口匹配

为了使lambda与单个方法接口（也称为“功能接口”）匹配，需要满足几个条件：

*   功能接口必须仅具有一个未实现的方法，并且该方法（自然）必须是抽象的。接口中可以包含实现的静态方法和默认方法，但重要的是，只有一种抽象方法。
*   abstract方法必须以相同的顺序接受与lambda接受的参数相对应的参数。
*   方法和lambda函数的返回类型必须匹配。

如果满足所有条件，则已满足所有匹配条件，您可以将lambda分配给变量。

让我们定义我们的接口：

```java
public interface HelloWorld {
    abstract void world();
}

```

如您所见，我们有一个非常无用的功能接口。

它仅包含一个函数，并且该函数可以执行任何操作，只要它不接受任何参数且不返回任何值。

我们将使用此程序制作一个简单的*Hello World*程序，但是如果您想玩它，那么想象力是极限：

```java
public class Main {
    public static void main(String[] args) {
        HelloWorld hello = () -> System.out.println("Hello World!");
        hello.world();
    }
}

```

如我们所见，如果运行此命令，我们的lambda函数已成功匹配该`HelloWorld`接口，并且该对象`hello`现在可以用于访问其方法。

其背后的想法是，您可以在任何其他情况下使用lambda来使用函数接口来传递函数。如果您还记得我们的`Comparator`示例，`Comparator<T>`它实际上是一个功能接口，实现了一个方法\- `compare()`。

这就是为什么我们可以用行为类似于该方法的lambda替换它。

### Implementation

lambda函数背后的基本思想与方法背后的基本思想相同-它们将参数输入并在由表达式组成的主体内使用它们。

实现只是有些不同。让我们以`String`lambda排序为例：

```java
(s1,s2) -> s1.length() - s2.length()

```

其语法可以理解为：

```
parameters -> body

```

#### Parameters

**参数**与函数参数相同，它们是传递给lambda函数以供其执行操作的值。

参数通常用括号括起来，并用逗号分隔，尽管在仅接收一个参数的lambda情况下，可以省略括号。

lambda函数可以接受任意数量的参数，包括零，因此您可能会遇到以下情况：

```java
() -> System.out.println("Hello World!")

```

当与相应接口匹配时，此lambda函数将与以下函数相同：

```java
static void printing(){
    System.out.println("Hello World!");
}

```

同样，我们可以使用带有一个，两个或多个参数的lambda函数。

一个具有一个参数的函数的经典示例正在`forEach`循环中处理集合的每个元素：

```java
public class Main {
    public static void main(String[] args) {
        LinkedList<Integer> childrenAges = new LinkedList<Integer>(Arrays.asList(2, 4, 5, 7));
        childrenAges.forEach( age -> System.out.println("One of the children is " + age + " years old."));
    }
}

```

在这里，唯一的参数是`age`。请注意，我们在此处删除了括号，因为只有一个参数时才允许这样做。

使用更多参数的工作原理类似，它们只是用逗号分隔并括在括号中。当我们将其匹配`Comparator`以对字符串进行排序时，我们已经看到了两参数lambda 。

#### Body

Lambda表达式的主体由单个表达式或语句块组成。

#### 订阅我们的新闻

在收件箱中获取偶尔的教程，指南和作业。从来没有垃圾邮件。随时退订。

电子报注册 

订阅

如果仅将一个表达式指定为lambda函数的主体（无论是在语句块中还是在其自身中），则lambda将自动返回该表达式的求值。

如果语句块中有多行，或者只是想（一个自由的国家/地区），则可以在语句块中显式使用return语句：

```java
// just the expression
(s1,s2) -> s1.length() - s2.length()

// statement block
(s1,s2) -> { s1.length() - s2.length(); }

// using return
(s1,s2) -> {
    s1.length() - s2.length();
    return; // because forEach expects void return
}

```

您可以尝试在本文开头将所有这些替换为我们的排序示例，您会发现它们的工作原理完全相同。

#### 变量获取

变量获取使lambda可以使用在lambda本身之外声明的变量。

有三种非常相似的变量获取类型：

*   局部变量获取
*   实例变量获取
*   静态变量获取

语法几乎与您从任何其他函数访问这些变量的方式相同，但是可以使用的条件不同。

仅当**局部变量***有效地为final时*，您才能访问该**局部变量**，这意味着它在赋值后不会更改其值。不必明确将其声明为final，但建议这样做以避免混淆。如果在lambda函数中使用它，然后更改其值，则编译器将开始发出抱怨。

之所以不能这样做，是因为lambda无法可靠地引用局部变量，因为在执行lambda之前它可能已被销毁。因此，它制作了一个[深层副本](https://en.wikipedia.org/wiki/Object_copying#Deep_copy)。更改局部变量可能会导致一些令人困惑的行为，因为程序员可能希望lambda中的值会发生变化，因此为避免混淆，明确禁止这样做。

关于**实例变量**，如果您的lambda与您要访问的变量在同一类之内，则可以简单地用于`this.field`访问该类中的字段。此外，该字段*不必是final*，可以在程序执行过程中稍后进行更改。

这是因为，如果在类中定义了lambda，则该lambda会与该类一起实例化并绑定到该类实例，因此可以轻松地引用其所需字段的值。

**静态变量**的捕获与实例变量非常相似，不同之处在于您不会使用**静态变量**`this`来引用它们。出于相同的原因，它们可以更改，并且不必是最终的。

#### 方法引用

有时，lambda只是特定方法的替身。本着使语法简短有趣的精神，在这种情况下，您实际上不必键入整个语法。例如：

```java
s -> System.out.println(s)

```

等效于：

```java
System.out::println

```

该`::`语法将使编译器知道您只需要一个将给定参数传递给的lambda `println`。您始终始终在方法名称前加上`::`编写lambda函数的位置，否则将像往常一样访问该方法，这意味着您仍然必须在双冒号之前指定所有者类。

方法引用有多种类型，具体取决于您要调用的方法类型：

*   静态方法参考
*   参数方法参考
*   实例方法参考
*   构造方法参考

##### 静态方法参考

我们需要一个接口：

```java
public interface Average {
    abstract double average(double a, double b);
}

```

静态函数：

```java
public class LambdaFunctions {
    static double averageOfTwo(double a, double b){
        return (a+b)/2;
    }
}

```

然后我们的lambda函数并调用`main`：

```java
Average avg = LambdaFunctions::averageOfTwo;
System.out.println(avg.average(20.3, 4.5));

```

##### 参数方法参考

再次，我们输入`main`。

```java
Comparator<Double> cmp = Double::compareTo;
Double a = 20.3;
System.out.println(cmp.compare(a, 4.5));

```

该`Double::compareTo`lambda相当于：

```java
Comparator<Double> cmp = (a, b) -> a.compareTo(b)

```

##### 实例方法参考

如果我们使用`LambdaFunctions`类和函数`averageOfTwo`（来自“ [静态方法参考”](#staticmethodreference)）并使之成为非静态的，则会得到以下信息：

```java
public class LambdaFunctions {
    double averageOfTwo(double a, double b){
        return (a+b)/2;
    }
}

```

要访问它，我们现在需要一个类的实例，因此我们必须在`main`：

```java
LambdaFunctions lambda = new LambdaFunctions();
Average avg = lambda::averageOfTwo;
System.out.println(avg.average(20.3, 4.5));

```

##### 构造方法参考

如果我们有一个`MyClass`要调用的类并想通过lambda函数调用其构造函数，则我们的lambda将如下所示：

```java
MyClass::new

```

它将接受与构造函数之一匹配的尽可能多的参数。

### 结论

总之，lambda是使我们的代码更简单，更短且更具可读性的有用功能。

当团队中有很多初级人员时，有些人会避免使用它们，因此，我建议您在重构所有代码之前先咨询您的团队，但是当每个人都在同一页面上时，它们是一个很好的工具。

#### 文章参考


*   [Streams](https://stackabuse.com/introduction-to-java-8-streams/)
*   [事件监听器](https://www.dummies.com/programming/java/how-to-use-lambda-expressions-to-handle-events-in-java/)
*   [Oracle上的Lambda表达式](https://docs.oracle.com/javase/tutorial/java/javaOO/lambdaexpressions.html)
