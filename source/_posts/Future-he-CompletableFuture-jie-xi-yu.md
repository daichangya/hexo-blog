---
title: Future和CompletableFuture解析与使用
id: 1514
date: 2024-10-31 22:01:59
author: daichangya
permalink: /archives/Future-he-CompletableFuture-jie-xi-yu/
categories:
- java
---



# 一、Future模式

Java 1.5开始，提供了Callable和Future，通过它们可以在任务执行完毕之后得到任务执行结果。

Future接口可以构建异步应用，是多线程开发中常见的设计模式。

当我们需要调用一个函数方法时。如果这个函数执行很慢,那么我们就要进行等待。但有时候,我们可能并不急着要结果。

因此,我们可以让被调用者立即返回,让他在后台慢慢处理这个请求。对于调用者来说,则可以先处理一些其他任务,在真正需要数据的场合再去尝试获取需要的数据。

  
![](https://images2018.cnblogs.com/blog/1075644/201808/1075644-20180812105351567-1063438885.png)

## 1、Callable与Runnable

java.lang.Runnable是一个接口，在它里面只声明了一个run()方法，run返回值是void，任务执行完毕后无法返回任何结果

```
public interface Runnable {
    public abstract void run();
}
```

Callable位于java.util.concurrent包下，它也是一个接口，在它里面也只声明了一个方法叫做call()，这是一个泛型接口，call()函数返回的类型就是传递进来的V类型

```
public interface Callable<V> {
    V call() throws Exception;
}
```

## 2、Future + Callable

Future就是对于具体的Runnable或者Callable任务的执行结果进行取消、查询是否完成、获取结果。必要时可以通过get方法获取执行结果，该方法会阻塞直到任务返回结果

```
public interface Future<V> {
    boolean cancel(boolean mayInterruptIfRunning);
    boolean isCancelled();
    boolean isDone();
    V get() throws InterruptedException, ExecutionException;
    V get(long timeout, TimeUnit unit)
        throws InterruptedException, ExecutionException, TimeoutException;
}
```

怎么使用Future和Callable呢？一般情况下是配合ExecutorService来使用的，在ExecutorService接口中声明了若干个submit方法的重载版本

```
<T> Future<T> submit(Callable<T> task);
<T> Future<T> submit(Runnable task, T result);
Future<?> submit(Runnable task);
```

Future+Callable，使用示例如下（采用第一个方法）：

```

```

 结果：

```
result:297483790
```

 其它方式：

```
import java.util.Random;import java.util.concurrent.*;/** * @program: callable * @description: testfuture * @author: Mr.Wang * @create: 2018-08-12 12:11 **/public class Testfuture {    public static void main(String[] args){        //第一种方式        FutureTask<Integer> task = new FutureTask<Integer>(new Callable<Integer>() {            @Override            public Integer call() throws Exception {                return new Random().nextInt();            }        });        new Thread(task).start();        //第二种方方式//        ExecutorService executor = Executors.newSingleThreadExecutor();//        FutureTask<Integer> task = new FutureTask<Integer>(new Callable<Integer>() {//            @Override//            public Integer call() throws Exception {//                return new Random().nextInt();//            }//        });//        executor.submit(task);        try {            System.out.println("result: "+task.get());        } catch (InterruptedException e) {            e.printStackTrace();        } catch (ExecutionException e) {            e.printStackTrace();        }    }}
```

```
result:-358490809
```

## 3、Future 接口的局限性

 了解了Future的使用，这里就要谈谈Future的局限性。Future很难直接表述多个Future 结果之间的依赖性，开发中，我们经常需要达成以下目的：

*   将两个异步计算合并为一个（这两个异步计算之间相互独立，同时第二个又依赖于第一个的结果）

*   等待 Future 集合中的所有任务都完成。
*   仅等待 Future 集合中最快结束的任务完成，*并返回它的结果。*

# 二、CompletableFuture

首先，CompletableFuture类实现了CompletionStage和Future接口，因此你可以像Future那样使用它。

莫急，下面通过例子来一步一步解释CompletableFuture的使用。

## 创建CompletableFuture对象

说明：Async结尾的方法都是可以异步执行的，如果指定了线程池，会在指定的线程池中执行，如果没有指定，默认会在ForkJoinPool.commonPool()中执行。下面很多方法都是类似的，不再做特别说明。

四个静态方法用来为一段异步执行的代码创建CompletableFuture对象，方法的参数类型都是函数式接口，所以可以使用lambda表达式实现异步任务

runAsync方法：它以Runnabel函数式接口类型为参数，所以CompletableFuture的计算结果为空。

supplyAsync方法以Supplier<U>函数式接口类型为参数，CompletableFuture的计算结果类型为U。

```
public static CompletableFuture<Void> runAsync(Runnable runnable)
public static CompletableFuture<Void> runAsync(Runnable runnable, Executor executor)
public static <U> CompletableFuture<U> supplyAsync(Supplier<U> supplier)
public static <U> CompletableFuture<U> supplyAsync(Supplier<U> supplier, Executor executor)
```

## 1、变换结果

```
public <U> CompletionStage<U> thenApply(Function<? super T,? extends U> fn);
public <U> CompletionStage<U> thenApplyAsync(Function<? super T,? extends U> fn);
public <U> CompletionStage<U> thenApplyAsync(Function<? super T,? extends U> fn,Executor executor);
```

这些方法的输入是上一个阶段计算后的结果，返回值是经过转化后结果

例子：

```
import java.util.concurrent.CompletableFuture;

/**
 * @program: callable
 * @description: test
 * @author: Mr.Wang
 * @create: 2018-08-12 12:36
 **/
public class TestCompleteFuture {
    public static void main(String[] args){
        String result = CompletableFuture.supplyAsync(()->{return "Hello ";}).thenApplyAsync(v -> v + "world").join();
        System.out.println(result);
    }
}
```

结果：

```
Hello world
```

## 2、消费结果

```
public CompletionStage<Void> thenAccept(Consumer<? super T> action);
public CompletionStage<Void> thenAcceptAsync(Consumer<? super T> action);
public CompletionStage<Void> thenAcceptAsync(Consumer<? super T> action,Executor executor);
```

这些方法只是针对结果进行消费，入参是Consumer，没有返回值

例子：

```
import java.util.concurrent.CompletableFuture;

/**
 * @program: callable
 * @description: test
 * @author: Mr.Wang
 * @create: 2018-08-12 12:36
 **/
public class TestCompleteFuture {
    public static void main(String[] args){
        CompletableFuture.supplyAsync(()->{return "Hello ";}).thenAccept(v -> { System.out.println("consumer: " + v);});
    }
}
```

结果：

```
consumer: Hello 
```

## 3、结合两个CompletionStage的结果，进行转化后返回

```
public <U,V> CompletionStage<V> thenCombine(CompletionStage<? extends U> other,BiFunction<? super T,? super U,? extends V> fn);
public <U,V> CompletionStage<V> thenCombineAsync(CompletionStage<? extends U> other,BiFunction<? super T,? super U,? extends V> fn);
public <U,V> CompletionStage<V> thenCombineAsync(CompletionStage<? extends U> other,BiFunction<? super T,? super U,? extends V> fn,Executor executor);
```

需要上一阶段的返回值，并且other代表的CompletionStage也要返回值之后，把这两个返回值，进行转换后返回指定类型的值。

说明：同样，也存在对两个CompletionStage结果进行消耗的一组方法，例如thenAcceptBoth，这里不再进行示例。

例子：

```
import java.util.concurrent.CompletableFuture;


/**
 * @program: callable
 * @description: test
 * @author: Mr.Wang
 * @create: 2018-08-12 12:36
 **/
public class TestCompleteFuture {
    public static void main(String[] args){

        String result = CompletableFuture.supplyAsync(()->{
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            return "Hello";
        }).thenCombine(CompletableFuture.supplyAsync(()->{
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            return "world";
        }),(s1,s2)->{return s1 + " " + s2;}).join();
        System.out.println(result);
    }
}
```

结果：

```
Hello world
```

## 4、两个CompletionStage，谁计算的快，就用那个CompletionStage的结果进行下一步的处理

```
public <U> CompletionStage<U> applyToEither(CompletionStage<? extends T> other,Function<? super T, U> fn);
public <U> CompletionStage<U> applyToEitherAsync(CompletionStage<? extends T> other,Function<? super T, U> fn);
public <U> CompletionStage<U> applyToEitherAsync(CompletionStage<? extends T> other,Function<? super T, U> fn,Executor executor);
```

两种渠道完成同一个事情，就可以调用这个方法，找一个最快的结果进行处理，最终有返回值。

例子：

```
import java.util.concurrent.CompletableFuture;


/**
 * @program: callable
 * @description: test
 * @author: Mr.Wang
 * @create: 2018-08-12 12:36
 **/
public class TestCompleteFuture {
    public static void main(String[] args){

       String result = CompletableFuture.supplyAsync(()->{
           try {
               Thread.sleep(100);
           } catch (InterruptedException e) {
               e.printStackTrace();
           }
           return "Hi Boy";
       }).applyToEither(CompletableFuture.supplyAsync(()->{
           try {
               Thread.sleep(300);
           } catch (InterruptedException e) {
               e.printStackTrace();
           }
           return "Hi Girl";
       }),(s)->{return s;}).join();
       System.out.println(result);
    }
}
```

结果：

```
Hi Boy
```

## 5、运行时出现了异常，可以通过exceptionally进行补偿

```
public CompletionStage<T> exceptionally(Function<Throwable, ? extends T> fn);
```

例子：

```
import java.util.concurrent.CompletableFuture;


/**
 * @program: callable
 * @description: test
 * @author: Mr.Wang
 * @create: 2018-08-12 12:36
 **/
public class TestCompleteFuture {
    public static void main(String[] args){

       String result = CompletableFuture.supplyAsync(()->{
           try {
               Thread.sleep(100);
           } catch (InterruptedException e) {
               e.printStackTrace();
           }
           if(true) {
               throw new RuntimeException("exception test!");
           }

           return "Hi Boy";
       }).exceptionally(e->{
           System.out.println(e.getMessage());
           return "Hello world!";
       }).join();
       System.out.println(result);
    }
}
```

结果：

java.lang.RuntimeException: exception test!  
Hello world!

# 三、结束

OK，了解了以上使用，基本上就对CompletableFuture比较清楚了。

后面会找个时间说说CompletableFuture实现原理
