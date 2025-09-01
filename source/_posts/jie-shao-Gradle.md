---
title: 介绍Gradle
id: 1269
date: 2024-10-31 22:01:50
author: daichangya
excerpt: 1.概述Gradle是基于Groovy的构建管理系统，专门用于构建基于Java的项目。可以在此处找到安装说明。2.BuildingBlocks–ProjectsandTasks(构件-项目和任务)在Gradle中，构建由一个或多个项目组成，每个项目由一个或多个任务组成。Gradle中的项目可以组装j
permalink: /archives/jie-shao-Gradle/
categories:
- gradle教程
---

## 1.概述
Gradle是基于Groovy的构建管理系统，专门用于构建基于Java的项目。

可以在此处找到安装说明。


## 2. Building Blocks – Projects and Tasks(构件-项目和任务)
在Gradle中，构建由一个或多个项目组成，每个项目由一个或多个任务组成。

Gradle中的项目可以组装jar，war甚至是zip文件。

一项任务是一项工作。这可以包括编译类，或创建和发布 Java/web archives.

一个简单的任务可以定义为：
```
task hello {
    doLast {
        println 'Baeldung'
    }
}
```
如果我们在build.gradle所在的位置使用gradle -q hello命令执行上述任务，则应该在控制台中看到输出。
### 2.1. Tasks
Gradle的构建脚本不过是Groovy而已：
```
task toLower {
    doLast {
        String someString = 'HELLO FROM BAELDUNG'
        println "Original: "+ someString
        println "Lower case: " + someString.toLowerCase()
    }
}
```
我们可以定义依赖于其他任务的任务。可以通过在任务定义中传递dependsOn：taskName参数来定义任务依赖项：

```
task helloGradle {
    doLast {
        println 'Hello Gradle!'
    }
}
 
task fromBaeldung(dependsOn: helloGradle) {
    doLast {
        println "I'm from Baeldung"
    }
}
```
### 2.2。向任务添加行为
我们可以定义任务并通过一些其他行为来增强它：
```
task helloBaeldung {
    doLast {
        println 'I will be executed second'
    }
}
 
helloBaeldung.doFirst {
    println 'I will be executed first'
}
 
helloBaeldung.doLast {
    println 'I will be executed third'
}
 
helloBaeldung {
    doLast {
        println 'I will be executed fourth'
    }
}
```
doFirst和doLast分别在操作列表的顶部和底部添加操作，并且可以在单个任务中多次定义操作。

### 2.3。添加任务属性
我们还可以定义属性：
```
task ourTask {
    ext.theProperty = "theValue"
}
```
Here, we're setting “theValue” as theProperty of the ourTask task.
## 3.管理插件
Gradle中有两种类型的插件：脚本和二进制。

为了从附加功能中受益，每个插件都需要经历两个阶段：解析和应用。

解决意味着找到正确的插件jar版本，并将其添加到项目的类路径中。

应用插件是在项目上执行Plugin.apply（T） 。

### 3.1。应用脚本插件
在aplugin.gradle中，我们可以定义一个任务：
```
task fromPlugin {
    doLast {
        println "I'm from plugin"
    }
}
```
如果要将此插件应用于项目build.gradle文件，我们要做的就是将以下行添加到build.gradle中：

1
apply from: 'aplugin.gradle'
现在，执行gradle task命令应该在任务列表中显示fromPlugin任务。

### 3.2. Applying Binary Plugins Using Plugins DSL
在添加核心二进制插件的情况下，我们可以添加短名称或插件ID：
```
plugins {
    id 'application'
}
```
现在，应用程序插件中的运行任务应该在项目中可用，以执行任何可运行的 jar。要应用社区插件，我们必须提到一个完全合格的插件ID：

```
plugins {
    id "org.shipkit.bintray" version "0.9.116"
}
```
现在，Shipkit任务应该在gradle任务列表中可用。


插件DSL的局限性是：

- 它不支持plugins块内的Groovy代码
plugins块必须是项目的构建脚本中的顶级语句（在其之前仅允许buildscripts {}块）
- 插件DSL不能写在脚本插件，settings.gradle文件或init脚本中
- DSL插件仍在发展中。在更高的Gradle版本中，DSL和其他配置可能会更改。

### 3.3。应用插件的旧程序
我们也可以使用“ apply plugin”来应用插件：
```
apply plugin: 'war'
```
如果需要添加社区插件，则必须使用buildscript {}块将外部jar添加到构建类路径。

然后，我们可以在构建脚本中应用该插件，但是 只能在任何现有的plugins {}块之后：
```
buildscript {
    repositories {
        maven {
            url "https://plugins.gradle.org/m2/"
        }
    }
    dependencies {
        classpath "org.shipkit:shipkit:0.9.117"
    }
}
apply plugin: "org.shipkit.bintray-release"
```
## 4.依赖管理
Gradle支持非常灵活的依赖项管理系统，它与多种可用方法兼容。

Gradle中依赖性管理的最佳实践是版本控制，动态版本控制，解决版本冲突和管理可传递依赖性。

### 4.1。依赖配置
依赖性分为不同的配置。配置具有名称，并且它们可以彼此扩展。

