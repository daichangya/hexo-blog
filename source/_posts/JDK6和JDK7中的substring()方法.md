---
title: JDK6和JDK7中的substring()方法
id: 635
date: 2024-10-31 22:01:45
author: daichangya
excerpt: "substring(int beginIndex, int endIndex)在JDK6与JDK7中的实现方式不一样，理解他们的差异有助于更好的使用它们。为了简单起见，下面所说的substring()指的就是substring(int beginIndex, int end"
permalink: /archives/19079409/
categories:
 - java
---


在JDK6与JDK7这两个版本中,substring(int beginIndex, int endIndex)方法是不同的. 了解两个版本间的区别可以让你更好地使用它们. 为简单起见,本文中以 substring() 表示 substring(int beginIndex, int endIndex).  
  
**1\. substring()功能简介**  
String对象的substring(int beginIndex, int endIndex)方法返回此对象的一个子串,从beginIndex 开始，一直到 endIndex-1 结束,共 (endIndex - beginIndex)个字符。  
新手提示:   
    1.1 String 的索引和数组一样，都是从0开始.  
    1.2 注意，方法名字是substring(),全小写.  
    1.3 有个重载方法是substring(int beginIndex),从beginIndex索引处开始,取得子字符串.  

	String x = "abcdef";
	int begin=1;
	int end=3;
	x = x.substring(begin, end);
	System.out.println(x);

  
执行结果(包含索引为 begin,直到 end-1 的字符):

bc

  
**2\. 当substring()被调用时,发生了什么?**  
你应该知道,因为 x 是不可变的,当 指定 x 等于 x.substring(begin, end)时,实际上 x 指向了一个全新的字符串,如下图所示:  
![](http://img.blog.csdn.net/20131102185832421?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvcmVuZnVmZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)  

图1

  
  
然而，这幅图并不是完全正确的,堆内存中所真正发生的事也不是这么简单.那么,在JDK6和JDK7之间 substring()的调用到底有些什么区别呢?  
  
**3\. JDK 6中的substring()方法**  
String实际上是一个字符数组.在 JDK6中, String对象主要包含3个属性域:   

	private final char value[];
	private final int offset;
	private final int count;

  
他们用于存储实际的字符数组,数组的第一个索引,以及String的字符个数.  
当调用 substring() 方法时,创建了一个新的String对象,但是string的value[] 属性域仍然指向堆内存中的原来的那个数组。区别就是 两个对象的 count 和 offset 这两个值不同了。 如下图所示:  
![](http://img.blog.csdn.net/20131102185939437?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvcmVuZnVmZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)  

图2

要解释这个问题,下面是最关键部分的代码:  

	// JDK6,包级私有构造,共享 value数组提升速度
	String(int offset, int count, char value[]) {
		this.value = value;
		this.offset = offset;
		this.count = count;
	}


	public String substring(int beginIndex, int endIndex) {
		// ... 检查边界的代码
		// 如果范围和自己一模一样,则返回自身,否则用value字符数组构造一个新的对象
		return ((beginIndex == 0) && (endIndex == count)) ? this :
			new String(offset + beginIndex, endIndex - beginIndex, value);
	}

  
**4\. JDK 6中substring()引起的问题**  
如果有一个"**非常**"长的字符串,但每次使用substring()时只想要很小的一部分,那么将会引起另一个性能问题: 虽然你只需要很小的一部分,但是持有了整个value[]的引用,从而导致大量内存被占用。  
要解决这个问题，在JDK6中可以让其指向一个真正的子字符串,示例代码:  

	x = x.substring(begin, end) + "";

  
**5\. JDK 7中的substring()方法**  
在JDK 7 中这个问题得到改进, substring()方法真实地在堆内存中创建了另一个字符数组.  
![](http://img.blog.csdn.net/20131102190138875?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvcmVuZnVmZWk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)  

图3

  

	// JDK 7, 权限变为 public 
	public String(char value[], int offset, int count) {
		// ... 检查边界..
		// value 数组拷贝
		this.value = Arrays.copyOfRange(value, offset, offset+count);
	}


	public String substring(int beginIndex, int endIndex) {
		// ... 检查边界..
		int subLen = endIndex - beginIndex;
		// 如果和自身一样,那就返回自身,否则返回构造的新对象
		return ((beginIndex == 0) && (endIndex == value.length)) ? this
					: new String(value, beginIndex, subLen);
	}

  
**参考:**  

1\. [Changes to substring](http://www.javaadvent.com/2012/12/changes-to-stringsubstring-in-java-7.html) 

2\. [Java 6 vs Java 7 when implementation matters](http://nextmovesoftware.com/blog/2013/07/05/java-6-vs-java-7-when-implementation-matters/)  
  
**相关阅读:**  

1\. [Top 10 questions about Java String.](http://www.programcreek.com/2013/09/top-10-faqs-of-java-strings/)

2\. [Java method for spliting a camelcase string](http://www.programcreek.com/2011/03/java-method-for-spliting-a-camelcase-string/)

3\. [Java: Convert File to Char Array](http://www.programcreek.com/2012/12/java-convert-file-to-char-array/)

4\. [Count Number of Statements in a Java Method By Using Eclipse JDT ASTParser](http://www.programcreek.com/2011/07/java-count-number-of-statements-in-a-method/)

原文链接: [The substring() Method in JDK 6 and JDK 7 ](http://www.programcreek.com/2013/09/the-substring-method-in-jdk-6-and-jdk-7/)  
   
  