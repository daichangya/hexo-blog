---
title: Java设计模式——适配器模式：解锁接口兼容的神奇“魔法”
id: 710b9eae-34b6-4ce5-b5a3-8d0b60c42a4a
date: 2024-11-29 12:14:45
author: daichangya
cover: https://images.jsdiff.com/design05.jpg
excerpt: 在编程这片充满奇幻与挑战的领域中，我们时常会遭遇棘手难题，就像不同国度的人操着各自独特的语言，彼此难以顺畅沟通一样。软件世界里，诸多类本身功能完备、实力强劲，却因接口的“语言不通”，在协作之路上举步维艰。而今天要揭秘的适配器模式（Adapter
  Pattern），宛如一位神通广大的“翻译官”，凭借神
permalink: /archives/Java-she-ji-mo-shi-shi-pei-qi-mo-shi/
categories:
- 设计模式
---

在编程这片充满奇幻与挑战的领域中，我们时常会遭遇棘手难题，就像不同国度的人操着各自独特的语言，彼此难以顺畅沟通一样。软件世界里，诸多类本身功能完备、实力强劲，却因接口的“语言不通”，在协作之路上举步维艰。而今天要揭秘的适配器模式（Adapter Pattern），宛如一位神通广大的“翻译官”，凭借神奇魔力，巧妙化解接口差异，让原本“鸡同鸭讲”的类紧密携手，协同奏响流畅运行的乐章。快跟着我，一同深入探寻这奇妙设计模式背后的神秘面纱吧！💥

## 一、“困境突围”：适配器模式诞生的使命🎯

想象一下，你正精心搭建一座宏伟的软件“城堡”，各类组件如同形态各异的“砖石”，本应严丝合缝地拼接在一起，撑起稳固架构。可偏就碰上了接口不兼容的“捣蛋鬼”，让这些“砖石”相互“排斥”，无法按预期组合发力。适配器模式正是为此横空出世，它的核心要义，便是像一位智慧的桥梁建筑师，把一个类那“个性十足”的接口，巧妙转换成客户心心念念、能无缝对接的另一种接口模样。如此一来，那些因接口“闹别扭”而无法并肩作战的类，就能在它的牵线搭桥下，冰释前嫌，和谐共处，让整个系统如精密齿轮组般顺滑运转。🌟

## 二、“生活智慧”：类比现实的妙处🤔

生活里，处处藏着适配器模式的“影子”。不妨设想这样一个场景：你邂逅了一位来自韩国的友人，你满心热情，想畅聊一番，分享趣事，可尴尬的是，你对韩语一窍不通，对方对汉语亦是两眼一抹黑。这时候，咋办呢？要是选择从零开始教他汉语，先不提这得耗费多少时间、精力，还得考量对方的学习热情、吸收能力诸多因素，实在是个“大工程”。但要是有一位专业翻译在场，那可就大不一样啦！翻译官就像拥有“语言超能力”，在你们之间轻松切换、协调语言差异，成本低、效率高还灵活多变。往后啊，要是再碰上日本朋友，只需换一位精通日语的翻译，沟通桥梁瞬间就能架起。编程中的适配器模式，可不就恰似这厉害的翻译官，凭借“转换接口”这一绝技，让不同“语言体系”（接口）的类顺利“对话”、紧密合作。😎

## 三、“实战驱动”：绘图编辑器里的巧思🎨
<separator></separator>
来瞧瞧在绘图编辑器这个“战场”上，适配器模式是如何大显身手的。绘图编辑器肩负着绘制、编排各类基本图元，像直线、多边形、正文这些元素，组合出精美图片与图表的重任。直线和多边形的实现，相对来说驾轻就熟，可正文部分的开发，却像一座难啃的“硬骨头”。要是重新埋头苦干、从零打造，既费时间又耗资源，还难保质量。这时候，适配器模式闪亮登场！通过精心定义一个适配器类，就拿“TextShape”来说，巧妙复用早已稳坐图形工具箱的正文编辑器（类似“TextView”），恰似“移花接木”，避免了重复造轮子的麻烦，大大提升开发效率，还确保了系统的稳健可靠。这，就是适配器模式在实战中的“四两拨千斤”之力。✨

## 四、“Java 解法”：类与对象模式大揭秘🧐

