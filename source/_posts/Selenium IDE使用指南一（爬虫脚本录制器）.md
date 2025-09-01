---
title: Selenium IDE使用指南一（爬虫脚本录制器）
id: 1398
date: 2024-10-31 22:01:53
author: daichangya
excerpt: "安装从Chrome或Firefox网络商店安装SeleniumIDE。启动IDE安装后，通过从浏览器菜单栏中单击其图标来启动它。故障排除在菜单栏中没有看到SeleniumIDE的图标？选项1确保在浏览器的扩展程序设置中启用了IDE。通过在地址栏中输入以下内容并点击，您可以快速到达目的地Enter。C"
permalink: /archives/seleniumide1/
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

[](#installation)安装
-------------------

从[Chrome](https://chrome.google.com/webstore/detail/selenium-ide/mooikfkahbdckldjjndioackbalphokd)或[Firefox](https://addons.mozilla.org/en-US/firefox/addon/selenium-ide/)网络商店安装Selenium IDE 。

[](#launch-the-ide)启动IDE
------------------------

安装后，通过从浏览器菜单栏中单击其图标来启动它。

### [](#troubleshooting)故障排除

在菜单栏中没有看到Selenium IDE的图标？

#### [](#option-1)选项1

确保在浏览器的扩展程序设置中启用了IDE。

通过在地址栏中输入以下内容并点击，您可以快速到达目的地`Enter`。

*   Chrome： `chrome://extensions`
*   Firefox： `about:addons`

#### [](#option-2)选项2

该扩展名可能已启用，但图标已隐藏。尝试调整菜单栏的大小，以提供更多空间。

在Chrome浏览器中，您可以通过以下方法执行此操作：单击地址栏的右侧，按住该单击，然后将其向左或向右拖动。

在Firefox中，您需要右键单击，单击`Customize`，对菜单栏进行调整，然后单击`Done`。

[](#welcome-screen)欢迎屏幕
-----------------------

启动IDE后，将显示一个欢迎对话框。

这将使您快速访问以下选项：

*   在新项目中记录新测试
*   打开一个现有项目
*   创建一个新项目
*   关闭IDE

如果这是您第一次使用IDE（或者您正在启动新项目），请选择第一个选项。

[](#recording-your-first-test)记录您的第一个测试
---------------------------------------

创建新项目后，将提示您命名它，然后要求您提供基本URL。基本URL是您正在测试的应用程序的URL。只需设置一次，它就会在该项目的所有测试中使用。如果需要，您可以稍后更改。

完成这些设置后，将打开一个新的浏览器窗口，加载基本URL，并开始记录。
<separator></separator>

与页面进行交互，您的每个动作都将记录在IDE中。要停止录制，请切换到IDE窗口，然后单击录制图标。

[](#organizing-your-tests)整理测试
------------------------------

### [](#tests)测验

您可以通过单击`+`左侧工具栏菜单顶部（`Tests`标题右侧）的符号，命名它，然后单击来添加新测试`ADD`。

添加后，您可以手动输入命令，也可以单击IDE右上角的记录图标。

### [](#suites)套房

可以将测试分组到套件中。

在创建项目时，`Default Suite`会创建一个，并且您的第一个测试会自动添加到其中。

要创建和管理套件，请转到`Test suites`面板。您可以通过单击左侧工具栏菜单顶部的下拉菜单（例如，单击单词`Tests`）并选择来到达那里`Test suites`。

#### [](#add-a-suite)添加套房

要添加套件，请单击标题`+`右侧左侧栏菜单顶部的符号`Test Suites`，提供名称，然后单击`ADD`。

#### [](#add-a-test)添加测试

要将测试添加到套件上，请将鼠标悬停在套件名称上，然后执行以下操作：

1.  单击`Test Suites`标题右侧显示的图标
2.  请点击 `Add tests`
3.  从菜单中选择要添加的测试
4.  请点击 `Select`

#### [](#remove-a-test)删除测试

要删除测试，请将鼠标悬停在该测试上，然后单击`X`名称右侧显示的。

#### [](#remove-or-rename-a-suite)删除或重命名套件

要删除套件，请单击其名称右侧出现的图标，单击`Delete`，然后`Delete`在出现提示时再次单击。

要在套件名称上重命名套件，请单击名称右侧出现的图标，单击`Rename`，更新名称，然后单击`RENAME`。

[](#save-your-work)保存工作
-----------------------

要保存您刚刚在IDE中完成的所有操作，请单击IDE右上角的保存图标。

它将提示您输入保存项目的位置和名称。最终结果是带有`.side`扩展名的单个文件。

[](#playback)回放
---------------

### [](#in-browser)浏览器内

您可以在IDE中播放测试，方法是选择要播放的测试或套件，然后单击测试编辑器上方菜单栏中的播放按钮。

测试将在浏览器中播放。如果仍在从录制中打开一个窗口，则将其用于播放。否则，将打开并使用一个新窗口。

### [](#cross-browser)跨浏览器

如果要在其他浏览器上运行IDE测试，请确保安装命令行运行器。