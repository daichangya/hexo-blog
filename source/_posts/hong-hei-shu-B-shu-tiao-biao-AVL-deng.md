---
title: 红黑树、B(+)树、跳表、AVL等数据结构，应用场景及分析，以及一些英文缩写
id: 1482
date: 2024-10-31 22:01:57
author: daichangya
excerpt: 红黑树、B(+)树、跳表、AVL等数据结构，应用场景及分析，以及一些英文缩写在网上学习了一些材料。这一篇：https//www.zhihu.com/question/30527705AVL树最早的平衡二叉树之一。应用相对其他数据结构比较少。windows对进程地址空间的管理用到了AVL树红黑树
permalink: /archives/hong-hei-shu-B-shu-tiao-biao-AVL-deng/
tags:
- 算法
---


在网上学习了一些材料。

这一篇：https://www.zhihu.com/question/30527705

```
AVL树:最早的平衡二叉树之一。应用相对其他数据结构比较少。windows对进程地址空间的管理用到了AVL树

红黑树:平衡二叉树，广泛用在C++的STL中。map和set都是用红黑树实现的。我们熟悉的STL的map容器底层是RBtree,当然指的不是unordered_map,后者是hash。

B/B+树用在磁盘文件组织 数据索引和数据库索引

Trie树 字典树，用在统计和排序大量字符串

------

AVL是一种高度平衡的二叉树，所以通常的结果是，维护这种高度平衡所付出的代价比从中获得的效率收益还大，故而实际的应用不多，更多的地方是用追求局部而不是非常严格整体平衡的红黑树。当然，如果场景中对插入删除不频繁，只是对查找特别有要求，AVL还是优于红黑的。

红黑树的应用就很多了，除了上面同学提到的STL，还有
epoll在内核中的实现，用红黑树管理事件块
nginx中，用红黑树管理timer等
Java的TreeMap实现
著名的linux进程调度Completely Fair Scheduler,用红黑树管理进程控制块

B和B+主要用在文件系统以及数据库中做索引等，比如Mysql：B-Tree Index in MySql

trie 树的一个典型应用是前缀匹配，比如下面这个很常见的场景，在我们输入时，搜索引擎会给予提示
还有比如IP选路，也是前缀匹配，一定程度会用到trie

------

跳表：Redis中就使用跳表，而不是红黑树来存储管理其中的元素（应该说的是一级元素-直接的Key,里面的value应该是有不同的数据结构）。

首先，跳表是skiplist？不是ziplist。ziplist在redis中是一个非常省内存的链表（代价是性能略低），所以在hash元素的个数很少（比如只有几十个），那么用这个结构来存储则可以在性能损失很小的情况下节约很多内存（redis是内存数据库啊，能省还是要省的）。好这个问题清楚了。

在server端，对并发和性能有要求的情况下，如何选择合适的数据结构（这里是跳跃表和红黑树）。
如果单纯比较性能，跳跃表和红黑树可以说相差不大，但是加上并发的环境就不一样了，如果要更新数据，跳跃表需要更新的部分就比较少，锁的东西也就比较少，所以不同线程争锁的代价就相对少了，而红黑树有个平衡的过程，牵涉到大量的节点，争锁的代价也就相对较高了。性能也就不如前者了。
在并发环境下skiplist有另外一个优势，红黑树在插入和删除的时候可能需要做一些rebalance的操作，这样的操作可能会涉及到整个树的其他部分，而skiplist的操作显然更加局部性一些，锁需要盯住的节点更少，因此在这样的情况下性能好一些。
```

另外Redis作者描述的使用跳表的原因：

```
请看开发者说的，他为什么选用skiplist The Skip list

There are a few reasons:
1) They are not very memory intensive. It's up to you basically. 
Changing parameters about the probability of a node to have a 
given number of levels will make then less memory intensive than 
btrees.
注：跳表的一个缺点是耗内存（因为要重复分层存节点），但是作者也说了
，可以调参数来降低内存消耗，和那些平衡树结构达到差不多。
2) A sorted set is often target of many ZRANGE or ZREVRANGE 
operations, that is, traversing the skip list as a linked list.
 With this operation the cache locality of skip lists is at least
 as good as with other kind of balanced trees.
注：redis经查有范围操作，这样利用跳表里面的双向链表，可以方便地操作
。另外还有缓存区域化（cache locality）不会比平衡树差。
```

上面文章中有一些英文缩写，整理如下：

