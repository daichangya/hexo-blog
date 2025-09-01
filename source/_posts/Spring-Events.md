---
title: Spring Events
id: 21
date: 2024-10-31 22:01:39
author: daichangya
permalink: /archives/Spring-Events/
categories:
- spring
---

## 1.Overview
在本文中，我们将讨论如何在Spring中使用事件。

Events件是框架中最容易被忽略的功能之一，但也是更有用的功能之一。而且，与Spring中的许多其他事情一样，Spring – event发布是ApplicationContext提供的功能之一。

有一些简单的准则可以遵循：
- 该事件应扩展ApplicationEvent
- 发布者应该注入一个ApplicationEventPublisher对象
- 侦听器应实现ApplicationListener接口

## 2.自定义事件(A Custom Event)
Spring允许创建和发布自定义事件，这些事件默认情况下是同步的。这具有一些优点-例如，侦听器能够参与发布者的交易环境。

2.1。一个简单的应用程序事件
让我们创建一个简单的事件类 –只是一个占位符来存储事件数据。在这种情况下，事件类包含String消息：

```
public class CustomSpringEvent extends ApplicationEvent {
    private String message;
 
    public CustomSpringEvent(Object source, String message) {
        super(source);
        this.message = message;
    }
    public String getMessage() {
        return message;
    }
}
```
#### 2.2. A Publisher
现在，让我们创建该事件的发布者。发布者构造事件对象并将其发布给正在收听的任何人。

要发布事件，发布者可以简单地注入ApplicationEventPublisher并使用publishEvent（） API：
```
@Component
public class CustomSpringEventPublisher {
    @Autowired
    private ApplicationEventPublisher applicationEventPublisher;
 
    public void doStuffAndPublishAnEvent(final String message) {
        System.out.println("Publishing custom event. ");
        CustomSpringEvent customSpringEvent = new CustomSpringEvent(this, message);
        applicationEventPublisher.publishEvent(customSpringEvent);
    }
}
```
或者，发布者类可以实现ApplicationEventPublisherAware接口–这还将在应用程序启动时注入事件发布者。通常，使用@Autowire注入发布者会更简单。

#### 2.3. A Listener
最后，让我们创建监听器。

侦听器的唯一要求是成为一个bean并实现  ApplicationListener接口：
```
@Component
public class CustomSpringEventListener implements ApplicationListener<CustomSpringEvent> {
    @Override
    public void onApplicationEvent(CustomSpringEvent event) {
        System.out.println("Received spring custom event - " + event.getMessage());
    }
}
```
注意，我们的自定义侦听器是如何通过自定义事件的通用类型进行参数设置的–这使onApplicationEvent（）方法类型安全。这也避免了必须检查对象是否是特定事件类的实例并进行强制转换。

并且，正如已经讨论的（默认情况下，spring事件是同步的），doStuffAndPublishAnEvent（）方法将阻塞，直到所有侦听器完成对事件的处理为止。

## 3.创建异步事件
在某些情况下，同步发布事件并不是我们真正想要的，我们可能需要异步处理事件。

您可以通过使用执行程序创建ApplicationEventMulticaster bean 来在配置中将其打开  。出于我们的目的，SimpleAsyncTaskExecutor效果很好：
```
@Configuration
public class AsynchronousSpringEventsConfig {
    @Bean(name = "applicationEventMulticaster")
    public ApplicationEventMulticaster simpleApplicationEventMulticaster() {
        SimpleApplicationEventMulticaster eventMulticaster =
          new SimpleApplicationEventMulticaster();
         
        eventMulticaster.setTaskExecutor(new SimpleAsyncTaskExecutor());
        return eventMulticaster;
    }
}
```
事件，发布者和侦听器的实现与以前相同–但是现在，侦听器将在单独的线程中异步处理事件。

## 4.现有框架事件
Spring本身可以发布各种事件。例如，ApplicationContext将触发各种框架事件。例如ContextRefreshedEvent，ContextStartedEvent，RequestHandledEvent等。

这些事件为应用程序开发人员提供了一个选项，可以挂接到应用程序和上下文的生命周期，并在需要时添加自己的自定义逻辑。

这是一个侦听器监听上下文刷新的快速示例：
```
public class ContextRefreshedListener 
  implements ApplicationListener<ContextRefreshedEvent> {
    @Override
    public void onApplicationEvent(ContextRefreshedEvent cse) {
        System.out.println("Handling context re-freshed event. ");
    }
}
```
要了解有关现有框架事件的更多信息，请在此处查看我们的下一个教程。

