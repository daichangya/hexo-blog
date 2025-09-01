---
title: 通过Java Swing看透MVC设计模式
id: 1024
date: 2024-10-31 22:01:48
author: daichangya
cover: https://images.jsdiff.com/design01.jpg
permalink: /archives/tong-guo-java-swingkan-tou-mvcshe-ji-mo-shi/
categories:
 - 设计模式
tags:  
 - 设计模式
---

# 通过Java Swing看透MVC设计模式

## 一、引言
### （一）GUI设计思想的启发
在现实世界中，一个简单的电脑键盘按键，如按钮，就体现了GUI设计的规则。它由动作特性（如可被按下）和表现（如代表的字母）两部分构成。这种设计思想可应用于软件开发，例如Model/View/Controller（MVC）设计模式。MVC设计模式鼓励重用，减轻设计工作的时间和难度，就像通过改变按钮表面的字母就能制造出“不同”的按钮，而无需重新设计整个按钮结构。

### （二）MVC与Java Swing的关系
MVC设计模式通常用于设计整个用户界面（GUI），而Java Foundation Class（JFC）中的Swing组件将MVC设计模式应用于单个组件。如表格（JTable）、树（JTree）、组合下拉列表框（JComboBox）等组件都有各自的Model、View和Controller，且这些部分可以独立改变，即使组件正在被使用，这使得开发GUI界面的工具包非常灵活。

## 二、MVC设计模式概述
### （一）Model
1. **功能与特性**
   - Model代表组件状态和低级行为，管理自身状态并处理所有对状态的操作。它不知道使用自己的View和Controller是谁，系统维护其与View的关系，当Model发生改变时，系统负责通知相应的View。例如，在一个游戏角色的模型中，它包含角色的生命值、攻击力等状态信息，以及升级、受伤等操作这些状态的方法。
### （二）View
1. **功能与特性**
   - View负责管理Model所含数据的视觉呈现。一个Model可以有多个View，但在Swing中这种情况较少。比如，在一个数据可视化系统中，同一组数据可以通过柱状图、折线图等不同的View来展示给用户。
### （三）Controller
1. **功能与特性**
   - Controller管理Model和用户之间的交互控制，提供处理Model状态变化情况的方法。以游戏中的角色控制为例，Controller接收用户的输入（如键盘按键、鼠标点击），并根据这些输入改变角色Model的状态（如移动、攻击）。

### （四）MVC在按钮中的示例（配图：一个简单的按钮示意图，标注出Model、View/Controller部分）
用键盘按钮类比，Model就像按钮的整个机械装置，负责按钮的行为逻辑，如是否被按下、是否可用等状态的管理；View/Controller则如同按钮的表面部分，负责按钮的外观显示以及接收用户对按钮的操作（如点击、鼠标悬停等）。

## 三、Button组件中的MVC实现
### （一）Button类
1. **关联Model和View/Controller的代码分析**
   - Button类是Model和View/Controller之间的黏合剂。每个按钮组件都与一个Model和一个Controller关联，Model定义按钮行为，View/Controller定义按钮表现，应用程序可随时改变这些关联。
```java
public void setModel(ButtonModel buttonmodel) {
    if (this.buttonmodel!= null) {
        this.buttonmodel.removeChangeListener(buttonchangelistener);
        this.buttonmodel.removeActionListener(buttonactionlistener);
        buttonchangelistener = null;
        buttonactionlistener = null;
    }
    this.buttonmodel = buttonmodel;
    if (this.buttonmodel!= null) {
        buttonchangelistener = new ButtonChangeListener();
        buttonactionlistener = new ButtonActionListener();
        this.buttonmodel.addChangeListener(buttonchangelistener);
        this.buttonmodel.addActionListener(buttonactionlistener);
    }
    updateButton();
}

public void setUI(ButtonUI buttonui) {
    if (this.buttonui!= null) {
        this.buttonui.uninstallUI(this);
    }
    this.buttonui = buttonui;
    if (this.buttonui!= null) {
        this.buttonui.installUI(this);
    }
    updateButton();
}

public void updateButton() {
    invalidate();
}
```
   - 上述代码中，`setModel`方法用于设置按钮的Model。当设置新的Model时，会先移除旧Model的相关监听器，然后添加新Model的监听器，并更新按钮状态。`setUI`方法用于设置按钮的View/Controller，类似地，会先卸载旧的UI，再安装新的UI并更新按钮。`updateButton`方法则通过调用`invalidate`来触发按钮的重绘，确保按钮的显示与新的Model和View/Controller设置保持一致。

### （二）ButtonModel类
1. **状态信息与事件通知代码分析**
   - ButtonModel维护按钮的状态信息，如是否被按下（pressed）、是否“武装上了”（armed）、是否被选择（selected），这些都是布尔类型值。
```java
private boolean boolPressed = false;
public boolean isPressed() {
    return boolPressed;
}
public void setPressed(boolean boolPressed) {
    this.boolPressed = boolPressed;
    fireChangeEvent(new ChangeEvent(button));
}
```
   - 以上代码展示了`pressed`状态的实现。`isPressed`方法用于查询按钮是否被按下，`setPressed`方法不仅设置按钮的按下状态，还会通过`fireChangeEvent`方法触发状态改变事件，通知其他监听器按钮状态发生了变化。
   - ButtonModel还负责通知其他对象（事件监听器）感兴趣的事件，通过维护一个监听器列表来实现。
