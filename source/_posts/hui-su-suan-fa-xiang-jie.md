---
title: 回溯算法详解
id: 32c92e37-712c-44fe-95f8-cc6d026e7b93
date: 2025-07-01 15:48:18
author: daichangya
excerpt: 回溯算法是一种通过深度优先搜索（DFS）的方式来遍历问题的所有可能解空间，以找到满足特定条件的解的算法策略。在搜索过程中，当发现当前的选择无法得到有效的解时，算法会“回溯”到上一步，撤销当前的选择，然后尝试其他可能的选择，直到找到所有符合条件的解或者遍历完整个解空间。
  基本思想 回溯算法的核心思想可
permalink: /archives/hui-su-suan-fa-xiang-jie/
categories:
- suan-fa
---

回溯算法是一种通过深度优先搜索（DFS）的方式来遍历问题的所有可能解空间，以找到满足特定条件的解的算法策略。在搜索过程中，当发现当前的选择无法得到有效的解时，算法会“回溯”到上一步，撤销当前的选择，然后尝试其他可能的选择，直到找到所有符合条件的解或者遍历完整个解空间。

### 基本思想
回溯算法的核心思想可以概括为“尝试所有可能，不行就回头”。具体步骤如下：
1. **选择**：在每一步中，从所有可能的选择中做出一个选择。
2. **递归**：在做出选择后，递归地继续处理剩余的问题。
3. **撤销选择**：如果当前的选择无法得到有效的解，撤销这个选择，回到上一步，尝试其他的选择。

### 适用场景
回溯算法适用于以下类型的问题：
- **组合问题**：从给定的元素集合中选取若干个元素，组成满足特定条件的组合。例如，从 `n` 个不同元素中选取 `k` 个元素的所有组合。
- **排列问题**：对给定的元素集合进行全排列，找出所有可能的排列方式。例如，生成 `n` 个不同元素的全排列。
- **子集问题**：找出给定元素集合的所有子集。
- **棋盘问题**：如八皇后问题，在一个 `8×8` 的棋盘上放置八个皇后，使得它们互不攻击。
- **路径搜索问题**：在图或迷宫中寻找满足特定条件的路径。

### 算法框架
回溯算法的一般代码框架如下：
```java
// 用于存储最终结果
List<SolutionType> result = new ArrayList<>();

public void backtrack(路径, 选择列表) {
    if (满足结束条件) {
        result.add(路径);
        return;
    }
    for (选择 : 选择列表) {
        // 做选择
        路径.add(选择);
        // 进入下一层决策树
        backtrack(路径, 新的选择列表);
        // 撤销选择
        路径.remove(选择);
    }
}
```
### 示例分析

#### 全排列问题
给定一个不含重复数字的数组 `nums`，返回其所有可能的全排列。

```java
import java.util.ArrayList;
import java.util.List;

public class Permutations {
    // 存储最终结果
    List<List<Integer>> result = new ArrayList<>();

    public List<List<Integer>> permute(int[] nums) {
        // 用于存储当前排列
        List<Integer> path = new ArrayList<>();
        // 标记元素是否已经使用
        boolean[] used = new boolean[nums.length];
        backtrack(nums, path, used);
        return result;
    }

    private void backtrack(int[] nums, List<Integer> path, boolean[] used) {
        // 满足结束条件：当前排列的长度等于数组的长度
        if (path.size() == nums.length) {
            result.add(new ArrayList<>(path));
            return;
        }
        for (int i = 0; i < nums.length; i++) {
            // 如果元素已经使用过，则跳过
            if (used[i]) continue;
            // 做选择
            path.add(nums[i]);
            used[i] = true;
            // 进入下一层决策树
            backtrack(nums, path, used);
            // 撤销选择
            path.remove(path.size() - 1);
            used[i] = false;
        }
    }

    public static void main(String[] args) {
        Permutations permutations = new Permutations();
        int[] nums = {1, 2, 3};
        List<List<Integer>> result = permutations.permute(nums);
        for (List<Integer> permutation : result) {
            System.out.println(permutation);
        }
    }
}
```
#### 代码解释
- **`result`**：用于存储最终的全排列结果。
- **`path`**：用于存储当前正在构建的排列。
- **`used`**：一个布尔数组，用于标记数组中的元素是否已经在当前排列中使用过。
- **`backtrack` 方法**：
  - 当 `path` 的长度等于数组的长度时，说明已经得到一个完整的排列，将其添加到 `result` 中。
  - 遍历数组中的每个元素，如果该元素未被使用，则将其添加到 `path` 中，并标记为已使用，然后递归调用 `backtrack` 方法。
  - 递归返回后，撤销当前的选择，将元素从 `path` 中移除，并标记为未使用。

### 复杂度分析
- **时间复杂度**：回溯算法的时间复杂度通常是指数级的，因为它需要遍历所有可能的解空间。对于全排列问题，时间复杂度为 $O(n!)$，其中 $n$ 是数组的长度。
- **空间复杂度**：主要用于存储路径和递归调用栈的空间，空间复杂度为 $O(n)$，其中 $n$ 是数组的长度。