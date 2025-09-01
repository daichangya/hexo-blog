---
title: Spring Richclient — 企业级富客户端开发框架介绍
id: 473
date: 2024-10-31 22:01:43
author: daichangya
excerpt: "简介： 本系列文章的第 1 部分主要讲述了如何使用 Spring Richclient 构建企业级胖客户端应用，本文是该系列文章的第 2 部分，主要讲述与 Spring Richclient 架构相关的知识，从而使您更深入的了解该框架的设计思想。"
permalink: /archives/7690987/
categories:
 - java
---


## 前言

基于 Swing 的富客户端开发在企业级应用开发中占据了重要的地位，而可视化开发工具尽管提高了 Swing 的开发效率，却降低了程序的可维护性。在此情况下，诸多 Swing 开发框架应运而生，Spring Richclient 便是其中一个。作为 Spring 的子项目，Spring Richclient 承袭了 Spring 对企业级应用的支持。通过 Spring 容器，Spring Richclient 将各种客户端组件以松耦合的方式组织到一起，大大增加了应用程序的灵活性。同时，Spring Richclient 对 Swing 控件进行了优雅的封装，大大提高了 Swing UI 的开发效率。在本系列的第 1 部分中，我将向您介绍如何使用 Spring Richclient 快速搭建 Swing 富客户端应用。

## 环境搭建

首先您需要下载 Spring Richclient 相关发布包以及依赖库（查看参考资料），Spring Richclient 的最新版本为 1.1.0，由于 Spring Richclient 从 1.0 开始接口变化较大，建议您下载最新版本进行开发。

解压后，便可以看到 Spring Richclient 发布包共 4 个模块：

*   spring-richclient-core-1.1.0.jar 包含了 Spring Richclient 的所有核心功能
*   spring-richclient-jdk6-1.1.0.jar 包含了 Spring Richclient 基于 jdk6 新特性对核心功能的扩展，包括一个启动屏幕（SplashScreen）的实现、单选枚举的数据绑定、基于脚本的视图实现
*   spring-richclient-resources-1.1.0.jar 包含了 Spring Richclient 依赖的基础资源信息，包括图片信息和国际化信息
*   spring-richclient-sandbox-1.1.0.jar 作为 Spring Richclient 的沙箱模块，包含了一些非常实用的扩展功能

除此之外，Spring Richclient 发布包内还包括 spring-richclient-swingdocking-1.1.0.jar 和 spring-richclient-vldocking-1.1.0.jar，分别提供了两种视图 docking 的功能实现。从包名便不难看出，这两个功能是通过第三方库 swingdocking 和 vldocking 实现的。

接下来，您可以按照下列步骤在 Eclipse 中搭建 Spring Richclient 工程依赖环境：

