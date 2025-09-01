---
title: 如何在Python和lxml中使用XPath语法
id: 1352
date: 2024-10-31 22:01:51
author: daichangya
cover: https://images.jsdiff.com/python-xml-title_1588046761759.png
excerpt: "如何在Python和lxml中使用XPath语法示例XML和XML等方言成为各种文档的事实上的标准格式，例如Spring的框架配置文件，Struts，VisualStudio的IDE项目，Web服务的响应，Android的UI布局语言等的解析和处理。它们已成为任何编程基础结构的必备组件。因为格式无处"
permalink: /archives/%E5%A6%82%E4%BD%95%E5%9C%A8python%E5%92%8Clxml%E4%B8%AD%E4%BD%BF%E7%94%A8xpath%E8%AF%AD%E6%B3%95/
categories:
 - python基础教程
tags: 
 - lxml
 - python
---

XML和XML等方言成为各种文档的事实上的标准格式，例如Spring的框架配置文件，Struts，Visual Studio的IDE项目，Web服务的响应，Android的UI布局语言等的解析和处理。它们已成为任何编程基础结构的必备组件。因为格式无处不在，所以程序员在这里和那里遇到它们几乎是不可避免的。XML就是数据，AST就是代码。XML掌握数据的本质或语义，它是描述数据和信息的理想通用语言，从字面上看，它无处不在。读取，解析，导航和操作XML文档的能力是任何程序员必备的技能。

该LXML 是一个Python化的C库libxml2和其中的libxslt很容易使用时绑定。对于简单的查询（如查找标签），可以使用findtext，对于复杂的查询，则需要更强大的工具。XPath来了，XPath是一种迷你语言，它允许您指定如何以声明方式选择XML文档中的元素。在某些方面，它类似于用于选择DOM元素的CSS选择器，XPath允许您像浏览CSS一样浏览XML文档中的元素和属性。路径标识一组节点，包括元素，属性，文本等。

XPath在XSLT和XSL中被大量使用，因为它所做的只是在输入文档中定位元素并对其进行转换以在输出文档中生成结果，就像CSS使用选择器在HTML文档中定位元素并应用样式一样在上面。

在本文中，我们将通过示例HTML文件和lxml api 来说明XPath的语法。

### 创建示例HTML文件

创建具有以下内容的HTML文件xpath-test.html
```
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-highlight"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
     </ul>
 </div>
```


读取文件并使用lxml.html模块进行解析

```
import lxml.html
html = lxml.html.parse("xpath-test.html")
```

### Child operator /

使用此运算符可以分隔父级和子级。
当子运算符是路径的第一个字符时，表示这是绝对路径，即从根节点开始。

使用绝对路径找到div节点

```
nodes = html.xpath('/html/body/div')
```

请注意，HTML解析器将通过添加缺少的html和body来修复文档，根节点应为html。您可以打印正在使用的HTML源

```
from lxml import etree
print(etree.tostring(html))
```

输出将是

```

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">
<html><body><div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
     </li></ul>
 </div>
</body>
</html>

```


选择所有链接的文字

```
nodes = html.xpath('/html/body/div/ul/li/a/text()')
```

打印

```
['first item', 'second item', 'third item', 'fourth item', 'fifth item']
```

### Descendant operator //

选择父节点的子孙，当第一个子孙时，意味着搜索从根开始

如下修改HTML

```
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
    </ul>
    <div>
      <ul>
        <li><a href="link6.html">sixth item</a></li>
      </ul>  
    </div>  
 </div>
```
 

获取所有链接

```
lis = html.xpath('//li/a/text()')
```

得到

```
['first item', 'second item', 'third item', 'fourth item', 'fifth item', 'sixth item']
```


使用绝对路径将需要两个查询，而后代运算符只需要一个。

仅在第二个ul列表中获得链接

```
lis = html.xpath('/html/body/div/div//li/a/text()')
print (lis)
['sixth item']
```

### 属性@运算符

按元素属性（例如class属性）过滤元素

选择所有具有class属性为“ item-0”的元素：

```
attributes = html.xpath('//li[@class="item-0"]/a/text()')
print (attributes)
['first item', 'fifth item']
```

### 逻辑运算符

逻辑查询返回布尔值，如果匹配的元素与查询匹配，则返回true，否则返回false。

测试第二个列表中的链接是否包含文本内容等于“第一项”的链接

```
logics = html.xpath("//div/div//a/text()='first item'")
print (logics)
False
```