在 GOF 设计模式这座“宝藏库”里，适配器模式掏出了类模式和对象模式这两把“利器”，准备应对 Java 编程世界的接口兼容挑战。不过在 Java 这片天地，多重继承可不被允许，使得类模式得动点“脑筋”、做点调整，得靠继承“Adaptee”类，再实现“Target”接口来达成目的。但这么做，也带来了俩小“麻烦”：其一，“Target”必须化身接口，不然“Adapter”没法实现它，就像钥匙和锁不匹配，打不开协同之门；其二，“Adapter”成了“Adaptee”的子类后，好似被戴上了“紧箍咒”，有了身份局限，某些灵活操作施展不开。

反观对象模式，它另辟蹊径，玩起了“委托”的巧妙把戏，如同找了个可靠“中间人”帮忙协调，灵活性瞬间拉满。接下来，咱们详细剖析下这俩模式在特性上的“同与不同”，好让大家按需“取剑”，精准出击。🧩

## 五、“优劣对对碰”：类模式 VS 对象模式🌈

### （一）Adapter 对 Adaptee 的“特殊定制”
1. **类模式**：由于“Adapter”稳稳扎根于“Adaptee”家族树，是它的子类，这层血缘关系赋予了“Adapter”一项特权——能轻松改写“Adaptee”里的个别方法，按自身特殊需求“量体裁衣”。打个比方，在特定场景下，要是觉得“Adaptee”某个方法效率欠佳或者功能不够完善，“Adapter”便能大显身手，深入内部优化、拓展，就像给老房子翻新改造，得心应手。
2. **对象模式**：“Adapter”与“Adaptee”没有这层直系血缘，只是合作的“伙伴关系”。要是对“Adaptee”个别方法有特殊“挑剔”，那就得新建“Adaptee”的子类，再让“Adapter”和这个子类携手共事。虽说步骤稍显繁琐，但也像打开了一扇“任意门”，换来更大操作空间、更多灵活选择。

### （二）Adaptee 的“家族扩张”应对
1. **类模式**：一旦“Adapter”选定继承某一“Adaptee”，就像在婚姻里许下了一生承诺，编译完成后，可没法随意“改嫁”、更换父类“Adaptee”咯。要是“Adaptee”家族开枝散叶，拓展出庞大类层次结构，那相应地，得费劲巴拉地给“Adapter”家族也搭建起一整套复杂分支，而且往后再有新成员加入“Adaptee”家族，适配工作就变得极为不便，好似给老旧房子加盖楼层，处处受限。
2. **对象模式**：“Adapter”和“Adaptee”凭借“委托”关联，如同商业合作，随时能依据需求“换搭档”。系统运行时，只要新来的“Adaptee”类型相符，就能轻松替换，携手共进。所以当“Adaptee”家族添丁进口、不断扩张时，“Adapter”能从容应对，灵活调整，持续保障系统顺畅运行。

|对比维度|类模式|对象模式|
|---|---|---|
|对 Adaptee 方法特殊定制|可直接重定义，方便优化拓展|需新建子类配合，灵活性高|
|应对 Adaptee 类层次扩展|编译后难更换，扩展不便|运行时可灵活替换，适应性强|]

## 六、“代码实战秀”：图形绘制场景下的适配器魔法🎯

