---
title: UML用例图总结
id: 731
date: 2024-10-31 22:01:45
author: daichangya
excerpt: "用例图主要用来描述“用户、需求、系统功能单元”之间的关系。它展示了一个外部用户能够观察到的系统功能模型图。　　【用途】：帮助开发团队以一种可视化的方式理解系统的功能需求。　　用例图所包含的元素如下：　　1. 参与者(Actor)　　表示与您的应用程序或系统进行交互的用户、组"
permalink: /archives/8871839/
tags: 
 - uml
---


　　用例图主要用来描述“用户、需求、系统功能单元”之间的关系。它展示了一个外部用户能够观察到的系统功能模型图。

　　【用途】：帮助开发团队以一种可视化的方式理解系统的功能需求。

　　用例图所包含的元素如下：

　　1.&nbsp;参与者(Actor)

　　表示与您的应用程序或系统进行交互的用户、组织或外部系统。用一个小人表示。


<img src="http://pic001.cnblogs.com/images/2012/1/2012013015202157.gif" alt="" style="margin:0px; padding:0px; font-size:12px; border:none">

　　2.&nbsp;用例(Use Case)

&nbsp;　　用例就是外部可见的系统功能，对系统提供的服务进行描述。用椭圆表示。


<img src="http://pic001.cnblogs.com/images/2012/1/2012013015210973.gif" alt="" style="margin:0px; padding:0px; font-size:12px; border:none">

　　3. 子系统(Subsystem)

　　用来展示系统的一部分功能，这部分功能联系紧密。


<img src="http://pic001.cnblogs.com/images/2012/1/2012013015215321.gif" alt="" style="margin:0px; padding:0px; font-size:12px; border:none">

　　4.&nbsp;关系

　　用例图中涉及的关系有：关联、泛化、包含、扩展。

　　如下表所示：


<img src="http://pic001.cnblogs.com/images/2012/1/2012013015241550.png" alt="" style="margin:0px; padding:0px; font-size:12px; border:none">

　　a. 关联(Association)

　　表示参与者与用例之间的通信，任何一方都可发送或接受消息。

　　【箭头指向】：指向消息接收方


<img src="http://pic001.cnblogs.com/images/2012/1/2012013015250613.gif" alt="" style="margin:0px; padding:0px; font-size:12px; border:none">

　　b. 泛化(Inheritance)

　　就是通常理解的继承关系，子用例和父用例相&#20284;，但表现出更特别的行为；子用例将继承父用例的所有结构、行为和关系。子用例可以使用父用例的一段行为，也可以重载它。父用例通常是抽象的。

　　【箭头指向】：指向父用例


<img src="http://pic001.cnblogs.com/images/2012/1/2012013015260081.gif" alt="" style="margin:0px; padding:0px; font-size:12px; border:none">

　　c. 包含(Include)

　　包含关系用来把一个较复杂用例所表示的功能分解成较小的步骤。

　　【箭头指向】：指向分解出来的功能用例


<img src="http://pic001.cnblogs.com/images/2012/1/2012013015265841.gif" alt="" style="margin:0px; padding:0px; font-size:12px; border:none">

　　d. 扩展(Extend)

　　扩展关系是指用例功能的延伸，相当于为基础用例提供一个附加功能。

　　【箭头指向】：指向基础用例


<img src="http://pic001.cnblogs.com/images/2012/1/2012013015274296.gif" alt="" style="margin:0px; padding:0px; font-size:12px; border:none">

　　e. 依赖(Dependency)

　　以上4种关系，是UML定义的标准关系。但VS2010的用例模型图中，添加了依赖关系，用带箭头的虚线表示，表示源用例依赖于目标用例。

　　【箭头指向】：指向被依赖项


<img src="http://pic001.cnblogs.com/images/2012/1/2012013015290255.gif" alt="" style="margin:0px; padding:0px; font-size:12px; color:rgb(35,35,35); border:none"><br style="margin:0px; padding:0px; line-height:10px">


　　5. 项目(Artifact)

　　用例图虽然是用来帮助人们形象地理解功能需求，但却没多少人能够通看懂它。很多时候跟用户交流甚至用Excel都比用例图强，VS2010中引入了“项目”这样一个元素，以便让开发人员能够在用例图中链接一个普通文档。

　　用依赖关系把某个用例依赖到项目上：


<img src="http://pic001.cnblogs.com/images/2012/1/2012013015295762.gif" alt="" style="margin:0px; padding:0px; font-size:12px; border:none">

　　然后把项目-》属性&nbsp;的Hyperlink设置到你的文档上；

　　这样当你在用例图上双击项目时，就会打开相关联的文档。

　　6. 注释(Comment)


<img src="http://pic001.cnblogs.com/images/2012/1/2012013015305290.gif" alt="" style="margin:0px; padding:0px; font-size:12px; border:none">&nbsp;

　　包含(include)、扩展(extend)、泛化(Inheritance)&nbsp;的区别：

　　条件性：泛化中的子用例和include中的被包含的用例会无条件发生，而extend中的延伸用例的发生是有条件的；

　　直接性：泛化中的子用例和extend中的延伸用例为参与者提供直接服务，而include中被包含的用例为参与者提供间接服务。

　　对extend而言，延伸用例并不包含基础用例的内容，基础用例也不包含延伸用例的内容。

　　对Inheritance而言，子用例包含基础用例的所有内容及其和其他用例或参与者之间的关系；

　　一个用例图示例：


<img src="http://pic001.cnblogs.com/images/2012/1/2012013015315117.gif" alt="" style="margin:0px; padding:0px; font-size:12px; border:none">&nbsp;

　　牢骚：

　　感觉用例图还不成熟，并不能很好地表达系统的需求，&nbsp;没有UML背景的用户几乎不知道画的是些什么。

　　其次，包含关系、扩展关系的箭头符号竟然是同样的箭头，仅靠上方写个文字来加以区别，翻译成其他语言的话，几乎就不知道代表什么意思。扩展关系的箭头朝向也很难理解，为何要指向基用例，而不指向扩展用例。

　　VS2010添加的“项目”元素，是个很好的创新，能够在用例图中关联word, excel这些文档。但为什么不把这些功能直接集成到用例里面，双击用例就弹出一份文档岂不更容易理解，非要画蛇添足地加一个元件，仅仅为了提供个链接功能。&nbsp;

　　用例描述表：

　　鉴于用列图并不能清楚地表达功能需求，开发中大家通常用描述表来补充某些不易表达的用例，下图的表给大家提供一个参考：


<img src="http://pic001.cnblogs.com/images/2012/1/2012013015331348.gif" alt="" style="margin:0px; padding:0px; font-size:12px; border:none">