```java
private Vector vectorChangeListeners = new Vector();
public void addChangeListener(ChangeListener changelistener) {
    vectorChangeListeners.addElement(changelistener);
}
public void removeChangeListener(ChangeListener changelistener) {
    vectorChangeListeners.removeElement(changelistener);
}
protected void fireChangeEvent(ChangeEvent changeevent) {
    Enumeration enumeration = vectorChangeListeners.elements();
    while (enumeration.hasMoreElements()) {
        ChangeListener changelistener =(ChangeListener)enumeration.nextElement();
        changelistener.stateChanged(changeevent);
    }
}
```
   - `addChangeListener`和`removeChangeListener`方法用于添加和移除监听器，`fireChangeEvent`方法在状态改变时遍历监听器列表，调用每个监听器的`stateChanged`方法，通知它们按钮状态发生了改变。（配图：一个按钮状态变化的流程图，展示从用户操作到Model状态改变，再到通知监听器的过程）

### （三）ButtonUI类
1. **构建表示层与事件处理代码分析**
   - ButtonUI负责构建按钮的表示层，默认情况下仅用背景色画一个矩形。
```java
public void update(Button button, Graphics graphics) {
}
public void paint(Button button, Graphics graphics) {
    Dimension dimension = button.getSize();
    Color color = button.getBackground();
    graphics.setColor(color);
    graphics.fillRect(0, 0, dimension.width, dimension.height);
}
```
   - `update`方法可用于在按钮状态改变时进行一些预处理，`paint`方法则负责绘制按钮的外观，根据按钮的大小和背景色绘制一个矩形。
   - ButtonUI不直接处理AWT事件，而是通过定制的事件监听器将低级的AWT事件翻译为高级的Button模型期望的语义事件。
```java
private static ButtonUIListener buttonuilistener = null;
public void installUI(Button button) {
    button.addMouseListener(buttonuilistener);
    button.addMouseMotionListener(buttonuilistener);
    button.addChangeListener(buttonuilistener);
}
public void uninstallUI(Button button) {
    button.removeMouseListener(buttonuilistener);
    button.removeMouseMotionListener(buttonuilistener);
    button.removeChangeListener(buttonuilistener);
}
```
   - `installUI`方法在按钮安装时添加相关事件监听器，`uninstallUI`方法在按钮卸载时移除这些监听器。（配图：一个按钮绘制过程的示意图，展示从ButtonUI的paint方法到实际在屏幕上显示按钮的过程）

### （四）ButtonUIListener类
1. **事件处理逻辑代码分析**
   - ButtonUIListener帮助Button类将鼠标或键盘输入转换为对按钮模型的操作，实现了MouseListener、MouseMotionListener和ChangeListener接口。
```java
public void mouseDragged(MouseEvent mouseevent) {
    Button button = (Button)mouseevent.getSource();
    ButtonModel buttonmodel = button.getModel();
    if (buttonmodel.isPressed()) {
        if (button.getUI().contains(button, mouseevent.getPoint())) {
            buttonmodel.setArmed(true);
        } else {
            buttonmodel.setArmed(false);
        }
    }
}
public void mousePressed(MouseEvent mouseevent) {
    Button button = (Button)mouseevent.getSource();
    ButtonModel buttonmodel = button.getModel();
    buttonmodel.setPressed(true);
    buttonmodel.setArmed(true);
}
public void mouseReleased(MouseEvent mouseevent) {
    Button button = (Button)mouseevent.getSource();
    ButtonModel buttonmodel = button.getModel();
    buttonmodel.setPressed(false);
    buttonmodel.setArmed(false);
}
public void stateChanged(ChangeEvent changeevent) {
    Button button = (Button)changeevent.getSource();
    button.repaint();
}
```
   - `mouseDragged`方法在鼠标拖动时，根据按钮Model的按下状态和鼠标位置更新按钮的“武装”状态；`mousePressed`方法在鼠标按下时设置按钮的按下和“武装”状态；`mouseReleased`方法在鼠标释放时重置按钮的按下和“武装”状态；`stateChanged`方法在按钮状态改变时（如通过代码设置按钮状态），调用按钮的`repaint`方法重绘按钮，以反映最新状态。

## 四、总结
通过对Java Swing中Button组件的MVC设计模式分析，我们看到了MVC在单个组件中的实现细节。在实际使用中，我们无需深入了解其底层实现即可方便地使用Swing组件，因为它们提供了默认的Model、View和Controller。然而，当我们自己开发组件时，MVC思想的强大之处就会显现出来，它能帮助我们构建出结构清晰、易于维护和扩展的软件系统。这种设计模式使得组件的各个部分职责分明，Model专注于数据和状态管理，View专注于显示，Controller专注于用户交互控制，它们之间的低耦合性保证了系统的灵活性和可维护性，为开发高质量的GUI应用提供了坚实的基础。