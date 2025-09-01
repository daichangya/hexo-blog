---
title: 【Java 面试必备】代码面试中最常考的 10 大算法类型全解析
id: 12634f39-598d-4fc4-a199-d7d39fe594e1
date: 2024-12-05 19:59:36
author: daichangya
cover: https://images.jsdiff.com/JavaInterview.jpg
excerpt: "【Java面试必备】代码面试中最常考的10大算法类型全解析 在Java程序员的求职之路上，代码面试犹如一道难以逾越的关卡，而算法知识则是通关的必备利器。今天，我们就来深入剖析那些在代码面试中最常出现的10大算法类型，助你在面试中脱颖而出！ 一、String/Array/Matrix类型 （一）核心方"
permalink: /archives/java-mian-shi-bi-bei-dai-ma-mian-shi-zhong-zui/
categories:
 - 面试指南
---

# 【Java面试必备】代码面试中最常考的10大算法类型全解析

在Java程序员的求职之路上，代码面试犹如一道难以逾越的关卡，而算法知识则是通关的必备利器。今天，我们就来深入剖析那些在代码面试中最常出现的10大算法类型，助你在面试中脱颖而出！

## 一、String/Array/Matrix类型

### （一）核心方法与技巧
在Java中，String是一个包含char数组和其他字段、方法的类。一些常用的方法如toCharArray()（获取字符串的字符数组）、Arrays.sort()（对数组进行排序）、Arrays.toString(char[] a)（将字符数组转换为字符串）、charAt(int x)（获取指定索引处的字符）、length()（字符串长度）、length（数组大小）、substring(int beginIndex)和substring(int beginIndex, int endIndex)（截取字符串）、Integer.valueOf()（字符串转整数）、String.valueOf()（整数转字符串）等，都是我们在处理String和Array时的得力助手。

### （二）经典问题与示例
1. **Evaluate Reverse Polish Notation（逆波兰表达式求值）**
   - 问题描述：给定一个逆波兰表达式（后缀表达式），计算其结果。例如，输入["2", "1", "+", "3", "*"]，输出9，因为它等价于((2 + 1) * 3)。
   - 代码示例：
```java
import java.util.Stack;

public class EvaluateReversePolishNotation {
    public int evalRPN(String[] tokens) {
        Stack<Integer> stack = new Stack<>();
        for (String token : tokens) {
            if (isOperator(token)) {
                int operand2 = stack.pop();
                int operand1 = stack.pop();
                int result = calculate(operand1, operand2, token);
                stack.push(result);
            } else {
                stack.push(Integer.parseInt(token));
            }
        }
        return stack.pop();
    }

    private boolean isOperator(String token) {
        return token.equals("+") || token.equals("-") || token.equals("*") || token.equals("/");
    }

    private int calculate(int operand1, int operand2, String operator) {
        switch (operator) {
            case "+":
                return operand1 + operand2;
            case "-":
                return operand1 - operand2;
            case "*":
                return operand1 * operand2;
            case "/":
                return operand1 / operand2;
            default:
                return 0;
        }
    }
}
```
2. **Longest Palindromic Substring（最长回文子串）**
   - 问题描述：给定一个字符串，找到其中最长的回文子串。例如，输入"babad"，输出"bab"或"aba"。
   - 代码示例（使用中心扩展法）：
```java
public class LongestPalindromicSubstring {
    public String longestPalindrome(String s) {
        if (s == null || s.length() < 1) {
            return "";
        }
        int start = 0, end = 0;
        for (int i = 0; i < s.length(); i++) {
            int len1 = expandAroundCenter(s, i, i);
            int len2 = expandAroundCenter(s, i, i + 1);
            int len = Math.max(len1, len2);
            if (len > end - start) {
                start = i - (len - 1) / 2;
                end = i + len / 2;
            }
        }
        return s.substring(start, end + 1);
    }

    private int expandAroundCenter(String s, int left, int right) {
        while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
            left--;
            right++;
        }
        return right - left - 1;
    }
}
```

## 二、链表类型

### （一）链表的基本实现
在Java中，链表的实现相对简单。每个节点包含一个值和指向下一个节点的引用。例如：
```java
class Node {
    int val;
    Node next;

    Node(int x) {
        val = x;
        next = null;
    }
}
```

