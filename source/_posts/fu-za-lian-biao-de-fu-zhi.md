---
title: 复杂链表的复制
id: 1486
date: 2024-10-31 22:01:57
author: daichangya
excerpt: https//blog.csdn.net/sunandstarws/article/details/88259143
permalink: /archives/fu-za-lian-biao-de-fu-zhi/
categories:
- 面试
---

**题目：** 输入一个复杂链表（每个节点中有节点值，以及两个指针，一个指向下一个节点，另一个特殊指针指向任意一个节点），返回结果为复制后复杂链表的head。（注意，输出结果中请不要返回参数中的节点引用，否则判题程序会直接返回空）

**思路：** 刚看完题目，感觉挺简单的，就是复制链表嘛，但在实际操作中，出现很多bug，一直提交出错，说“空”。可能就是题目最后那句话的原因把，后面明白，就是重新创建一个链表，然后一个一个复制过来，有两种方法。

一种递归思路，每一次递归都复制一个节点，这样子思路简洁，而且代码短，我用Js实现这个思路提交对了，但是java就不可以，我怀疑牛客网评测系统有问题，我已经发现三个问题了了。

另外一种思路：如下图分析（图从别人那里借来的）

1.首先复制节点，每一次复杂的节点放在原来的节点后面

![](https://uploadfiles.nowcoder.com/images/20160726/737942_1469488971641_84B136C6E4052690517046794A4F80B0)

2、复制随机节点

![](https://uploadfiles.nowcoder.com/images/20160726/737942_1469488996797_F052D5F977FA4E843FE926BA3200084A)

3、把复制的链表和原来的链表分开

![](https://uploadfiles.nowcoder.com/images/20160726/737942_1469489231960_95E2453212A43966E21F1ABC09A80999)

在实现代码的过程中，总是很难写出来，出现很多问题，但是一看上面的图，就懂了。

**代码：**

**js:**

```
/*function RandomListNode(x){
    this.label = x;
    this.next = null;
    this.random = null;
}*/
function Clone(pHead)
{
    if(pHead==null)
            return pHead;
        var a=new RandomListNode(pHead.label);
       a.random=pHead.random;
        a.next=Clone(pHead.next);
        return a;
    
    // write code here
}
```

**java**

```
/*
public class RandomListNode {
    int label;
    RandomListNode next = null;
    RandomListNode random = null;
 
    RandomListNode(int label) {
        this.label = label;
    }
}
*/
 
public class Solution {
    public RandomListNode Clone(RandomListNode pHead)
    {
        if (pHead == null)
           return null ;
         RandomListNode p1=pHead;
        while(p1!=null){
            RandomListNode temp=new  RandomListNode(p1.label);
            temp.next=p1.next;
            p1.next=temp;
            p1=temp.next;
        }
        p1=pHead;
        while(p1!=null){
            if(p1.random!=null)
            p1.next.random=p1.random.next;//这个易错，看分析图
            p1=p1.next.next;
            
        }
        RandomListNode head=pHead.next;
        RandomListNode temp1=head;
        p1=pHead;
        while(p1.next!=null){
            temp1=p1.next;
            p1.next=temp1.next;
            p1=temp1;
        }
        return head;
      //  return pHead;
    }
}
```