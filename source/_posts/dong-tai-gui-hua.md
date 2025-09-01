---
title: 动态规划
id: 1503
date: 2024-10-31 22:01:58
author: daichangya
excerpt: 动态规划问题一直是大厂面试时最频繁出现的算法题，主要原因在于此类问题灵活度高，思维难度大，没有很明显的套路做法。也正是因为这个原因，我们将持续更新此回答来尝试破解面试中所涉及的动态规划问题。首先我们主要了解动态规划是什么，动态规划问题应该如何思考？一共分成三个部分，具体内容框架如下所示：一、宝石挑选
permalink: /archives/dong-tai-gui-hua/
tags:
- 算法
---



动态规划问题一直是大厂面试时最频繁出现的算法题，主要原因在于此类问题灵活度高，思维难度大，没有很明显的套路做法。

也正是因为这个原因，我们将持续更新此回答来尝试破解面试中所涉及的动态规划问题。首先我们主要了解动态规划是什么，动态规划问题应该如何思考？

一共分成三个部分，具体内容框架如下所示：

![](https://pic2.zhimg.com/80/v2-c52955197d68993e184159c566b1646e_720w.jpg?source=1940ef5c)

## **一、宝石挑选**

### **​问题引入**

小 Q 是一个宝石爱好者。

这一天，小 Q 来到了宝石古董店，店家觉得小 Q 是个宝石行家，于是决定和小 Q 玩一个游戏。

游戏是这样的，一共有 ![[公式]](https://www.zhihu.com/equation?tex=n) 块宝石，每块宝石在小 Q 心中都有其对应的价值。注意，由于某些宝石质量过于差劲，因此存在只有店家倒贴钱，小 Q 才愿意带走的宝石，即价值可以为负数。

​小 Q 可以免费带走一个连续区间中的宝石，比如区间 ![[公式]](https://www.zhihu.com/equation?tex=%5B1%2C+3%5D) 或区间 ![[公式]](https://www.zhihu.com/equation?tex=%5B2%2C+4%5D) 中的宝石。

请问小 Q 能带走的最大价值是多少？

### **问题分析**

首先思考最暴力的解法。

枚举所有区间，暴力累加区间中宝石的价值，最后选一个价值最大的区间。时间复杂度 ![[公式]](https://www.zhihu.com/equation?tex=O%28n%5E3%29)。

![[公式]](https://www.zhihu.com/equation?tex=O%28n%5E3%29) 显然有些无法接受，因此想想有没有办法优化，比如优化掉暴力累加的部分。

### **优化 1.0**

仔细思考不难发现，我们可以枚举区间右端点，然后固定右端点，左端点不断向左移动，边移动边累加，就可以将时间复杂度优化到 ![[公式]](https://www.zhihu.com/equation?tex=O%28n%5E2%29) 。

例如我们固定右端点是 3，那么左端点就从 3 移动到 1，边移动边累加答案，就可以在移动过程中计算出区间 ![[公式]](https://www.zhihu.com/equation?tex=%5B3%2C3%5D) 、 ![[公式]](https://www.zhihu.com/equation?tex=%5B2%2C3%5D) 、 ![[公式]](https://www.zhihu.com/equation?tex=%5B1%2C3%5D+) 的答案了。因此枚举所有区间右端点，即可在 ![[公式]](https://www.zhihu.com/equation?tex=O%28n%5E2%29+) 时间复杂度内找到答案。

但是 ![[公式]](https://www.zhihu.com/equation?tex=O%28n%5E2%29+) 时间还是有些过高了，因此思考有没有办法继续优化呢？

### **优化 2.0**

观察 ![[公式]](https://www.zhihu.com/equation?tex=O%28n%5E2%29) 的解法，不难发现我们用了 ![[公式]](https://www.zhihu.com/equation?tex=O%28n%29) 的时间复杂度才求出了固定某个点为区间右端点时，区间最大价值和。

例如固定了 ![[公式]](https://www.zhihu.com/equation?tex=n+) 为区间右端点后，我们通过从 ![[公式]](https://www.zhihu.com/equation?tex=n+) 到 ![[公式]](https://www.zhihu.com/equation?tex=1) 枚举左端点，才求出了以 ![[公式]](https://www.zhihu.com/equation?tex=n) 为区间右端点时的区间最大价值和，即 ![[公式]](https://www.zhihu.com/equation?tex=+O%28n%29+) 的时间复杂度。

那么继续思考，「以 ![[公式]](https://www.zhihu.com/equation?tex=n) 为区间右端点的区间最大和」，与「以 ![[公式]](https://www.zhihu.com/equation?tex=n+-+1) 为区间右端点的区间最大和」，这两者是否有关联呢？

为了描述方便，接下来我们用 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D) 来代替「以 ![[公式]](https://www.zhihu.com/equation?tex=i) 为区间右端点的区间最大和」，用 ![[公式]](https://www.zhihu.com/equation?tex=a%5Bi%5D) 来代替第 ![[公式]](https://www.zhihu.com/equation?tex=i) 块宝石的价值。

不难发现，如果 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bn+-+1%5D+) 为正数，则 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bn%5D) 一定等于 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bn+-+1%5D+%2B+a%5Bn%5D) ；如果 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bn+-+1%5D+) 为负数，则 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bn%5D) 一定等于 ![[公式]](https://www.zhihu.com/equation?tex=a%5Bn%5D) 。因此我们可以推导出如下转移方程：

![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%3Dmax%28f%5Bi-1%5D%2Ba%5Bi%5D%2Ca%5Bi%5D%29)

根据上述转移方程，我们可以在 ![[公式]](https://www.zhihu.com/equation?tex=+O%28n%29+) 时间复杂度内求出最大的 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D) ，即将此题时间复杂度优化到 ![[公式]](https://www.zhihu.com/equation?tex=O%28n%29) ，而这个优化的过程就是「动态规划」的过程。

​在上述推导过程中，一共分为两步：

1\. 将整个问题划分为一个个子问题，并令 ![[公式]](https://www.zhihu.com/equation?tex=+f%5Bi%5D) 为第 ![[公式]](https://www.zhihu.com/equation?tex=i) 个子问题的答案

2\. 思考大规模的子问题如何从小规模的子问题推导而来，即如何由 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi+-+1%5D) 推出 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D)

这两个步骤便是「动态规划」解题思路的核心所在，即确定动态规划时的「状态」与「转移方程」。

## **二、动态规划概述**

动态规划（Dynamic Programming），因此常用 DP 指代动态规划。本块内容我们主要讲解「动态规划解题思路」与「动态规划问题类别」。

### **动态规划解题思路**

动态规划主要分为两个核心部分，一是确定「DP 状态」，二是确定「DP 转移方程」。

### **DP 状态**

「DP 状态」的确定主要有两大原则：

1.  最优子结构
2.  无后效性

### **最优子结构**

我们仍以「宝石挑选」例题来讲解这两大原则，首先是「最优子结构」。

什么是「最优子结构」？将原有问题化分为一个个子问题，即为子结构。而对于每一个子问题，其最优值均由「更小规模的子问题的最优值」推导而来，即为最优子结构。

因此「DP 状态」设置之前，需要将原有问题划分为一个个子问题，且需要确保子问题的最优值由「更小规模子问题的最优值」推出，此时子问题的最优值即为「DP 状态」的定义。

例如在「宝石挑选」例题中，原有问题是「最大连续区间和」，子问题是「以 ![[公式]](https://www.zhihu.com/equation?tex=i) 为右端点的连续区间和」。并且「以 ![[公式]](https://www.zhihu.com/equation?tex=i) 为右端点的最大连续区间和」由「以 ![[公式]](https://www.zhihu.com/equation?tex=i+-+1+) 为右端点的最大连续区间和」推出，此时后者即为更小规模的子问题，因此满足「最优子结构」原则。

由此我们才定义 DP 状态 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D+) 表示子问题的最优值，即「以 ![[公式]](https://www.zhihu.com/equation?tex=+i+) 为右端点的最大连续区间和」。

### **无后效性**

而对于「无后效性」，顾名思义，就是我们只关心子问题的最优值，不关心子问题的最优值是怎么得到的。

仍以「宝石挑选」例题为例，我们令 DP 状态 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D) 表示「以 ![[公式]](https://www.zhihu.com/equation?tex=i+) 为右端点的最大连续区间和」，我们只关心「以 ![[公式]](https://www.zhihu.com/equation?tex=i) 为右端点的区间」这个子问题的最优值，并不关心这个子问题的最优值是从哪个其它子问题转移而来。

即无论 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D) 所表示区间的左端点是什么，都不会影响后续 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi+%2B+1%5D) 的取值。影响 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi+%2B+1%5D) 取值的只有 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D) 的数值大小。

那怎样的状态定义算「有后效性」呢？

我们对「宝石挑选」例题增加一个限制，即小 Q 只能挑选长度 ![[公式]](https://www.zhihu.com/equation?tex=%5Cleq+k) 的连续区间。此时若我们定义 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D+) 表示「以 ![[公式]](https://www.zhihu.com/equation?tex=i) 为右端点的长度 ![[公式]](https://www.zhihu.com/equation?tex=%5Cleq+k) 的最大连续区间和」，则 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%2B1%5D) 的取值不仅取决于 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D) 的数值，还取决于 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D) 是如何得到的。

因为如果 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D) 取得最优值时区间长度 ![[公式]](https://www.zhihu.com/equation?tex=%3Dk) ，则 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi+%2B+1%5D) 不能从 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D+) 转移得到，即 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D+) 的状态定义有后效性。

最后概括一下，「最优子结构」就是「DP 状态最优值由更小规模的 DP 状态最优值推出」，此处 DP 状态即为子问题。而「无后效性」就是「无论 DP 状态是如何得到的，都不会影响后续 DP 状态的取值」。

### **DP 转移方程**

有了「DP 状态」之后，我们只需要用「分类讨论」的思想来枚举所有小状态向大状态转移的可能性即可推出「DP 转移方程」。

我们继续以「宝石挑选」问题为例。

在我们定义「DP 状态」 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D) 之后，我们考虑状态 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D) 如何从 ![[公式]](https://www.zhihu.com/equation?tex=f%5B1%5D%5Csim+f%5Bi-1%5D) 这些更小规模的状态转移而来。

仔细思考可以发现，由于 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D) 表示的是连续区间的和，因此其取值只与 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi-1%5D) 有关，与 ![[公式]](https://www.zhihu.com/equation?tex=f%5B1%5D%5Csim+f%5Bi-2%5D) 均无关。

我们再进一步思考， ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D) 取值只有两种情况，一是向左延伸，包含 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi-1%5D)，二是不向左延伸，仅包含 ![[公式]](https://www.zhihu.com/equation?tex=a%5Bi%5D) ，由此我们可以得到下述「DP 转移方程」：

![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%3Dmax%28f%5Bi-1%5D%2Ba%5Bi%5D%29)

注意， ![[公式]](https://www.zhihu.com/equation?tex=i%5Cin%5B1%2Cn%5D) 且 ![[公式]](https://www.zhihu.com/equation?tex=f%5B0%5D%3D0) 。

### **动态规划问题类别**

讲述完 DP 问题的解题思路后，我们来大致列举一下 DP 问题的类别。

DP 问题主要分为两大类，第一大类是 DP 类型，第二大类是 DP 优化方法。


![](https://pic2.zhimg.com/80/v2-21366d47656574b928749040c6cc1888_720w.jpg?source=1940ef5c)

其中在 DP 类型部分，面试中最常考察的就是「线性 DP」，而在优化方法部分，最常见的是「RMQ 优化」，即使用线段树或其它数据结构查询区间最小值，来优化 DP 的转移过程。

## **三、习题练习**

接下来我们以三道习题为例，来强化一下确定「DP 状态」和「DP 转移方程」的 DP 问题求解思路。

### **[面试题 08.01. 三步问题](https://link.zhihu.com/?target=https%3A//leetcode-cn.com/problems/three-steps-problem-lcci/)**

[力扣​leetcode-cn.com](https://link.zhihu.com/?target=https%3A//leetcode-cn.com/problems/three-steps-problem-lcci/)

### **题目描述**

三步问题。有个小孩正在上楼梯，楼梯有 n 阶台阶，小孩一次可以上 1 阶、2 阶或 3 阶。实现一种方法，计算小孩有多少种上楼梯的方式。结果可能很大，你需要对结果模 1000000007。

**示例 1:**

```text
输入：n = 3 
输出：4
说明: 有四种走法
```

**示例 2:**

```text
输入：n = 5
输出：13
```

**数据范围**

```text
n 范围在 [1, 1000000] 之间
```

### **解题思路**

DP 问题思路主要就是确定「DP 状态」与「DP 转移方程」，因此我们首先考虑「DP 状态」。

「DP 状态」的确定有两大原则，一是「最优子结构」，二是「无后效性」，简要概括就是将原问题划分为多个子问题，且「大规模子问题最优值」仅与「小规模子问题最优值」有关，与「小规模子问题最优值」是如何得到的无关。

此题需要求出爬 n 阶楼梯的总方案数，因此很容易想到子问题是爬 i 阶楼梯的总方案数。接下来再进一步验证该状态是否符合「最优子结构」与「无后效性」两大原则。

令 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D) 表示爬 ![[公式]](https://www.zhihu.com/equation?tex=i) 阶楼梯的总方案数，原问题被划分为了多个求最优值的子问题，继续思考，不难发现小孩爬楼梯只有三种选项，一次上 1、2、3 阶，因此 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D) 的值仅由 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi+-+1%5D) 、 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi+-+2%5D)、 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi+-+3%5D) 的值决定，因此符合「最优子结构」原则。

再进一步思考， ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D) 的取值与 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi+-+1%5D) 、 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi+-+2%5D) 、 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi+-+3%5D+) 的数值是如何得到的无关，因此符合「无后效性」原则。

确定完「DP 状态」后，我们再来确定「DP 转移方程」。

由于小孩只有三种爬楼选项，因此 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D) 的值仅由![[公式]](https://www.zhihu.com/equation?tex=f%5Bi-3%5D%5Csim+f%5Bi-1%5D)决定。且由于爬楼的最后一步不同，因此 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D) 的值由 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi-3%5D%5Csim+f%5Bi-1%5D) 累加得到，即如下所示：

![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%3D%28f%5Bi-1%5D%2Bf%5Bi-2%5D%2Bf%5Bi-3%5D%29%5C+%5C%25%5C+mod)

注意， ![[公式]](https://www.zhihu.com/equation?tex=f%5B1%5D+%3D+1) ，且转移时需要注意 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi-1%5D) 、 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi-2%5D) 、 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi-3%5D) 不要越界。

**​C++ 代码实现**

```cpp
class Solution {
public:
    vector<int> f;
    int mod = 1000000007;
    int waysToStep(int n) {
        f.resize(n+1);
        f[0] = 1;
        for(int i = 1; i <= n; i++) {
            f[i] = f[i-1];
            if(i >= 2) f[i] = (f[i] + f[i-2]) % mod;
            if(i >= 3) f[i] = (f[i] + f[i-3]) % mod;
        }
        return f[n];
    }
};

```

  

## [64\. 最小路径和](https://link.zhihu.com/?target=https%3A//leetcode-cn.com/problems/minimum-path-sum/)

[力扣​leetcode-cn.com](https://link.zhihu.com/?target=https%3A//leetcode-cn.com/problems/minimum-path-sum/)

### **题目描述**

给定一个包含非负整数的 m x n 网格，请找出一条从左上角到右下角的路径，使得路径上的数字总和为最小。

**说明：**每次只能向下或者向右移动一步。

### **示例 1:**

```cpp
输入:
[
  [1,3,1],
  [1,5,1],
  [4,2,1]
]
输出: 7
解释: 因为路径 1→3→1→1→1 的总和最小。

```

### **解题思路**

仍然是相同的解题思路，即依次确定「DP 状态」与「DP 转移方程」，且「DP 状态」的确定需要满足「最优子结构」与「无后效性」。

此题需要求出从左上角出发，到达坐标 ![[公式]](https://www.zhihu.com/equation?tex=%EF%BC%88m%2Cn%EF%BC%89) 的路径数字和最小值。因此不难想到，子问题就是从左上角出发，到达坐标 ![[公式]](https://www.zhihu.com/equation?tex=%EF%BC%88i%2Cj%EF%BC%89) 的路径数字和最小值。

令 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5Bj%5D) 表示从左上角到坐标 ![[公式]](https://www.zhihu.com/equation?tex=%EF%BC%88i%2Cj%EF%BC%89) 的路径数字和最小值，原问题即可被划分为多个求最优值的子问题，且由于每次只能向下或向右移动一步，因此 ![[公式]](https://www.zhihu.com/equation?tex=+f%5Bi%5D%5Bj%5D+) 的取值由 ![[公式]](https://www.zhihu.com/equation?tex=+f%5Bi+-+1%5D%5Bj%5D) 和 ![[公式]](https://www.zhihu.com/equation?tex=+f%5Bi%5D%5Bj+-+1%5D+) 的值决定，即符合「最优子结构原则」。

进一步验证，可以发现， ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5Bj%5D+) 的取值与 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi+-+1%5D%5Bj%5D+) 和 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5Bj+-+1%5D+) 所对应的具体路径无关，因此符合「无后效性」。

此处啰嗦一下。如果题目改为每次可以向上、下、左、右移动一步，且不能走重复的格子，则 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5Bj%5D+) 的值虽然与 ![[公式]](https://www.zhihu.com/equation?tex=+f%5Bi%5D%5Bj+-+1%5D) 、 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5Bj%2B1%5D) 、![[公式]](https://www.zhihu.com/equation?tex=f%5Bi+-+1%5D%5Bj%5D) 、 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi+%2B+1%5D%5Bj%5D) 的值有关，但由于「不能走重复的格子」这一限制， ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5Bj+-+1%5D+%EF%BD%9E+f%5Bi+%2B+1%5D%5Bj%5D) 所对应的具体路径会影响到 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5Bj%5D) 的取值，即不符合「无后效性」。

确定完「DP 状态」后，继续确定「DP 转移方程」。

由于只能向下或向右移动一步，且由于其最后一步不同，因此 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5Bj%5D) 由 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi+-+1%5D%5Bj%5D) 和 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5Bj+-+1%5D+)中的最小值转移得到，即如下所示：