## 5.注释驱动的事件监听器
从Spring 4.2开始，事件侦听器不必是实现ApplicationListener接口的Bean  ，可以通过@EventListener批注在托管Bean的任何公共方法上注册它：
```
@Component
public class AnnotationDrivenContextStartedListener {
    // @Async
    @EventListener
    public void handleContextStart(ContextStartedEvent cse) {
        System.out.println("Handling context started event.");
    }
}
```
和以前一样，方法签名声明其使用的事件类型。和以前一样，此侦听器被同步调用。但是现在使其异步就像添加@Async注释一样简单  （不要忘记在应用程序中启用Async支持）。

## 6.泛型支持
还可以使用事件类型中的泛型信息来调度事件。

#### 6.1. A Generic Application Event
让我们创建一个通用事件类型。在我们的示例中，事件类包含任何内容和成功状态指示符：
```
public class GenericSpringEvent<T> {
    private T what;
    protected boolean success;
 
    public GenericSpringEvent(T what, boolean success) {
        this.what = what;
        this.success = success;
    }
    // ... standard getters
}
```
注意GenericSpringEvent和CustomSpringEvent之间的区别。现在，我们可以灵活地发布任何任意事件，并且不再需要从ApplicationEvent扩展它。

#### 6.2. A Listener
现在，让我们创建该事件的侦听器。我们可以像以前一样通过实现ApplicationListener接口来定义侦听器：

```
@Component
public class GenericSpringEventListener 
  implements ApplicationListener<GenericSpringEvent<String>> {
    @Override
    public void onApplicationEvent(@NonNull GenericSpringEvent<String> event) {
        System.out.println("Received spring generic event - " + event.getWhat());
    }
}
```
但不幸的是，此定义要求我们从  ApplicationEvent类继承GenericSpringEvent。因此，对于本教程，让我们利用前面讨论的注释驱动的事件侦听器。

通过在@EventListener注释上定义布尔SpEL表达式，  也可以使事件侦听器有条件。在这种情况下，the event handler will only be invoked for a successful GenericSpringEvent of String：

```
@Component
public class AnnotationDrivenEventListener {
    @EventListener(condition = "#event.success")
    public void handleSuccessful(GenericSpringEvent<String> event) {
        System.out.println("Handling generic event (conditional).");
    }
}
```
The Spring Expression Language (SpEL) is a powerful expression language that's covered in details in another tutorial
#### 6.3. A Publisher

事件发布类似于所描述的一个以上。但是由于类型擦除，我们需要发布一个事件来解析将要过滤的泛型参数。例如，类GenericStringSpringEvent扩展了GenericSpringEvent <String>。

还有一种发布事件的替代方法。如果我们从带有@EventListener注释的方法中返回非空值作为结果，Spring Framework将为我们发送该结果作为新事件。此外，作为事件处理的结果，我们可以通过将它们返回到集合中来发布多个新事件。

## 7. Transaction Bound Events
本段是关于使用@TransactionalEventListener批注的。要了解有关事务管理的更多信息，请查看“ Spring事务和JPA”教程。

从Spring 4.2开始，该框架提供了一个新的@TransactionalEventListener批注，它是@EventListener的扩展，它允许将事件的侦听器绑定到事务的某个阶段。可以绑定到以下事务阶段：

如果事务成功完成，则使用AFTER_COMMIT（默认值）来触发事件
AFTER_ROLLBACK –如果事务已回滚
AFTER_COMPLETION –如果事务已完成（AFTER_COMMIT和  AFTER_ROLLBACK的别名）
BEFORE_COMMIT  用于在事务提交之前立即触发事件
这是事务性事件侦听器的快速示例：
```
@TransactionalEventListener(phase = TransactionPhase.BEFORE_COMMIT)
public void handleCustom(CustomSpringEvent event) {
    System.out.println("Handling event inside a transaction BEFORE COMMIT.");
}
```
仅当存在事件生成器正在运行且即将提交的事务时，才会调用此侦听器。

而且，如果没有事务在运行，则除非我们通过将fallbackExecution  属性设置为true来覆盖此事件，否则根本不会发送该事件  。

## 8. Conclusion
在本快速教程中，我们介绍了在Spring中处理事件的基础知识-创建一个简单的自定义事件，将其发布，然后在侦听器中进行处理。

我们还简要介绍了如何在配置中启用事件的异步处理。

然后，我们了解了Spring 4.2中引入的改进，例如注释驱动的侦听器，更好的泛型支持以及绑定到事务阶段的事件。

与往常一样，可以在Github上获得本文中提供的代码。这是一个基于Maven的项目，因此应该很容易直接导入和运行。