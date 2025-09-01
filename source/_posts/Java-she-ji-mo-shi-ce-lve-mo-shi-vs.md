---
title: Java设计模式——策略模式 vs 工厂模式：解锁软件设计 “超能力”，码农必备！
id: 5ef09b5c-803e-4e6c-8494-bb9e6f9ff40e
date: 2024-11-27 12:28:50
author: daichangya
cover: https://images.jsdiff.com/design01.jpg
excerpt: 嘿，各位奋战在代码“一线”的小伙伴们！今天咱要开启一场设计模式界的“巅峰对决”，主角就是策略模式与工厂模式这两大“王牌选手”。在软件开发这片“江湖”，选对设计模式，就如同大侠手握神兵，能让代码“如有神助”，轻松应对各种复杂“战局”。闲话不多说，现在就深挖它们的“绝技”，看谁才是你项目里的“最强辅助”
permalink: /archives/Java-she-ji-mo-shi-ce-lve-mo-shi-vs/
categories:
- 设计模式
---

嘿，各位奋战在代码“一线”的小伙伴们！今天咱要开启一场设计模式界的“巅峰对决”，主角就是策略模式与工厂模式这两大“王牌选手”。在软件开发这片“江湖”，选对设计模式，就如同大侠手握神兵，能让代码“如有神助”，轻松应对各种复杂“战局”。闲话不多说，现在就深挖它们的“绝技”，看谁才是你项目里的“最强辅助”！

## 一、策略模式：算法“百变精灵”，灵活切换“超神了”！

### （一）策略模式是啥“神秘武器”？

想象你正坐镇“代码指挥中心”，指挥一场“编程大战”，战场形势瞬息万变（运行时各种复杂状况），得随时切换作战“策略”（算法），还得保证“指挥系统”（客户端代码）稳如泰山。这时候，策略模式就像“天降奇兵”，它是行为型设计模式里的“智慧担当”，把各类算法封装进独立“锦囊”（策略类），藏于代码“宝库”，按需调用。不管战况咋变，换个“锦囊”就能应对，严守“开闭原则”，扩展轻松，修改无忧，简直是代码界“百变精灵”，变形超顺滑，战斗力爆表！
用个简单表格呈现策略模式结构：
| 组件 | 描述 | 示例 | 图示示意 |
| ---- | ---- | ---- | ---- |
| 抽象策略类 | 定义通用策略行为接口，是具体策略类遵循的“模板”，规定核心方法。 | `PromotionStrategy` 接口，`applyPromotion` 方法定规则。 | [画个长方形框代表抽象策略类，里面写方法名] |
| 具体策略类 | 实现抽象策略类，承载独特算法逻辑，各显神通。 | `FullReductionStrategy`（满减）、`DiscountStrategy`（折扣）。 | [多个小长方形框代表具体策略类，分别指向抽象策略类大框，标注各自算法特色] |
| 上下文类 | 持有策略类引用，按场景调用方法，像“指挥官”调配策略。 | `ShoppingCart`，依总价调用策略算最终价。 | [画个圆形框代表上下文类，用箭头指向抽象策略类，体现关联] |

### （二）生活实例：披萨店的“创意大厨养成”

进一家超有个性披萨店，点份培根披萨，老板不走寻常路，给你食材和制作指南，让你自由发挥。多放芝士、精准控火候、妙调佐料，这些“操作”就是“策略”。你（客户端）依口味挑策略做披萨，正如策略模式里，客户端据实际灵活调用策略类达个性化目的，秒懂了吧！

### （三）代码实战：电商“促销魔法秀”

电商“战场”竞争白热化，促销策略是“秘密武器”。咱用 Java 代码建个“促销魔法库”，看策略模式“施法”。

