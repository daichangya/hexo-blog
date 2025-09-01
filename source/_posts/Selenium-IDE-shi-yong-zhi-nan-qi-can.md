---
title: Selenium IDE使用指南七（参数定义）
id: 1404
date: 2024-10-31 22:01:54
author: daichangya
excerpt: alertText名称：alertText描述：要检查的文字answer名称：answer描述：响应弹出提示而给出的答案。attributeLocator名称：attributeLocator描述：元素定位符，后跟一个@符号，然后是属性名称，例如“foo@bar”。arrayVariableName
permalink: /archives/Selenium-IDE-shi-yong-zhi-nan-qi-can/
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

[](#alerttext)alertText
-----------------------

名称：alertText

描述：要检查的文字

* * *

[](#answer)answer
-------------

名称：answer

描述：响应弹出提示而给出的答案。

* * *

[](#attributelocator)attributeLocator
-------------------------------------

名称：attributeLocator

描述：元素定位符，后跟一个@符号，然后是属性名称，例如“ foo @ bar”。

* * *

[](#arrayvariablename)arrayVariableName
---------------------------------------

名称：arrayVariableName

描述：包含JavaScript数组的变量的名称。

* * *

[](#conditionalexpression)conditionalExpression
------------------------------

名称：conditionalExpression

描述：返回一个布尔结果以用于控制流命令的JavaScript表达式。

* * *

[](#coord)coord
------------

名称：coord string

description：指定鼠标事件相对于从定位器找到的元素的x，y位置（例如-10,20）。

* * *

[](#expectedvalue)expectedValue
---------------------

名称：expectedValue

描述：您希望变量包含的结果（例如，true，false或其他某个值）。

* * *

[](#expression)expression
-----------------

名称：expression

描述：您要存储的值。

* * *

[](#formlocator)formLocator
---------------------------

名称：form Locator

描述：要提交的表单的元素定位器。

* * *

[](#handle)handle
-------------

名称：window handle

描述：代表特定页面（选项卡或窗口）的句柄。

* * *

[](#iteratorvariablename)iteratorVariableName
---------------------------------------------

名称：迭代器变量名称

描述：在循环控制流命令中迭代集合时使用的变量名称（例如，每个变量）。

* * *

[](#json)json
-------------

名称：json

description：JavaScript对象的字符串表示形式。

* * *

[](#keysequence)keySequence
---------------------------

名称：按键序列

描述：可以键入的键序列可用于发送键击（例如$ {KEY\_ENTER}）。

* * *

[](#locator)locator
---------------

名称：定位器

描述：元素定位器。

* * *

[](#locatorofdragdestinationobject)locatorOfDragDestinationObject
-----------------------------------------------------------------

名称：拖动目标对象的定位器

描述：元素的定位器，其位置（例如，其中最中心的像素）将成为要拖动的对象的定位器被放置的点。

* * *

[](#locatorofobjecttobedragged)locatorOfObjectToBeDragged
---------------------------------------------------------

名称：要拖动的对象的定位器

描述：要拖动的元素的定位器。

* * *

[](#looplimit)loopLimit
-----------------------

名称：循环限制

描述：可选参数，指定循环控制流命令可以执行的最大次数。这样可以防止无限循环。默认值设置为1000。

* * *

[](#message)message
--------------

名称：message

描述：要打印的消息。

* * *

[](#optionlocator)optionLocator
-------------------------------

名称：选项

描述：一个选项定位器，通常只是一个选项标签（例如“ John Smith”）。

* * *

[](#pattern)pattern
--------------

名称：text

描述：完全匹配的字符串。正在支持模式匹配。有关详细信息，请参见[https://github.com/SeleniumHQ/selenium-ide/issues/141](https://github.com/SeleniumHQ/selenium-ide/issues/141)。

* * *

[](#region)region
-------------

名称：地区

描述：指定一个具有坐标和长度的矩形（例如，“ x：257，y：300，宽度：462，高度：280”）。

* * *

[](#resolution)resolution
------------------

名称：分辨率

描述：使用WidthxHeight指定窗口分辨率。（例如1280x800）。

* * *

[](#script)script
-------------

名称：脚本

描述：要运行的JavaScript代码段。

* * *

[](#selectlocator)selectLocator
-------------------------------

名称：选择定位器

描述：标识下拉菜单的元素定位器。

* * *

[](#testcase)testcase
-----------------

名称：测试用例

描述：项目中的测试用例名称。

* * *

[](#text)text
-----------

名称：文字

说明：要使用的文字。

* * *

[](#times)times
-----------

名称：times

描述：控制流循环将执行其块内命令的尝试次数。

* * *

[](#url)url
----------

名称：url

description：要打开的URL（可以是相对的或绝对的）。

* * *

[](#value)value
-----------

名称：值

描述：要输入的值。

* * *

[](#variablename)variableName
--------------------

名称：变量名

描述：不带括号的变量名称。

* * *

[](#waittime)waitTime
-----------------

名称：等待时间

描述：等待时间（以毫秒为单位）。

* * *

[](#xpath)xpath
------------

名称：xpath

描述：要评估的xpath表达式。

* * *