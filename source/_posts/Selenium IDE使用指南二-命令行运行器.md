---
title: Selenium IDE使用指南二（命令行运行器）
id: 1399
date: 2024-10-31 22:01:53
author: daichangya
excerpt: "现在，您可以在任何浏览器上，并行和在Grid上运行所有SeleniumIDE测试，而无需编写任何代码。只需安装SeleniumIDE命令行运行程序，获取必要的浏览器驱动程序（如果在本地运行测试）以及从命令提示符启动具有所需选项的运行程序，就可以了。先决条件要使命令行运行程序正常运行，需要以下依赖项："
permalink: /archives/seleniumide2/
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

现在，您可以在任何浏览器上，并行和在Grid上运行所有Selenium IDE测试，而无需编写任何代码。

只需安装Selenium IDE命令行运行程序，获取必要的浏览器驱动程序（如果在本地运行测试）以及从命令提示符启动具有所需选项的运行程序，就可以了。

![命令行运行器样本](https://images.jsdiff.com/runner_1589633750620.png)

[](#prerequisites)先决条件
----------------------

要使命令行运行程序正常运行，需要以下依赖项：

*   `node`（Node.js编程语言）版本`8`或`10`
*   `npm` （NodeJS程序包管理器），通常与 `node`
*   `selenium-side-runner` （Selenium IDE命令行运行程序）
*   以及我们要使用的浏览器驱动程序（在下一节中有更多介绍）

    > brew install node
    > npm install -g selenium-side-runner
    

**注意：您的系统配置可能与上面的示例中使用的配置不同（例如，MacOS上的Homebrew）。如果是这样，请参阅[软件包管理器的Node安装文档，](https://nodejs.org/en/download/package-manager/)或直接从[Node downloads页面下载](https://nodejs.org/en/download/)适用于您操作系统的Node安装程序。**

[](#installing-a-browser-driver)安装浏览器驱动程序
-----------------------------------------

如果要在_本地_运行测试_，_则每个浏览器都需要一些其他设置。

Selenium通过一个称为浏览器驱动程序的小型二进制应用程序与每个浏览器进行通信。每个浏览器都有自己的浏览器，您可以手动下载并添加到系统路径，也可以使用程序包管理器安装最新版本的浏览器驱动程序（推荐）。

您还需要在计算机上安装浏览器。

### [](#chrome)Chrome

对于Chrome，您需要[ChromeDriver](http://chromedriver.chromium.org)。

    > npm install -g chromedriver
    

### [](#edge)Edge

对于Microsoft Edge，您需要在Windows上运行，并且还需要[EdgeDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)。

    > npm install -g edgedriver
    

### [](#firefox)火狐浏览器

对于Firefox，您需要[geckodriver](https://github.com/mozilla/geckodriver)。

    > npm install -g geckodriver
    

### [](#internet-explorer)IE浏览器
<separator></separator>
对于Internet Explorer，您需要在Windows上运行，并且还需要[IEDriver](https://github.com/SeleniumHQ/selenium/wiki/InternetExplorerDriver)。

    > npm install -g iedriver
    

要使IEDriver工作，还需要一些其他设置。详细信息[在这里](https://github.com/SeleniumHQ/selenium/wiki/InternetExplorerDriver#required-configuration)。

### [](#safari)苹果浏览器

对于Safari，您需要[SafariDriver](https://developer.apple.com/documentation/webkit/testing_with_webdriver_in_safari)。

它附带了最新版本的Safari。您只需采取几个步骤就可以在计算机上启用它。有关详细信息，请参见[SafariDriver文档的本部分](https://developer.apple.com/documentation/webkit/testing_with_webdriver_in_safari#2957277)。

[](#launching-the-runner)Launching the runner
-----------------------------

安装`selenium-side-runner`完所有组件后，只需在命令行中调用测试，然后再调用之前保存的项目文件的路径即可运行测试请参阅 使用指南一。

    > selenium-side-runner /path/to/your-project.side
    

_注意：如果您有多个`.side`文件，则可以使用通配符（例如`/path/to/*.side`）。_

当您运行此命令时，它将在多个浏览器窗口中并行启动测试，并跨`n`进程分布（这`n`是计算机上可用CPU内核的数量）。

进程数可以在运行时通过可提供的各种参数进行配置（除其他外）。

**注意：并行执行在套件级别自动发生。如果要并行执行套件中的测试，则需要更改一个设置。有关详细信息，请参见[套件中的测试并行化](#test-parallelization-in-a-suite)。**

[](#run-time-configuration)运行时配置
--------------------------------

使用运行程序，您可以在运行时传递不同的配置参数。

### [](#running-on-a-different-browser-locally)在本地不同的浏览器上运行

功能最常见的用途是为本地测试执行指定其他浏览器。

    selenium-side-runner -c "browserName=chrome"
    selenium-side-runner -c "browserName='internet explorer'"
    selenium-side-runner -c "browserName=edge"
    selenium-side-runner -c "browserName=firefox"
    selenium-side-runner -c "browserName=safari"
    

**注意：在本地运行测试时，每个浏览器都需要进行一些设置。有关详细信息，请参见[安装浏览器驱动程序](#installing-a-browser-driver)。**

### [](#running-on-selenium-grid)在Selenium Grid上运行

要在网格（例如，您自己的网格或诸如Sauce Labs的托管提供程序）上运行测试，可以指定它以及其他功能。

    selenium-side-runner --server http://localhost:4444/wd/hub -c "browserName='internet explorer' version='11.0' platform='Windows 8.1'"
    

`--server`指定网格的URL，并且`-c`是您希望网格使用的功能。

您可以[在此处查看](https://github.com/SeleniumHQ/selenium/wiki/DesiredCapabilities)可用功能的完整列表。

### [](#specify-the-number-of-parallel-processes)指定并行进程数

在网格上运行时，您可能需要控制正在运行的并行会话数。为此，您可以使用`-w n`命令标志（其中`n`是所需的进程数）。

    selenium-side-runner -w 10 --server http://localhost:4444/wd/hub
    

运行程序将自动将工作程序数量设置为计算机上可用的CPU核心数量。在大多数情况下，这是最佳选择。

### [](#chrome-specific-capabilities)Chrome特定功能

如果您将Chrome安装在计算机的非标准位置，则可以指定路径，以便ChromeDriver知道要查找的位置。

    selenium-side-runner -c "goog:chromeOptions.binary='/path/to/non-standard/Chrome/install'"
    

使用特定于Chrome的功能，您还可以轻松运行测试。

    selenium-side-runner -c "goog:chromeOptions.args=[disable-infobars, headless]"
    

[](#a-framework-at-your-fingertips)触手可及的框架
------------------------------------------

runner还提供其他一些便利。您期望在传统的测试自动化框架中可以使用的东西。

### [](#change-the-base-url)更改基本URL

通过指定其他基本URL的能力，您可以轻松地将测试指向不同的环境（例如，本地开发，测试，登台，生产）。

    selenium-side-runner --base-url https://localhost
    

### [](#filter-tests)筛选测试

您还可以选择使用`--filter target`命令标志（其中`target`是正则表达式值）运行测试的目标子集。包含给定搜索条件的测试名称将是唯一运行的测试名称。

    selenium-side-runner --filter smoke
    

### [](#output-test-results-to-a-file)将测试结果输出到文件

如果需要将测试结果导出到文件中（例如，作为CI进程的一部分运行时），则可以使用`--output-directory`和`--output-format`标志的组合。

`--output-directory`定义放置测试结果文件的位置。它可以采用绝对路径或相对路径。

`--output-format`定义用于测试结果文件的格式。它可以是`jest`（例如，JSON）或`junit`（例如，XML）。默认格式为`jest`（例如，如果您未指定类型）。

    selenium-side-runner --output-directory=results
    # Outputs results in `jest` frormat in `./results/projectName.json'
    

    selenium-side-runner --output-directory=results --output-format=jest
    # Outputs results in `jest` frormat in `./results/projectName.json'
    

    selenium-side-runner --output-directory=results --output-format=junit
    # Outputs results in `junit` frormat in `./results/projectName.xml'
    

### [](#specify-a-default-configuration)指定默认配置

您不必记住所有需要的命令行参数（这些参数可能很笨拙），而是可以将运行时参数存储在配置文件中。

您可以使用两种配置文件。

#### [](#option-1)选项1

`.side.yml`在将要运行测试的目录中创建一个文件。跑步者将自动捡起它。这是文件内容的示例。

    capabilities:
      browserName: "firefox"
    baseUrl: "https://www.seleniumhq.org"
    server: "http://localhost:4444/wd/hub"
    

如果要忽略文件并改用命令行参数，`--no-sideyml`请在运行时与其他命令一起使用。

#### [](#option-2)选项2

除了使用`.side.yml`文件之外，您还可以在YAML文件中使用您选择的名称和位置指定运行时参数，然后在运行测试时指定其位置。

    selenium-side-runner --config-file "/path/to/your/config.yaml"
    

**注意：使用`--config-file`标志时，`.side.yml`将被忽略。**

[](#selenium-ide-configuration)Selenium IDE配置
---------------------------------------------

### [](#test-parallelization-in-a-suite)在套件中测试并行化

开箱即用，跑步者并行执行套件，但是套件中的测试是顺序执行的。

要在给定套件中并行运行测试，您需要在Selenium IDE中更新该套件的设置。

1.  切换到`Test Suites`Selenium IDE中的视图
2.  点击您要配置的套件名称旁边的下拉菜单，然后点击 `Settings`
3.  单击复选框 `Run in parallel`
4.  请点击 `Submit`
5.  保存您的Selenium IDE项目文件

要配置多个套件以这种方式运行，请在每个套件中重复步骤1-4。完成后，请确保保存项目文件。

[](#advanced-options)高级选项
-------------------------

### [](#additional-params)其他参数

Selenium IDE的插件可以指定自己的唯一运行时参数。您可以通过`--params`标志使用它们。

此选项采用各种选项的字符串（类似于您指定功能的方式）。

#### [](#basic-usage)基本用法

您指定参数的名称及其值。最基本的方法是指定一个字符串值。

    selenium-side-runner --params "a='example-value'"
    

#### [](#nested-parameters)嵌套参数

也可以使用点符号嵌套参数。

    selenium-side-runner --params "a.b='another example-value'"
    

#### [](#array-values)数组值

除了字符串，还可以指定字母数字值的数组。

    selenium-side-runner --params "a.b.c=[1,2,3]"
    

#### [](#multiple-parameters)多个参数

`--params` 只能被调用一次，但是您可以通过空格分隔来指定多个参数。

    selenium-side-runner --params "a='example-value' a.b='another example-value' a.b.c=[1,2,3]"
    

### [](#using-a-proxy-server)使用代理服务器

您可以使用运行程序中的以下选项将代理功能传递给浏览器。

#### [](#direct-proxy)直接代理

此选项将WebDriver配置为绕过所有浏览器代理。

##### [](#from-the-command-line)在命令行中：

    > selenium-side-runner --proxy-type=direct
    

##### [](#in-sideyaml)在`.side.yaml`：

    proxyType: direct
    

#### [](#manual-proxy)手动代理

手动配置浏览器代理。

##### [](#from-the-command-line-1)在命令行中：

    selenium-side-runner --proxy-type=manual --proxy-options="http=localhost:434 bypass=[http://localhost:434, http://localhost:8080]"
    

##### [](#in-sideyaml-1)在`.side.yaml`：

    proxyType: manual
    proxyOptions:
      http: http://localhost:434
      https: http://localhost:434
      ftp: http://localhost:434
      bypass:
        - http://localhost:8080
        - http://host:434
        - http://somethingelse:32
    

#### [](#pac-proxy)PAC代理

配置WebDriver以使用给定URL处的PAC文件设置浏览器代理。

##### [](#from-the-command-line-2)在命令行中：

    selenium-side-runner --proxy-type=pac --proxy-options="http://localhost/pac"
    

##### [](#in-sideyaml-2)在`.side.yaml`：

    proxyType: pac
    proxyOptions: http://localhost/pac
    

#### [](#socks-proxy)SOCKS 代理

为SOCKS代理创建代理配置。

##### [](#from-the-command-line-3)在命令行中：

    selenium-side-runner --proxy-type=socks --proxy-options="socksProxy=localhost:434 socksVersion=5"
    

##### [](#in-sideyaml-3)在`.side.yaml`：

    proxyType: socks
    proxyOptions:
      socksProxy: localhost:434
      socksVersion: 5
    

#### [](#system-proxy)系统代理

配置WebDriver以使用当前系统的代理。

##### [](#from-the-command-line-4)在命令行中：

    selenium-side-runner --proxy-type=system
    

##### [](#in-sideyaml-4)在`.side.yaml`：

    proxyType: system
    

### [](#code-export)代码导出

如果您想学习如何将记录的测试转换为WebDriver代码，或者想要将记录的测试集成到现有的自定义测试框架中，则需要的是代码导出，现在可用于某些语言。您可以[在此处](/archives/selenium-ide-code-export)了解更多[信息](/archives/selenium-ide-code-export)！