```java
// 抽象策略接口，画促销“蓝图”，定通用规则
interface PromotionStrategy {
 double applyPromotion(double totalPrice);
}
// 满减策略，达门槛就减钱，超给力
class FullReductionStrategy implements PromotionStrategy {
 private double fullAmount;
 private double reductionAmount;
 public FullReductionStrategy(double fullAmount, double reductionAmount) {
 this.fullAmount = fullAmount;
 this.reductionAmount = reductionAmount;
 }
 @Override
 public double applyPromotion(double totalPrice) {
 if (totalPrice >= fullAmount) {
 return totalPrice - reductionAmount;
 } else {
 return totalPrice;
 }
 }
}
// 折扣策略，按折扣率“削价”
class DiscountStrategy implements PromotionStrategy {
 private double discountRate;
 public DiscountStrategy(double discountRate) {
 this.discountRate = discountRate;
 }
 @Override
 public double applyPromotion(double totalPrice) {
 return totalPrice * discountRate;
 }
}
// 上下文类，“促销指挥官”，拿策略“指挥棒”调度
class ShoppingCart {
 private PromotionStrategy promotionStrategy;
 private double totalPrice;
 public ShoppingCart(PromotionStrategy promotionStrategy) {
 this.promotionStrategy = promotionStrategy;
 }
 public void addItem(double price) {
 totalPrice += price;
 }
 public double calculateFinalPrice() {
 return promotionStrategy.applyPromotion(totalPrice);
 }
}
// 测试代码，“实战演练”看策略威力
public class StrategyPatternDemo {
 public static void main(String[] args) {
 // 首波“攻势”，满减策略登场，满 200 减 50，模拟结账
 PromotionStrategy fullReduction = new FullReductionStrategy(200, 50);
 ShoppingCart cart1 = new ShoppingCart(fullReduction);
 cart1.addItem(100);
 cart1.addItem(100);
 System.out.println("满减策略下最终价格: " + cart1.calculateFinalPrice());
 // 次波“浪潮”，折扣策略来袭，打 8 折，再结账
 PromotionStrategy discount = new DiscountStrategy(0.8);
 ShoppingCart cart2 = new ShoppingCart(discount);
 cart2.addItem(150);
 cart2.addItem(50);
 System.out.println("折扣策略下最终价格: " + cart2.calculateFinalPrice());
 }
}
```

在这“魔法阵”里，`PromotionStrategy` 接口如“魔法法典”，规促销“咒语”。`FullReductionStrategy` 和 `DiscountStrategy` 像“魔法师”算优惠，`ShoppingCart` 似“指挥官”，依策略算花费。换策略？改传入对象就行，主代码稳如泰山！

### （四）策略模式“超能力”盘点

