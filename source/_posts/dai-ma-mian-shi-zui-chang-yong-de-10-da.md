---
title: 代码面试最常用的10大算法
id: 111
date: 2024-10-31 22:01:40
author: daichangya
excerpt: '摘要：面试也是一门学问，在面试之前做好充分的准备则是成功的必须条件，而程序员在代码面试时，常会遇到编写算法的相关问题，比如排序、二叉树遍历等等。

  在程序员的职业生涯中，算法亦算是一门基础课程，尤其是在面试的时候，很多公司都会让程序员编写一些算法实例，例如快速排序、二叉树查找等等。

  本文总结了程序员在代码面试中最常遇到的10大算法类型，想要真正了解这些算法的原理，还需程序员们花些功夫。'
permalink: /archives/dai-ma-mian-shi-zui-chang-yong-de-10-da/
categories:
- 面试
tags:
- 算法
---

## 摘要：
面试也是一门学问，在面试之前做好充分的准备则是成功的必须条件，而程序员在代码面试时，常会遇到编写算法的相关问题，比如排序、二叉树遍历等等。

在程序员的职业生涯中，算法亦算是一门基础课程，尤其是在面试的时候，很多公司都会让程序员编写一些算法实例，例如快速排序、二叉树查找等等。

这篇文章总结了编码采访中的常见主题，包括_1）字符串/数组/矩阵，2）链表，3）树，4）堆，5）图，6）排序，7）动态编程，8）位操作， 9）组合和排列，以及10）数学。_将问题归为一类总是不容易的，因为问题可能属于多个类别。

