---
title: spring的beanFactory和factoryBean
id: 952
date: 2024-10-31 22:01:47
author: daichangya
excerpt: 在Spring中有BeanFactory和FactoryBean这2个接口，从名字来看很相似，比较容易搞混。## 一、BeanFactory`BeanFactory`是一个接口，它是Spring中工厂的顶层规范，是SpringIoc容器的核心接口，它定义了`getBean()`、`containsBean()`等管理Bean的通用方法。Spring的容器都是它的具体实现如：
permalink: /archives/spring-de-beanFactory-he-factoryBean/
categories:
- spring
---


> 在Spring中有BeanFactory和FactoryBean这2个接口，从名字来看很相似，比较容易搞混。

## 一、BeanFactory

`BeanFactory`是一个接口，它是Spring中工厂的顶层规范，是SpringIoc容器的核心接口，它定义了`getBean()`、`containsBean()`等管理Bean的通用方法。Spring的容器都是它的具体实现如：

*   DefaultListableBeanFactory
    
*   XmlBeanFactory
    
*   ApplicationContext
    

这些实现类又从不同的维度分别有不同的扩展。

### 1.1、源码

```
public interface BeanFactory {

	//对FactoryBean的转义定义，因为如果使用bean的名字检索FactoryBean得到的对象是工厂生成的对象，
	//如果需要得到工厂本身，需要转义
	String FACTORY_BEAN_PREFIX = "&";

	//根据bean的名字，获取在IOC容器中得到bean实例
	Object getBean(String name) throws BeansException;

	//根据bean的名字和Class类型来得到bean实例，增加了类型安全验证机制。
	<T> T getBean(String name, @Nullable Class<T> requiredType) throws BeansException;

	Object getBean(String name, Object... args) throws BeansException;

	<T> T getBean(Class<T> requiredType) throws BeansException;

	<T> T getBean(Class<T> requiredType, Object... args) throws BeansException;

	//提供对bean的检索，看看是否在IOC容器有这个名字的bean
	boolean containsBean(String name);

	//根据bean名字得到bean实例，并同时判断这个bean是不是单例
	boolean isSingleton(String name) throws NoSuchBeanDefinitionException;

	boolean isPrototype(String name) throws NoSuchBeanDefinitionException;

	boolean isTypeMatch(String name, ResolvableType typeToMatch) throws NoSuchBeanDefinitionException;

	boolean isTypeMatch(String name, @Nullable Class<?> typeToMatch) throws NoSuchBeanDefinitionException;

	//得到bean实例的Class类型
	@Nullable
	Class<?> getType(String name) throws NoSuchBeanDefinitionException;

	//得到bean的别名，如果根据别名检索，那么其原名也会被检索出来
	String[] getAliases(String name);
}
复制代码
```

### 1.1、使用场景

*   从Ioc容器中获取Bean(byName or byType)
*   检索Ioc容器中是否包含指定的Bean
*   判断Bean是否为单例

## 二、FactoryBean

首先它是一个Bean，但又不仅仅是一个Bean。它是一个能生产或修饰对象生成的工厂Bean，类似于设计模式中的工厂模式和装饰器模式。它能在需要的时候生产一个对象，且不仅仅限于它自身，它能返回任何Bean的实例。

### 2.1、源码

```
public interface FactoryBean<T> {

	//从工厂中获取bean
	@Nullable
	T getObject() throws Exception;

	//获取Bean工厂创建的对象的类型
	@Nullable
	Class<?> getObjectType();

	//Bean工厂创建的对象是否是单例模式
	default boolean isSingleton() {
		return true;
	}
}
复制代码
```

从它定义的接口可以看出，`FactoryBean`表现的是一个工厂的职责。 **即一个Bean A如果实现了FactoryBean接口，那么A就变成了一个工厂，根据A的名称获取到的实际上是工厂调用`getObject()`返回的对象，而不是A本身，如果要获取工厂A自身的实例，那么需要在名称前面加上'`&`'符号。**

*   getObject('name')返回工厂中的实例
*   getObject('&name')返回工厂本身的实例

通常情况下，bean 无须自己实现工厂模式，Spring 容器担任了工厂的 角色；但少数情况下，容器中的 bean 本身就是工厂，作用是产生其他 bean 实例。由工厂 bean 产生的其他 bean 实例，不再由 Spring 容器产生，因此与普通 bean 的配置不同，不再需要提供 class 元素。

### 2.2、示例

先定义一个Bean实现FactoryBean接口

```
@Component
public class MyBean implements FactoryBean {
    private String message;
    public MyBean() {
        this.message = "通过构造方法初始化实例";
    }
    @Override
    public Object getObject() throws Exception {
        // 这里并不一定要返回MyBean自身的实例，可以是其他任何对象的实例。
        //如return new Student()...
        return new MyBean("通过FactoryBean.getObject()创建实例");
    }
    @Override
    public Class<?> getObjectType() {
        return MyBean.class;
    }
    public String getMessage() {
        return message;
    }
}
复制代码
```

MyBean实现了FactoryBean接口的两个方法，getObject()是可以返回任何对象的实例的，这里测试就返回MyBean自身实例，且返回前给message字段赋值。同时在构造方法中也为message赋值。然后测试代码中先通过名称获取Bean实例，打印message的内容，再通过`&+名称`获取实例并打印message内容。

```
@RunWith(SpringRunner.class)
@SpringBootTest(classes = TestApplication.class)
public class FactoryBeanTest {
    @Autowired
    private ApplicationContext context;
    @Test
    public void test() {
        MyBean myBean1 = (MyBean) context.getBean("myBean");
        System.out.println("myBean1 = " + myBean1.getMessage());
        MyBean myBean2 = (MyBean) context.getBean("&myBean");
        System.out.println("myBean2 = " + myBean2.getMessage());
        System.out.println("myBean1.equals(myBean2) = " + myBean1.equals(myBean2));
    }
}
复制代码
```

```
myBean1 = 通过FactoryBean.getObject()初始化实例
myBean2 = 通过构造方法初始化实例
myBean1.equals(myBean2) = false
复制代码
```

### 2.3、使用场景

说了这么多，为什么要有`FactoryBean`这个东西呢，有什么具体的作用吗？  
FactoryBean在Spring中最为典型的一个应用就是用来**创建AOP的代理对象**。

我们知道AOP实际上是Spring在运行时创建了一个代理对象，也就是说这个对象，是我们在运行时创建的，而不是一开始就定义好的，这很符合工厂方法模式。更形象地说，AOP代理对象通过Java的反射机制，在运行时创建了一个代理对象，在代理对象的目标方法中根据业务要求织入了相应的方法。这个对象在Spring中就是——`ProxyFactoryBean`。

所以，FactoryBean为我们实例化Bean提供了一个更为灵活的方式，我们可以通过FactoryBean创建出更为复杂的Bean实例。

## 三、区别

*   他们两个都是个工厂，但`FactoryBean`本质上还是一个Bean，也归`BeanFactory`管理
*   `BeanFactory`是Spring容器的顶层接口，`FactoryBean`更类似于用户自定义的工厂接口。

> 总结

`BeanFactory`与`FactoryBean`的区别确实容易混淆，死记硬背是不行的，最好还是从源码层面，置于spring的环境中去理解。

参考：  
[www.cnblogs.com/yulinfeng/p…](https://www.cnblogs.com/yulinfeng/p/11456587.html)  
[www.cnblogs.com/guitu18/p/1…](https://www.cnblogs.com/guitu18/p/11284894.html)
