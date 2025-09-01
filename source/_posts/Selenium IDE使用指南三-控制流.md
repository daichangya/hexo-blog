---
title: Selenium IDE使用指南三（控制流）
id: 1400
date: 2024-10-31 22:01:53
author: daichangya
excerpt: "SeleniumIDE附带的命令使您可以添加条件逻辑和循环到测试中。这使您仅在满足应用程序中的某些条件时才执行命令（或一组命令），或根据预定义的标准重复执行命令。JavaScript表达式通过使用JavaScript表达式检查应用程序中的条件。您可以在测试过程中的任何时候使用executescrip"
permalink: /archives/seleniumide3/
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

Selenium IDE附带的命令使您可以添加条件逻辑和循环到测试中。

这使您仅在满足应用程序中的某些条件时才执行命令（或一组命令），或根据预定义的标准重复执行命令。

[](#javascript-expressions)JavaScript表达式
----------------------------------------

通过使用JavaScript表达式检查应用程序中的条件。

您可以在测试过程中的任何时候使用`execute script`或`execute async script`命令运行一段JavaScript，并将结果存储在变量中。这些变量可以在控制流命令中使用。

您也可以直接在控制流命令中使用JavaScript表达式。

[](#available-commands)可用命令
---------------------------

控制流命令通过指定打开和关闭命令来表示一组命令（或块）来工作。

以下是每个可用的控制流命令以及它们的伴随命令和/或关闭命令。

*   `if`，`else if`，`else`，`end`
*   `times`， `end`
*   `do`， `repeat if`
*   `while`， `end`

让我们逐一介绍示例。

[](#conditional-branching)条件分支
------------------------------

条件分支使您可以更改测试中的行为。

![如果示例](https://images.jsdiff.com/if_1589633826630.png)

### [](#if-selenium-ide-docs-en-api-commands-if)[`if`](/archives/selenium-ide-commands#if)

这是条件块的打开命令。

同时提供了您要评估的JavaScript表达式。这可以包含从测试中的先前JavaScript表达式创建的变量。所有这些都`target`输入到`if`命令的输入字段中。

如果该表达式评估为`true`则测试将执行它后面，直到下一个条件控制流命令命令（例如，`else if`，`else`，或`end`）。

如果表达式的计算来`false`将跳过随后的命令和跳转到下一个相关条件控制流命令（例如，`else if`，`else`，或`end`）。

### [](#else-if-selenium-ide-docs-en-api-commands-else-if)[`else if`](/archives/selenium-ide-commands#else-if)

该命令在`if`命令块中使用。

就像`if`在`target`输入字段中使用JavaScript表达式来求值一样，执行它后面的命令分支，或者跳到下一个相关的控制流命令（例如`else`或`end`）。

### [](#else-selenium-ide-docs-en-api-commands-else)[`else`](/archives/selenium-ide-commands#else)

`else`是您在一个`if`区块中可以拥有的最终条件。如果不满足任何先决条件，则将执行此命令分支。

完成后，将跳转到`end`命令。

### [](#end-selenium-ide-docs-en-api-commands-end)[`end`](/archives/selenium-ide-commands#end)

该命令终止条件命令块。没有它，命令块将不完整，您将收到一条有用的错误消息，让您知道何时尝试运行测试。

[](#looping)循环播放
----------------

循环使您可以遍历给定的命令集。

### [](#times-selenium-ide-docs-en-api-commands-times)[`times`](/archives/selenium-ide-commands#times)

有了`times`你可以指定一个迭代次数要执行的命令集。该数字进入命令的`target`输入字段`times`。

要关闭`times`命令块，请确保使用`end`命令。

![时间示例](https://www.selenium.dev/selenium-ide/img/docs/control-flow/times.png)

### [](#do-selenium-ide-docs-en-api-commands-do)[`do`](/archives/selenium-ide-commands#do)

您从`do`命令开始此循环，然后是要执行的命令，然后以命令结束`repeat if`。`repeat if`接受您要在`target`输入字段中求值的JavaScript表达式。

`do`将先执行之后的命令，然后再对中的表达式`repeat if`求值。如果表达式返回，`true`则测试将跳回到`do`命令并重复该序列。

![做例子](https://images.jsdiff.com/do_1589633860170.png)

这将一直持续到条件返回`false`或触发无限循环保护-默认为`1000`尝试。您可以通过`value`在`repeat if`命令的输入字段中指定一个数字来覆盖此默认值。

### [](#while-selenium-ide-docs-en-api-commands-while)[`while`](/archives/selenium-ide-commands#while)

通过`while`提供JavaScript表达式，您希望在`target`输入字段中求值。如果它求值到`true`命令块，则将继续执行直到到达`end`命令。

完成后，测试将跳回到`while`命令并重复相同的顺序（首先检查条件是否变为`true`或`false`）。

要关闭`while`命令块，请使用`end`命令。

![while-example](https://images.jsdiff.com/while_1589633937937.png)

循环将重试，直到条件返回`false`或无限循环保护被触发为止（默认为`1000`尝试）。您可以通过`value`在`while`命令的输入字段中指定一个数字来覆盖此默认值。

### [](#foreach-selenium-ide-docs-en-api-commands-for-each)[`forEach`](/archives/selenium-ide-commands#for-each)

尽力做到最好，我们有能力遍历一个集合（例如，一个JS数组），并在我们执行该过程时引用该集合中的每个项目。

在该`target`字段中，指定包含要迭代的数组的变量的名称。在该`value`字段中，指定要使用的迭代器变量的名称。对于数组中的每个条目，将执行以下命令。在每次迭代期间，将通过迭代器变量访问当前条目的内容。

![每个例子](https://images.jsdiff.com/for-each_1589633972398.png)
[](#nesting-commands)嵌套命令
-------------------------

您可以根据需要嵌套控制流命令（例如，一个`if`块可以放在一个`while`块内部，反之亦然）。

![嵌套示例](https://images.jsdiff.com/nested_1589634003147.png)
[](#syntax-validation)语法验证
--------------------------

如果不确定控制流语法是否正确，请尝试运行测试以查看。IDE将发现控制流语法中的错误，并调出不正确或丢失的特定命令。

![错误示例](https://images.jsdiff.com/error_1589634033058.png)