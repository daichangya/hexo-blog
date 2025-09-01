---
title: Kubernetes 儿童插图指南
id: 1409
date: 2024-10-31 22:01:54
author: daichangya
excerpt: "原文地址：TheIllustratedChildren’sGuidetoKubernetes原文作者：CLOUDNATIVECOMPUTINGFOUNDATIONKubernetes儿童插图指南献给所有试图向孩子们解释软件工程的家长。很久很久以前，有一个叫Phippy的应用程序。她是一个简单的应用程"
permalink: /archives/kubernetes%E5%84%BF%E7%AB%A5%E6%8F%92%E5%9B%BE%E6%8C%87%E5%8D%97/
tags: 
 - kubernetes
---

> * 原文地址：[The Illustrated Children’s Guide to Kubernetes](https://www.cncf.io/the-childrens-illustrated-guide-to-kubernetes/)
> * 原文作者：[CLOUD NATIVE COMPUTING FOUNDATION](https://www.cncf.io)

# Kubernetes 儿童插图指南

![page1.png](https://images.jsdiff.com/page1_1591018964208.png)

![TheIllustratedChildrensGuidetoKubernetesBookFilesSept2018CNCF1024x791.jpg](https://images.jsdiff.com/The-Illustrated-Childrens-Guide-to-Kubernetes-Book-Files-Sept-2018-CNCF-1024x791_1591019010112.jpg)

![kubernetesillustratedguideillustration1.png](https://images.jsdiff.com/kubernetes-illustrated-guide-illustration-1_1591019075411.png)

**献给所有试图向孩子们解释软件工程的家长。**

![kubernetesillustratedguideillustration3.png](https://images.jsdiff.com/kubernetes-illustrated-guide-illustration-3_1591019281886.png)

很久很久以前，有一个叫 Phippy 的应用程序。她是一个简单的应用程序，由 PHP 编写且只有一个页面。她住在一个需要和其他可怕的应用程序分享环境的主机中，她不认识这些应用程序并且不愿意和他们来往。她希望她能拥有一个属于自己的环境：只有她自己和她可以称之为家的 Web 服务器。

![kubernetesillustratedguidediagram2.png](https://images.jsdiff.com/kubernetes-illustrated-guide-diagram-2_1591019319768.png)

每个应用程序都有个运行所依赖的环境。对于 PHP 应用程序来说，这个环境可能包括 Web 服务器，一个可读文件系统和 PHP 引擎本身。

![kubernetesillustratedguideillustration4.png](https://images.jsdiff.com/kubernetes-illustrated-guide-illustration-4_1591019338242.png)

有一天，一只善良的鲸鱼出现了。他建议小 Phippy 住在容器里，这样可能会更快乐。所以应用程序 Phippy 迁移到了容器中。这个容器很棒，但是……它有点像一个漂浮在大海中央的豪华起居室。

![kubernetesillustratedguidediagram3.png](https://images.jsdiff.com/kubernetes-illustrated-guide-diagram-3_1591019365222.png)

容器提供了一个独立的环境，应用程序可以在这个环境中运行。但是这些孤立的容器常常需要被管理并与外面的世界连接。对于孤立的容器而言，共享文件系统、网络通信、调度、负载均衡和分发都是要面对的挑战。

![kubernetesillustratedguideillustration5.png](https://images.jsdiff.com/kubernetes-illustrated-guide-illustration-5_1591019388112.png)

鲸鱼耸了耸肩。“对不起，孩子。”他说着，消失在海面下。就在 Phippy 甚至开始绝望时，一位驾驶着巨轮的船长出现在海平线上。这艘船由几十个绑在一起的木筏组成，但从外面来看，它就像一艘巨轮。

“你好呀，这位 PHP 应用程序朋友。我是 Kube 船长。”睿智的老船长说。

![kubernetesillustratedguidediagram4.png](https://images.jsdiff.com/kubernetes-illustrated-guide-diagram-4_1591019552848.png)

“Kubernetes” 在希腊语中是船长的意思。我们可以从这个单词中得到 **Cybernetic** 和 **Gubernatorial** 这两个词组。Kubernetes 项目专注于构建一个健壮的平台，用于在生产环境中运行数千个容器。

![kubernetesillustratedguidediagram6.png](https://images.jsdiff.com/kubernetes-illustrated-guide-diagram-6_1591019567318.png)

“我是 Phippy。”小应用程序说。

“很高兴认识你。”船长一边说，一边在她身上贴上了一张标有姓名的标签。

![kubernetesillustratedguideillustration5.png](https://images.jsdiff.com/kubernetes-illustrated-guide-illustration-5_1591019580237.png)

Kubernetes 使用标签作为“名牌”来标识事物。它可以根据这些标签进行查询。标签是开放性的：你可以用他们来表示角色、稳定性或其他重要的属性。

![kubernetesillustratedguidediagram7.png](https://images.jsdiff.com/kubernetes-illustrated-guide-diagram-7_1591019597990.png)

船长建议应用程序把她的容器搬到船上的一个船舱中。Phippy 很高兴地把她的容器搬到 Kube 船长巨轮的船舱内。Phippy 觉得这里像家一样。

![kubernetesillustratedguideillustration6.png](https://images.jsdiff.com/kubernetes-illustrated-guide-illustration-6_1591019626105.png)

在 Kubernetes 中，Pod 代表一个可运行的工作单元。通常，你会在 Pod 中运行一个容器。但是对于一些容器紧密耦合的情况，你可以选择在同一个 Pod 中运行多个容器。Kubernetes 负责将你的 Pod 和网络以及 Kubernetes 的其余环境相连。

![kubernetesillustratedguideillustration8.png](https://images.jsdiff.com/kubernetes-illustrated-guide-illustration-8_1591019643495.png)

Phippy 有一些不同寻常的兴趣，她很喜欢遗传学和绵羊。所以她问船长：“如果我想克隆我自己，是否可以根据需求克隆任意次数呢？”

“这很容易。”船长说。船长把 Phippy 介绍给了 Replication Controller。

![kubernetesillustratedguideillustration7.png](https://images.jsdiff.com/kubernetes-illustrated-guide-illustration-7_1591019659462.png)

Replication Controller 提供一种管理任意数量 Pod 的方法。一个 Replication Controller 包含一个 Pod 模板，该模板可以被复制任意次数。通过 Replication Controller，Kubernetes 将管理 Pod 的生命周期，包括伸缩、滚动更新和监控。

![kubernetesillustratedguideillustration9.png](https://images.jsdiff.com/kubernetes-illustrated-guide-illustration-9_1591019673945.png)

无数个日夜，小应用程序在她的船舱中与她的复制品相处十分愉快。但与自己为伍并没有所说的那么好……即使你拥有 N 个自己的克隆体。

Kube 船长慈祥地笑了笑：“我正好有一样东西。”

他刚开口，在 Phippy 的 Replication Controller 和船的其他部分之间打开了一条隧道。Kube 船长笑着说：“即使你的复制品来了又去，这条隧道始终会留在这里，你可以通过它发现其他 Pod，其他 Pod 也可以发现你！”

![kubernetesillustratedguideillustration8.png](https://images.jsdiff.com/kubernetes-illustrated-guide-illustration-8_1591019691521.png)

服务告知 Kubernetes 环境的其余部分（包括其他 Pod 和 Replication Controller）你的应用程序包含了哪些服务，当 Pod 来来往往，服务的 IP 地址和端口始终保持不变。其他应用程序可以通过 Kurbenetes 服务发现找到你的服务。

![kubernetesillustratedguideillustration10.png](https://images.jsdiff.com/kubernetes-illustrated-guide-illustration-10_1591019707013.png)

多亏了这些服务，Phippy 开始探索船的其他部分。不久之后，Phippy 遇到了 Goldie。他们成了最好的朋友。有一天，Goldie 做了一件不同寻常的事。她送给 Phippy 一件礼物。Phippy 看了礼物一眼，悲伤的泪水夺眶而出。

“你为什么这么伤心呢？”Goldie 问道。

“我喜欢这个礼物，但我没有地方可以放它！”Phippy 抽噎道。

但 Goldie 知道该怎么做。“为什么不把它放入卷中呢？”

![kubernetesillustratedguidediagram9.png](https://images.jsdiff.com/kubernetes-illustrated-guide-diagram-9_1591019758552.png)


卷表示容器可以访问和存储信息的位置。对于应用程序，卷显示为本地文件系统的一部分。但卷可以由本地存储、Ceph、Gluster、持久性块存储，以及其他存储后端支持。

Phippy 喜欢在 Kube 船长的船上生活，她很享受来自新朋友的陪伴（Goldie 的每个克隆人都同样令人愉悦）。但是，当她回想起在可怕的主机度过的日子，她想知道她是否也可以拥有一点自己的隐私。

“这听起来像是你所需要的，”Kube 船长说，“这是一个命名空间。”

![kubernetesillustratedguidediagram10.png](https://images.jsdiff.com/kubernetes-illustrated-guide-diagram-10_1591019777382.png)

命名空间是 Kubernetes 内部的分组机制。服务、Pod、Replication Controller 和卷可以在命名空间内部轻松协作，但命名空间提供了与集群其他部分一定程度的隔离。

Phippy 与她的新朋友一起乘坐 Kube 船长的巨轮航行于大海之上。她经历了许多伟大的冒险，但最重要的是，Phippy 找到了自己的家。

所以 Phippy 从此过上了幸福的生活。
![back1024x787.jpg](https://images.jsdiff.com/back-1024x787_1591019796818.jpg)
[下一篇](https://blog.jsdiff.com/archives/8-things-you-need-to-know-before-system-design-interviews)https://blog.jsdiff.com