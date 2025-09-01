---
title: Gradle 转 Maven POM
id: 1266
date: 2024-10-31 22:01:50
author: daichangya
excerpt: "1.简介在本教程中，我们将研究如何将Gradle构建文件转换为MavenPOM文件。我们还将探讨一些可用的自定义选项。2.GradleBuildFile让我们以一个标准的摇篮Java项目开始，gradle这个对Maven的，具有以下的build.gradle文件：repositories{maven"
permalink: /archives/gradle%E8%BD%ACmavenpom/
categories:
 - gradle教程
---

## 1.简介
在本教程中，我们将研究如何将Gradle构建文件转换为Maven POM文件。我们还将探讨一些可用的自定义选项。

## 2. Gradle Build File
让我们以一个标准的摇篮Java项目开始，gradle这个对Maven的， 具有以下的build.gradle文件：
```
repositories {
    mavenCentral()
}
 
group = 'com.daicy'
version = '0.0.1-SNAPSHOT'
 
apply plugin: 'java'
 
dependencies {
    compile('org.slf4j:slf4j-api')
    testCompile('junit:junit')
}
```
## 3. Maven插件
Gradle附带了Maven插件，该插件增加了将Gradle文件转换为Maven POM文件的支持。它还可以将工件部署到Maven存储库。

要使用此功能，我们将Maven插件添加到我们的build.gradle文件中：

```
apply plugin: 'maven'
```
该插件使用Gradle文件中存在的组和版本，并将它们添加到POM文件中。同样，它会自动从目录名称中获取artifactId。

该插件也会自动添加安装任务。因此，要进行转换，请运行以下命令：

```
gradle install
```
运行上面的命令将创建一个包含三个子目录的构建目录：

- 库–包含名称为$ {artifactId}-$ {version} .jar的jar
- poms –包含名称为pom-default.xml的转换后的POM文件
- tmp / jar –包含清单
生成的POM文件将如下所示：
```
<?xml version="1.0" encoding="UTF-8"?>
<project xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
    xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.baeldung</groupId>
  <artifactId>gradle-to-maven</artifactId>
  <version>0.0.1-SNAPSHOT</version>
  <dependencies>
    <dependency>
      <groupId>org.slf4j</groupId>
      <artifactId>slf4j-api</artifactId>
      <scope>compile</scope>
    </dependency>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <scope>test</scope>
    </dependency>
  </dependencies>
</project>
```
该安装任务还上传生成的POM文件和JAR的本地Maven仓库。

## 4.自定义Maven插件
在某些情况下，在生成的POM文件中自定义项目信息可能很有用。让我们来看看。
### 4.1. groupId, artifactId, and version
更改groupId，artifactId和POM 的版本可以在install块中处理：
```
install {
    repositories {
        mavenInstaller {
            pom.version = '0.0.1-maven-SNAPSHOT'
            pom.groupId = 'com.daicy.sample'
            pom.artifactId = 'gradle-maven-converter'
        }
    }
}
```
现在，运行 安装任务将生成具有以上信息的POM文件：
```
<groupId>com.daicy.sample</groupId>
<artifactId>gradle-maven-converter</artifactId>
<version>0.0.1-maven-SNAPSHOT</version>
```
### 4.2. Directory and Name of the POM
有时，我们可能需要将POM文件复制到其他目录并使用不同的名称。因此，让我们在安装块中添加以下内容：

```
pom.writeTo("${mavenPomDir}/${project.group}/${project.name}/pom.xml")
```
该插件公开了mavenPomDir属性，该属性将指向build / poms。我们还可以提供要将POM文件复制到的任何目录的绝对路径。

运行安装任务后，我们可以在build / poms / com.baeldung / gradle-to-maven中看到pom.xml。

### 4.3.自动生成的内容
Maven插件还使您可以直接更改任何生成的POM元素。例如，要使依赖项为可选，我们可以将以下闭包添加到pom.whenConfigured中：
```
pom.whenConfigured { pom ->
    pom.dependencies.find {dep -> dep.groupId == 'junit' && dep.artifactId == 'junit' }.optional = true
}
```
这将产生添加到依赖项的可选属性：

```
<dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <scope>test</scope>
      <optional>true</optional>
</dependency>
```
### 4.4. Additional Information
最后，如果要添加其他信息，可以将任何Maven支持的元素包括到pom.project构建器中。

让我们添加一些许可证信息：

```
pom.project {
    inceptionYear '2020'
    licenses {
        license {
            name 'My License'
            url 'http://www.mycompany.com/licenses/license.txt'
            distribution 'repo'
        }
    }
}
```
现在，我们可以看到许可证信息已添加到POM：

```
<inceptionYear>2020</inceptionYear>
<licenses>
    <license>
      <name>My License</name>
      <url>http://www.mycompany.com/licenses/license.txt</url>
      <distribution>repo</distribution>
    </license>
</licenses>
```
5.结论
在本快速教程中，我们学习了如何将Gradle构建文件转换为Maven POM。

与往常一样，本文的源代码可以在GitHub上找到。