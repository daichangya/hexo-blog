---
title: Java8 Stream
id: 1444
date: 2024-10-31 22:01:56
author: daichangya
permalink: /archives/java8stream/
categories:
 - java
tags: 
 - java8
---


Java中的Stream可以定义为来自源的一系列元素,这些元素支持对它们的聚合操作。这里的源是指向流提供数据的Collection或Array。

Stream保持数据在源中的顺序。该聚合操作或批量操作是操作这让我们很容易和清楚地表达对流元素共同操作。

在继续之前,了解Java 8 Streams的设计方式使得大多数流操作仅返回流是很重要的。这有助于我们创建流操作链。这称为管道内衬。在这篇文章中,我将多次使用该术语,因此请牢记。

## 1. Java流与集合

我们所有人都已经在youtube或其他此类网站上观看了在线视频。当您开始观看视频时,文件的一小部分首先会加载到计算机中并开始播放。开始播放之前,无需下载完整的视频。这称为流式传输。我将尝试将此概念与集合相关联,并通过Streams进行区分。

在基本级别上,集合和流之间的差异与计算事物时有关。甲Collection是一个存储器内数据结构,它包含所有的数据结构目前有-每在Collection元件具有被计算之前它可以被添加到集合中的值。甲流是概念性地固定数据结构,其中的元件上计算需求。这带来了显着的编程优势。这样的想法是,用户将仅从Stream中提取他们需要的值,并且这些元素仅在需要时对用户无形地生成。这是生产者-消费者关系的一种形式。

在java中,java.util.Stream表示可以在其上执行一个或多个操作的流。流操作是中间操作或终端操作。虽然终端操作返回一个特定类型的结果,中间操作返回流本身,从而可以在一排链中的多个方法调用。流是在源上创建的,例如列表或集合(不支持映射)之类的java.util.Collection。流操作可以顺序执行,也可以并行执行。

基于以上几点,如果我们列出Stream的各种特征,它们将如下所示:

- 不是数据结构
- 专为lambdas设计
- 不支持索引访问
- 可以轻松输出为数组或列表
- 支持延迟访问
- 可并行化

## 2.创建流的不同方法

以下是从集合构建流的最流行的不同方法。

### 2.1. Stream.of(val1, val2, val3….)
    public class StreamBuilders {
        public static void main(String[] args) {
            Stream<Integer> stream = Stream.of(1, 2, 3, 4, 5, 6, 7, 8, 9);
            stream.forEach(p -> System.out.println(p));
        }
    }
### 2.2. Stream.of(arrayOfElements)
    public class StreamBuilders {
        public static void main(String[] args) {
            Stream<Integer> stream = Stream.of(new Integer[]{1, 2, 3, 4, 5, 6, 7, 8, 9});
            stream.forEach(p -> System.out.println(p));
        }
    }
### 2.3. List.stream()
    public class StreamBuilders {
         public static void main(String[] args)
         {
             List<Integer> list = new ArrayList<Integer>();
     
             for(int i = 1; i< 10; i++){
                 list.add(i);
             }
     
             Stream<Integer> stream = list.stream();
             stream.forEach(p -> System.out.println(p));
         }
    }
### 2.4. Stream.generate() or Stream.iterate()
    public class StreamBuilders {
         public static void main(String[] args)
         {
             Stream<Date> stream = Stream.generate(() -> { return new Date(); });
             stream.forEach(p -> System.out.println(p));
         }
    }
### 2.5. String chars or String tokens

    public class StreamBuilders {
         public static void main(String[] args)
         {
            IntStream stream = "12345_abcdefg".chars();
            stream.forEach(p -> System.out.println(p));
             
            //OR
             
            Stream<String> stream = Stream.of("A$B$C".split("\\$"));
            stream.forEach(p -> System.out.println(p));
         }
    }

除了上面列出的方法以外,还有其他一些方法,例如使用Stream.Buider或使用中间操作。我们将不时在单独的文章中了解它们。

## 3.将流转换为集合

我应该说将流转换为其他数据结构。

