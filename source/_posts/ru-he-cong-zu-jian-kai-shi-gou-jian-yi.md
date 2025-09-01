---
title: 如何从组件开始构建一座城市？
id: 396
date: 2024-10-31 22:01:43
author: daichangya
excerpt: 为什么越来越多的企业应用开发正在转向组件框架和解决方案？组件架构是否有前途？我相信答案是肯定的
permalink: /archives/ru-he-cong-zu-jian-kai-shi-gou-jian-yi/
categories:
- 系统架构
---



![](https://static001.infoq.cn/resource/image/21/53/217f973d6c393174ca1d59e1c35ead53.jpg)
为什么越来越多的企业应用开发正在转向组件框架和解决方案？组件架构是否有前途？我相信答案是肯定的，而且很快所有开发框架都将会是基于组件的——这是近在眼前的事情。下面让我来向你揭示这一切的原因。

你怎么来建设你的房子？一般你会从砌块开始。我们可以将构建 Web 应用与构建你的乡间小屋进行对比。你能够快速构建一个非常好看的应用，而且它具有所有必需的功能。同样，在你的房子里面，每一间房间都是针对具体的需求来创建的，例如厨房、起居室、卧室或浴室。房子的布局使你能够通过走廊和楼梯很方便地在房间之间移动。

现在你能够做得更好，而且能够承担建设一座更大更好的房子的投入——你也许希望拥有桑拿房、游泳池、影院以及一座满是爬行动物的巨大的水族馆☺。但要想改变房子的设计却是件非常困难的事情。若要添加额外的设施，房子最终看起来也许就不那么漂亮了。此外，由于你添加的这些设施必须放在不太方便的位置，它们也会影响房子使用的便利性，例如你必须穿过主卧室才能进入台球室。

最后，你那漂亮又整洁的房子将拥有一堆不同的功能，但它会变得笨拙又不舒适。同样的道理也适用于应用开发。

问题是，有没有可能设计一款应用，能够根据你的需求成长和改变？

**组件是应用的积木式构件**

![](https://static001.infoq.cn/resource/image/e7/65/e7da8857db9409bba99f7e80b93e8065.jpg) 
组件是扩展应用功能的首要方法。创建组件的过程，与基于组件创建应用的过程有一些差异。组件不止应该提供有用的功能，还应该从一开始就设计成可复用的。

**组件复用**

![](https://static001.infoq.cn/resource/image/7a/1b/7aa76d75e378478b825ff38aa2ee591b.jpg) 
组件应该采用松耦合方式设计以便于复用。为实现这一目标，不同的框架往往基于观察者模式实现其事件模型。该模式允许多个接收者订阅同一事件。

观察者模式的实现最早出现在 Smalltalk 中。Smalltalk 是一个基于 MVC 的用户界面框架，现在它已经成为 MVC 框架的关键部分。我希望你能注意到，自 Java 1.0 版本起，观察者模式就已经在 Java 中存在。下面让我们深入了解它。

下面的 UML 图展现了观察者模式：

![](https://static001.infoq.cn/resource/image/e1/9d/e13b9c2c7b1d3e7515cb2801018f2f9d.jpg)

以下则是一段基本的 Java 实现：


	public class ObservableX extends Observable {
	  ...
	  public void setAmount(double amount) {
	    this.amount = amount;
	    super.setChanged();
	    super.notifyObservers();
	}

	}
	  public class ObserverA implements Observer {
	  public void public void update(Observable o) {
	  // gets updated amount
	}

	}
	  public class ObserverB implements Observer {
	  public void public void update(Observable o) {
	  // gets updated amount
	}

	}
	//instantiate concrete observableX
	ObservableX observableX = new ObservableX();
	//somewhere in code
	observableX.addObserver(new ObserverA());
	observableX.addObserver(new ObserverB());
	//much later

	observableX.setAmount(amount);

它是这样工作的：

首先我们创建一个 ObservableX 类的实例，将 ObserverA 和 ObserverB 实例添加到 observableX 对象中，然后在代码中的某个位置，我们使用 setAmount 方法设定“一定数量”的值。被观察者（observable）类的功能将接收到的数量通知所有注册的观察者。

观察者担当着中介的角色，维持接收者的列表。当组件里有事件发生时，该事件将被发送到列表上的所有接收者。

由于这个中介角色的存在，组件并不知道其接收者。而接收者可以订阅某个特定类型的不同组件中的事件。

![](https://static001.infoq.cn/resource/image/54/d9/54b1b2a9b1231ded68c60692660880d9.jpg)

当一个类使用事件将自身的变化通知观察者时，该类就可以成为一个组件。而这可以通过观察者模式来实现。

**使用组件比创建组件容易**

通过使用组件，你能够快速创建各种窗体、面板、窗口以及界面中的其他合成元素。不过，为了能够复用新的由组件创建的合成部分，应该将它们转化为组件。

为了实现这一目标，你需要决定组件所要生成的外部事件，以及消息传递机制。例如，你至少需要创建新的事件类并且定义接口或回调方法以接收这些事件。

这个方式让实现可复用的应用组件变得更复杂。当系统只是由少量合成元素组成时没什么问题——这时合成元素最多不超过 10 个。然而当系统包含数以百计的此类元素时，又当如何？

与之相反，不遵从这一方式将导致元素间的紧耦合，并且会把复用的机会降低到 0。这反过来会导致代码复制，从而让未来的代码维护变得更复杂，并将导致系统中的 bug 数量上升。

由于组件使用者往往不了解如何定义和传递他们自己的新事件，问题将变得更为严重。但他们可以轻松地使用组件框架提供的现成的事件。他们知道如何接收但不知道如何发送事件。

为了解决这个问题，让我们考虑如何简化应用中使用的事件模型。

**太多的事件监听者**

在 Java Swing、GWT、JSF 和 Vaadin 中，观察者模式被用于实现多用户能够订阅同一事件的模型，并将用于添加事件监听者的列表作为其实现方式。相关事件一旦发生，将被发送到列表上的全部接收者。

![](https://static001.infoq.cn/resource/image/ae/7d/aea60a3c95a0d9aebd9a90ccea42197d.jpg)

每个组件为一个或多个事件创建自己的事件监听者集合。这将导致应用中类的数量不断增多。反过来，这也会使系统的支持和开发变得更复杂。

借助注解机制（annotation），Java 找到了一条让单个方法订阅特定事件的道路。例如，考虑 Java EE 6 里的 CDI（Contexts and Dependency Injection，[上下文和依赖注入](http://docs.oracle.com/javaee/6/tutorial/doc/giwhb.html)）中对事件模型的实现。


	 public class PaymentHandler {
	      public void creditPayment(@Observes @Credit PaymentEvent event) {
		...
	      }
	}

	public class PaymentBean {

	    @Inject
	    @Credit
	    Event<<paymentevent> creditEvent;

	   public String pay() {
	     PaymentEvent creditPayload = new PaymentEvent();
		    // populate payload ... 
		    creditEvent.fire(creditPayload);
	      }
	}

你可以看到，当 PaymentBean 对象的 pay() 方法被调用时，PaymentEvent 被触发。接下来 PaymentHandler 对象的 creditPayment() 方法接收了它。

另一个例子是 [Guava 类库中事件总线](https://code.google.com/p/guava-libraries/wiki/EventBusExplained)的实现：


	// Class is typically registered by the container.
	class EventBusChangeRecorder {
	  @Subscribe public void recordCustomerChange(ChangeEvent e) {
	    recordChange(e.getChange());
	  }
	}
	// somewhere during initialization
	eventBus.register(new EventBusChangeRecorder());
	// much later
	public void changeCustomer() {
	  ChangeEvent event = getChangeEvent();
	  eventBus.post(event);
	}

EventBus 注册了 EventBusChangeRecorder 类的对象。接下来对 changeCustomer() 方法的调用会使 EventBus 接收 ChangeEvent 对象并调用 EventBusChangeRecorde 对象的 recordCustomerChange () 方法。

![](https://static001.infoq.cn/resource/image/0a/36/0a9953d5da6270e9afab0cf0b6c51336.jpg)

现在你不需要为你的组件实现若干事件监听者，在应用中使用事件也变得更简单了。

当所有组件都同时在屏幕上展现时，使用事件总线是很方便的。如下图所示，它们使用事件总线进行消息交换。

![](https://static001.infoq.cn/resource/image/9d/44/9de1651ed56559e8a108d28c51a0fa44.jpg)

这里，所有元素——标题、左侧的菜单、内容、右侧的面板——都是组件。

**订阅事件——别忘记取消订阅**

通过将事件监听者替换为注解，我们在简化事件模型使用的道路上前进了一大步。但即使如此，系统中的每个组件依旧需要连接到事件总线，然后，必须订阅上面的事件并在正确的时间取消订阅。

![](https://static001.infoq.cn/resource/image/ad/57/ad2ad8c9b113d3779292f416b80f0e57.jpg)

当相同的接收者多次订阅同一个事件时，将会出现许多重复提醒，这种情况很容易出现。而相似的情况还会在多个系统组件订阅同一事件时发生，这将会触发一系列级联事件。

为了能更好地控制事件模型，将工作与事件一起迁移到配置中，并让应用容器负责事件管理是很有意义的。由于特定的事件仅在特定条件下有效，将这些事件的状态管理迁移到配置中也是合理的。

![](https://static001.infoq.cn/resource/image/ad/57/ad2ad8c9b113d3779292f416b80f0e57.jpg)

下面是一段配置的例子：


	<?xml version="1.0"?>
	<application initial="A">

	    <view id="A">
		<on event="next" to="B"/>
	    </view>

	    <view id="B">
		<on event="previous" to="A"/>
		<on event="next" to="C"/>
	    </view>

	    <view id="C">
		<on event="previous" to="B"/>
		<on event="next" to="D"/>
	    </view>

	    <view id="D">
		<on event="previous" to="C"/>
		<on event="finish" to="finish"/>
	    </view>

	    <final id="finish" /> 

	</application>


视图 A 中的“下一个（next）”事件触发了向视图 B 的转变。在视图 B 中，用户可以通过“前一个（previous）”事件回到 A，或是通过“下一个（next）”事件进入 C。D 视图中的结束事件将转入“最终（final）”状态，将通知应用结束其中的工作流。

[有限状态机](http://en.wikipedia.org/wiki/Finite-state_machine)是专为这样的需求设计的。状态机是一种数学[计算模型](http://en.wikipedia.org/wiki/Model_of_computation)。它被设想为一种抽象的机器，可以处于有限数量的状态中的一个，并且在同一时间里只会处于一个状态——这被称为当前状态。事件或条件将触发向另一个状态的转变。使用这一方式，你能够轻松地定义活动画面，并让某事件来触发向另一个画面的转变。

**使用有限状态机来配置应用的好处**

大部分情况下，应用配置是静态定义的。使用依赖注入配置应用，我们在启动时定义应用结构。但我们忘记了在探索应用的过程中它的状态可能会改变。在应用的代码中，状态改变往往属于硬编码，它让未来的调整和维护变得复杂。

![](https://static001.infoq.cn/resource/image/90/80/90c0d0ed0f6c560ef3389b2934bdf980.jpg)

将状态间的转变迁移到配置中可以提高灵活性。而且这正是为什么我们在创建诸如窗体、窗口或面板等复杂应用元素时，无需为了应用应该进入哪个状态而操心。你可以稍后来处理它们，在配置中设定其行为。

![](https://static001.infoq.cn/resource/image/57/6f/57a0445b20616c088abc94a946c1996f.jpg)

所有组件都可以使用标准的事件发送机制进行交流——即通过事件总线。同时，[状态机](http://en.wikipedia.org/wiki/State_diagram)能够控制组件事件到事件总线的订阅。这一方式将应用的全部组件（窗体、窗口、面板）变为可复用组件，可以通过外部配置轻松地管理它们。

如果有兴趣，你可以看一下 [Enterprise Sampler](http://samples.lexaden.com/) 中一些配置的例子。

你也可以将状态配置看作城市的公路图，把事件看作递送商品的汽车，而将城市里的人看作目的地。

我确信采用这样的方式，不仅能够轻松地设计和构建一间规模虽小却做好了成长准备的房子，还能够建设拥有摩天大楼、公路和高速公路的城市。

![](https://static001.infoq.cn/resource/image/cb/78/cba9d840328b0ac35660cd0fd04cc178.jpg)

**关于作者**

![](https://static001.infoq.cn/resource/image/69/28/693eb14b06d627e4b23598541507c928.jpg)**Aliaksei Papou**是 [Lexaden.com](http://lexaden.com/) 的 CTO、软件架构师和联合创始人，他拥有超过 10 年的企业级应用开发经验，他对于技术创新有着强烈爱好。他与 Lexaden.com 的 CEODenis Skarbichev（另一位联合创始人）一同开发了可以创建大规模敏捷企业级应用的 [Lexaden Web Flow](http://www.lexaden.com/main/entry/web_flow) 语言。

**原文链接：** [How Would You Build Up a City from Components?](http://www.infoq.com/articles/component-city)
