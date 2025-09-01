---
title: 什么是MVEL?
id: 1581
date: 2024-10-31 22:02:02
author: daichangya
permalink: /archives/%E4%BB%80%E4%B9%88%E6%98%AFmvel/
tags: 
 - 表达式
---


### 1.MVEL是啥？它能做啥？

简单来说是一种强大的表达式解析器。我们可以自己写一些表达式，交给mvel进行解析计算，得到这个表达式计算的值。玩概念，我不懂，😢

还是举个例子靠谱。👍  
比如我们要进行一个加法运算。在java中我们这样写：

```
int res = 1+1;  // 2

```

若我用mvel则这样写：

```
Object res = MVEL.eval("1+1");  //2

```

是不是很吃惊😱。“1+1”就是一个表达式，第一种我们是硬编码实现的计算结果，但是第二种方案，直接给evel函数传递一个表达式字符串，直接能计算出结果。这样如果想计算1-1。直接传人不同的表达式即可。现在要计算'(2+2)*3+5/2'或'2>1?1+1:2+2'。来吧你硬编码试试这些计算？是不是又要多写几行代码，而且不便扩展。

你以为mvel只能做这些了？那就真的是太年轻了。目前mvel支持大量的语法，条件，循环等。还可以支持自定义函数，这就🐂了。那么我们工作中用这东西来干嘛？

### 2.在自定义数据流转中的使用

#### ① 啥是数据流转

数据流转就是不同对象间数据的转换。比如a对象数据通过某些规则转化为b对象数据。ca，这说的是不是数据清洗？？？。对，说的没错，但是数据清洗只是其中的一个具体项罢了。👍，来个图：  
![](https://oscimg.oschina.net/oscnet/391bba8cf95500a2b9d89a94d09888dcace.jpg)

由图可以看出两个对象name和age都是一对一映射，但是目标对象不需要sex字段，但是多了一个出生年的字段，而且是通过年龄计算而来。下面我们就以代码来模拟一下这个转换过程,在这里我对象都用map来定义。

```
HashMap<Object, Object> srcMap = Maps.newHashMap();
srcMap.put("name","zs");
srcMap.put("age",10);
srcMap.put("sex","女");
//字段映射关系
HashMap<String, String> mapping = Maps.newHashMap();
mapping.put("name","name");
mapping.put("age","age");
//这里先把当前年份写死为2019
mapping.put("birthYear","2019-age");
//目标对象
HashMap<Object, Object> targetMap = Maps.newHashMap();
//k为目标表字段，v为转换规则
mapping.forEach((k,v)->{
    Object reValue = MVEL.eval(v,srcMap);
    targetMap.put(k,reValue);
});
System.out.println("源对象"+srcMap);    //源对象{sex=女, name=zs, age=10}
System.out.println("目标对象"+targetMap);   //目标对象{birthYear=2009, name=zs, age=10}

```

对就这么简单，但是我们这里计算出生年份中的当前年份写死了啊。明细不不是我们想要的，没事我们慢慢来。

.自定义函数

定义获取当前年份函数

```
/**
 * 获取当前年份方法
 * @return
 */
public static Object getCurrentYear(){
    Calendar date = Calendar.getInstance();
    String year = String.valueOf(date.get(Calendar.YEAR));
    return year;
}

```

.将自定义函数注册

直接上代码

```
static ParserContext context = new ParserContext();
static {
    //MvelTest是getCurrentYear函数的类
    Method[] declaredMethods = MvelTest.class.getDeclaredMethods();
    for(Method method : declaredMethods){
        context.addImport(method.getName(),method);
    }
}

```

.使用

直接将Object reValue = MVEL.eval(v,srcMap);替换为

```
Object reValue = MVEL.executeExpression(MVEL.compileExpression(v, context),srcMap);

```

即可。compileExpression的作用就是将我们的规则进行编译成mvel可以识别的一个过程

birthYear规则替换为mapping.put("birthYear","getCurrentYear()-age");执行得到相同的结果。

有了这些我们可以自定义更多的转换规则，还可以借此开发一套用户配置工具，根据用户自己的配置，进行相应的资源映射。得到想要的目标数据。

### 3.小结

这里只是在工作中用到mvel的一个小小的尝试。更多的研究后续进行。