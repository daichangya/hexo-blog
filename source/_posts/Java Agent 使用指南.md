---
title: Java Agent 使用指南
id: 1434
date: 2024-10-31 22:01:55
author: daichangya
excerpt: "1.简介在本教程中,我们将讨论JavaInstrumentationAPI。 它提供了将字节码添加到现有已编译Java类的功能。我们还将讨论JavaAgent以及如何使用它们来检测代码。2.设定在整篇文章中,我们将使用工具构建一个应用程序。我们的应用程序将包含两个模块允许我们提款的ATM应用还有一"
permalink: /archives/javaagent%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97/
tags: 
 - aop
---


## **1.简介**

在本教程中,我们将讨论 [Java Instrumentation API。](https://docs.oracle.com/javase/7/docs/api/java/lang/instrument/Instrumentation.html) 它提供了将字节码添加到现有已编译Java类的功能。

我们还将讨论Java Agent以及如何使用它们来检测代码。

## **2.设定**

在整篇文章中,我们将使用工具构建一个应用程序。

我们的应用程序将包含两个模块:

1.  允许我们提款的ATM应用
2.  还有一个Java Agent,它将使我们能够通过测量投入的时间来衡量ATM的性能

**Java Agent将修改ATM字节码,从而使我们无需修改ATM应用即可测量提款时间。**

我们的项目将具有以下结构:


```
<groupId>com.baeldung.instrumentation</groupId>
<artifactId>base</artifactId>
<version>1.0.0</version>
<packaging>pom</packaging>
<modules>
    <module>agent</module>
    <module>application</module>
</modules>
```

在深入介绍检测细节之前,让我们看看什么是Java Agent。

## **3.什么是Java Agent**

通常,Java Agent只是特制的jar文件。**它利用 JVM提供的 [Instrumentation API](https://docs.oracle.com/javase/7/docs/api/java/lang/instrument/Instrumentation.html)来更改JVM中加载的现有字节码。**

为了使 Agent正常工作,我们需要定义两种方法:

*   *premain* –将在JVM启动时使用-javaagent参数静态加载 Agent
*   *agentmain* –使用[Java Attach API](https://docs.oracle.com/javase/7/docs/jdk/api/attach/spec/com/sun/tools/attach/package-summary.html)将 Agent动态加载到JVM中[](https://docs.oracle.com/javase/7/docs/jdk/api/attach/spec/com/sun/tools/attach/package-summary.html)

需要记住的一个有趣概念是,JVM实现(例如Oracle,OpenJDK和其他)可以提供一种动态启动 Agent的机制,但这不是必需的。

首先,让我们看看如何使用现有的Java Agent。

之后,我们将研究如何从头开始创建一个以在字节码中添加所需的功能。

## **4.加载Java Agent**

为了能够使用Java Agent,我们必须首先加载它。

我们有两种类型的负载:

*   静态–使用*premain* 通过-javaagent选项加载 Agent
*   动态–使用*agentmain*通过[Java Attach API](https://docs.oracle.com/javase/7/docs/jdk/api/attach/spec/com/sun/tools/attach/package-summary.html)将 Agent加载到JVM中[](https://docs.oracle.com/javase/7/docs/jdk/api/attach/spec/com/sun/tools/attach/package-summary.html)

接下来,我们将研究每种类型的负载并解释其工作方式。

### **4.1。静态加载**

在应用程序启动时加载Java Agent称为静态加载。 **在执行任何代码之前,静态加载会在启动时修改字节代码。**

请记住,静态负载使用*premain*方法,该方法将在任何应用程序代码运行之前运行,要使其运行,我们可以执行:



```
java -javaagent:agent.jar -jar application.jar
```

重要的是要注意,我们应该始终将*–javaagent *参数放在– *jar *参数之前。

以下是我们命令的日志:

```
22:24:39.296 [main] INFO - [Agent] In premain method
22:24:39.300 [main] INFO - [Agent] Transforming class MyAtm
22:24:39.407 [main] INFO - [Application] Starting ATM application
22:24:41.409 [main] INFO - [Application] Successful Withdrawal of [7] units!
22:24:41.410 [main] INFO - [Application] Withdrawal operation completed in:2 seconds!
22:24:53.411 [main] INFO - [Application] Successful Withdrawal of [8] units!
22:24:53.411 [main] INFO - [Application] Withdrawal operation completed in:2 seconds!
```

我们可以看到*premain*方法何时运行以及*MyAtm *类何时被转换。我们还看到了两个ATM取款交易日志,其中包含完成每个操作所花费的时间。

请记住,在我们原始的应用程序中,我们没有这个事务的完成时间,它是由我们的Java Agent添加的。

### **4.2。动态加载**

**将Java Agent加载到已经运行的JVM的过程称为动态加载。** 使用[Java Attach API附加](https://docs.oracle.com/javase/7/docs/jdk/api/attach/spec/com/sun/tools/attach/package-summary.html) Agent。

一个更复杂的场景是,当我们已经在生产环境中运行了ATM应用程序时,我们希望动态添加交易的总时间,而不会导致应用程序停机。

让我们写一小段代码来做到这一点,然后将此类 *称为AgentLoader。 *为简单起见,我们将此类放在应用程序jar文件中。因此,我们的应用程序jar文件既可以启动我们的应用程序,又可以将我们的 Agent附加到ATM应用程序:


```
VirtualMachine jvm = VirtualMachine.attach(jvmPid);
jvm.loadAgent(agentFile.getAbsolutePath());
jvm.detach();
```

现在我们有了*AgentLoader*,我们将启动我们的应用程序,以确保在事务之间的十秒钟暂停中,我们将使用*AgentLoader*动态地附加Java Agent。

我们还要添加胶水,使我们可以启动应用程序或加载 Agent。

我们将此类称为*Launcher*,它将是我们的主要jar文件类:



```
public class Launcher {
    public static void main(String[] args) throws Exception {
        if(args[0].equals("StartMyAtmApplication")) {
            new MyAtmApplication().run(args);
        } else if(args[0].equals("LoadAgent")) {
            new AgentLoader().run(args);
        }
    }
}
```

#### **运行StartMyAtmApplication**



```
java -jar application.jar StartMyAtmApplication
22:44:21.154 [main] INFO - [Application] Starting ATM application
22:44:23.157 [main] INFO - [Application] Successful Withdrawal of [7] units!
```

#### **附加Java Agent**

第一次操作后,我们将Java Agent附加到我们的JVM:


```
java -jar application.jar LoadAgent
22:44:27.022 [main] INFO - Attaching to target JVM with PID: 6575
22:44:27.306 [main] INFO - Attached to target JVM and loaded Java agent successfully
```

#### **检查应用程序日志**

现在,将Agent附加到JVM,我们将看到第二次ATM提取操作的总完成时间。

这意味着我们在应用程序运行时动态添加了我们的功能:



```
22:44:27.229 [Attach Listener] INFO - [Agent] In agentmain method
22:44:27.230 [Attach Listener] INFO - [Agent] Transforming class MyAtm
22:44:33.157 [main] INFO - [Application] Successful Withdrawal of [8] units!
22:44:33.157 [main] INFO - [Application] Withdrawal operation completed in:2 seconds!
```

## **5.创建一个Java Agent**

学习了如何使用 Agent后,让我们看看如何创建 Agent。我们将研究 [如何使用Javassist](https://www.baeldung.com/javassist)更改字节码,并将其与一些工具API方法结合使用。

由于Java Agent使用[Java Instrumentation API](https://docs.oracle.com/javase/7/docs/api/java/lang/instrument/Instrumentation.html),因此在深入创建 Agent之前,让我们看一下该API中一些最常用的方法以及它们的作用的简短说明:

*   *addTransformer* –将一个转换器添加到仪表引擎
*   *getAllLoadedClasses* –返回由JVM当前加载的所有类的数组
*   *retransformClasses* –通过添加字节码来促进已加载类的检测
*   *removeTransformer* –注销提供的Transformer
*   *redefineClasses* –使用提供的类文件*重新*定义提供的类集,这意味着该类将被完全替换,而不是像*retransformClasses*一样进行修改

### **5.1。创建*Premain*和*Agentmain*方法**

我们知道,每个Java Agent都至少需要一种*premain* 或*agentmain*方法。后者用于动态加载,而前者用于将Java Agent静态加载到JVM。

让我们在 Agent中定义它们两者,以便我们能够静态和动态加载该 Agent:


```
public static void premain(
  String agentArgs, Instrumentation inst) {
  
    LOGGER.info("[Agent] In premain method");
    String className = "com.baeldung.instrumentation.application.MyAtm";
    transformClass(className,inst);
}
public static void agentmain(
  String agentArgs, Instrumentation inst) {
  
    LOGGER.info("[Agent] In agentmain method");
    String className = "com.baeldung.instrumentation.application.MyAtm";
    transformClass(className,inst);
}
```

在每个方法中,我们都声明要更改的类,然后使用*transformClass*方法向下挖掘以转换该类。

以下是为帮助我们转换*MyAtm*类而定义的*transformClass*方法的代码。

在此方法中,我们找到了要转换的类,并使用了 *transform *方法。另外,我们将Transformer添加到仪器引擎中:


```
private static void transformClass(
  String className, Instrumentation instrumentation) {
    Class<?> targetCls = null;
    ClassLoader targetClassLoader = null;
    // see if we can get the class using forName
    try {
        targetCls = Class.forName(className);
        targetClassLoader = targetCls.getClassLoader();
        transform(targetCls, targetClassLoader, instrumentation);
        return;
    } catch (Exception ex) {
        LOGGER.error("Class [{}] not found with Class.forName");
    }
    // otherwise iterate all loaded classes and find what we want
    for(Class<?> clazz: instrumentation.getAllLoadedClasses()) {
        if(clazz.getName().equals(className)) {
            targetCls = clazz;
            targetClassLoader = targetCls.getClassLoader();
            transform(targetCls, targetClassLoader, instrumentation);
            return;
        }
    }
    throw new RuntimeException(
      "Failed to find class [" + className + "]");
}
 
private static void transform(
  Class<?> clazz,
  ClassLoader classLoader,
  Instrumentation instrumentation) {
    AtmTransformer dt = new AtmTransformer(
      clazz.getName(), classLoader);
    instrumentation.addTransformer(dt, true);
    try {
        instrumentation.retransformClasses(clazz);
    } catch (Exception ex) {
        throw new RuntimeException(
          "Transform failed for: [" + clazz.getName() + "]", ex);
    }
}
```

顺便说一句,让我们为*MyAtm*类定义转换*器*。

### **5.2。定义我们的*Transformer***

类转换器必须实现 *ClassFileTransformer*并实现transform方法。

我们将使用[Javassist](https://www.baeldung.com/javassist)将字节代码添加到*MyAtm*类,并添加具有ATW提取事务总时间的日志:



```
public class AtmTransformer implements ClassFileTransformer {
    @Override
    public byte[] transform(
      ClassLoader loader,
      String className,
      Class<?> classBeingRedefined,
      ProtectionDomain protectionDomain,
      byte[] classfileBuffer) {
        byte[] byteCode = classfileBuffer;
        String finalTargetClassName = this.targetClassName
          .replaceAll("\\.", "/");
        if (!className.equals(finalTargetClassName)) {
            return byteCode;
        }
 
        if (className.equals(finalTargetClassName)
              && loader.equals(targetClassLoader)) {
  
            LOGGER.info("[Agent] Transforming class MyAtm");
            try {
                ClassPool cp = ClassPool.getDefault();
                CtClass cc = cp.get(targetClassName);
                CtMethod m = cc.getDeclaredMethod(
                  WITHDRAW_MONEY_METHOD);
                m.addLocalVariable(
                  "startTime", CtClass.longType);
                m.insertBefore(
                  "startTime = System.currentTimeMillis();");
 
                StringBuilder endBlock = new StringBuilder();
 
                m.addLocalVariable("endTime", CtClass.longType);
                m.addLocalVariable("opTime", CtClass.longType);
                endBlock.append(
                  "endTime = System.currentTimeMillis();");
                endBlock.append(
                  "opTime = (endTime-startTime)/1000;");
 
                endBlock.append(
                  "LOGGER.info(\"[Application] Withdrawal operation completed in:" +
                                "\" + opTime + \" seconds!\");");
 
                m.insertAfter(endBlock.toString());
 
                byteCode = cc.toBytecode();
                cc.detach();
            } catch (NotFoundException | CannotCompileException | IOException e) {
                LOGGER.error("Exception", e);
            }
        }
        return byteCode;
    }
}
```

### 5.3。创建 Agent Manifest文件

最后,为了获得有效的Java Agent,我们需要一个带有几个属性的 Manifest文件。

因此,我们可以在[Instrumentation Package](https://docs.oracle.com/javase/7/docs/api/java/lang/instrument/package-summary.html)官方文档中找到 Manifest属性的完整列表。

在最终的Java Agentjar文件中,我们将以下行添加到 Manifest文件中:

```
Agent-Class: com.baeldung.instrumentation.agent.MyInstrumentationAgent
Can-Redefine-Classes: true
Can-Retransform-Classes: true
Premain-Class: com.baeldung.instrumentation.agent.MyInstrumentationAgent
```

我们的Java工具 Agent现已完成。要运行它,请参阅本文的“ [加载Java Agent”](#loading-a-java-agent) 部分。

## **六,结论**

在本文中,我们讨论了Java Instrumentation API。我们研究了如何将Java Agent静态和动态地加载到JVM中。

我们还研究了如何从头开始创建自己的Java Agent。

可以[在Github](https://github.com/eugenp/tutorials/tree/master/core-java-modules/core-java-jvm)上找到示例的完整实现。

