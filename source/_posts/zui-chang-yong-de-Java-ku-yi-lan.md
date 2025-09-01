---
title: 最常用的Java库一览
id: 632
date: 2024-10-31 22:01:44
author: daichangya
excerpt: 1) 本文列出的名单是根据我自己的调查，并结合个人的经验。有可能是它们不恰恰是最流行的，但至少众所周知的。2) 我会不断更新这个列表，使之更加完整和准确。感谢您的意见。
permalink: /archives/zui-chang-yong-de-Java-ku-yi-lan/
categories:
- java
---



写在前面：

> 1) 本文列出的名单是根据我自己的调查，并结合个人的经验。有可能是它们不恰恰是最流行的，但至少众所周知的。
> 
> 2) 我会不断更新这个列表，使之更加完整和准确。感谢您的意见。

一个典型的Java项目依赖于第三方库。本文总结的Java库适用于各种应用，比较流行并且广泛使用。其中一些还提供简单的示例（来自[ProgramCreek](http://www.programcreek.com/)）。

[Java SDK ](http://www.oracle.com/technetwork/java/javase/overview/index.html)肯定是使用最广的库，所以本文的名单焦点是流行的第三方库。该列表可能并不完善，所以如果你觉得有什么应该出现在列表中的，请留下您的评论。非常感谢！

1、核心库

*   Apache Commons Lang：来自Apache的核心库，为java.lang API补充了许多常用的工具类，如字符串操作、对象的创建等。
*   Google Guava：来自谷歌的核心库，包括集合（Collection）、缓存（Caching）、支持原语（Primitives）等。[（示例）](http://www.programcreek.com/2013/10/google-guava-splitter-example/)

2、HTML、XML Parser

*   Jsoup：一个简化了的 HTML操作的库。[（示例）](http://www.programcreek.com/2012/05/parse-html-in-java/)
*   STaX：一组可以高效处理 XML的API。 [（示例）](http://www.programcreek.com/2011/08/java-code-use-stax-to-create-xml-file/)

3、Web框架

*   Spring：Java平台上众所周知的开源框架和依赖注入容器。[（示例）](http://www.programcreek.com/2012/06/spring-framework-tutorial-hello-world/)
*   Struts2：来自Apache的流行Web框架。 [（示例）](http://www.programcreek.com/2010/03/struts-2-tutorials-sample-application-login-module/)
*   Google Web Toolkit：Google提供的开发工具库，主要用于构建和优化复杂的Web程序用。 [（示例）](http://www.programcreek.com/2011/01/a-example-application-of-gwt/)
*   Strips：使用最新Java技术构建的Web程序框架，推荐使用。
*   Tapestry：面向组件的框架，用于使用Java创建动态、健壮、扩展性高的Web应用程序。

请猛击[这里](http://www.programcreek.com/2011/08/java-web-frameworks-comparison/) 查看以上面框架之间的比较。

4、图表、报表、图像

*   JFreeChart：用于创建如条形图、折线图、饼图等图表。
*   JFreeReport：创建于输出PDF格式的报表。
*   JGraphT：创建图像，其中只包含由线段连接的点集。

5、窗口

*   Swing：SDK提供的GUI库。[（示例）](http://www.programcreek.com/2009/01/the-steps-involved-in-building-a-swing-gui-application/)
*   SWT：[Eclipse](http://res.importnew.com/eclipse "Eclipse ImportNew主页")提供的GUI库。

[SWT与Swing的比较](http://www.programcreek.com/2012/04/swing-vs-swt-side-by-side-comparison/)。

6.、GUI框架

*   Eclipse RCP。[（示例）](http://www.programcreek.com/2013/02/eclipse-rcp-tutorial-add-a-popup-menu/)

7、自然语言处理

*   OpenNLP：来自Apache的自然语言处理库。 [（示例）](http://www.programcreek.com/2012/05/opennlp-tutorial/)
*   Stanford Parser：斯坦福大学提供的自然语言处理库。[（示例）](http://www.programcreek.com/2012/07/java-example-for-using-stanford-postagger/)

如果你是一名NLP专家，请猛击[这里](http://www.programcreek.com/2013/05/collection-of-natural-language-processing-tools/) 查看更多工具库介绍。

8、静态分析

*   Eclipse JDT：由IBM提供的静态分析库，可以操作Java源代码。[（示例）](http://www.programcreek.com/2011/01/a-complete-standalone-example-of-astparser/)
*   WALA：可以处理jar包文件（即字节码）的工具库。[（示例）](http://www.programcreek.com/2012/10/wala-tutorial/)

9、JSON

*   Jackson： 用于处理JSON数据格式的多用途的Java库。Jackson 旨在快速、准确、轻量、对开人员友好之间找到最好的平衡点。
*   XStream：一个简单用于对象和XML互相转换的库。
*   Google Gson：一个专门用于Java对象和Json对象相互转换的工具库。[（示例）](http://www.programcreek.com/2012/05/call-google-search-api-in-java-program/)
*   JSON-lib：用于 beans、maps、collections、java arrays、XML 和 JSON 之间相互转换操作的工具库。

10、数学

*   Apache Commons Math：提供数学计算和数值统计需函数的工具库。

11、日志

*   Apache Log4j：风行一时的日志记录操作库。 [（示例）](http://www.programcreek.com/2009/06/an-entry-example-of-log4j/)
*   Logback：当前流行的log4j项目的继任者。
*   SLF4J（The Simple Logging Facade for Java）： 各种日志框架的一个简单的外观或抽象（如java.util.logging 、logback、log4j等），允许用户在部署时加入需要的日志框架。

12、Office

*   Apache POI：利用其提供的APIs，可以使用纯Java代码操作各种基于微软OLE2合成文档格式的文档。
*   Docx4j：一个用于创建、操作微软公开的XML文件的库（支持Word docx、 Powerpoint pptx和Excel xlsx）。

13、日期和时间

*   Joda-Time：如有质量问题包退包换的Java日期和时间类。

14、数据库

*   Hibernate、EclipseLink、JPA
*   JDO
*   jOOQ
*   SpringJDBC、Spring Data
*   Apache DbUtils

15、开发工具

*   Lambok： 旨在减少代码编写的Java开发库。
*   原文链接： [programcreek](http://www.programcreek.com/2011/08/the-most-widely-used-java-apis/) 