---
title: 调试和测试 Swing 代码
id: 1191
date: 2024-10-31 22:01:50
author: daichangya
excerpt: 了解未知 Swing 代码的工具和方法简介： 当您需要使用或维护其他/她 Java™ 开发人员的代码时，调试和测试有助于您了解其运作方式。不过对于可视化代码，这些强大的实践方法更难运用，除非您有合适的工具。本文介绍的两个开源工具
  — Swing Explorer 和 FEST-Swing — 能使 Swing UI 调试
permalink: /archives/diao-shi-he-ce-shi-Swing-dai-ma/
tags:
- swing
---



Swing 是一个强大的 GUI 工具包；它可扩展、可配置且跨平台。不过 Swing 的灵活性既是它的主要优势也是它的重大弱点。Swing 可以不同的方式构建同一 UI。例如，您可以使用插页、空白边框或填充符在 GUI 组件之间置入间隔。鉴于 Swing 选项太多，了解现有 GUI 如同编写新 GUI 一样令人畏惧，且将其视觉外观与底层代码对应起来也并非易事。（试着在阅读几个使用 `GridBagLayout` 的代码行时想象一下 GUI。）

不管您是在维护未曾写过的 Swing GUI 还是集成第三方 GUI 组件到您的应用程序中，理解代码的一种合理方法是编写测试。在编写测试的同时您也就熟悉了未知代码的内部构造。这样做会同时产生另一个有价值的结果，即您最终会有一个测试套件，它有助于在维护代码时预防回归的引入。对于第三方 GUI 组件，测试套件有助于查明新版本的库是否引入了任何行为变化。

一开始最好先编写功能测试，以了解 GUI 如何响应用户输入。为 GUI 编写测试比为非可视化代码编写测试更复杂，因为：

*   理论上，测试必须是自动化的，但是 GUI 则是供人类 — 而非计算机程序 — 使用的。
*   传统的单元测试涉及到隔离类的测试，不适合 GUI 组件。在 GUI 术语中，一个 “单元” 涉及多个 GUI 组件的协作，因此它本身包含不止一个类。
*   GUI 响应用户生成的事件。要测试 GUI，你需要一种可以模拟用户输入的方法，一直等到生成的事件散播给所有侦听者，然后检查结果，就像 GUI 响应用户一样。编写模拟用户与 GUI 交互的代码会很繁琐且易出错。
*   更改 GUI 的布局不应影响强健的功能测试。

另外一个问题就是您必须事先熟知要测试的 GUI 的结构和行为，否则您不知道自动化测试应使用哪些组件，且哪些内容需要验证。总而言之，要编写 GUI 测试，您必须知道：

*   GUI 中用于测试的组件
*   如何在测试中惟一标识这样的组件
*   特定用例中组件的预期状态（或属性）

使用可视化设计工具（比如 NetBeans Matisse）您可以弄清 GUI 的结构。不过这种工具仅显示 GUI 的设计时信息，这会与您在运行时看到的不一样。例如，有些组件可能会根据用户输入而显示为可见或不可见。

传统的调试程序在执行特定用例时不能帮助您了解 GUI 的状态。当调试程序停在 Swing 代码中置入的断点时，GUI 绘图中断，使得 GUI 看起来像一个空白方框。理想情况下，*当* 您使用调试程序进行单步调试时您希望看到 GUI 运作的方式。

幸运的是，两个开源工具 — Swing Explorer 和 FEST-Swing — 可以帮助您快速了解现有 Swing 代码。本文向您介绍这些工具，向您展示如何结合使用它们检查应用程序的 GUI 结构，测试其功能，并识别潜在问题。

### 要探究的应用程序

