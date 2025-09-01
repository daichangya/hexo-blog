---
title: Java你不知道的那些事儿—Java隐藏特性
id: 980
date: 2024-10-31 22:01:47
author: daichangya
excerpt: 每种语言都很强大，不管你是像我一样的初学者还是有过N年项目经验的大神，总会有你不知道的东西。就其语言本身而言，比如Java，也许你用Java开发
  了好几年，对其可以说是烂熟于心，但你能保证Java所有的用法你都知道吗？今天没事就来整理下Java中有哪些隐藏的特性呢？
permalink: /archives/Java-ni-bu-zhi-dao-de-na-xie-shi-er/
categories:
- java
---

每种语言都很强大，不管你是像我一样的初学者还是有过N年项目经验的大神，总会有你不知道的东西。就其语言本身而言，比如Java，也许你用Java开发 了好几年，对其可以说是烂熟于心，但你能保证Java所有的用法你都知道吗？今天没事就来整理下Java中有哪些隐藏的特性呢？知道的可以举手哦~~~

### 一、双括号初始化语法（ [DoubleBraceInitialization](http://www.c2.com/cgi/wiki?DoubleBraceInitialization)）（这里指的是大括号{}）

 主要指的是集合类（List，Map，Set等），我们创建一个常量集合或传递一个常量集合作为参数，往往都会这么做（以Set为例）：
```
Set<String> validCodes = new HashSet<String>();
 validCodes.add("XZ13s");
 validCodes.add("AB21/X");
 validCodes.add("YYLEX");
 validCodes.add("AR2D");
 removeProductsWithCodeIn(validCodes);
```
//或在类中初始化一个常量集合：
```
private static final Set<String> VALID_CODES = new HashSet<String>();
 static {
    validCodes.add("XZ13s");
    validCodes.add("AB21/X");
    validCodes.add("YYLEX");
    validCodes.add("AR2D");
 }
```
 会不会觉得每次都这样很费时费力，其实，有更好的办法，那就是双括号语法，像下面这样：
```
private static final Set<String> VALID_CODES = new  HashSet<String>() {{
    add("XZ13s");
    add("AB21/X");
    add("YYLEX");
    add("AR2D");
 }};
 
// Or:
 
 removeProductsWithCodeIn(new HashSet<String>() {{
    add("XZ13s");
    add("AB21/X");
    add("YYLEX");
    add("AR5E");
 }});
```
 这里解释下这两个括号：第一个括号创建了一个新的匿名内部类，相信这个大家都知道；第二个括号声明了匿名内部类实例化时运行的实例初始化块。

**使用双括号语法需要注意两点：**

1. 如果要在匿名内部类中要建立匿名子类，那么只能用于非final的类，这很明显，且不仅局限于集合类，可以用来实例化任何对象，例如用于GUI对象，如下：
```
add(new JPanel() {{
    setLayout(...);
    setBorder(...);
    add(new JLabel(...));
    add(new JSpinner(...));
 }});
```
 2, `这种语法与常用的equals(` `Object` `o)方法不兼容。例如Example类有这样的方法：`
```
public boolean equals(final Object o) {
    if (o == null) {
        return false;
    } else if (!getClass().equals(o.getClass())) {
        return false;
    } else {
        Example other = (Example) o;
        // Compare this to other.
    }
  }
```
那么，使用双括号初始化语法创建的任何对象都不会与未使用双括号语法创建的对象相等。因此，建议大家：如果类中需要equals(Object o)方法，那就老老实实不要使用这种语法了。不过集合类没有这种问题，应该是因为集合内部优化了的原因。

_那么什么时候建议大家使用双括号语法呢？_

如果你只是要创建并初始化一个实例而不是创建一个新类，或者创建任何不添加字段属性或重载方法的匿名类时，用双括号语法就很nice了。

3. 如果你用的是集合类且该类有构造器参数接受另一个集合生成该集合的实例，那么有个更好的更惯用的替代方法，如大家都知道的List初始化可以用Arrays.asList()，如下：
```
List<String> myList = new ArrayList<String>(Arrays.asList("One", "Two", "Three"));
```
 但需要注意：

