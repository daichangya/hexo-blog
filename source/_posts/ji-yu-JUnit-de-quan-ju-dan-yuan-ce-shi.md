---
title: 基于 JUnit 的全局单元测试程序
id: 1030
date: 2024-10-31 22:01:48
author: daichangya
excerpt: 简介： 在 Java 程序中，JUnit 是备受开发人员喜爱的单元测试工具。通常，程序员会对每个程序的每个模块写单元测试。对于小型程序来说，程序员只需要手工执行这些单元测试程序就可以，工作量并不大，但是对于中大型程序来说，可能拥有非常多的程序模块，而每个程序模块内又含有众多
permalink: /archives/ji-yu-JUnit-de-quan-ju-dan-yuan-ce-shi/
tags:
- junit
---

背景介绍
----

最近参与了一个新产品的研发工作。新产品是采用模块式开发方式，拥有众多的功能模块，每一个模块是一个独立的 Java 工程。在产品中，为了保证各个模块的功能，目前其都有相应的 JUnit 测试程序。随着产品功能的逐渐完善，我们发现，程序中光是 JUnit Test 测试文件，全部加起来已经有几百个。由于这些文件分布在几十个不同的工程不同的子目录结构中，目前并没有很好的工具可以将所有的单元测试一次运行。而手工的运行这些单元测试是非常繁琐的，对程序员来说是浪费时间的；又或者可以用脚本完成运行所有测试文件的目的，但是由于我们采取的是敏捷开发的模式，JUnit Test 测试集合会不断的持续增长，每增加一个 JUnit Test 文件，就需要立即修改脚本；一旦忘记修改，这个新加的测试文件可能就无法被执行可见，用脚本来执行测试文件也并不是很好的手段，依然给我们的开发带来额外工作。这里我们有了一个想法，做一个全局的单元测试程序，去自动的检索工程集中所有的 JUnit Test 测试程序。这个全局单元测试程序将基于 JUnit4 去运行。

核心机制：JUnit4 支持一次运行多个测试程序
------------------------

首先我们要了解 JUnit4 支持多个 Class 集合作为输入，并且调用 org.junit.runner.Runner.run() 方法运行输入的测试类集合。JUnit4 中已经定义了一些默认的 Runner，可以分别处理不同的输入类集合：比如 BlockJUnit4ClassRunner，就是默认处理带有 @Test 的 JUnit4 测试类的运行器；Suite，可以处理兼容 JUnit3 的测试类的运行器，等等。

我们可以来看下面的 Runner 结构图：

##### 图 1. JUnit Runner 结构图

