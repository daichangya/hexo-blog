---
title: 2025 Mac电脑Jdk,Maven,Idea的安装与配置,Spring boot项目创建
id: 8ac189d1-e512-42ba-8709-fbc5b22c6056
date: 2024-11-05 09:27:37
author: daichangya
excerpt: "目录 l JDK安装与配置 l Maven安装与配置 l IDEA安装与配置 l Spring Boot项目创建与运行 JDK安装与配置 JDK版本选择建议 在选择JDK版本时，需要考虑以下因素： l 稳定性：选择已经经过广泛验证的稳定版本，如JDK 8或JDK 11，或者JDK17。 l 兼容性："
permalink: /archives/macdian-nao-jdk-maven-ideade-an-zhuang-yu-pei-zhi-spring-bootxiang-mu-chuang-jian/
categories:
 - 其他
tags: 
 - springboot
---

**目录**

l JDK安装与配置

l Maven安装与配置

l IDEA安装与配置

l Spring Boot项目创建与运行

**JDK安装与配置**

**JDK版本选择建议**

在选择JDK版本时，需要考虑以下因素：

l **稳定性**：选择已经经过广泛验证的稳定版本，如JDK 8或JDK 11，或者JDK17。

l **兼容性**：根据项目需求选择适合的JDK版本，确保与所使用的框架和库兼容。

l **新特性需求**：如果项目需要使用JDK新引入的特性，可以选择较新的版本，如JDK 17。

**安装步骤**

1\. **下载JDK安装包**

访问Oracle官网[https://www.oracle.com/java/](https://www.oracle.com/java/)下载对应版本的JDK安装包。

1\. **安装JDK**

双击安装包进行安装，按照提示完成安装过程。

1\. **配置环境变量**

打开终端，进入用户主目录，编辑.bash\_profile或.zshrc文件，添加以下配置：

   export JAVA\_HOME=/Library/Java/JavaVirtualMachines/jdk<version>.jdk/Contents/Home   export PATH=$JAVA\_HOME/bin:$PATH

保存并关闭文件，然后在终端中执行source ~/.bash\_profile或source ~/.zshrc使配置生效。

1\. **验证安装**

在终端中输入以下命令，查看Java版本信息：

   java -version   javac -version

**Maven安装与配置**

**Maven简介及作用**

Maven是一个自动化构建工具，主要用于Java项目，能够自动化处理构建、依赖管理等任务。其核心特性包括依赖管理、构建生命周期、插件机制等，使得项目构建更加灵活和高效。

**安装步骤**

1\. **下载Maven安装包**

前往Maven官方网站[https://maven.apache.org/download.cgi](https://maven.apache.org/download.cgi)，下载最新稳定版本的Maven安装包。

1\. **解压安装包**

将下载的安装包解压到指定目录，如：/usr/local/maven。

   unzip Downloads/apache-maven-3.9.9-bin.zip   sudo mv apache-maven-3.9.9 /usr/local/maven

1\. **配置环境变量**

编辑系统环境变量配置文件（如：~/.bash\_profile、~/.zshrc等），添加Maven的bin目录到PATH环境变量中。

   export PATH=/usr/local/maven/bin:$PATH

1\. **验证安装**

在终端中输入mvn -v命令，查看Maven版本信息及相关配置，确认安装成功。

**Maven仓库设置与优化建议**

Maven仓库用于存储项目所需的依赖库及插件，包括本地仓库和远程仓库。在Maven的配置文件settings.xml中设置本地仓库路径，用于存储下载的依赖库及插件。定期清理本地仓库中不再使用的依赖库，以减少存储空间占用；根据项目需求，合理配置远程仓库，提高依赖下载速度。

**IDEA安装与配置**

**IDEA简介及版本选择**

IntelliJ IDEA是一款强大的集成开发环境（IDE），支持众多编程语言和框架，广泛应用于Java开发领域。IDEA提供社区版（Community Edition）和旗舰版（Ultimate Edition），根据个人或团队需求选择合适的版本。

**安装步骤**

1\. **下载安装包**

访问IDEA官方网站[https://www.jetbrains.com/idea/download/other.html](https://www.jetbrains.com/idea/download/other.html)，下载对应版本的安装包。

1\. **安装过程**

双击安装包，按照提示完成安装，可选择自定义安装路径和组件。

1\. **首次启动与基本设置**

安装完成后，双击IDEA图标启动程序，根据个人喜好，设置主题、字体、编码等基本参数。

**插件市场**

IDEA支持丰富的插件扩展，可通过插件市场搜索并安装所需插件。推荐插件如Lombok、Maven Integration、Spring Assistant等，可提升开发效率和便利性。

**Spring Boot项目创建与运行**

**Spring Boot框架简介**

Spring Boot是一个开源的Java Web框架，旨在简化Spring应用的初始搭建以及开发过程。它提供了大量常用的非业务性功能，如配置管理、安全控制、日志记录等，帮助开发者快速构建稳定、可靠的应用。

**创建Spring Boot项目**

1\. **安装Spring Boot插件**

打开IntelliJ IDEA，在弹出的窗口中，选择“Plugins”，并输入Start Spring Boot Project, 然后安装插件。

1\. **生成项目**

选择所需的Spring Boot版本，点击Generate，选择“Create New Project”。

1\. **项目结构**

¡ src/main/resources：资源文件目录，包含应用的配置文件、静态资源等。

¡ @SpringBootApplication：Spring Boot应用的核心注解，用于启用自动配置和扫描组件。

¡ Maven：项目构建工具，用于管理项目的依赖、编译、打包等任务。

¡ src/main/java：Java源代码目录，包含应用的主要逻辑和配置。

¡ application.properties或application.yml：Spring Boot应用的配置文件，用于设置应用的各种属性。

¡ REST Controller：用于处理HTTP请求的组件，通常使用@RestController注解进行标记。

**编写并运行Hello World程序**

在IDEA中打开新创建的Spring Boot项目，在src/main/java目录下，找到主应用类（通常带有@SpringBootApplication注解），在该类中添加一个简单的REST Controller，用于处理HTTP请求并返回“Hello World”字符串。运行主应用类，启动Spring Boot应用，使用浏览器或命令行工具（如curl）访问应用的URL（http://localhost:8080/hello），查看返回的“Hello World”字符串。

**结语**

感谢您的观看，希望本指南能帮助您顺利搭建Mac上的Java开发环境，并成功创建与运行Spring Boot项目。祝您开发愉快！