### （二）常用链表操作与示例
1. **插入两个数字（链表表示的数字相加）**
   - 问题描述：给定两个用链表表示的非负整数，数字最高位位于链表开始位置，每个节点只存储一位数字，将这两个数相加并返回一个新的链表。例如，输入(2 -> 4 -> 3) + (5 -> 6 -> 4)，输出7 -> 0 -> 8，因为342 + 465 = 807。
   - 代码示例：
```java
public class AddTwoNumbers {
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        l1 = reverseList(l1);
        l2 = reverseList(l2);
        ListNode dummy = new ListNode(0);
        ListNode current = dummy;
        int carry = 0;
        while (l1!= null || l2!= null) {
            int sum = carry;
            if (l1!= null) {
                sum += l1.val;
                l1 = l1.next;
            }
            if (l2!= null) {
                sum += l2.val;
                l2 = l2.next;
            }
            current.next = new ListNode(sum % 10);
            current = current.next;
            carry = sum / 10;
        }
        if (carry > 0) {
            current.next = new ListNode(carry);
        }
        return reverseList(dummy.next);
    }

    private ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode current = head;
        while (current!= null) {
            ListNode next = current.next;
            current.next = prev;
            prev = current;
            current = next;
        }
        return prev;
    }
}
```
2. **重新排序列表**
   - 问题描述：给定一个单链表L：L0→L1→…→Ln - 1→Ln，将其重新排列为：L0→Ln→L1→Ln - 1→L2→Ln - 2→…。例如，给定链表1 -> 2 -> 3 -> 4，重新排列为1 -> 4 -> 2 -> 3。
   - 代码示例：
```java
public class ReorderList {
    public void reorderList(ListNode head) {
        if (head == null || head.next == null) {
            return;
        }
        ListNode slow = head;
        ListNode fast = head;
        while (fast.next!= null && fast.next.next!= null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        ListNode secondHalf = slow.next;
        slow.next = null;
        secondHalf = reverseList(secondHalf);
        ListNode firstHalf = head;
        while (secondHalf!= null) {
            ListNode temp1 = firstHalf.next;
            ListNode temp2 = secondHalf.next;
            firstHalf.next = secondHalf;
            secondHalf.next = temp1;
            firstHalf = temp1;
            secondHalf = temp2;
        }
    }

    private ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode current = head;
        while (current!= null) {
            ListNode next = current.next;
            current.next = prev;
            prev = current;
            current = next;
        }
        return prev;
    }
}
```

## 三、树&堆类型

### （一）二叉树的基本概念与实现
二叉树在Java中通常通过节点类来表示，每个节点包含一个值、左子节点引用和右子节点引用。例如：
```java
class TreeNode {
    int value;
    TreeNode left;
    TreeNode right;
}
```

### （二）常见二叉树算法与示例
1. **二叉树前序遍历**
   - 问题描述：按照根节点、左子树、右子树的顺序遍历二叉树。
   - 代码示例（递归实现）：
```java
public class BinaryTreePreorderTraversal {
    public List<Integer> preorderTraversal(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        preorder(root, result);
        return result;
    }

    private void preorder(TreeNode root, List<Integer> result) {
        if (root == null) {
            return;
        }
        result.add(root.value);
        preorder(root.left, result);
        preorder(root.right, result);
    }
}
```
   - 代码示例（非递归实现，使用栈）：
```java
public class BinaryTreePreorderTraversal {
    public List<Integer> preorderTraversal(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) {
            return result;
        }
        Stack<TreeNode> stack = new Stack<>();
        stack.push(root);
        while (!stack.isEmpty()) {
            TreeNode current = stack.pop();
            result.add(current.value);
            if (current.right!= null) {
                stack.push(current.right);
            }
            if (current.left!= null) {
                stack.push(current.left);
            }
        }
        return result;
    }
}
```
2. **验证二叉查找树**
   - 问题描述：给定一个二叉树，判断它是否是一个有效的二叉查找树（BST）。二叉查找树的左子树所有节点的值小于根节点的值，右子树所有节点的值大于根节点的值。
   - 代码示例：