![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5Bj%5D%3Dmin%28f%5Bi-1%5D%5Bj%5D%2Cf%5Bi%5D%5Bj-1%5D%29%2Bgrid%5Bi%5D%5Bj%5D)

注意， ![[公式]](https://www.zhihu.com/equation?tex=grid%5Bi%5D%5Bj%5D) 表示坐标 ![[公式]](https://www.zhihu.com/equation?tex=%EF%BC%88i%2Cj%EF%BC%89) 处的数字大小， ![[公式]](https://www.zhihu.com/equation?tex=f%5B1%5D%5B1%5D+%3D+grid%5B1%5D%5B1%5D) ，转移时需要注意不要越界。

**C++ 代码实现**

```cpp
class Solution {
public:
    int minPathSum(vector<vector<int>>& grid) {
        for(int i = 0; i < grid.size(); i++)
            for(int j = 0; j < grid[0].size(); j++) {
                if(i == 0 && j == 0) continue;
                int tp = 1e9;
                if(i > 0) tp = min(tp, grid[i-1][j]);
                if(j > 0) tp = min(tp, grid[i][j-1]);
                grid[i][j] += tp;
            }
        return grid[grid.size()-1][grid[0].size()-1];
    }
};

```

  

## [152\. 乘积最大子数组](https://link.zhihu.com/?target=https%3A//leetcode-cn.com/problems/maximum-product-subarray/)

[力扣​leetcode-cn.com](https://link.zhihu.com/?target=https%3A//leetcode-cn.com/problems/maximum-product-subarray/)

### **题目描述**

给你一个整数数组 nums ，请你找出数组中乘积最大的连续子数组（该子数组中至少包含一个数字），并返回该子数组所对应的乘积。

### **示例 1:**

```text
输入: [2,3,-2,4]
输出: 6
解释: 子数组 [2,3] 有最大乘积 6。
```

**示例 2:**

```text
输入: [-2,0,-1]
输出: 0
解释: 结果不能为 2, 因为 [-2,-1] 不是子数组。
```

### **解题思路**

继续采用相同的解题思路，即依次确定「DP 状态」与「DP 转移方程」，且「DP 状态」的确定需要满足「最优子结构」与「无后效性」。

此题其实是「宝石挑选」问题的进阶版，即连续区间最大乘积。因此与「宝石挑选」问题的思路一致，令 f\[i\] 表示以 i 为右端点的连续区间最大乘积，即可将原问题划分为多个求最优值的子问题，但这个状态定义是否符合「最优子结构」原则呢？

我们可以举一个例子来进一步思考。

例如给出 ![[公式]](https://www.zhihu.com/equation?tex=nums+%3D+%5B2%2C-1%2C-2%5D) ，根据上述 f\[i\] 的定义，我们可以得到 ![[公式]](https://www.zhihu.com/equation?tex=f+%3D+%5B2%2C-1%2C4%5D) 。不难发现 ![[公式]](https://www.zhihu.com/equation?tex=f%5B3%5D%3D4%5Cnot%3Dnums%5B3%5D%5Cnot%3Df%5B2%5D%2Anums%5B3%5D) ， ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D) 的值与 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi-1%5D) 的值无关，即 DP 状态最优值无法由更小规模的 DP 状态最优值推出，因此不符合「最优子结构」原则。

于是问题来了，怎样的状态定义才符合「最优子结构」呢？

继续思考可以发现，上述状态定义出错的原因主要在于如果 ![[公式]](https://www.zhihu.com/equation?tex=nums%5Bi%5D) 为负数，则 ![[公式]](https://www.zhihu.com/equation?tex=+f%5Bi-1%5D%2Anums%5Bi%5D) 只会越乘越小。因此我们需要根据 ![[公式]](https://www.zhihu.com/equation?tex=nums%5Bi%5D) 的正负值进行分类讨论：

*   ![[公式]](https://www.zhihu.com/equation?tex=nums%5Bi%5D%3E0)

![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%3D+max%28nums%5Bi%5D%2Cf%5Bi-1%5D%2Anums%5Bi%5D%29)

*   ![[公式]](https://www.zhihu.com/equation?tex=nums%5Bi%5D+%5Cleq+0)

![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%3D+max%28nums%5Bi%5D%2C) 「以 ![[公式]](https://www.zhihu.com/equation?tex=i-1) 为右端点的连续区间最小乘积」\* ![[公式]](https://www.zhihu.com/equation?tex=nums%5Bi%5D%29)

由此可以发现，我们需要引入新的「DP 状态」。令 ![[公式]](https://www.zhihu.com/equation?tex=maxn%5Bi%5D) 表示「以 ![[公式]](https://www.zhihu.com/equation?tex=i) 为右端点的连续区间最大乘积」， ![[公式]](https://www.zhihu.com/equation?tex=minn%5Bi%5D) 表示「以 ![[公式]](https://www.zhihu.com/equation?tex=i) 为右端点的连续区间最小乘积」。

不难发现 ![[公式]](https://www.zhihu.com/equation?tex=maxn%5Bi%5D) 、 ![[公式]](https://www.zhihu.com/equation?tex=minn%5Bi%5D) 的取值由 ![[公式]](https://www.zhihu.com/equation?tex=maxn%5Bi-1%5D) 、 ![[公式]](https://www.zhihu.com/equation?tex=minn%5Bi-1%5D) 的值推导而来，且与其具体的区间大小无关，因此同时满足「最优子结构」与「无后效性」原则。

最后我们再通过「分类讨论」即可确定如下「DP 转移方程」：

```cpp
if(nums[i] > 0) {
    maxn[i] = max(nums[i], maxn[i - 1] * nums[i]);
    minn[i] = min(nums[i], minn[i - 1] * nums[i]);
}
else {
    maxn[i] = max(nums[i], minn[i - 1] * nums[i]);
    minn[i] = min(nums[i], maxn[i - 1] * nums[i]);
}

```

总结一下，此题根据「最优子结构」原则否定了第一种状态定义。否定之后进一步观察题目性质，得到了新的「DP 状态」，并通过「分类讨论」的方式推出「DP 转移方程」，使得本题得以圆满解决。

### **C++ 代码实现**

```cpp
class Solution {
public:
    vector<int> maxn, minn;
    int maxProduct(vector<int>& nums) {
        int n = nums.size(), ans = nums[0];
        maxn.resize(n);
        minn.resize(n);
        maxn[0] = minn[0] = nums[0];
        for (int i = 1; i < nums.size(); ++i) {
            if(nums[i] > 0) {
                maxn[i] = max(nums[i], maxn[i - 1] * nums[i]);
                minn[i] = min(nums[i], minn[i - 1] * nums[i]);
            }
            else {
                maxn[i] = max(nums[i], minn[i - 1] * nums[i]);
                minn[i] = min(nums[i], maxn[i - 1] * nums[i]);
            }
            ans = max(ans, maxn[i]);
        }
        return ans;
    }
};

```

## **总结**

最后我们来总结一下 DP 问题的解题思路：

*   确定「DP 状态」
*   符合「最优子结构」原则：DP 状态最优值由更小规模的 DP 状态最优值推出
*   符合「无后效性」原则：状态的得到方式，不会影响后续其它 DP 状态取值

  

*   确定「DP 转移方程」
*   分类讨论，细心枚举

  

下面开始聚焦于常见线性 DP 模型的讲解。线性DP 是所有 DP 模型中最为常见与基础的模型，也是面试中最频繁考察的动态规划模型。

一共分成四个部分，具体内容框架如下所示：

![](https://pic2.zhimg.com/v2-e15e5f7e750aafd7c2deb1ceb5f259b7_r.jpg)


## **一、动态规划解题思路回顾**

在正式开始线性 DP 的介绍前，我们再回顾一下前面的内容。

动态规划主要分为两个核心部分，一是确定「**DP 状态**」，二是确定「**DP 转移方程**」。

「DP 状态」的确定有两大原则，一是「**最优子结构**」，二是「**无后效性**」，简要概括就是将原问题划分为多个子问题，且「大规模子问题最优值」仅与「小规模子问题最优值」有关，与「小规模子问题最优值」是如何得到的无关。

此处的「大规模」与「小规模」，就是「DP 问题」的关键所在，也是 DP 问题分类的重要标准。

确定完「DP 状态」后，只需要分类讨论、细心枚举各种情况，即可得到「DP 转移方程」。

大家在做题时，需要仔细体会每道题的「DP 状态」与「DP 转移方程」，认真考虑这两部分是通过怎样的思考得出的，才能不断加深对「动态规划」问题的理解。

## **二、线性 DP 概述**

线性划分 DP 规模的动态规划算法被统称为线性 DP。在线性 DP 中，DP 状态从「小规模」转移到「大规模」的同时， DP 状态沿着各个维度线性增长。

线性 DP 的常见分类如下，其中「最长上升子序列 LIS」、「最长公共子序列 LCS」、「数字三角形」为基础线性 DP 模型，将于本回答下一部分介绍，而「背包问题」由于种类繁多，将放到后续中讲解。


![](https://pic2.zhimg.com/v2-d1acec6a5a19547d2d4bca74641f9c57_r.jpg)

  

## **三、基础模型**

熟练掌握「动态规划」问题的基础模型对于后续的习题练习非常重要，因此对于下述的三个模型，大家需要仔细把握其思想，尤其是「DP 状态」的设立思想。

### **[300\. 最长上升子序列（LIS）](https://link.zhihu.com/?target=https%3A//leetcode-cn.com/problems/longest-increasing-subsequence/)**

[a​leetcode-cn.com](https://link.zhihu.com/?target=https%3A//leetcode-cn.com/problems/longest-increasing-subsequence/)

### **题目描述**

给定一个无序的整数数组，找到其中最长上升子序列的长度。

### **示例**​

```text
输入: [10,9,2,5,3,7,101,18]
输出: 4 
解释: 最长的上升子序列是 [2,3,7,101]，它的长度是 4。
```

  

### **模型讲解**

求一个无序数组的最长上升子序列，如果是第一次见到这样的问题，那肯定没有什么思路，这个时候我们可以减小长度，从小规模的问题着手思考。

如果长度为 1，答案等于多少？

很明显，答案也等于 1。那如果长度为 2 呢？

那我们需要考虑第二个数是否比第一个数大，如果比第一个数大，则答案为 2，否则为 1。那如果长度为 3 呢？

那我们需要枚举第三个数是否比第二个数或第一个数大，如果比它大，则可以直接从第二个数或第一个数的答案直接转移而来。因此我们可以如下制定「DP 状态」， ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D)表示仅考虑前 ![[公式]](https://www.zhihu.com/equation?tex=i)个数，以第 i 个数为结尾的最长上升子序列的最大长度。

由此我们可以推出如下转移方程：

![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%3Dmax%281%2C+f%5Bj%5D%2B1%29%2Ca%5Bj%5D%3Ca%5Bi%5D%2Cj%3Ci)

该模型「DP 状态」的关键在于固定了最后一个数字，而这样做的原因在于对于一个最长上升子序列，我们只需要关注它最后一个数字，对于其前面的数字我们并不关心。

该模型的时间复杂度为 ![[公式]](https://www.zhihu.com/equation?tex=O%28n%5E2%29)，其中 ![[公式]](https://www.zhihu.com/equation?tex=n)为数组长度。另外，该模型还可以用二分优化到 ![[公式]](https://www.zhihu.com/equation?tex=O%28nlog%28n%29%29),大家感兴趣的话可以自行了解。

  

**C++ 代码实现**

```cpp
class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        int sz = nums.size(), ans = 0;
        vector<int> f(sz, 0);
        for(int i = 0; i < sz; i++) {
            int tmp = 1;
            for(int j = i-1; j >= 0; j--) {
                if(nums[i] > nums[j])
                    tmp = max(tmp, f[j]+1);
            }  
            f[i] = tmp;
            ans = max(ans, tmp);
        }
        return ans;
    }
};

```

  

**[1143\. 最长公共子序列（LCS）](https://link.zhihu.com/?target=https%3A//leetcode-cn.com/problems/longest-common-subsequence/)**

[a​leetcode-cn.com](https://link.zhihu.com/?target=https%3A//leetcode-cn.com/problems/longest-common-subsequence/)

### **题目描述**

给定两个字符串 text1 和 text2，返回这两个字符串的最长公共子序列的长度。

一个字符串的「子序列」是指这样一个新的字符串：它是由原字符串在不改变字符的相对顺序的情况下删除某些字符（也可以不删除任何字符）后组成的新字符串。

例如，"ace" 是 "abcde" 的子序列，但 "aec" 不是 "abcde" 的子序列。两个字符串的「公共子序列」是这两个字符串所共同拥有的子序列。

若这两个字符串没有公共子序列，则返回 0。

  

**示例 1**

```text
输入：text1 = "abcde", text2 = "ace" 
输出：3  
解释：最长公共子序列是 "ace"，它的长度为 3。
```

  

**示例 2**

```text
输入：text1 = "abc", text2 = "abc"
输出：3
解释：最长公共子序列是 "abc"，它的长度为 3。

```

  

**示例 3**

```text
输入：text1 = "abc", text2 = "def"
输出：0
解释：两个字符串没有公共子序列，返回 0。
```

  

**提示**

*   ![[公式]](https://www.zhihu.com/equation?tex=1+%5Cleq+text1.length+%5Cleq+1000)
*   ![[公式]](https://www.zhihu.com/equation?tex=1+%5Cleq+text2.length+%5Cleq+1000)
*   输入的字符串只含有小写英文字符。

  

**模型讲解**

与 LIS 模型不同的是，最长公共子序列 LCS 涉及到了两个字符数组，不再是基于单数组的问题。

根据 LIS 模型「DP 状态」设置的经验，以及「线性 DP」的核心特点，即 DP 状态沿着各个维度线性增长，我们可以如下制定「DP 状态」， ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5Bj%5D)表示第一个串的前 ![[公式]](https://www.zhihu.com/equation?tex=i)个字符与第二个串的前 ![[公式]](https://www.zhihu.com/equation?tex=j)个字符的最长公共子序列长度。

该状态的转移方程没有上一个模型这么直接，因此我们需要进行分类讨论。

假如 ![[公式]](https://www.zhihu.com/equation?tex=text1%5Bi%5D+%5Cnot%3D+text2%5Bj%5D),即 ![[公式]](https://www.zhihu.com/equation?tex=text1%5Bi%5D)无法与 ![[公式]](https://www.zhihu.com/equation?tex=text2%5Bj%5D)匹配，因此 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5Bj%5D%3Dmax%28f%5Bi%5D%5Bj-1%5D%2Cf%5Bi-1%5D%5Bj%5D%29)。

假如 ![[公式]](https://www.zhihu.com/equation?tex=text1%5Bi%5D+%3D%3D+text2%5Bj%5D)，则 ![[公式]](https://www.zhihu.com/equation?tex=text1%5Bi%5D)可以与 ![[公式]](https://www.zhihu.com/equation?tex=text2%5Bj%5D)匹配，因此我们可以增加一种转移方式， ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5Bj%5D+%3D+f%5Bi-1%5D%5Bj-1%5D%2B1)。

综合上述情况，我们可以得到最终的「DP 转移方程」：

![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5Bj%5D%3D%5Cleft%5C%7B+%5Cbegin%7Baligned%7D+%26+f%5Bi-1%5D%5Bj%5D+%5C%5C+%26+f%5Bi%5D%5Bj-1%5D+%5C%5C+%26+f%5Bi-1%5D%5Bj-1%5D%2B1%2C+text1%5Bi%5D%3D%3Dtext2%5Bj%5D+%5Cend%7Baligned%7D+%5Cright.)

LCS 作为最基本的双串匹配 DP 模型，其转移方式考察较为频繁，大家需要好好把握理解。该算法时间复杂度为 ![[公式]](https://www.zhihu.com/equation?tex=O%28nm%29)， ![[公式]](https://www.zhihu.com/equation?tex=n)、 ![[公式]](https://www.zhihu.com/equation?tex=m)分别为 ![[公式]](https://www.zhihu.com/equation?tex=text1)、 ![[公式]](https://www.zhihu.com/equation?tex=text2)串的长度。

**C++ 代码实现**

```cpp
class Solution {
public:
    int longestCommonSubsequence(string text1, string text2) {
        int n = text1.length(), m = text2.length();
        vector<vector<int> > f(n+1, vector<int>(m+1, 0));
        for(int i = 1; i <= n; i++) {
            for(int j = 1; j <= m; j++) {
                f[i][j] = max(f[i-1][j], f[i][j-1]);
                if(text1[i-1] == text2[j-1])
                    f[i][j] = max(f[i][j], f[i-1][j-1]+1);
            }
        }
        return f[n][m];
    }
};

```

  

## [120\. 三角形最小路径和](https://link.zhihu.com/?target=https%3A//leetcode-cn.com/problems/triangle/)

[a​leetcode-cn.com](https://link.zhihu.com/?target=https%3A//leetcode-cn.com/problems/triangle/)

### **题目描述**

给定一个三角形，找出自顶向下的最小路径和。每一步只能移动到下一行中相邻的结点上。

相邻的结点 在这里指的是「下标」与「上一层结点下标」相同或者等于「上一层结点下标 \+ 1 」的两个结点。

例如，给定三角形：

```text
[
     [2],
    [3,4],
   [6,5,7],
  [4,1,8,3]
]
```

自顶向下的最小路径和为 11（即，2 + 3 + 5 + 1 = 11）。

### **说明**

如果你可以只使用 ![[公式]](https://www.zhihu.com/equation?tex=O%28n%29)的额外空间（​ ![[公式]](https://www.zhihu.com/equation?tex=n)为三角形的总行数）来解决这个问题，那么你的算法会很加分。

### **模型讲解**

该模型即为「线性 DP」基础模型之一：数字三角形，即最常见的二维坐标系「DP 模型」。

考虑到「线性 DP」中 DP 状态沿着各个维度线性增长的这一特点，以及本题所求的从上到下的最小路径和，不难得出状态 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5Bj%5D)表示从顶点出发到达第 ![[公式]](https://www.zhihu.com/equation?tex=i)行第 ![[公式]](https://www.zhihu.com/equation?tex=j)列这个点时的最小路径和。

由于题目中限制 ![[公式]](https://www.zhihu.com/equation?tex=%28i%2Cj%29)只能由 ![[公式]](https://www.zhihu.com/equation?tex=%28i-1%2Cj-1%29)和 ![[公式]](https://www.zhihu.com/equation?tex=%28i-1%2Cj%29)两个点到达，因此我们可以得到如下「DP 转移方程」：

![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5Bj%5D%3Dtriangle%5Bi%5D%5Bj%5D%2Bmin%28f%5Bi-1%5D%5Bj-1%5D%2Cf%5Bi-1%5D%5Bj%5D%29)

书写代码时需要注意边界的处理，如对于特定的 ![[公式]](https://www.zhihu.com/equation?tex=%28i%2Cj%29)来说，数字三角形中不存在 ![[公式]](https://www.zhihu.com/equation?tex=%28i-1%2Cj-1%29)或 ![[公式]](https://www.zhihu.com/equation?tex=%28i-1%2Cj%29)。

该模型的重要意义在于告诉了我们二维坐标系中也是可以进行「线性 DP」的，而且我们可以直接根据坐标点设置「DP 状态」。

### **C++ 代码实现**

```cpp
class Solution {
public:
    int minimumTotal(vector<vector<int>>& triangle) {
        int n = triangle.size(), ans = 1e9;
        vector<vector<int> > f(n+1, vector<int>(n+1, 0));
        for(int i = 0; i < n; i++) {
            for(int j = 0; j < triangle[i].size(); j++) {
                if(j == triangle[i].size()-1)
                    f[i+1][j+1] = triangle[i][j] + f[i][j];
                else if(j == 0)
                    f[i+1][j+1] = triangle[i][j] + f[i][j+1];
                else
                    f[i+1][j+1] = triangle[i][j] + min(f[i][j+1], f[i][j]);
                if(i == n-1)
                    ans = min(ans, f[i+1][j+1]);
            }
        }
        return ans;
    }
};

```

### **滚动数组优化**

上述「DP 转移方程」的时间复杂度为 ![[公式]](https://www.zhihu.com/equation?tex=O%28n%5E2%29)，空间复杂度也为 ![[公式]](https://www.zhihu.com/equation?tex=O%28n%5E2%29)，但根据题目中的提示，本题是可以优化至 ![[公式]](https://www.zhihu.com/equation?tex=O%28n%29)空间复杂度的。

这种优化方法称为「滚动数组优化」，在「DP 问题」中非常常见，主要适用于 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5Bj%5D)仅由 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi-1%5D%5Bk%5D)转移而来的情况。

例如在本题中，「DP 转移方程」如下：

![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5Bj%5D%3Dtriangle%5Bi%5D%5Bj%5D%2Bmin%28f%5Bi-1%5D%5Bj-1%5D%2Cf%5Bi-1%5D%5Bj%5D%29)

不难发现， ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5Bj%5D)仅由 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi-1%5D%5Bj-1%5D)和 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi-1%5D%5Bj%5D)所决定，因此对于一个固定的 ![[公式]](https://www.zhihu.com/equation?tex=i)，我们可以从 ![[公式]](https://www.zhihu.com/equation?tex=n)到 1 倒序枚举 ![[公式]](https://www.zhihu.com/equation?tex=j)，由此可以优化至如下转移方程：

![[公式]](https://www.zhihu.com/equation?tex=f%5Bj%5D%3Dtriangle%5Bi%5D%5Bj%5D%2Bmin%28f%5Bj-1%5D%2Cf%5Bj%5D%29)

代码形式如下所示：（未进行边界处理，仅作为转移示例）

```cpp
for(int i = 0; i < n; i++) {
    for(int j = triangle[i].size()-1; j >= 0; j--) {
        f[j] = triangle[i][j] + min(f[j-1], f[j]);
    }
}

```

在上述代码中我们可以发现，在更新 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bj%5D)时， ![[公式]](https://www.zhihu.com/equation?tex=f%5Bj-1%5D)与 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bj%5D)并未更新，此时的 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bj-1%5D)与 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bj%5D)其实是 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi-1%5D%5Bj-1%5D)和 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi-1%5D%5Bj%5D)的值，因此这种转移方式正确。

经过滚动数组优化后，该算法的空间复杂度为 ![[公式]](https://www.zhihu.com/equation?tex=O%28n%29),时间复杂度不变，仍为 ![[公式]](https://www.zhihu.com/equation?tex=O%28n%5E2%29)。

  

**滚动数组完整代码**

```cpp
class Solution {
public:
    int minimumTotal(vector<vector<int>>& triangle) {
        int n = triangle.size(), ans = 1e9;
        vector<int> f(n+1, 0);
        for(int i = 0; i < n; i++) {
            for(int j = triangle[i].size()-1; j >= 0; j--) {
                if(j == triangle[i].size()-1)
                    f[j+1] = triangle[i][j] + f[j];
                else if(j == 0)
                    f[j+1] = triangle[i][j] + f[j+1];
                else
                    f[j+1] = triangle[i][j] + min(f[j+1], f[j]);
                if(i == n-1)
                    ans = min(ans, f[j+1]);
            }
        }
        return ans;
    }
};

```

  

## **四、习题练习**

了解完三个常见的「线性 DP」模型后，我们来进行适当的习题练习。对于下述习题，大家需要仔细关注三点：

1.  如何识别这是一道「线性 DP」问题
2.  「DP 状态」是如何设置的
3.  如何根据「DP 状态」得到「DP 转移方程」

### **[198\. 打家劫舍](https://link.zhihu.com/?target=https%3A//leetcode-cn.com/problems/house-robber/)**

[a​leetcode-cn.com](https://link.zhihu.com/?target=https%3A//leetcode-cn.com/problems/house-robber/)

### **题目描述**

你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警。

给定一个代表每个房屋存放金额的非负整数数组，计算你「不触动警报装置的情况下」，一夜之内能够偷窃到的最高金额。

**示例 1**

```text
输入：[1,2,3,1]
输出：4
解释：偷窃 1 号房屋 (金额 = 1) ，然后偷窃 3 号房屋 (金额 = 3)。
     偷窃到的最高金额 = 1 + 3 = 4 。
```

  

**示例 2**

```text
输入：[2,7,9,3,1]
输出：12
解释：偷窃 1 号房屋 (金额 = 2), 偷窃 3 号房屋 (金额 = 9)，接着偷窃 5 号房屋 (金额 = 1)。
     偷窃到的最高金额 = 2 + 9 + 1 = 12 。
```

  

**提示**

*   ![[公式]](https://www.zhihu.com/equation?tex=0+%5Cleq+nums.length+%5Cleq+100)
*   ![[公式]](https://www.zhihu.com/equation?tex=0+%5Cleq+nums%5Bi%5D+%5Cleq+400)

### **解题思路**

首先我们简要概括一下题意，即不能同时偷窃相邻两间房屋，求偷窃的最大金额。

不难发现，偷窃的过程是线性增长的，即从左到右，沿街依次偷窃，非常符合「线性 DP」的特征，因此我们可以令 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D)表示前 ![[公式]](https://www.zhihu.com/equation?tex=i)间房屋能偷窃到的最高金额，由此得到如下「DP 转移方程」：

![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D+%3D+max%28f%5Bi-1%5D%2C+nums%5Bi%5D%2Bf%5Bi-2%5D%29)

其中 ![[公式]](https://www.zhihu.com/equation?tex=nums%5Bi%5D)表示第 ![[公式]](https://www.zhihu.com/equation?tex=i)间房屋的金额。

回顾一下之前的最长上升子序列（LIS)，我们令 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D)表示以第 ![[公式]](https://www.zhihu.com/equation?tex=i)个数为结尾的最长上升子序列的最大长度，因为最长上升子序列在转移时我们需要知道最后一个数的大小。

仿照 LIS 的「DP 状态」，我们也可以令 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D)表示前 ![[公式]](https://www.zhihu.com/equation?tex=i)间房屋能偷窃到的最高金额，且第 ![[公式]](https://www.zhihu.com/equation?tex=i)间房屋被偷窃。这样的「DP 状态」也是可以解决本题的，但需要修改「DP 转移方程」，大家可以自行思考并进行尝试。

**C++ 代码实现**

```cpp
class Solution {
public:
    int rob(vector<int>& nums) {
        int n = nums.size();
        if(n == 0) return 0;
        vector<int> f(n, 0);
        for(int i = 0; i < n; i++) {
            f[i] = nums[i];
            if(i >= 2) f[i] = max(f[i], f[i-2]+nums[i]);
            if(i >= 1) f[i] = max(f[i], f[i-1]);
        }
        return f[n-1];
    }
};

```

  

## [354\. 俄罗斯套娃信封问题](https://link.zhihu.com/?target=https%3A//leetcode-cn.com/problems/russian-doll-envelopes/)

[a​leetcode-cn.com](https://link.zhihu.com/?target=https%3A//leetcode-cn.com/problems/russian-doll-envelopes/)

### **题目描述**

给定一些标记了宽度和高度的信封，宽度和高度以整数对形式 (w, h) 出现。当另一个信封的宽度和高度都比这个信封大的时候，这个信封就可以放进另一个信封里，如同俄罗斯套娃一样。

请计算最多能有多少个信封能组成一组“俄罗斯套娃”信封（即可以把一个信封放到另一个信封里面）。

### **说明**

不允许旋转信封。

### **示例**

```text
输入: envelopes = [[5,4],[6,4],[6,7],[2,3]]
输出: 3 
解释: 最多信封的个数为 3, 组合为: [2,3] => [5,4] => [6,7]。
```

### **解题思路**

简要概括题意，求一组二维上升子序列 ![[公式]](https://www.zhihu.com/equation?tex=p1%2Cp2%2C...%2Cpm)，同时满足：

![[公式]](https://www.zhihu.com/equation?tex=w_%7Bp1%7D%3Cw_%7Bp2%7D%3C...%3Cw_%7Bpm%7D+%5C%5C+h_%7Bp1%7D%3Ch_%7Bp2%7D%3C...%3Ch_%7Bpm%7D+%5C%5C)

在之前的最长上升子序列（LIS）问题中，我们令 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D)表示以第 ![[公式]](https://www.zhihu.com/equation?tex=i)个数为结尾的最长上升子序列的最大长度，即该「DP 状态」只能作用于一维 LIS。

而本题为二维 LIS，若令 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5Bj%5D)表示以 ![[公式]](https://www.zhihu.com/equation?tex=w%3Di%2Ch%3Dj)的信封为结尾的最长上升子序列显然不太合适，因此我们需要先控制一维，然后在另一维上进行「DP 转移」。

先控制一维，使得「DP 转移」时满足 ![[公式]](https://www.zhihu.com/equation?tex=i+%3C+j)，则 ![[公式]](https://www.zhihu.com/equation?tex=w_i%5Cleq+w_j)，因此我们可以先对于信封进行排序， ![[公式]](https://www.zhihu.com/equation?tex=w)为第一关键字， ![[公式]](https://www.zhihu.com/equation?tex=h)为第二关键字，排完序后再进行初始的一维 LIS「DP 转移」。

因此我们排完序后，令 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D)表示以第 ![[公式]](https://www.zhihu.com/equation?tex=%28w_i%2Ch_i%29)为结尾的最长上升子序列，「DP 转移方程」如下：

![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%3Dmax%281%2Cf%5Bj%5D%2B1%29%2C+j%3Ci%2C+h_j%3Ch_i+%2Cw_j%3Cw_i)

由此我们将本问题转化成了基础的 LIS 问题，具体代码如下所示。

### **C++ 代码实现**

```cpp
class Solution {
public:
    int maxEnvelopes(vector<vector<int>>& envelopes) {
        sort(envelopes.begin(), envelopes.end());
        int n = envelopes.size(), ans = 0;
        vector<int> f(n, 0);
        for(int i = 0; i < n; i++) {
            int tmp = 0;
            for(int j = 0; j < i; j++) {
                if(envelopes[j][1] < envelopes[i][1] && envelopes[j][0] < envelopes[i][0])
                    tmp = max(tmp, f[j]);
            }
            f[i] = tmp + 1;
            ans = max(f[i], ans);
        }
        return ans;
    }
};

```

  

## [72\. 编辑距离](https://link.zhihu.com/?target=https%3A//leetcode-cn.com/problems/edit-distance/)

[a​leetcode-cn.com](https://link.zhihu.com/?target=https%3A//leetcode-cn.com/problems/edit-distance/)

### **题目描述**

给你两个单词「word1」和「word2」，请你计算出将「word1」转换成「word2」所使用的最少操作数。

你可以对一个单词进行如下三种操作：

1.  插入一个字符
2.  删除一个字符
3.  替换一个字符

**示例 1**

```text
输入：word1 = "horse", word2 = "ros"
输出：3
解释：
horse -> rorse (将 'h' 替换为 'r')
rorse -> rose (删除 'r')
rose -> ros (删除 'e')
```

  

**示例 2**

```text
输入：word1 = "intention", word2 = "execution"
输出：5
解释：
intention -> inention (删除 't')
inention -> enention (将 'i' 替换为 'e')
enention -> exention (将 'n' 替换为 'x')
exention -> exection (将 'n' 替换为 'c')
exection -> execution (插入 'u')
```

  

### **解题思路**

简要概括题意，使用最少的操作使得「word1」与「word2」相同。很明显所要进行的操作是从左至右线性增长的，不难联想到最长公共子序列（LCS），因此我们令 ![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5Bj%5D)表示最少的操作使得 「word1」的前 ![[公式]](https://www.zhihu.com/equation?tex=i)个字符与「word2」的前 ![[公式]](https://www.zhihu.com/equation?tex=j+)个字符相同。

与 LCS 的思考过程一致，假如 ![[公式]](https://www.zhihu.com/equation?tex=word1%5Bi%5D%5Cnot%3D+word2%5Bj%5D)，则必定涉及删除或增加：

![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5Bj%5D%3Dmin%28f%5Bi-1%5D%5Bj%5D%2Cf%5Bi%5D%5Bj-1%5D%29%2B1)

假如 ![[公式]](https://www.zhihu.com/equation?tex=word1%5Bi%5D%3D%3Dword2%5Bj%5D)，则需要在原先基础上增加一种转移方式：

![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5Bj%5D%3Dmin%28f%5Bi-1%5D%5Bj-1%5D%2C+min%28f%5Bi-1%5D%5Bj%5D%2Cf%5Bi%5D%5Bj-1%5D%29%2B1%29)

最后我们需要控制一下边界：

![[公式]](https://www.zhihu.com/equation?tex=f%5Bi%5D%5B0%5D%3Di%2Cf%5B0%5D%5Bj%5D%3Dj%2C1%5Cleq+i%5Cleq+word1.length%28%29%2C1%5Cleq+j%5Cleq+word2.length%28%29)

  

**C++ 代码实现**

```cpp
class Solution {
public:
    int minDistance(string word1, string word2) {
        int n = word1.length(), m = word2.length();
        vector<vector<int> > f(n+1, vector<int>(m+1, 0));
        for(int i = 1; i <= n; i++) f[i][0] = i;
        for(int j = 1; j <= m; j++) f[0][j] = j;
        for(int i = 1; i <= n; i++) {
            for(int j = 1; j <= m; j++) {
                if(word1[i-1] == word2[j-1]) f[i][j] = f[i-1][j-1];
                else f[i][j] = min(f[i-1][j-1]+1, min(f[i][j-1]+1, f[i-1][j]+1));
            }
        }
        return f[n][m];
    }
};

```

  

## **总结**

上述习题练习的后两道，「俄罗斯套娃信封问题」与「编辑距离」在力扣上的难度均为困难，但做完题后不难发现其本质仍然是基础线性 DP 模型「LIS」与「LCS」的变形。事实上，大部分「线性 DP」问题（不涉及背包）都可以在最初介绍的三个基础模型「LIS」、「LCS」、「数字三角形」中找到类似的解题思路，因此大家需要熟练掌握。

为了方便大家后续查阅，我们将三个模型总结如下：

![](https://pic1.zhimg.com/80/v2-43b95486d78778ed5b47159ba562f678_720w.jpg?source=1940ef5c)

注意，上述「DP 转移方程」均未包含边界控制，大家写题时需要注意。

最后，希望大家在求解「线性 DP」问题时可以回忆起上述三个基础模型，参考其「DP 思想」。