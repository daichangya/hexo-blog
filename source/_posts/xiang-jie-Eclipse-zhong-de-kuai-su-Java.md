---
title: 详解Eclipse中的快速Java编码（代码模板）
id: 90ec4d02-c627-40cf-aed9-ac27b71682d4
date: 2024-12-10 09:51:09
author: daichangya
excerpt: 一、简介 Eclipse提供了通过定义和使用代码模板来提高工作效率与代码可预测性的能力。本文介绍如何编辑现有的代码模板以及定义新的代码模板，还包括内置变量的例子，展示在编辑器中这些内置变量被解析成的内容。
  问题 缺乏一致性：团队多人编辑或个人遗忘编写方式时，代码易出现差异，难以搜索和维护。 工作效率
permalink: /archives/xiang-jie-Eclipse-zhong-de-kuai-su-Java/
categories:
- 其他
---

## 一、简介
Eclipse提供了通过定义和使用代码模板来提高工作效率与代码可预测性的能力。本文介绍如何编辑现有的代码模板以及定义新的代码模板，还包括内置变量的例子，展示在编辑器中这些内置变量被解析成的内容。

### 问题
1. **缺乏一致性**：团队多人编辑或个人遗忘编写方式时，代码易出现差异，难以搜索和维护。
2. **工作效率不高**：编辑代码主要是打字工作，键入或复制粘贴大段代码花费时间多。

### 代码模板
代码模板虽能提高效率，但不能替代真正的代码重用（如编写方法或函数）。使用模板前，常用手动提高一致性和效率的方法是复制粘贴并修改。而使用Eclipse中的模板可解决上述问题，只需编写一次代码就能应用于整个应用程序。

## 二、调用模板
在编辑器中输入时，开始键入模板名称并使用Ctrl + Space调用代码完成功能，名称匹配的模板会出现在列表中（如图1）。若再次按Ctrl + Space，Eclipse会循环遍历模板类型。插入模板可使用箭头键选择后按Enter，也可鼠标双击模板名称。模板插入后，可用Tab键在变量间切换并键入变量值。

### 图1. 从列表中选择模板
![eclipse1.gif](https://images.jsdiff.com/eclipse1.gif)

## 三、编辑模板
通过选择Window > Preferences打开Eclipse Preferences，转到Java > Editor > Templates查看现有模板。单击列表中的模板并单击Edit编辑，Edit Template窗口出现（如图2）。

### 图2. 编辑模板
![eclipse2.gif](https://images.jsdiff.com/eclipse2.gif)


Edit Template窗口中各字段含义如下：
- **Name**：模板的名称。
- **Context**：模板的上下文。Eclipse将模板的选择限定于对该上下文有效的那些模板（如编辑XML文件时不会出现Java语句模板）。
- **Automatically insert**：若选中，Eclipse在模板全部名称输入完毕且调用模板插入后（如按Ctrl + Space）自动插入模板。
- **Description**：描述模板，出现在下拉列表中，有助于识别模板（模板名称不需唯一）。
- **Pattern**：作为模板插入的实际代码，包含需Eclipse解析的全部变量。

可编辑模板值，完成后单击OK。编辑模板时若要插入内置变量，可单击Insert Variable，更多变量信息可查阅“Taking advantage of variables in templates”。

## 四、创建模板
单击New创建模板，根据“编辑一个模板”部分介绍编辑值，完成后单击OK，新模板出现在列表内，最后单击OK编辑文件。

## 五、利用模板内的变量
使用模板的挑战是了解内置变量解析内容。变量可自动插入如当前类型名称、光标位置等内容，使模板更动态，减少手动更改工作量。

### 清单1. 面向登录声明的模板
`
${imp:import(java.util.logging.Logger)} 
   private static Logger logger = Logger.getLogger(${enclosing_type}.class.getName());
`
### 清单2. 在插入登录声明后的Automobile类
`
private static Logger logger = Logger.getLogger(Automobile.class.getName());
`

如清单1和2所示，类名称会自动解析，且Logger的导入声明自动添加在类顶端。

### 表2. Eclipse针对Java模板的内置变量
|变量名|描述|示例|
|---|---|---|
|cursor|将编辑器的光标放在这个位置|N/A|
|date|插入当前日期|Oct 20, 2009|
|dollar|插入货币的文字符号|$|
|elemType|尝试猜测具有给定ID的这个元素的类型|MyType|
|enclosing_method|插入模板被插入其中的那个方法的名称|method()|
|enclosing_method_arguments|为包围方法插入参数|arg1, arg2|
|enclosing_package|插入当前类的包名|com.example.ui|
|enclosing_project|插入包含所编辑的这个类的项目的名称|myProject|
|enclosing_type|插入正在编辑的类型（类）的名称|MyType|
|exception_variable_name|插入一个异常变量名称，进行最佳猜测|e, ioe|
|file|文件的简称|MyType.java|
|import|如果尚未导入，那么针对给定类型插入一个导入声明|import com.example.ui.MyOtherType|
|importStatic|与import相同，只不过是静态导入|import static com.example.ui.MyOtherType.*|
|line_selection|将选中的行插入到这里，对用模板包装行有用|以选中行作为主体的do、while循环|
|primary_type_name|没有扩展名的文件简称|MyType|
|time|插入当前的时间|9:09:35 a.m.|
|todo|注释中的TODO标记|TODO|
|user|当前用户的名字|ngood|
|var|解析为本地变量，如果不只一个，就提供一个列表|myvar|
|word_selection|插入当前选中的单词|N/A|
|year|将现在的年份插入到代码中|2009|

也可创建自己的变量，在模板插入后输入值，键入的值会在变量出现的所有位置替换。如清单3模板：

### 清单3. 创建您自己的变量
`
public void test${my_variable}() { 
     String expected = "value"; ${my_object}.set${my_variable}(expected); 
     assertEquals("${message}", expected, ${my_object}.get${my_variable}); 
     }
`

### 图3. 自动插入值
![eclipse3.gif](https://images.jsdiff.com/eclipse3.gif)

插入模板后，只需键入第一个值，其余自动替换，完成后按Tab移到下一个变量。

## 六、导出模板
为与他人共享模板，可将其导出到文件（XML格式，含模板信息，可导入到Eclipse其他实例）。选中模板并单击Export，Eclipse提示保存位置，完成导出后单击OK关闭Preferences窗口。

## 七、导入模板
可从包含导出模板的文件中导入模板。单击Import，Eclipse提示要导入的文件，导入后单击OK，新模板即可导入到编辑器中。

## 八、结束语
Eclipse内的代码模板是提高工作效率和应用程序一致性的有效方式。可构建自己的代码模板，在代码内定义变量以自动插入相关内容，还可通过导出和导入模板共享。例如，每次写小测试类时输入main方法很繁琐，可利用代码模板解决（如配置“psvm代码模板”）。编辑面板中关键五项如下：
- **Name**：名称，即以后可用的代码缩写。
- **Context**：模板上下文，指定模板生效位置（Java至少包含Java type members、Java statements、Java、Java doc等）。
- **模板变量**：Eclipse预置了一些（如${cursor}等），也可定义自己的变量。
- **Pattern**：代码模板对应的模式，按期望格式输入。

还可利用代码模板给类添加注释等。软件工程中工具高效使用能节省成本，应了解并发挥工具最大潜能。本文只对Java代码模板作了粗浅介绍，其在编写HTML代码时优势更大（如自定义“ul_list_menu”模板生成菜单代码）。

### 其他有用参考
- http://shareal.blog.163.com/blog/static/27659056201193063914196/
- http://www.coderli.com/eclipse-javadoc-template