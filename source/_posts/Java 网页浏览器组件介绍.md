---
title: Java 网页浏览器组件介绍
id: 511
date: 2024-10-31 22:01:44
author: daichangya
excerpt: "简介： 使用 Java 开发客户端应用有时会需要使用到浏览器组件，本文将介绍在 Java 用户界面中使用浏览器的四种方法，并且比较它们各自的优点与不足，便于 Java 开发者在实际开发过程中选择。"
permalink: /archives/11909555/
categories:
 - java
---


## 前言

在使用 Java 开发客户端程序时，有时会需要在界面中使用网页浏览器组件，用来显示一段 HTML 或者一个特定的网址。本文将介绍在界面中使用浏览器组件的四种方法，给出示例的代码，并且分析每种方法的优点与不足，便于 Java 开发者在实际开发过程中根据自己的需要来选择。

## JDK 中的实现 - JEditorPane

Swing 是一个用于开发 Java 应用程序图形化用户界面的工具包，它是以抽象窗口工具包（AWT）为基础使跨平台应用程序可以使用任何可插拔的外观风格，而且它是轻量级（light-weight）组件，没有本地代码，不依赖于操作系统的支持，这是它与 AWT 组件的最大的区别。

在 Swing 中，有一个组件是 JEditorPane，它是一个可以编辑任意内容的文本组件。这个类使用了 EditorKit 来实现其操作，对于给予它的各种内容，它能有效地将其类型变换为适当的文本编辑器种类。该编辑器在任意给定时间的内容类型由当前已经安装的 EditorKit 来确定。

默认情况下，JEditorPane 支持以下的内容类型：

*   text/plain
    
    纯文本的内容，在此情况下使用的工具包是 DefaultEditorKit 的扩展，可生成有换行的纯文本视图。
    
*   text/html
    
    HTML 文本，在此情况下使用的工具包是 javax.swing.text.html.HTMLEditorKit，它支持 HTML3.2。
    
*   text/rtf
    
    RTF 文本，在此情况下使用的工具包是类 javax.swing.text.rtf.RTFEditorKit，它提供了对多样化文本格式（Rich Text Format）的有限支持。
    

### JEditorPane 的常用方法

*   `JEditorPane()`
    
    创建一个新的 JEditorPane 对象
    
*   `JEditorPane(String url)`
    
    根据包含 URL 规范的字符串创建一个 JEditorPane
    
*   `JEditorPane(String type,String text)`
    
    创建一个已初始化为给定文件的 JEdiorPane
    
*   `JEditorPane(URL initialPage)`
    
    根据输入指定的 URL 来创建一个 JEditorPane
    
*   `scrollToReference(String reference)`
    
    将视图滚动到给定的参考位置（也就是正在显示的 URL 的 URL.getRef 方法所返回的值）
    
*   `setContentType(String type)`
    
    设置此编辑器所处理的内容类型
    
*   `setEditorKit(EditorKit kit)`
    
    设置当前为处理内容而安装的工具包
    
*   `setPage(String url)`
    
    设置当前要显示的 URL, 参数是一个 String
    
*   `setPage(URL page)`
    
    设置当前要显示的 URL, 参数是一个 java.net.URL 对象
    
*   `setText(String t)`
    
    将此 TextComponent 的文本设置为指定内容，预期以此编辑器的内容类型格式提供该内容
    

### JEditorPane 显示网页

要使用 JEditorPane 来显示 HTML，需要完成以下几个步骤：

*   创建一个 JEditorPane 对象
    
    ```
    private JEditorPane jep=new JEditorPane();
    ```
    
*   设置 JEditorPane 显示的内容为 text/html
    
    ```
    jep.setContentType("text/html");
    ```
    
*   设置它不可编辑
    
    ```
    jep.setEditable(false);
    ```
    
*   处理超链接事件
    
    ```
    jep.addHyperlinkListener(this);
    ```
    

JEditorPane 需要注册一个 HyperlinkListener 对象来处理超链接事件，这个接口定义了一个方法 `hyperlinkUpdate(HyperlinkEvent e)`，示例代码如下：

```
public void hyperlinkUpdate(HyperlinkEvent event)
{
    if(event.getEventType() == HyperlinkEvent.EventType.ACTIVATED)
    {
        try
        {
            jep.setPage(event.getURL());
        }
        catch(IOException ioe)
        {
            ioe.printStackTrace();
        }
    }       
}
```