请注意,这不是真正的转换。它只是将流中的元素收集到集合或数组中。
### 3.1. 将流转换为列表– – Stream.collect( Collectors.toList() )
    public class StreamBuilders {
         public static void main(String[] args){
             List<Integer> list = new ArrayList<Integer>();
             for(int i = 1; i< 10; i++){
                 list.add(i);
             }
             Stream<Integer> stream = list.stream();
             List<Integer> evenNumbersList = stream.filter(i -> i%2 == 0).collect(Collectors.toList());
             System.out.print(evenNumbersList);
         }
    }
### 3.2.将Stream转换为数组– Stream.toArray(EntryType [] :: new)
    public class StreamBuilders {
         public static void main(String[] args){
             List<Integer> list = new ArrayList<Integer>();
             for(int i = 1; i< 10; i++){
                 list.add(i);
             }
             Stream<Integer> stream = list.stream();
             Integer[] evenNumbersArr = stream.filter(i -> i%2 == 0).toArray(Integer[]::new);
             System.out.print(evenNumbersArr);
         }
    }

还有很多其他的方法还收集流进一个Set,Map或者到多个方面。只需完成收集器课程,并记住它们即可。

## 4.核心流操​​作

流抽象为您提供了一长串有用的功能。我不会覆盖所有内容,但是我打算在这里列出所有最重要的内容,您必须第一手知道。

在继续之前,让我们预先构建String的集合。我们将在此列表上构建示例,以便易于联系和理解。

    List<String> memberNames = new ArrayList<>();
    memberNames.add("Amitabh");
    memberNames.add("Shekhar");
    memberNames.add("Aman");
    memberNames.add("Rahul");
    memberNames.add("Shahrukh");
    memberNames.add("Salman");
    memberNames.add("Yana");
    memberNames.add("Lokesh");

这些核心方法分为以下两个部分:

### 4.1. Intermediate operations

中间操作返回流本身,因此您可以连续链接多个方法调用。让我们学习重要的东西。

#### 4.1.1. Stream.filter()

Filter接受谓词以过滤流中的所有元素。此操作是中间操作,它使我们可以对结果调用另一个流操作(例如forEach)。

    memberNames.stream().filter((s) -> s.startsWith("A"))
                        .forEach(System.out::println);
                                     
    Output: 
     
    Amitabh
    Aman
#### 4.1.2, Stream.map()

中间操作映射通过给定的函数将每个元素转换为另一个对象。下面的示例将每个字符串转换为大写字符串。但是您也可以使用map()将每个对象转换为另一种类型。

    memberNames.stream().filter((s) -> s.startsWith("A"))
                         .map(String::toUpperCase)
                         .forEach(System.out::println);
                                 
    Output: 
     
    AMITABH
    AMAN
####  4.1.3. Stream.sorted()

Sorted是一个中间操作,它返回流的排序视图。除非您通过自定义比较器,否则元素将以自然顺序排序。

    memberNames.stream().sorted()
                        .map(String::toUpperCase)
                        .forEach(System.out::println);
    Output:
     
    AMAN
    AMITABH
    LOKESH
    RAHUL
    SALMAN
    SHAHRUKH
    SHEKHAR
    YANA

请记住,sorted只会创建流的排序视图,而不会操纵支持的集合的顺序。的顺序memberNames保持不变。

### 4.2. Terminal operations

终端操作返回某种类型的结果,而不是流。

####  4.2.1。Stream.forEach()

此方法有助于迭代流的所有元素,并对每个元素执行一些操作。该操作作为lambda表达式参数传递。

    memberNames.forEach(System.out::println);
    
####  4.2.2。Stream.collect()

collect() 方法,用于从蒸汽中接收元素并将其存储在集合中,并在参数函数中提到。

    List<String> memNamesInUppercase = memberNames.stream().sorted()
                                .map(String::toUpperCase)
                                .collect(Collectors.toList());
             
    System.out.print(memNamesInUppercase);
     
    Output: [AMAN, AMITABH, LOKESH, RAHUL, SALMAN, SHAHRUKH, SHEKHAR, YANA]
####  4.2.3。Stream.match()

