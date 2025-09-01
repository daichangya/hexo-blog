---
title: MyBatis 缓存机制深度解剖
id: 1131
date: 2024-10-31 22:01:49
author: daichangya
excerpt: 缓存概述 正如大多数持久层框架一样，MyBatis 同样提供了一级缓存和二级缓存的支持
permalink: /archives/MyBatis-huan-cun-ji-zhi-shen-du-jie-pou/
tags:
- mybatis
- 缓存
---

 

缓存概述  

*   正如大多数持久层框架一样，MyBatis 同样提供了一级缓存和二级缓存的支持；
*   一级缓存基于 [PerpetualCache](http://grepcode.com/file/repo1.maven.org/maven2/org.mybatis/mybatis/3.0.1/org/apache/ibatis/cache/impl/PerpetualCache.java#PerpetualCache) 的 HashMap 本地缓存，其存储作用域为 Session，当 Session flush 或 close 之后，该Session中的所有 Cache 就将清空。
*   二级缓存与一级缓存其机制相同，默认也是采用 PerpetualCache，HashMap存储，不同在于其存储作用域为 Mapper(Namespace)，并且可自定义存储源，如 Ehcache、Hazelcast等。
*   对于缓存数据更新机制，当某一个作用域(一级缓存Session/二级缓存Namespaces)的进行了 C/U/D 操作后，默认该作用域下所有 select 中的缓存将被clear。
*   MyBatis 的缓存采用了delegate机制 及 装饰器模式设计，当put、get、remove时，其中会经过多层 delegate cache 处理，其Cache类别有：**BaseCache**(基础缓存)、**EvictionCache**(排除算法缓存) 、**DecoratorCache**(装饰器缓存)：          **BaseCache         ：**为缓存数据最终存储的处理类，默认为 PerpetualCache，基于Map存储；可自定义存储处理，如基于EhCache、Memcached等；   
              **EvictionCache    ：**当缓存数量达到一定大小后，将通过算法对缓存数据进行清除。默认采用 Lru 算法(LruCache)，提供有 fifo 算法(FifoCache)等；   
              **DecoratorCache：**缓存put/get处理前后的装饰器，如使用 LoggingCache 输出缓存命中日志信息、使用 SerializedCache 对 Cache的数据 put或get 进行序列化及反序列化处理、当设置flushInterval(默认1/h)后，则使用 ScheduledCache 对缓存数据进行定时刷新等。
*   一般缓存框架的数据结构基本上都是 Key-Value 方式存储，MyBatis 对于其 Key 的生成采取规则为：\[hashcode : checksum : mappedStementId : offset : limit : executeSql : queryParams\]。
*   对于并发 Read/Write 时缓存数据的同步问题，MyBatis 默认基于 JDK/concurrent中的[ReadWriteLock](http://ilkinbalkanay.blogspot.com/2008/01/readwritelock-example-in-java.html)，使用[ReentrantReadWriteLock](http://man.ddvip.com/program/java_api_zh/java/util/concurrent/locks/ReadWriteLock.html) 的实现，从而通过 Lock 机制防止在并发 Write Cache 过程中线程安全问题。

  
源码剖解  
接下来将结合 MyBatis 序列图进行源码分析。在分析其Cache前，先看看其整个处理过程。   
**执行过程**:  
![](http://dl.iteye.com/upload/attachment/518760/d7e1c109-87e8-3baa-bf8b-94465c75d898.png "点击查看原始大小图片")  
① 通常情况下，我们需要在 Service 层调用 Mapper Interface 中的方法实现对数据库的操作，上述根据产品 ID 获取 Product 对象。   
② 当调用 ProductMapper 时中的方法时，其实这里所调用的是 [MapperProxy](http://grepcode.com/file/repo1.maven.org/maven2/org.mybatis/mybatis/3.0.1/org/apache/ibatis/binding/MapperProxy.java#MapperProxy) 中的方法，并且 MapperProxy已经将将所有方法拦截，其具体原理及分析，参考 [MyBatis+Spring基于接口编程的原理分析](http://denger.iteye.com/blog/1060588)，其 invoke 方法代码为：   



      //当调用 Mapper 所有的方法时，将都交由Proxy 中的 invoke 处理：  
      public Object invoke(Object proxy, Method method, Object\[\] args) throws Throwable {  
          try {  
            if (!OBJECT_METHODS.contains(method.getName())) {  
              final Class declaringInterface = findDeclaringInterface(proxy, method);  
              // 最终交由 MapperMethod 类处理数据库操作，初始化 MapperMethod 对象  
              final MapperMethod mapperMethod = new MapperMethod(declaringInterface, method, sqlSession);  
              // 执行 mapper method，返回执行结果   
              final Object result = mapperMethod.execute(args);  
              ....  
              return result;  
            }  
          } catch (SQLException e) {  
            e.printStackTrace();  
          }  
          return null;  
        }  

  
③其中的 mapperMethod 中的 execute  方法代码如下：   



      public Object execute(Object\[\] args) throws SQLException {  
          Object result;  
          // 根据不同的操作类别，调用 DefaultSqlSession 中的执行处理  
          if (SqlCommandType.INSERT == type) {  
            Object param = getParam(args);  
            result = sqlSession.insert(commandName, param);  
          } else if (SqlCommandType.UPDATE == type) {  
            Object param = getParam(args);  
            result = sqlSession.update(commandName, param);  
          } else if (SqlCommandType.DELETE == type) {  
            Object param = getParam(args);  
            result = sqlSession.delete(commandName, param);  
          } else if (SqlCommandType.SELECT == type) {  
            if (returnsList) {  
              result = executeForList(args);  
            } else {  
              Object param = getParam(args);  
              result = sqlSession.selectOne(commandName, param);  
            }  
          } else {  
            throw new BindingException("Unkown execution method for: " + commandName);  
          }  
          return result;  
        }  

由于这里是根据 ID 进行查询，所以最终调用为 sqlSession.selectOne函数。也就是接下来的的 DefaultSqlSession.selectOne 执行；   
④ ⑤ 可以在 [DefaultSqlSession](http://grepcode.com/file/repo1.maven.org/maven2/org.mybatis/mybatis/3.0.1/org/apache/ibatis/session/defaults/DefaultSqlSession.java#DefaultSqlSession) 看到，其 selectOne 调用了 selectList 方法：



      public Object selectOne(String statement, Object parameter) {  
          List list = selectList(statement, parameter);  
          if (list.size() == 1) {  
            return list.get(0);  
          }   
          ...  
      }  

      public List selectList(String statement, Object parameter, RowBounds rowBounds) {  
          try {  
            MappedStatement ms = configuration.getMappedStatement(statement);  
            // 如果启动用了Cache 才调用 CachingExecutor.query，反之则使用 BaseExcutor.query 进行数据库查询   
            return executor.query(ms, wrapCollection(parameter), rowBounds, Executor.NO\_RESULT\_HANDLER);  
          } catch (Exception e) {  
            throw ExceptionFactory.wrapException("Error querying database.  Cause: " + e, e);  
          } finally {  
            ErrorContext.instance().reset();  
          }  
      }  

⑥到这里，已经执行到具体数据查询的流程，在分析 CachingExcutor.query 前，先看看 MyBatis 中 Executor 的结构及构建过程。   
  
  
**执行器(Executor)**:  
[Executor](http://grepcode.com/file/repo1.maven.org/maven2/org.mybatis/mybatis/3.0.1/org/apache/ibatis/executor/Executor.java#Executor):  执行器接口。也是最终执行数据获取及更新的实例。其类结构如下：   
![](http://dl.iteye.com/upload/attachment/518977/421423d6-4dcf-3748-9e99-c66b1bb77780.png)  
[BaseExecutor](http://grepcode.com/file/repo1.maven.org/maven2/org.mybatis/mybatis/3.0.1/org/apache/ibatis/executor/BaseExecutor.java#BaseExecutor): 基础执行器抽象类。实现一些通用方法，如createCacheKey 之类。并且采用 模板模式 将具体的数据库操作逻辑(doUpdate、doQuery)交由子类实现。另外，可以看到变量 localCache: PerpetualCache，在该类采用 PerpetualCache 实现基于 Map 存储的一级缓存，其 query 方法如下：



      public List query(MappedStatement ms, Object parameter, RowBounds rowBounds, ResultHandler resultHandler) throws SQLException {  
          ErrorContext.instance().resource(ms.getResource()).activity("executing a query").object(ms.getId());  
          // 执行器已关闭  
          if (closed) throw new ExecutorException("Executor was closed.");  
          List list;  
          try {  
            queryStack++;   
            // 创建缓存Key  
            CacheKey key = createCacheKey(ms, parameter, rowBounds);   
            // 从本地缓存在中获取该 key 所对应 的结果集  
            final List cachedList = (List) localCache.getObject(key);   
            // 在缓存中找到数据  
            if (cachedList != null) {   
              list = cachedList;  
            } else { // 未从本地缓存中找到数据，开始调用数据库查询  
              //为该 key 添加一个占位标记  
              localCache.putObject(key, EXECUTION_PLACEHOLDER);   
              try {  
                // 执行子类所实现的数据库查询 操作  
                list = doQuery(ms, parameter, rowBounds, resultHandler);   
              } finally {  
                // 删除该 key 的占位标记  
                localCache.removeObject(key);  
              }  
              // 将db中的数据添加至本地缓存中  
              localCache.putObject(key, list);  
            }  
          } finally {  
            queryStack--;  
          }  
          // 刷新当前队列中的所有 DeferredLoad实例，更新 MateObject  
          if (queryStack == 0) {   
            for (DeferredLoad deferredLoad : deferredLoads) {  
              deferredLoad.load();  
            }  
          }  
          return list;  
        }  

[BatchExcutor](http://grepcode.com/file/repo1.maven.org/maven2/org.mybatis/mybatis/3.0.1/org/apache/ibatis/executor/BatchExcutor.java#BatchExcutor)、[ReuseExcutor](http://grepcode.com/file/repo1.maven.org/maven2/org.mybatis/mybatis/3.0.1/org/apache/ibatis/executor/ReuseExcutor.java#ReuseExcutor)、[ SimpleExcutor](http://grepcode.com/file/repo1.maven.org/maven2/org.mybatis/mybatis/3.0.1/org/apache/ibatis/executor/SimpleExcutor.java#SimpleExcutor): 这几个就没什么好说的了，继承了 BaseExcutor 的实现其 doQuery、doUpdate 等方法，同样都是采用 JDBC 对数据库进行操作；三者区别在于，批量执行、重用 Statement 执行、普通方式执行。具体应用及场景在Mybatis 的文档上都有详细说明。   
  
[CachingExecutor](http://grepcode.com/file/repo1.maven.org/maven2/org.mybatis/mybatis/3.0.1/org/apache/ibatis/executor/CachingExecutor.java#CachingExecutor): 二级缓存执行器。个人觉得这里设计的不错，灵活地使用 delegate机制。其委托执行的类是 BaseExcutor。 当无法从二级缓存获取数据时，同样需要从 DB 中进行查询，于是在这里可以直接委托给 BaseExcutor 进行查询。其大概流程为：   
![](http://dl.iteye.com/upload/attachment/519008/0ddd9c89-53c5-3103-9c9e-d6ee28f36c2a.png)  
流程为： 从二级缓存中进行查询 -\> \[如果缓存中没有，委托给 BaseExecutor\] -> 进入一级缓存中查询 -> \[如果也没有\] -> 则执行 JDBC 查询，其 query 代码如下：



      public List query(MappedStatement ms, Object parameterObject, RowBounds rowBounds, ResultHandler resultHandler) throws SQLException {  
          if (ms != null) {  
            // 获取二级缓存实例  
            Cache cache = ms.getCache();  
            if (cache != null) {  
              flushCacheIfRequired(ms);  
              // 获取 读锁( Read锁可由多个Read线程同时保持)  
              cache.getReadWriteLock().readLock().lock();  
              try {  
                // 当前 Statement 是否启用了二级缓存  
                if (ms.isUseCache()) {  
                  // 将创建 cache key 委托给 BaseExecutor 创建  
                  CacheKey key = createCacheKey(ms, parameterObject, rowBounds);  
                  final List cachedList = (List) cache.getObject(key);  
                  // 从二级缓存中找到缓存数据  
                  if (cachedList != null) {  
                    return cachedList;  
                  } else {  
                    // 未找到缓存，很委托给 BaseExecutor 执行查询  
                    List list = delegate.query(ms, parameterObject, rowBounds, resultHandler);  
                    tcm.putObject(cache, key, list);  
                    return list;  
                  }  
                } else { // 没有启动用二级缓存，直接委托给 BaseExecutor 执行查询   
                  return delegate.query(ms, parameterObject, rowBounds, resultHandler);  
                }  
              } finally {  
                // 当前线程释放 Read 锁  
                cache.getReadWriteLock().readLock().unlock();  
              }  
            }  
          }  
          return delegate.query(ms, parameterObject, rowBounds, resultHandler);  
      }  

至此，已经完完了整个缓存执行器的整个流程分析，接下来是对缓存的 缓存数据管理实例进行分析，也就是其 Cache 接口，用于对缓存数据 put 、get及remove的实例对象。   
  
  
**Cache 委托链构建**:  
正如最开始的缓存概述所描述道，其缓存类的设计采用 装饰模式，基于委托的调用机制。   
缓存实例构建：  
缓存实例的构建 ，Mybatis 在解析其 Mapper 配置文件时就已经将该实现初始化，在 org.apache.ibatis.builder.xml.XMLMapperBuilder 类中可以看到：   



      private void cacheElement(XNode context) throws Exception {  
          if (context != null) {  
            // 基础缓存类型  
            String type = context.getStringAttribute("type", "PERPETUAL");  
            Class typeClass = typeAliasRegistry.resolveAlias(type);  
            // 排除算法缓存类型  
            String eviction = context.getStringAttribute("eviction", "LRU");  
            Class evictionClass = typeAliasRegistry.resolveAlias(eviction);  
            // 缓存自动刷新时间  
            Long flushInterval = context.getLongAttribute("flushInterval");  
            // 缓存存储实例引用的大小  
            Integer size = context.getIntAttribute("size");  
            // 是否是只读缓存  
            boolean readWrite = !context.getBooleanAttribute("readOnly", false);  
            Properties props = context.getChildrenAsProperties();  
            // 初始化缓存实现  
            builderAssistant.useNewCache(typeClass, evictionClass, flushInterval, size, readWrite, props);  
          }  
        }  

以下是  useNewCache 方法实现：   



      public Cache useNewCache(Class typeClass,  
                                 Class evictionClass,  
                                 Long flushInterval,  
                                 Integer size,  
                                 boolean readWrite,  
                                 Properties props) {  
          typeClass = valueOrDefault(typeClass, PerpetualCache.class);  
          evictionClass = valueOrDefault(evictionClass, LruCache.class);  
          // 这里构建 Cache 实例采用 Builder 模式，每一个 Namespace 生成一个  Cache 实例  
          Cache cache = new CacheBuilder(currentNamespace)  
              // Builder 前设置一些从XML中解析过来的参数  
              .implementation(typeClass)  
              .addDecorator(evictionClass)  
              .clearInterval(flushInterval)  
              .size(size)  
              .readWrite(readWrite)  
              .properties(props)  
              // 再看下面的 build 方法实现  
              .build();  
          configuration.addCache(cache);  
          currentCache = cache;  
          return cache;  
      }  

      public Cache build() {  
          setDefaultImplementations();  
          // 创建基础缓存实例  
          Cache cache = newBaseCacheInstance(implementation, id);  
          setCacheProperties(cache);  
          // 缓存排除算法初始化，并将其委托至基础缓存中  
          for (Class<? extends Cache> decorator : decorators) {  
            cache = newCacheDecoratorInstance(decorator, cache);  
            setCacheProperties(cache);  
          }  
          // 标准装饰器缓存设置，如LoggingCache之类，同样将其委托至基础缓存中  
          cache = setStandardDecorators(cache);  
          // 返回最终缓存的责任链对象  
          return cache;  
      }  

最终生成后的缓存实例对象结构：   
![](http://dl.iteye.com/upload/attachment/519089/bb42d63b-b52c-36b4-a30c-88b751d18d77.png)  
可见，所有构建的缓存实例已经通过责任链方式将其串连在一起，各 Cache 各负其责、依次调用，直到缓存数据被 Put 至 基础缓存实例中存储。   
  
  
**Cache 实例解剖**:  
实例类：[SynchronizedCache](http://grepcode.com/file/repo1.maven.org/maven2/org.mybatis/mybatis/3.0.2/org/apache/ibatis/cache/decorators/SynchronizedCache.java#SynchronizedCache)  
说   明：用于控制 ReadWriteLock，避免并发时所产生的线程安全问题。   
解   剖：  
对于 Lock 机制来说，其分为 Read 和 Write 锁，其 Read 锁允许多个线程同时持有，而 Write 锁，一次能被一个线程持有，如果当 Write 锁没有释放，其它需要 Write 的线程只能等待其释放才能去持有。   
其代码实现：



      public void putObject(Object key, Object object) {  
          acquireWriteLock();  // 获取 Write 锁  
          try {  
            delegate.putObject(key, object); // 委托给下一个 Cache 执行 put 操作  
          } finally {  
            releaseWriteLock(); // 释放 Write 锁  
          }  
        }  

对于 Read 数据来说，也是如此，不同的是 Read 锁允许多线程同时持有 :   



      public Object getObject(Object key) {  
          acquireReadLock();  
          try {  
            return delegate.getObject(key);  
          } finally {  
            releaseReadLock();  
          }  
        }  

其具体原理可以看看 jdk concurrent 中的 ReadWriteLock 实现。   
  
  
实例类：[LoggingCache](http://grepcode.com/file/repo1.maven.org/maven2/org.mybatis/mybatis/3.0.2/org/apache/ibatis/cache/decorators/LoggingCache.java#LoggingCache)  
说   明：用于日志记录处理，主要输出缓存命中率信息。   
解   剖：  
说到缓存命中信息的统计，只有在 get 的时候才需要统计命中率：   



      public Object getObject(Object key) {  
          requests++; // 每调用一次该方法，则获取次数+1  
          final Object value = delegate.getObject(key);  
          if (value != null) {  // 命中！ 命中+1  
            hits++;  
          }  
          if (log.isDebugEnabled()) {  
            // 输出命中率。计算方法为： hits / requets 则为命中率  
            log.debug("Cache Hit Ratio \[" + getId() + "\]: " + getHitRatio());  
          }  
          return value;  
      }  

  
  
  
实例类：[SerializedCache](http://grepcode.com/file/repo1.maven.org/maven2/org.mybatis/mybatis/3.0.2/org/apache/ibatis/cache/decorators/SerializedCache.java#SerializedCache)  
说   明：向缓存中 put 或 get 数据时的序列化及反序列化处理。   
解   剖：  
序列化在Java里面已经是最基础的东西了，这里也没有什么特殊之处：   



      public void putObject(Object key, Object object) {  
           // PO 类需要实现 Serializable 接口  
          if (object == null || object instanceof Serializable) {  
            delegate.putObject(key, serialize((Serializable) object));   
          } else {  
            throw new CacheException("SharedCache failed to make a copy of a non-serializable object: " + object);  
          }  
        }  

        public Object getObject(Object key) {  
          Object object = delegate.getObject(key);  
          // 获取数据时对 byte数据进行反序列化  
          return object == null ? null : deserialize((byte\[\]) object);  
        }  

其 serialize 及 deserialize 代码就不必要贴了。   
  
  
实例类：[LruCache](http://grepcode.com/file/repo1.maven.org/maven2/org.mybatis/mybatis/3.0.2/org/apache/ibatis/cache/decorators/LruCache.java#LruCache)  
说   明：最近最少使用的:移除最长时间不被使用的对象，基于LRU算法。   
解   剖：  
这里的 LRU 算法基于 LinkedHashMap 覆盖其 removeEldestEntry 方法实现。好象之前看过 XMemcached 的 LRU 算法也是这样实现的。   
初始化 LinkedHashMap，默认为大小为 1024 个元素：   



      public LruCache(Cache delegate) {  
          this.delegate = delegate;  
          setSize(1024); // 设置 map 默认大小  
      }  
      public void setSize(final int size) {  
          // 设置其 capacity 为size, 其 factor 为.75F  
          keyMap = new LinkedHashMap(size, .75F, true) {  
            // 覆盖该方法，当每次往该map 中put 时数据时，如该方法返回 True，便移除该map中使用最少的Entry  
            // 其参数  eldest 为当前最老的  Entry  
            protected boolean removeEldestEntry(Map.Entry eldest) {  
              boolean tooBig = size() > size;  
              if (tooBig) {  
                eldestKey = eldest.getKey(); //记录当前最老的缓存数据的 Key 值，因为要委托给下一个 Cache 实现删除  
              }  
              return tooBig;  
            }  
          };  
        }  

      public void putObject(Object key, Object value) {  
          delegate.putObject(key, value);  
          cycleKeyList(key);  // 每次 put 后，调用移除最老的 key  
      }  
      // 看看当前实现是否有 eldestKey, 有的话就调用 removeObject ，将该key从cache中移除  
      private void cycleKeyList(Object key) {  
          keyMap.put(key, key); // 存储当前 put 到cache中的 key 值  
          if (eldestKey != null) {  
            delegate.removeObject(eldestKey);  
            eldestKey = null;  
          }  
        }  

      public Object getObject(Object key) {  
          keyMap.get(key); // 便于 该 Map 统计 get该key的次数  
          return delegate.getObject(key);  
        }  

  
  
实例类：[PerpetualCache](http://grepcode.com/file/repo1.maven.org/maven2/org.mybatis/mybatis/3.0.2/org/apache/ibatis/cache/decorators/PerpetualCache.java#PerpetualCache)  
说   明：这个比较简单，直接通过一个 HashMap 来存储缓存数据。所以没什么说的，直接看下面的 MemcachedCache 吧。   
  
  
自定义二级缓存/Memcached  
其自定义二级缓存也较为简单，它本身默认提供了对 Ehcache 及 Hazelcast 的缓存支持：[Mybatis-Cache](http://code.google.com/p/mybatis/wiki/Caches)，我这里参考它们的实现，自定义了针对 Memcached 的缓存支持，其代码如下:   



      package com.xx.core.plugin.mybatis;  

      import java.util.LinkedList;  
      import java.util.concurrent.locks.ReadWriteLock;  
      import java.util.concurrent.locks.ReentrantReadWriteLock;  

      import org.apache.ibatis.cache.Cache;  
      import org.slf4j.Logger;  
      import org.slf4j.LoggerFactory;  

      import com.xx.core.memcached.JMemcachedClientAdapter;  
      import com.xx.core.memcached.service.CacheService;  
      import com.xx.core.memcached.service.MemcachedService;  

      /** 
       * Cache adapter for Memcached. 
       *  
       * @author denger 
       */  
      public class MemcachedCache implements Cache {  

          // Sf4j logger reference  
          private static Logger logger = LoggerFactory.getLogger(MemcachedCache.class);  

          /** The cache service reference. */  
          protected static final CacheService CACHE_SERVICE = createMemcachedService();  

          /** The ReadWriteLock. */  
          private final ReadWriteLock readWriteLock = new ReentrantReadWriteLock();  

          private String id;  
          private LinkedList<String> cacheKeys = new LinkedList<String>();  

          public MemcachedCache(String id) {  
              this.id = id;  
          }  
          // 创建缓存服务类，基于java-memcached-client  
          protected static CacheService createMemcachedService() {  
              JMemcachedClientAdapter memcachedAdapter;  

              try {  
                  memcachedAdapter = new JMemcachedClientAdapter();  
              } catch (Exception e) {  
                  String msg = "Initial the JMmemcachedClientAdapter Error.";  
                  logger.error(msg, e);  
                  throw new RuntimeException(msg);  
              }  
              return new MemcachedService(memcachedAdapter);  
          }  

          @Override  
          public String getId() {  
              return this.id;  
          }  

          // 根据 key 从缓存中获取数据  
          @Override  
          public Object getObject(Object key) {  
              String cacheKey = String.valueOf(key.hashCode());  
              Object value = CACHE_SERVICE.get(cacheKey);  
              if (!cacheKeys.contains(cacheKey)){  
                  cacheKeys.add(cacheKey);  
              }  
              return value;  
          }  

          @Override  
          public ReadWriteLock getReadWriteLock() {  
              return this.readWriteLock;  
          }  

          // 设置数据至缓存中  
          @Override  
          public void putObject(Object key, Object value) {  
              String cacheKey = String.valueOf(key.hashCode());  

              if (!cacheKeys.contains(cacheKey)){  
                  cacheKeys.add(cacheKey);  
              }  
              CACHE_SERVICE.put(cacheKey, value);  
          }  
          // 从缓存中删除指定 key 数据  
          @Override  
          public Object removeObject(Object key) {  
              String cacheKey = String.valueOf(key.hashCode());  

              cacheKeys.remove(cacheKey);  
              return CACHE_SERVICE.delete(cacheKey);  
          }  
          //清空当前 Cache 实例中的所有缓存数据  
          @Override  
          public void clear() {  
              for (int i = 0; i < cacheKeys.size(); i++){  
                  String cacheKey = cacheKeys.get(i);  
                  CACHE_SERVICE.delete(cacheKey);  
              }  
              cacheKeys.clear();  
          }  

          @Override  
          public int getSize() {  
              return cacheKeys.size();  
          }  
      }  

  
在  ProductMapper 中增加配置：   

Xml代码  ![收藏代码](http://www.iteye.com/images/icon_star.png)

      <cache eviction="LRU" type="com.xx.core.plugin.mybatis.MemcachedCache" />  

  
启动Memcached:   

      memcached -c 2000 -p 11211 -vv -U 0 -l 192.168.1.2 -v  

  
执行Mapper 中的查询、修改等操作，Test:   



         @Test  
          public void testSelectById() {  
              Long pid = 100L;  

              Product dbProduct = productMapper.selectByID(pid);  
              Assert.assertNotNull(dbProduct);  

              Product cacheProduct = productMapper.selectByID(pid);  
              Assert.assertNotNull(cacheProduct);  

              productMapper.updateName("IPad", pid);  

              Product product = productMapper.selectByID(pid);  
              Assert.assertEquals(product.getName(), "IPad");  
          }  

  
Memcached Loging:   
![](http://dl.iteye.com/upload/attachment/519096/b512954b-c8af-375e-b3ef-76c3caafc358.png)  
看上去没什么问题~ OK了。