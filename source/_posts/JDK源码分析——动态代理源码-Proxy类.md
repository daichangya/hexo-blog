---
title: JDK源码分析——动态代理源码(Proxy类)
id: 55
date: 2024-10-31 22:01:40
author: daichangya
excerpt: "读源码,怕过两天又忘记了,还是记录下吧..动态代理最重要的实现就是Proxy.newInstance ,那我们直接看这个方法public static Object newProxyInstance(ClassLoader loader,       Class[] interfaces,       InvocationHandler h)//这里有三个参数,第一个是传入classl"
permalink: /archives/7252173/
tags: 
 - 设计模式
---

 

```java
读源码,怕过两天又忘记了,还是记录下吧..
 
动态代理最重要的实现就是Proxy.newInstance ,那我们直接看这个方法
 
public static Object newProxyInstance(ClassLoader loader,
       Class<?>[] interfaces,
       InvocationHandler h)//这里有三个参数,第一个是传入classloader,一般情况是传入当前的classloader.但是我在上一节模拟实现里传入的是URL loader..第二个参数表示的是接口,第三个是Invocationhandler,除了第一个参数,其他和我在上一节里的一样.JDK的封装的比较好,所以他传入的是Interface的数组,
 throws IllegalArgumentException
    {
 if (h == null) {
     throw new NullPointerException();//如果Invocationhandler 为空,抛异常
 }
 
 /*
  * Look up or generate the designated proxy class.这个方法里最主要的地方在这里,它直接通过调用 getProxyClass方法获取到了自动生成的动态代理类的二进制码.在我上一节的内容里,我们是通过自己生成JAVA文件,然后通过JAVA文件动态编译成对应的class文件,然后通过URLClassLoader.loadClass("com.cjb.proxy.Proxy1");这个方法来获取对应的二进制码的.这个方法下面会继续解释.
  */
 Class cl = getProxyClass(loader, interfaces);
 
 /*
  * Invoke its constructor with the designated invocation handler.这个方法就是获取对应class的Constructor,然后通过这个Constructor来实例化..
  */
 try {
     Constructor cons = cl.getConstructor(constructorParams);
     return (Object) cons.newInstance(new Object[] { h });
 } catch (NoSuchMethodException e) {
     throw new InternalError(e.toString());
 } catch (IllegalAccessException e) {
     throw new InternalError(e.toString());
 } catch (InstantiationException e) {
     throw new InternalError(e.toString());
 } catch (InvocationTargetException e) {
     throw new InternalError(e.toString());
 }
    }
 
上面的方法,除了最重要的getProxyClass,其他都很容易理解.,那么下面开始读getProxyClass方法
 
public static Class<?> getProxyClass(ClassLoader loader, 
                                         Class<?>... interfaces)
 throws IllegalArgumentException
    {
 if (interfaces.length > 65535) {
     throw new IllegalArgumentException("interface limit exceeded");//JDK想的果然比较到位,连interface传的太多都想到了..~!~
 }
 
 Class proxyClass = null;//这个就是最后要生成的二进制码,首先初始化一下
 
 /* collect interface names to use as key for proxy class cache */
 String[] interfaceNames = new String[interfaces.length];//这个存放的是对应的Interface的名字..
 
 Set interfaceSet = new HashSet(); //这个HashSet 是为了检测interface重复记录的.
 
 for (int i = 0; i < interfaces.length; i++) {
     /*
      * Verify that the class loader resolves the name of this
      * interface to the same Class object.
      */
     String interfaceName = interfaces[i].getName();
     Class interfaceClass = null;
     try {
  interfaceClass = Class.forName(interfaceName, false, loader);//创建对应接口的二进制码,第二个参数false表示,不需要初始化
     } catch (ClassNotFoundException e) {
     }
     if (interfaceClass != interfaces[i]) {//如果创建出来的二进制码和原来的接口不一样,表示这个接口对于这个classloader来说是不可见的
  throw new IllegalArgumentException(
      interfaces[i] + " is not visible from class loader");
     }
 
     /*
      * Verify that the Class object actually represents an
      * interface.
      */
     if (!interfaceClass.isInterface()) {//如果不是接口,那么就抛异常,这里就规定了,我们必须通过接口来代理..或者说,必须面向接口编程
  throw new IllegalArgumentException(
      interfaceClass.getName() + " is not an interface");
     }
 
     /*
      * Verify that this interface is not a duplicate.前面说,InterfaceSet是拿来判断对应的interface接口是否有重复的.这里的方法是:在循环interfaces的时候,把每个interface都添加到interfaceSet里..当然,在添加之前会判断,当前循环到的接口在InterfaceSet里是否有,如果已经有了,则抛异常,说这个接口重复了..没有,则添加..
      */
     if (interfaceSet.contains(interfaceClass)) {
  throw new IllegalArgumentException(
      "repeated interface: " + interfaceClass.getName());
     }
     interfaceSet.add(interfaceClass);
 
     interfaceNames[i] = interfaceName;//这句就是把每个接口名放到interfaceNames数组里..
 }
 
 /*
  * Using string representations of the proxy interfaces as
  * keys in the proxy class cache (instead of their Class
  * objects) is sufficient because we require the proxy
  * interfaces to be resolvable by name through the supplied
  * class loader, and it has the advantage that using a string
  * representation of a class makes for an implicit weak
  * reference to the class.
  */
 Object key = Arrays.asList(interfaceNames);//这里把Interface数组转换成list..这里直接写成了Object类型
 
 /*
  * Find or create the proxy class cache for the class loader.
  */
 Map cache;//放缓存的Map
 synchronized (loaderToCache) {//loaderToCache也是一个Map.它的key是classloader,对应的value是对应的缓存,也是一个HashMap.他把对应的不同的classloader放到loaderToCache里,如果下次还要调用这个方法创建代理,并传入的是同一个classloader,那么可以直接从cache里取..增加速度.当然,如果没有,则创建一条记录,放到loaderToCache里
     cache = (Map) loaderToCache.get(loader);
     if (cache == null) {
  cache = new HashMap();
  loaderToCache.put(loader, cache);
     }
     /*
      * This mapping will remain valid for the duration of this
      * method, without further synchronization, because the mapping
      * will only be removed if the class loader becomes unreachable.
      */
 }
 
 /*
  * Look up the list of interfaces in the proxy class cache using
  * the key.  This lookup will result in one of three possible
  * kinds of values:
  *     null, if there is currently no proxy class for the list of
  *         interfaces in the class loader,
  *     the pendingGenerationMarker object, if a proxy class for the
  *         list of interfaces is currently being generated,
  *     or a weak reference to a Class object, if a proxy class for
  *         the list of interfaces has already been generated.
  */
 synchronized (cache) {
     /*
      * Note that we need not worry about reaping the cache for
      * entries with cleared weak references because if a proxy class
      * has been garbage collected, its class loader will have been
      * garbage collected as well, so the entire cache will be reaped
      * from the loaderToCache map.
      */
     do {
  Object value = cache.get(key);//这里从cache里获取对应的Object..第一次执行的话,明显获取到的是Null..key表示的是用接口名字转换而来的list..这个可以看上面的代码.
  if (value instanceof Reference) {
      proxyClass = (Class) ((Reference) value).get();//如果已经能获取到了,那么,我们需要的二进制码文件就是这个获取到的
  }
  if (proxyClass != null) {
      // proxy class already generated: return it
      return proxyClass;
  } else if (value == pendingGenerationMarker) {//这里的pendingGenerationMarker是一个静态常量,表示 new Object().JDK给出的 解释是,如果代理正在创建,那么等待他
      // proxy class being generated: wait for it
      try {
   cache.wait();
      } catch (InterruptedException e) {
   /*
    * The class generation that we are waiting for should
    * take a small, bounded time, so we can safely ignore
    * thread interrupts here.
    */
      }
      continue;
  } else {
      /*
       * No proxy class for this list of interfaces has been
       * generated or is being generated, so we will go and
       * generate it now.  Mark it as pending generation.
       */
      cache.put(key, pendingGenerationMarker);//如果cache里获取到的对应于key的value是Null ,那么,就创建一个object对象放进去.上面说了,pendingGenerationMarker= new Object();
      break;
  }
     } while (true);
 }
 
 try {
     String proxyPkg = null; // package to define proxy class in 这个是代理类的包名
 
     /*
      * Record the package of a non-public proxy interface so that the
      * proxy class will be defined in the same package.  Verify that
      * all non-public proxy interfaces are in the same package.
      */
     for (int i = 0; i < interfaces.length; i++) {
  int flags = interfaces[i].getModifiers();//getModifiers()方法返回的是该接口的修饰类型,用Int类型表示
  if (!Modifier.isPublic(flags)) {//如果不是public 的接口..
 
  //我们可以这样理解,我们动态创建的代理,他的修饰类型必须是和接口的修饰类型是一样的,我们知道,接口可以是public或者默认,两种修饰类型.这里的判断如果不是public接口,那么,该接口肯定是默认的,如果是默认修饰类型,那么,它只能被同一个包下面的类看到,所以,就必须为该代理类创建一个包名..当然,如果是public的话,就没必要,因为,反正所有的类都能看到..
      String name = interfaces[i].getName();
      int n = name.lastIndexOf('.');
      String pkg = ((n == -1) ? "" : name.substring(0, n + 1));//注意这里的N+1 ,其实是包括 "."的..比如 com.cjb.proxy.Proxy..它返回的就是"com.cjb.proxy."注意最后的那个点
 
      if (proxyPkg == null) {
   proxyPkg = pkg;
      } else if (!pkg.equals(proxyPkg)) {
   throw new IllegalArgumentException(
       "non-public interfaces from different packages");
      }
  }
     }
 
     if (proxyPkg == null) { // if no non-public proxy interfaces,这里可以看到,如果是public 的接口,对应代理类的包名就是"",也就是没有包名
  proxyPkg = "";  // use the unnamed package
     }
 
     {
  /*
   * Choose a name for the proxy class to generate.
   */
  long num;
  synchronized (nextUniqueNumberLock) {
      num = nextUniqueNumber++;//Num是一个计数器.用处是,创建代理的类名的时候用..我们可以看到,它是初始值是0.然后,每被调用一次,Num++.
  }
  String proxyName = proxyPkg + proxyClassNamePrefix + num;//proxyPkg是之前生成的包名, proxyClassNamePrefix 是一个静态常量,proxyClassNamePrefix="$Proxy".最后Num是计数器.也就是说,它的代理类的名字是从 $Proxy1 $Proxy2 $Proxy3一直在增长的,这样的话,就避免了重复.
  /*
   * Verify that the class loader hasn't already
   * defined a class with the chosen name.
   */
 
  /*
   * Generate the specified proxy class.下面打红字的两个方法是最后生成代理对象的..但是,很悲剧的是,他是用native修饰的,也就是说,它是不是用java来实现的..也就是说,最最关键的地方,不是用java实现的...
   */
  byte[] proxyClassFile = ProxyGenerator.generateProxyClass(
      proxyName, interfaces);
  try {
      proxyClass = defineClass0(loader, proxyName,
   proxyClassFile, 0, proxyClassFile.length);
  } catch (ClassFormatError e) {
      /*
       * A ClassFormatError here means that (barring bugs in the
       * proxy class generation code) there was some other
       * invalid aspect of the arguments supplied to the proxy
       * class creation (such as virtual machine limitations
       * exceeded).
       */
      throw new IllegalArgumentException(e.toString());
  }
     }
     // add to set of all generated proxy classes, for isProxyClass
     proxyClasses.put(proxyClass, null);
 
 } finally {
     /*
      * We must clean up the "pending generation" state of the proxy
      * class cache entry somehow.  If a proxy class was successfully
      * generated, store it in the cache (with a weak reference);
      * otherwise, remove the reserved entry.  In all cases, notify
      * all waiters on reserved entries in this cache.
      */
     synchronized (cache) {
  if (proxyClass != null) {
      cache.put(key, new WeakReference(proxyClass));
  } else {
      cache.remove(key);
  }
  cache.notifyAll();
     }
 }
 return proxyClass;
    }
 
可以看到,我们想看的,最重要的生成二进制码的方法,是native的..读了这么多源码,都是一些前期处理.关键的地方不知道..当然,虽然没看到关键的地方,但是对于它前面的处理的学习,也是非常有用的..看看JDK是怎么处理重名问题的,怎么处理cache.等等..
```