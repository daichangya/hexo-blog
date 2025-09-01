---
title: Java的设计模式
id: 942
date: 2024-10-31 22:01:47
author: daichangya
excerpt: 生命中唯一不变的事实就是世事时刻在变。这在软件开发的每一个阶段都不可避免。我们所要面对的挑战是：要以最小的延迟和最大的灵活性来适应变化。令人欣慰的是有人已经解决了你的设计问题，而且他们的方法已经形成了最佳实践了；这些公认为最佳实践的方法就是“设计模式”。今天我们要研究两个最流行的设计模式，学习怎样使用好的设计让你得代码更干净，让扩展性更好。适配器模式(Adapter
  Design
permalink: /archives/Java-de-she-ji-mo-shi/
categories:
- 设计模式
tags:
- 设计模式
---

 

生命中唯一不变的事实就是世事时刻在变。这在软件开发的每一个阶段都不可避免。我们所要面对的挑战是：要以最小的延迟和最大的灵活性来适应变化。

令人欣慰的是有人已经解决了你的设计问题，而且他们的方法已经形成了最佳实践了；这些公认为最佳实践的方法就是“[设计模式](http://www.amazon.cn/gp/product/B001130JN8/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&tag=importnew-23&linkCode=as2&camp=536&creative=3200&creativeASIN=B001130JN8 "设计模式:可复用面向对象软件的基础")”。今天我们要研究两个最流行的设计模式，学习怎样使用好的设计让你得代码更干净，让扩展性更好。

适配器模式(Adapter Design Pattern)

我们假设你有一个旧系统，现在你需要让它适应新的三方库，但是这个库用的是完全不同的API。旧系统适用的接口是完全不同于新库的。当然，你若够勇敢的话，可以改掉旧的代码以适用新的接口。但是对于所有旧系统来说，千万不要这么做。

![mismatch.jpg](https://images.jsdiff.com/mismatch_1610075974303.jpg)

适配器模式救了你的命！你可以简单的写一个适配器(新的封装类)

> 好的设计不仅是可以重复使用，还要具有可扩展性。

适配器使用了接口，并且转换成客户端可以解析的接口，使不兼容的类联系在一起。


![adapterWorks.jpg](https://images.jsdiff.com/adapterWorks_1610075988499.jpg)

实战适配器设计模式

好了，闲话少说，我们来实战演习。我们旧系统使用的是下面的LegacyVideoController接口来控制视频系统。

```
publicinterface LegacyVideoController{
 
   /**
    * Begins the playback after startTimeTicks
    * from the beginning of the video
    * @param startTimeTicks time in milliseconds
    */
   publicvoid startPlayback(long startTimeTicks);
   ...
}
```

客户端这样使用控制器：

```
publicvoid playBackVideo(long timeToStart, LegacyVideoController controller){
   if(controller!=null){
      controller.startPlayback(timeToStart);
   }
}
```

用户需求变了！

用户需求改变也不是什么新鲜事——这时常发生。用户需求总是在变，而我们的系统需要适应新的视频控制器，接口如下：

```
publicinterface AdvancedVideoController{
   /**
    * Places the controller head after time
    * from the beginning of the track
    * @param time time defines how much seek is required
    */
   publicvoid seek(Time time);
 
   /**
    * Plays the track
    */
   publicvoid play();
}
```

然后客户端代码失效了，新的接口不再兼容了。

适配器救了我们

那么我们如何处理这个改变了的接口，而不改变我们旧的代码呢？你知道答案了，不是吗？我们写个简单的适配器类，就像这样：

```
publicclass AdvancedVideoControllerAdapter implementsLegacyVideoController {
 
   privateAdvancedVideoController advancedVideoController;
 
   publicAdvancedVideoControllerAdapter(AdvancedVideoController advancedVideoController){
      this.advancedVideoController = advancedVideoController;
   }
 
   @Override
   publicvoid startPlayback(long startTimeTicks) {
 
      // Convert long into DateTime
      Time startTime = getTime(startTimeTicks);
 
      // Adapt
      advancedVideoController.seek(startTime);
      advancedVideoController.play();
   }
}
```

适配器实现了目标的接口，所以不需要更改客户端代码。我们的适配器类中含有需要兼容的接口(AdvancedVideoController)的实例。

> 这种“has-a”的关系让适配器将客户端的请求发给实际的实例。

适配器也能够减少客户端和实现代码之间的耦合。

现在我们可以简单的将新对象封装到适配器中去，而且不需要更改客户端代码，因为这个新对象已经兼容了以前的接口。

```
AdvancedVideoController advancedController = controllerFactory.createController();
// adapt
LegacyVideoController controllerAdapter = newAdvancedVideoControllerAdapter(advancedController);
playBackVideo(20, controllerAdapter);
```

适配器可以简单的传值，也可以提供一些扩展，取决于需要支持的接口的复杂度。类似的，如果目标接口很复杂，新的功能需要切分成多个类，适配器也可以封装不止一个对象。

和其他模式的比较

* 装饰模式(Decorator)：装饰模式改变了接口，将对象封装起来，加上新的功能。而适配器模式是将被适配的接口转换成能够被客户端代码理解的目标接口。

* 外观模式(Facade)：外观模式是将之前的接口的复杂性抽象化形成的全新的接口，而适配器模式是将一个接口转换成另外一个，可以让不兼容的接口之间可以互相沟通。

* 代理模式(Proxy): 代理模式提供同样的接口。而适配器模式提供不一样的接口。

* 桥梁模式(Bridge): 桥梁模式使得抽象和实现独立起来，而适配器是用来将客户端的请求转发到被适配者，以适应已有的接口。

单例模式(Singleton Design Pattern)

虽然有许多创建对象的模式存在，有一个模式为大家所熟知。今天我们来看看最简单的也是容易弄错的单例模式。

就如同它的名字，单例只创建类的一个实例并提供全局化的访问。应用的例子可以是应用层的缓存，线程池，连接等。对这些应用而言，有且只有一个实例已经足够，而且如果多过一个会影响稳定性，甚至不能实现应用的功能。

实现单例模式

用Java实现的最基本的框架如下：

```
publicclass ApplicationCache{
 
   privateMap<String,Object> attributeMap;
   // Static instance
   privatestatic ApplicationCache instance;
 
   // Static accessor method
   publicstatic ApplicationCache getInstance(){
      if(instance == null){
         instance == newApplicationCache();
      }
      returninstance;
   }
 
   // private Constructor
   privateApplicationCache(){
      attributeMap = createCache(); // Initialize the cache
   }
}
```

我们的例子中有一个和类同样类型的静态成员，可以由静态方法(getInstance())获得。我们使用了延迟初始化(Lazy Initialization)，直到运行时需要时才实例化cache。构造器是private的，所以不可以通过new来创建类的实例。为了获得cache，我们调用：

```
ApplicationCache cache = ApplicationCache.getInstance();
// use cache to improve performance
```

如果是单线程,上面的代码没什么问题。但事情没有那么简单。多线程环境下，你要么同步延迟初始化(lazy initializtion)，或者不用延迟初始化，在加载类的时候就创建cache，通过使用静态程序块(static block)或者初始的时候声明cache可以做到。

双重检查锁定

我们通过延迟初始化来确保初始化的代码段只运行了一次。下面的代码在Java version 5.0以上上运行得很好，因为synchronized和volatile特性已经实现了。

```
publicclass ApplicationCache{
 
   privateMap<String,Object> attributeMap;
   // volatile so that JVM out-of-order writes do not happen
   privatestatic volatile ApplicationCache instance;
 
   publicstatic ApplicationCache getInstance(){
      // Checked once
      if(instance == null){
         // Synchronized on Class level lock
         synchronized(ApplicationCache.class){
            // Checked again
            if(instance == null){
               instance == newApplicationCache();
            }
         }
      }
      returninstance;
   }
 
   privateApplicationCache(){
      attributeMap = createCache(); // Initialize the cache
   }
}
```

我们让instance变量volatile，这样JVM避免了乱序写操作(out-of-order writes)。在对初始作同步时，对instance是否是null检查了两次，这样就避免了两个以上的线程创建多过一个cache的实例。我们也可以同步整个静态方法，但这种做法又太过了，因为我们在初始化之前只会调用一次，之后就不需要再同步了。

不用延迟初始化

更简单的方法是不使用延迟初始化，下面的代码看起来更简洁些：

```
publicclass ApplicationCache{
 
   privateMap<String,Object> attributeMap;
   // Initialized while declaration
   privatestatic ApplicationCache instance = newApplicationCache();
 
   publicstatic ApplicationCache getInstance(){
      returninstance;
   }
 
   // private Construcutor
   privateApplicationCache(){
      attributeMap = createCache(); // Initialize the cache
   }
}
```

加载类的时候变量会初始化，这样会调用私有的构造器来创建实例，使得只有一个cache实例。我们虽然没有了延迟初始化所带来的好处，但我们的代码更简洁些。两种方法都是线程安全的，你可以根据你的项目环境任选一种。

小心反射(Reflection)和序列化(Serialization)

根据你的需求，你可能要小心：

* 反射(Reflection)API会调用私有的构造器，所以为了防止创建超过一个实例，可以通过从构造器抛出异常来解决。

* 类似的，序列化和反序列化可能会创建两个不同的实例，可以通过重写序列化API中的readResolve()方法来解决。

设计模式与语言无关

我承认这个教程的标题有点误导，因为设计模式是与编程语言无关的。它们是那些解决软件设计中的重复问题的最佳方法的集合。

举个例子，下面是Javascript对单例模式的实现。概念是一样的：对创建对象进行控制和一个全局的访问，但实现随着语言的不同而不同。

```
varapplicationCache = function() {
 
   // Private stuff
   varinstance;
 
   functioninitCache() {
      return{
         proxyUrl:"/bin/getCache.json",
         cachePurgeTime:5000,
         permissions: {
            read:"everyone",
            write:"admin"
         }
      };
   }
 
   // Public
   return{
      getInstance:function() {
         if(!instance) instance = initCache();
         returninstance;
      },
      purgeCache:function() {
         instance = null;
      }
   };
};
```

另一个例子是jQuery也使用了大量的Facade设计模式，隐藏了子系统的复杂性，将更简化的接口呈现给用户。

结束语

> 不是所有的问题都需要某个设计模式来解决

要提醒一句：不要过度使用设计模式！不是所有的问题都需要某个设计模式来解决。你需要在使用之前仔细分析。学习设计模式有助于理解其他类库如jQuery, Spring等等，它们都大量使用了设计模式。

我希望读了这篇文章之后，你能更了解设计模式。如果你有什么问题或者想知道更多的设计模式，请留言，我会尽力解答！

英文原文：[tutsplus](http://net.tutsplus.com/tutorials/other/design-patterns-in-java)