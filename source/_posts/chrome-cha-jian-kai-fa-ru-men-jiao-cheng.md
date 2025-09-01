---
title: chrome插件开发入门教程
id: 1378
date: 2024-10-31 22:01:52
author: daichangya
permalink: /archives/chrome-cha-jian-kai-fa-ru-men-jiao-cheng/
categories:
- chrome
---

### 内容[#](#contents "Permalink")

1.  [创建清单](#manifest)
2.  [添加指令](#background)
3.  [介绍用户界面](#user_interface)
4.  [层逻辑](#logic)
5.  [给用户选项](#options)
6.  [采取下一步](#next-steps)

入门教程
====

扩展由不同的但相互联系的组件组成。组件可以包括 [后台脚本](https://developer.chrome.com/background_pages.html)， [内容脚本](https://developer.chrome.com/content_scripts.html)，[选项页](https://developer.chrome.com/options)， [UI元素](https://developer.chrome.com/user_interface.html) 和各种逻辑文件。扩展组件是使用Web开发技术创建的：HTML，CSS和JavaScript。扩展的组件将取决于其功能，并且可能不需要所有选项。

本教程将构建一个扩展，允许用户更改[developer.chrome.com](https://developer.chrome.com/)上任何页面的背景颜色 。它将使用许多核心组件来介绍它们之间的关系。

首先，创建一个新目录来保存扩展名的文件。

完整的扩展程序可以在[此处](https://developer.chrome.com/extensions//tutorials/get_started_complete.zip)下载 。

创建清单[#](#manifest "Permalink")
------------------------------

扩展从[清单](extensions/manifest)开始。创建一个名为`manifest.json` 并包含以下代码的文件，或在[此处](https://developer.chrome.com/extensions//tutorials/get_started/manifest.json)下载该文件 。

```
{
    "name": "Getting Started Example",
    "version": "1.0",
    "description": "Build an Extension!",
    "manifest_version": 2
}
```

可以在当前状态下以开发人员模式将包含清单文件的目录添加为扩展名。

1.  通过导航到来打开“扩展管理”页面 `chrome://extensions`。
    *   也可以通过点击Chrome菜单，将鼠标悬停在“ **更多工具”上，** 然后选择**扩展程序**来打开“扩展程序管理”页面。
2.  通过单击“ **开发人员模式”**旁边的切换开关启用“开发**人员模式”**。
3.  单击**LOAD UNPACKED**按钮，然后选择扩展目录。

![负荷扩展](https://developer.chrome.com/static/images/get_started/load_extension.png)

- 该扩展程序已成功安装。由于清单中未包含任何图标，因此将为扩展名创建通用工具栏图标。

添加指令[#](#background "Permalink")
--------------------------------

尽管已安装扩展，但没有说明。 通过创建标题为的文件或[在此处](https://developer.chrome.com/extensions//tutorials/get_started/background.js)下载 ，然后将其放置在扩展目录中来引入[背景脚本](https://developer.chrome.com/background_pages.html)。 `background.js`[](https://developer.chrome.com/extensions//tutorials/get_started/background.js)

后台脚本和许多其他重要组件必须在清单中注册。在清单中注册后台脚本会告诉扩展名要引用的文件以及该文件的行为。

```
{
    "name": "Getting Started Example",
    "version": "1.0",
    "description": "Build an Extension!",
    "background": {
        "scripts": [
            "background.js"
        ],
        "persistent": false
    },
    "manifest_version": 2
}
```

现在，该扩展程序知道它包含一个非持久性后台脚本，并将扫描注册文件中需要侦听的重要事件。

此扩展在安装后将需要来自持久变量的信息。首先[`runtime.onInstalled`](https://developer.chrome.com/runtime#event-onInstalled) 在后台脚本中包含一个监听事件 。在`onInstalled`侦听器内部，扩展将使用[存储](https://developer.chrome.com/storage) API 设置一个值 。这将允许多个扩展组件访问该值并进行更新。

```
chrome.runtime.onInstalled.addListener(function() {
	chrome.storage.sync.set({color: '#3aa757'}, function () {
		console.log('The color is green.');
	});
}
```

大多数API（包括[存储](https://developer.chrome.com/storage) API）都必须`"permissions"`在清单中的字段下注册，以便扩展程序使用它们。

```
  {
    "name": "Getting Started Example",
    "version": "1.0",
    "description": "Build an Extension!",
    "permissions": ["storage"],
    "background": {
      "scripts": ["background.js"],
      "persistent": false
    },
    "manifest_version": 2
  }
```

浏览回到扩展管理页面，然后单击“ **重新加载”**链接。带有蓝色链接**背景页面**的新字段“ **检查视图”**可用。

![检查视图](https://developer.chrome.com/static/images/get_started/view_background.png)

点击链接以查看后台脚本的控制台日志“ `The color is green.`”

介绍用户界面[#](#user_interface "Permalink")
--------------------------------------

扩展可以具有多种形式的[用户界面](https://developer.chrome.com/user_interface)，但是这种形式 将使用 [弹出窗口](https://developer.chrome.com/user_interface#popup)。创建并添加标题`popup.html`为目录的文件，或[在此处](https://developer.chrome.com/extensions//tutorials/get_started/popup.html)下载 。此扩展程序使用按钮来更改背景颜色。

```
  <!DOCTYPE html>
  <html>
    <head>
      <style>
        button {
          height: 30px;
          width: 30px;
          outline: none;
        }
      </style>
    </head>
    <body>
      <button id="changeColor"></button>
    </body>
  </html>
```

与后台脚本一样，该文件需要在清单下的清单中指定为弹出窗口 [`page_action`](https://developer.chrome.com/pageAction)。

```
  {
    "name": "Getting Started Example",
    "version": "1.0",
    "description": "Build an Extension!",
    "permissions": ["storage"],
    "background": {
      "scripts": ["background.js"],
      "persistent": false
    },
    "page_action": {
      "default_popup": "popup.html"
    },
    "manifest_version": 2
  }
```

工具栏图标的名称也包含`page_action` 在该`default_icons`字段下。在 [此处](https://developer.chrome.com/extensions//tutorials/get_started/images.zip)下载images文件夹 ，将其解压缩，并将其放置在扩展程序的目录中。更新清单，以便扩展程序知道如何使用图像。

```
  {
    "name": "Getting Started Example",
    "version": "1.0",
    "description": "Build an Extension!",
    "permissions": ["storage"],
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
    "manifest_version": 2
  }
```

扩展程序还会在扩展程序管理页面上显示图像，权限警告和网站图标。这些图像在清单中的下方指定 [`icons`](https://developer.chrome.com/user_interface#icons)。

```
  {
    "name": "Getting Started Example",
    "version": "1.0",
    "description": "Build an Extension!",
    "permissions": ["storage"],
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
如果在此阶段重新加载扩展，它将包含一个灰度图标，但不会包含任何功能差异。由于`page_action`是在清单中声明的​​，因此取决于扩展名来告知浏览器用户何时可以与进行交互`popup.html`。

使用侦听器事件中的[`declarativeContent`](https://developer.chrome.com/declarativeContent) API 将声明的规则添加到后台脚本 `runtime.onInstalled`。

```
  chrome.runtime.onInstalled.addListener(function() {
    chrome.storage.sync.set({color: '#3aa757'}, function() {
      console.log('The color is green.');
    });
    chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
      chrome.declarativeContent.onPageChanged.addRules([{
        conditions: [new chrome.declarativeContent.PageStateMatcher({
          pageUrl: {hostEquals: 'developer.chrome.com'},
        })
        ],
            actions: [new chrome.declarativeContent.ShowPageAction()]
      }]);
    });
  });
```

该扩展将需要权限才能访问[`declarativeContent`](https://developer.chrome.com/declarativeContent)其清单中的 API。

```
  {
    "name": "Getting Started Example",
  ...
    "permissions": ["declarativeContent", "storage"],
  ...
  }
```

![弹出](https://developer.chrome.com/static/images/get_started/popup_grey.png)

现在，当用户导航到包含的URL时，浏览器将在浏览器工具栏中显示一个全彩的页面操作图标 `"developer.chrome.com"`。该图标为全色时，用户可以单击它以查看popup.html。

弹出界面的最后一步是为按钮添加颜色。创建一个名为`popup.js`以下文件的文件并将其添加 到扩展目录，或[在此处](https://developer.chrome.com/extensions//tutorials/get_started/popup.js)下载 。

```
  let changeColor = document.getElementById('changeColor');

  chrome.storage.sync.get('color', function(data) {
    changeColor.style.backgroundColor = data.color;
    changeColor.setAttribute('value', data.color);
  });
```

此代码从中获取按钮`popup.html` 并从存储中请求颜色值。然后，它将颜色用作按钮的背景。包括脚本标记`popup.js`在`popup.html`。

```
<!DOCTYPE html>
<html>
...
  <body>
    <button id="changeColor"></button>
    <script src="popup.js"></script>
  </body>
</html>
```

重新加载扩展以查看绿色按钮。

层逻辑[#](#logic "Permalink")
--------------------------

现在，该扩展程序知道该弹出窗口对[developer.chrome.com](https://developer.chrome.com/)上的用户应该可用， 并显示一个彩色按钮，但是需要逻辑来进行进一步的用户交互。更新`popup.js`以包括以下代码。

```
  let changeColor = document.getElementById('changeColor');
  ...
  changeColor.onclick = function(element) {
    let color = element.target.value;
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      chrome.tabs.executeScript(
          tabs[0].id,
          {code: 'document.body.style.backgroundColor = "' + color + '";'});
    });
  };
```
更新的代码在按钮上添加了onclick事件，该事件触发了以 [编程方式注入的内容脚本](https://developer.chrome.com/content_scripts#pi)。这会将页面的背景色变成与按钮相同的颜色。使用程序注入可以允许用户调用内容脚本，而不是将不需要的代码自动插入网页中。

清单将需要[`activeTab`](activeTab) 许可权，以允许扩展程序临时访问 [`tabs`](https://developer.chrome.com/tabs)API。这使分机可以进行呼叫 [`tabs.executeScript`](https://developer.chrome.com/tabs#method-executeScript)。

```
  {
    "name": "Getting Started Example",
  ...
    "permissions": ["activeTab", "declarativeContent", "storage"],
  ...
  }
```

该扩展程序现在可以正常使用了！重新加载扩展程序，刷新此页面，打开弹出窗口，然后单击按钮将其变为绿色！但是，某些用户可能希望将背景更改为其他颜色。

给用户选项[#](#options "Permalink")
------------------------------

该扩展程序当前仅允许用户将背景更改为绿色。包括一个选项页面使用户可以更好地控制扩展功能，从而进一步自定义其浏览体验。

首先在名为的目录中创建一个文件，`options.html` 并包含以下代码，或[在此处](https://developer.chrome.com/extensions//tutorials/get_started/options.html)下载 。

```
  <!DOCTYPE html>
  <html>
    <head>
      <style>
        button {
          height: 30px;
          width: 30px;
          outline: none;
          margin: 10px;
        }
      </style>
    </head>
    <body>
      <div id="buttonDiv">
      </div>
      <div>
        <p>Choose a different background color!</p>
      </div>
    </body>
    <script src="options.js"></script>
  </html>
```
然后在清单中注册选项页面，

```
  {
    "name": "Getting Started Example",
    ...
    "options_page": "options.html",
    ...
    "manifest_version": 2
  }
```

重新加载扩展，然后单击**DETAILS**。

![检查视图](https://developer.chrome.com/static/images/get_started/click_details.png)

向下滚动详细信息页面，然后选择**扩展选项** 以查看选项页面，尽管该页面当前将显示为空白。

![检查视图](https://developer.chrome.com/static/images/get_started/options.png)

最后一步是添加选项逻辑。`options.js`使用以下代码在扩展目录中创建一个名为的文件，或[在此处](https://developer.chrome.com/extensions//tutorials/get_started/options.js)下载 。

```
  let page = document.getElementById('buttonDiv');
  const kButtonColors = ['#3aa757', '#e8453c', '#f9bb2d', '#4688f1'];
  function constructOptions(kButtonColors) {
    for (let item of kButtonColors) {
      let button = document.createElement('button');
      button.style.backgroundColor = item;
      button.addEventListener('click', function() {
        chrome.storage.sync.set({color: item}, function() {
          console.log('color is ' + item);
        })
      });
      page.appendChild(button);
    }
  }
  constructOptions(kButtonColors);
```
提供了四个颜色选项，然后使用onclick事件侦听器将它们生成为选项页面上的按钮。用户单击按钮时，它将更新扩展程序全局存储中的颜色值。由于所有扩展名文件均从全局存储中提取颜色信息，因此无需更新其他值。



恭喜你！该目录现在包含一个功能齐全的Chrome扩展程序，尽管过于简单。
