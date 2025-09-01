---
title: Java实现对二叉树前序/中序/后序的递归与非递归算法
id: 1199
date: 2024-10-31 22:01:50
author: daichangya
excerpt: "二叉树的前序、中序、后序遍历的定义：前序遍历：对任一子树，先访问跟，然后遍历其左子树，最后遍历其右子树；中序遍历：对任一子树，先遍历其左子树，然后访问根，最后遍历其右子树；后序遍历：对任一子树，先遍历其左子树，然后遍历其右子树，最后访问根。首先创建节点类，并在里面添加了一个创建树的方法，调用后就可以返回一个包含7个节点的二叉树。点击(此处)折叠或打开"
permalink: /archives/javashi-xian-dui-er-cha-shu-qian-xu-zhong-xu/
tags: 
 - 算法
---

 

二叉树的前序、中序、后序遍历的定义：  
前序遍历：对任一子树，先访问跟，然后遍历其左子树，最后遍历其右子树；  
中序遍历：对任一子树，先遍历其左子树，然后访问根，最后遍历其右子树；  

后序遍历：对任一子树，先遍历其左子树，然后遍历其右子树，最后访问根。

首先创建节点类，并在里面添加了一个创建树的方法，调用后就可以返回一个包含7个节点的二叉树。  

```
public class Node {
    // 节点值
    public int value;

    // 左子节点
    public Node left;

    // 右子节点
    public Node right;

    Node(int va) {
        value = va;
    }

    Node(int va, Node le, Node ri) {
        value = va;
        left = le;
        ri = right;
    }

    /**
     * 创建一颗二叉树
     *
     * @return 根节点
     */
    public static Node createTree() {
        Node root = new Node(0);
        Node node1 = new Node(1);
        Node node2 = new Node(2);
        Node node3 = new Node(3);
        Node node4 = new Node(4);
        Node node5 = new Node(5);
        Node node6 = new Node(6);
        Node node7 = new Node(7);

        root.left = node1;
        root.right = node2;
        node1.left = node3;
        node1.right = node4;
        node2.left = node5;
        node2.right = node6;
        node3.left = node7;
        return root;
    }
}
```

  

            创建遍历类，在该类里实现各种遍历方法。

  

```
import java.util.ArrayList;

public class Traverse {

    /**
     * 递归前序遍历
     *
     * @param root
     */
    public void recursiveProOrder(Node root) {
        // 遍历根节点
        if (root != null) {
            System.out.print(root.value);
        }
        // 遍历左子树
        if (root.left != null) {
            recursiveProOrder(root.left);
        }
        // 遍历右子树
        if (root.right != null) {
            recursiveProOrder(root.right);
        }
    }

    /**
     * 前序遍历
     *
     * @param root
     */
    public void proOrder(Node root) {
        // 使用ArrayList作为堆栈
        ArrayList<Node> stack = new ArrayList<Node>();
        // 栈指针
        int top = -1;
        Node current = root;
        while (true) {
            if (current != null) {
                System.out.print(current.value);
            }
            // 右子节点进栈
            if (current.right != null) {
                stack.add(current.right);
                top++;
            }
            // 左子节点进栈
            if (current.left != null) {
                stack.add(current.left);
                top++;
            }
            // 如果栈内还有节点，栈顶节点出栈
            if (top > -1) {
                current = stack.get(top);
                stack.remove(top--);
            } else {
                break;
            }
        }
    }

    /**
     * 递归中序遍历
     *
     * @param root
     */
    public void recursiveInOrder(Node root) {
        if (root != null) {
            if (root.left != null) {
                recursiveInOrder(root.left);
            }
            System.out.print(root.value);
            if (root.right != null) {
                recursiveInOrder(root.right);
            }
        }
    }

    /**
     * 中序遍历
     *
     * @param root
     */
    public void inOrder(Node root) {
        if (root != null) {
            ArrayList<Node> stack = new ArrayList<Node>();
            int top = -1;
            Node current = root;
            while (current != null || top > -1) {
                if (current != null) {
                    // 一直深入地寻找左子节点，并将路上的节点都进栈
                    stack.add(current);
                    top++;
                    current = current.left;
                } else {
                    // 取出栈顶节点，并继续遍历右子树
                    current = stack.get(top);
                    stack.remove(top--);
                    System.out.print(current.value);
                    current = current.right;
                }
            }
        }
    }

    /**
     * 递归后续遍历
     *
     * @param root
     */
    public void recursivePostOrder(Node root) {
        if (root != null) {
            if (root.left != null) {
                recursivePostOrder(root.left);
            }
            if (root.right != null) {
                recursivePostOrder(root.right);
            }
            System.out.print(root.value);
        }
    }

    /**
     * 后序遍历：可以被遍历的节点都要进栈出栈两次，所以添加第二个栈用来标示进栈次数
     *
     * @param root
     */
    public void postOrder(Node root) {
        if (root != null) {
            // 用来保存节点的栈
            ArrayList<Node> stack = new ArrayList<Node>();
            // 用来保存标志位的栈
            ArrayList<Integer> stack2 = new ArrayList<Integer>();
            // 两个栈共用的栈指针
            int top = -1;
            int tag;
            Node current = root;
            do {
                //将所有左子节点进栈
                while (current != null) {
                    stack.add(current);
                    stack2.add(0);
                    top++;
                    current = current.left;
                }
                //取出栈顶节点，并判断其标志位
                current = stack.get(top);
                tag = stack2.get(top);
                stack2.remove(top);
                if (tag == 0) {
                    // tag为0,表明该节点第一次进栈，还需要进栈一次，同时修改标志位
                    current = current.right;
                    stack2.add(1);
                } else {
                    // tag不位0,表明非首次进栈，可以遍历了。
                    stack.remove(top);
                    top--;
                    System.out.print(current.value);
                    current = null;
                }
            } while (current != null || top != -1);
        }
    }
}
```

             实例化遍历类并调用各个遍历方法。

         点击(此处)折叠或打开

```
public class Algorithm {

    public static void main(String[] args) {

         Node root=Node.createTree();
         System.out.print("前序遍历： ");
         new Traverse().proOrder(root);
         System.out.println();
         System.out.print("前序递归遍历： ");
         new Traverse().recursiveProOrder(root);
         System.out.println();
         System.out.print("中序遍历： ");
         new Traverse().inOrder(root);
         System.out.println();
         System.out.print("中序递归遍历： ");
         new Traverse().recursiveInOrder(root);
         System.out.println();
         System.out.print("后序遍历： ");
         new Traverse().postOrder(root);
         System.out.println();
         System.out.print("后序递归遍历： ");
         new Traverse().recursivePostOrder(root);
    }
```

  

输出结果：
前序遍历：        01374256
前序递归遍历： 01374256
中序遍历：        73140526
中序递归遍历： 73140526
后序遍历：        73415620
后序递归遍历： 73415620