对于文章的大部分示例，我将使用一种名为 HTMLDocumentEditor 的免费功能性 HTML 编辑器，将其作为要测试的应用程序（参见 [参考资料](#artrelatedtopics)）。如果您想自己完成示例，可以 [下载](#artdownload) 应用程序和样例测试代码。图 1 显示了运行中的 HTMLDocumentEditor：

##### 图 1\. HTML 编辑器

![HTML 编辑器应用程序截图](https://www.ibm.com/developerworks/cn/java/j-swingtest/htmleditor.jpg)


在编写 GUI 测试之前，您需要了解 GUI 的构成方式。HTML 编辑器很简单，包含一个文本区域和若干用于打开、保存和编辑 HTML 文档的菜单。

熟悉每个组件的具体类型也是很重要的。这将有助于您了解 GUI 组件通过 API 为您提供哪些动作或属性用于测试。对于 HTML 编辑器，您需要确定文本区域是否是 `JTextArea`、`JTextPane` 或一个通用的 GUI 组件。确定 GUI 组件类型的一种方法是检查源码。 根据 GUI 的实现方式，这可以是个简单工作，也可以是挑战性任务。HTMLDocumentEditor 的源码可读且易于掌握，快速检查该源码后发现文本区域是一个 `JTextPane`。但在您的技术生涯中，你很可能会遇到写得很差的 GUI 代码，非常难以理解。当这种情况发生时，您可以选择花费大量时间破译代码，也可以选择寻找一种可提供有效帮助的工具。

## Swing Explorer 简介

Swing Explorer 允许您可视地检查 Swing GUIs 的内部结构（参见 [参考资料](#artrelatedtopics)）。其简单直观的 UI 使我们更易于：发现 GUI 中的所有组件，调查其绘制方式，检查任意时间的属性，等等。

Swing Explorer 可同时作为独立应用程序和插件在 Eclipse 和 NetBeans 中使用。建议通过 IDE 插件使用它。在本文中，我将使用 Eclipse 插件（参见 [参考资料](#artrelatedtopics)）。

安装插件之后，我使用 Swing Explorer 启动了 HTML 编辑器主类，如图 2 所示：

##### 图 2\. Swing Explorer 中启动的编辑器应用程序

![强调三个窗口视图的 Swing Explorer 截图](https://www.ibm.com/developerworks/cn/java/j-swingtest/swingexplorer.jpg)


Swing Explorer 提供多个视图帮助您查明 Swing GUI 的内部构造：

1.  显示组件层次结构的一个树视图
2.  检查中的 GUI
3.  一个选项卡面板，显示选中组件（名称、大小等）的属性，且包含其他有用、有趣的工具（参见 [参考资料](#artrelatedtopics) 了解详情）

使用 Swing Explorer 了解 GUI 的构造很简单。出于本练习的需要，假定您不能通过阅读源码查明在 HTML 编辑器中用作文本区域的组件的类型。通过 Swing Explorer，您仅需选择组件树视图上的文本区域或单击 GUI 中显示的组件本身。在下面的图 3 中，Swing Explorer 确认文本区域是一个 `JTextPane`：

##### 图 3\. 显示选中组件属性的 Swing Explorer

![显示选中组件的 Swing Explorer 截图](https://www.ibm.com/developerworks/cn/java/j-swingtest/selected.jpg)


## 了解和测试应用程序行为

一旦确定要测试的 GUI 的结构，下一步就要了解应用程序的行为，这样才能知道要验证的期望值是哪些。这可以通过不同的方式完成：会见当前终端用户，阅读应用程序文档（如果有的话）或仅仅使用应用程序本身。

一开始我要选择两个用例进行测试：

1.  打开一个 HTML 文件
2.  改变文档字体的颜色

现在我准备开始编写功能 GUI 测试了。

功能 GUI 测试验证应用程序是否按预期运行。它专注于应用程序的行为，而非 GUI 的外观。 以下因素是创建强健的功能 GUI 测试所必不可少的：

*   能够模拟用户输入（键盘和鼠标）
*   拥有用于查找 GUI 组件的可靠机制
*   能够容许组件位置或布局的变化

### 空想：直接使用 `Robot`

要确保一个自动化测试能真正模拟用户输入，您需要生成操作系统级的 “原生” 事件，就像用户在使用键盘和鼠标一样。 JDK 自 1.3 版本以来通过 Abstract Window Toolkit (AWT) `Robot` 为输入模拟提供支持。不过 `Robot` 仅对屏幕坐标有效，而对 Swing 组件参考无效，因此直接使用它会使测试很脆弱，这意味着任何布局变化都会中止测试。

而且 AWT `Robot` 级别太低；它只知道如何单击鼠标按钮和按键。您需要编写能翻译高级动作的代码，比如*选择该组合框中的第三个元素* 放入 `Robot` 动作中。根据测试所需的动作数量和相关组件的不同类型，这需要大量工作。 另外，AWT `Robot` 不为组件查询（比如查找*带有文本 “OK” 的按钮*）提供可靠机制。您还是需要自己编写代码。

总而言之，直接使用 AWT `Robot` 需要大量精力和时间。当编写功能 GUI 测试时，您需要将注意力放在要查证的行为上，而不是放在使 GUI 测试成为可能的底层管道上。

### FEST-Swing 简介

FEST（Fixtures for Easy Software Testing）Swing 模块是能够轻松创建和维护强健的功能 GUI 测试的一个库。 它的主要特性包括：

*   建立于 AWT `Robot` 之上，用于模拟真实的用户输入。
*   有一个紧凑、直观、可读的连贯接口，能简化功能 GUI 测试的创建和维护。清单 1 显示了如何编码实现高级动作：*在 `firstName` 文本字段中输入 “luke” 文本然后单击 “ok” 按钮*。
    
    ##### 清单 1\. FEST-Swing 的连贯接口
    
    ```
    dialog.textBox("firstName").enterText("Luke");
    dialog.button("ok").click();
    ```
    
*   验证 GUI 组件状态的断言方法。清单 2 显示了一个断言，它验证了标签名为 “answer” 的文本是 “21”：
    
    ##### 清单 2\. FEST-Swing 的断言
    
    ```
    dialog.label("answer").requireText("21");
    ```
    
*   促进强健测试：布局变化*不会* 中断测试。
*   支持出现在 JDK 中的 Swing 组件。
*   支持 JUnit 4 和 TestNG。
*   为正确的 Swing 线程使用提供验证。
*   简化故障检修失败测试。

## 用 FEST-Swing 编写功能 GUI 测试

目前我们已经了解了编辑器应用程序的 GUI 的结构，收集了要测试的用例，找到了可靠的测试工具，终于可以开始编写功能 GUI 测试了。

### 用例：打开一个 HTML 文件

在 HTML 编辑器中打开文件需要执行以下操作：

1.  选择 File > Open 子菜单
2.  在显示的文件选择器中选择要打开的文件
3.  确保编辑器加载了文件内容

清单 3 显示了这一用例的代码：

##### 清单 3\. 打开 HTML 文件的测试

```
public class HTMLDocumentEditor_Test extends FestSwingJUnitTestCase {
 
 
   private FrameFixture editor;
 
   protected void onSetUp() {
     editor = new FrameFixture(robot(), createNewEditor());
     editor.show();
   }
 
   @RunsInEDT
   private static HTMLDocumentEditor createNewEditor() {
     return execute(new GuiQuery<HTMLDocumentEditor>() {
       protected HTMLDocumentEditor executeInEDT() {
         return new HTMLDocumentEditor();
       }
     });
   }
 
   @Test
   public void should_open_file() {
     editor.menuItemWithPath("File", "Open").click();
     JFileChooserFixture fileChooser = findFileChooser().using(robot());
     fileChooser.setCurrentDirectory(temporaryFolder())
                .selectFile(new File("helloworld.html"))
                .approve();
     assertThat(editor.textBox("document").text()).contains("Hello");
   }
}
```

以下内容详细介绍了清单 3 中的测试工作：

*   第一行扩展了 FEST-Swing 的 `FestSwingJUnitTestCase`。它提供对 FEST-Swing `Robot` 的自动创建，对正确 Swing 线程的验证（稍后详细介绍），对资源的自动清理（关闭打开的窗口，释放鼠标和键盘，等等）。
*   `editor = new FrameFixture(robot(), createNewEditor());` 创建一个新的 `FrameFixture`，能够在 `Frame` 上模拟用户输入，查询它内部的组件（使用多种搜索标准）并验证其状态。
*   `editor.show()；`在屏幕上显示 HTML 编辑器。
*   `@RunsInEDT` 用文档记录保证要在事件调度线程（EDT）中执行的 `createNewEditor()` 方法。
*   `return execute(new GuiQuery<HTMLDocumentEditor>()` 创建 EDT 中`HTMLDocumentEditor` 的一个新实例。
*   在 `editor.menuItemWithPath("File", "Open").click();` 中，FEST-Swing 模拟一个用户单击File > Open 子菜单。
*   在 `JFileChooserFixture fileChooser = findFileChooser().using(robot());` 中，FEST-Swing 查找由 HTML 编辑器启动的 “Open File” `JFileChooser`。
*   在接下来三行中，FEST-Swing 模拟用户选择位于系统临时文件夹中的 helloworld.html 文件。
*   `assertThat(editor.textBox("document").text()).contains("Hello");` 通过检查文件中是否包含 *Hello* 来验证是否将文件加载到了编辑器中。

注意，清单 3 按照名称（`editor`）查询 `JTextPane`。这是在一个测试中查找组件最可靠的方式；它保证组件查找从不失败，即使 GUI 的布局在将来会改变。

### 用例：改变文档字体的颜色

要验证 HTML 编辑器将文档字体的颜色改为黄色，您需要：

1.  选择 Color > Yellow 子菜单
2.  在编辑器中输入内容
3.  验证输入文本的颜色是黄色

清单 4 显示了如何使用 FEST-Swing 实现上述操作：

##### 清单 4\. 用于更改文档字体颜色的测试

```
@Test
public void should_change_document_color() {
  editor.menuItemWithPath("Color", "Yellow").click();
  JTextComponentFixture textBox = editor.textBox();
  textBox.enterText("Hello");
  assertThat(textBox.text()).contains("<font color=\"#ffff00\">Hello</font>");
}
```

到目前为止，我展示了如何测试简单的 GUI 组件，比如菜单和文本框。接下来我将介绍一种不太直观的测试模式。

### 更加复杂的测试

为展示 FEST-Swing 直观紧凑的 API，我将使用 Swing 的一个高度复杂的组件 — `JTable`。

我将使用 Sun 公司 Swing 教程中的 `TableDialogEditoDemo` 应用程序（参见 [参考资料](#artrelatedtopics)）。该应用程序使用带有定制编辑器的 `JTable`：`JComboBox`es 和 `JCheckBox`es，如图 4 所示：

##### 图 4\. `TableDialogEditDemo`

![TableDialogEditDemo 窗口截图](https://www.ibm.com/developerworks/cn/java/j-swingtest/table.jpg)


为用作示例，我将编写一个测试，模拟用户选择 0 行处组合框中的第二个元素。测试要执行的动作是：

1.  按需上下滚动表格使该行可见。
2.  单击第 0 行第 2 列的单元格。
3.  等待组合框出现。
4.  找到并单击组合框。
5.  从组合框中选择第二个元素。

这只是对我要编码的动作的粗略描述。编写真实代码并非微不足道的工作。幸运的是，FEST-Swing 的 API 简化了该任务，如清单 5 所示：

##### 清单 5\. 选择 0 行处组合框中的第三个元素

```
dialog.table.enterValue(row(0).column(2), "Knitting");
```

FEST-Swing 可以简化 GUI 测试甚至是复杂测试的编写和阅读。

## Swing 线程

Swing 是一个单线程 UI 工具包。因为它不是线程安全的，所以所有 Swing 代码必须在 EDT 中执行。如官方文档所述，从多线程中调用 Swing 代码会造成线程冲突或内存一致性错误（参见 [参考资料](#artrelatedtopics)）。

Swing 的线程策略状态：

*   Swing 组件必须在 EDT 中创建。
*   Swing 组件必须在 EDT 中进行访问，除非您调用文档化为线程安全的方法。

虽然这看起来很简单，不过很容易破坏规则。Swing 不为正确的 EDT 使用提供任何运行时检查，而且大部分时候表面上 “行为良好” 的 Swing UI 实际上却破坏了这些规则。

Swing Explorer 和 FEST-Swing 都支持查找 Swing 线程策略的违规行为。图 5 显示了 Swing Explorer 的 EDT 监视器。EDT 监视器可以在执行应用程序时报告 EDT 访问违规行为。

##### 图 5\. Swing Explorer 的 EDT 监视器

![EDT 监视器截图](https://www.ibm.com/developerworks/cn/java/j-swingtest/edtmonitor.jpg)


FEST-Swing 提供 `FailOnThreadViolationRepaintManager` 来检查 EDT 违规行为，如果检测到任何违规，它会强迫测试终止。配置很简单：在标有 `@BeforeClass` 注释的 set-up 方法中放入它，如清单 6 所示：

##### 清单 6\. 安装 `FailOnThreadViolationRepaintManager`

```
@BeforeClass public void setUpOnce() {
  FailOnThreadViolationRepaintManager.install();
}
```

另外， UI 测试可将 FEST-Swing 的 `FestSwingTestngTestCase` 或 `FestSwingJunitTestCase` 分为子类，这两个类均已安装了 `FailOnThreadViolationRepaintManager`。 FEST-Swing 也提供有用的抽象类来确保对 Swing 组件的访问是在 EDT 中完成的。欲了解更多信息，参见 [参考资料](#artrelatedtopics)。

## GUI 测试失败故障排除

不管编写功能 GUI 测试所用的库是什么，这种测试都易受到环境相关事件的攻击。FEST-Swing 也不例外。例如，一次预定的反病毒扫描可能弹出一个对话框来阻止正在测试的 GUI。FEST-Swing `Robot` 将不能访问 GUI 并最终因超时而强迫测试终止。测试失败不是程序错误造成的，只是不合时宜而已。

FEST-Swing 的一个非常有用的特性是它能够在测试失败时摄取桌面截图。当您在 IDE 内执行单个测试时，该截图会被自动嵌入到 JUnit 或 TestNG 报告中，或保存在目录中。图 6 显示了 GUI 测试失败后的一个 JUnit HTML 报告。注意测试失败时 FEST-Swing 添加到桌面截图中的链接。

##### 图 6\. 从失败测试链接到桌面截图的 JUnit HTML 报告

![JUnit HTML 报告截图](https://www.ibm.com/developerworks/cn/java/j-swingtest/junit-ext.jpg)


造成测试失败的另一个常见原因是组件查询失败。推荐的查询组件的方式是根据组件的惟一名称查询。有时您要测试的 GUI 的组件没有惟一名称，这时就只能使用通用的搜索标准。有两种类型的组件查询失败：

1.  *无法找到 GUI 组件。* 例如，假设您在查询名称为 `firstName` 的 `JTextField` ，但是原先的开发人员忘记将该名称赋给组件。在这种情况下，FEST-Swing 在抛出的 `ComponentLookupException` 中包含可用的组件层次结构，从而易于发现失败的原因。在本例中，您可以检查组件层次结构以查看 `JTextField` 是否有正确的名称，或是否真正将 `JTextField` 添加到 GUI。清单 7 显示了一个嵌入在 `ComponentLookupException` 中的组件层次结构：
    
    ##### 清单 7\. 包含组件层次结构的 `ComponentLookupException`
    
    ```
    org.fest.swing.exception.ComponentLookupException:
      Unable to find component using matcher
      org.fest.swing.core.NameMatcher[name='ok', requireShowing=false].
     
    Component hierarchy:
    myapp.MyFrame[name='testFrame', title='Test', enabled=true, showing=true]
      javax.swing.JRootPane[]
        javax.swing.JPanel[name='null.glassPane']
          javax.swing.JLayeredPane[]
            javax.swing.JPanel[name='null.contentPane']
            javax.swing.JTextField[name='name', text='Click Me', enabled=true]
    ```
    
      
    清单 7 中的组件层次结构有助于您推断出原先的开发人员为 `JTextField` 提供了错误的名称。当前名称不是 `firstName`，而应该是 `name`。
2.  *找到多个 GUI 组件。*这种情况会在有多个 GUI 组件匹配给定的搜索标准时发生。例如，`firstName` 可能被不小心提供给两个 `JTextField`。当查询名为 `firstName` 的 `JTextField` 时，查询就会失败（并终止测试），因为两个组件具有同一名称。为帮助您诊断这种问题，抛出的 `ComponentLookupException` 显示所有找到的匹配组件，如清单 8 所示：
    
    ##### 清单 8\. `ComponentLookupException` 包含与某个搜索标准匹配的组件列表
    
    ```
    org.fest.swing.exception.ComponentLookupException:
      Found more than one component using matcher
      org.fest.swing.core.NameMatcher[
        name='firstName', type=javax.swing.JTextField, requireShowing=false].
     
    Found:
    javax.swing.JTextField[name='firstName', text='', enabled=true]
    javax.swing.JTextField[name='firstName', text='', enabled=true]
    ```
    

有时，在抛出的 `ComponentLookupException` 中检查组件层次结构会很难，特别是当您在处理含有大量组件的 GUI 时。Swing Explorer 在这里再次提供很大的帮助。 如上所示，您仅需直接单击组件就可以选择和检查组件层级结构中任何组件的属性。大的组件层次结构在 Swing Explorer 的 GUI 中要比由 `ComponentLookupException` 提供的基于文本的表示要容易理解得多。

## 结束语

Swing 威力以其复杂度作为代价；理解 Swing 代码与编写该代码一样有挑战性。为探究未知 GUI 代码而编写测试比为非可视化代码编写测试要复杂。幸运的是，Swing Explorer 和 FEST-Swing 可以帮助您从这种单调乏味的工作中解脱出来。通过 Swing Explorer，您可以在应用程序运行时探究 GUI 的结构。一旦了解了要测试的 GUI 的结构和行为之后，您就可以使用 FEST-Swing 紧凑直观的 API 来编写功能 GUI 测试。除了其连贯 API 之外，FEST-Swing 验证 Swing 线程和特性的正确使用，这在检测失败的 GUI 测试时可帮助您节省时间。本文只介绍了这对强大工具的一些基本功能。

类似于 Swing Explorer 和 FEST-Swing 的一种更好的解决方案是一种记录/回放工具，它记录 Java 代码中的用户交互，如同它是由开发人员手动创建一样。记录/回放工具在最短的时间内为您提供测试套件。您与现有 GUI 交互，且用户生成的所有事件都记录在一个脚本中。稍后您可以回放该脚本，以为特定场景重新创建用户交互。现有记录/回放工具的主要弱点就是生成测试的维护很昂贵。应用程序的任何改变都需要重新记录所有测试场景。同时，在测试与以前类似的场景时，记录所有测试场景会创建重复的测试代码。记录的脚本通常很长，且用专用语言编写，缺乏面向对象（OO）的语言特性。重复动作的模块化需要很大的工作量，易于产生错误，且通常需要了解一种新的编程语言。

通过使用一个基于一种流行和成熟的 OO 语言 — Java 语言 — 的记录/回放工具，开发人员可享受功能丰富的 IDE 带来的诸多益处，这些 IDE 能将繁琐、易出错的任务（比如代码重构）变得快速且微不足道，从而可提高效率并降低维护成本。这正是 FEST 项目团队目前正专注的工作：开发一种回放/记录工具，它可以使用 FEST-Swing Java API 生成完全基于对象的 GUI 测试。我们希望在 2010 年第二季度之前能看到该工具。

* * *

#### 下载资源

*   [本文样例 GUI 测试](http://www.ibm.com/developerworks/apps/download/index.jsp?contentid=474266&filename=jswingtest-code.zip&method=http&locale=zh_CN) (jswingtest-code.zip | 1.28MB)

* * *

#### 相关主题

*   [Swing Explorer](https://swingexplorer.dev.java.net/)：访问 Swing Explorer 项目站点。
*   [FEST-Swing](http://fest.easytesting.org/swing/wiki/pmwiki.php)：查找文档、文章和软件下载链接。
*   “[Writing EDT-safe Swing UI tests](http://alexruiz.developerblogs.com/?p=160)”（Alex Ruiz 的博客，2009 年 7 月）：了解遵循 Swing 线程策略编写测试用例的步骤。
*   “[追求代码质量: 使用 TestNG-Abbot 实现自动化 GUI 测试](http://www.ibm.com/developerworks/cn/java/j-cq02277/)”（Andrew Glover，developerWorks，2007 年 2 月）：阅读 TestNG-Abbot 相关的 GUI 测试，TestNG-Abbot 是 FEST-Swing 之前的一种测试工具。
*   “[WYSIWYG Html Editor with JEditorPane and HTMLEditorKit](http://www.artima.com/forums/flat.jsp?forum=1&thread=1276)”（Artima.com，2002 年 2 月）：Charles Bell 在这里发布了 HTMLDocumentEditor 源。
*   [How to Use Tables](http://java.sun.com/docs/books/tutorial/uiswing/components/table.html)：这是关于如何使用表格的 Swing 教程。
*   [developerWorks Java 技术专区](http://www.ibm.com/developerworks/cn/java/)：可以找到几百篇关于 Java 编程的各个方面的文章。
*   [Swing Explorer](https://swingexplorer.dev.java.net/downloads.html)：下载 Swing Explorer 或 Swing Explorer 插件。
*   [FEST](http://code.google.com/p/fest/downloads/list)：下载 FEST-Swing。
