---
title: Selenium IDE使用指南六（指令列表）
id: 1403
date: 2024-10-31 22:01:54
author: daichangya
excerpt: "addselection将选择添加到多选元素中的选项集。论点locator：元素定位器。value：要输入的值。answeronnextprompt影响下一个警报提示。此命令将向其发送指定的答案字符串。如果警报已存在，请改用“可见提示时的webdriver回答”。论点答案：提示弹出窗口时给出的答案。"
permalink: /archives/selenium-ide-commands/
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

[](#add-selection)`add selection`
---------------------------------

将选择添加到多选元素中的选项集。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [value](/archives/selenium-ide-arguments#value)：要输入的值。
    

* * *

[](#answer-on-next-prompt)`answer on next prompt`
-------------------------------------------------

影响下一个警报提示。此命令将向其发送指定的答案字符串。如果警报已存在，请改用“可见提示时的webdriver回答”。

**论点**

*   [答案](/archives/selenium-ide-arguments#answer)：提示弹出窗口时给出的答案。

* * *

[](#assert)`assert`
-------------------

检查变量是否为期望值。变量的值将转换为字符串以进行比较。如果断言失败，则测试将停止。

**论点**

*   [变量名](/archives/selenium-ide-arguments#variablename)：不带括号的[变量名](/archives/selenium-ide-arguments#variablename)。
    
*   [期望值](/archives/selenium-ide-arguments#expectedvalue)：您期望变量包含的结果（例如，true，false或其他某个值）。
    

* * *

[](#assert-alert)`assert alert`
-------------------------------

确认已使用提供的文本呈现警报。如果断言失败，则测试将停止。

**论点**

*   [提示文字](/archives/selenium-ide-arguments#alerttext)：要检查的文字

* * *

[](#assert-checked)`assert checked`
-----------------------------------

确认目标元素已被检查。如果断言失败，则测试将停止。
<separator></separator>
**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。

* * *

[](#assert-confirmation)`assert confirmation`
---------------------------------------------

确认已提交确认。如果断言失败，则测试将停止。

**论点**

*   [text](/archives/selenium-ide-arguments#text)：要使用的文本。

* * *

[](#assert-editable)`assert editable`
-------------------------------------

确认目标元素是可编辑的。如果断言失败，则测试将停止。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。

* * *

[](#assert-element-present)`assert element present`
---------------------------------------------------

确认目标元素存在于页面上的某处。如果断言失败，则测试将停止。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。

* * *

[](#assert-element-not-present)`assert element not present`
-----------------------------------------------------------

确认目标元素不在页面上任何地方。如果断言失败，则测试将停止。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。

* * *

[](#assert-not-checked)`assert not checked`
-------------------------------------------

确认尚未检查目标元素。如果断言失败，则测试将停止。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。

* * *

[](#assert-not-editable)`assert not editable`
---------------------------------------------

确认目标元素不可编辑。如果断言失败，则测试将停止。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。

* * *

[](#assert-not-selected-value)`assert not selected value`
---------------------------------------------------------

确认下拉元素中所选选项的value属性不包含提供的值。如果断言失败，则测试将停止。

**论点**

*   [select locator](/archives/selenium-ide-arguments#selectlocator)：标识下拉菜单的元素定位器。
    
*   [text](/archives/selenium-ide-arguments#text)：完全匹配的字符串。正在支持模式匹配。有关详细信息，请参见[https://github.com/SeleniumHQ/selenium-ide/issues/141](https://github.com/SeleniumHQ/selenium-ide/issues/141)。
    

* * *

[](#assert-not-text)`assert not text`
-------------------------------------

确认元素的文本不包含提供的值。如果断言失败，则测试将停止。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [text](/archives/selenium-ide-arguments#text)：完全匹配的字符串。正在支持模式匹配。有关详细信息，请参见[https://github.com/SeleniumHQ/selenium-ide/issues/141](https://github.com/SeleniumHQ/selenium-ide/issues/141)。
    

* * *

[](#assert-prompt)`assert prompt`
---------------------------------

确认已呈现JavaScript提示。如果断言失败，则测试将停止。

**论点**

*   [text](/archives/selenium-ide-arguments#text)：要使用的文本。

* * *

[](#assert-selected-value)`assert selected value`
-------------------------------------------------

确认下拉元素中所选选项的value属性包含提供的值。如果断言失败，则测试将停止。

**论点**

*   [select locator](/archives/selenium-ide-arguments#selectlocator)：标识下拉菜单的元素定位器。
    
*   [text](/archives/selenium-ide-arguments#text)：完全匹配的字符串。正在支持模式匹配。有关详细信息，请参见[https://github.com/SeleniumHQ/selenium-ide/issues/141](https://github.com/SeleniumHQ/selenium-ide/issues/141)。
    

* * *

[](#assert-selected-label)`assert selected label`
-------------------------------------------------

确认下拉菜单中所选选项的标签包含提供的值。如果断言失败，则测试将停止。

**论点**

*   [select locator](/archives/selenium-ide-arguments#selectlocator)：标识下拉菜单的元素定位器。
    
*   [text](/archives/selenium-ide-arguments#text)：完全匹配的字符串。正在支持模式匹配。有关详细信息，请参见[https://github.com/SeleniumHQ/selenium-ide/issues/141](https://github.com/SeleniumHQ/selenium-ide/issues/141)。
    

* * *

[](#assert-text)`assert text`
-----------------------------

确认元素的文本包含提供的值。如果断言失败，则测试将停止。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [text](/archives/selenium-ide-arguments#text)：完全匹配的字符串。正在支持模式匹配。有关详细信息，请参见[https://github.com/SeleniumHQ/selenium-ide/issues/141](https://github.com/SeleniumHQ/selenium-ide/issues/141)。
    

* * *

[](#assert-title)`assert title`
-------------------------------

确认当前页面的标题包含提供的文本。如果断言失败，则测试将停止。

**论点**

*   [text](/archives/selenium-ide-arguments#text)：完全匹配的字符串。正在支持模式匹配。有关详细信息，请参见[https://github.com/SeleniumHQ/selenium-ide/issues/141](https://github.com/SeleniumHQ/selenium-ide/issues/141)。

* * *

[](#assert-value)`assert value`
-------------------------------

确认输入字段的（空白修饰）值（或其他带有value参数的值）。对于复选框/单选元素，根据是否选中该元素，其值为“ on”或“ off”。如果断言失败，则测试将停止。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [text](/archives/selenium-ide-arguments#text)：完全匹配的字符串。正在支持模式匹配。有关详细信息，请参见[https://github.com/SeleniumHQ/selenium-ide/issues/141](https://github.com/SeleniumHQ/selenium-ide/issues/141)。
    

* * *

[](#check)`check`
-----------------

检查一个切换按钮（复选框/单选）。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。

* * *

[](#choose-cancel-on-next-confirmation)`choose cancel on next confirmation`
---------------------------------------------------------------------------

影响下一个确认警报。此命令将取消它。如果警报已经存在，则使用“ webdriver选择在可见确认时取消”。

* * *

[](#choose-cancel-on-next-prompt)`choose cancel on next prompt`
---------------------------------------------------------------

影响下一个警报提示。此命令将取消它。如果警报已经存在，则使用“ webdriver在可见的提示下选择取消”。

* * *

[](#choose-ok-on-next-confirmation)`choose ok on next confirmation`
-------------------------------------------------------------------

影响下一个确认警报。此命令将接受它。如果警报已经存在，请改用“ Webdriver在可见确认中选择确定”。

* * *

[](#click)`click`
-----------------

单击目标元素（例如，链接，按钮，复选框或单选按钮）。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。

* * *

[](#click-at)`click at`
-----------------------

单击目标元素（例如，链接，按钮，复选框或单选按钮）。坐标是相对于目标元素的（例如，0,0是元素的左上角），并且主要用于检查在其上传递的效果，例如材料波纹效果。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [坐标字符串](/archives/selenium-ide-arguments#coordstring)：指定鼠标事件相对于从定位器找到的元素的x，y位置（例如-10,20）。
    

* * *

[](#close)`close`
-----------------

关闭当前窗口。无需关闭初始窗口，IDE会重新使用它；关闭它可能会导致测试性能下降。

* * *

[](#debugger)`debugger`
-----------------------

中断执行并进入调试器

* * *

[](#do)`do`
-----------

创建一个至少执行一次执行命令的循环。使用repeat if命令终止分支。

* * *

[](#double-click)`double click`
-------------------------------

双击元素（例如，链接，按钮，复选框或单选按钮）。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。

* * *

[](#double-click-at)`double click at`
-------------------------------------

双击目标元素（例如，链接，按钮，复选框或单选按钮）。坐标是相对于目标元素的（例如，0,0是元素的左上角），并且主要用于检查在其上传递的效果，例如材料波纹效果。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [坐标字符串](/archives/selenium-ide-arguments#coordstring)：指定鼠标事件相对于从定位器找到的元素的x，y位置（例如-10,20）。
    

* * *

[](#drag-and-drop-to-object)`drag and drop to object`
-----------------------------------------------------

拖动一个元素并将其拖放到另一个元素上。

**论点**

*   [要拖动的对象](/archives/selenium-ide-arguments#locatorofobjecttobedragged)的定位器：[要拖动](/archives/selenium-ide-arguments#locatorofobjecttobedragged)的元素的定位器。
    
*   [拖动目标对象](/archives/selenium-ide-arguments#locatorofdragdestinationobject)的定位器：放置元素（其位置（例如，其中的最中心像素）将成为要拖动的对象的定位器）的点的定位器。
    

* * *

[](#echo)`echo`
---------------

将指定的消息打印到Selenese表中的第三个表单元格中。对于调试很有用。

**论点**

*   [message](/archives/selenium-ide-arguments#message)：要打印的消息。

* * *

[](#edit-content)`edit content`
-------------------------------

设置内容可编辑元素的值，就像您在其中键入一样。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [value](/archives/selenium-ide-arguments#value)：要输入的值。
    

* * *

[](#else)`else`
---------------

if块的一部分。如果不满足if和/或else if条件，请在此分支中执行命令。使用end命令终止分支。

* * *

[](#else-if)`else if`
---------------------

if块的一部分。如果不满足if条件，请在此分支中执行命令。使用end命令终止分支。

**论点**

*   [条件表达式](/archives/selenium-ide-arguments#conditionalexpression)：JavaScript表达式，它返回布尔值以用于控制流命令。

* * *

[](#end)`end`
-------------

终止控制流块是否为时，为时和为时间。

* * *

[](#execute-script)`execute script`
-----------------------------------

在当前选定的框架或窗口的上下文中执行一段JavaScript。脚本片段将作为匿名函数的主体执行。要存储返回值，请使用“ return”关键字，并在值输入字段中提供一个变量名称。

**论点**

*   [script](/archives/selenium-ide-arguments#script)：要运行的JavaScript代码段。
    
*   [变量名](/archives/selenium-ide-arguments#variablename)：不带括号的[变量名](/archives/selenium-ide-arguments#variablename)。
    

* * *

[](#execute-async-script)`execute async script`
-----------------------------------------------

在当前选定的框架或窗口的上下文中执行JavaScript的异步代码段。该脚本片段将作为匿名函数的主体执行，并且必须返回Promise。如果您使用'return'关键字，则Promise结果将保存在变量中。

**论点**

*   [script](/archives/selenium-ide-arguments#script)：要运行的JavaScript代码段。
    
*   [变量名](/archives/selenium-ide-arguments#variablename)：不带括号的[变量名](/archives/selenium-ide-arguments#variablename)。
    

* * *

[](#for-each)`for each`
-----------------------

创建一个循环，为给定集合中的每个项目执行执行命令。

**论点**

*   [数组变量名称](/archives/selenium-ide-arguments#arrayvariablename)：包含JavaScript数组的变量的名称。
    
*   [迭代器变量名称](/archives/selenium-ide-arguments#iteratorvariablename)：在循环控制流命令中迭代集合时使用的[变量名称](/archives/selenium-ide-arguments#iteratorvariablename)（例如，每个变量）。
    

* * *

[](#if)`if`
-----------

在测试中创建一个条件分支。使用end命令终止分支。

**论点**

*   [条件表达式](/archives/selenium-ide-arguments#conditionalexpression)：JavaScript表达式，它返回布尔值以用于控制流命令。

* * *

[](#mouse-down)`mouse down`
---------------------------

模拟用户按下鼠标左键（尚未释放它）。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。

* * *

[](#mouse-down-at)`mouse down at`
---------------------------------

模拟用户在指定位置按下鼠标左键（尚未释放它）。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [坐标字符串](/archives/selenium-ide-arguments#coordstring)：指定鼠标事件相对于从定位器找到的元素的x，y位置（例如-10,20）。
    

* * *

[](#mouse-move-at)`mouse move at`
---------------------------------

模拟用户在指定元素上按下鼠标按钮（尚未释放它）。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [坐标字符串](/archives/selenium-ide-arguments#coordstring)：指定鼠标事件相对于从定位器找到的元素的x，y位置（例如-10,20）。
    

* * *

[](#mouse-out)`mouse out`
-------------------------

模拟用户将鼠标指针从指定元素移开。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。

* * *

[](#mouse-over)`mouse over`
---------------------------

模拟用户将鼠标悬停在指定元素上。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。

* * *

[](#mouse-up)`mouse up`
-----------------------

模拟当用户释放鼠标按钮时发生的事件（例如，停止按住按钮）。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。

* * *

[](#mouse-up-at)`mouse up at`
-----------------------------

模拟当用户在指定位置释放鼠标按钮（例如，停止按住按钮时）时发生的事件。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [坐标字符串](/archives/selenium-ide-arguments#coordstring)：指定鼠标事件相对于从定位器找到的元素的x，y位置（例如-10,20）。
    

* * *

[](#open)`open`
---------------

打开URL，然后等待页面加载，然后继续。这既接受相对URL，也接受绝对URL。

**论点**

*   [url](/archives/selenium-ide-arguments#url)：要打开的URL（可以是相对的或绝对的）。

* * *

[](#pause)`pause`
-----------------

等待指定的时间。

**论点**

*   [等待时间](/archives/selenium-ide-arguments#waittime)：[等待时间](/archives/selenium-ide-arguments#waittime)（以毫秒为单位）。

* * *

[](#remove-selection)`remove selection`
---------------------------------------

使用选项定位器从多选元素中的一组选定选项中删除一个选择。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [option](/archives/selenium-ide-arguments#option)：一个选项定位器，通常只是一个选项标签（例如“ John Smith”）。
    

* * *

[](#repeat-if)`repeat if`
-------------------------

有条件地终止“执行”控制流分支。如果提供的条件表达式的结果为true，则它将开始do循环。否则，它将结束循环。

**论点**

*   [条件表达式](/archives/selenium-ide-arguments#conditionalexpression)：JavaScript表达式，它返回布尔值以用于控制流命令。

* * *

[](#run)`run`
-------------

从当前项目运行测试用例。

**论点**

*   [测试用例](/archives/selenium-ide-arguments#testcase)：项目中的测试用例名称。

* * *

[](#run-script)`run script`
---------------------------

在当前测试窗口的主体中创建一个新的“ script”标记，并将指定的文本添加到命令主体中。请注意，这些脚本标记中引发的JS异常不是由Selenium管理的，因此，如果脚本有可能引发异常，则应该将脚本包装在try / catch块中。

**论点**

*   [script](/archives/selenium-ide-arguments#script)：要运行的JavaScript代码段。

* * *

[](#select)`select`
-------------------

使用选项定位器从下拉菜单中选择一个元素。选项定位符提供了指定选择元素的不同方法（例如，label =，value =，id =，index =）。如果未提供选项定位符前缀，则将尝试在标签上进行匹配。

**论点**

*   [select locator](/archives/selenium-ide-arguments#selectlocator)：标识下拉菜单的元素定位器。
    
*   [option](/archives/selenium-ide-arguments#option)：一个选项定位器，通常只是一个选项标签（例如“ John Smith”）。
    

* * *

[](#select-frame)`select frame`
-------------------------------

在当前窗口中选择一个框架。您可以通过从0开始的索引号来选择帧（例如，选择“ index = 0”的第一帧或“ index = 2”的第三帧）。对于嵌套框架，您将需要多次调用此命令（对树中的每个框架都必须调用一次，直到到达所需的框架为止）。您可以使用“ relative = parent”选择父框架。要返回页面顶部，请使用“ relative = top”。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。

* * *

[](#select-window)`select window`
---------------------------------

使用窗口定位器选择弹出窗口。选择弹出窗口后，所有命令都将转到该窗口。窗口定位器使用手柄选择窗口。

**论点**

*   [窗口句柄](/archives/selenium-ide-arguments#windowhandle)：代表特定页面（选项卡或窗口）的句柄。

* * *

[](#send-keys)`send keys`
-------------------------

模拟指定元素上的击键事件，就像您按键键入值一样。这模拟真实用户在指定字符串中键入每个字符；它也受到实际用户的限制，例如不能键入不可见或只读元素。这对于需要显式键事件的动态UI小部件（如自动完成组合框）很有用。与简单的“类型”命令直接将指定的值强制进入页面不同，该命令不会替换现有内容。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [按键序列](/archives/selenium-ide-arguments#keysequence)：可以键入的按键序列可用于发送按键（例如$ {KEY\_ENTER}）。
    

* * *

[](#set-speed)`set speed`
-------------------------

设置执行速度（例如，设置每次Selenium操作之后的延迟的毫秒长度）。默认情况下，不存在此类延迟，例如，延迟为0毫秒。此设置是全局设置，将影响所有测试运行，直到更改。

**论点**

*   [等待时间](/archives/selenium-ide-arguments#waittime)：[等待时间](/archives/selenium-ide-arguments#waittime)（以毫秒为单位）。

* * *

[](#set-window-size)`set window size`
-------------------------------------

设置浏览器的窗口大小，包括浏览器的界面。

**论点**

*   [resolution](/archives/selenium-ide-arguments#resolution)：使用WidthxHeight指定窗口分辨率。（例如1280x800）。

* * *

[](#store)`store`
-----------------

将目标字符串另存为变量，以方便重用。

**论点**

*   [text](/archives/selenium-ide-arguments#text)：要使用的文本。
    
*   [变量名](/archives/selenium-ide-arguments#variablename)：不带括号的[变量名](/archives/selenium-ide-arguments#variablename)。
    

* * *

[](#store-attribute)`store attribute`
-------------------------------------

获取元素属性的值。在不同的浏览器中，属性的值可能有所不同（例如，“样式”属性就是这种情况）。

**论点**

*   [属性定位符](/archives/selenium-ide-arguments#attributelocator)：元素定位符，后跟@符号，然后是属性名称，例如“ foo @ bar”。
    
*   [变量名](/archives/selenium-ide-arguments#variablename)：不带括号的[变量名](/archives/selenium-ide-arguments#variablename)。
    

* * *

[](#store-json)`store json`
---------------------------

未定义

**论点**

*   [json](/archives/selenium-ide-arguments#json)：JavaScript对象的字符串表示形式。
    
*   [变量名](/archives/selenium-ide-arguments#variablename)：不带括号的[变量名](/archives/selenium-ide-arguments#variablename)。
    

* * *

[](#store-text)`store text`
---------------------------

获取元素的文本并将其存储以备后用。这适用于任何包含文本的元素。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [变量名](/archives/selenium-ide-arguments#variablename)：不带括号的[变量名](/archives/selenium-ide-arguments#variablename)。
    

* * *

[](#store-title)`store title`
-----------------------------

获取当前页面的标题。

**论点**

*   [text](/archives/selenium-ide-arguments#text)：要使用的文本。
    
*   [变量名](/archives/selenium-ide-arguments#variablename)：不带括号的[变量名](/archives/selenium-ide-arguments#variablename)。
    

* * *

[](#store-value)`store value`
-----------------------------

获取element的值并将其存储以供以后使用。这适用于任何输入类型元素。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [变量名](/archives/selenium-ide-arguments#variablename)：不带括号的[变量名](/archives/selenium-ide-arguments#variablename)。
    

* * *

[](#store-window-handle)`store window handle`
---------------------------------------------

获取当前页面的句柄。

**论点**

*   [窗口句柄](/archives/selenium-ide-arguments#windowhandle)：代表特定页面（选项卡或窗口）的句柄。

* * *

[](#store-xpath-count)`store xpath count`
-----------------------------------------

获取与指定xpath匹配的节点数（例如，“ // table”将给出表数）。

**论点**

*   [xpath](/archives/selenium-ide-arguments#xpath)：要评估的xpath表达式。
    
*   [变量名](/archives/selenium-ide-arguments#variablename)：不带括号的[变量名](/archives/selenium-ide-arguments#variablename)。
    

* * *

[](#submit)`submit`
-------------------

提交指定的表格。这对于没有提交按钮的表单特别有用，例如单输入“搜索”表单。

**论点**

*   [表单定位器](/archives/selenium-ide-arguments#formlocator)：您要提交的表单的元素定位器。

* * *

[](#times)`times`
-----------------

创建一个循环执行n次执行命令。

**论点**

*   [times](/archives/selenium-ide-arguments#times)：控制流循环将执行其块内命令的尝试次数。
    
*   [循环限制](/archives/selenium-ide-arguments#looplimit)：一个可选参数，指定循环控制流命令可以执行的最大次数。这样可以防止无限循环。默认值设置为1000。
    

* * *

[](#type)`type`
---------------

设置输入字段的值，就像您在其中键入一样。也可以用于设置组合框，复选框等的值。在这种情况下，value应该是所选选项的值，而不是可见的文本。仅限Chrome：如果给出了文件路径，它将被上传到输入（对于type = file），注意：不支持XPath定位器。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [value](/archives/selenium-ide-arguments#value)：要输入的值。
    

* * *

[](#uncheck)`uncheck`
---------------------

取消选中切换按钮（复选框/单选）。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。

* * *

[](#verify)`verify`
-------------------

软断言变量是期望值。变量的值将转换为字符串以进行比较。即使验证失败，测试也将继续。

**论点**

*   [变量名](/archives/selenium-ide-arguments#variablename)：不带括号的[变量名](/archives/selenium-ide-arguments#variablename)。
    
*   [期望值](/archives/selenium-ide-arguments#expectedvalue)：您期望变量包含的结果（例如，true，false或其他某个值）。
    

* * *

[](#verify-checked)`verify checked`
-----------------------------------

软断言已选中切换按钮（复选框/单选）。即使验证失败，测试也将继续。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。

* * *

[](#verify-editable)`verify editable`
-------------------------------------

软断言指定的输入元素是否可编辑（例如，尚未禁用）。即使验证失败，测试也将继续。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。

* * *

[](#verify-element-present)`verify element present`
---------------------------------------------------

软断言指定的元素在页面上的某处。即使验证失败，测试也将继续。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。

* * *

[](#verify-element-not-present)`verify element not present`
-----------------------------------------------------------

软断言指定的元素不在页面上。即使验证失败，测试也将继续。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。

* * *

[](#verify-not-checked)`verify not checked`
-------------------------------------------

软断言未选中切换按钮（复选框/单选）。即使验证失败，测试也将继续。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。

* * *

[](#verify-not-editable)`verify not editable`
---------------------------------------------

软断言指定的输入元素是否不可编辑（例如，尚未禁用）。即使验证失败，测试也将继续。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。

* * *

[](#verify-not-selected-value)`verify not selected value`
---------------------------------------------------------

软断言所期望的元素尚未在其选择属性的选择菜单中选择。即使验证失败，测试也将继续。

**论点**

*   [select locator](/archives/selenium-ide-arguments#selectlocator)：标识下拉菜单的元素定位器。
    
*   [option](/archives/selenium-ide-arguments#option)：一个选项定位器，通常只是一个选项标签（例如“ John Smith”）。
    

* * *

[](#verify-not-text)`verify not text`
-------------------------------------

软断言元素的文本不存在。即使验证失败，测试也将继续。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [text](/archives/selenium-ide-arguments#text)：要使用的文本。
    

* * *

[](#verify-selected-label)`verify selected label`
-------------------------------------------------

对指定的select元素中的选定选项进行软断言。即使验证失败，测试也将继续。

**论点**

*   [select locator](/archives/selenium-ide-arguments#selectlocator)：标识下拉菜单的元素定位器。
    
*   [text](/archives/selenium-ide-arguments#text)：完全匹配的字符串。正在支持模式匹配。有关详细信息，请参见[https://github.com/SeleniumHQ/selenium-ide/issues/141](https://github.com/SeleniumHQ/selenium-ide/issues/141)。
    

* * *

[](#verify-selected-value)`verify selected value`
-------------------------------------------------

软断言所期望的元素已通过其选项属性在选择菜单中选择。即使验证失败，测试也将继续。

**论点**

*   [select locator](/archives/selenium-ide-arguments#selectlocator)：标识下拉菜单的元素定位器。
    
*   [option](/archives/selenium-ide-arguments#option)：一个选项定位器，通常只是一个选项标签（例如“ John Smith”）。
    

* * *

[](#verify-text)`verify text`
-----------------------------

软断言元素的文本存在。即使验证失败，测试也将继续。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [text](/archives/selenium-ide-arguments#text)：要使用的文本。
    

* * *

[](#verify-title)`verify title`
-------------------------------

软断言当前页面的标题包含提供的文本。即使验证失败，测试也将继续。

**论点**

*   [text](/archives/selenium-ide-arguments#text)：要使用的文本。

* * *

[](#verify-value)`verify value`
-------------------------------

软断言输入字段的（经空白修饰的）值（或带有value参数的其他任何值）。对于复选框/单选元素，根据是否选中该元素，其值为“ on”或“ off”。即使验证失败，测试也将继续。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [text](/archives/selenium-ide-arguments#text)：完全匹配的字符串。正在支持模式匹配。有关详细信息，请参见[https://github.com/SeleniumHQ/selenium-ide/issues/141](https://github.com/SeleniumHQ/selenium-ide/issues/141)。
    

* * *

[](#wait-for-element-editable)`wait for element editable`
---------------------------------------------------------

等待元素可编辑。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [等待时间](/archives/selenium-ide-arguments#waittime)：[等待时间](/archives/selenium-ide-arguments#waittime)（以毫秒为单位）。
    

* * *

[](#wait-for-element-not-editable)`wait for element not editable`
-----------------------------------------------------------------

等待元素不可编辑。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [等待时间](/archives/selenium-ide-arguments#waittime)：[等待时间](/archives/selenium-ide-arguments#waittime)（以毫秒为单位）。
    

* * *

[](#wait-for-element-not-present)`wait for element not present`
---------------------------------------------------------------

等待目标元素不出现在页面上。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [等待时间](/archives/selenium-ide-arguments#waittime)：[等待时间](/archives/selenium-ide-arguments#waittime)（以毫秒为单位）。
    

* * *

[](#wait-for-element-not-visible)`wait for element not visible`
---------------------------------------------------------------

等待目标元素在页面上不可见。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [等待时间](/archives/selenium-ide-arguments#waittime)：[等待时间](/archives/selenium-ide-arguments#waittime)（以毫秒为单位）。
    

* * *

[](#wait-for-element-present)`wait for element present`
-------------------------------------------------------

等待目标元素出现在页面上。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [等待时间](/archives/selenium-ide-arguments#waittime)：[等待时间](/archives/selenium-ide-arguments#waittime)（以毫秒为单位）。
    

* * *

[](#wait-for-element-visible)`wait for element visible`
-------------------------------------------------------

等待目标元素在页面上可见。

**论点**

*   [locator](/archives/selenium-ide-arguments#locator)：元素定位器。
    
*   [等待时间](/archives/selenium-ide-arguments#waittime)：[等待时间](/archives/selenium-ide-arguments#waittime)（以毫秒为单位）。
    

* * *

[](#webdriver-answer-on-visible-prompt)`webdriver answer on visible prompt`
---------------------------------------------------------------------------

影响当前显示的警报提示。此命令指示Selenium为它提供指定的答案。如果尚未出现警报，请改用“在下一个提示时回答”。

**论点**

*   [答案](/archives/selenium-ide-arguments#answer)：提示弹出窗口时给出的答案。

* * *

[](#webdriver-choose-cancel-on-visible-confirmation)`webdriver choose cancel on visible confirmation`
-----------------------------------------------------------------------------------------------------

影响当前显示的确认警报。此命令指示Selenium取消它。如果警报尚未出现，请改用“在下次确认时选择取消”。

* * *

[](#webdriver-choose-cancel-on-visible-prompt)`webdriver choose cancel on visible prompt`
-----------------------------------------------------------------------------------------

影响当前显示的警报提示。此命令指示Selenium取消它。如果警报尚未出现，请改用“在下一个提示时选择取消”。

* * *

[](#webdriver-choose-ok-on-visible-confirmation)`webdriver choose ok on visible confirmation`
---------------------------------------------------------------------------------------------

影响当前显示的确认警报。此命令指示Selenium接受它。如果警报尚未出现，请改用“在下次确认时选择确定”。

* * *

[](#while)`while`
-----------------

只要提供的条件表达式为true，就创建一个循环重复执行执行命令的循环。

**论点**

*   [条件表达式](/archives/selenium-ide-arguments#conditionalexpression)：JavaScript表达式，它返回布尔值以用于控制流命令。
    
*   [循环限制](/archives/selenium-ide-arguments#looplimit)：一个可选参数，指定循环控制流命令可以执行的最大次数。这样可以防止无限循环。默认值设置为1000。
    

* * *