asList返回的是一个长度不可变的列表。数组是多长，转换成的列表是多长，我们是无法通过add、remove来增加或者减少其长度的。

### 二、类型参数的与操作&（ [TypeParameterJointUnion](https://www.reddit.com/r/programming/comments/1fr8fv/little_known_java_feature_joint_union_in_type/)）

就是参数绑定多个类型，如：
```
public class ClassName<T extends Class & Interface1 & Interface2 & ...> {}
```
_注意：这里extends后面只有第一个为类Class，后面&的全部都是接口Interface，而且类Class的声明或定义必须在Interface之前。_

举个例子：如果你想要一个既是 Comparable类又是Collection类的参数，实现的功能是：两个给定的集合是否相等或两个集合中的任一个是否包含指定的元素，那么你可以用下面的函数实现：
```
public static <A, B extends Collection<A> & Comparable<B>> boolean foo(B b1, B b2, A a) {
    return (b1.compareTo(b2) == 0) || b1.contains(a) || b2.contains(a);
}
```
 这里b1和b2可以同时具有类型Collection和Comparable类型，因此可以使用Collection类的contains方法也可以使用Comparable类的compareTo方法。

### 三、VisualVM监控工具（ [Java VisualVM](http://visualvm.java.net/)）

这是JDK6.0 update 7 中自带的监控工具(java启动时不需要特定参数，该工具在bin/jvisualvm.exe)，能够监控线程，内存情况，查看方法的CPU时间和内存 中的对象，已被GC的对象，反向查看分配的堆栈(如100个String对象分别由哪几个对象分配出来的)。

双击打开，从UI上来看，这个软件是基于NetBeans开发的了。

![](http://cdn1.importnew.com/2013/12/VisualVM1.png)

从界面上看还是比较简洁的，左边是树形结构，自动显示当前本机所运行的Java程序，还可以添加远程的Java VM，其中括号里面的PID指的是进程ID。OverView界面显示VM启动参数以及该VM对应的一些属性。Monitor界面则是监控Java堆大 小，Permgen大小，Classes和线程数量。Profiler界面比较有趣，看样子似乎可以动态的对某个Java程序进行调优了。不过我没试用这 个功能，感觉要调优还是在Netbeans里面比较自然一点，起码有代码，没代码调优了用处也不大。

### 四、Classpath支持通配符（ [Setting the class path](https://docs.oracle.com/javase/6/docs/technotes/tools/windows/classpath.html)）

这是Java 6开始支持的功能，比如在工程中经常会有这样的配置：
```
java -classpath ./lib/log4j.jar:./lib/commons-codec.jar:./lib/commons-httpclient.jar:./lib/commons-collections.jar:./lib/myApp.jar so.Main
```
 比较复杂，还容易出错，其实可以用通配符更加简洁方便：

java -classpath ./lib/\* so.Main

 

### 五、协变返回类型（  [covariant return types](http://www.java-tips.org/java-se-tips/java.lang/covariant-return-types.html)）

这是Java 5添加的功能，在Java5之前我们在子类中覆盖基类的方法时是不能改变被覆盖方法的返回类型的，就是基类和父类的方法必须一模一样，想要改变只能在创建 对象时Cast。Java 5过后，我们就可以改变了，不过需要注意的是：改变后的类型必须是原类型的子类型。举个例子就一目了然了。
```
public class CovariantReturnTypesTest {
 
    public static void main(String\[\] args) {
        // TODO Auto-generated method stub
 
        Mill m = new Mill();
        Grain g = m.process();
        System.out.println(g);  // output: Grain
        m = new WheatMill();
        g = m.process();
        System.out.println(g); // output: Wheat
    }
 
}
 
class Grain {
    public String toString() {
        return "Grain";
    }
}
 
class Wheat extends Grain {
    public String toString() {
        return "Wheat";
    }
}
 
class Mill {
    Grain process() {
        return new Grain();
    }
}
 
class WheatMill extends Mill {
    // 这里返回类型改为了Grain的子类型Wheat
    Wheat process() {
        return new Wheat();
    }
}
```
  