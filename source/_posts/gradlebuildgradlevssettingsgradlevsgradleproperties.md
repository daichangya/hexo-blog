---
title: Gradle:build.gradle vs. settings.gradle vs. gradle.properties
id: 1268
date: 2024-10-31 22:01:50
author: daichangya
excerpt: "1.Overview在本文中，我们将研究GradleJava项目的不同配置文件。另外，我们将看到实际构建的细节。您可以查看本文以获得Gradle的一般介绍。2.build.gradle假设我们只是通过运行gradleinit–typejava-application创建一个新的Java项目。这将为我"
permalink: /archives/gradlebuildgradlevssettingsgradlevsgradleproperties/
categories:
 - gradle教程
---

## 1. Overview
在本文中，我们将研究Gradle Java项目的不同配置文件。另外，我们将看到实际构建的细节。

您可以查看  [Gradle简介](http://images.jsdiff.com/archives/%E4%BB%8B%E7%BB%8Dgradle)以获得Gradle的一般介绍。


## 2. build.gradle
假设我们只是通过运行gradle init –type java-application创建一个新的Java项目。这将为我们提供一个具有以下目录和文件结构的新项目：
```
build.gradle
gradle    
    wrapper
        gradle-wrapper.jar
        gradle-wrapper.properties
gradlew
gradlew.bat
settings.gradle
src
    main
        java  
            App.java
    test      
        java
            AppTest.java
```
我们可以将build.gradle文件视为项目的心脏或大脑。本示例的结果文件如下所示：

```
plugins {
    id 'java'
    id 'application'
}
 
mainClassName = 'App'
 
dependencies {
    compile 'com.google.guava:guava:23.0'
 
    testCompile 'junit:junit:4.12'
}
 
repositories {
    jcenter()
}
```
它由Groovy代码或更准确地说由用于描述构建的基于Groovy的DSL（域特定语言）组成。我们可以在此处定义依赖关系，还可以添加诸如Maven存储库之类的用于依赖关系解析的内容。

Gradle的基本构建块是项目和任务。在这种情况下，由于应用了  Java插件，因此隐式定义了用于构建Java项目的所有必要任务。其中一些任务是assemble，check，build，jar，javadoc，clean等。

这些任务的设置方式也是如此，它们描述了Java项目的有用依赖关系图，这意味着通常足以执行构建任务，并且Gradle（和Java插件）将确保已执行所有必需的任务。

如果我们需要其他专门任务，例如构建Docker映像，它也将放入build.gradle文件中。任务的最简单定义如下所示：
```
task hello {
    doLast {
        println 'Hello Baeldung!'
    }
}
```
我们可以通过将任务指定为Gradle CLI的参数来运行任务，如下所示：

```
$ gradle -q hello
Hello Baeldung!
```
它不会做任何有用的事情，而是打印出“ Hello Baeldung！”。当然。

如果是多项目构建，我们可能会有多个不同的build.gradle文件，每个项目一个。

该的build.gradle文件针对执行项目实例，一个项目实例每个子项目创建。可以在build.gradle文件中定义的上述任务作为Task对象集合的一部分驻留在Project实例中。任务本身由多个操作组成（作为有序列表）。


在前面的示例中，我们添加了一个Groovy闭包来打印“ Hello Baeldung！”。通过在hello Task对象上调用doLast（Closure action），可以将此列表移到此列表的末尾  。在Task执行期间，Gradle  通过调用Action.execute（T）方法按顺序  执行其每个Action。

## 3. settings.gradle
Gradle还会生成settings.gradle文件：
```
rootProject.name = 'gradle-example'
```
该settings.gradle文件是Groovy脚本也是如此。

与build.gradle文件相比，每个Gradle构建仅执行一个settings.gradle文件。我们可以使用它来定义多项目构建的项目。

此外，我们还可以将代码注册为构建的不同生命周期挂钩的一部分。

该框架要求 在多项目构建中存在settings.gradle，而对于单项目构建则是可选的。

在创建构建的Settings实例之后，通过对该文件执行文件并对其进行配置，来使用该文件。这意味着我们要在settings.gradle文件中定义子项目，如下所示：

```
include 'foo', 'bar'
```
创建构建时，Gradle 在Settings实例上调用void include（String…projectPaths）方法。

## 4. gradle.properties
Gradle 默认情况下不会创建gradle.properties文件。它可以位于不同的位置，例如在项目根目录中，GRADLE_USER_HOME内或-Dgradle.user.home命令行标志指定的位置中。

该文件由键值对组成。我们可以使用它来配置框架本身的行为，它是使用命令行标志进行配置的替代方法。

可能的键示例包括：
- org.gradle.caching=(true,false)
- org.gradle.daemon=(true,false)
- org.gradle.parallel=(true,false)
- org.gradle.logging.level=(quiet,warn,lifecycle,info,debug)
另外，您可以使用此文件将属性直接添加到Project对象，例如，具有名称空间的属性：  org.gradle.project.property_to_set

另一个用例是指定JVM参数，如下所示：

```
org.gradle.jvmargs=-Xmx2g -XX:MaxPermSize=256m -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8
```
请注意，它需要启动JVM进程来解析gradle.properties文件。这意味着这些JVM参数仅影响单独启动的JVM进程。

## 5.简而言之(The Build in a Nutshell)
假设我们不将其作为守护程序运行，我们可以将Gradle构建的一般生命周期总结如下：

它作为新的JVM进程启动
它解析  gradle.properties文件并相应地配置Gradle
接下来，它为构建创建一个  Settings实例
然后，它根据Settings对象评估  settings.gradle文件
它根据配置的Settings对象创建Projects的层次结构
最后，它将针对其项目执行每个build.gradle文件
## 6. Conclusion
我们已经看到，不同的Gradle配置文件如何实现各种开发目的。我们可以根据项目的需要使用它们来配置Gradle构建以及Gradle本身。