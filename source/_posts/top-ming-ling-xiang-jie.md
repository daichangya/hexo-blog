---
title: top命令详解
id: 1330
date: 2024-10-31 22:01:51
author: daichangya
excerpt: 这是一张top的图第一行字符含义top-100319当前系统时间up137days,1040系统已运行时间2user在线用户loadaverage0.00,0.01,0.05系统负载。三个数值分别为1分钟、5分钟、15分钟前到现在的平均值。2user，包含系统用户。第二行字符含义Tasks
permalink: /archives/top-ming-ling-xiang-jie/
tags:
- linux
---

## 这是一张top的图
![top](http://images.jsdiff.com/upload/2020/04/aylmu-5xewf-7e6f10122db5489b92aa74049d335e87.jpg)
<h3>第一行</h3>
<table>
<thead>
<tr>
<th style="text-align:center">字符</th>
<th style="text-align:center">含义</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center">top - 10:03:19</td>
<td style="text-align:center">当前系统时间</td>
</tr>
<tr>
<td style="text-align:center">up 137 days , 10:40</td>
<td style="text-align:center">系统已运行时间</td>
</tr>
<tr>
<td style="text-align:center">2 user</td>
<td style="text-align:center">在线用户</td>
</tr>
<tr>
<td style="text-align:center">load average: 0.00, 0.01, 0.05</td>
<td style="text-align:center">系统负载。三个数值分别为  1分钟、5分钟、15分钟前到现在的平均值。</td>
</tr>
</tbody>
</table>
<blockquote>
<p>2 user，包含系统用户。</p>
</blockquote>
<hr>
<h3>第二行</h3>
<table>
<thead>
<tr>
<th style="text-align:center">字符</th>
<th style="text-align:center">含义</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center">Tasks : 92 total</td>
<td style="text-align:center">总进程数</td>
</tr>
<tr>
<td style="text-align:center">2 running</td>
<td style="text-align:center">正在运行的进程数</td>
</tr>
<tr>
<td style="text-align:center">90 sleeping</td>
<td style="text-align:center">正在睡眠的进程数</td>
</tr>
<tr>
<td style="text-align:center">0 stopped</td>
<td style="text-align:center">停止的进程数</td>
</tr>
<tr>
<td style="text-align:center">0 zombie</td>
<td style="text-align:center">僵尸进程数</td>
</tr>
</tbody>
</table>
<blockquote>
<p>僵尸进程:一个子进程在其父进程没有调用wait()或waitpid()的情况下退出。这个子进程就是僵尸进程。如果其父进程还存在而一直不调用wait，则该僵尸进程将无法回收，等到其父进程退出后该进程将被init回收。</p>
</blockquote>
<hr>
<h3>第三行</h3>
<table>
<thead>
<tr>
<th style="text-align:center">字符</th>
<th style="text-align:center">含义</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center">%Cpu(s): 0.3 us</td>
<td style="text-align:center">cpu占用率(%)，用户进程占用cpu百分率</td>
</tr>
<tr>
<td style="text-align:center">0.3 sy</td>
<td style="text-align:center">系统占用cpu百分率</td>
</tr>
<tr>
<td style="text-align:center">0.0 ni</td>
<td style="text-align:center">用户进程空间内改变过优先级的进程占用CPU百分比</td>
</tr>
<tr>
<td style="text-align:center">99.3 id</td>
<td style="text-align:center">cpu空闲率</td>
</tr>
<tr>
<td style="text-align:center">0.0 wa</td>
<td style="text-align:center">等待IO的CPU时间百分比</td>
</tr>
<tr>
<td style="text-align:center">0.0 hi</td>
<td style="text-align:center">硬中断（Hardware IRQ）占用CPU的百分比</td>
</tr>
<tr>
<td style="text-align:center">0.0 si</td>
<td style="text-align:center">软中断（Software Interrupts）占用CPU的百分比</td>
</tr>
</tbody>
</table>
<blockquote>
<p>cpu的使用情况</p>
</blockquote>
<hr>
<h3>第四行</h3>
<table>
<thead>
<tr>
<th style="text-align:center">字符</th>
<th style="text-align:center">含义</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center">KiB Mem : 1016916 total</td>
<td style="text-align:center">内存总量（我这里是1G）</td>
</tr>
<tr>
<td style="text-align:center">82280 free</td>
<td style="text-align:center">内存空闲量</td>
</tr>
<tr>
<td style="text-align:center">233848 used</td>
<td style="text-align:center">内存使用量</td>
</tr>
<tr>
<td style="text-align:center">700788 buff/cache</td>
<td style="text-align:center">缓存的内存量</td>
</tr>
</tbody>
</table>
<blockquote>
<p>内存使用率</p>
</blockquote>
<hr>
<h3>第五行</h3>
<table>
<thead>
<tr>
<th style="text-align:center">字符</th>
<th style="text-align:center">含义</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center">KiB Swap: 0 total</td>
<td style="text-align:center">交换区总量</td>
</tr>
<tr>
<td style="text-align:center">0 free</td>
<td style="text-align:center">交换区空闲量</td>
</tr>
<tr>
<td style="text-align:center">0 used</td>
<td style="text-align:center">交换区使用量</td>
</tr>
</tbody>
</table>
<blockquote>
<p>我这里没有swap分区，所以都为0</p>
</blockquote>
<hr>
<h3>第六行</h3>
<table>
<thead>
<tr>
<th style="text-align:center">字符</th>
<th style="text-align:center">含义</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center">PID</td>
<td style="text-align:center">进程号</td>
</tr>
<tr>
<td style="text-align:center">USER</td>
<td style="text-align:center">进程创建者</td>
</tr>
<tr>
<td style="text-align:center">PR</td>
<td style="text-align:center">进程优先级</td>
</tr>
<tr>
<td style="text-align:center">NI</td>
<td style="text-align:center">nice值。越小优先级越高，最小-20，最大20（用户设置最大19）</td>
</tr>
<tr>
<td style="text-align:center">VIRT</td>
<td style="text-align:center">进程使用的虚拟内存总量，单位kb。VIRT=SWAP+RES</td>
</tr>
<tr>
<td style="text-align:center">RES</td>
<td style="text-align:center">进程使用的、未被换出的物理内存大小，单位kb。RES=CODE+DATA</td>
</tr>
<tr>
<td style="text-align:center">SHR</td>
<td style="text-align:center">共享内存大小，单位kb</td>
</tr>
<tr>
<td style="text-align:center">S</td>
<td style="text-align:center">进程状态。D=不可中断的睡眠状态 R=运行 S=睡眠 T=跟踪/停止 Z=僵尸进程</td>
</tr>
<tr>
<td style="text-align:center">%CPU</td>
<td style="text-align:center">进程占用cpu百分比</td>
</tr>
<tr>
<td style="text-align:center">%MEM</td>
<td style="text-align:center">进程占用内存百分比</td>
</tr>
<tr>
<td style="text-align:center">TIME+</td>
<td style="text-align:center">进程运行时间</td>
</tr>
<tr>
<td style="text-align:center">COMMAND</td>
<td style="text-align:center">进程名称</td>
</tr>
</tbody>
</table>
<blockquote>
<p>PR 越低优先级 越高，PRI(new)=PRI(old)+nice<br>
PR中的rt为实时进程优先级即rt_priority，prio=MAX_RT_PRIO - 1- p-&gt;rt_priority<br>
MAX_RT_PRIO = 99，prio大小决定最终优先级。这样意味着rt_priority值越大，优先级越高而内核提供的修改优先级的函数，是修改rt_priority的值，所以越大，优先级越高。<br>
例：改变优先级：进入top后按“r”–&gt;输入进程PID–&gt;输入nice值</p>
</blockquote>
<h3>top命令（在进入top后使用）</h3>
<blockquote>
<p>P：以占据CPU百分比排序<br>
M：以占据内存百分比排序<br>
T：以累积占用CPU时间排序<br>
q：退出命令：按q键退出top查看页面<br>
s：修改刷新时间间隔。按下s键，然后按下数字，即可修改刷新时间间隔为你输入的数字，单位为秒。例如：按下s键，在按数字1键，即可实现每秒刷新一次<br>
k：终止指定的进程。按下k键--&gt;再输入要杀死的进程的pid--&gt;按enter键--&gt;(选择信号类型，以数字标示，默认15为杀死)本步可省略按enter键（常用为-9）</p>
</blockquote>
<p>kill信号大全：<a href="https://link.jianshu.com?t=http://www.2cto.com/os/201202/119425.html" target="_blank" rel="nofollow">http://www.2cto.com/os/201202/119425.html</a></p>
<hr>
</article>