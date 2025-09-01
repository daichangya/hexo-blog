---
title: chrome插件开发入门指南
id: 1377
date: 2024-10-31 22:01:52
author: daichangya
excerpt: 什么是扩展插件？扩展插件是可以定制浏览体验的小型软件程序。它们使用户可以根据个人需要或偏好来定制Chrome功能和行为。它们基于Web技术（例如HTML，JavaScript和CSS）构建。扩展必须满足狭义定义且易于理解的单一目的。一个扩展可以包含多个组件和一系列功能，只要所有内容都有助于实现共同的
permalink: /archives/chrome-cha-jian-kai-fa-ru-men-zhi-nan/
categories:
- chrome
---

什么是扩展插件？
=======

扩展插件是可以定制浏览体验的小型软件程序。它们使用户可以根据个人需要或偏好来定制Chrome功能和行为。它们基于Web技术（例如HTML，JavaScript和CSS）构建。

扩展必须满足 狭义定义且易于理解的 [单一目的](single_purpose)。一个扩展可以包含多个组件和一系列功能，只要所有内容都有助于实现共同的目标。

用户界面应最少且具有意图。它们的范围从简单的图标到[覆盖](override)整个页面。

扩展文件被压缩到`.crx`用户下载并安装的单个程序包中。这意味着扩展与普通的Web应用程序不同，它不依赖于Web上的内容。

扩展程序通过 [Chrome开发人员信息中心](https://chrome.google.com/webstore/developer/dashboard)分发， 并发布到 [Chrome网上应用店](http://chrome.google.com/webstore)。有关更多信息，请参阅 [商店开发人员文档](http://code.google.com/chrome/webstore)。

你好插件
----

通过此快速的Hello扩展示例，对扩展进行一小步。首先创建一个新目录来存储扩展的文件，或者从[示例页面](/extensions/samples#search:hello)下载它们 。

接下来，添加一个名为的文件，`manifest.json` 并包含以下代码：

```
{
  "name": "Hello Extensions",
  "description" : "Base Level Extension",
  "version": "1.0",
  "manifest_version": 2
}
```

每个扩展都需要一个清单，尽管大多数扩展仅对清单没有多大作用。为了快速入门，扩展程序在该[`browser_action`](browserAction)字段下声明了一个弹出文件和图标 ：

```
{
  "name": "Hello Extensions",
  "description" : "Base Level Extension",
  "version": "1.0",
  "manifest_version": 2,
  "browser_action": {
    "default_popup": "hello.html",
    "default_icon": "hello_extensions.png"
  }
}
```

[在此处](/static/images/index/hello_extensions.png) 下载 ，然后创建一个名为的文件： [`hello_extensions.png`](/static/images/index/hello_extensions.png)`hello.html`

```
<html>
<body>
<h1>Hello Extensions</h1>
</body>
</html>
```

现在`hello.html`，单击该图标时将显示扩展名。下一步是在中包含`manifest.json`启用键盘快捷键的命令。此步骤很有趣，但不是必需的：

```
{
  "name": "Hello Extensions",
  "description" : "Base Level Extension",
  "version": "1.0",
  "manifest_version": 2,
  "browser_action": {
    "default_popup": "hello.html",
    "default_icon": "hello_extensions.png"
  },
  "commands": {
    "_execute_browser_action": {
      "suggested_key": {
        "default": "Ctrl+Shift+F",
        "mac": "MacCtrl+Shift+F"
      },
      "description": "Opens hello.html"
    }
  }

}
```

最后一步是在您的本地计算机上安装扩展。

1.  `chrome://extensions`在浏览器中导航到。您还可以通过点击多功能框右上角的Chrome菜单，将鼠标悬停在“ **更多工具”上，**然后选择**扩展程序**来访问此页面。
2.  选中“ **开发人员模式** ”旁边的框。
3.  单击“ **加载解压缩的扩展名”，**然后为“ Hello扩展名”扩展名选择目录。

恭喜你！现在，您可以通过单击`hello_world.png`图标或按 `Ctrl+Shift+F`键盘来使用基于弹出窗口的扩展名。

接下来是什么？
-------

1.  遵循[入门教程](getstarted)
2.  阅读 [概述](overview)
3.  阅读[Chromium博客](http://blog.chromium.org/)以了解最新信息[](http://blog.chromium.org/)
4.  订阅 [铬扩展组](http://groups.google.com/a/chromium.org/group/chromium-extensions)

精选视频
----

[技术视频](http://www.youtube.com/view_play_list?p=CA101D6A85FE9D4B)  
[开发人员快照](http://www.youtube.com/view_play_list?p=38DF05697DE372B1)

根据[CC-By 3.0许可提供的内容](http://creativecommons.org/licenses/by/3.0/)