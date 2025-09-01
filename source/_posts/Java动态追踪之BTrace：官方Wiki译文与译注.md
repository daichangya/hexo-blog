---
title: Java动态追踪之BTrace：官方Wiki译文与译注
id: 1437
date: 2024-10-31 22:01:55
author: daichangya
excerpt: "Btrace用于Java的安全的动态追踪工具。BTrace通过动态地调改正在运行的Java程序的字节码来工作。其在运行的Java类上hotswap，来插入追踪动作。"
permalink: /archives/java%E5%8A%A8%E6%80%81%E8%BF%BD%E8%B8%AA%E4%B9%8Bbtrace%E5%AE%98%E6%96%B9wiki%E8%AF%91%E6%96%87%E4%B8%8E%E8%AF%91%E6%B3%A8/
tags: 
 - btrace
---



本文翻译自 [https://github.com/btraceio/btrace/wiki](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fbtraceio%2Fbtrace%2Fwiki)

* * *

## 首页

### Btrace

用于Java的安全的动态追踪工具。BTrace通过动态地调改正在运行的Java程序的字节码来工作。其在运行的Java类上hotswap，来插入追踪动作。

### 快速开始

键入 `btrace <PID> AllMethods.java` ，其中`PID`可以是任何正在运行的目标Java程序。  
这个样本脚本[trace script](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fbtraceio%2Fbtrace%2Fwiki%2FTrace-Scripts)（*AllMethods.java*）会埋点所有 javax.swing.*下的类的所有方法。而埋点将会在每个被埋点的方法进入时打印类名和方法名。  
（译注：instrument不是很好翻译，经过检索相关资料，在这篇文章的上下文中，我认为将instrument翻译为了“埋点”更好理解。这个词的其他近似的含义有，插桩、调改、调控、监测等）

所有的输出会打印到标准输出（stdout）

当脚本运行期间，你可以键入Ctrl-C来停止Btrace工具运行。

*片段1 - AllMethods.java*

```  language-dart
package samples;

import com.sun.btrace.annotations.*;
import static com.sun.btrace.BTraceUtils.*;

/**
 * 这个脚本会追踪每个javax.swing 包下的方法进入
 * 使用前三思，这个操作会显著地减慢你的程序的运行 
 */
@BTrace public class AllMethods {
    @OnMethod(
        clazz="/javax\\.swing\\..*/",
        method="/.*/"
    )
    public static void m(@ProbeClassName String probeClass, @ProbeMethodName String probeMethod) {
        print(Strings.strcat("entered ", probeClass));
        println(Strings.strcat(".", probeMethod));
    }
}

```

### 运行BTrace的细节

#### 动态依附应用程序

对于快速依附于一个已经运行的程序、获取感兴趣的数据、再取消依附、删掉追踪的代码很有用。  
依附的命令行是：  
`btrace [-p <port>] [-cp <classpath>] <pid> <btrace-script> [<args>]`

*   **port** 是BTrace 代理监听的接口，这是一个可选参数。
*   **classpath** 是目录、jar文件的集合。用来在BTrace执行编译过程中找到这些要编译或链入的文件。默认是"."。
*   **btrace-script** 是我们的追踪脚本。如果它是一个".java"文件，那么在它被提交前会被编译。否则这个参数就应该指明一个已经编译好的".class"文件，其会被直接提交。

运行`btrace -h`会打印命令用法。

#### 同时运行应用程序和BTrace

在这个模式下，BTrace的运行甚至要早于应用程序的初始代码运行。这给我们机会去跟踪应用程序生命周期中最早期的运行情况。

运行应用程序的同时开启BTrace代理的命令是：  
`java -javaagent:btrace-agent.jar=[<agent-arg>[,<agent-arg>]*]? <launch-args>`  
这个代理接受逗号分隔的参数列表。

*   **noServer** \- 不启动socket server
*   **bootClassPath** -（译注：bootstrap classloader加载java.*或javax.*下的类时用的路径）
*   **systemClassPath** \- （译注：system classloader 加载类时用到的寻找路径）
*   **debug** \- 开关：verbose调试信息（true/false）
*   **trusted** \- 开关：不检查是否违反了btace的限制（true/false）
*   **dumpClasses** \- 开关：dump转换后的字节码到文件中（true/false）
*   **dumpDir** \- 标明转换后的class文件要dump到哪个目录中
*   **stdout** \- 开关：重定向btrace的输出到标准输出，而不是写入一个任意文件（true/false）
*   **probeDescPath** \- 寻找探针描述符XML的路径
*   **startupRetransform** \- 开关：在attach时将所有已经加载的经过转换的类转换回去（true/false）
*   **scriptdir** \- 在agent开启时寻找脚本的路径
*   **scriptOutputFile** \- 存有btrace的输出的文件路径
*   **script** \- 在代理开始后要运行的脚本的列表，其用冒号分隔

要运行的脚本必须提前已经用[btracec](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fbtraceio%2Fbtrace%2Fwiki%2Fbtracec)编译成字节码（*.class* 文件）

* * *

## 适应性埋点

### 适应性埋点

BTrace支持用埋点等级来做到适应性埋点。每个探针可以通过注解标记其最小生效等级。这样一些轻量级埋点可以总被设置成0级，而一些运行代价较大的埋点可以考虑设置成100以上。

埋点等级在运行期间是可以调整的，它甚至可以在一个探针的handler里进行调整，这样就可以让一些我们期待的特定触发点去动态地升高或降低埋点等级。

#### 声明探针的生效埋点等级

每个探针的埋点等级可以通过`@Level`注解来定义。这个注解接受诸如 \[=,>,<,<=,>=\]的字符串来声明他们等级

```  language-java
// 下面的探针将会在过滤的埋点等级至少为100时才会激活
@Level("100") // @Level(">=100")的效果是同样的
// 也可以根据需求设置成诸如 @Level("<100") @Level(">100") @Level("<=100") @Level("=100")
@OnMethod(...)
public void handler() {
   ...
}

```

#### 调整埋点等级

探针的埋点等级可以通过调用 `BTraceUtils.setInstrumentationLevel(level)`来设置。而`BTraceUtils.getInstrumentationLevel()`则可以获取当前的埋点等级。

#### 性能效益

停用探针的handler只会造成整型比较和指令跳转的额外性能代价，而这些相对于整个探针handler的工作造成的性能代价是微不足道的。 开、关埋点等级，二者间的性能差异也就在微秒之间。

* * *

## BTrace 注解

### BTrace 注解

#### 方法注解

##### @OnMethod

> 用于标明在目标类、目标方法、目标方法的埋点位置。  
> `@OnMethod(clazz=<cname_spec>[, method=<mname_spec>]? [, type=<signature>]? [, location=<location_spec>]?)`

*   **cname_spec**\* = <class\_name> | +<class\_name> | /regex/
*   **class_name** 是类全名
*   **+class_name** 是一个 \+ 号再加上类/接口全名，意味着目标类/接口的所有子类或实现类
*   **/regex/** 是能标明目标类名字的标准正则表达式
*   **mname_spec** = <method_name> | /regex/
*   **method_name** 是简单方法名（没有函数签名或返回类型）
*   **signature** = <return\_type> ((arg\_type(,arg_type)*)?
*   **return_type** 是方法的返回类型（例如：`void`，`java.lang.String`）
*   **arg_type** 是参数类型

被注解标注的action 将会在匹配的方法运行到指定的位置时而触发。在OnMethod 注解中，被追踪的类用"clazz"、被追踪的方法用"method"属性标明。"clazz"可以是类全名（就像java.awt.Component或者是一个用左右两个斜杠括住的正则表达式。可以参看这两个例子 [NewComponent.java](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fjbachorik%2Fbtrace%2Fblob%2Fmaster%2Fsamples%2FNewComponent.java) 和 [Classload.java](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fjbachorik%2Fbtrace%2Fblob%2Fmaster%2Fsamples%2FClassload.java).）

正则表达式可以匹配零到多个类，这些类都会被埋点。例如`/java\.awt\..+/` 匹配 java.awt 包下的所有类。并且，方法名同理也可以用正则表达式来标明。例如 [MultiClass.java](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fjbachorik%2Fbtrace%2Fblob%2Fmaster%2Fsamples%2FMultiClass.java)。

还有一种方式可以抽象地标明被追踪的类或方法。被追踪的类和方法名可以被注解来标识。举个例子，如果 "clazz" 属性设置为 @javax.jws.WebService。BTrace会给所有被添加了WebService注解的类埋点。类似地，目标程序里方法上的注解也可以被用来抽象地标明让BTrace埋点哪个方法。例如 [WebServiceTracker.java](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fjbachorik%2Fbtrace%2Fblob%2Fmaster%2Fsamples%2FWebServiceTracker.java)。

使用正则表达式来标明注解也是可以的，例如 `@/com\.acme\..+/`匹配了所有匹配指定正则表达式的注解所标注了的类。

还可以通过指定超类（译注：基类）的方式来指明要匹配该超类的所有子类。 例如 +java.lang.Runnable 匹配了所有实现了 java.lang.Runnable接口的类型。 参考例子[SubtypeTracer.java](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fjbachorik%2Fbtrace%2Fblob%2Fmaster%2Fsamples%2FSubTypeTracer.java)。

##### @OnTimer

> 用来标明追踪action必须每隔N毫秒周期性地执行

`@OnTimer([[value=]?<value>]?)`

*   **value** 指定的时间周期  
    时间周期通过注解的"value"属性指定。参考例子[Histogram.java](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fbtraceio%2Fbtrace%2Fblob%2Fmaster%2Fsamples%2FHistogram.java)

##### @OnError

> 用来标明如果其他探针的追踪action抛出了异常，所要做的动作  
> 当任何相同BTrace Class中的其他BTrace action产生了异常，该注解标注的方法会被执行。

##### @OnExit

> 用来标注当BTrace代码执行了内建函数`exit(int)`去关闭BTrace会话时要执行的动作。参考例子 [ProbeExit.java](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fjbachorik%2Fbtrace%2Fblob%2Fmaster%2Fsamples%2FProbeExit.java)。

##### @OnEvent

> 用来关联追踪方法与BTrace客户端发送的外部事件。  
> `@OnEvent([[value=]?<event_name>]?)`

*   **event_name** 是这个handler要相应的event名字。

当BTrace客户端发送了一个事件，被该注解标注的BTrace方法会被执行。客户端发送的事件可以是用户的请求的某种形式（比如 Ctrl-C 或者 GUI 菜单）。字符串值可以被用来作为事件的名字。这样，无论这些“事件”什么时候被用户触发，这些特定的action都会执行。

现在，只要用户按下了 Ctrl-C（SIGINT），BTrace的命令行客户端就可以发送事件。按下Ctrl-C后，一个命令行菜单会显示出来。你可以选择发送事件或者退出。[HistoOnEvent.java](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fjbachorik%2Fbtrace%2Fblob%2Fmaster%2Fsamples%2FHistoOnEvent.java)

##### @OnLowMemory

> 用来追踪内存使用已超出限定值的事件  
> 可以参考例子[MemAlerter.java](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fjbachorik%2Fbtrace%2Fblob%2Fmaster%2Fsamples%2FMemAlerter.java)

##### @OnProbe

> 用来标注无需使用BTrace脚本里定义的target（译注：存疑原文"used to specify to avoid using implementation internal classes in BTrace scripts"）  
> `@OnProbe(namespace=<namespace_name>, name=<probe_name>)`

*   **namespace_name** 是一个任意的Java包的命名空间
*   **probe_name** 是一个任意的探针名字

@OnProbe 探针声明会映射到一个或多个BTrace代理声明的@OnMethod。现在这个声明可以使用一个XML探针描述符来指定某个探针名（这个XML文件会被BTrace代理访问）。可以参考例子 [SocketTracker1.java](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fjbachorik%2Fbtrace%2Fblob%2Fmaster%2Fsamples%2FSocketTracker1.java)和其使用的XML探针描述文件[java.net.socket.xml](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fjbachorik%2Fbtrace%2Fblob%2Fmaster%2Fsamples%2Fjava.net.socket.xml)。

（译注：这里的含义其实就是，在BTrace脚本里声明探针位置的方式一般是使用@OnMethod注解指定啥的。但是还有一种方式是不使用@OnMethod指定，而是额外写一个XML文件来间接地定义探针位置，里面可以定义一些探针标签，并且每个探针标签下可以再通过@OnMethod指定具体的位置。这样BTrace脚本里直接使用@OnProbe注解指定XML里面声明的探针名字就好了，可以对比下 [SocketTracker.java](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fbtraceio%2Fbtrace%2Fblob%2Fmaster%2Fsamples%2FSocketTracker.java)（使用@OnMethod指定位置）和 [SocketTracker1.java](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fbtraceio%2Fbtrace%2Fblob%2Fmaster%2Fsamples%2FSocketTracker1.java)（使用XML声明探针，脚本里使用XML定义的探针）这个两个文件就懂了 ）。

当运行这个例子时，这个XML文件需要放置在目标JVM运行的目录里（或者在btracer.bat里去修改probeDescPath选项，去指明.xml文件的位置）

##### @Sampled

> 为被注解了的handler开启[sampling](https://links.jianshu.com/go?to=http%3A%2F%2Fjbachorik.github.io%2Fbtrace%2F2015%2F02%2Fsampled-profiling)。与@OnMethod注解一起连用。  
> `@Sampled([kind=<sampler_kind>[,mean=<number>])`

*   **<sampler_kind>** 只能是Sampler.Const, Sampler.Adaptive 和 Sampler.None 中的一个。

#### 参数注解

##### @ProbeClassName

> 用来标识handler的这个入参是当前打断的方法是哪个类的。只能在被标注了@OnMethod注解的探针handler方法里使用。

##### @ProbeMethodName

> 用来标识handler的这个入参是当前打断的哪个方法。只能在被标注了@OnMethod注解的探针handler方法里使用

`@ProbeMethodName([fqn=(true|false)]?)`

*   **fqn** 表示应该使用方法全名而不是简单名， 默认是false

##### @Self

表示该参数是用来访问当前打断的成员方法所依附的实例。对一个handler参数使用该注解会有效地过滤掉其他匹配的静态方法。  
（译注：这个的含义就是通过名字、签名等方式匹配出来的目标方法可能是static的也可能是非static的。使用这个注解，会直接表明我们要的是非static的，因为只有非static的方法才有一个隐式的this指针指向一个实例，即该参数）

##### @Return

> 该注解标识该参数是打断的目的方法的返回值。只可以用于 `location=@Location(Kind.RETURN)`的情况。并且该注解会造成，如果目的方法没有返回值那么就不会触发改handler

##### @Duration

> 目标方法的执行耗时会通过注解了@Duration的参数提供。只可以用于 `location=@Location(Kind.RETURN)`或 long 的情况。

##### @TargetInstance

> 这个注解标识该参数提供访问当前打断的成员方法所依附的实例（和@Self很像）但是可以用于`location=@Location([Kind.CALL|Kind.FIELD_GET|Kind.FIELD_SET)`，即非static方法被调用、字段被设置或者读取的情况。

##### @TargetMethodOrField

> 这个注解标识该参数提供方法或字段的访问（类似于 @ProbeMethodName），适用于`location=@Location([Kind.CALL|Kind.FIELD_GET|Kind.FIELD_SET)`

`@TargetMethodOrField([fqn=(true|false)]?)`

*   **fqn 表示是否使用全名而不是简单名，默认为false

* * *

## btracec

### btracec

btracec 是用来把追踪脚本（[trace scripts](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fbtraceio%2Fbtrace%2Fwiki%2FTrace-Scripts)）编译为class文件的命令行工具。

其命令用法是：  
`btracec [-cp <classpath>] [-d <directory>] <one-or-more-BTrace-.java-files>`

*   **classpath** 是用来编译BTrace 程序的classpath。默认是"."
*   **directory** 是编译后的class文件存放的目录。默认是"."

与通常使用的javac不同的是，btracec 能够在编译期间检查脚本正确性，防止其在运行期间产生关于脚本正确性的初级错误。

* * *

## btracer

### btracer

btracer是一个脚本。用于方便地在开启应用程序同时打开btrace。

其命令行语法是：  
`btracer <pre-compiled-btrace.class> <vm-arg> <application-args>`

*   **pre-compiled-btrace.class** 通过[btracec](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fbtraceio%2Fbtrace%2Fwiki%2Fbtracec)编译出的trace脚本class文件
*   **vm-args** 虚拟机参数，例如`-cp app.jar Main.class`或`-jar app.jar`
*   **application-args** 指定应用程序的参数

* * *

## Trace 脚本

### Trace 脚本

Trace脚本定义了要追踪的是什么并且怎样追踪。 它们就是一些看起来被加上了许多注解的普通Java类。注解（[annotations](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fbtraceio%2Fbtrace%2Fwiki%2FBTrace-Annotations)）标识了埋点应该在哪里放置，并且什么数据传给action。

#### 脚本元素（Script Elements）

##### 探针点（Probe Point）

即在"location" 或发生 "event"时，trace action的一系列语句才会被执行。探针点指的是在目标程序中，我们添加的一些感兴趣的点或者事件发生的时刻。

##### 追踪动作（Trace Actions or Actions）

当一个探针被触发时，要执行的一系列指令语句。

##### 动作方法（Action Methods）

当探针被触发时，会被运行的那些在脚本里定义的static方法。

#### 限制

为了保证在目标程序中动态注入代码的安全性，有下面几点强制的限制。

*   不允许new 一个对象
*   不允许new 一个数组
*   不允许手动抛出异常
*   不允许捕获任何异常
*   不允许随意调用实例的方法或static方法，在BTrace程序中只能调用在该程序中声明的方法（译注：存疑）
*   不允许声明外部、内部、嵌套、局部类
*   不允许有synchronized块或synchronized方法
*   不允许有循环语句（for，while，do...while）
*   不允许继承类（超类只能是 java.lang.Object）
*   不允许实现接口
*   不允许有assert断言语句
*   不允许有字面值
