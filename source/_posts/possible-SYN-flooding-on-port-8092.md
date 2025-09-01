---
title: possible SYN flooding on port 8092. Sending cookies
id: 1452
date: 2024-10-31 22:01:56
author: daichangya
excerpt:   实际生产环境中出现SYNflooding的情况好多次了，之前虽然解决了，但一直没好好整理一下。直到上周五又出现该问题，这次利用周末的空闲时间好好查阅资料研究了翻，整理一篇博文。想说的是，养成写博客或者整理文档的习惯真的很重要，因为当你把它写成一篇文章的时候，首先你自己必须要先理解，然后思路必须要
permalink: /archives/possible-SYN-flooding-on-port-8092/
tags:
- tcp
---

    实际生产环境中出现SYN flooding的情况好多次了，之前虽然解决了，但一直没好好整理一下。直到上周五又出现该问题，这次利用周末的空闲时间好好查阅资料研究了翻，整理一篇博文。想说的是，养成写博客或者整理文档的习惯真的很重要，因为当你把它写成一篇文章的时候，首先你自己必须要先理解，然后思路必须要清晰，有时候可能需要花上一整天的时间查资料，对自己也是一种提高，才算是对自己和读者的负责。  

    先介绍下**什么是SYN flooding**。  

  SYN Flood是当前最流行的DoS（拒绝服务攻击）与DDoS（分布式拒绝服务攻击）的方式之一，这是一种利用TCP协议缺陷，发送大量伪造的TCP连接请求，塞满TCP等待连接队列，导致资源耗尽（CPU满负荷或内存不足），让正常的业务请求连接不进来，从而间接达到攻击的目的。

  说起TCP协议，不得不提三次握手。SYN Flood攻击利用的正是IPv4中TCP协议的三次握手过程进行的攻击。如果一端想向另一端发起TCP连接，它需要首先发送TCP SYN 包到对方，对方收到后发送一个TCP SYN+ACK包回来，发起方再发送TCP ACK包回去，这样三次握手就结束了。我们把TCP连接的发起方叫作"TCP客户机（TCP Client）"，TCP连接的接收方叫作"TCP服务器（TCP Server）"。值得注意的是在TCP服务器收到TCP SYN request包时，在发送TCP SYN+ACK包回TCP客户机前，TCP服务器要先分配好一个数据区专门服务于这个即将形成的TCP连接。一般把收到SYN包而还未收到ACK包时的连 接状态成为半开连接（Half-open Connection）。

  在最常见的SYN Flood攻击中，攻击者在短时间内发送大量的TCP SYN包给受害者，这时攻击者是TCP客户机，受害者是TCP服务器。根据上面的描述，受害者会为每个TCP SYN包分配一个特定的数据区，只要这些SYN包具有不同的源地址（这一点对于攻击者来说是很容易伪造的）。这将给TCP服务器系统造成很大的系统负担， 最终导致系统不能正常工作。

  **那如何防御呢？**

  通常会把tcp cookie的功能打开。那又为什么发送cookie呢？这个cookie是什么呢？

  这个cookie是指SYN Cookie。在目前以IPv4为支撑的网络协议上搭建的网络环境中，SYN Flood是一种非常危险而常见的DoS攻击方式。到目前为止，能够有效防范SYN Flood攻击的手段并不多，而SYN Cookie就是其中最著名的一种。SYN Cookie原理由D.J.Bernstain和Eric Schenk发明。在很多操作系统上都有各种各样的实现。其中包括Linux。

 我查了[kernel documention](https://github.com/torvalds/linux/blob/6b15d6650c5301ce023d8df0cc3a60b1a76d377e/Documentation/networking/ip-sysctl.txt)，里面有syn_cookies的官方介绍：  

```bash
Note, that syncookies is fallback facility.    
It MUST NOT be used to help highly loaded servers to stand    
against legal connection rate. If you see SYN flood warnings    
in your logs, but investigation	shows that they occur    
because of overload with legal connections, you should tune    
another parameters until this warning disappear.    
See: tcp_max_syn_backlog, tcp_synack_retries, tcp_abort_on_overflow.    

syncookies seriously violate TCP protocol, do not allow    
to use TCP extensions, can result in serious degradation    
of some services (f.e. SMTP relaying), visible not by you,    
but your clients and relays, contacting you. While you see    
SYN flood warnings in logs not being really flooded, your server    
is seriously misconfigured.
```

  **官方明确说明了当看到有SYN flood warning的时候并不一定真的是flooded,有可能是你的服务器没有正确的配置。** 同理，有时你的服务器有此报警的时候也并不一定是真的有攻击，这时就需要你调整你的内核参数。

  上张图，用dmesg或者在系统的syslog里能够查看有关SYN flooding的报错信息：  

![image.png](https://images.jsdiff.com/image_1594805837732.png)

**内核调优**

  上面官方文档中也提到当出现此问题的时候，可以调整内核的三个参数：tcp\_max\_syn\_backlog, tcp\_synack\_retries, tcp\_abort\_on\_overflow。

tcp\_max\_syn_backlog变量告诉你在内存中可以缓存多少个SYN请求。该变量需要打开tcp_syncookies才有效。如果服务器负载很高，可以尝试提高该变量的值。

tcp\_synack\_retries变量用于TCP三次握手机制中第二次握手，当收到客户端发来的SYN连接请求后，服务端将回复SYN+ACK包，这时服务端处于SYN_RCVD状态，并等 待客户端发来的回复ACK包。如果服务端没有收到客户端的ACK包，会重新发送SYN+ACK包，直到收到客户端的ACK包。该变量设置发送 SYN+ACK包的次数，超过这个次数，服务端将放弃连接。默认值是5。

tcp\_abort\_on_overflow变量的值是个布尔值，默认值为0（FALSE关闭）。如果开启，当服务端接收新连接的速度变慢时，服务端会发送RST包（reset包）给客户端，令客户端 重新连接。这意味着如果突然发生溢出，将重获连接。仅当你真的确定不能通过调整监听进程使接收连接的速度变快，可以启用该选项。该选项会影响到客户的连接。

  **实际测试，只更改这几个参数有时是不管用的。解决办法如下：**

我目前的解决办法是调整以下几个内核参数，实践证明调整之后暂时未再复现问题。而官方文档中提到的retry和overflow的两个参数，建议还是不要调整，用默认的就好，以免产生副作用。

```bash
# vim /etc/sysctl.conf 
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_tw_recycle = 1
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_max_syn_backlog = 2048
保存退出后，执行：
# sysctl -p
```

参数说明如下：

net.ipv4.tcp_syncookies = 1  
#表示开启SYN Cookies。当出现SYN等待队列溢出时，启用cookies来处理，可防范少量SYN攻击，默认为0，表示关闭；  

net.ipv4.tcp\_tw\_reuse = 1  
#表示开启重用。允许将TIME-WAIT sockets重新用于新的TCP连接，默认为0，表示关闭；为1，开启；  
net.ipv4.tcp\_tw\_recycle = 1  
#表示开启TCP连接中TIME-WAIT sockets的快速回收，默认为0，表示关闭；为1，开启；

net.ipv4.tcp\_fin\_timeout

#修改系統默认的 TIMEOUT 时间，**这里根据服务器的实际情况设置**。

  另外细心的朋友可能发现了，报错信息： Possible SYN flooding on port 13370. Sending cookies.后面跟了句"Check SNMP counters"。这句我当时差点被误导，因为我的服务器上正好跑了一个snmp抓流量的服务，开始以为是它导致的，后来一想那是udp的协议，和tcp没关系呀。查了[kernel](https://github.com/torvalds/linux/blob/797cee982eef9195736afc5e7f3b8f613c41d19a/net/ipv4/tcp_input.c)的代码发现，原来那是print打印的固定info输出：

```bash
static bool tcp_syn_flood_action(const struct sock *sk,
				const struct sk_buff *skb,
				const char *proto)
{
	struct request_sock_queue *queue = &inet_csk(sk)->icsk_accept_queue;
	const char *msg = "Dropping request";
	bool want_cookie = false;
	struct net *net = sock_net(sk);
#ifdef CONFIG_SYN_COOKIES
	if (net->ipv4.sysctl_tcp_syncookies) {
		msg = "Sending cookies";
		want_cookie = true;
		__NET_INC_STATS(sock_net(sk), LINUX_MIB_TCPREQQFULLDOCOOKIES);
	} else
#endif
		__NET_INC_STATS(sock_net(sk), LINUX_MIB_TCPREQQFULLDROP);
	if (!queue->synflood_warned &&
	net->ipv4.sysctl_tcp_syncookies != 2 &&
	xchg(&queue->synflood_warned, 1) == 0)
		pr_info("%s: Possible SYN flooding on port %d. %s.  Check SNMP counters.\n",
			proto, ntohs(tcp_hdr(skb)->dest), msg);
	return want_cookie;
}
```

参考:
https://zhuanlan.zhihu.com/p/58067219
https://www.cnblogs.com/tony2017/p/11236448.html
https://my.oschina.net/zhangxc73912/blog/512763?p={{currentPage+1}}
https://iyaozhen.com/nginx-tomcat-502-and-proxy_next_upstream.html