### （一）对象模式“首秀”
1. **基础“砖石”搭建：Point 类**
先打造一个“Point”类，它宛如绘图坐标世界里的精准“定位仪”，标识画面坐标中的点，代码如下：
```java
package qinysong.pattern.adapter;

public class Point {
    private int coordinateX;
    private int coordinateY;

    public Point(int coordinateX, int coordinateY) {
        this.coordinateX = coordinateX;
        this.coordinateY = coordinateY;
    }

    public String toString() {
        return "Point[x=" + coordinateX + ",y=" + coordinateY + "]";
    }

    public int getCoordinateX() {
        return coordinateX;
    }

    public int getCoordinateY() {
        return coordinateY;
    }
}
```
2. **抽象“蓝图”绘制：Shape 接口**
接着定义“Shape”接口，这可是图元们的“通用模板”，对应适配器模式里的“Target”角色，为后续各类图元形状勾勒出统一规范，代码如下：
```java
package qinysong.pattern.adapter;

public interface Shape {
    Point getBottomLeftPoint();
    Point getTopRightPoint();
}
```
3. **原始“素材”登场：TextView 类**
然后请出“TextView”类，它是图形工具箱里的“文本能手”，也就是适配器模式中的“Adaptee”，自带一堆文本属性获取方法，代码如下：
```java
package qinysong.pattern.adapter;

public class TextView {
    public int getCoordinateX() {
        System.out.println("TextView.getCoordinateX()...");
        return 10;
    }

    public int getCoordinateY() {
        System.out.println("TextView.getCoordinateY()...");
        return 20;
    }

    public int getHeight() {
        System.out.println("TextView.getHeight()...");
        return 30;
    }

    public int getWidth() {
        System.out.println("TextView.getWidth()...");
        return 40;
    }

    public boolean isEmpty() {
        return false;
    }
}
```
4. **神奇“翻译官”现身：TextShape 类**
重点来了，“TextShape”类作为对象模式下的适配器闪亮登台，它手握“TextView”实例，凭借委托协调之力，让文本在绘图形状世界里找到“立足之地”，代码如下：
```java
package qinysong.pattern.adapter;

public class TextShape implements Shape {
    private TextView textView;

    public TextShape(TextView textView) {
        this.textView = textView;
    }

    // 借助委托，调用 TextView 方法实现接口功能
    public Point getBottomLeftPoint() {
        System.out.println("TextShape.getBottomLeftPoint()...");
        int coordinateX = textView.getCoordinateX();
        int coordinateY = textView.getCoordinateY();
        return new Point(coordinateX, coordinateY);
    }

    // 借助委托，调用 TextView 方法实现接口功能
    public Point getTopRightPoint() {
        System.out.println("TextShape.getTopRightPoint()...");
        int coordinateX = textView.getCoordinateX();
        int coordinateY = textView.getCoordinateY();
        int height = textView.getHeight();
        int width = textView.getWidth();
        return new Point(coordinateX + width, coordinateY + height);
    }
}
```
5. **“客户体验”时刻：Client 类**
最后，“Client”类作为使用者，登场检验适配器模式的神奇效果，代码如下：
```java
package qinysong.pattern.adapter;

public class Client {
    public static void main(String[] args) {
        System.out.println("Client.main begin..........");
        System.out.println("Client.main 以下是通过实例委托方式实现的 Adapter");
        Shape shape = new TextShape(new TextView());
        Point bottomLeft = shape.getBottomLeftPoint();
        Point topRight = shape.getTopRightPoint();
        System.out.println("Client.main shape's bottomLeft: " + bottomLeft);
        System.out.println("Client.main shape's topRight: " + topRight);
        System.out.println("Client.main end..........");
    }
}
```

### （二）类模式“接力”
同样为实现图形绘制适配，在“Point”、“Shape”、“TextView”类前期定义相同（此处省略重复代码展示）基础上，类模式推出“TextShape2”类这一“答卷”，代码如下：
```java
package qinysong.pattern.adapter;

public class TextShape2 extends TextView implements Shape {
    // 利用继承自 TextView 的优势，协调实现接口方法
    public Point getBottomLeftPoint() {
        System.out.println("TextShape2.getBottomLeftPoint()...");
        int coordinateX = getCoordinateX();
        int coordinateY = getCoordinateY();
        return new Point(coordinateX, coordinateY);
    }

    // 利用继承自 TextView 的优势，协调实现接口方法
    public Point getTopRightPoint() {
        System.out.println("TextShape2.getTopRightPoint()...");
        int coordinateX = getCoordinateX();
        int coordinateY = getCoordinateY();
        int height = getHeight();
        int width = getWidth();
        return new Point(coordinateX + width, coordinateY + height);
    }

    // 凸显类模式特色，重定义父类方法
    public int getCoordinateX() {
        System.out.println("TextShape2.getCoordinateX()...");
        return 100;
    }
}
```

通过这两套代码“实战演练”，大家能清晰洞察类模式与对象模式在适配器模式舞台上的“表演细节”、独特魅力，日后编程实战，便能依据项目需求“对号入座”，充分释放适配器模式的超强能量，让各类接口“握手言和”，共筑强大软件系统“摩天大楼”。🚀 