完整的代码可以在本文中 [下载](#artdownload) 到。在这个例子中，实现了一个 HyperlinkListener 接口，在方法实现中，

```
if(event.getEventType()==HyperlinkEvent.EventType.ACTIVATED)
```

这行代码表示首先判断 HyperlinkListener 的类型，在这里只处理事件类型为 `HyperlinkEvent.EventType.ACTIVATED` 的事件（即点击了某个超链接的事件），然后通过调用 HyperlinkEvent 的 getURL() 方法来获取超链接的 URL 地址。

最后通过调用 jep.setPage(event.getURL()) 方法，使得 JEditorPane 显示新的 URL 地址。

### JEditorPane 优缺点

由于 JEditorPane 是包含在 J2SE 中的 Swing 中，所以不需要导入第三方的 jar 文件，相对来说比较简单。但是 JEditorPane 类对于网页中的 CSS 的显示处理以及对 JavaScript 脚本执行的支持很弱，而且官方似乎也没有对 JEditorPane 类进行改进的打算，如果想用 JEditorPane 来显示常见的网址，会发现显示出来的页面与 IE,Firefox 有很大的差别，而且不能正常地处理页面逻辑。所以如果仅仅用来显示比较简单的 HTML, 用 JEditorPane 还是一个不错的选择。

## 开源的 Java Web 浏览器实现 - Lobo

Lobo 项目是一个第三方的开源 Java 浏览器项目，它的官方网站是 [http://lobobrowser.org/java-browser.jsp](http://lobobrowser.org/java-browser.jsp)。 它是使用 100%Java 代码实现的，而且能完整地支持 HTML4、JavaScript 以及 CSS2，除此之外，它还支持直接的 JavaFX 渲染。

Lobo 本身就已经是一个完整的浏览器软件，同时它还提供了很多与网页浏览器相关的 API，便于 Java 程序员在自己的代码中使用或者进行扩展，其中包括渲染引擎 API、浏览器 API 以及插件系统 API 等等。具体的功能可以在它的官方网站上查看。

### Lobo 中的 FramePanel

Lobo 中实现 Web 浏览器的类叫 FramePanel，它提供了对 HTML 页面显示的封装，并且提供了一些辅助的方法。下面是一些常见方法的介绍：

*   `FramePanel()`
    
    创建一个单独的 FramePanel 对象，它能被添加到任意的 Swing 窗口或者组件上。
    
*   `boolean back()`
    
    浏览器返回上一个页面
    
*   `boolean alert(String message)`
    
    打开一个提示对话框，并且显示消息
    
*   `boolean forward()`
    
    浏览器进入下一个界面
    
*   `boolean confirm(String message)`
    
    打开一个确认对话框，显示特定的消息
    
*   `void navigate(String url)`
    
    在这个组件里面显示特定的网址，参数一个网址的 String
    
*   `void reload()`
    
    重新加载当前的界面
    
*   `addContentListener(ContentListener listener)`
    
    添加一个内容变化的监听器
    
*   `addNavigationListener(NavigationListener listener)`
    
    添加一个导航（所显示的 URL 变化）的监听器
    
*   `addResponseListener(ResponseListener listener)`
    
    添加一个获取服务器返回结果的监听器
    

### 使用 FramePanel

要想使用 FramePanel，首先需要在它的官方网站上面下载它的安装包，然后在安装目录下，可以看到有 lobo.jar 以及 lobo-pub.jar，将这两个 jar 文件添加到 classpath 中。类似于 JEditorPane, 要使用 FramePanel 有以下的步骤：

*   创建一个 FramePanel 的对象
    
    ```
    FramePanel browser=new FramePanel();
    ```
    
*   将这个对象添加到界面上。Frame 是继承自 JPanel, 所以可以像其他 Swing 组件一样地添加到 JPanel 或者窗口上面。
*   通过调用 FramePanel.navigate(url) 的方法来设置要显示的网址。
*   不同于 JEditorPane，FramePanel 已经默认处理了点击超链接的事件，不需要另外手动地编写代码来处理。

### Lobo 浏览器 API 的优缺点

首先 Lobo 的 FramePanel 是 100% 纯 Java 的实现，具有良好的可移植性，在 Window/Linux 平台下都能正常地运行。它相比于 Swing 中的 JEditorPane，对于 HTML、CSS 的显示以及对于 JavaScript 的执行都有了比较大的提高。经过实际的使用测试，在访问大多数网页的时候，都能比较正常的显示，与主流的 IE/Firefox 效果类似，不过它对于 CSS 支持还不是很完整，对于某些比较复杂的网页的，显示出入比较大。另外 Lobo 项目的文档还不是特别完善，这可能是限制它广泛使用的一个原因。

## JDICplus 中的浏览器组件

JDIC（Java Desktop Integration Components）项目的背景是当可以不考虑 Java 代码的平台可移植性的时候，能让 Java 程序与系统无缝地整合在一起。它提供给 Java 代码直接访问本地桌面的功能，其中包含了一系列的 Java 包以及工具，包含了嵌入本地浏览器组件的功能，启动桌面应用程序，在桌面的系统托盘处添加托盘图标以及注册文件类型关联等等。

JDICplus 是在 JDIC 项目上的另外一个扩展，它是一个 Java 的 win32 操作系统的扩展开发工具包，也就是说，它只能在 Windows 操作系统上使用，所以不具有平台无关性。它提供了很多类似于 Windows API 的功能，除了提供了对 IE 组件的封装之外，还有地图显示组件，以及编辑浏览 MS Word、MS PPT、MS Excel、MS Outlook、PDF 的组件。JDICplus 的官方网站是 [https://jdic.dev.java.net/documentation/incubator/JDICplus/index.html](https://jdic.dev.java.net/documentation/incubator/JDICplus/index.html)，这个页面上展示了很多使用了 JDICplus 这个库的 DEMO，这里讨论的主要是对 Windows IE 封装的浏览器组件。

### 使用 JDICplus 的浏览器组件

使用 JDICplus，首先需要的是环境的配置。JDICplus 需要的是 JDK6.0 或更高的版本，您需要首先从 www.sun.com 下载最新的版本。否则代码不能正常编译运行。

其次是下载 JDICplus 的类库，然后将它添加到 classpath 中。

JDICplus 中对 IE 封装的组件是 org.jdic.web.BrTabbed，它除了封装了网页的显示，还处理了多个标签页的功能，所以它相对是比较强大的。使用它的步骤如下：

*   初始化 JDICplus 组件，设置它为非设计模式。这个组件它默认的模式是设计模式，此时如果用来显示 HTML 内容，会有很多无用的信息。代码如下：
    
    ```
    org.jdic.web.BrComponent.DESIGN_MODE = false;
    ```
    
*   初始化一个 BrTabbed 组件：
    
    ```
    private BrTabbed browser=new BrTabbed();
    ```
    
*   添加到界面中，BrTabbed 是 JPanel 的子类，所以能直接在 Swing 中使用，就像其他 Swing 组件一样添加到 JPanel 或者窗口中。

BrTabbed 类已经处理了点击超链接的事件，而且还支持多标签，这些不需要手动编写代码来处理。

### JDICplus 浏览器组件的优缺点

JDICplus 中的浏览器组件使用了 JNI 来对 IE 进行了封装，所以它显示的效果与 IE 完全相同（还包括其中的右键菜单），而且 BrTabbed 还内置了多标签的功能，使用起来相对比较简单，同样不需要去处理点击超链接的事件。它的缺点首先在于它必须是使用 JDK6.0 或以上版本，要求比较高，同时它底层使用的是 Windows 操作系统相关的 API，所以不具有平台无关性。

## SWT 中的浏览器组件

SWT（The Standard Widget Kit）是 Java 的一套开源组件库，它提供了一种高效的创建图像化用户界面的能力，也是 Eclipse 平台的 UI 组件之一。它相比于 Swing，速度相对比较快，而且因为使用了与操作系统相同的渲染方式，界面上与操作模式上比较接近操作系统的风格。SWT 的跨平台性是通过不同的底层支持库来解决的。

### SWT 的 Browser 类

org.eclipse.swt.browser.Browser 类是 SWT 中用来实现网页浏览器可视化组件的类，它能显示 HTML 文档，并且实现文档之间的超链接。它主要有以下的方法。

*   ```
    boolean back()
    ```
    
    当前的会话返回到历史上前一个界面
    
*   ```
    boolean execute(String script)
    ```
    
    执行特定的脚本
    
*   ```
    boolean forward()
    ```
    
    当前的会话前进到历史上下一个页面
    
*   ```
    void refresh()
    ```
    
    刷新显示当前的界面
    
*   ```
    setText(String html)
    ```
    
    显示特定的 HTML 内容
    
*   ```
    setUrl(String url)
    ```
    
    显示特定的网页内容，传入的参数是网页的地址
    

### 使用 Browser 类

以下的代码演示了如何使用 SWT 中的 Browser 类：

##### SWT 的 Browser 类 demo

```
package org.dakiler.browsers;
 
import org.eclipse.swt.SWT;
import org.eclipse.swt.browser.Browser;
import org.eclipse.swt.widgets.Button;
import org.eclipse.swt.widgets.Display;
import org.eclipse.swt.widgets.Event;
import org.eclipse.swt.widgets.Label;
import org.eclipse.swt.widgets.Listener;
import org.eclipse.swt.widgets.Shell;
import org.eclipse.swt.widgets.Text;
 
public class SWTBrowserTest
{
    public static void main(String args[])
    {
        Display display=new Display();
        Shell shell=new Shell(display);
        shell.setText("SWT Browser Test");
        shell.setSize(800,600);
         
        final Text text=new Text(shell,SWT.BORDER);
        text.setBounds(110,5,560,25);
        Button button=new Button(shell,SWT.BORDER);
        button.setBounds(680,5,100,25);       
        button.setText("go");
        Label label=new Label(shell,SWT.LEFT);
        label.setText("输入网址 :");
        label.setBounds(5, 5, 100, 25);
         
        final Browser browser=new Browser(shell,SWT.FILL);
        browser.setBounds(5,30,780,560);
         
        button.addListener(SWT.Selection, new Listener()
        {
            public void handleEvent(Event event)
            {
                String input=text.getText().trim();
                if(input.length()==0)return;
                if(!input.startsWith("http://"))
                {
                    input="http://"+input;
                    text.setText(input);
                }
                browser.setUrl(input);
            }
        });
         
        shell.open();
        while (!shell.isDisposed()) {
            if (!display.readAndDispatch())
              display.sleep();
          }
          display.dispose();
         
    }
}
```

## 结束语

本文介绍了四种在 Java 图形界面中显示 HTML 或者特定网页的方法，包括 Swing 中的 JEditorPane 组件、Lobo 浏览器的实现、JDICplus 以及 SWT 的 Browser 组件。

对于熟练使用 SWT 的 Java 开发者来说，使用 SWT 中的浏览器组件是一个很好的选择。如果是对于使用 Swing 的程序员来说，如果仅仅是显示不太复杂的 HTML，JEditorPane 就可以胜任了；如果不需要考虑到软件的可移植性，只需要在 Windows 下运行，那么使用 JDICplus 的浏览器组件是一个很好的选择；如果需要考虑可移植性，可以考虑使用 Lobo 浏览器。

* * *

#### 下载资源

*   [本文源代码](http://www.ibm.com/developerworks/apps/download/index.jsp?contentid=481918&filename=BrowserTest.zip&method=http&locale=zh_CN) (BrowserTest.zip | 13 KB)

* * *

#### 相关主题

*   您可以在 [Lobo 官方网站](http://lobobrowser.org/java-browser.jsp) 中获取到关于 Lobo 开源 Java 浏览器的信息。
*   如果想了解 JDICplus 中其它组件的 demo, 您可以查看 [JDICplus 网页](https://jdic.dev.java.net/documentation/incubator/JDICplus/index.html)。
*   参考 [SWT 项目首页](http://www.eclipse.org/swt/)。
*   “[在 Java 程序中内嵌 Mozilla 浏览器](http://www.ibm.com/developerworks/cn/opensource/os-cn-embedmozila/)”（developerWorks，2009 年 10 月）：本文主要包含两个方面的内容：使用 SWT 浏览器部件在 java 代码中内嵌 mozilla 浏览器；使用 JavaXPCOM bridge 定制浏览器功能及与 xulrunner 进行更多交互。