更新列表可[在此处获得](https://www.programcreek.com/2013/08/leetcode-problem-classification/)。您可以下载[PDF版本](https://www.programcreek.com/wp-content/uploads/2012/11/coding-interview-in-java.pdf)

**1.字符串/数组**

算法问题的输入通常是字符串或数组。在没有自动完成任何IDE的情况下，应记住以下方法。

```
toCharArray() //get char array of a String
charAt(int x) //get a char at the specific index
length() //string length
length //array size 
substring(int beginIndex) 
substring(int beginIndex, int endIndex)
Integer.valueOf()//string to integer
String.valueOf()/integer to string
Arrays.sort()  //sort an array
Arrays.toString(char[] a) //convert to string
Arrays.copyOf(T[] original, int newLength)
System.arraycopy(Object src, int srcPos, Object dest, int destPos, int length)
```

经典问题：  
[1）旋转数组](https://www.programcreek.com/2015/03/rotate-array-in-java/ "用Java旋转数组")，[字符串中的反向单词](https://www.programcreek.com/2014/05/leetcode-reverse-words-in-a-string-ii-java/)  
[2）评估反向波兰符号（堆栈）](https://www.programcreek.com/2012/12/leetcode-evaluate-reverse-polish-notation/)  
[3）同构字符串](https://www.programcreek.com/2014/05/leetcode-isomorphic-strings-java/ "LeetCode –同构字符串（Java）")  
[4）梯子（BFS）](https://www.programcreek.com/2012/12/leetcode-word-ladder/)，[字梯II（BFS）](https://www.programcreek.com/2014/06/leetcode-word-ladder-ii-java/ "LeetCode – Word Ladder II（Java）")  
[5）两个排序数组的中位数](https://www.programcreek.com/2012/12/leetcode-median-of-two-sorted-arrays-java/)  
[5）Kth数组中的最大元素](https://www.programcreek.com/2014/05/leetcode-kth-largest-element-in-an-array-java/ "LeetCode –数组中第K个最大的元素（Java）")  
[6）通配符匹配](https://www.programcreek.com/2014/06/leetcode-wildcard-matching-java/)，[正则表达式匹配](https://www.programcreek.com/2012/12/leetcode-regular-expression-matching-in-java/)  
[7）合并间隔](https://www.programcreek.com/2012/12/leetcode-merge-intervals/)，[插入间隔](https://www.programcreek.com/2012/12/leetcode-insert-interval/)  
[9）两个总和](https://www.programcreek.com/2012/12/leetcode-solution-of-two-sum-in-java/)，[两个总和II](https://www.programcreek.com/2014/03/two-sum-ii-input-array-is-sorted-java/)，[两个总和III](https://www.programcreek.com/2014/03/two-sum-iii-data-structure-design-java/)，[3Sum](https://www.programcreek.com/2012/12/leetcode-3sum/)，[4Sum](https://www.programcreek.com/2013/02/leetcode-4sum-java/)  
[10）3Sum最接近](https://www.programcreek.com/2013/02/leetcode-3sum-closest-java/)  
[11）字符串到整数](https://www.programcreek.com/2012/12/leetcode-string-to-integer-atoi/)  
[12）合并排序的数组](https://www.programcreek.com/2012/12/leetcode-merge-sorted-array-java/)  
[13）有效括号](https://www.programcreek.com/2012/12/leetcode-valid-parentheses-java/)  
[13）最长有效括号](https://www.programcreek.com/2014/06/leetcode-longest-valid-parentheses-java/ "LeetCode –最长有效括号（Java）")  
[14）实现strStr（）](https://www.programcreek.com/2012/12/leetcode-implement-strstr-java/)  
[15）最小大小的子](https://www.programcreek.com/2014/05/leetcode-minimum-size-subarray-sum-java/ "LeetCode –最小大小子数组总和（Java）")[数组](https://www.programcreek.com/2012/12/leetcode-implement-strstr-java/)[总和](https://www.programcreek.com/2014/05/leetcode-minimum-size-subarray-sum-java/ "LeetCode –最小大小子数组总和（Java）")  
[16）搜索插入位置](https://www.programcreek.com/2013/01/leetcode-search-insert-position/)  
[17）最长连续序列](https://www.programcreek.com/2013/01/leetcode-longest-consecutive-sequence-java/)  
[18）有效回文](https://www.programcreek.com/2013/01/leetcode-valid-palindrome-java/)  
[19）之字形转换](https://www.programcreek.com/2014/05/leetcode-zigzag-conversion-java/ "LeetCode – ZigZag转换（Java）")  
[20）添加二进制数](https://www.programcreek.com/2014/05/leetcode-add-binary-java/ "LeetCode –添加二进制（Java）")  
[21）最后一个字的长度](https://www.programcreek.com/2014/05/leetcode-length-of-last-word-java/ "LeetCode –字长（Java）")  
[22）三角](https://www.programcreek.com/2013/01/leetcode-triangle-java/)  
24）包含重复项：[I](https://www.programcreek.com/2014/05/leetcode-contains-duplicate-java/)，[II](https://www.programcreek.com/2014/05/leetcode-contains-duplicate-ii-java/)，[III](https://www.programcreek.com/2014/06/leetcode-contains-duplicate-iii-java/)  
25）从已排序数组中删除重复项：[I](https://www.programcreek.com/2013/01/leetcode-remove-duplicates-from-sorted-array-java/)，[II](https://www.programcreek.com/2013/01/leetcode-remove-duplicates-from-sorted-array-ii-java/)，[Remove Element](https://www.programcreek.com/2014/04/leetcode-remove-element-java/)，[移动零](https://www.programcreek.com/2014/05/leetcode-move-zeroes-java/)  
[27）最长的子字符串而不重复字符](https://www.programcreek.com/2013/02/leetcode-longest-substring-without-repeating-characters-java/)  
[28）包含2个唯一字符的最长的子字符串](https://www.programcreek.com/2013/02/longest-substring-which-contains-2-unique-characters/) \[Google\]  
[28）具有所有单词串联的子串](https://www.programcreek.com/2014/06/leetcode-substring-with-concatenation-of-all-words-java/ "LeetCode –带有所有单词串联的子字符串（Java）")  
[29）最小窗口子串](https://www.programcreek.com/2014/05/leetcode-minimum-window-substring-java/ "LeetCode –最小窗口子字符串（Java）")  
31）在旋转排序数组中找到最小值：[I](https://www.programcreek.com/2014/02/leetcode-find-minimum-in-rotated-sorted-array/)，[II](https://www.programcreek.com/2014/03/leetcode-find-minimum-in-rotated-sorted-array-ii-java/)  
32）在旋转数组中搜索：[I](https://www.programcreek.com/2014/06/leetcode-search-in-rotated-sorted-array-java/)，[II](https://www.programcreek.com/2014/06/leetcode-search-in-rotated-sorted-array-ii-java/)  
[33）最小堆栈](https://www.programcreek.com/2014/02/leetcode-min-stack-java/ "LeetCode –最小堆栈（Java）")  
34）多数元素：[I](https://www.programcreek.com/2014/02/leetcode-majority-element-java/ "LeetCode –多数元素（Java）")，[II](https://www.programcreek.com/2014/07/leetcode-majority-element-ii-java/)  
[35）公牛和母牛](https://www.programcreek.com/2014/05/leetcode-bulls-and-cows-java/)  
[36）直方图中最大的矩形](https://www.programcreek.com/2014/05/leetcode-largest-rectangle-in-histogram-java/ "LeetCode –直方图中的最大矩形（Java）")  
[37）最长的公共前缀](https://www.programcreek.com/2014/02/leetcode-longest-common-prefix-java/) \[Google\]  
[38）最大的数字](https://www.programcreek.com/2014/02/leetcode-largest-number-java/)  
[39）简化路径](https://www.programcreek.com/2014/04/leetcode-simplify-path-java/ "LeetCode –简化路径（Java）")  
[40）比较版本号](https://www.programcreek.com/2014/03/leetcode-compare-version-numbers-java/ "LeetCode –比较版本号（Java）")  
[41）加油站](https://www.programcreek.com/2014/03/leetcode-gas-station-java/ "LeetCode –加油站（Java）")  
44）帕斯卡三角形：[I](https://www.programcreek.com/2014/03/leetcode-pascals-triangle-java/)，[II](https://www.programcreek.com/2014/04/leetcode-pascals-triangle-ii-java/)  
[45）装满水的容器](https://www.programcreek.com/2014/03/leetcode-container-with-most-water-java/ "LeetCode –装满水的容器（Java）")  
[45）糖果](https://www.programcreek.com/2014/03/leetcode-candy-java/ "LeetCode –糖果（Java）") \[谷歌\]  
[45）诱捕雨水](https://www.programcreek.com/2014/06/leetcode-trapping-rain-water-java/ "LeetCode –捕获雨水（Java）")  
[46）数数并说](https://www.programcreek.com/2014/03/leetcode-count-and-say-java/ "LeetCode –计数并说（Java）")  
[47）搜索范围](https://www.programcreek.com/2014/04/leetcode-search-for-a-range-java/ "LeetCode –搜索范围（Java）")  
[48）基本计算器](https://www.programcreek.com/2014/06/leetcode-basic-calculator-java/)，[基本计算器II](https://www.programcreek.com/2014/05/leetcode-basic-calculator-ii-java/)  
[49）组字母图](https://www.programcreek.com/2014/04/leetcode-anagrams-java/ "LeetCode – Anagrams（Java）")  
[50）最短回文](https://www.programcreek.com/2014/06/leetcode-shortest-palindrome-java/ "LeetCode –最短回文（Java）")  
[51）矩形区域](https://www.programcreek.com/2014/06/leetcode-rectangle-area-java/ "LeetCode –矩形区域（Java）")  
[52）摘要范围](https://www.programcreek.com/2014/07/leetcode-summary-ranges-java/ "LeetCode –摘要范围（Java）")  
[53）增加三重](https://www.programcreek.com/2015/02/leetcode-increasing-triplet-subsequence-java/ "LeetCode –增加三重子序列（Java）")[态子序列](https://www.programcreek.com/2014/04/leetcode-anagrams-java/ "LeetCode – Anagrams (Java)")  
[54）使用目标数字列表和算术运算](https://www.programcreek.com/2016/04/get-target-using-number-list-and-arithmetic-operations-google/)  
[55）字符串的反元音](https://www.programcreek.com/2015/04/leetcode-reverse-vowels-of-a-string-java/)  
[56）翻转游戏](https://www.programcreek.com/2014/04/leetcode-flip-game-java/)，[翻转游戏II](https://www.programcreek.com/2014/05/leetcode-flip-game-ii-java/)  
[57）缺少数字](https://www.programcreek.com/2014/05/leetcode-missing-number-java/)，[找到重复的数字](https://www.programcreek.com/2015/06/leetcode-find-the-duplicate-number-java/)，[第一个缺少正数](https://www.programcreek.com/2014/05/leetcode-first-missing-positive-java/ "LeetCode –首次缺失肯定（Java）")  
[58）有效字谜](https://www.programcreek.com/2014/05/leetcode-valid-anagram-java/)，[组移位的字符串](https://www.programcreek.com/2014/05/leetcode-group-shifted-strings-java/)  
[59）前K个常见元素](https://www.programcreek.com/2014/05/leetcode-top-k-frequent-elements-java/)  
[60）查找峰值元素](https://www.programcreek.com/2014/02/leetcode-find-peak-element/)  
[61）字模式](https://www.programcreek.com/2014/05/leetcode-word-pattern-java/)，[字型II](https://www.programcreek.com/2014/07/leetcode-word-pattern-ii-java/)  
[62）H-Index](https://www.programcreek.com/2014/05/leetcode-h-index-java/)，[H-Index II](https://www.programcreek.com/2014/05/leetcode-h-index-ii-java/)  
[63）回文对](https://www.programcreek.com/2014/05/leetcode-palindrome-pairs-java/)  
[64）一个编辑距离](https://www.programcreek.com/2014/05/leetcode-one-edit-distance-java/)  
[65）扰乱字符串](https://www.programcreek.com/2014/05/leetcode-scramble-string-java/)  
[66）第一个不良版本](https://www.programcreek.com/2014/05/leetcode-first-bad-version-java/)  
[67）整数以英语单词](https://www.programcreek.com/2014/05/leetcode-integer-to-english-words-java/)  
[68）文本对齐方式](https://www.programcreek.com/2014/05/leetcode-text-justification-java/)  
[69）删除无效的括号](https://www.programcreek.com/2014/05/leetcode-remove-invalid-parentheses-java/)  
[70）交集两个数组的数量](https://www.programcreek.com/2015/05/leetcode-intersection-of-two-arrays-java/)，[两个数组的](https://www.programcreek.com/2015/05/leetcode-intersection-of-two-arrays-java/)[交集II](https://www.programcreek.com/2014/05/leetcode-intersection-of-two-arrays-ii-java/)  
[71）滑动窗口最大值](https://www.programcreek.com/2014/05/leetcode-sliding-window-maximum-java/)，[数据流的移动平均值](https://www.programcreek.com/2014/05/leetcode-moving-average-from-data-stream-java/)  
[72）猜测数更高或更低](https://www.programcreek.com/2014/07/leetcode-guess-number-higher-or-lower-java/)

**2.矩阵**

解决矩阵相关问题的常用方法包括DFS，BFS，动态编程等。

经典问题：  
[1）设置矩阵零点](https://www.programcreek.com/2012/12/leetcode-set-matrix-zeroes-java/)  
[2）螺旋矩阵](https://www.programcreek.com/2013/01/leetcode-spiral-matrix-java/)  
[2）螺旋矩阵II](https://www.programcreek.com/2014/05/leetcode-spiral-matrix-ii-java/ "LeetCode –螺旋矩阵II（Java）")  
[3）搜索2D矩阵](https://www.programcreek.com/2013/01/leetcode-search-a-2d-matrix-java/)  
[3）搜索2D矩阵II](https://www.programcreek.com/2014/04/leetcode-search-a-2d-matrix-ii-java/)  
[4）旋转图像](https://www.programcreek.com/2013/01/leetcode-rotate-image-java/) \[Palantir\]  
[5）有效数独](https://www.programcreek.com/2014/05/leetcode-valid-sudoku-java/ "LeetCode –有效的数独（Java）")  
[6）最小路径总和（DP）](https://www.programcreek.com/2014/05/leetcode-minimum-path-sum-java/ "LeetCode –最小路径总和（Java）") \[ Google\]  
[7）唯一路径（DP）](https://www.programcreek.com/2014/05/leetcode-unique-paths-java/ "LeetCode –唯一路径（Java）") \[Google\]  
[7）唯一路径II（DP）](https://www.programcreek.com/2014/05/leetcode-unique-paths-ii-java/ "LeetCode –唯一路径II（Java）")  
[8）](https://www.programcreek.com/2014/04/leetcode-number-of-islands-java/ "LeetCode –岛屿数量（Java）")孤岛[数](https://www.programcreek.com/2015/01/leetcode-number-of-islands-ii-java/)[（DFS / BFS）](https://www.programcreek.com/2014/04/leetcode-number-of-islands-java/ "LeetCode –岛屿数量（Java）")，孤岛[数II](https://www.programcreek.com/2015/01/leetcode-number-of-islands-ii-java/)（不交集），[无向图中连接的组件数](https://www.programcreek.com/2014/05/leetcode-number-of-connected-components-in-an-undirected-graph-java/)  
[9）周围区域（BFS）](https://www.programcreek.com/2014/04/leetcode-surrounded-regions-java/ "LeetCode –周围地区（Java）")  
[10）最大矩形](https://www.programcreek.com/2014/05/leetcode-maximal-rectangle-java/ "LeetCode –最大矩形（Java）")  
[10）最大正方形](https://www.programcreek.com/2014/06/leetcode-maximal-square-java/ "LeetCode –最大正方形（Java）")  
[11）单词搜索（DFS）](https://www.programcreek.com/2014/06/leetcode-word-search-java/ "LeetCode –单词搜索（Java）")  
[11）单词搜索II](https://www.programcreek.com/2014/06/leetcode-word-search-ii-java/ "LeetCode –单词搜索II（Java）")  
[13）范围总和查询2D –不可变](https://www.programcreek.com/2014/04/leetcode-range-sum-query-2d-immutable-java/)  
[14）矩阵中最长的增加路径（DFS）](https://www.programcreek.com/2014/05/leetcode-longest-increasing-path-in-a-matrix-java/)  
[15）与所有建筑物的最短距离](https://www.programcreek.com/2014/05/leetcode-shortest-distance-from-all-buildings-java/)  
[16）生命游戏](https://www.programcreek.com/2014/05/leetcode-game-of-life-java/)  
[17）油漆房](https://www.programcreek.com/2014/05/leetcode-paint-house-java/)，[油漆房II](https://www.programcreek.com/2014/05/leetcode-paint-house-ii-java/)  
[18）数独解算器（DFS）](https://www.programcreek.com/2014/05/leetcode-sudoku-solver-java/)  
[19）墙和门（DFS / BFS）](https://www.programcreek.com/2014/05/leetcode-walls-and-gates-java/)  
[20）井字游戏](https://www.programcreek.com/2014/05/leetcode-tic-tac-toe-java/)  
[21）最佳集合点](https://www.programcreek.com/2014/07/leetcode-best-meeting-point-java/)

**3.链表**

在Java中，链表的实现非常简单。每个节点都有一个值和到下一个节点的链接。
```
class Node {
	int val;
	Node next;
 
	Node(int x) {
		val = x;
		next = null;
	}
}
```

链表的两个流行应用是堆栈和队列。
Stack
```
class Stack{
	Node top; 
 
	public Node peek(){
		if(top != null){
			return top;
		}
 
		return null;
	}
 
	public Node pop(){
		if(top == null){
			return null;
		}else{
			Node temp = new Node(top.val);
			top = top.next;
			return temp;	
		}
	}
 
	public void push(Node n){
		if(n != null){
			n.next = top;
			top = n;
		}
	}
}
```
Queue
```
class Queue{
	Node first, last;
 
	public void enqueue(Node n){
		if(first == null){
			first = n;
			last = first;
		}else{
			last.next = n;
			last = n;
		}
	}
 
	public Node dequeue(){
		if(first == null){
			return null;
		}else{
			Node temp = new Node(first.val);
			first = first.next;
			return temp;
		}	
	}
}
```
Java标准库包含一个名为“ [Stack](https://docs.oracle.com/javase/7/docs/api/java/util/Stack.html) ” 的类。Java SDK中的另一个类是[LinkedList](https://docs.oracle.com/javase/7/docs/api/java/util/LinkedList.html)，它可用作队列（add（）和remove（））。（LinkedList实现Queue接口。）如果在面试过程中需要堆栈或队列来解决问题，则可以使用它们。

经典问题：  
[0）使用数组实现堆栈](https://www.programcreek.com/2015/03/implement-a-stack-using-an-array/)  
[1）添加两个数字](https://www.programcreek.com/2012/12/add-two-numbers/)  
[2）重新排序列表](https://www.programcreek.com/2013/12/in-place-reorder-a-singly-linked-list-in-java/)  
[3）链接列表循环](https://www.programcreek.com/2012/12/leetcode-linked-list-cycle/)  
[4）使用随机指针复制列表](https://www.programcreek.com/2012/12/leetcode-copy-list-with-random-pointer/)  
[5）合并两个排序的列表](https://www.programcreek.com/2012/12/leetcode-merge-two-sorted-lists-java/)  
[6）奇偶链接列表](https://www.programcreek.com/2015/03/leetcode-odd-even-linked-list-java/)  
[7）从排序中删除重复项列表](https://www.programcreek.com/2013/01/leetcode-remove-duplicates-from-sorted-list/)  
[7）从排序列表II中删除重复项](https://www.programcreek.com/2014/06/leetcode-remove-duplicates-from-sorted-list-ii-java/ "LeetCode –从排序列表II（Java）中删除重复项")  
[8）分区列表](https://www.programcreek.com/2013/02/leetcode-partition-list-java/)  
[9）LRU缓存](https://www.programcreek.com/2013/03/leetcode-lru-cache-java/)  
[10）两个链接列表的交集](https://www.programcreek.com/2014/02/leetcode-intersection-of-two-linked-lists-java/ "LeetCode –两个链表的交集（Java）")  
[11）删除链接列表元素](https://www.programcreek.com/2014/04/leetcode-remove-linked-list-elements-java/ "LeetCode –删除链接列表元素（Java）")  
[12）成对交换节点](https://www.programcreek.com/2014/04/leetcode-swap-nodes-in-pairs-java/ "LeetCode –成对交换节点（Java）")  
[13）反向链接列表](https://www.programcreek.com/2014/05/leetcode-reverse-linked-list-java/ "LeetCode –反向链接列表（Java）")，[反向链接列表II](https://www.programcreek.com/2014/06/leetcode-reverse-linked-list-ii-java/ "LeetCode –反向链接列表II（Java）")，打印链接列表以相反的顺序  
[14）从列表末尾删除第N个节点（快慢指针）](https://www.programcreek.com/2014/05/leetcode-remove-nth-node-from-end-of-list-java/ "LeetCode –从列表末尾删除第N个节点（Java）")  
[15）使用队列实现堆栈](https://www.programcreek.com/2014/06/leetcode-implement-stack-using-queues-java/ "LeetCode –使用队列实现堆栈（Java）")  
[15）使用堆栈实现队列](https://www.programcreek.com/2014/07/leetcode-implement-queue-using-stacks-java/ "LeetCode –使用堆栈实现队列（Java）")  
[16）回文链接列表](https://www.programcreek.com/2014/07/leetcode-palindrome-linked-list-java/ "LeetCode –回文链接列表（Java）")  
[17）使用数组实现队列](https://www.programcreek.com/2014/07/implement-a-queue-using-an-array-in-java/ "使用Java中的数组实现队列")  
[18）链接列表中的删除节点](https://www.programcreek.com/2014/07/leetcode-delete-node-in-a-linked-list-java/ "LeetCode –删除链接列表中的节点（Java）")  
[19）k组中的反向节点](https://www.programcreek.com/2014/05/leetcode-reverse-nodes-in-k-group-java/)

**4.树，堆和树**

树通常是指二叉树。每个节点都包含一个左节点和一个右节点，如下所示：

```
class TreeNode{
	int value;
	TreeNode left;
	TreeNode right;
}
```

以下是一些与树相关的概念：

1.  _二进制搜索树_：对于所有节点，左子节点<=当前节点<=右子节点
2.  _平衡与不平衡_：在平衡树中，每个节点的左右子树的深度相差1或更小。
3.  _完整的二叉树_：除叶子外的每个节点都有两个孩子。
4.  _完美二叉树_：完整的二叉树，其中所有叶子处于相同深度或相同级别，并且每个父级都有两个子级。
5.  _完整的二叉树_：一个二叉树，其中每个级别（除了最后一个级别）都已完全填充，并且所有节点都尽可能地靠左

[堆](https://en.wikipedia.org/wiki/Heap_(data_structure))是满足堆属性的基于树的专用数据结构。其操作的时间复杂度很重要（例如，find-min，delete-min，insert等）。在Java中，必须了解[PriorityQueue](https://www.programcreek.com/2009/02/using-the-priorityqueue-class-example/)。

**4.1树**

1）二叉树的遍历：[预订](https://www.programcreek.com/2012/12/leetcode-solution-for-binary-tree-preorder-traversal-in-java/)，[中序](https://www.programcreek.com/2012/12/leetcode-solution-of-binary-tree-inorder-traversal-in-java/)，[后序](https://www.programcreek.com/2012/12/leetcode-solution-of-iterative-binary-tree-postorder-traversal-in-java/)，[级订单](https://www.programcreek.com/2014/04/leetcode-binary-tree-level-order-traversal-java/)，[级订单II](https://www.programcreek.com/2014/04/leetcode-binary-tree-level-order-traversal-ii-java/)，[垂直顺序](https://www.programcreek.com/2014/04/leetcode-binary-tree-vertical-order-traversal-java/)  
[2）反转二叉树](https://www.programcreek.com/2014/06/leetcode-invert-binary-tree-java/ "LeetCode –反转二叉树（Java）")  
[在BST 3）第K个最小元素](https://www.programcreek.com/2014/07/leetcode-kth-smallest-element-in-a-bst-java/ "LeetCode – BST（Java）中的Kth最小元素")  
[4）二叉树最长连续序列](https://www.programcreek.com/2014/04/leetcode-binary-tree-longest-consecutive-sequence-java/)  
[5）确认二叉搜索树](https://www.programcreek.com/2012/12/leetcode-validate-binary-search-tree-java/)  
[6）平铺二叉树到链表](https://www.programcreek.com/2013/01/leetcode-flatten-binary-tree-to-linked-list/)  
[7）路径总和（DFS或BFS）](https://www.programcreek.com/2013/01/leetcode-path-sum/)  
[7）路径总和II（DFS）](https://www.programcreek.com/2014/05/leetcode-path-sum-ii-java/ "LeetCode –路径求和II（Java）")  
[8）从有序和后序遍历](https://www.programcreek.com/2013/01/construct-binary-tree-from-inorder-and-postorder-traversal/)  
[构造二叉树8）](https://www.programcreek.com/2014/06/leetcode-construct-binary-tree-from-preorder-and-inorder-traversal-java/ "LeetCode –通过预排序和有序遍历（Java）构造二叉树")[从有序和有序遍历](https://www.programcreek.com/2013/01/construct-binary-tree-from-inorder-and-postorder-traversal/)[构造二叉树](https://www.programcreek.com/2014/06/leetcode-construct-binary-tree-from-preorder-and-inorder-traversal-java/ "LeetCode –通过预排序和有序遍历（Java）构造二叉树")  
[9）将排序的数组转换为二叉搜索树](https://www.programcreek.com/2013/01/leetcode-convert-sorted-array-to-binary-search-tree-java/) \[Google\]  
[10）将排序后的列表转换为二进制搜索树](https://www.programcreek.com/2013/01/leetcode-convert-sorted-list-to-binary-search-tree-java/)\[Google\]  
[11）二叉树的最小深度](https://www.programcreek.com/2013/02/leetcode-minimum-depth-of-binary-tree-java/)  
[12）二叉树的最大路径总和\*](https://www.programcreek.com/2013/02/leetcode-binary-tree-maximum-path-sum-java/)  
[13）平衡二叉树](https://www.programcreek.com/2013/02/leetcode-balanced-binary-tree-java/)  
[14）对称树](https://www.programcreek.com/2014/03/leetcode-symmetric-tree-java/ "LeetCode –对称树（Java）")  
[15）二叉搜索树迭代器](https://www.programcreek.com/2014/04/leetcode-binary-search-tree-iterator-java/ "LeetCode –二进制搜索树迭代器（Java）")  
[16）二叉树右侧视图](https://www.programcreek.com/2014/04/leetcode-binary-tree-right-side-view-java/ "LeetCode –二叉树右侧视图（Java）")  
[17）二叉搜索树的最低共同祖先](https://www.programcreek.com/2014/07/leetcode-lowest-common-ancestor-of-a-binary-search-tree-java/ "LeetCode –二进制搜索树的最低公共祖先（Java）")  
[18）二叉树的最低公共祖先](https://www.programcreek.com/2014/07/leetcode-lowest-common-ancestor-of-a-binary-tree-java/ "LeetCode –二叉树的最低公共祖先（Java）")  
[19）验证](https://www.programcreek.com/2015/01/leetcode-verify-preorder-serialization-of-a-binary-tree-java/)[二叉树的](https://www.programcreek.com/2014/07/leetcode-lowest-common-ancestor-of-a-binary-tree-java/ "LeetCode –二叉树的最低公共祖先（Java）")[预序列化](https://www.programcreek.com/2015/01/leetcode-verify-preorder-serialization-of-a-binary-tree-java/)  
[20）在每个节点中填充下一个右指针](https://www.programcreek.com/2014/05/leetcode-populating-next-right-pointers-in-each-node-java/ "LeetCode –在每个节点中填充下一个右指针（Java）")  
[21）在每个节点II中填充下一个右指针](https://www.programcreek.com/2014/06/leetcode-populating-next-right-pointers-in-each-node-ii-java/ "LeetCode –在每个节点II中填充下一个右指针（Java）")  
[21）唯一的二进制搜索树（DP）](https://www.programcreek.com/2014/05/leetcode-unique-binary-search-trees-java/ "LeetCode –唯一二进制搜索树（Java）")  
[21）唯一的二进制搜索树II（DFS）](https://www.programcreek.com/2014/05/leetcode-unique-binary-search-trees-ii-java/ "LeetCode –唯一二进制搜索树II（Java）")  
[22）根到叶的总数（DFS）](https://www.programcreek.com/2014/05/leetcode-sum-root-to-leaf-numbers-java/ "LeetCode –叶数的总根（Java）")  
[23）计数完整树节点](https://www.programcreek.com/2014/06/leetcode-count-complete-tree-nodes-java/ "LeetCode –计数完整树节点（Java）")  
[24）最近的二叉搜索树值](https://www.programcreek.com/2014/05/leetcode-closest-binary-search-tree-value-java/)  
[25）二叉树路径](https://www.programcreek.com/2014/05/leetcode-binary-tree-paths-java/)  
[26）二叉树的最大深度](https://www.programcreek.com/2014/05/leetcode-maximum-depth-of-binary-tree-java/)  
[27恢复二叉搜索树](https://www.programcreek.com/2014/05/leetcode-recover-binary-search-tree-java/)  
[28）相同树](https://www.programcreek.com/2012/12/check-if-two-trees-are-same-or-not/)  
[29）对二叉树进行序列化和反序列化](https://www.programcreek.com/2014/05/leetcode-serialize-and-deserialize-binary-tree-java/)  
[30）在BST中顺序](https://www.programcreek.com/2014/05/leetcode-inorder-successor-in-bst-java/)[排序](https://www.programcreek.com/2014/05/leetcode-recover-binary-search-tree-java/)  
[31）查找二叉树的叶子](https://www.programcreek.com/2014/07/leetcode-find-leaves-of-binary-tree-java/)  
[32）最大的BST子树](https://www.programcreek.com/2014/07/leetcode-largest-bst-subtree-java/)

**4.2堆**

[1）合并k个排序数组](https://www.programcreek.com/2014/05/merge-k-sorted-arrays-in-java/ "合并Java中的K个排序数组") \[Google\]  
[2）合并k个排序列表\*](https://www.programcreek.com/2013/02/leetcode-merge-k-sorted-lists-java/)  
[3）从数据流中查找中位数](https://www.programcreek.com/2015/01/leetcode-find-median-from-data-stream-java/)  
[4）会议室II](https://www.programcreek.com/2014/05/leetcode-meeting-rooms-ii-java/)，[会议室](https://www.programcreek.com/2014/07/leetcode-meeting-rooms-java/)  
[5）范围添加](https://www.programcreek.com/2014/07/leetcode-range-addition-java/)

**4.3特里**

[1）实施Trie（前缀树）](https://www.programcreek.com/2014/05/leetcode-implement-trie-prefix-tree-java/ "LeetCode –实施Trie（前缀树）（Java）")  
[2）添加和搜索Word-数据结构设计（DFS）](https://www.programcreek.com/2014/05/leetcode-add-and-search-word-data-structure-design-java/ "LeetCode –添加和搜索Word –数据结构设计（Java）")

**4.4段树**

[1）范围总和查询-可变](https://www.programcreek.com/2014/04/leetcode-range-sum-query-mutable-java/)  
[2）天际线问题](https://www.programcreek.com/2014/06/leetcode-the-skyline-problem-java/)

**5.图**

与图相关的问题主要集中在深度优先搜索和呼吸优先搜索。深度优先搜索非常简单，您可以从根节点开始遍历所有邻居。

以下是图形和呼吸优先搜索的简单实现。关键是使用队列存储节点。

![呼吸优先搜索](https://www.programcreek.com/wp-content/uploads/2012/11/breath-first-search-300x284.png)
1) Define a GraphNode
```
class GraphNode{ 
	int val;
	GraphNode next;
	GraphNode[] neighbors;
	boolean visited;
 
	GraphNode(int x) {
		val = x;
	}
 
	GraphNode(int x, GraphNode[] n){
		val = x;
		neighbors = n;
	}
 
	public String toString(){
		return "value: "+ this.val; 
	}
}
```
2) Define a Queue
```
class Queue{
	GraphNode first, last;
 
	public void enqueue(GraphNode n){
		if(first == null){
			first = n;
			last = first;
		}else{
			last.next = n;
			last = n;
		}
	}
 
	public GraphNode dequeue(){
		if(first == null){
			return null;
		}else{
			GraphNode temp = new GraphNode(first.val, first.neighbors);
			first = first.next;
			return temp;
		}	
	}
}
```
3) Breath First Search uses a Queue
```
public class GraphTest {
 
	public static void main(String[] args) {
		GraphNode n1 = new GraphNode(1); 
		GraphNode n2 = new GraphNode(2); 
		GraphNode n3 = new GraphNode(3); 
		GraphNode n4 = new GraphNode(4); 
		GraphNode n5 = new GraphNode(5); 
 
		n1.neighbors = new GraphNode[]{n2,n3,n5};
		n2.neighbors = new GraphNode[]{n1,n4};
		n3.neighbors = new GraphNode[]{n1,n4,n5};
		n4.neighbors = new GraphNode[]{n2,n3,n5};
		n5.neighbors = new GraphNode[]{n1,n3,n4};
 
		breathFirstSearch(n1, 5);
	}
 
	public static void breathFirstSearch(GraphNode root, int x){
		if(root.val == x)
			System.out.println("find in root");
 
		Queue queue = new Queue();
		root.visited = true;
		queue.enqueue(root);
 
		while(queue.first != null){
			GraphNode c = (GraphNode) queue.dequeue();
			for(GraphNode n: c.neighbors){
 
				if(!n.visited){
					System.out.print(n + " ");
					n.visited = true;
					if(n.val == x)
						System.out.println("Find "+n);
					queue.enqueue(n);
				}
			}
		}
	}
}
```
Output:
```
value: 2 value: 3 value: 5 Find value: 5
value: 4
```

经典问题：  
[1）复制图表](https://www.programcreek.com/2012/12/leetcode-clone-graph-java/)  
[2）课程表](https://www.programcreek.com/2014/05/leetcode-course-schedule-java/ "LeetCode –课程表（Java）")，[课程表II](https://www.programcreek.com/2014/06/leetcode-course-schedule-ii-java/ "LeetCode –课程表II（Java）")，[最小身高树](https://www.programcreek.com/2014/07/leetcode-minimum-height-trees-java/)  
[3）重建行程](https://www.programcreek.com/2015/03/leetcode-reconstruct-itinerary-java/)  
[4）图有效树](https://www.programcreek.com/2014/05/graph-valid-tree-java/)

**6.排序**

不同排序算法的时间复杂度。您可以转到Wiki来查看它们的基本概念。

|  Algorithm     |  Average Time |  Worst Time | Space   |
|----------------|---------------|-------------|---------|
|  Bubble sort   |  n^2          |  n^2        | 1       |
| Selection sort | n^2           | n^2         | 1       |
| Insertion sort | n^2           | n^2         |         |
| Quick sort     | n log\(n\)    | n^2         |         |
| Merge sort     | n log\(n\)    | n log\(n\)  | depends |


要看

\* BinSort，Radix Sort和CountSort与其他假设使用不同的假设集，因此它们不是“常规”排序方法。（感谢Fidel指出这一点）

这是一些实现/演示，此外，您可能想了解[Java开发人员在实践中的排序方式](https://www.programcreek.com/2014/03/how-developers-sort-in-java/)。  
[1）Mergesort](https://www.programcreek.com/2012/11/leetcode-solution-merge-sort-linkedlist-in-java/)  
[2）Quicksort](https://www.programcreek.com/2012/11/quicksort-array-in-java/)  
[3）InsertionSort](https://www.programcreek.com/2012/11/leetcode-solution-sort-a-linked-list-using-insertion-sort-in-java/)。  
[4）最大间隙（桶排序）](https://www.programcreek.com/2014/03/leetcode-maximum-gap-java/ "LeetCode –最大差距（Java）")  
[5）颜色排序（计数排序）](https://www.programcreek.com/2014/06/leetcode-sort-colors-java/ "LeetCode –排序颜色（Java）")

**7.动态编程**

动态编程是一种用于解决具有以下属性的问题的技术：

1.  使用较小实例的解决方案来解决实例。
2.  对于较小实例的解决方案可能需要多次。
3.  较小实例的解决方案存储在表中，因此每个较小实例仅解决一次。
4.  额外的空间用于节省时间。

？  
攀登台阶的问题完全适合这4个属性。因此，可以通过使用动态编程来解决。

```
public static int[] A = new int[100];
 
public static int f3(int n) {
	if (n <= 2)
		A[n]= n;
 
	if(A[n] > 0)
		return A[n];
	else
		A[n] = f3(n-1) + f3(n-2);//store results so only calculate once!
	return A[n];
}
```

经典问题：  
[1）编辑距离](https://www.programcreek.com/2013/12/edit-distance-in-java/ "用Java编辑距离")  
[1）不同的](https://www.programcreek.com/2013/01/leetcode-distinct-subsequences-total-java/)  
[子序列](https://www.programcreek.com/2013/12/leetcode-solution-of-longest-palindromic-substring-java/ "Java中最长回文子串的Leetcode解决方案")[总数](https://www.programcreek.com/2013/01/leetcode-distinct-subsequences-total-java/)[2）最长的回文子串](https://www.programcreek.com/2013/12/leetcode-solution-of-longest-palindromic-substring-java/ "Java中最长回文子串的Leetcode解决方案")  
[3）断字](https://www.programcreek.com/2012/12/leetcode-solution-word-break/ "Leetcode解决方案–分词")  
[3）断字II](https://www.programcreek.com/2014/03/leetcode-word-break-ii-java/ "LeetCode – Word Break II（Java）")  
[4）最大子数组](https://www.programcreek.com/2013/02/leetcode-maximum-subarray-java/)  
[4）最大乘积子数组](https://www.programcreek.com/2014/03/leetcode-maximum-product-subarray-java/ "LeetCode –最大产品子数组（Java）")  
[5）回文分区](https://www.programcreek.com/2013/03/leetcode-palindrome-partitioning-java/ "LeetCode –回文分区（Java）")  
[5）回文分区II](https://www.programcreek.com/2014/04/leetcode-palindrome-partitioning-ii-java/ "LeetCode –回文分区II（Java）")  
[6）强盗](https://www.programcreek.com/2014/03/leetcode-house-robber-java/ "LeetCode –强盗（Java）") \[Google \]  
[6）抢劫犯II](https://www.programcreek.com/2014/05/leetcode-house-robber-ii-java/ "LeetCode – House Robber II（Java）")  
[6）抢劫犯III](https://www.programcreek.com/2015/03/leetcode-house-robber-iii-java/)  
[7）跳跃游戏](https://www.programcreek.com/2014/03/leetcode-jump-game-java/ "LeetCode –跳跃游戏（Java）")  
[7）跳跃游戏II](https://www.programcreek.com/2014/06/leetcode-jump-game-ii-java/ "LeetCode –跳跃游戏II（Java）")  
[8）最佳买卖股票](https://www.programcreek.com/2014/02/leetcode-best-time-to-buy-and-sell-stock-java/ "LeetCode –买卖股票的最佳时间（Java）")  
[时间8）最佳买卖股票](https://www.programcreek.com/2014/02/leetcode-best-time-to-buy-and-sell-stock-ii-java/ "LeetCode –最佳买卖股票II（Java）")  
[时间](https://www.programcreek.com/2014/02/leetcode-best-time-to-buy-and-sell-stock-iii-java/ "LeetCode –最佳买卖股票III（Java）")[II](https://www.programcreek.com/2014/02/leetcode-best-time-to-buy-and-sell-stock-ii-java/ "LeetCode –最佳买卖股票II（Java）") [8）最佳买卖股票时间III](https://www.programcreek.com/2014/02/leetcode-best-time-to-buy-and-sell-stock-iii-java/ "LeetCode –最佳买卖股票III（Java）")  
[8 ）买卖股票IV的最佳时间](https://www.programcreek.com/2014/03/leetcode-best-time-to-buy-and-sell-stock-iv-java/ "LeetCode –最佳买卖股票IV（Java）")  
[9）地下城游戏](https://www.programcreek.com/2014/03/leetcode-dungeon-game-java/ "LeetCode –地牢游戏（Java）")  
[10）最小路径总和](https://www.programcreek.com/2014/05/leetcode-minimum-path-sum-java/ "LeetCode –最小路径总和（Java）")  
[11）唯一路径](https://www.programcreek.com/2014/05/leetcode-unique-paths-java/ "LeetCode –唯一路径（Java）")  
[12）解码方式](https://www.programcreek.com/2014/06/leetcode-decode-ways-java/ "LeetCode –解码方式（Java）")  
[13）最长的公共](https://www.programcreek.com/2014/04/longest-common-subsequence-java/)  
[子序列14）最长的公共子串](https://www.programcreek.com/2015/04/longest-common-substring-java/)  
[15）最长的增长](https://www.programcreek.com/2014/04/leetcode-longest-increasing-subsequence-java/)[子序列](https://www.programcreek.com/2015/04/longest-common-substring-java/)  
[16）硬币找零](https://www.programcreek.com/2015/04/leetcode-coin-change-java/)  
[17）完美正方形](https://www.programcreek.com/2014/05/leetcode-perfect-squares-java/)

**8.位操作**

位运算符：
| OR \(\|\) | AND \(&\) | XOR \(^\) | Left Shift \(<<\) | Right Shift \(>>\) | Not \(~\) |
|-----------|-----------|-----------|-------------------|--------------------|-----------|
| 1\|0=1    | 1&0=0     | 1^0=1     | 0010<<2=1000      | 1100>>2=0011       | ~1=0      |

得到第i个给定数字n。（我从0开始计数，从右开始）

```
public static boolean getBit(int num, int i){
	int result = num & (1<<i);
 
	if(result == 0){
		return false;
	}else{
		return true;
	}
}
```


例如，获取数字10的第二位。

```
i=1, n=10
1<<1= 10 1010&10=10 10 is not 0, so return true;
```

经典问题：  
[1）单个数字](https://www.programcreek.com/2012/12/leetcode-solution-of-single-number-in-java/)  
[1）单个数字II](https://www.programcreek.com/2014/03/leetcode-single-number-ii-java/ "LeetCode –单一数字II（Java）")  
[2）最大二进制间隙](https://www.programcreek.com/2013/02/twitter-codility-problem-max-binary-gap/)  
[3）1个位数](https://www.programcreek.com/2014/03/leetcode-number-of-1-bits-java/ "LeetCode – 1位数量（Java）")  
[4）反转位](https://www.programcreek.com/2014/03/leetcode-reverse-bits-java/ "LeetCode –反向位（Java）")  
[5）重复的DNA序列](https://www.programcreek.com/2014/03/leetcode-repeated-dna-sequences-java/ "LeetCode –重复的DNA序列（Java）")  
[6）数字范围的按位与](https://www.programcreek.com/2014/04/leetcode-bitwise-and-of-numbers-range-java/ "LeetCode –数字范围的按位与（Java）")  
[7）两个整数的总和](https://www.programcreek.com/2015/07/leetcode-sum-of-two-integers-java/)  
[8）计数位](https://www.programcreek.com/2015/03/leetcode-counting-bits-java/)  
[9 ）字长的最大乘积](https://www.programcreek.com/2014/04/leetcode-maximum-product-of-word-lengths-java/)  
[10）格雷码](https://www.programcreek.com/2014/05/leetcode-gray-code-java/)

**9.组合和排列**

组合和排列之间的区别在于顺序是否重要。

范例1：

> 给定5个数字-1、2、3、4和5，打印出5个数字的不同顺序。4不能是第三个，3和5不能相邻。有多少种不同的组合？

范例2：

> 给定5个banaba，4个梨和3个苹果，假设一种水果是相同的，那么有多少种不同的组合？

类问题：  
[1）排列](https://www.programcreek.com/2013/02/leetcode-permutations-java/)  
[2）排列II](https://www.programcreek.com/2013/02/leetcode-permutations-ii-java/)  
[3）排列序列](https://www.programcreek.com/2013/02/leetcode-permutation-sequence-java/)  
[4）生成括号](https://www.programcreek.com/2014/01/leetcode-generate-parentheses-java/)  
[5）组合和（DFS）](https://www.programcreek.com/2014/02/leetcode-combination-sum-java/ "LeetCode –组合和（Java）")，[II（DFS）](https://www.programcreek.com/2014/04/leetcode-combination-sum-ii-java/ "LeetCode –组合和II（Java）")，[III（DFS）](https://www.programcreek.com/2014/05/leetcode-combination-sum-iii-java/ "LeetCode –组合总和III（Java）")，[IV（DP）](https://www.programcreek.com/2014/07/leetcode-combination-sum-iv-java/)  
[6）组合（DFS）](https://www.programcreek.com/2014/03/leetcode-combinations-java/ "LeetCode –组合（Java）")  
[7）字母组合电话号码（DFS）](https://www.programcreek.com/2014/04/leetcode-letter-combinations-of-a-phone-number-java/ "LeetCode –电话号码的字母组合（Java）")  
[8）恢复IP地址](https://www.programcreek.com/2014/06/leetcode-restore-ip-addresses-java/ "LeetCode –恢复IP地址（Java）")  
[9）因素组合](https://www.programcreek.com/2014/07/leetcode-factor-combinations-java/)（DFS）

**10.数学**

解决数学问题通常需要我们从观察中找到规律性或重复模式。如果您没有任何想法，请首先列出一小部分数字的结果。

[1）反转整数](https://www.programcreek.com/2012/12/leetcode-reverse-integer/)  
[2）回文编号](https://www.programcreek.com/2013/02/leetcode-palindrome-number-java/)  
3）[的Pow（X，N）](https://www.programcreek.com/2012/12/leetcode-powx-n/) ，[两个功率](https://www.programcreek.com/2014/07/leetcode-power-of-two-java/ "LeetCode – 2的幂（Java）")，[三个功率](https://www.programcreek.com/2014/04/leetcode-power-of-three-java/)，[四电源](https://www.programcreek.com/2015/04/leetcode-power-of-four-java/)  
[4）亚群](https://www.programcreek.com/2013/01/leetcode-subsets-java/)  
[5）亚群II](https://www.programcreek.com/2013/01/leetcode-subsets-ii-java/)  
[6）馏分循环小数](https://www.programcreek.com/2014/03/leetcode-fraction-to-recurring-decimal-java/ "LeetCode –递归小数的分数（Java）")（谷歌）  
[7）的Excel工作表列号](https://www.programcreek.com/2014/03/leetcode-excel-sheet-column-number-java/ "LeetCode – Excel工作表列号（Java）")  
[8）Excel工作表列标题](https://www.programcreek.com/2014/03/leetcode-excel-sheet-column-title-java/ "LeetCode – Excel工作表列标题（Java）")  
[9）因子尾随零](https://www.programcreek.com/2014/04/leetcode-factorial-trailing-zeroes-java/ "LeetCode –阶乘尾随零（Java）")  
[10）快乐数](https://www.programcreek.com/2014/04/leetcode-happy-number-java/ "LeetCode –快乐号码（Java）")  
[11）计数素数](https://www.programcreek.com/2014/04/leetcode-count-primes-java/ "LeetCode –素数（Java）")  
[12）加上1](https://www.programcreek.com/2014/05/leetcode-plus-one-java/ "LeetCode –加一（Java）")  
[13）除以两个整数](https://www.programcreek.com/2014/05/leetcode-divide-two-integers-java/ "LeetCode –除以两个整数（Java）")  
[14）乘以字符串](https://www.programcreek.com/2014/05/leetcode-multiply-strings-java/ "LeetCode –乘法字符串（Java）")  
[15）一行上的最大点](https://www.programcreek.com/2014/04/leetcode-max-points-on-a-line-java/ "LeetCode –线上最大点数（Java）")  
[16）数组乘积（自我除外](https://www.programcreek.com/2014/07/leetcode-product-of-array-except-self-java/ "LeetCode –阵列除自身（Java）产品")  
[）17）整数中断](https://www.programcreek.com/2015/04/leetcode-integer-break-java/)  
[18）添加数字](https://www.programcreek.com/2014/04/leetcode-add-digits-java/)  
[21）丑数](https://www.programcreek.com/2014/05/leetcode-ugly-number-java/)，9 [丑数II](https://www.programcreek.com/2014/05/leetcode-ugly-number-ii-java/)，[超级丑数](https://www.programcreek.com/2014/05/leetcode-super-ugly-number-java/)，[求和最小的K对](https://www.programcreek.com/2015/07/leetcode-find-k-pairs-with-smallest-sums-java/)

更新：我决定在下面添加更多类别。

**11\. HashMap**

[1）最短单词距离II](https://www.programcreek.com/2014/07/leetcode-shortest-word-distance-ii-java/)

附加问题：  
[1）自穿越](https://www.programcreek.com/2015/03/leetcode-self-crossing-java/)  
[2）修补阵列](https://www.programcreek.com/2015/01/leetcode-patching-array-java/)  
[3）尼姆游戏](https://www.programcreek.com/2014/04/leetcode-nim-game-java/)  
[4）灯泡切换器](https://www.programcreek.com/2014/05/leetcode-bulb-switcher-java/)  
[5）止痛栅栏](https://www.programcreek.com/2014/05/leetcode-pain-fence-java/)  
[6）嵌套列表权重总和](https://www.programcreek.com/2014/05/leetcode-nested-list-weight-sum-java/)

**其他资源**  
1\. [将您的代码共享到Github / BitBucket](https://www.programcreek.com/2013/02/how-to-share-your-eclipse-projects-to-github/)

### 相关文章：

1.  [LeetCode – Word Ladder II（Java）](https://www.programcreek.com/2014/06/leetcode-word-ladder-ii-java/ "LeetCode – Word Ladder II（Java）")
2.  [如何回答面试中的编码问题？](https://www.programcreek.com/2013/02/how-to-answer-coding-questions-for-your-interview/ "如何回答面试中的编码问题？")
3.  [LeetCode – LRU缓存（Java）](https://www.programcreek.com/2013/03/leetcode-lru-cache-java/ "LeetCode – LRU缓存（Java）")
4.  [LeetCode –自我后的小数计数（Java）](https://www.programcreek.com/2015/12/leetcode-count-of-smaller-numbers-after-self-java/ "LeetCode –自我后的小数计数（Java）")