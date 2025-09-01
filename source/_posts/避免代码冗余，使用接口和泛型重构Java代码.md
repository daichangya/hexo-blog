---
title: 避免代码冗余，使用接口和泛型重构Java代码
id: 766
date: 2024-10-31 22:01:45
author: daichangya
excerpt: "在使用动态语言和.NET工作了若干年后，我又回到老本行–Java开发。在Ruby中，清除代码冗余是非常方便的，而在Java中则需要结合接口和泛型实现类似的功能。"
permalink: /archives/18565423/
categories:
 - 软件设计
---

在使用动态语言和.NET工作了若干年后，我又回到老本行–Java开发。在Ruby中，清除代码冗余是非常方便的，而在Java中则需要结合接口和泛型实现类似的功能。

**原始代码**

以下是这个类中的一些方法用于后续的阐述。为了使例子更简洁，我移除了些代码。

```
public V get(final K key) {
        Session s;
        try {
            s = oGrid.getSession();
            ObjectMap map = s.getMap(cacheName);
            return (V) map.get(key);
        } catch (ObjectGridException oge) {
            throw new RuntimeException("Error performing cache operation", oge);
        } finally {
            if (s != null)
                s.close();
        }
        return null;
    }

    public void put(final K key, final V value) {
        Session s;
        try {
            s = oGrid.getSession();
            ObjectMap map = s.getMap(cacheName);
            map.upsert(key, value);
        } catch (ObjectGridException oge) {
            throw new RuntimeException("Error performing cache operation", oge);
        } finally {
            if (s != null)
                s.close();
        }
    }

    public Map<K, V> getAll(Set<? extends K> keys) {
        final List<V> valueList = new ArrayList<V>();
        final List<K> keyList = new ArrayList<K>();
        keyList.addAll(keys);

        Session s;
        try {
            s = oGrid.getSession();
            ObjectMap map = s.getMap(cacheName);
            valueList.addAll(map.getAll(keyList));
        } catch (ObjectGridException oge) {
            throw new RuntimeException("Error performing cache operation", oge);
        } finally {
            if (s != null)
                s.close();
        }

        Map<K, V> map = new HashMap<K, V>();
        for (int i = 0; i < keyList.size(); i++) {
            map.put(keyList.get(i), valueList.get(i));
        }
        return map;
    }
```

**遇到的问题**

```
        Session s;
        try {
            s = oGrid.getSession();
            ObjectMap map = s.getMap(cacheName);
            // Some small bit of business logic goes here
        } catch (ObjectGridException oge) {
            throw new RuntimeException("Error performing cache operation", oge);
        } finally {
            if (s != null)
                s.close();
        }
```

上面的代码段几乎存在于类的每个方法中，这违反了DRY原则 。将来如果需要改变检索Session 和 ObjectMap实例的方式，或着某天这段代码被发现有缺陷，我们就不得不修改每个(包含这段代码的)方法，因此需要找到一种方式来复用这些执行代码。

**重构后的代码**

为了传递包含了原方法中业务逻辑的实例，我们创建一个带有抽象方法的 Executable 接口 。execute()方法参数为我们欲操作的ObjectMap实例。
```
interface Executable<T> {
  public T execute(ObjectMap map) throws ObjectGridException;
}
```
由于我们的目的仅仅是在每个方法中操作ObjectMap实例，可以创建executeWithMap()方法封装前述的那一大段重复代码。这个方法的参数是Executable接口的实例，实例包含着操作map的必要逻辑(译者注：这样Executable接口的实例中就是纯粹的业务逻辑，实现了解耦合)。

```
 private <T> T executeWithMap(Executable<T> ex) {
        Session s;
        try {
            s = oGrid.getSession();
            ObjectMap map = s.getMap(cacheName);
            // Execute our business logic
            return ex.execute(map);
        } catch (ObjectGridException oge) {
            throw new RuntimeException("Error performing cache operation", oge);
        } finally {
            if (s != null)
                s.close();
        }
    }
```
现在，可以用如下形式的模板代码替换掉第一个例子中的代码：这个模板创建了一个匿名内部类，实现了Executable接口和execute()方法。其中execute()方法执行业务逻辑，并以getXXX()的方式返回结果(若为Void方法，返回null)
```
public V get(final K key) {
  return executeWithMap(new Executable<V>() {
      public V execute(ObjectMap map) throws ObjectGridException {
          return (V) map.get(key);
      }
  });              
}      

public void put(final K key, final V value) {
  executeWithMap(new Executable<Void>() {
      public Void execute(ObjectMap map) throws ObjectGridException {
          map.upsert(key, value);
          return null;
      }
  });              
}

public Map<K, V> getAll(Set<? extends K> keys) {
  final List<K> keyList = new ArrayList<K>();
  keyList.addAll(keys);
  List<V> valueList = executeWithMap(new Executable<List<V>>() {
      public List<V> execute(ObjectMap map) throws ObjectGridException {
          return map.getAll(keyList);
      }
  });                              

  Map<K, V> map = new HashMap<K, V>();
  for(int i = 0; i < keyList.size(); i++) {
      map.put(keyList.get(i), valueList.get(i));
  }
  return map;
}
```
**FunctionalInterface Annotation (功能接口注释)**

Java 8 的 @FunctionalInterface annotation 使这一切变的简单。若某接口带有一个抽象方法，这个接口便可以被用作为lambda表达式的参数，称为功能接口。
```
@FunctionalInterface
interface Executable<T> {
  public T execute(ObjectMap map) throws ObjectGridException;
}
```
只要接口仅仅包含一个抽象方法，便可以使用这个annotation。这样就能减少相当数量的模板代码。

```
public V get(final K key) {
        return executeWithMap((ObjectMap map) -> (V) map.get(key));
    }

    public void put(final K key, final V value) {
        executeWithMap((ObjectMap map) -> {
            map.upsert(key, value);
            return null;
        });
    }

    public Map<K, V> getAll(Set<? extends K> keys) {
        final List<K> keyList = new ArrayList<K>();
        keyList.addAll(keys);
        List<V> valueList = executeWithMap((ObjectMap map) -> map.getAll(keyList));

        Map<K, V> map = new HashMap<K, V>();
        for (int i = 0; i < keyList.size(); i++) {
            map.put(keyList.get(i), valueList.get(i));
        }
        return map;
    }
```

**结论**

实现这些重构我很开心。它比原始的代码略复杂一点，但是更简明，更DRY，所以一切都是值得的。 尽管还有提升的空间，但这是一个良好的开始。

原文链接： [michaelbrameld](http://www.michaelbrameld.com/blog/2013/11/02/refacoring-java-generic-functional-interface/) 