```java
public class ValidateBinarySearchTree {
    public boolean isValidBST(TreeNode root) {
        return isValidBST(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }

    private boolean isValidBST(TreeNode root, long minVal, long maxVal) {
        if (root == null) {
            return true;
        }
        if (root.value <= minVal || root.value >= maxVal) {
            return false;
        }
        return isValidBST(root.left, minVal, root.value) && isValidBST(root.right, root.value, maxVal);
    }
}
```

### （三）堆（优先队列）的应用
堆是一种基于树的数据结构，在Java中可以使用PriorityQueue来实现。它常用于解决需要获取最大或最小元素的问题，例如任务调度（根据任务优先级执行任务）等。

## 四、Graph类型

### （一）图的基本表示与搜索算法
在Java中，图可以通过节点类和邻接表（或邻接矩阵）来表示。例如，使用邻接表表示图的节点类：
```java
class GraphNode {
    int val;
    GraphNode next;
    GraphNode[] neighbors;
    boolean visited;

    GraphNode(int x) {
        val = x;
    }

    GraphNode(int x, GraphNode[] n) {
        val = x;
        neighbors = n;
    }
}
```

### （二）深度优先搜索（DFS）与宽度优先搜索（BFS）示例
1. **深度优先搜索（DFS）示例（简单递归实现）**
   - 问题描述：从给定的起始节点开始，深度优先地遍历图。
   - 代码示例：
```java
public class GraphDFS {
    public void dfs(GraphNode root) {
        if (root == null) {
            return;
        }
        root.visited = true;
        System.out.print(root.val + " ");
        for (GraphNode neighbor : root.neighbors) {
            if (!neighbor.visited) {
                dfs(neighbor);
            }
        }
    }
}
```
2. **宽度优先搜索（BFS）示例（使用队列实现）**
   - 问题描述：从给定的起始节点开始，宽度优先地遍历图。
   - 代码示例（与原文中的BFS代码类似，但进行了一些优化和注释）：
```java
public class GraphBFS {
    public void bfs(GraphNode root) {
        if (root == null) {
            return;
        }
        Queue<GraphNode> queue = new LinkedList<>();
        root.visited = true;
        queue.add(root);
        while (!queue.isEmpty()) {
            GraphNode current = queue.poll();
            System.out.print(current.val + " ");
            for (GraphNode neighbor : current.neighbors) {
                if (!neighbor.visited) {
                    neighbor.visited = true;
                    queue.add(neighbor);
                }
            }
        }
    }
}
```

### （三）图算法的实际应用场景
图算法在许多领域都有广泛应用，如社交网络分析（寻找用户之间的关系、社区发现等）、地图导航（最短路径搜索）、网络拓扑结构分析等。

## 五、排序类型

### （一）常见排序算法概述
1. **归并排序**
   - 基本思想：采用分治策略，将数组分成两半，对每一半进行排序，然后将排序好的两半合并起来。
   - 时间复杂度：平均、最坏和最好情况下均为O(n log n)。
   - 空间复杂度：O(n)，因为在合并过程中需要额外的空间来存储临时数组。
   - 稳定性：稳定排序算法。
   - 代码示例：
```java
public class MergeSort {
    public void mergeSort(int[] arr) {
        if (arr == null || arr.length <= 1) {
            return;
        }
        int[] temp = new int[arr.length];
        mergeSort(arr, 0, arr.length - 1, temp);
    }

    private void mergeSort(int[] arr, int left, int right, int[] temp) {
        if (left < right) {
            int mid = left + (right - left) / 2;
            mergeSort(arr, left, mid, temp);
            mergeSort(arr, mid + 1, right, temp);
            merge(arr, left, mid, right, temp);
        }
    }

    private void merge(int[] arr, int left, int mid, int right, int[] temp) {
        int i = left;
        int j = mid + 1;
        int k = left;
        while (i <= mid && j <= right) {
            if (arr[i] <= arr[j]) {
                temp[k++] = arr[i++];
            } else {
                temp[k++] = arr[j++];
            }
        }
        while (i <= mid) {
            temp[k++] = arr[i++];
        }
        while (j <= right) {
            temp[k++] = arr[j++];
        }
        for (int l = left; l <= right; l++) {
            arr[l] = temp[l];
        }
    }
}
```
2. **快速排序**
   - 基本思想：选择一个基准值，将数组分为两部分，小于基准值的元素放在左边，大于基准值的元素放在右边，然后对左右两部分递归地进行排序。
   - 时间复杂度：平均情况下为O(n log n)，最坏情况下为O(n^2)（当数组已经有序或接近有序时）。
   - 空间复杂度：O(log n)，因为递归调用栈的深度为O(log n)。
   - 稳定性：不稳定排序算法。
   - 代码示例：
