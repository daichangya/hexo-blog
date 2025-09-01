---
title: chrome插件调试
id: 1379
date: 2024-10-31 22:01:52
author: daichangya
excerpt: 内容＃找到日志后台脚本弹出内容脚本扩展标签监控网络请求声明权限下一步重要提示：Chrome将删除所有平台上对Chrome应用的支持。Chrome浏览器和Chrome网上应用店将继续支持扩展程序。阅读公告，并了解有关迁移应用程序的更多信息。调试扩展扩展程序可以利用ChromeDevTools为网页提供
permalink: /archives/chrome-cha-jian-diao-shi/
categories:
- chrome
---

[TOC]

**重要提示：** Chrome将删除所有平台上对Chrome应用的支持。Chrome浏览器和Chrome网上应用店将继续支持扩展程序。 [**阅读公告，**](https://blog.chromium.org/2020/01/moving-forward-from-chrome-apps.html) 并了解有关[**迁移应用程序的**](https://developers.chrome.com/apps/migration)更多信息 。

调试扩展
====

扩展程序可以利用 [Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools/)为网页提供的相同调试 [优势](https://developers.google.com/web/tools/chrome-devtools/) ，但是它们具有独特的行为属性。成为主扩展调试器需要了解以下行为，扩展组件如何相互配合以及在哪里处理错误。本教程使开发人员对调试扩展有基本的了解。

找到日志
----------------------------

扩展由许多不同的组件组成，这些组件有各自的职责。[在此处](examples/tutorials/broken_background_color.zip)下载损坏的扩展程序 [，](examples/tutorials/broken_background_color.zip) 以开始查找不同扩展程序组件的错误日志。

### 后台脚本

导航至chrome扩展管理页面， `chrome://extensions`并确保已启用开发人员模式。单击**加载未打包的**按钮，然后选择损坏的扩展目录。扩展名加载后，它应具有三个按钮： **Details**，**Remove**和**Errors** in red letter。

![扩展管理页面上的图像显示错误按钮](https://developer.chrome.com/static/images/debugging/error_button.png)

单击**错误**按钮以查看错误日志。扩展程序系统在后台脚本中发现了一个问题。

`Uncaught TypeError: Cannot read property ‘addListener’ of undefined`

![扩展管理页面显示后台脚本错误](https://developer.chrome.com/static/images/debugging/background_error.png)

此外，通过选择**检查视图**旁边的蓝色链接，可以打开Chrome DevTools面板以显示背景脚本 。

![DevTools显示后台脚本错误](https://developer.chrome.com/static/images/debugging/inspect_views_background.png)

返回代码。

```
  chrome.runtime.oninstalled.addListener(function() {
    chrome.storage.sync.set({color: '#3aa757'}, function() {
      console.log('The color is green.');
    });
    chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
      chrome.declarativeContent.onPageChanged.addRules([{
        conditions: [new chrome.declarativeContent.PageStateMatcher({
          pageUrl: {hostEquals: 'developer.chrome.com'},
        })],
        actions: [new chrome.declarativeContent.ShowPageAction()]
      }]);
    });
  });
```              

后台脚本正在尝试侦听该 [`onInstalled`](extensions/runtime#event-onInstalled) 事件，但是属性名称要求使用大写字母“ I”。更新代码以反映正确的呼叫，单击右上角的**全部清除**按钮，然后重新加载该分机。

### 弹出

现在，该扩展名已正确初始化，可以测试其他组件了。刷新此页面，或打开一个新选项卡并导航到developer.chrome.com上的任何页面，打开弹出窗口并单击绿色方块。而且...什么都没发生。

导航回到“扩展管理页面”，“ **错误”**按钮重新出现。单击它以查看新日志。

`Uncaught ReferenceError: tabs is not defined`

![扩展管理页面显示弹出错误](https://developer.chrome.com/static/images/debugging/popup_error.png)

弹出错误也可以通过检查弹出窗口来查看。

![DevTools显示弹出错误](https://developer.chrome.com/static/images/debugging/inspect_popup.png)

错误`tabs is undefined`表示扩展名不知道将内容脚本注入哪里。可以通过调用[`tabs.query()`](/extensions/tabs#method-query) 方法，然后选择活动选项卡来更正此问题 。

```
  let changeColor = document.getElementById('changeColor');

  chrome.storage.sync.get('color', function(data) {
    changeColor.style.backgroundColor = data.color;
    changeColor.setAttribute('value', data.color);
  });

  changeColor.onclick = function(element) {
    let color = element.target.value;
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      chrome.tabs.executeScript(
          tabs[0].id,
          {code: 'document.body.style.backgroundColor = color;'});
    });
  };
```
更新代码，单击右上角的**全部清除**按钮，然后重新加载扩展。

### 内容脚本

刷新页面，打开弹出窗口，然后单击绿色框。而且...不，背景仍然没有变色！浏览回扩展管理页面，然后...没有**错误**按钮。可能的罪魁祸首是在网页内运行的内容脚本。

打开扩展正在尝试更改的网页的DevTools面板。

![网页控制台中显示的扩展错误](https://developer.chrome.com/static/images/debugging/content_script_error.png)

仅运行时错误，`console.warning` 并且`console.error`将记录在扩展管理页面上。

要从内容脚本中使用DevTools，请单击**顶部**旁边的下拉箭头，然后选择扩展名。

![未捕获的ReferenceError：未定义选项卡](https://developer.chrome.com/static/images/debugging/inspect_content_script.png)

错误消息`color`未定义。扩展名不能正确传递变量。更正注入的脚本以将color变量传递到代码中。

```
  {code: 'document.body.style.backgroundColor = "' + color + '";'});
```

### 扩展标签

可以在网页控制台和扩展管理页面中找到 显示为选项卡的扩展页面的日志，例如[替代页面](extensions/override)和 [整页选项](extensions/options#full_page)。

监控网络请求
-----------------------------------

弹出窗口通常会发出所有必需的网络请求，即使是最快的开发人员也可以打开DevTools。要查看这些请求，请从网络面板内部刷新。它将在不关闭DevTools面板的情况下重新加载弹出窗口。

![在网络面板内刷新以查看弹出的网络请求](https://developer.chrome.com/static/images/debugging/network_reload.gif)

声明权限
-----------------------------------

尽管扩展具有与网页相似的功能，但它们通常需要获得许可才能使用某些功能，例如[Cookie](/extensions/cookies)， [存储](/extensions/storage)和 [跨源XMLHttpRequsts](/extensions/xhr)。请参阅[权限文章](extensions/permission_warnings) 和可用的[Chrome API，](/extensions/api_index) 以确保扩展程序在其[清单中](/extensions/manifest)请求正确的权限 。

```
  {
    "name": "Broken Background Color",
    "version": "1.0",
    "description": "Fix an Extension!",
    "permissions": [
      "activeTab",
      "declarativeContent",
      "storage"
    ],
    "options_page": "options.html",
    "background": {
      "scripts": ["background.js"],
      "persistent": false
    },
    "page_action": {
      "default_popup": "popup.html",
      "default_icon": {
        "16": "images/get_started16.png",
        "32": "images/get_started32.png",
        "48": "images/get_started48.png",
        "128": "images/get_started128.png"
      }
    },
    "icons": {
      "16": "images/get_started16.png",
      "32": "images/get_started32.png",
      "48": "images/get_started48.png",
      "128": "images/get_started128.png"
    },
    "manifest_version": 2
  }
```