1.  新建一个 Java Project：
    
    ##### 图 1\. 新建工程
    
    ![图 1. 新建工程](https://www.ibm.com/developerworks/cn/java/j-lo-spring-richclient1/image001.jpg)
    
    
    
2.  点击“Next”，设置 Spring Richclient 项目依赖库：
    
    ##### 图 2\. 设置依赖库
    
    ![图 2. 设置依赖库](https://www.ibm.com/developerworks/cn/java/j-lo-spring-richclient1/image002.jpg)
    
    
    
3.  点击“Finish”，完成工程创建。

现在便可以使用该环境开发 Spring Richclient 应用了，[图 2](#fig2) 仅列出了最基本的依赖库，如果使用 Spring Richclient 的其他功能，需要增加相应的依赖 jar 包（后续的系列文章将会详细介绍）。

## Hello World

本章我们将使用 Spring Richclient 开发一个简单的 Hello World 程序，初探该框架的独特之处。如 [清单 1](#listing1) 所示，只需要几行代码，我们便可以成功显示一个主窗体，效果如 [图 3](#fig3) 所示，这在 1.0 以前的版本是很难做到的，可见 Spring Richclient 项目组对框架的重大改进。

##### 清单 1\. Main 类

```
package org.springframework.richclient.example;
 
import org.springframework.richclient.application.Application;
 
public class Main {
 
    public static void main(String[] args) {
        Application app = new Application();
        try {
            app.afterPropertiesSet();
        } catch (Exception e) {
            e.printStackTrace();
        }
        app.start();
    }
 
}
```

##### 图 3\. 效果图

![图 3. 效果图](https://www.ibm.com/developerworks/cn/java/j-lo-spring-richclient1/image003.jpg)



很神奇吧？尽管略显单薄，可窗体已经有了菜单栏（因为我们没有配置任何菜单，所以菜单栏上显示为空）、状态栏。可这并不是我们想要的效果，即使是 Hello World 也不够。

在给该窗体添加一个 Hello World 视图之前，让我们变更一下程序的启动方式，采用 Spring 上下文的方式。开始您会觉得这样相对比较繁琐，可事实上 Spring 上下文使我们的应用程序更易于管理，大大增加了程序的可维护性和可扩展性，而且在后续讲解中您会发现，要使用编码的方式增加菜单、视图将是一个比较复杂的过程。Spring 上下文也是推荐的 Spring Richclient 项目的开发方式。Spring 上下文配置和启动代码分别如 [清单 2](#listing2) 和 [清单 3](#listing3) 所示

##### 清单 2\. application.xml

```
<?xml version="1.0" encoding="GB2312"?>
<!DOCTYPE beans PUBLIC  "-//SPRING//DTD BEAN//EN"
 "http://www.springframework.org/dtd/spring-beans.dtd">
<beans>
    <bean id="application"
        class="org.springframework.richclient.application.Application">
    </bean>
</beans>
```

##### 清单 3\. Main 类

```
package org.springframework.richclient.example;
 
import org.springframework.richclient.application.ApplicationLauncher;
 
public class Main {
 
    public static void main(String[] args) {
        new ApplicationLauncher("", new String[]
        {"org/springframework/richclient/example/application.xml"});
    }
 
}
```

从 [清单 3](#listing3) 可以看出，Spring Richclient 是通过 ApplicationLauncher 加载 Spring 上下文和启动应用程序的。该类构造方法包括两个参数，第一个为启动屏幕配置（同样是 Spring 配置文件，如果不希望有启动屏幕，则可以为空），第二个为 Spring 配置文件列表。Spring Richclient 之所以将启动屏幕的配置与其他上下文配置分开，是因为这样可以将其他配置文件的加载延迟到与启动屏幕显示同步，加快了程序启动，而且这也是启动屏幕功能的初衷。

接下来，让我们增加一个 WelcomeView 视图作为我们的默认启动视图，显示我们的“Hello World”。

首先，我们先来完成 WelcomeView 视图的代码，所有视图均需要实现接口 View，而一般情况下，我们仅需要继承其抽象类 AbstractView 即可，代码如 [清单 4](#listing4) 所示。

##### 清单 4\. WelcomeView 类

```
package org.springframework.richclient.sample.view;
 
import javax.swing.JComponent;
import javax.swing.JLabel;
 
import org.springframework.richclient.application.support.AbstractView;
 
public class WelcomeView extends AbstractView{
 
    @Override
    protected JComponent createControl() {
        return new JLabel("Hello World");
    }
 
}
```

很简单，我们只需要添加一个 JLabel 来显示我们的“Hello World”。

Spring Richclient 默认视图是通过应用程序生命周期管理类 ApplicationLifecycleAdvisor 维护的，从命名看类似于 Spring AOP 中的 Advisor，不过此类是在窗体创建以及销毁过程中手动调用的，在这里我们使用它的默认实现 DefaultApplicationLifecycleAdvisor。

作为企业级应用，我们还需要对国际化信息以及图片资源等进行管理，Spring Richclient 也已经为我们想到了，这些信息维护在类 DefaultApplicationServices 以及静态调用类 ApplicationServicesLocator 中。当然对于框架来说是面向接口编程的，但是这里使用 Spring Richclient 的默认设置即可，application.xml 的配置信息过长，不再详细列出，具体可参见示例工程，关于 WelcomeView 的配置如 [清单 5](#listing5)，所有 View 均配置为 DefaultViewDescriptor 类型的 Bean，这也是出于性能上的考虑，通过这种方式，View 实现了延时创建。当然如果您想给 View 设置属性，可直接将其注入到 DefaultViewDescriptor 的 viewProperties 属性，这是一个 Map，Key 为 View 中的属性名，Value 为希望注入的 Bean 或数值。DefaultViewDescriptor 创建 View 实例时，会自动为您完成注入。另外，WelcomeView 之所以会作为默认视图显示，是因为我们将其注入到了 lifecycleAdvisor 的 startingPageId 属性。效果如 [图 4](#fig4) 所示。

##### 清单 5\. WelcomeView Bean 配置

```
<bean id="welcomeView"
    class="org.springframework.richclient.application.support.DefaultViewDescriptor">
    <property name="viewClass"
        value="org.springframework.richclient.sample.view.WelcomeView" />
</bean>
<bean id="lifecycleAdvisor"
    class="org.springframework.richclient.application.
    config.DefaultApplicationLifecycleAdvisor">
    <property name="windowCommandBarDefinitions"
        value="org/springframework/richclient/sample/commands-context-sample.xml" />
    <property name="startingPageId" value="welcomeView" />
    <property name="menubarBeanName" value="menuBar" />
</bean>
```

##### 图 4\. 效果图

![图 4. 效果图](https://www.ibm.com/developerworks/cn/java/j-lo-spring-richclient1/image004.jpg)



至此，我们的 Hello World 便完成了，它拥有标题，而且完全支持国际化，如果您愿意，还可以在资源文件中为其配置图标（对，不需要编写代码，仅仅需要配置）。这些如果使用编码方式实现将是一个多么繁琐的过程，而使用 Spring Richclient 仅需要简单的配置即可，自始至终我们仅编写过一个视图类和启动类。也许您会发现除了欢迎界面外，还增加了一个“File”菜单，那么菜单是如何加上去的呢（细心的您可能已经从 [清单 5](#listing5) 中发现了些许端倪）？ Spring Richclient 还有哪些让我们眼前一亮的特性呢？让我们继续。

## 进阶

作为 Hello World 程序，上述工作已经足够，可它与企业应用毫不沾边。如果 Spring Richclient 仅仅为我们做了这些工作，剩下的还是手动编写 Swing 控件，那么它就不会引起我们过多的关注。令人欣慰的是，Spring Richclient 不但为我们的应用程序提供了一个扩展性和维护性良好的架构，而且还为我们提供了各式各样的组件封装，下面我们将分几节讲解 Spring Richclient 最常见的几种组件封装，最终构建一个企业级富客户端界面的雏形，效果如 [图 5](#fig5) 所示：

##### 图 5\. UserManageView

![图 5. UserManageView](https://www.ibm.com/developerworks/cn/java/j-lo-spring-richclient1/image005.jpg)



从 [图 5](#fig5) 可以看出，我们的管理界面包含了查询 Form、表格、按钮（而且按钮均拥有快捷键）。当然，如果您运行示例工程，并且点击其中的 Add 或者 Modify 按钮，您将会看到 Spring Richclient 的对话框，充分领略 Spring Richclient 对话框为我们带来的便捷。

### Command

为了简化按钮的创建与初始化，Spring Richclient 将具有按钮特性的控件（菜单项、工具栏按钮、普通按钮）抽象为 AbstractCommand，对于使用者来说，仅仅需要指定 CommandId（用于国际化以及配置图片信息）和具体的响应处理即可（即 AbstractCommand 类的抽象方法）。而且为了实现树状结构的按钮（菜单），Spring Richclient 提供了一个 CommandGroup 类（继承自 AbstractCommand），它的子节点可以是 AbstractCommand 和 CommandGroup。

AbstractCommand 分别提供了创建按钮和菜单项的方法，而 CommandGroup 则提供了创建菜单、工具栏和按钮栏的方法（[图 5](#fig5) 下方的按钮栏便是通过 CommandGroup 创建的）。最常用的 AbstractCommand 子类为 ActionCommand（用于创建普通按钮）、ShowViewCommand（用于创建弹出视图的菜单项）、ShowPageCommand（用于创建弹出页面的菜单项）、CommandGroup。如 [清单 6](#listing6) 所示，我们可以创建普通按钮栏。

##### 清单 6\. 创建按钮栏的代码

```
//创建增加按钮
addCommand = new ActionCommand("addCommand") {
 
    @Override
    protected void doExecuteCommand() {
        //TODO 按钮响应代码
    }
};
//创建按钮栏
CommandGroup.createCommandGroup(
    new Object[] { addCommand, modifyCommand, deleteCommand })
        .createButtonBar();
```

##### 清单 7\. 按钮国际化（sampleMessage.properties）

```
## 国际化规则 CommandId.label
addCommand.label=Add(&A)
```

##### 清单 8\. 按钮图标（sampleImages.properties）

```
## 国际化规则 CommandId.icon
addCommand.icon=/org/springframework/richclient/images/bullets/genericvariable_obj.gif
```

查看 [清单 7](#listing7) 可以发现，国际化信息末端增加了“`(&A)`”，这样，我们便可以使用快捷键 Alt+A 了，这就是 Spring Richclient 配置快捷键的方式。

那么我们怎么配置菜单呢？菜单最终体现为一个 CommandGroup 的实例，而 Spring Richclient 通过 lifecycleAdvisor 的 menubarBeanName 确定使用哪个 CommandGroup 实例创建菜单。所有 Command 的实例在上下文 commands-context-sample.xml 中进行配置（具体参见示例工程），当然工具栏的配置方式与菜单完全相同（toolbarBeanName）。

最后，我们再说一下 ShowViewCommand，通过该类我们可以创建按钮（菜单项），点击时将注入的 View 显示在 **当前激活的页面**上，您可以通过点击示例工程 User Management 菜单项查看效果。对于 ShowViewCommand 来说，它默认将注入 View 的 Bean Id 作为自己的 Command Id 用来国际化。

### 表单（Form）

对于 Spring Richclient 来说，表单是一个比较重要的概念。与 WEB 应用一样，Spring Richclient 的表单也是用来完成一组数据的输入。Spring Richclient 的表单需要实现接口 Form，通常情况下，我们会使用它的抽象类 AbstractForm。

下面我们定义一个用户信息输入的 Form，实体类和 Form 类分别如 [清单 9](#listing9) 和 [清单 10](#listing10)：

##### 清单 9\. User 实体类

```
package org.springframework.richclient.sample.model;
 
import java.io.Serializable;
 
public class User implements Serializable {
     
    private String firstName;
    private String lastName;
    private Integer age;
    private String remark;
     
    public String getFirstName() {return firstName;}
    public void setFirstName(String firstName) {this.firstName = firstName;}
    public String getLastName() {return lastName;}
    public void setLastName(String lastName) {this.lastName = lastName;}
    public Integer getAge() {return age;}
    public void setAge(Integer age) {this.age = age;}
    public String getRemark() {return remark;}
    public void setRemark(String remark) {this.remark = remark;}
}
```

##### 清单 10\. UserForm 类

```
package org.springframework.richclient.sample.form;
 
import javax.swing.JComponent;
 
import org.springframework.richclient.form.AbstractForm;
import org.springframework.richclient.form.FormModelHelper;
import org.springframework.richclient.form.builder.TableFormBuilder;
import org.springframework.richclient.sample.model.UserQueryCondition;
 
public class UserForm extends AbstractForm {
 
    public UserForm(){
        super(FormModelHelper.createFormModel(new UserQueryCondition(),
            "UserForm"),"UserForm");
    }
     
    @Override
    protected JComponent createFormControl() {
        TableFormBuilder builder = new TableFormBuilder(getBindingFactory());
        builder.add("firstName");
        builder.add("lastName");
        builder.row();
        builder.add("age");
        builder.row();
        builder.addTextArea("remark");
        return builder.getForm();
    }
 
}
```

Spring Richclient 中 Form 的设计方式与 Swing 类似，是视图与数据分离的。Form 编辑对象由 FormModel 维护，而 Form 的视图则是由具体的 Swing 控件完成。因此 Form 的构造方法需要指定 FormModel 和 FormId。

让我们分析一下 Form 的 createFormControl 方法，从代码中不难发现，我们没有手动创建 Swing 控件，而是仅仅指定了我们需要显示和编辑的属性，那么 Spring Richclient 为我们做了那些工作呢？首先根据我们的属性类型找到合适的控件（除了编辑控件还有 Label 标签），然后为控件增加数据绑定，同时为 Label 标签进行国际化。除此之外，还为我们提供了一种易于使用但是能够实现复杂效果的布局方案（封装第三方库 jgoodies），这一切都是通过 TableFormBuilder 完成的，如无特殊功能需求，该类能够完全满足我们构造 Form 的需要。

除此之外，Spring Richclient 还为 Form 提供了数据验证功能，所有验证规则均由 RulesSource 维护，通常情况下，我们使用其默认实现 DefaultRulesSource 即可。增加验证规则的代码如 [清单 11](#listing11) 所示：

##### 清单 11\. UserForm 的验证规则

```
package org.springframework.richclient.sample;
 
import org.springframework.beans.factory.InitializingBean;
import org.springframework.richclient.sample.model.User;
import org.springframework.rules.Rules;
import org.springframework.rules.support.DefaultRulesSource;
 
public class SampleRulesSource extends DefaultRulesSource implements InitializingBean{
 
    public void afterPropertiesSet() throws Exception {
        doInit();
    }
 
    private void doInit() {
        Rules userRule = new Rules(User.class);
        userRule.add("firstName", userRule.maxLength(20));
        userRule.add("lastName", userRule.maxLength(20));
        userRule.add("age", userRule.and(userRule.gte(0), userRule.gte(150)));
        userRule.add("remark",userRule.maxLength(200));
        addRules(userRule);
        //add Rules for other classes
    }
 
}
```

Spring Richclient 的验证规则是针对实体对象的，而非具体 Form，因此 Spring Richclient 的验证规则有更好的复用性，当然，如果您希望同一实体类拥有不同验证规则，那么您还可以在构建 Form 时为其指定验证规则（对于 Spring Richclient 的验证规则，后续将有专门文章进行讲解，此处仅简单介绍其使用方法）。

最后 RulesSource 作为服务，由 DefaultApplicationServices 维护并供应用程序调用，配置如 [清单 12](#listing12)。

##### 清单 12\. RulesSource 配置

```
<bean id="rulesSource"
    class="org.springframework.richclient.sample.SampleRulesSource"></bean>
<bean id="applicationServices"
    class="org.springframework.richclient.application.support.
        DefaultApplicationServices">
    <property name="rulesSourceId" value="rulesSource" />
</bean>
```

Form 是如何国际化的呢？对于 Form 来说，主要的国际化信息包括标签国际化和验证规则国际化，但是我们需要做的只是对属性完成国际化即可，方式：FormId.propertyName 或者 FormId.propertyName.label。您可以运行示例工程查看 UserForm 的所有效果。

配置完毕后，我们便可以将 Form 添加到任何面板上了。至于如何使用 Form 中的数据，Spring Richclient 为我们提供了极为方便的管理，包括数据缓存、数据提交（commit）、数据回退（revert）、数据重置（reset）。因此，我们在使用 Form 的数据以前，必须手动调用 commit 来提交我们的编辑结果（如果在存在验证错误的情况下强行提交，Spring Richclient 将提示异常）。

### Table（表格）

对于企业应用来说，Table 是必不可少的展现组件，Spring Richclient 提供了一种更面向对象的 TableModel 实现，大大简化了 Table 操作。下面我们看看，如何使用 Spring Richclient 构造一个 Table，代码如 [清单 13](#listing13)：

##### 清单 13\. Table 示例

```
queryResultModel = new BeanTableModel(User.class,
                (MessageSource) ApplicationServicesLocator.services()
                        .getService(MessageSource.class)) {
 
    @Override
    protected String[] createColumnPropertyNames() {
        return new String[] { "firstName", "lastName", "age", "remark" };
    }
 
    @Override
    protected Class[] createColumnClasses() {
        return new Class[] { String.class, String.class, Integer.class,
                        String.class };
    }
};
queryResultTable = new JTable(queryResultModel);
queryResultModel.addRow(user);//增加行
```

BeanTableModel 拥有两个抽象方法：createColumnPropertyNames 指定列信息，每一列对应对象的某个属性；createColumnClasses 指定列类型。创建 Table 时，BeanTableModel 会自动根据我们指定的属性名的国际化信息来命名列名，增加行时，它又能自动获取属性值赋于相应列，对于我们来说，则完全以一种面向对象的方式操作 Table。

### Dialog（对话框）

对话框也是应用程序必不可少的组件，Spring Richclient 提供了多种对话框的扩展，我们这里仅介绍常用的一种：TitledPageApplicationDialog。该对话框支持显示 Form，而且对于 Form 的验证规则提供了良好的支持，效果如 [图 5](#fig5)。

##### 图 5\. User Dialog

![图 5. User Dialog](https://www.ibm.com/developerworks/cn/java/j-lo-spring-richclient1/image006.jpg)



我们可以看到，该对话框显示了 UserForm，并且进行了数据验证。如果输入错误，对话框的“确定”按钮不可用，验证错误的信息会显示到对话框上方的 Title 面板区域。所有这一切均由框架完成，我们需要做的就是指定对话框“确定”的处理流程。Dialog 的创建代码如 [清单 14](#listing14)。

##### 清单 14\. Dialog 示例

```
final UserForm form = new UserForm();
form.setFormObject(user);
TitledPageApplicationDialog dialog = new TitledPageApplicationDialog(
                form, Application.instance().getActiveWindow().getControl()) {
 
    @Override
    protected boolean onFinish() {
        form.commit();
        // do something with form object
        return true;
    }
};
dialog.setCallingCommand(callingCommand);
dialog.setPreferredSize(new Dimension(380, 180));
```

很简单吧？综上我们可以看到，Spring Richclient 通过一系列的面向对象的封装，为我们提供了复用性更好的开发方式，通过该框架，我们能够最大程度上实现客户端组件的复用，并且使我们的应用程序拥有良好的可维护性和可扩展性。

## 小结

本文主要介绍了如何搭建 Spring Richclient 开发环境以及 Spring Richclient 主要组件的使用方法，希望您阅读完本文后，可以对 Spring Richclient 的相关功能有一个初步的了解，在后续文章中，我将对 Spring Richclient 的架构以及数据绑定、验证规则等核心功能进行详细讲解。

* * *

#### 下载资源

*   [工程代码](http://www.ibm.com/developerworks/apps/download/index.jsp?contentid=591757&filename=SpringRichclient.zip&method=http&locale=zh_CN) (SpringRichclient.zip | 15KB)

* * *

#### 相关主题

*   参考：[Spring Richclient 的入门知识](http://java.dzone.com/news/spring-rcp-tutorial)。
*   进一步了解：[Spring Richclient](http://java.dzone.com/news/getting-further-with-spring-rc)。
*   下载：[Spring Richclient 相关包](http://sourceforge.net/projects/spring-rich-c/files/)。
*   [developerWorks Java 技术专区](http://www.ibm.com/developerworks/cn/java/)：数百篇关于 Java 编程各个方面的文章。

