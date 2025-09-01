---
title: 推荐给初级Java程序员的3本进阶书
id: 1027
date: 2024-10-31 22:01:48
author: daichangya
excerpt: " 原作者在这篇文章中介绍3本不错的技术书籍。作者认为这些书籍对新手或者学生而言尤其有帮助。通过一些基础性的教程入门后，我们可以使用Java做基础性的编程。然而，当我们需要从初级提升更高的一个层次时，大多数的人却不知道从何入手。一些好的书籍在这个阶段可以很好地帮助初级开发人员。"
permalink: /archives/18567857/
categories:
 - java
tags: 
 - 学习
---

原作者在这篇文章中介绍3本不错的技术书籍。作者认为这些书籍对新手或者学生而言尤其有帮助。通过一些基础性的教程入门后，我们可以使用Java做基础性的编程。然而，当我们需要从初级提升更高的一个层次时，大多数的人却不知道从何入手。一些好的书籍在这个阶段可以很好地帮助初级开发人员。

![](https://ask.qcloudimg.com/http-save/yehe-2214491/2yx85s7d7o.jpeg?imageView2/2/w/1620)

《[Head First设计模式](http://www.amazon.cn/gp/product/B0011FBU34/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=536&creative=3200&creativeASIN=B0011FBU34&linkCode=as2&tag=importnew-23)》

这本书介绍 [GoF](http://en.wikipedia.org/wiki/Gang_of_Four_%28software%29) 常用[设计模式](http://www.amazon.cn/gp/product/B001130JN8/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&tag=importnew-23&linkCode=as2&camp=536&creative=3200&creativeASIN=B001130JN8 "设计模式:可复用面向对象软件的基础")的方式引人入胜。如果只看封面很难看出来这是一本技术书籍，更不用说这本技术书籍介绍的还是面向对象编程的一些很有用的技巧。这本书采用 [Kathy Sierra](http://headrush.typepad.com/about.html) 式编写风格：虽然她的博客已经关了，但是还是能从前面这个链接看到一些她的文章，建议读一读。如果你周围有人认为设计模式没有什么用处，这本书倒是能够让他们改变看法。个人而言，我认为经典的 GoF 手册是一个很好的参考，但它并不是专为新手准备的。因此强烈推荐在校生（包括那些不清楚组合模式是什么的程序员们）阅读此书。

书中介绍的设计模式是程序开发中比较基本的编程模式，也是面向对象编程的程序员应该了解和掌握的。接下来要介绍的这本书则更偏向于Java语言本身，这也是我日常使用的编程语言。

![](https://ask.qcloudimg.com/http-save/yehe-2214491/sd0pyb6czl.jpeg?imageView2/2/w/1620)

《[Effective Java中文版](http://www.amazon.cn/gp/product/B001PTGR52/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&tag=importnew-23&linkCode=as2&camp=536&creative=3200&creativeASIN=B001PTGR52)》第二版

每个Java程序员的书桌上都应该放有这本书。让我们先了解下作者：

Joshua Bloch是Google公司的首席Java设计师，并且也是一位Jolt 奖获得者。他之前是Sun的一位杰出工程师（distinguished engineer），也是Transarc公司的一个资深系统设计师。Bloch主导了众多基于Java平台的软件系统的设计和实现，包括JDK5.0的功能加强以及获得过奖项的Java集合框架的设计实现。他同时也参与编写了《[Java解惑](http://www.amazon.cn/gp/product/B004EF8C6Q/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=536&creative=3200&creativeASIN=B004EF8C6Q&linkCode=as2&tag=importnew-23 "Java解惑") | Java Puzzlers》 和《[](http://www.amazon.cn/gp/product/B0077K9XHW/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&tag=importnew-23&linkCode=as2&camp=536&creative=3200&creativeASIN=B0077K9XHW)[Java并发编程实战](http://www.amazon.cn/gp/product/B0077K9XHW/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&tag=importnew-23&linkCode=as2&camp=536&creative=3200&creativeASIN=B0077K9XHW "Java并发编程实战") | [Java Concurrency in Practice](http://www.amazon.com/gp/product/0321349601/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&tag=job0ae-20&linkCode=as2&camp=1789&creative=9325&creativeASIN=0321349601 "Java Concurrency in Practice")》这两本技术书。

就凭“Java集合框架开发者”这个称号，我们就应该认真听取这位值得尊敬的程序员的建议。这些建议在这本书中组织成78个点：读者可以按照自己的速度进行阅读。

*   在复写equals和hashcode方法时，我们应该遵循什么规则？
*   不可变类（immutable class）是什么？
*   在特定的情况下，应当选用哪种最相关的异常类型?运行时异常（Runtime exception）还是可捕获异常（checked exception）？
*   对于一个托管语言（managed language，详细请参考 [wiki](http://en.wikipedia.org/wiki/Managed_code)介绍），如何在混淆编译时保留（preserve）类的成员？

上面所有的问题（也包括其他74个）都有实用主义者Joshua Bloch的详细解释。读完这本书，程序员应该能意识到使用[Findbugs](http://findbugs.sourceforge.net/)、[Checkstyle](http://checkstyle.sourceforge.net/)这些工具的必要性了。

![](https://ask.qcloudimg.com/http-save/yehe-2214491/g8nm6a6yj4.jpeg?imageView2/2/w/1620)

《[Java并发编程实战](http://www.amazon.cn/gp/product/B0077K9XHW/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&tag=importnew-23&linkCode=as2&camp=536&creative=3200&creativeASIN=B0077K9XHW)》

 一年前我正努力在做 UI 开发工作时（在[Eclipse](http://res.importnew.com/eclipse "Eclipse ImportNew主页") 插件中使用SWT/JFace，其他一些项目则使用Swing ），就看了这本书。那时，我想了解如何实现一个快速响应的UI，从而能给用户更好的使用体验。我知道自己写线程安全的代码是非常复杂的，尽管运行时间长的操作通常是一个独立的线程。UI开发和多核系统应用开发是学习如何开发线程安全的软件系统的一个很好的理由。

这本书的作者如下：[Brian Goetz](http://www.briangoetz.com/)，Joshua Bloch（又出现这位大牛了，我们刚提到过，还记得吗？）， [Doug Lea](http://en.wikipedia.org/wiki/Doug_Lea)（java.util.concurrent包的开发者）， [David Holmes](http://blogs.sun.com/dholmes/)，Tim Peierls 和[Joseph Bowbeer](http://home.comcast.net/~joebowbeer/main/joeswork.htm)。

这本书的风格非常直接，有的代码在非线程安全的环境下表现不错，可一旦到了线程安全的环境下就变得十分的危险。接着，这本书介绍了基本的保证线程安全的机制：同步机制，volatile关键字等。本书还有对java.util.concurrent接口的介绍，你可以根据自己的需要来选择适合的并发集合类。这本书也介绍了程序运行时的错误管理，以及如何测试代码是否是线程安全的。而且书中还提供了说明性的注释（Annotation）（[下载](http://www.javaconcurrencyinpractice.com/)），这些注释通过了FindBugs的检查！

还有其它推荐吗？

其实还有不少书值得推荐，不过现在我优先讨论这三本。如果你一本都还从没读过，那么我建议你按照本文介绍顺序进行阅读。好啦，你喜欢的技术书籍有哪些呢？

英文原文：[coderfriendly](http://www.coderfriendly.com/2009/04/10/the-books-starter-pack/)