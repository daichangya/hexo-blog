---
title: Java设计模式概述
id: bc65558b-bbf3-428b-822b-7639c0573d1b
date: 2024-11-25 10:49:18
author: daichangya
cover: https://images.jsdiff.com/design02.jpg
excerpt: Java的设计模式概述 一、设计模式的重要性 在软件开发领域，变化是永恒的主题。从项目的启动到维护，需求的变更、技术的演进以及环境的变化无处不在。而我们面临的关键挑战，就是要以最小的延迟和最大的灵活性来适应这些变化。幸运的是，前人在应对各种设计问题时积累了丰富的经验，并形成了被广泛认可的最佳实践，这
permalink: /archives/Java-she-ji-mo-shi-gai-shu/
categories:
- 设计模式
---

# Java的设计模式概述

## 一、设计模式的重要性
在软件开发领域，变化是永恒的主题。从项目的启动到维护，需求的变更、技术的演进以及环境的变化无处不在。而我们面临的关键挑战，就是要以最小的延迟和最大的灵活性来适应这些变化。幸运的是，前人在应对各种设计问题时积累了丰富的经验，并形成了被广泛认可的最佳实践，这就是“设计模式”。设计模式为我们提供了经过验证的解决方案，能够帮助我们打造出更优质、更具扩展性的软件系统。接下来，我们将深入探讨两种流行的设计模式：适配器模式和单例模式。

### （一）适配器模式（Adapter Design Pattern）
1. **适配器模式的应用场景**
   - 假设存在一个旧系统，其原本使用特定接口与系统的其他部分交互。然而，当需要引入一个新的三方库时，问题出现了。新库采用了完全不同的API，与旧系统适用的接口不兼容。此时，直接修改旧系统的代码以适应新接口是一种非常冒险且不推荐的做法，尤其是对于大型复杂的旧系统而言，可能会引发一系列难以预料的问题。而适配器模式就如同救世主一般，为我们提供了一种优雅的解决方案。它允许我们创建一个适配器（新的封装类），使不兼容的类能够协同工作。
2. **适配器模式的原理与作用**
   - 适配器模式利用接口，将不兼容的接口进行转换，使其能够被客户端正确解析。通过这种方式，它在不兼容的类之间架起了一座桥梁，实现了不同接口之间的通信。
3. **实战适配器设计模式**
   - **旧系统接口与客户端代码**：旧系统使用`LegacyVideoController`接口来控制视频系统，例如：
```java
public interface LegacyVideoController {
    /**
     * Begins the playback after startTimeTicks
     * from the beginning of the video
     * @param startTimeTicks time in milliseconds
     */
    public void startPlayback(long startTimeTicks);
    // 其他可能的方法...
}
```
客户端使用该控制器的方式如下：
```java
public void playBackVideo(long timeToStart, LegacyVideoController controller) {
    if (controller!= null) {
        controller.startPlayback(timeToStart);
    }
}
```
   - **用户需求变更与新接口**：随着业务发展，用户需求发生改变，新的视频控制器接口`AdvancedVideoController`被引入：
```java
public interface AdvancedVideoController {
    /**
     * Places the controller head after time
     * from the beginning of the track
     * @param time time defines how much seek is required
     */
    public void seek(Time time);

    /**
     * Plays the track
     */
    public void play();
}
```
这导致原有的客户端代码失效，因为新接口与旧接口不兼容。
   - **适配器类的实现**：为解决接口不兼容问题，我们创建一个适配器类`AdvancedVideoControllerAdapter`：
```java
public class AdvancedVideoControllerAdapter implements LegacyVideoController {
    private AdvancedVideoController advancedVideoController;

    public AdvancedVideoControllerAdapter(AdvancedVideoController advancedVideoController) {
        this.advancedVideoController = advancedVideoController;
    }

    @Override
    public void startPlayback(long startTimeTicks) {
        // 将 long 类型转换为 Time 类型（假设存在相应转换方法）
        Time startTime = getTime(startTimeTicks);

        // 适配操作
        advancedVideoController.seek(startTime);
        advancedVideoController.play();
    }
}
```
适配器实现了目标接口`LegacyVideoController`，这样就无需更改客户端代码。适配器类持有需要兼容的接口`AdvancedVideoController`的实例，通过“has - a”关系将客户端请求转发给实际实例。
   - **适配器的使用与优势**：现在，我们可以将新对象封装到适配器中，无需修改客户端代码，因为新对象已通过适配器兼容了旧接口。例如：
```java
AdvancedVideoController advancedController = controllerFactory.createController();
// 适配
LegacyVideoController controllerAdapter = new AdvancedVideoControllerAdapter(advancedController);
playBackVideo(20, controllerAdapter);
```
适配器不仅可以简单地传递值，还能根据需要支持的接口复杂度提供扩展功能。如果目标接口复杂，需要多个类来实现新功能，适配器也可以封装多个对象。
4. **与其他模式的比较**
   - **装饰模式（Decorator）**：装饰模式主要用于给对象添加新功能，它会改变对象的接口，通过封装对象来实现功能增强。而适配器模式的重点是将不兼容的接口转换为客户端可理解的接口，不改变被适配对象的功能，只是使其能与客户端协同工作。
   - **外观模式（Facade）**：外观模式是将一个或多个复杂子系统的接口抽象为一个更简单的统一接口，为客户端提供一个高层次的、易于使用的接口，隐藏了子系统的复杂性。适配器模式则专注于使两个不兼容的接口能够相互通信，不涉及对接口复杂性的抽象。
   - **代理模式（Proxy）**：代理模式为目标对象提供了一个代理，代理和目标对象实现相同的接口，客户端通过代理来访问目标对象，通常用于控制对目标对象的访问、增强目标对象的功能或进行资源管理等。适配器模式提供的是不同的接口，目的是适配不兼容的接口。
   - **桥梁模式（Bridge）**：桥梁模式的核心是将抽象部分与实现部分分离，使它们可以独立变化，通过组合的方式将抽象和实现联系起来。适配器模式主要是用于转发客户端请求到被适配者，以适应已有接口，不涉及抽象与实现的分离。

