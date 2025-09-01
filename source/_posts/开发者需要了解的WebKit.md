---
title: 开发者需要了解的WebKit
id: 787
date: 2024-10-31 22:01:46
author: daichangya
excerpt: "对许多开发者来说，WebKit就像一个黑盒。我们把HTML、CSS、JS和其他一大堆东西丢进去，然后WebKit魔法般的以某种方式把一个看起来不错的网页展现给我们。但事实上，Paul的同事Ilya Grigorik说：WebKit才不是个黑盒。它是个白盒。并且，它是个打开的白盒。"
permalink: /archives/9883177/
categories:
 - 其他
---


　　[Paul Irish](http://paulirish.com/about/)是著名的前端开发工程师，同时他也是Chrome开发者关系团队成员，jQuery团队成员，Modernizr、 Yeoman、CSS3 Please和HTML5 Boilerplate的lead developer。针对大家对WebKit的种种误解，他在自己的博客发表了[《WebKit for Developers》](http://paulirish.com/)一文，试图为大家解惑。

　　对许多开发者来说，WebKit就像一个黑盒。我们把HTML、CSS、JS和其他一大堆东西丢进去，然后WebKit魔法般的以某种方式把一个看起来不错的网页展现给我们。但事实上，Paul的同事Ilya Grigorik说：

> WebKit才不是个黑盒。它是个白盒。并且，它是个打开的白盒。

　　所以让我们来花些时间了解这些事儿：

*   什么是WebKit？
*   什么不是WebKit？
*   基于WebKit的浏览器是如何使用WebKit的？
*   为什么又有不同的WebKit？

　　现在，特别是Opera宣布将浏览器引擎转换为WebKit之后，我们有很多使用WebKit的浏览器，但是我们很难去界定它们有哪些相同与不同。下面我争取为这个谜团做些解读。而你也将会更懂得判断浏览器的不同，了解如何在正确的地方报告bug，还会了解如何在特定浏览器下高效开发。

　　标准Web浏览器组件

　　让我们列举一些现代浏览器的组件：

*   HTML、XML、CSS、JavsScript解析器
*   Layout
*   文字和图形渲染
*   图像解码
*   GPU交互
*   网络访问
*   硬件加速

　　这里面哪些是WebKit浏览器共享的？差不多只有前两个。其他部分每个WebKit都有各自的实现，所谓的“port”。现在让我们了解一下这是什么意思……

　　WebKit Ports是什么？

　　在WebKit中有不同的“port”，但是这里允许我来让WebKit hacker，Sencha的工程主管Ariya Hidayat来解释：

> WebKit最常见的参考实现是Apple在Mac OS X上的实现（这也是[最早和最原始的WebKit库](http://lists.kde.org/?l=kfm-devel&m=104197092318639&w=2)）。但是你也能猜到，在Mac OS X下，许多不同的接口在很多不同的原生库下被实现，大部分集中在[CoreFoundation](https://developer.apple.com/technologies/mac/)。举例来说，如果你定义了一个纯色圆角的按钮，WebKit知道要去哪里，也知道要如何去绘制这个按钮。但是，绘制按钮的工作最终还是会落到[CoreGraphics](http://developer.apple.com/library/ios/#documentation/CoreGraphics/Reference/CoreGraphics_Framework/_index.html)去。

　　上面已经提到，CoreGraphics只是Mac port的实现。不过Mac Chrome用的是[Skia](http://www.chromium.org/developers/design-documents/graphics-and-skia)。

> 随时间推移，WebKit被“port”（移植）到了各个不同的平台，包括桌面端和移动端。这种做法被称作“WebKit port”。对Windows版Safari来说，Apple通过[（有限实现的）Windows版本CoreFoundation](http://developer.apple.com/opensource/internet/webkit_sptlib_agree.html) 来port WebKit。

　　……不过Windows版本的Safari[现在已经死掉了](http://www.macworld.com/article/1167904/safari_6_available_for_mountain_lion_and_lion_but_not_windows.html)。

> 除此之外，还有很多很多其它的“port”（[参见列表](http://trac.webkit.org/wiki#WebKitPorts)）。Google创建并维护着它的Chromium port。这其实也是一个基于Gtk+的WebKitGtk。诺基亚通过收购Trolltech，维护着以[QtWebKit module](http://doc.qt.nokia.com/qtwebkit.html)而闻名的WebKit Qt port。

　　让我们看看其中一些WebKit ports：

*   Safari
    *   OS X Safari和Windows Safari使用的是不同的port
    *   用于OS X Safari的WebKit Nightly以后会渐渐成为一个边缘版本
*   Mobile Safari
    *   在一个私有代码分支上维护，不过代码现在正在[合并到主干](http://trac.webkit.org/changeset/142373)
    *   iOS Chrome（使用了Apple的WebView，不过后面的部分有很多不同）
*   Chrome（Chromium）
    *   安卓Chrome（直接使用Chromium port）
    *   Chromium也驱动了[Yandex Browser](http://browser.yandex.ru/)、 [360 Browser](http://se.360.cn/)、[Sogou Browser](http://ie.sogou.com/)，很快，还会有Opera。
*   [还有很多](http://trac.webkit.org/wiki#WebKitPorts)： Amazon Silk、Dolphin、Blackberry、QtWebKit、WebKitGTK+、The EFL port (Tizen)、wxWebKit、WebKitWinCE……

　　不同的port专注于不同的领域。Mac的port注意力集中在浏览器和操作系统的分割上，允许把ObjectC和C++绑定并嵌入原生应用的渲染。Chromium专注在浏览器上。QtWebKit的port在他的跨平台GUI应用架构上给apps提供运行时环境或者渲染引擎。

　　WebKit浏览器共享了那些东西？

　　首先，让我们来看看这些WebKit ports的共同之处：

　　（作者注：很有意思，这些内容我写了很多次，每次Chrome团队成员都给我纠正错误，正如你看到的……）

1.  “WebKit在使用相同的方式解析WebKit。”——实际上，Chrome是唯一支持多线程HTML解析的port。
2.  “一旦解析完成，DOM树也会构建成相同的样子。”——实际上Shadow DOM只有在Chromium才被开启。所以DOM的构造也是不同的。自定义元素也是如此。
3.  “WebKit为每个人创建了‘window’对象和‘document’对象。”——是的，尽管它暴露出的属性和构造函数可以通过[feature flags](https://trac.webkit.org/wiki/FeatureFlags)来控制。
4.  “CSS解析都是相同的。将CSS解析为对象模型是个相当标准的过程。”——不过，Chrome只支持-webkit-前缀，而Apple和其他的ports支持遗留的-khtml-和-apple-前缀。
5.  “布局定位？这些是基本生计问题啊”—— 尽管Sub-pixel layout和saturated layout算法是WebKit的一部分，不过各个port的实现效果还是有很多不同。

　　所以，情况很复杂。

　　就像Flickr和GitHub通过flag标识来实现自己的功能一样，WebKit也有相同处理。这允许各个port自行决定是否启用[WebKit编译特性标签](https://trac.webkit.org/wiki/FeatureFlags)的各种功能。通过[命令行开关](http://peter.sh/experiments/chromium-command-line-switches/3)，或者通过[about:flags](http://blogs.adobe.com/cantrell/archives/2012/07/all-about-chrome-flags.html)还可以控制是否通过运行时标识来展示功能特性。

　　好，现在让我们再尝试一次搞清楚WebKit究竟有哪些相同…

　　每个WebKit port有哪些共同之处

*   DOM、winow、document
*   CSS对象模型
*   CSS解析，键盘事件处理
*   HTML解析和DOM构建
*   所有的布局和定位
*   Chrome开发工具和WebKit检查器的UI与检查器
*   contenteditable、pushState、文件API、大多数SVG、CSS Transform math、Web Audio API、localStorage等功能
*   [很多其他功能与特性](http://trac.webkit.org/browser/trunk/Source/WebCore)

　　这些领域现在有点儿模糊，让我们尝试把事情弄得更清楚一点。

　　什么是WebKit port们并没有共享的：

*   GPU相关技术
    *   3D转换
    *   WebGL
    *   视频解码
*   将2D图像绘制到屏幕
    *   解析方式
    *   SVG和CSS渐变绘制
*   文字绘制和断字
*   网络层（SPDY、预渲染、WebSocket传输）
*   JavaScript引擎
    *   JavaScriptCore 在WebKit repo中。V8和JavaScriptCore被绑定在WebKit中。
*   表单控制器的渲染
*   <video>和<audio>的元素表现和解码实现
*   图像解码
*   页面导航 前进/后退
    *   pushState()的导航部分
*   SSL功能，比如Strict Transport Security和Public Key Pins

　　让我们谈谈其中的2D图像部分： 根据port的不同，我们使用完全不同的库来处理图像到屏幕的绘制过程：

![](http://images.cnitblog.com/news/145819/201303/18170015-47a4838db76f4a97b8e54d692c737c20.png)

　　更宏观一点来看，一个最近刚添加的功能：CSS.supports()在除了没有css3特性检测功能的win和wincairo这两个port之外，在其它所有port中都[可用](http://trac.webkit.org/changeset/142739)。

　　现在到了卖弄学问的技术时间。上面讲的内容其实并不正确。事实上那是WebCore被共享的东西。而WebCore其实是当大家讨论HTML和SVG的布局、渲染和DOM处理时提到的WebKit。技术上讲，WebKit是WebCore和各种ports之间的绑定层，尽管通常来说这个差别并不那么重要。

　　一个图表应该可以帮助大家理解：

![](http://images.cnitblog.com/news/145819/201303/18165902-9c43d0e6c5b84860a1f902fc9c0e858f.png)

　　WebKit中的许多组件都是可以更换的（图中标灰色的部分）。

　　举个例子来说，Webkit的JavaScript引擎，JavaScriptCore，是WebKit的默认组件。（它最初是当WebKit从KHTML分支时从KJS演变来的）。同时，Chromium port用V8引擎做了替换，还使用了独特的DOM绑定来映射上面的组件。

　　字体和文字渲染是平台上的重要部分。在WebKit中有两个独立的文字路径：Fast和Complex。这两者都需要平台特性的支持，但是Fast只需要知道如何传输字型，而Complex实际上需要掌握平台上所有的字符串，并说“请绘制这个吧”。

> "WebKit就像一个三明治。尽管Chromium的包装更像是一个墨西哥卷。一个美味的Web平台墨西哥卷。"
> 
> —— Dimitri Glazkov, Chrome WebKit hacker，Web Components和Shadow DOM拥护者。

　　现在，让我们放宽镜头看看一些port和一些子系统。下面是WebKit的5个port；尽管它们共享了WebCore的大部分，但考虑一下它们的stack有哪些不同。

<table id="wk-matrix" style="border:1px solid rgb(192,192,192);border-collapse:collapse;width:617px;"><tbody><tr><td style="line-height:25px;border:1px solid rgb(192,192,192);border-collapse:collapse;">&nbsp;</td><th style="border:1px solid rgb(192,192,192);border-collapse:collapse;">Chrome (OS X)</th><th style="border:1px solid rgb(192,192,192);border-collapse:collapse;">Safari (OS X)</th><th style="border:1px solid rgb(192,192,192);border-collapse:collapse;">QtWebKit</th><th style="border:1px solid rgb(192,192,192);border-collapse:collapse;">Android Browser</th><th style="border:1px solid rgb(192,192,192);border-collapse:collapse;">Chrome for iOS</th></tr><tr><th style="border:1px solid rgb(192,192,192);border-collapse:collapse;">Rendering</th><td style="line-height:25px;border:1px solid rgb(192,192,192);border-collapse:collapse;">Skia</td><td style="line-height:25px;border:1px solid rgb(192,192,192);border-collapse:collapse;">CoreGraphics</td><td style="line-height:25px;border:1px solid rgb(192,192,192);border-collapse:collapse;">QtGui</td><td style="line-height:25px;border:1px solid rgb(192,192,192);border-collapse:collapse;">Android stack/Skia</td><td style="line-height:25px;border:1px solid rgb(192,192,192);border-collapse:collapse;">CoreGraphics</td></tr><tr><th style="border:1px solid rgb(192,192,192);border-collapse:collapse;">Networking</th><td style="line-height:25px;border:1px solid rgb(192,192,192);border-collapse:collapse;">Chromium network stack</td><td style="line-height:25px;border:1px solid rgb(192,192,192);border-collapse:collapse;">CFNetwork</td><td style="line-height:25px;border:1px solid rgb(192,192,192);border-collapse:collapse;">QtNetwork</td><td style="line-height:25px;border:1px solid rgb(192,192,192);border-collapse:collapse;">Fork of Chromium’s network stack</td><td style="line-height:25px;border:1px solid rgb(192,192,192);border-collapse:collapse;">Chromium stack</td></tr><tr><th style="border:1px solid rgb(192,192,192);border-collapse:collapse;">Fonts</th><td style="line-height:25px;border:1px solid rgb(192,192,192);border-collapse:collapse;">CoreText via Skia</td><td style="line-height:25px;border:1px solid rgb(192,192,192);border-collapse:collapse;">CoreText</td><td style="line-height:25px;border:1px solid rgb(192,192,192);border-collapse:collapse;">Qt internals</td><td style="line-height:25px;border:1px solid rgb(192,192,192);border-collapse:collapse;">Android stack</td><td style="line-height:25px;border:1px solid rgb(192,192,192);border-collapse:collapse;">CoreText</td></tr><tr><th style="border:1px solid rgb(192,192,192);border-collapse:collapse;">JavaScript</th><td style="line-height:25px;border:1px solid rgb(192,192,192);border-collapse:collapse;">V8</td><td style="line-height:25px;border:1px solid rgb(192,192,192);border-collapse:collapse;">JavaScriptCore</td><td style="line-height:25px;border:1px solid rgb(192,192,192);border-collapse:collapse;">JSC (V8 is used elsewhere in Qt)</td><td style="line-height:25px;border:1px solid rgb(192,192,192);border-collapse:collapse;">V8</td><td style="line-height:25px;border:1px solid rgb(192,192,192);border-collapse:collapse;">JavaScriptCore (without JITting) *</td></tr></tbody></table>

　　*iOS Chrome注：你可能知道它使用 UIWebView。由于UIWebView的能力限制。它只能使用移动版Safari的渲染层，JavaScriptCore（而不是V8）和单进程模式。然而，大量的Chromium 代码还是起到了调节作用 ，比如网络层、同步、书签架构、地址栏、度量工具和崩溃报告。（同时，由于JavaScript很少成为移动端的瓶颈，缺少JIT编译器只有很小的影响。）

　　好吧，那么我们该怎么办？

　　现在所有WebKit完全不同了，我好怕。

　　别这样！[WebKit的layoutTests覆盖面](http://trac.webkit.org/browser/trunk/LayoutTests)非常广（据最新统计，有28,000个layoutTests），这些test不仅针对已存在的特性，而且针对任何发现的回归。实际上，每当你探索一些新的或难懂的DOM/CSS/HTML5特性时，在整个web平台上，layoutTests经常已经有了一些奇妙的小demo。

　　另外，W3C正在努力研究一致性测试套件。这意味着我们可以期待使用同一个测试套件来测试不同的WebKit port和浏览器，以此来获得更少的怪异模式，和一个带来更少的怪癖模式和更具互操作性的web。对所有参加过[Test The Web Forward](http://testthewebforward.org/)活动的人们……致谢！

　　Opera刚刚迁移到了WebKit了。会怎样？

　　Robert Nyman和 Rob Hawkes也[谈到了这个](http://robertnyman.com/2013/02/14/webkit-an-objective-view/) ，但是我会再补充一些：Opera在公告中明显指出Opera将采用Chromium。这意味着WebGL，Canvas，HTML5 表单，2D图像实现——Chrome和Opera将在所有这些功能上保持一致。API和后端实现也会完全相同。由于Opera是基于 Chromium，你可以有足够的信心去相信你的尖端工作将会在Chrome和Opera上获得兼容。

　　我还应该指出，所有的Opera浏览器都将采用Chromium：包括他的Windows，Mac、Linux版本，和Opera Mobile（完全成熟的移动浏览器）。甚至Opera Mini都将使用基于Chromium的服务器渲染集群来替换当前的基于Presto的服务器端渲染。

　　……那WebKit Nightly是什么？

　　它是WebKit的[mac port](http://trac.webkit.org/browser/trunk/Source/WebKit/mac) ，和Safari运行的二进制文件一样（尽管会替换一些底层库）。因为苹果在项目中起主导地位，所以它的表现和功能与Safari的总是那么一致。在很多情况下，当其它port可能会试验新功能的时候，Apple却显得相对保守。不管怎样，如果你想我用中学一样的类比，想想这个好了：WebKit Nightly对于Safari就像Chromium对于Chrome。

　　同样的，[Chrome Canary](http://paulirish.com/2012/chrome-canary-for-developers/) 有着最新的WebKit资源。

　　告诉我更多的WebKit内幕吧。

　　就在这儿了，小伙子：

[![](http://images.cnitblog.com/news/145819/201303/18165902-991d8e783ecf4bf2aad9faa3dca0bc89.png)](https://docs.google.com/presentation/d/1ZRIQbUKw9Tf077odCh66OrrwRIVNLvI_nhLm2Gi__F0/embed?start=false&loop=false&delayms=3000)