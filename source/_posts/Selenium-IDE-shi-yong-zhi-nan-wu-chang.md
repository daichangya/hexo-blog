---
title: Selenium IDE使用指南五（常见问题）
id: 1402
date: 2024-10-31 22:01:53
author: daichangya
excerpt: 如何记录悬停？鼠标悬停（aka悬停）操作很难作为记录周期的一部分自动捕获。要在您的测试中添加鼠标悬停，需要进行一些手动干预。您可以通过两种不同的方式来做到这一点。选项1：在录制时添加录制时，右键单击要悬停的元素在出现的菜单中，单击SeleniumIDE，然后MouseOver确认MouseOver测
permalink: /archives/Selenium-IDE-shi-yong-zhi-nan-wu-chang/
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

### [](#how-do-i-record-hovers)如何记录悬停？

鼠标悬停（aka悬停）操作很难作为记录周期的一部分自动捕获。

要在您的测试中添加鼠标悬停，需要进行一些手动干预。您可以通过两种不同的方式来做到这一点。

_选项1：在录制时添加_

1.  录制时，右键单击要悬停的元素
2.  在出现的菜单中，单击`Selenium IDE`，然后`Mouse Over`
3.  确认`Mouse Over`测试步骤在测试中的正确位置（如果需要，将其拖放到其他位置）

_选项2：在测试编辑器中手动添加_

1.  右键单击IDE中的测试步骤
2.  选择 `Insert new command`
3.  输入`mouse over`到`Command`输入字段
4.  在`Target`输入字段中输入要悬停的定位器（或单击`Select target in page`并选择要悬停的元素）

### [](#why-don-t-numbers-that-are-typed-into-a-date-input-field-appear-correctly)为什么在日期输入字段中键入的数字不能正确显示？

通过Selenium IDE的命令行运行器运行测试时，会出现此问题。

要绕开它，您将需要启用w3c模式，您可以通过`-c "chromeOptions.w3c=true"`在启动运行程序时传递来进行此操作。

启用w3c模式会影响Selenium Actions的性能（如果您的测试最终使用它们）是毫无价值的，因此仅当日期输入字段存在问题时才使用此模式。

### [](#how-do-i-get-the-ide-to-wait-for-a-certain-condition-to-be-true-before-proceeding)我如何让IDE等待特定条件成立才能继续进行？

在某些情况下，IDE中的内置等待策略还不够。发生这种情况时，可以使用可用的显式等待命令之一。

*   `wait for element editable`
*   `wait for element present`
*   `wait for element visible`
*   `wait for element not editable`
*   `wait for element not present`
*   `wait for element not visible`

### [](#how-can-i-use-regex-in-text-verifications)如何在文本验证中使用正则表达式？

这是我们最终将要添加的功能（[有关详细信息，](https://github.com/SeleniumHQ/selenium-ide/issues/141)请参阅[问题141](https://github.com/SeleniumHQ/selenium-ide/issues/141)）。解决方法是，可以将XPath定位器与`starts-with`和`contains`关键字一起使用。
```
command	assertElementPresent
target	//a@[starts-with(.,'you are the') and contains(.,'User to log in today')]
```
### [](#how-do-i-scroll)我如何滚动？

Selenium IDE中没有用于滚动的独特命令，因为Selenium中没有实现任何命令。相反，您可以使用`scrollTo`JavaScript中的命令通过指定`x`和`y`滚动到所需坐标来完成此任务。
```
command	executeScript
target	window.scrollTo(0,1000)
```
### [](#saving-files)保存文件

#### [](#why-is-the-location-i-saved-my-side-project-to-not-remembered)为什么我保存SIDE项目的位置不记得了？

#### [](#why-do-i-need-to-step-through-a-save-as-flow-everytime-i-want-to-save-my-project)为什么每次要保存项目时都需要逐步执行“另存为”流程？

#### [](#why-do-i-need-to-overwrite-a-previously-saved-file)为什么需要覆盖以前保存的文件？

所有这些问题都是同一个问题的一部分-因为浏览器扩展Selenium IDE不能访问文件系统。提供“保存”功能的唯一方法是通过下载文件。当IDE移至本机应用程序时，将解决此问题。这将使IDE具有首要的文件系统访问权限，从而使它能够提供优美的“保存”体验。

如果要保持更新，可以按照[问题363进行操作](https://github.com/SeleniumHQ/selenium-ide/issues/363)。

### [](#how-to-install-the-ide-behind-strict-proxy-firewall)如何在严格的代理/防火墙后面安装IDE？

在某些情况下，您可能没有完全的公共Internet访问权限（例如，在“公司代理或防火墙”后面）。在这些环境中，您将需要获取内置的Selenium IDE ZIP文件的副本，以便记录自动测试脚本。可以在GitHub的“发布”部分中找到：

[https://github.com/SeleniumHQ/selenium-ide/releases](https://github.com/SeleniumHQ/selenium-ide/releases)

并非所有版本都包含“ selenium-ide.zip”，因为其中一些仅仅是“源代码”版本。查找具有此zip文件的最新版本。这意味着它是提交给Chrome和Firefox商店的最新版本。

#### [](#officially-signed-versions)正式签署的版本

从项目发行页面下载zip文件可为您提供未签名的ZIP文件。或者，您可以从以下位置获取经过正式签名的安装程序，这些安装程序可以在“安全环境”中更好地发挥作用：

*   [Firefox附加组件](https://addons.mozilla.org/en-US/firefox/addon/selenium-ide/)
*   [所需的“ .xpi”安装程序的下载说明](https://superuser.com/questions/646856/how-to-save-firefox-addons-for-offline-installation)

**注意：如果您已经安装了插件（例如，在便携式计算机上尝试获取安装程序的副本），则在尝试访问它们时只会看到“删除”按钮。因此，将它们删除一次，让安装程序移至另一台未连接的计算机，然后根据需要在主设备的浏览器中重新安装。**

*   [Chrome商店](https://chrome.google.com/webstore/detail/selenium-ide/mooikfkahbdckldjjndioackbalphokd)
*   [所需的“ .crx”安装程序的下载说明](https://stackoverflow.com/questions/25480912/how-to-download-a-chrome-extension-without-installing-it)

**注意：您不能直接从Chrome商店中获取“ .crx”文件。相反，您需要在本地安装一次，然后转到计算机上的安装目录以进行检索。**

### [](#why-does-no-save-dialog-appear-once-a-plugin-is-attached)附加了插件后，为什么没有保存对话框出现？

由于当前的[Chrome错误](https://bugs.chromium.org/p/chromium/issues/detail?id=922373)，如果您不答复Selenium IDE发出的消息，则不会进行进一步处理。为了解决此问题，请确保侦听`emit`该实体的操作`project`并使用进行回复`undefined`：

    chrome.runtime.onMessageExternal.addListener((message, sender, sendResponse) => {
      if (message.action === "emit" && message.entity === "project") {
        sendResponse(undefined);
      }
    });