```java
public class QuickSort {
    public void quickSort(int[] arr) {
        if (arr == null || arr.length <= 1) {
            return;
        }
        quickSort(arr, 0, arr.length - 1);
    }

    private void quickSort(int[] arr, int left, int right) {
        if (left < right) {
            int pivotIndex = partition(arr, left, right);
            quickSort(arr, left, pivotIndex - 1);
            quickSort(arr, pivotIndex + 1, right);
        }
    }

    private int partition(int[] arr, int left, int right) {
        int pivot = arr[right];
        int i = left - 1;
        for (int j = left; j < right; j++) {
            if (arr[j] <= pivot) {
                i++;
                swap(arr, i, j);
            }
        }
        swap(arr, i + 1, right);
        return i + 1;
    }

    private void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

3. **插入排序**
   - 基本思想：将未排序元素插入到已排序部分的正确位置。
   - 时间复杂度：平均和最坏情况下为\(O(n^2)\)，最好情况下为\(O(n)\)（当数组已经有序时）。
   - 空间复杂度：\(O(1)\)，因为只需要常数级的额外空间。
   - 稳定性：稳定排序算法。
   - 代码示例：
```java
public class InsertionSort {
    public void insertionSort(int[] arr) {
        for (int i = 1; i < arr.length; i++) {
            int key = arr[i];
            int j = i - 1;
            while (j >= 0 && arr[j] > key) {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = key;
        }
    }
}
```
4. **选择排序**
   - 基本思想：每次从未排序元素中选择最小（或最大）的元素，将其放到已排序序列的末尾。
   - 时间复杂度：无论平均、最坏还是最好情况均为\(O(n^2)\)。
   - 空间复杂度：\(O(1)\)，仅需常数级额外空间。
   - 稳定性：不稳定排序算法。
   - 代码示例：
```java
public class SelectionSort {
    public void selectionSort(int[] arr) {
        for (int i = 0; i < arr.length - 1; i++) {
            int minIndex = i;
            for (int j = i + 1; j < arr.length; j++) {
                if (arr[j] < arr[minIndex]) {
                    minIndex = j;
                }
            }
            if (minIndex!= i) {
                int temp = arr[i];
                arr[i] = arr[minIndex];
                arr[minIndex] = temp;
            }
        }
    }
}
```
5. **冒泡排序**
   - 基本思想：通过多次比较相邻元素，将最大（或最小）元素逐步“冒泡”到数组末尾。
   - 时间复杂度：平均和最坏情况是\(O(n^2)\)，最好情况（数组已有序）为\(O(n)\)。
   - 空间复杂度：\(O(1)\)。
   - 稳定性：稳定排序算法。
   - 代码示例：
```java
public class BubbleSort {
    public void bubbleSort(int[] arr) {
        boolean swapped;
        for (int i = 0; i < arr.length - 1; i++) {
            swapped = false;
            for (int j = 0; j < arr.length - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                    swapped = true;
                }
            }
            if (!swapped) {
                break;
            }
        }
    }
}
```

## 六、动态规划类型

### （一）动态规划基础概念
动态规划是一种通过把原问题分解为相对简单的子问题，并保存子问题的解以避免重复计算，从而高效解决问题的算法策略。关键在于找出问题的最优子结构以及定义合适的状态转移方程。

### （二）经典动态规划示例
1. **斐波那契数列**
   - 问题描述：计算斐波那契数列的第\(n\)项，斐波那契数列定义为：\(F(0)=0\)，\(F(1)=1\)，\(F(n)=F(n - 1)+F(n - 2)\)（\(n\geq 2\)）。
   - 代码示例（普通递归实现，效率低，存在大量重复计算）：
```java
public class Fibonacci {
    public static int fibonacci(int n) {
        if (n == 0) {
            return 0;
        }
        if (n == 1) {
            return 1;
        }
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}
```
   - 代码示例（动态规划优化，使用数组保存中间结果）：
```java
public class Fibonacci {
    public static int fibonacci(int n) {
        if (n == 0) {
            return 0;
        }
        if (n == 1) {
            return 1;
        }
        int[] dp = new int[n + 1];
        dp[0] = 0;
        dp[1] = 1;
        for (int i = 2; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2];
        }
        return dp[n];
    }
}
```
2. **最长递增子序列**
   - 问题描述：给定一个整数序列，求其最长的递增子序列长度。例如，给定序列\([10, 9, 2, 5, 3, 7, 101, 18]\)，最长递增子序列是\([2, 5, 7, 101]\)，长度为\(4\)。
   - 代码示例：
```java
public class LongestIncreasingSubsequence {
    public static int lengthOfLIS(int[] nums) {
        if (nums == null || nums.length == 0) {
            return 0;
        }
        int[] dp = new int[nums.length];
        dp[0] = 1;
        int maxLen = 1;
        for (int i = 1; i < nums.length; i++) {
            dp[i] = 1;
            for (int j = 0; j < i; j++) {
                if (nums[j] < nums[i]) {
                    dp[i] = Math.max(dp[i], dp[j] + 1);
                }
            }
            maxLen = Math.max(maxLen, dp[i]);
        }
        return maxLen;
}
```

## 七、贪心算法类型

### （一）贪心算法原理
贪心算法在每一步决策时，都选择当前状态下的最优选择，而不考虑整体的最优解是否受影响。它依赖于问题具有贪心选择性质和最优子结构性质。

### （二）贪心算法实例
1. **找零问题**
   - 问题描述：假设有面额为\(1\)元、\(5\)元、\(10\)元、\(20\)元的纸币，给定要找零的金额，用最少的纸币张数给出找零方案。
   - 代码示例：
```java
public class CoinChange {
    public static int[] coinChange(int amount) {
        int[] coins = {20, 10, 5, 1};
        int[] result = new int[4];
        for (int i = 0; i < coins.length; i++) {
            result[i] = amount / coins[i];
            amount %= coins[i];
        }
        return result;
    }
}
```
2. **活动安排问题**
   - 问题描述：有一系列活动，每个活动都有开始时间和结束时间，要求在有限的时间内安排尽可能多的活动。
   - 代码示例：
```java
import java.util.Arrays;
import java.util.Comparator;

public class ActivitySelection {
    public static int activitySelection(int[][] activities) {
        Arrays.sort(activities, new Comparator<int[]>() {
            @Override
            public int compare(int[] o1, int[] o2) {
                return o1[1] - o2[1];
            }
        });
        int count = 1;
        int endTime = activities[0][1];
        for (int i = 1; i < activities.length; i++) {
            if (activities[i][0] >= endTime) {
                count++;
                endTime = activities[i][1];
            }
        }
        return count;
    }
}
```

## 八、搜索算法类型

### （一）二分搜索
1. 基本思想：针对有序数组，每次将搜索区间一分为二，根据目标值与中间元素的大小关系，确定下一步搜索区间，从而快速定位目标元素。
2. 代码示例（在有序整数数组中查找目标值）：
```java
public class BinarySearch {
    public static int binarySearch(int[] nums, int target) {
        int left = 0;
        int right = nums.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] == target) {
                return mid;
            } else if (nums[mid] > target) {
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        }
        return -1;
    }
}
```

### （二）深度优先搜索（DFS）与广度优先搜索（BFS）拓展
在之前的树和图算法中已介绍过基础的 DFS 和 BFS 实现。它们在实际应用场景极为广泛，比如在迷宫求解问题中：
 - 用 DFS 求解时，一旦选定一条路径就尽可能深入探索，直到无法继续前行才回溯，适合找所有可能路径；
 - 用 BFS 求解时，从起点开始逐层向外拓展，先找到的出口往往是最短路径，适合求最短路径问题。

## 九、回溯算法类型

### （一）回溯算法核心要点
回溯算法是一种深度优先搜索的变形，它在搜索过程中，当发现当前选择无法得到解时，就回溯到上一个状态，尝试其他选择。关键在于记录当前路径、状态，以及适时回溯调整选择。

### （二）典型回溯算法题目
1. **全排列问题**
   - 问题描述：给定一个不重复的整数序列，求其所有可能的全排列。例如，给定序列\([1, 2, 3]\)，其全排列有\([1, 2, 3]\)、\([1, 3, 2]\)、\([2, 1, 3]\)、\([2, 3, 1]\)、\([3, 1, 2]\)、\([3, 2, 1]\)。
   - 代码示例：
```java
import java.util.ArrayList;
import java.util.List;