如果应用Java插件，则将具有可用于对依赖项进行分组的compile，testCompile，运行时配置。在默认的C onfiguration伸出“ 运行”。

### 4.2。声明依赖项
让我们看一个使用几种不同方式添加一些依赖项（Spring和Hibernate）的示例：
```
dependencies {
    compile group: 
      'org.springframework', name: 'spring-core', version: '4.3.5.RELEASE'
    compile 'org.springframework:spring-core:4.3.5.RELEASE',
            'org.springframework:spring-aop:4.3.5.RELEASE'
    compile(
        [group: 'org.springframework', name: 'spring-core', version: '4.3.5.RELEASE'],
        [group: 'org.springframework', name: 'spring-aop', version: '4.3.5.RELEASE']
    )
    testCompile('org.hibernate:hibernate-core:5.2.12.Final') {
        transitive = true
    }
    runtime(group: 'org.hibernate', name: 'hibernate-core', version: '5.2.12.Final') {
        transitive = false
    }
}
```
我们在各种配置中声明依赖项：compile，testCompile和运行时各种格式。


有时我们需要具有多个工件的依赖项。在这种情况下，我们可以添加仅工件的符号@extensionName（或扩展形式的ext）来下载所需的工件：

```
runtime "org.codehaus.groovy:groovy-all:2.4.11@jar"
runtime group: 'org.codehaus.groovy', name: 'groovy-all', version: '2.4.11', ext: 'jar'
```
在这里，我们添加了@jar表示法，以仅下载jar工件，而没有依赖项。

要将依赖项添加到任何本地文件中，我们可以使用如下代码：
```
compile files('libs/joda-time-2.2.jar', 'libs/junit-4.12.jar')
compile fileTree(dir: 'libs', include: '*.jar')
```
当我们想要避免传递依赖时， 可以在配置级别或依赖级别上进行：

```
configurations {
    testCompile.exclude module: 'junit'
}
  
testCompile("org.springframework.batch:spring-batch-test:3.0.7.RELEASE"){
    exclude module: 'junit'
}
```
## 5.多项目构建
### 5.1。建立生命周期
在初始化阶段，Gradle确定哪些项目将参与多项目构建。

通常在位于项目根目录中的settings.gradle文件中提到此问题。Gradle还会创建参与项目的实例。

在配置阶段，将根据需要根据Gradle功能配置来配置所有创建的项目实例。

在此功能中，仅将必需的项目配置为用于特定任务执行。这样，可以大大减少大型多项目构建的配置时间。此功能仍在发展中。

最后，在执行阶段，将执行创建和配置的任务子集。我们可以在settings.gradle和build.gradle文件中包含代码以感知这三个阶段。

在settings.gradle中：
```
println 'At initialization phase.'
```
在build.gradle中：
```
println 'At configuration phase.'
 
task configured { println 'Also at the configuration phase.' }
 
task execFirstTest { doLast { println 'During the execution phase.' } }
 
task execSecondTest {
    doFirst { println 'At first during the execution phase.' }
    doLast { println 'At last during the execution phase.' }
    println 'At configuration phase.'
}
```
### 5.2。创建多项目构建
我们可以在根文件夹中执行gradle init命令来为settings.gradle和build.gradle文件创建框架。

所有通用配置将保留在根构建脚本中：

```
allprojects {
    repositories {
        mavenCentral() 
    }
}
 
subprojects {
    version = '1.0'
}
```
设置文件需要包含根项目名称和子项目名称：
```
rootProject.name = 'multi-project-builds'
include 'greeting-library','greeter'
```
现在，我们需要有几个子文件夹，分别名为greeting-library和greeter，以演示多项目构建。每个子项目都需要有一个单独的构建脚本来配置它们各自的依赖关系和其他必要的配置。

如果我们想让greeter项目依赖于greeting-library，我们需要在greeter的构建脚本中包含依赖项：
```
dependencies {
    compile project(':greeting-library') 
}
```
## 6.使用Gradle包装器
如果Gradle项目具有针对Linux的gradlew文件和针对Windows的gradlew.bat文件，那么我们无需安装Gradle即可构建该项目。

如果我们在Windows中执行gradlew 构建，而在Linux中执行./gradlew构建，则gradlew文件中指定的Gradle发行版将自动下载。

如果我们想将Gradle包装器添加到我们的项目中：
```
gradle wrapper --gradle-version 4.2.1
```
该命令需要从项目的根目录执行。这将创建所有必要的文件和文件夹，以将Gradle包装器绑定到项目。另一种方法是将包装器任务添加到构建脚本中：
```
task wrapper(type: Wrapper) {
    gradleVersion = '4.2.1'
}
```
现在，我们需要执行包装器任务，该任务会将我们的项目绑定到包装器。除了gradlew文件之外，在gradle文件夹内还会生成一个包装器文件夹，其中包含一个jar和一个属性文件。

如果我们想切换到摇篮的新版本中，我们只需要更改的条目gradle- wrapper.properties。


7.结论
在本文中，我们对Gradle进行了研究，发现在解决版本冲突和管理传递依赖方面，它比其他现有的构建工具具有更大的灵活性。