```
imho， imo（in my humble opinion， in my opinion）：在我看来，常见于论坛。

idk（I don’t know）：我不知道。

rofl（rolling on the floor laughing）：笑到摔到地上。

roflmao（rolling on the floor laughing my ass of）：前两个的结合版，也就是超级搞笑的意思。

sth（something）：某事某物。

nth（nothing）：什么也没有。

plz（please）：请。please 字尾是z 音，所以按照读音缩写为plz。

thx（thanks）：谢谢。按照发音来看，thanks字尾的ks可以用字母X代替。
```

红黑树与B(+)树工程实现的比较：

```
已有的几个答案都是从算法角度分析的，我尝试分析下从工程角度区分红黑树与b+树的应用场景，红黑树一个node只存一对kv，因此可以使用类似嵌入式链表的方式实现，数据结构本身不管理内存，比较轻量级，使用更灵活也更省内存，比如一个node可以同时存在若干个树或链表中，内核中比较常见。而b+树由于每个node要存多对kv，node结构的内存一般就要由数据结构自己来管，是真正意义上的container，相对嵌入式方法实现的红黑树，好处是用法简单，自己管理内存更容易做lockfree，一个node存多对kv的方式cpu cache命中率更高，所以用户态实现的高并发索引一般还是选b+树。再说b树与b+树，btree的中间节点比b+树多存了value，同样出度的情况下，node更大，相对来说cpu cache命中率是不如b+树的。另外再提一句，b+树的扫描特性（链表串起来的叶子节点）在无锁情况下是很难做的（我还没见到过解法），因此我目前见到的无锁b+树叶子节点都是不串起来的。
```

从各自特点特征角度，分析各种数据结构的应用场景：

```
红黑树，AVL树简单来说都是用来搜索的呗。
AVL树：平衡二叉树，一般是用平衡因子差值决定并通过旋转来实现，左右子树树高差不超过1，那么和红黑树比较它是严格的平衡二叉树，平衡条件非常严格（树高差只有1），只要插入或删除不满足上面的条件就要通过旋转来保持平衡。由于旋转是非常耗费时间的。我们可以推出AVL树适合用于插入删除次数比较少，但查找多的情况。

红黑树：平衡二叉树，通过对任何一条从根到叶子的简单路径上各个节点的颜色进行约束，确保没有一条路径会比其他路径长2倍，因而是近似平衡的。所以相对于严格要求平衡的AVL树来说，它的旋转保持平衡次数较少。用于搜索时，插入删除次数多的情况下我们就用红黑树来取代AVL。
（现在部分场景使用跳表来替换红黑树，可搜索“为啥 redis 使用跳表(skiplist)而不是使用 red-black？”）

B树，B+树：它们特点是一样的，是多路查找树，一般用于数据库系统中，为什么，因为它们分支多层数少呗，都知道磁盘IO是非常耗时的，而像大量数据存储在磁盘中所以我们要有效的减少磁盘IO次数避免磁盘频繁的查找。
B+树是B树的变种树，有n棵子树的节点中含有n个关键字，每个关键字不保存数据，只用来索引，数据都保存在叶子节点。是为文件系统而生的。

Trie树：
又名单词查找树，一种树形结构，常用来操作字符串。它是不同字符串的相同前缀只保存一份。
相对直接保存字符串肯定是节省空间的，但是它保存大量字符串时会很耗费内存（是内存）。
类似的有
前缀树(prefix tree)，后缀树(suffix tree)，radix tree(patricia tree, compact prefix tree)，crit-bit tree（解决耗费内存问题），以及前面说的double array trie。
简单的补充下我了解应用
前缀树：字符串快速检索，字符串排序，最长公共前缀，自动匹配前缀显示后缀。
后缀树：查找字符串s1在s2中，字符串s1在s2中出现的次数，字符串s1,s2最长公共部分，最长回文串。
radix tree：linux内核，nginx。
```

红黑树的介绍可以看这两篇文章：史上最清晰的红黑树讲解（上）+（下）

http://mt.sohu.com/20161014/n470317653.shtml

http://mt.sohu.com/20161018/n470610910.shtml

```
当查找树的结构发生改变时，红黑树的条件可能被破坏，需要通过调整使得查找树重新满足红黑树的条件。
调整可以分为两类：
一类是颜色调整，即改变某个节点的颜色；
另一类是结构调整，集改变检索树的结构关系。结构调整过程包含两个基本操作：左旋（Rotate Left），右旋（RotateRight）

记住，无论有多少情况，具体的调整操作只有两种：1.改变某些节点的颜色，2.对某些节点进行旋转。
```
