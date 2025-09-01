---
title: Selenium IDE使用指南四（代码导出）
id: 1401
date: 2024-10-31 22:01:53
author: daichangya
excerpt: 入门您可以通过右键单击测试或套件，选择Export，选择目标语言，然后单击，将测试或套件的测试导出到WebDriver代码Export。这会将包含导出的目标语言代码的文件保存到浏览器的下载目录中。原产地跟踪代码注释导出时，有一个可选的切换开关可启用源跟踪代码注释。这会将内联代码注释放置在导出的文件中
permalink: /archives/Selenium-IDE-shi-yong-zhi-nan-si-dai-ma/
categories:
- selenium-ide
---

1. [Selenium IDE使用指南一（爬虫脚本录制器）](https://blog.jsdiff.com/archives/seleniumide1)
2. [Selenium IDE使用指南二（命令行运行器）](https://blog.jsdiff.com/archives/seleniumide2)
3. [Selenium IDE使用指南三（控制流）](https://blog.jsdiff.com/archives/seleniumide3)
4. [Selenium IDE使用指南四（代码导出）](https://blog.jsdiff.com/archives/selenium-ide-code-export)
5. [Selenium IDE使用指南五（常见问题）](https://blog.jsdiff.com/archives/seleniumide5)
6. [Selenium IDE使用指南六（指令列表）](https://blog.jsdiff.com/archives/selenium-ide-commands)
7. [Selenium IDE使用指南七（参数定义）](https://blog.jsdiff.com/archives/selenium-ide-arguments)

[](#getting-started)入门
----------------------

您可以通过右键单击测试或套件，选择`Export`，选择目标语言，然后单击，将测试或套件的测试导出到WebDriver代码`Export`。

![代码导出右键单击](https://images.jsdiff.com/right-click_1589634458789.png)
![代码导出菜单](https://images.jsdiff.com/menu_1589634473800.png)

这会将包含导出的目标语言代码的文件保存到浏览器的下载目录中。

### [](#origin-tracing-code-comments)原产地跟踪代码注释

导出时，有一个可选的切换开关可启用源跟踪代码注释。

这会将内联代码注释放置在导出的文件中，其中包含有关生成该文件的Selenium IDE中的测试步骤的详细信息。

[](#supported-exports)支持的出口
---------------------------

当前，支持导出到以下语言和测试框架。

*   C＃NUnit
*   Java JUnit
*   JavaScript Mocha
*   python pytest

我们打算在每种语言的至少一个测试框架中支持所有官方支持的Selenium编程语言绑定（例如Java，JavaScript，C＃，Python和Ruby）。

欢迎提供帮助以添加特定语言的新语言和测试框架。有关[如何操作](#how-to-contribute)的详细信息，请参见[如何贡献](#how-to-contribute)。

### [](#c-nunit)C＃NUnit

C＃NUnit的导出代码被构建为与[.NET Core](https://dotnet.microsoft.com/learn/dotnet/hello-world-tutorial/install)，NUnit 3.11和最新版本的Selenium一起使用。

要创建一个与NUnit一起使用的新样板项目，请使用以下`dotnet new`命令。

    dotnet new nunit -n NUnit-Tests --framework netcoreapp2.0
    

使用以下`.csproj`文件，您可以使用以下`dotnet restore`命令安装正确的软件包和版本。

    <!-- filename: example.csproj -->
    <Project Sdk="Microsoft.NET.Sdk">
    
      <PropertyGroup>
        <TargetFramework>netcoreapp2.0</TargetFramework>
    
        <IsPackable>false</IsPackable>
      </PropertyGroup>
    
      <ItemGroup>
        <PackageReference Include="nunit" Version="3.11.0" />
        <PackageReference Include="NUnit3TestAdapter" Version="3.13.0" />
        <PackageReference Include="Microsoft.NET.Test.Sdk" Version="16.0.1" />
        <PackageReference Include="Selenium.Support" Version="4.0.0-alpha03" />
        <PackageReference Include="Selenium.WebDriver" Version="4.0.0-alpha03" />
      </ItemGroup>
    
    </Project>
    

    > dotnet restore example.csproj
    

### [](#c-xunit)C＃xUnit

C＃xUnit的导出代码被构建为可与C＃，xUnit和最新版本的Selenium一起使用。

就像C＃Nunit一样，您可以使用dotnet工具安装它，并在安装这些依赖项之后运行它（例如，使用`Install-Package Selenium.WebDriver`or或`dotnet add package Selenium.WebDriver`）。

要创建一个与xUnit一起使用的新样板项目，请使用以下`dotnet new`命令。

    > dotnet new xUnitTests
    

使用以下`.csproj`文件，您可以使用以下`dotnet restore`命令安装正确的软件包和版本。

    <!-- filename: example.csproj -->
    <Project Sdk="Microsoft.NET.Sdk">
    
      <PropertyGroup>
        <TargetFramework>netcoreapp2.0</TargetFramework>
    
        <IsPackable>false</IsPackable>
      </PropertyGroup>
    
      <ItemGroup>
        <PackageReference Include="xunit" Version="2.4.1" />
        <PackageReference Include="Microsoft.NET.Test.Sdk" Version="16.0.1" />
        <PackageReference Include="Selenium.Support" Version="4.0.0-alpha03" />
        <PackageReference Include="Selenium.WebDriver" Version="4.0.0-alpha03" />
      </ItemGroup>
    
    </Project>
    

    > dotnet restore example.csproj
    

### [](#java-junit)Java JUnit

Java JUnit的导出代码可与Java 8，JUnit 4.12和最新版本的Selenium一起使用。

您应该能够将导出的Java文件放入带有`pom.xml`列出这些依赖关系的文件的标准Maven目录结构中并运行它。

这是一个示例`pom.xml`，可帮助您入门。

    <project>
      <modelVersion>4.0.0</modelVersion>
      <groupId>org.seleniumhq.selenium</groupId>
      <artifactId>selenium-ide-java-code-export</artifactId>
      <version>1</version>
      <url>http://maven.apache.org</url>
      <dependencies>
        <dependency>
          <groupId>junit</groupId>
          <artifactId>junit</artifactId>
          <version>4.12</version>
          <scope>test</scope>
        </dependency>
        <dependency>
          <groupId>org.seleniumhq.selenium</groupId>
          <artifactId>selenium-java</artifactId>
          <version>4.0.0-alpha-3</version>
        </dependency>
      </dependencies>
    </project>
    

### [](#javascript-mocha)JavaScript Mocha

JavaScript Mocha的导出代码被构建为与Node 10，Mocha 6.1.x和最新版本的Selenium一起使用。

安装这些依赖项（例如，使用`npm install`）后，您应该能够获取导出的JavaScript文件并运行它。

这是一个示例`package.json`，可帮助您入门。

    {
      "dependencies": {
        "mocha": "^6.1.4",
        "selenium-webdriver": "^4.0.0-alpha.3"
      }
    }
    

### [](#python-pytest)python pytest

Python pytest的导出代码可与Python 3，pytest 4.6.x和最新版本的Selenium一起使用。

安装这些依赖项（例如，使用`pip3 install`）后，您应该能够获取导出的JavaScript文件并运行它。

这是一个示例`requirements.txt`，可帮助您入门。

    pytest == 4.6.3
    selenium == 4.0.0a1
    

    > pip3 install -r ./requirements.txt
    

### [](#ruby-rspec)Ruby RSpec

Ruby Rspec的导出代码可与Ruby 2.6.x，RSpec 3.9.x和最新版本的Selenium一起使用。

通过使用[Bundler](https://www.google.com/search?q=bundler)和以下工具，`Gemfile`您可以安装必要的依赖项。

    # Gemfile
    source 'https://rubygems.org'
    
    gem 'selenium-webdriver'
    gem 'rspec'
    

    > gem install bunder
    > bundle install
    

[](#how-to-contribute)如何贡献
--------------------------

代码导出以模块化方式构建，以帮助实现贡献。

每种语言和测试框架都有自己的包含要导出代码的包。每个代码段都映射到Selenium IDE中的命令，并且每个程序包都依赖于底层的“核心”程序包，该程序包承担了所有繁重的工作。

以下是在一种已经建立的语言中为一种新语言或一种新的测试框架创建代码的步骤。

### [](#1-create-a-new-package)1.创建一个新包

首先，复制一个现有的语言包（例如`packages/code-export-java-junit`），然后将其重命名（例如，文件夹和文件中的详细信息`package.json`）为您想要贡献的目标语言和框架（例如`packages/code-export-ruby-rspec`，等等）。

接下来，添加新的软件包作为依赖于[该`package.json`在`code-export`](https://github.com/SeleniumHQ/selenium-ide/blob/c55c556ffc947fd3f6ee8ab317915c6f879a88dc/packages/code-export/package.json#L22)。

最后，`yarn`从项目的根目录运行，然后使用构建项目`yarn watch`（[此处](https://github.com/SeleniumHQ/selenium-ide/blob/v3/README.md)提供了进行本地构建的完整详细信息）。

### [](#2-update-the-locators-and-commands)2.更新定位器和命令

代码导出的基础是特定于语言的字符串，这些字符串将转换为输出的代码。其中最突出的是命令和定位器策略（例如，“ by”查找的语法）。

对于给定的语言，每种语言都有一个文件，以及随附的测试文件。

您可以在中看到一个示例`packages/code-export-java-junit`。

*   [指令](https://github.com/SeleniumHQ/selenium-ide/blob/v3/packages/code-export-java-junit/src/command.js)
*   [命令测试](https://github.com/SeleniumHQ/selenium-ide/blob/v3/packages/code-export-java-junit/__test__/src/command.spec.js)
*   [定位器策略](https://github.com/SeleniumHQ/selenium-ide/blob/v3/packages/code-export-java-junit/src/location.js)
*   [定位器策略测试](https://github.com/SeleniumHQ/selenium-ide/blob/v3/packages/code-export-java-junit/__test__/src/location.spec.js)

声明新命令时，可以将其输出指定[为字符串](https://github.com/SeleniumHQ/selenium-ide/blob/v3/packages/code-export-java-junit/src/command.js#L192)，也可以指定[为](https://github.com/SeleniumHQ/selenium-ide/blob/v3/packages/code-export-java-junit/src/command.js#L192)[指定缩进级别的对象](https://github.com/SeleniumHQ/selenium-ide/blob/v3/packages/code-export-java-junit/src/command.js#L242-L249)。

内置在代码导出中的是一个前缀控件，用于控制输出代码的缩进。如果命令的输出是冗长的并且您想明确显示，则此结构很有用。或者，如果命令更改了紧随其后的命令的缩进级别。

### [](#3-create-the-hooks)3.创建钩子

钩子构成了要导出的代码的大部分结构（例如，套件，测试以及其中包含的所有内容，例如设置，拆卸等）。它们还使插件能够将代码导出到测试或套件的不同部分。

有9种不同的钩子：

*   `afterAll` （所有测试完成后）
*   `afterEach`（完成每个测试后-之前`afterAll`）
*   `beforeAll` （在运行所有测试之前）
*   `beforeEach`（在运行每个测试之前-之后`beforeAll`）
*   `command` （为插件添加的新命令发出代码）
*   `dependency` （添加其他语言依赖性）
*   `inEachBegin` （在每个测试的开始阶段）
*   `inEachEnd` （在每个测试的末尾）
*   `variable` （声明将在整个套件中使用的新变量）

您可以在`packages/code-export-java-junit`此处看到实现钩子的示例：[钩子](https://github.com/SeleniumHQ/selenium-ide/blob/v3/packages/code-export-java-junit/src/hook.js)

### [](#4-update-the-language-specific-attributes)4.更新语言特定的属性

您需要使用每种语言指定一些底层细节。诸如缩进多少空间，如何声明方法，测试，套件等之类的事情。

您可以在`packages/code-export-java-junit`此处查看实现此示例：[语言特定的选项](https://github.com/SeleniumHQ/selenium-ide/blob/v3/packages/code-export-java-junit/src/index.js)

### [](#5-add-it-to-the-mix)5.将其添加到混合物中

将其他所有内容准备就绪后，就可以将其连接起来以在UI中使用了。

这是可能的[`packages/code-export/src/index.js`](https://github.com/SeleniumHQ/selenium-ide/blob/v3/packages/code-export/src/index.js)。

您需要将语言添加到中`availableLanguages`。

### [](#6-test-and-tune)6.测试和调整

导出代码的最佳端到端测试是导出一系列测试，并验证它们是否按预期运行。

从开发版本中，您可以访问种子测试。这是验证所有标准库命令都适用于您的新语言的良好起点。

再次测试，修复和测试，直到您对最终结果充满信心。