各种匹配操作可用于检查某个谓词是否与流匹配。所有这些操作都是终端操作,并返回布尔结果。

    boolean matchedResult = memberNames.stream()
                        .anyMatch((s) -> s.startsWith("A"));
     
    System.out.println(matchedResult);
     
    matchedResult = memberNames.stream()
                        .allMatch((s) -> s.startsWith("A"));
     
    System.out.println(matchedResult);
     
    matchedResult = memberNames.stream()
                        .noneMatch((s) -> s.startsWith("A"));
     
    System.out.println(matchedResult);
     
    Output: 
     
    true
    false
    false
####  4.2.4。Stream.count()

Count是一个终端操作,返回流中元素的数量作为long值。

    long totalMatched = memberNames.stream()
                        .filter((s) -> s.startsWith("A"))
                        .count();
     
    System.out.println(totalMatched);
     
    Output: 2
####  4.2.5。Stream.reduce()

此终端操作使用给定功能对流的元素进行归约。结果是一个可选保留减少的值。

    Optional<String> reduced = memberNames.stream()
                        .reduce((s1,s2) -> s1 + "#" + s2);
     
    reduced.ifPresent(System.out::println);
     
    Output: Amitabh#Shekhar#Aman#Rahul#Shahrukh#Salman#Yana#Lokesh

## 5. Stream short-circuit operations

尽管对满足谓词的集合内的所有元素执行流操作,但经常需要在迭代过程中遇到匹配元素时中断操作。在外部迭代中,将使用if-else块。在内部迭代中,可以使用某些方法来实现此目的。让我们来看两个这样的方法的示例:

### 5.1。Stream.anyMatch()

一旦作为谓词传递的条件满足,此方法将返回true。它将不再处理任何元素。

    boolean matched = memberNames.stream()
                        .anyMatch((s) -> s.startsWith("A"));
     
    System.out.println(matched);
     
    Output: true
### 5.2。Stream.findFirst()

它将从流中返回第一个元素,然后将不再处理任何元素。

    String firstMatchedName = memberNames.stream()
                    .filter((s) -> s.startsWith("L"))
                    .findFirst().get();
     
    System.out.println(firstMatchedName);
     
    Output: Lokesh

## 6. Java Steam中的并行性

借助Java SE 7中添加的Fork / Join框架,我们有了有效的机制来在我们的应用程序中实现并行操作。但是,实现此框架本身是一项复杂的任务,如果没有正确执行,那么这是一项艰巨的任务。它是可能导致应用程序崩溃的复杂多线程错误的来源。通过引入内部迭代,我们可以并行进行操作。

要启用并行性,您要做的就是创建并行流,而不是顺序流。令您惊讶的是,这确实非常容易。在上面列出的任何流示例中,只要您想在并行内核中使用多个线程来完成特定作业,您都必须调用方法parallelStream()方法而不是stream()方法。

    public class StreamBuilders {
         public static void main(String[] args){
            List<Integer> list = new ArrayList<Integer>();
             for(int i = 1; i< 10; i++){
                 list.add(i);
             }
             //Here creating a parallel stream
             Stream<Integer> stream = list.parallelStream();  
             Integer[] evenNumbersArr = stream.filter(i -> i%2 == 0).toArray(Integer[]::new);
             System.out.print(evenNumbersArr);
         }
    }

这项工作的主要推动力是使并行性更易于开发人员使用。尽管Java平台已经为并发和并行性提供了强大的支持,但是开发人员在根据需要将其代码从顺序迁移到并行时会遇到不必要的障碍。因此,重要的是要鼓励顺序友好和并行友好的习语。通过将重点转移到描述应该执行什么计算而不是应该如何执行计算上,可以方便地进行操作。

同样重要的是要在使并行性变得更容易而又不至于使其变得不可见之间取得平衡。使并行性透明将引入不确定性,并可能在用户可能不期望的情况下进行数据竞争。

关于Java 8中引入的Stream抽象的基础,这就是我要分享的全部内容。我将在以后的文章中讨论与Streams相关的其他各种事情。