public class Permutations {
    public static List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        backtrack(result, new ArrayList<>(), nums, new boolean[nums.length]);
        return result;
    }

    private static void backtrack(List<List<Integer>> result, List<Integer> path, int[] nums, boolean[] used) {
        if (path.size() == nums.length) {
            result.add(new ArrayList<>(path));
            return;
        }
        for (int i = 0; i < nums.length; i++) {
            if (!used[i]) {
                used[i] = true;
                path.add(nums[i]);
                backtrack(result, path, nums, used);
                used[i] = false;
                path.remove(path.size() - 1);
            }
        }
}
```
2. **N 皇后问题**
   - 问题描述：在\(N×N\)的棋盘上放置\(N\)个皇后，要求皇后之间不能相互攻击（即任意两个皇后不在同一行、同一列、同一对角线），求所有可行的放置方案。
   - 代码示例：
```java
import java.util.ArrayList;
import java.util.List;

public class NQueens {
    public static List<List<String>> solveNQueens(int n) {
        List<List<String>> result = new ArrayList<>();
        char[][] board = new char[n][n];
        for (char[] row : board) {
            Arrays.fill(row, '.');
        }
        backtrack(result, board, 0);
        return result;
    }

    private static void backtrack(List<List<String>> result, char[][] board, int row) {
        if (row == board.length) {
            List<String> solution = new ArrayList<>();
            for (char[] line : board) {
                solution.add(new String(line));
            }
            result.add(solution);
            return;
        }
        for (int col = 0; col < board.length; col++) {
            if (isValid(board, row, col)) {
                board[row][col] = 'Q';
                backtrack(result, board, row + 1);
                board[row][col] = '.';
            }
        }
    }