![JUnit Runner 结构图](https://www.ibm.com/developerworks/cn/java/j-lo-junitglobletest/fig1.jpg)


Runner 类定义了运行测试用例的接口，Suite 类继承自 Runner 类，Suite 类支持 JUnit3 风格的测试类，可以用来执行多个测试用例。因此我们的想法是，自定义一个继承自 Suite 类的 Runner，就是上图中得 AllClassRunner 类。这个 Runner 的输入将是工程集中所有找到的 JUnit Test Class 集合，这样就可以一次运行工程中不同工程不同目录下的所有 JUnit Test 文件了。下面是我们的 AllClassRunner 类的代码：

##### 清单 1. AllClassRunner 类的代码

```
public class AllJunitTestRunner extends Suite {    
  public AllJunitTestRunner(Class<?> clazz, RunnerBuilder builder) throws 
      InitializationError { 
      // 调用父类 Suite 方法直接运行所有符合要求的 JUnit Test 对象
      super(builder, clazz, loadAllTestClass(filterClassNameList 
      (clazz, loadAllClassesName(clazz)))); 
   } 
}
```

loadAllClassesName 方法将会找到工程集中所有的 Class 文件名的集合，filterClassNameList 将会对找到的 Class 文件集合进行过滤，过滤条件是针对文件名称。loadAllTestClass 则会找到所有符合条件的 JUnitTest Class 集合。

如何找到所有的需要的 JUnit Test 测试类集合
---------------------------

我们来看下面的流程图：

##### 图 2. 找到需要的 JUnit Test Class 对象集合的流程图

![找到需要的 JUnit Test Class 对象集合的流程图](https://www.ibm.com/developerworks/cn/java/j-lo-junitglobletest/fig2.jpg)


流程图要素介绍：

*   找到工程集内所有的 .class 文件名
*   对找到的文件名集合根据过滤条件进行初步过滤
*   根据 .class 文件名转换到相应的 Class 对象
*   判断是否属于 Abstract 类，如果不是的话，继续判断
*   判断是否属于 Inner 类，如果不是的话，继续判断
*   判断是否属于 JUnit3 或者 JUnit4 风格的类，如果是的话，加入结果集

经过上述步骤，将找到所有需要的 JUnit Test class 集合。将找到的 Class 集合放入到自定义 Runner 中，可以达到一次运行工程集内所有测试程序的目的。

### 如何找出所有的 Class 文件名集合

首先根据默认的 Java classpath 属性，找到当前运行的 JUnit Test 文件所在工程集中所有的文件及文件夹：

##### 清单 2. 找到工程集中所有 Jar 及 .Class 所在目录集合

```
public static String getClasspath() { 
   return System.getProperty(CONSTANT.DEFAULT_CLASSPATH_PROPERTY); 
}
```
这里得到的将是一个路径集合的 String 对象，包括文件目录及 .jar 文件（jar 文件内也包含 Class 文件名）。我们需要做的，是找到文件目录下的 Class 文件，因此通过 split 这个路径集合，剔除里面的 .jar 文件，我们将得到一个包含工程集中所有 Class 文件的目录集合。

因为 Class 文件可能会嵌套的包含在我们找到的目录集合中，所以我们需要递归的去找到所有的 Class 文件，并将 Class 文件的 Class 名放到一个集合中，示例代码如下：

##### 清单 3. 递归找到工程集中所有的 Class 对象集合

```
for (String path : Util.splitClassPath(Util.getClasspath())) { 
   // 此处不处理 Jar 包文件，感兴趣的读者可以考虑自己添加对 Jar 包中 JUnit Test 文件的处理
   if (!(path.toLowerCase().endsWith(CONSTANT.JAR_SUFFIX))) { 
    Util.loadAllClassNames(path, path, classesFileNameList); 
   } 
} 
 
public static void loadAllClassNames(String rootPath, String currentPath, 
   List<String> classNameList) { 
   File currentFile = new File(currentPath); 
if (currentFile.isFile()) { 
// 如果是文件的话，直接将路径名转换为文件名，并加入结果集
       if (Util.isClassFile(currentFile.getName())) { 
       classNameList.add( 
           Util.replaceFileSeparator( 
           Util.removeClassSuffix( 
           // 只获取文件的名字，并将路径中的反斜杠”/”转换为文件名中的”.”
           // 比如获取文件名为”com.aa.bb.cc”
           Util.getFileNameWithoutRootPath(currentFile, rootPath)))); 
    } 
} else { 
// 如果是文件夹的话，则取所有的子文件，递归处理所有取到的子文件
    for (File file : currentFile.listFiles()) { 
       if (file.isFile()) { 
        if (Util.isClassFile(file.getName())) {    
        classNameList.add(Util.replaceFileSeparator(Util.removeClassSuffix 
        (Util.getFileNameWithoutRootPath(file, rootPath)))); 
           } 
       } else { 
        loadAllClassNames(rootPath, file.getAbsolutePath(), classNameList); 
       } 
    } 
   } 
}
```
上面我们得到的将是所有一个 List<String> 对象，包含所有的 .class 文件。

### 如何过滤 Class 文件名

可以自定义一系列的过滤条件，比如对于 package “com.aa.bb.cc”下的所有 JUnit Test 文件都不测试，那么可以写如下的 filter：

##### 清单 4. 对 Class 名字使用过滤条件的示例代码

```
public static boolean classNameIsInArray(String className) { 
   String filters = "com.aa.bb.cc1.*;com.aa.bb.cc2.*"; 
   String[] filterList = filters.split(";"); 
 
   if (filters == null || filterList.length  < 1) { 
    return false; 
   } 
   for (String pattern : filterList) { 
    if (className.matches(pattern)) { 
        return true; 
    } 
   } 
   return false; 
}
```
### 如何过滤 Abstract 类

我们知道一个 JUnit Test 文件绝对不可能是 Abstract 类，因此可以把 Abstract 类从 Class 集合中首先过滤掉。示例代码如下：

##### 清单 5. 过滤 Abstract 类的示例代码

```
public static boolean isAbstractClass(Class<?> clazz) { 
    return (clazz.getModifiers()&Modifier.ABSTRACT) != 0; 
}
```

### 如何过滤 Inner 类

JUnit Test 类中一般来说不允许再定义一个子类，因此对于 Inner class 来说，也是我们的剔除对象。示例代码展示如何找到 Inner 类。

##### 清单 6. 过滤 Inner 类的示例代码

```
public static final String INNER_CLASS_CHAR = "$"; 
public static boolean isInnerClass(String className) { 
    return className.contains(INNER_CLASS_CHAR); 
}
```

### 如何找到 JUnit3 文件

首先我们来看一个典型的基于 JUnit3 的单元测试程序：

##### 清单 7. 典型 JUnit3 风格的测试代码

```
import junit.framework.TestCase; 
import static org.junit.Assert.*; 
public class AddOperationTest extends TestCase{ 
 
     public void setUp() throws Exception { 
     } 
 
     public void tearDown() throws Exception { 
     } 
      
     // 测试方法必须以 test 开头
     public void testAdd() { 
         int x = 0; 
         int y = 0; 
         AddOperation instance = new AddOperation(); 
         int expResult = 0; 
         int result = instance.add(x, y); 
         assertEquals(expResult, result);          
     } 
}
```

我们可以看到上面的单元测试拥有如下特征：

1.继承自 junit.framework.TestCase 类；

2.要测试的方法以 test 开头。

在这里我们只需要知道一个 .class 文件是否是 JUnit3 的测试程序，因此第二条特征暂时用不上，我们用是否继承自 TestCase 类来作为判断标准，代码如下：

##### 清单 8. 找出 JUnit3 风格的 JUnit Test 测试文件的示例代码

```
public static boolean isJUnit3TestClass(Class<?> clazz) { 
// class.isAssignableFrom() 方法可以找到即使是父类的父类的继承关系
// 因此认为如果输入的子类继承自 JUnit Test3.8 的 TestCase 类，则认为是 JUnit3 风格的 JUnit Test 类对象
   return TestCase.class.isAssignableFrom(clazz); 
}
```

如果是继承自 TestCase 这个类，则返回 true，代表是 JUnit3 的单元测试； 否则返回 false;.

### 如何找到 JUnit4 文件

对于 JUnit4，我们知道它最大的特征是引入了 Annotation 机制，简化了原来的单元测试的用法。我们可以来看下面的例子：

##### 清单 9. 典型 JUnit4 风格的测试代码
```
import junit.framework.TestCase; 
import org.junit.After; 
import org.junit.Before; 
import org.junit.Test; 
import static org.junit.Assert.*; 
 
public class AddOperationTest extends TestCase{ 
     @Before 
     public void setUp() throws Exception { 
     } 
 
     @After 
     public void tearDown() throws Exception { 
     } 
 
     @Test 
     public void add() { 
         int x = 0; 
         int y = 0; 
         AddOperation instance = new AddOperation(); 
         int expResult = 0; 
         int result = instance.add(x, y); 
         assertEquals(expResult, result);          
 
     }  
}
```

我们可以看到上面的 JUnit4 测试程序拥有如下特征：

1.继承自 junit.framework.TestCase 类；

2.拥有至少一个有 @Test 的注释的测试方法，且方法名称任意

因此对于 JUnit4 的 Class 文件来说，我们需要判断的是它的方法内是否有 @Test Annotation，如果没有的话，就不是一个有效的 JUnit4 测试文件。示例代码如下：

##### 清单 10. 找出 JUnit4 风格的 JUnit Test 测试文件的示例代码

```
public static boolean isJUnit4TestClass(Class<?> clazz) { 
try { 
for (Method method : clazz.getMethods()) { 
    // 如果在 class 对象所有的方法中发现 @Test 注释，则认为是 JUnit4 风格的 JUnit Test 对象
    if (method.getAnnotation(Test.class) != null) { 
       return true; 
    } 
   } 
} catch (NoClassDefFoundError ignore) { 
   return false; 
} 
return false; 
}
```

### 使用各种过滤条件

前面我们已经得到了一个在本工程集内的所有 Class 文件的集合，现在我们可以使用各种过滤条件对集合进行过滤，示例代码如下：

##### 清单 11. 联合使用各种过滤条件找出需要的 JUnit Test 的示例代码

```
for (String className : classesFileNameList) { 
   Class<?> classFromName = null; 
try { 
    // 从 class 名字转换为 class 对象              
    classFromName = Class.forName(className); 
   } catch (ClassNotFoundException e) { 
    // 如果转换失败，则跳过
        continue; 
} 
// JUnit Test class 对象不可能是内部 class，所以跳过检测所有的内部 class 
   if (!Util.isInnerClass(className)) { 
    Class<?> classFromName = Class.forName(className); 
    if (classFromName.isLocalClass()|| 
           classFromName.isAnonymousClass()) { 
           // JUnit Test class 对象也不可能是 local 或者 Anonymous 对象，跳过
           continue; 
    } 
    if (!Util.isAbstractClass(classFromName) && 
      (Util.isJUnit4TestClass(classFromName)|| Util.isJUnit38TestClass(classFromName))) 
      {                             
       toBeRanTestClassList.add(classFromName); 
      } 
   }           
}
```
这里我们找到的 toBeRanTestClassList 集合就是我们期望测试的 JUnit Test Class 对象集合。

JUnit 自动执行所有测试
--------------

现在我们已经有了自己的 AllJUnitTestRunner，也找到了工程集内所有的 JUnit Test Class 集合。下面要做的就是如何运行找到的 Class 集合。具体代码如下：

##### 清单 12. 我们的期望值 - 最终的 JUnit Test 示例代码

```
import org.junit.runner.RunWith; 
import junit.AllJunitTestRunner; 
@RunWith(AllJunitTestRunner.class) 
public class AllJunitTest { 
 
}
```

只需要一个空的 JUnitTest 测试文件，并将 AllJUnitTestRunner 作为这个测试文件的 Runner。那么在运行这个测试程序时，它将调用我们定义的 Runner 去自动运行所有我们期望的 JUnit Test 测试程序。是不是很方便呢？可以说基本达到了我们预期的目的。

改进点
---

*   我们知道在 JUnit4 中支持自定义的 Annotation，因此对于我们的各种过滤项，应该可以通过定义新的 Annotation 方式从而在最终的 JUnit Test 程序中任意定义，这样比硬编码在全局单元测试程序模块内更加方便使用。
*   递归查找整个工程集内所有的 class 文件名会对查找速度产生影响。本人觉得在递归的同时应该可以再次对路径名等进行过滤，避免在不必要的目录内不停的查找，以提高性能。

以上是本人目前想到的 2 个改进点，希望大家踊跃讨论，提高程序的性能及易用性。

总结
--

本文主要利用了 Class 文件的各种特征及 JUnit3、JUnit4 的特征，及 JUnit4 中可以一次执行多个 JUnit Test 文件的特性，达到一次执行全部工程集内的所有测试文件的目的。目前，在实际项目执行中起到了非常大的作用。对于所有新增的功能点，新增的测试文件，在正式上传到服务器之前都只需要执行一个 JUnit Test 文件，就可以发现是否影响原有功能，增加了程序开发过程的自动性，节约了大量程序开发纠错的时间，提高了产品的质量。

* * *

#### 相关主题

*   [单元测试利器 JUnit 4](http://www.ibm.com/developerworks/cn/java/j-lo-junit4/index.html)（developerWorks，2007 年 2 月）：本文主要介绍了如何使用 JUnit4 提供的各种功能开展有效的单元测试，并通过一个实例演示了如何使用 Ant 执行自动化的单元测试。
*   [扩展 JUnit4 以促进测试驱动开发](http://www.ibm.com/developerworks/cn/java/j-lo-junit4tdd/index.html)（developerWorks，2010 年 7 月）：介绍了如何充分利用 JUnit 4 更加高效的灵活的组织和运行测试用例的解决方案，促进测试驱动开发实践更有效地进行。
*   [developerWorks Java 技术专区：](http://www.ibm.com/developerworks/cn/java/)数百篇关于 Java 编程各个方面的文章。