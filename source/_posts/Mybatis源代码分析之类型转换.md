---
title: Mybatis源代码分析之类型转换
id: 420
date: 2024-10-31 22:01:43
author: daichangya
excerpt: "ORM框架最重要功能是将面向对象方法中的对象和关系型数据库中的表关联了起来，在关联过程中就必然涉及到对象中的数据类型和数据库中的表字段类型的转换，Mybatis中的org.apache.ibatis.type包主要就是实现这个功能。

一、org.apache.ibatis.type的基础类

在mybatis的官网中（http//mybatis.github.io/mybatis-3/"
permalink: /archives/21643999/
tags: 
 - mybatis
---

 

ORM框架最重要功能是将面向对象方法中的对象和关系型数据库中的表关联了起来，在关联过程中就必然涉及到对象中的数据类型和数据库中的表字段类型的转换，Mybatis中的org.apache.ibatis.type包主要就是实现这个功能。

## 一、org.apache.ibatis.type的基础类

在mybatis的官网中（[http://mybatis.github.io/mybatis-3/configuration.html#typeHandlers](http://mybatis.github.io/mybatis-3/configuration.html#typeHandlers "http://mybatis.github.io/mybatis-3/configuration.html#typeHandlers")）关于类型转换有如下的描述

Whenever MyBatis sets a parameter on a PreparedStatement or retrieves a value from a ResultSet, a TypeHandler is used to retrieve the value in a means appropriate to the Java type.

当MyBatis为PreparedStatement 设置参数时或者从ResultSet中获取数据时，会根据Java类型使用TypeHandler 去获取相应的值。

官网中也列出了每一个TypeHandler用来处理对应的ＪＤＢＣ类型和ＪＡＶＡ类型。

#### 1、TypeHandler接口

这个接口有三个方法，一个set，用来给PreparedStatement对象对应的列设置参数；两个get,从ResultSet和CallableStatement获取对应列的值,不同之处是一个是取第几个位置的值，一个是取具体列名所对应的值。set用来将Java对象中的数据类型转换为JDBC中对应的数据类型，get用来将JDBC中对应的数据类型转换为Java对象中的数据类型转换。

[![image](http://images.cnitblog.com/blog/330894/201304/09100900-6f126927fed141f8945da1ee490529e2.png "image")](http://images.cnitblog.com/blog/330894/201304/09100858-f18f504dd4e34d4fb58a3fbc767e303a.png)

#### 2、BaseTypeHandler抽象类

在进行软件设计时提倡面向接口的设计，但接口只是一个接口，并不做任何实质性的操作，还需有一系列的实现才可以真正的达到目标。BaseTypeHandler类便是对TypeHandler接口的初步实现，在实现TypeHandler接口的三个函数外，又引入了3个抽象函数用于null值的处理。

[![image](http://images.cnitblog.com/blog/330894/201304/09100904-893e6b705df544fd85110b9491332daa.png "image")](http://images.cnitblog.com/blog/330894/201304/09100902-2454cf566fb44260b3cc5678c684154a.png)

#### 3、DateTypeHandler

书接上文，BaseTypeHandler类也是一个抽象类，按照Java的规定抽象类并不能初始化，也不能直接使用，因而还需要有具体的类。在type包中有十多个具体的类来具体处理类型转换，每一个类处理一个数据类型，像long、int、double等等，我们以一个稍微复杂些的DateTypeHandler类为例，了解下对日期是如何进行处理的。

### 1）setNonNullParameter

```
public void setNonNullParameter(PreparedStatement ps, int i, Object parameter, JdbcType jdbcType)
      throws SQLException {
    ps.setTimestamp(i, new java.sql.Timestamp(((Date) parameter).getTime()));
}
```

首先将参数parameter这个Object转换为Date类型，而后通过Date对象的getTime()将日期转为毫秒数，而后再将毫秒数转换为java.sql.Timestamp对象。即将**java.util.Date**对象转换为**java.sql.Timestamp**对象。

### 2）getNullableResult

```
public Object getNullableResult(ResultSet rs, String columnName)
      throws SQLException {
    java.sql.Timestamp sqlTimestamp = rs.getTimestamp(columnName);
    if (sqlTimestamp != null) {
      return new java.util.Date(sqlTimestamp.getTime());
    }
    return null;
  }

  public Object getNullableResult(CallableStatement cs, int columnIndex)
      throws SQLException {
    java.sql.Timestamp sqlTimestamp = cs.getTimestamp(columnIndex);
    if (sqlTimestamp != null) {
      return new java.util.Date(sqlTimestamp.getTime());
    }
    return null;
  }
```

从上面的代码可以看出这两个函数的作用就是将 **java.sql.Timestamp**对象转换为 **java.util.Date**对象.

#### 4、类图

综合而言，type包基础类的类图示例如下：

[![image](http://images.cnitblog.com/blog/330894/201304/09100907-d41f9977555e4996a785f3c7b727f756.png "image")](http://images.cnitblog.com/blog/330894/201304/09100905-778ee570e04c49dbb72ce6d98972c62d.png)

## 二、自定义类型处理或覆盖默认的类型处理

在mybatis的官网中（[http://mybatis.github.io/mybatis-3/configuration.html#typeHandlers](http://mybatis.github.io/mybatis-3/configuration.html#typeHandlers "http://mybatis.github.io/mybatis-3/configuration.html#typeHandlers")）关于有如下的描述:

You can override the type handlers or create your own to deal with unsupported or non-standard types. To do so, simply extend theorg.apache.ibatis.type.BaseTypeHandler class and optionally map your new TypeHandler class to a JDBC type.

可以覆盖type handler或者创建自己的type handler去处理mybatis不支持的或者非标准的数据类型。实现这个功能，只需要继承org.apache.ibatis.type.BaseTypeHandler类然后选择新的TypeHandler类和JDBC类型的对应关系即可。

在官网中也给出了详细了示例，这里不再进行重复。其中用到了两个注解：MappedJdbcTypes 和 MappedTypes，我们可以看下这两个注解的定义文件：

```
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface MappedJdbcTypes {
    public JdbcType[] value();
}

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface MappedTypes {
    public Class[] value();
}
```

MappedJdbcTypes传入的是JdbcType类型的（JdbcType是type包中的一个枚举类型），MappedTypes传入的Class类型。

在声明完自己的类型转换之后，还需要让mybatis知道这些新的类型转换类，这可以通过在配置文件中添加typeHandlers节点来实现。可以添加一个类，也可以添加一个包中所有的类。

```
<typeHandlers>
  <typeHandler handler="org.mybatis.example.ExampleTypeHandler"/>
  <package name="org.mybatis.example"/>
</typeHandlers>
```

#### 三、typeHandler的注册：TypeHandlerRegistry

前面介绍了mybatis中已定义好的typeHandler，也介绍了如何自定义typehandler，以及如何让mybatis知道这次自定义的typehandler。现在剩下最关键的步骤，在mybatis初始化后如何将这些typehandler注册到mybatis中，在执行数据库操作去使用这些类。这些操作是由TypeHandlerRegistry类实施的。

我们已经知道，mybatis在使用时需要一个配置文件来进行各种各样的设置，与这个配置文件相对应的是org.apache.ibatis.session.Configuration这个类，配置文件中每一项都对应Configuration类中的一个属性，typehand就是Configuration类中的一个属性。

> protected final TypeHandlerRegistry typeHandlerRegistry = new TypeHandlerRegistry();

我们现在来看看TypeHandlerRegistry类中常用的方法及其作用。

### 1、TypeHandlerRegistry类中的属性和常用方法

```
private static final Map<Class<?>, Class<?>> reversePrimitiveMap = new HashMap<Class<?>, Class<?>>() {
    {
      put(Byte.class, byte.class);
      put(Short.class, short.class);
      put(Integer.class, int.class);
      put(Long.class, long.class);
      put(Float.class, float.class);
      put(Double.class, double.class);
      put(Boolean.class, boolean.class);
    }
  };

  private final Map<JdbcType, TypeHandler> JDBC_TYPE_HANDLER_MAP = new EnumMap<JdbcType, TypeHandler>(JdbcType.class);
  private final Map<Class<?>, Map<JdbcType, TypeHandler>> TYPE_HANDLER_MAP = new HashMap<Class<?>, Map<JdbcType, TypeHandler>>();
  private final TypeHandler UNKNOWN_TYPE_HANDLER = new UnknownTypeHandler(this);
```

##### 1）reversePrimitiveMap

可以看出来，这个map就是一个java中的基本数据类型和他们对应的类一一关联起来，像Byte和byte。在进行注册时会用到这个属性，详见第三小节。

##### 2）JDBC\_TYPE\_HANDLER_MAP

JdbcType和typehandler的对应关系，通过如下的函数进行维护

```
public void register(JdbcType jdbcType, TypeHandler handler) {
    JDBC_TYPE_HANDLER_MAP.put(jdbcType, handler);
}
```

##### 3）TYPE\_HANDLER\_MAP

TYPE\_HANDLER\_MAP属相是一个关键的属性，java类型和jdbctype的对应关系及处理类都存在这个属性中，从这个map的定义中可以看到多个jdbc类型能够对应到一个java类型。通过如下的函数进行维护：

```
public void register(Class<?> type, JdbcType jdbcType, TypeHandler handler) {
    //先查看这个java类型是否已经绑定过了，如果没有绑定过，创建了一个map，否则就直接添加新的
    Map<JdbcType, TypeHandler> map = TYPE_HANDLER_MAP.get(type);
    if (map == null) {
      map = new HashMap<JdbcType, TypeHandler>();
      TYPE_HANDLER_MAP.put(type, map);
    }
    map.put(jdbcType, handler);
    //如果当前添加的是属于Byte、Long等类型，将其对应的基本类型也进行注册
    if (reversePrimitiveMap.containsKey(type)) {
      register(reversePrimitiveMap.get(type), jdbcType, handler);
    }
  }
```

##### 4）注册自定义type handler

在注册自定义的type handler之前需要先定位到具体的类或者包，类的处理比较简单，直接利用java的反射机制就可以知道这个类的Class属性了。对于包就稍微复杂些，在mybatis中是利用io包ResolverUtil类中的find函数来实现的，这里不做详细介绍，等介绍到mybatis的io包时再详细说明。我们来看注册包的函数：

```
public void register(String packageName) {
    //    先声明一个ResolverUtil对象
    ResolverUtil<Class<?>> resolverUtil = new ResolverUtil<Class<?>>();
    //    利用find函数找到这个包里所有的类，并且放到resolverUtil 的matches属性中
    resolverUtil.find(new ResolverUtil.IsA(TypeHandler.class), packageName);
    Set<Class<? extends Class<?>>> handlerSet = resolverUtil.getClasses();
    //通过for循环依次将加载
    for (Class<?> type : handlerSet) {
      //Ignore inner classes and interfaces (including package-info.java) and abstract classes 
      //不处理内部类、接口、抽象类以及packgee_info类     
      if (!type.isAnonymousClass() && !type.isInterface() && !Modifier.isAbstract(type.getModifiers())) {
        try {
          //利用反射机制创建一个typehandler
          TypeHandler handler = (TypeHandler) type.getConstructor().newInstance();
          //注册
          register(handler);
        } catch (Exception e) {
          throw new RuntimeException("Unable to find a usable constructor for " + type, e);
        }
      }
    }
  }
```

从上面的代码中可以看到，真正进行注册用到的是如下的函数，先处理MappedTypes这个注解：

```
public void register(TypeHandler handler) {
    boolean mappedTypeFound = false;
    //判断这个类是否有MappedTypes这个注解
    MappedTypes mappedTypes = (MappedTypes) handler.getClass().getAnnotation(MappedTypes.class);
    if (mappedTypes != null) {
      for (Class<?> handledType : mappedTypes.value()) {
          //进行注册并设置mappedTypeFound变量为true  
          register(handledType, handler);
          mappedTypeFound = true;
      }
    }
    //如果mappedTypeFound为false，则抛出一个异常，
    //
    //注意，这里和官网上的示例不同，官网上的示例并没有这个注解，
    //但是在源代码中如果没有这个注解则不会继续下去，
    //因而如果是要自定义类型转换，还是需要添加这个注解
    if (!mappedTypeFound) {
      throw new RuntimeException("Unable to get mapped types, check @MappedTypes annotation for type handler " + handler);
    }
  }
```

上面的函数又调用了如下的函数，去处理MappedJdbcTypes注解：

```
public void register(Class<?> type, TypeHandler handler) {
    MappedJdbcTypes mappedJdbcTypes = (MappedJdbcTypes) handler.getClass().getAnnotation(MappedJdbcTypes.class);
   //    对注解进行判断，如果有MappedJdbcTypes这个注解，则对其对应的jdbctype依次进行注册，否则注册为null
     if (mappedJdbcTypes != null) {
      for (JdbcType handledJdbcType : mappedJdbcTypes.value()) {
        register(type, handledJdbcType, handler);
      }
    } else {
      register(type, null, handler);
    }
  }
```

最后调用第三小节中提到的函数进行注册到map中，供程序执行时调用。

#### 四、TypeHandlerRegistry的初始化

前面介绍了如何自定义类型转换处理类并注册到mybatis中，那type包中有不少mybatis已实现的类型转换处理类，这些类是如何及在何时注册到mybatis中的呢？

mybatis中的实现很简单，它把这些都放在了TypeHandlerRegistry的构造函数中了。由于构造函数比较大，也没有用到什么新方法，再此就不贴代码了，有兴趣的读者可以自己去观看。

#### 五、小结

    本文对Mybatis中的type转换做了介绍，介绍了其设计结构、常用的方法、如何自定义类型处理类、如何进行注册等内容，希望对大家理解mybatis如何实现java类型到JDBC类型转换有所帮助。

    当然，这里这是介绍了如何转换，但是这些转换是怎么使用的并没有涉及，这些内容将放到mybatis的executor中进行介绍。