    private static boolean isValid(char[][] board, int row, int col) {
        for (int i = 0; i < row; i++) {
            if (board[i][col] == 'Q') {
                return false;
            }
        }
        for (int i = row - 1, j = col - 1; i >= 0 && j >= 0; i--, j--) {
            if (board[i][j] == 'Q') {
                return false;
            }
        }
        for (int i = row - 1, j = col + 1; i >= 0 && j < board.length; i--, j++) {
            if (board[i][j] == 'Q') {
                return false;
            }
        }
        return true;
    }
}
```

## 十、位运算类型

### （一）位运算基础操作
Java 中位运算包括按位与(&)、按位或(|)、按位异或(^)、取反(~)、左移(<<)、右移(>>)、无符号右移(>>> )等。这些运算可以高效地处理整数，常用于优化代码性能、节省空间，尤其在处理二进制相关问题时优势明显。

### （二）位运算应用实例
1. **判断奇偶性**
   - 利用按位与运算判断一个整数的奇偶性，比用取模运算更快。因为偶数的二进制最低位是\(0\)，奇数是\(1\)，所以\(num & 1\)如果结果为\(0\)，则\(num\)为偶数；结果为\(1\)，则\(num\)为奇数。
   - 代码示例：
```java
public class ParityCheck {
    public static boolean isEven(int num) {
        return (num & 1) == 0;
    }
}
```
2. **交换两个整数**
   - 不用额外临时变量，借助异或运算交换两个整数的值。原理是基于异或运算的特性：\(a ^ a = 0\)，\(a ^ 0 = a\)。
   - 代码示例：
```java
public class SwapTwoIntegers {
    public static void swap(int a, int b) {
        a = a ^ b;
        b = a ^ b;
        a = a ^ b;
        System.out.println("交换后 a = " + a + ", b = " + b);
    }
}
```

掌握这 10 大算法类型，无论是面对一线大厂苛刻的面试，还是日常复杂项目开发，你都能胸有成竹。不断练习、深入理解它们背后的原理，让算法不再是你的“拦路虎”，而是助你腾飞的“翅膀”。在代码世界里，用扎实的算法功底闯出一片属于自己的天地吧！要是你在学习过程中有任何疑问、心得，欢迎在评论区留言分享，咱们一起进步！ 