### （二）单例模式（Singleton Design Pattern）
1. **单例模式的概念与应用场景**
   - 单例模式正如其名，旨在确保一个类只有一个实例，并提供全局访问点。在许多应用场景中，如应用层的缓存、线程池、数据库连接等，只需要一个实例就足以满足需求。若存在多个实例，可能会导致资源浪费、数据不一致等问题，甚至影响系统的稳定性和功能实现。
2. **单例模式的实现方式**
   - **基本实现框架（Java）**：
```java
public class ApplicationCache {
    private Map<String, Object> attributeMap;
    // 静态实例
    private static ApplicationCache instance;

    // 静态访问方法
    public static ApplicationCache getInstance() {
        if (instance == null) {
            instance = new ApplicationCache();
        }
        return instance;
    }

    // 私有构造函数
    private ApplicationCache() {
        attributeMap = createCache(); // 初始化缓存
    }
}
```
在这个例子中，类中有一个与类类型相同的静态成员，通过静态方法`getInstance()`获取实例。采用了延迟初始化（Lazy Initialization）策略，即直到运行时需要实例时才创建。构造函数被设为私有，防止通过`new`关键字创建多个实例。
   - **多线程环境下的考虑 - 双重检查锁定**：在多线程环境中，上述基本实现可能会出现问题。为确保初始化代码只执行一次，可使用双重检查锁定机制（适用于Java 5.0及以上版本）：
```java
public class ApplicationCache {
    private Map<String, Object> attributeMap;
    // 使用 volatile 关键字，防止JVM乱序写操作
    private static volatile ApplicationCache instance;

    public static ApplicationCache getInstance() {
        // 第一次检查
        if (instance == null) {
            // 同步类级锁
            synchronized (ApplicationCache.class) {
                // 第二次检查
                if (instance == null) {
                    instance = new ApplicationCache();
                }
            }
        }
        return instance;
    }

    private ApplicationCache() {
        attributeMap = createCache(); // 初始化缓存
    }
}
```
通过将`instance`变量声明为`volatile`，避免了JVM的乱序写操作。在初始化时进行两次`null`检查，有效防止多个线程创建多个实例。虽然也可以选择同步整个静态方法，但这样会增加不必要的性能开销，因为在初始化完成后，后续访问不再需要同步。
   - **另一种实现方式 - 不使用延迟初始化**：如果不考虑延迟初始化的好处，还可以采用更简单的实现方式：
```java
public class ApplicationCache {
    private Map<String, Object> attributeMap;
    // 在声明时初始化
    private static ApplicationCache instance = new ApplicationCache();

    public static ApplicationCache getInstance() {
        return instance;
    }

    // 私有构造函数
    private ApplicationCache() {
        attributeMap = createCache(); // 初始化缓存
    }
}
```
在类加载时就初始化变量，调用私有构造函数创建实例，保证只有一个实例存在。这种方式代码更简洁，但失去了延迟初始化的特性，可根据项目实际需求选择合适的实现方式。
3. **单例模式的注意事项**
   - **反射（Reflection）问题**：Java的反射API可以调用私有构造函数，这可能导致创建多个实例。为防止这种情况，可以在构造函数中抛出异常来阻止反射创建额外的实例。
   - **序列化（Serialization）问题**：序列化和反序列化过程可能会创建两个不同的实例。可以通过重写序列化API中的`readResolve()`方法来解决，确保反序列化时返回的是单例实例。
4. **设计模式与语言无关性**
   - 虽然本文以Java为例介绍设计模式，但实际上设计模式是与编程语言无关的。它们是解决软件设计中常见问题的通用最佳实践方法。例如，在Javascript中实现单例模式的概念与Java相同，但具体实现方式会因语言特性而异：
```javascript
var applicationCache = function() {
    // 私有变量
    var instance;

    function initCache() {
        return {
            proxyUrl: "/bin/getCache.json",
            cachePurgeTime: 5000,
            permissions: {
                read: "everyone",
                write: "admin"
            }
        };
    }

    // 公共接口
    return {
        getInstance: function() {
            if (!instance) instance = initCache();
            return instance;
        },
        purgeCache: function() {
            instance = null;
        }
    };
};
```
此外，像jQuery等库也大量使用了设计模式，如Facade设计模式，用于隐藏子系统的复杂性，为用户提供更简单易用的接口。

### （三）总结与建议
1. **设计模式的合理运用**
   - 设计模式是软件开发中的强大工具，但并非所有问题都需要使用设计模式来解决。在实际应用中，应根据具体情况仔细分析，避免过度使用设计模式。过度使用可能会导致代码过于复杂，增加维护成本。
2. **学习设计模式的意义**
   - 学习设计模式有助于深入理解其他类库和框架的设计思想。许多流行的类库和框架，如jQuery、Spring等，都广泛应用了各种设计模式。掌握设计模式能够更好地阅读和使用这些类库，提高开发效率和软件质量。

希望通过本文的介绍，读者能对设计模式有更深入的理解和认识。如果在学习或使用设计模式过程中有任何疑问或需要进一步了解的内容，欢迎留言交流。