1. **扩展似搭乐高，零压力**：电商想加“积分抵现金”策略，写个遵接口新类就好，代码“大厦”稳当当。
2. **切换“丝滑”，运行时从容**：购物节、新品首发，任场景切换，客户端代码淡定，轻松应对业务“路况”。
  
  ## 二、工厂模式：对象“神奇工坊”，一键产出“超省心”！
  
  ### （一）工厂模式啥“奇妙门道”？
  
  在软件“江湖”另一角，工厂模式扎根创建型设计模式“地盘”，像座“神奇工坊”。你当“甲方”递“订单”（创建对象请求），“工匠”（工厂类）按“秘方”（预设逻辑）造“珍宝”（对象），藏复杂过程。咱客户端（代码使用者）像“金主”，拿过来用就行，易用性、可维护性飙升，超贴心！
  也用表格展示工厂模式结构：
  
  | 组件  | 描述  | 示例  | 图示示意 |
  | --- | --- | --- | --- |
  | 抽象产品类 | 定义产品通用行为属性，作具体产品“模板”。 | `Shape` 接口，`draw` 方法定绘制规范。 | [长方形框代表抽象产品类，写方法] |
  | 具体产品类 | 实现抽象产品类，具实际功能特性。 | `Circle`（圆）、`Rectangle`（矩形）。 | [多个小框代表具体产品类，指向抽象产品类，展示独特风貌] |
  | 抽象工厂类 | 定义创建产品抽象方法，把控流程“大方向”。 | `ShapeFactory` 接口，`createShape` 方法定规则。 | [大圆形框代表抽象工厂类，写方法] |
  | 具体工厂类 | 实现抽象工厂类，按逻辑造具体产品。 | `CircleFactory`、`RectangleFactory`。 | [小圆形框代表具体工厂类，指向抽象工厂类与对应具体产品类，体现创建关联] |
  
  ### （二）生活对照：传统披萨店的“高效出餐”
  
  去传统披萨店点培根披萨，坐下等餐。后厨如“披萨工厂”，师傅依流程配料、烘焙，很快美味上桌。你（客户端）不管制作，只享美味，这就是工厂模式日常版，好理解吧！
  
  ### （三）代码落地：图形绘制“梦幻工厂”
  
  在图形绘制软件“天地”，用工厂模式建“图形梦幻工厂”管图形创建，代码如下：
  
  ```java
  // 抽象产品接口，定图形“绘画准则”，统“画风”
  interface Shape {
  void draw();
  }
  // 圆形，“丹青妙手”绘圆
  class Circle implements Shape {
  @Override
  public void draw() {
  System.out.println("绘制圆形");
  }
  }
  // 矩形，“几何大师”画矩形
  class Rectangle implements Shape {
  @Override
  public void draw() {
  System.out.println("绘制矩形");
  }
  }
  // 抽象工厂接口，“工厂掌门”定“生产规矩”
  interface ShapeFactory {
  Shape createShape();
  }
  // 圆形工厂，专“产”圆形，手艺精
  class CircleFactory implements ShapeFactory {
  @Override
  public Shape createShape() {
  return new Circle();
  }
  }
  // 矩形工厂，匠心造矩形，品质优
  class RectangleFactory implements ShapeFactory {
  @Override
  public Shape createShape() {
  return new Rectangle();
  }
  }
  // 测试代码，“艺术展”看产出绘制效果
  public class FactoryPatternDemo {
  public static void main(String[] args) {
  // 先画圆，启圆形工厂
  ShapeFactory circleFactory = new CircleFactory();
  Shape circle = circleFactory.createShape();
  circle.draw();
  // 再画矩形，矩形工厂接力
  ShapeFactory rectangleFactory = new RectangleFactory();
  Shape rectangle = rectangleFactory.createShape();
  rectangle.draw();
  }
  }
  ```
  
  在这“艺术工坊”，`Shape` 接口如“绘画宝典”，`Circle` 和 `Rectangle` 像“绘画大师”展独特画风，`ShapeFactory` 控流程，`CircleFactory` 等造图形。客户端靠工厂拿图形，不管细节，解耦彻底。加“三角形”？按套路扩代码，现有逻辑稳稳的。
  
  ### （四）工厂模式“闪光点”提炼
  
3. **创建使用“分家”，互不扰**：客户端“前台”用对象，工厂“后台”造，后台“装修”（改创建逻辑），前台照旧，系统似巨轮，超稳。
4. **创建逻辑“一统”，管理高效**：创建规则、资源调配在工厂“大本营”，优化图形参数等，内部微调，清晰快捷，“代码洁癖”福音。
  
  ## 三、终极对决：策略模式 vs 工厂模式
  
  咱用表格清晰对比二者：
  
  | 对比维度 | 策略模式 | 工厂模式 |
  | --- | --- | --- |
  | 设计初衷 | 聚焦算法灵活切换与封装，应对业务规则多变，让系统低成本适应变化。 | 着眼对象创建便利性，隔离复杂过程，提升系统易用与可维护性。 |
  | 角色职责 | 策略类（实现算法）、上下文类（调度策略）。策略类似“武林高手”精研算法，上下文类像“盟主”调配。 | 工厂类（把控创建）、产品类（展示功能）。工厂类如“资深工匠”造产品，产品类是“匠心作”待发挥。 |
  | 应用场景 | 算法频繁切换处，如金融产品利息计算（活期、定期等切换）。 | 对象创建复杂需管理处，像游戏角色创建（不同种族、职业）。 |
  | 小伙伴们，看完这场“巅峰对决”，策略模式和工厂模式是不是“门儿清”啦？以后项目里，别“乱点鸳鸯谱”，按需“配对”，让代码“战斗力”飙升，成为代码“大神”指日可待，冲呀！ |     |     |