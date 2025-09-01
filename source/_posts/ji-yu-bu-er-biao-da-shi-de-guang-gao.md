---
title: 基于布尔表达式的广告索引设计
id: 1516
date: 2024-10-31 22:01:59
author: daichangya
permalink: /archives/ji-yu-bu-er-biao-da-shi-de-guang-gao/
categories:
- 广告
---


## **问题背景**

广告主在广告投放平台勾选定向条件之后，当用户发起一个请求之后，需要广告引擎快速筛选出符合定向条件的广告。我们当然可以想到如下的代码结构:

```java
    Attributes = list<Attribute> // 用户的流量标签,例如:用户的年龄、性别...
    for (Ad ad : ads) {
        check attributes for each ad. // 对于每一个广告检查是不是符合流量标签,挑选广告.
    }
```

但是这样的问题是随着广告的数量增长而增长的，显然不能满足业务发展需要。无论是在品牌广告，还是竞价广告中，该问题都会遇到。很自然的，我们想到建索引，那么**索引结构如何设计就成为问题的关键**。

## **索引结构**


![](https://pic2.zhimg.com/80/v2-afb265730db94f398da5c52acb62cced_720w.jpg)

两层索引结构

为了说明两层索引结构，我们定义如下术语：

*   Attribute。单个流量标签，包含两个信息：属性类别和属性取值。如：*`AGE: 5`*
*   Assignment。多个流量标签组成的用户画像。如：*`AGE: 5，GENDER: 1，NETWORK: 1`*
*   Conjunction。布尔表达式的合取范式。如：*`AGE ∈ (4,5,6) ∧ GENDER ∈ (1）`*
*   Predicate。布尔表达式的一个子表达式。如：*`AGE ∈ (4,5,6)，GENDER ∈ (1）`*

两层索引设计的主要思想是：从Assignment 找出**包含**这些流量标签的Conjunction，**筛选满足条件的Conjunction**，根据筛选出的Conjunction，找出满足条件的广告集合。下面我们举个例子:

假设线上有7个广告，它们定向条件如下，其中A3和Ad7定向条件相同。Ad6包含反向定向，即该广告不能出在AppInterest的标签为（19-1）的用户上面。

```java
Ad1定向：PlacementType∈(2)
Ad2定向：PlacementType∈(2) ∧ AppInterest∈(15-0, 19-1) ∧ InstalledApp∈(30202)
Ad3定向：PlacementType∈(2) ∧ AppInterest∈(15-0, 19-1) ∧ NetworkType∈(1)
Ad4定向：PlacementType∈(2) ∧ AppInterest∈(19-1)
Ad5定向：PlacementType∈(2) ∧ InstalledApp∈(30202) ∧ NetworkType∈(1)
Ad6定向：PlacementType∈(2) ∧ IpGeo∈(141) ∧ NetworkType∈(1) ∧ AppInterest∉(19-1)
Ad7定向：PlacementType∈(2) ∧ AppInterest∈(15-0, 19-1) ∧ NetworkType∈(1)
```

对应定向条件有6个Conjuntion，可编号Conjuntion如下:

```cpp
conjunctionId	conjunction	size
1	PlacementType∈(2)	1
2	PlacementType∈(2) ∧ AppInterest∈(19-1)	2
3	PlacementType∈(2) ∧ IpGeo∈(141) ∧ NetworkType∈(1) ∧ AppInterest∉(19-1) 	3
4	PlacementType∈(2) ∧ InstalledApp∈(30202) ∧ NetworkType∈(1)	3
5	PlacementType∈(2) ∧ AppInterest∈(15-0, 19-1) ∧ InstalledApp∈(30202)	3
6	PlacementType∈(2) ∧ AppInterest∈(15-0, 19-1) ∧ NetworkType∈(1)	3           

```

其中，conjunctionId为编号，conjunction为布尔表达式内容，size为∈语句的个数。

可以建立conjunctionId到Ad的索引如下：

```text
conjunction1 -> Ad1
conjunction2 -> Ad4
conjunction3 -> Ad6
conjunction4 -> Ad5
conjunction5 -> Ad2
conjunction6 -> Ad3,Ad7
```

流量标签到布尔表达式的索引如下:


![](https://pic2.zhimg.com/80/v2-c583b64ab41abddc05d84c4ac8e93295_720w.jpg)

流量标签到布尔表达式索引

如上图，建立K-Index

*   K 代表Conjuntion的size大小
*   PostingList代表包含/不包含这个Attribute的Conjuntion

## **算法原理**

我们还是按照上面的例子说明，最后给出核心算法的伪代码。现在来了一个用户画像Assignment：

```text
PlacementType:2
AppInterest:19-1
NetworkType:1
```

由于有三个流量标签，那么我们满足条件的只可能是1-Index, 2-Index,3-Index。这就是为什么上面建索引的时候需要建立一个K-Index的索引，加上K-Index可以根据数目进行算法剪枝。同时每一个PostingList中的Conjuntion都已按照ConjuntionId升序排列。我们以检测3-Index为例。根据Assignment可以从索引里面取到如Conjuntions：

```java
PlacementType: 2      (3, ∈), (4, ∈), (5, ∈), (6, ∈)
AppInterest: 19-1     (3, ∉), (5, ∈), (6, ∈)
NetworkType: 1	      (3, ∈), (4, ∈), (6, ∈)
```

**需要判断当前最小的ConjuntionId至少出现在3个PostingList中，且不能出现∉的关系。**

每次check完成之后按照conjuntionId重排序(方便检测是不是至少出现在3个PostingList中)。

```java
PlacementType: 2      (3, ∈), (4, ∈), (5, ∈), (6, ∈)
AppInterest: 19-1     (3, ∉), (5, ∈), (6, ∈)
NetworkType: 1	      (3, ∈), (4, ∈), (6, ∈)
-------------------------------------------------------
MatchedConjuntion = [] (check Conjuntion3，发现出现了∉，故不满足)


PlacementType: 2      (4, ∈), (5, ∈), (6, ∈)
NetworkType: 1	      (4, ∈), (6, ∈)
AppInterest: 19-1     (5, ∈), (6, ∈)
-------------------------------------------------------
MatchedConjuntion = [] (check Conjuntion4，发现出现只出现在两个中，故不满足)


PlacementType: 2      (5, ∈), (6, ∈)
AppInterest: 19-1     (5, ∈), (6, ∈)
NetworkType: 1	      (6, ∈)
-------------------------------------------------------
MatchedConjuntion = [] (check Conjuntion5，发现出现只出现在两个中，故不满足)


PlacementType: 2      (6, ∈)
AppInterest: 19-1     (6, ∈)
NetworkType: 1	      (6, ∈)
-------------------------------------------------------
MatchedConjuntion = [6] (check Conjuntion6，至少出现在三个中，且没有∉关系，满足)
```

按照该算法继续检测2-Index、1-Index。得到最终结果: MatchedConjuntion =\[1,2,6\]。再根据MatchedConjuntion 检索出广告 MatchedAds = \[Ad1, Ad4, Ad3,Ad7\]。

## **算法伪代码**

c++版本可以参考《计算广告》 P225.

## **维度爆炸问题**

有的同学觉得这里会出现维度爆炸的问题，比如有50个兴趣标签，5个年龄段标签，2个性格标签。最极端的情况是可能会出现：

```text
50 * 5 * 2 * ... = 100 * ...
```

随着定向维度的增加而爆炸，实际上并不会，因为定向维度是取决于广告的规模的，最极端情况，假设我们线上有100w的广告，且这100w的广告定向标签都不一样，那么问题规模也是100w，并不会出现维度爆炸。另外，实际上，线上大量广告的定向标签是重复的，100w的广告定向的Conjuntion，远远小于广告数量。

## 用ES可以做吗？

这篇文章发出去之后，虽然点赞数寥寥无几，但是私信我的人蛮多。在这里提供另一种思路，如果你的公司是一个小公司，也没必要自己因为性能造轮子，直接使用es进行索引即可。es检索的dsl条件的伪代码如下：

```text
[（不存在性别定向）|| （存在性别定向且满足条件）]  
&&  [（不存在年龄定向）|| （存在年龄定向且满足条件）]
&&  [（不存在标签定向）|| （存在标签定向且满足条件）]
...
```

这样就可以把通投的（无任何定向）广告和有定向且满足条件的广告检索出来。

例如：请求是：26岁的男性用户，那么实际的es的dsl为：

```text
{
  "must": [
    {
      "bool": {
        "should": [
          {
            "bool": {
              "must_not": {
                "exists": {
                  "field": "age"
                }
              }
            }
          },
          {
            "bool": {
              "should": [
                {
                  "range": {
                    "age.min": {
                      "from": null,
                      "to": 26,
                      "include_lower": true,
                      "include_upper": true
                    }
                  }
                },
                {
                  "range": {
                     "age.max": {
                          "from": 26,
                          "to": null,
                          "include_lower": true,
                          "include_upper": true
                     }
                   }
                }
              ]
            }
          }
        ]
      }
    },
    {
      "bool": {
        "should": [
          {
            "bool": {
              "must_not": {
                "exists": {
                  "field": "gender"
                }
              }
            }
          },
          {
            "term": {
              "gender": "男"
            }
          }
        ]
      }
    }
  ]
}
```

## **参考资料**

*   [http://theory.stanford.edu/~sergei/papers/vldb09-indexing.pdf](https://link.zhihu.com/?target=http%3A//theory.stanford.edu/~sergei/papers/vldb09-indexing.pdf)
*   [https://pdfs.semanticscholar.org/28d5/eae010074ea82a635e9c36d5a420dba949fa.pdf](https://link.zhihu.com/?target=https%3A//pdfs.semanticscholar.org/28d5/eae010074ea82a635e9c36d5a420dba949fa.pdf)  
    [https://book.douban.com/subject/26596778/](https://link.zhihu.com/?target=https%3A//book.douban.com/subject/26596778/)