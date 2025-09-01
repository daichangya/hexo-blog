---
title: Java Callable Future Example
id: 1265
date: 2024-10-31 22:01:50
author: daichangya
excerpt: "Java执行程序框架的好处之一是我们可以运行并发任务，这些并发任务在处理任务后可以返回单个结果。在Java并发API实现了这一具有以下两个接口Callable和Future。1.JavaCallable和Future接口1.1.CallableCallable接口有call()方法。在这种方法中，我"
permalink: /archives/javacallablefutureexample/
categories:
 - java并发教程
---

Java执行程序框架的好处之一是我们可以运行并发任务，这些并发任务在处理任务后可以返回单个结果。在Java并发 API实现了这一具有以下两个接口Callable和Future。

## 1. Java Callable和Future接口
#### 1.1.Callable
Callable接口有call()方法。在这种方法中，我们必须实现任务的逻辑。该Callable接口是一个参数化接口，这意味着我们必须指示该call()方法将返回的数据类型。

#### 2.2.Future
Future接口具有获取Callable对象生成的结果并管理其状态的方法。

## 2. Java Callable Future示例
在此示例中，我们正在创建FactorialCalculator类型为的Callable。这意味着我们将覆盖它的call()方法，并且在计算之后，我们将从call()方法返回结果。以后可以从Future主程序保存的引用中检索此结果。
```
FactorialCalculator.java
public class FactorialCalculator implements Callable<Integer>
{
 
    private Integer number;
 
    public FactorialCalculator(Integer number) {
        this.number = number;
    }
 
    @Override
    public Integer call() throws Exception {
        int result = 1;
        if ((number == 0) || (number == 1)) {
            result = 1;
        } else {
            for (int i = 2; i <= number; i++) {
                result *= i;
                TimeUnit.MILLISECONDS.sleep(20);
            }
        }
        System.out.println("Result for number - " + number + " -> " + result);
        return result;
    }
}
```
现在，让我们使用两个线程和4个数字测试上面的阶乘计算器。
```
CallableExample.java
package com.howtodoinjava.demo.multithreading;
 
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
 
public class CallableExample 
{
      public static void main(String[] args) 
      {
          ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(2);
           
          List<Future<Integer>> resultList = new ArrayList<>();
           
          Random random = new Random();
           
          for (int i=0; i<4; i++)
          {
              Integer number = random.nextInt(10);
              FactorialCalculator calculator  = new FactorialCalculator(number);
              Future<Integer> result = executor.submit(calculator);
              resultList.add(result);
          }
           
          for(Future<Integer> future : resultList)
          {
                try
                {
                    System.out.println("Future result is - " + " - " + future.get() + "; And Task done is " + future.isDone());
                } 
                catch (InterruptedException | ExecutionException e) 
                {
                    e.printStackTrace();
                }
            }
            //shut down the executor service now
            executor.shutdown();
      }
}
```
程序输出。

```
Result for number - 4 -> 24
Result for number - 6 -> 720
Future result is -  - 720; And Task done is true
Future result is -  - 24; And Task done is true
Result for number - 2 -> 2
Result for number - 6 -> 720
Future result is -  - 720; And Task done is true
Future result is -  - 2; And Task done is true
```
在这里，我们Callable使用该submit()方法发送了要在执行程序中执行的对象。此方法接收一个Callable对象作为参数，并返回一个Future可以用于两个主要目标的对象–

- 我们可以控制任务的状态 –我们可以取消任务并检查任务是否完成。为此，我们使用了该isDone()方法来检查任务是否完成。
- 我们可以通过call（）方法获得返回的结果。为此，我们使用了该get()方法。该方法一直等到Callable对象完成该call()方法的执行并返回其结果。
如果线程在get()方法等待结果时被中断，则它将引发InterruptedException异常。如果该call()方法引发异常，则此方法引发ExecutionException异常。

该Future接口提供了另外一个版本get()，即方法得到（longtimeout，TimeUnitunit） 。如果任务的结果不可用，则此版本的get方法将在指定的时间内等待它。如果经过指定的时间段并且结果尚不可用，则该方法返回一个null值。

参考:http://images.jsdiff.com/archives/15507075