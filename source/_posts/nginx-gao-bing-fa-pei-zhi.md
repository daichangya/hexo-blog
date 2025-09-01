---
title: nginx-高并发配置
id: 1448
date: 2024-10-31 22:01:56
author: daichangya
excerpt: 一、nginx服务配置优化：1.nginx进程数，建议按照cpu数目来指定，一般为它的倍数。worker_processes定义了nginx对外提供web服务时的worker进程数。最优值取决于许多因素，包括（但不限于）CPU核的数量、存储数据的硬盘数量及负载模式。不能确定的时候，将其设置为可用的C
permalink: /archives/nginx-gao-bing-fa-pei-zhi/
categories:
- nginx
---



一 、nginx 服务配置优化：

1.nginx进程数，建议按照cpu数目来指定，一般为它的倍数。worker_processes 定义了nginx对外提供web服务时的worker进程数。最优值取决于许多因素，包括（但不限于）CPU核的数量、存储数据的硬盘数量及负载模式。不能确定的时候，将其设置为可用的CPU内核数将是一个好的开始（可以设置为“auto”将尝试自动检测它）。

```
worker_processes 8;
```

2.为每个进程分配cpu，上例中将8个进程分配到8个cpu，当然可以写多个，或者将一个进程分配到多个cpu。

```
worker_cpu_affinity 00000001 00000010 00000100 00001000 00010000 00100000 01000000 10000000;
```

3\. 指定worker 进程能够打开的最大句柄数，默认选择与 ulimit -n 的值一致。通过ulimit 修改配置文件。

```

```

4.nginx 使用epoll 模型。

```
use epoll;
```

5.单个worker 进程连接数限制，理论上每台nginx服务器的最大连接数为worker\_processes*worker\_connections。  
  

```
worker_connections 102400;
```

6.keepalive超时时间设置，建议为60s 不要设置太大。

```
keepalive_timeout 60;
```

  
7.客户端请求头部的缓冲区大小，这个可以根据你的系统分页大小来设置，一般一个请求的头部大小不会超过1k，不过由于一般系统分页都要大于1k，所以这里设置为分页大小。分页大小可以用命令getconf PAGESIZE取得。

```
client_header_buffer_size 4k;


[root@localhost ~]# getconf PAGESIZE
4096
[root@localhost ~]# 
```

8. 这个将为打开文件指定缓存，默认是没有启用的，max指定缓存数量，建议和打开文件数一致，inactive是指经过多长时间文件没被请求后删除缓存。

```
open_file_cache max=102400 inactive=20s;
```

9\. 指定多长时间检查一次缓存的有效性。

```
open_file_cache_valid 30s;
```

10. open\_file\_cache指令中的inactive参数时间内文件的最少使用次数，如果超过这个数字，文件描述符一直是在缓存中打开的，如上例，如果有一个文件在inactive时间内一次没被使用，它将被移除。

```
open_file_cache_min_uses 1;
```

二、内核参数的优化：

1. 表示系统同时保持TIME\_WAIT状态的socket数量, 如果超过这个值, TIME\_WAIT状态的socket会被清除, 同时打印警告日志，默认18000 ，减少这个值可以加快无效连接的回收

```
net.ipv4.tcp_max_tw_buckets = 6000
```

2\. 允许打开的端口范围

```
net.ipv4.ip_local_port_range = 1024 65000
```

3\. timewait 快速回收，tcp\_tw\_recycle参数使处于TIME_WAIT状态的的socket被快速回收(默认是2msl时间).

tcp\_tw\_recycle参数想要正常工作, 还依赖于tcp\_timestamp选项, 它要求数据包的时间戳严格顺序. 所以在公网环境下, 如果多client在同一NAT中, 上行包的timestamp无法保证顺序, 会出现严重问题. 所以tcp\_tw_recycle参数一般不建议打开, 保持默认为0.

```
net.ipv4.tcp_tw_recycle = 1
```

4.开启处于TIME_WAIT状态下的socket快速重用, 用于新的tcp连接

```
net.ipv4.tcp_tw_reuse = 1
```

5.开启SYN Cookies ,当出现SYN等待队列溢出时，启用cookies来处理

```
net.ipv4.tcp_syncookies = 1
```

6.web应用中listen函数的backlog默认会给我们内核参数的net.core.somaxconn限制到128，而nginx定义的NGX\_LISTEN\_BACKLOG默认为511，所以有必要调整这个值。

```
net.core.somaxconn = 262144
```

7.当网卡接受数据包的速率, 比kernel处理来的快时, 即kernel处理跟不上包率时, cache这些数据包的队列长度.

默认值是1k, 可以适当调大到2k或者4k, 再大的意义不是很大, kernel都忙不过来了, cache再多也只能治标不治本.

```
net.core.netdev_max_backlog = 4096
```

8. 表示没有任何handle的socket的最大数量, 通俗一点说, 即不属于任何进程的tcp socket最大数量. 超过这个数量的socket会被reset, 并同时告警.

这个参数是为了防御简单的DDOS攻击, 一般系统给的默认大多是8k或者16k, 某些防火墙会把它改成2k.

在网络特别繁忙时, 为了避免大量的告警信息, 也有将这个参数调大的, 例如256k.

建议这个参数保持默认就好.

```
net.ipv4.tcp_max_orphans = 262144
```

9.记录的那些尚未收到客户端确认信息的连接请求的最大值。对于有128M内存的系统而言，缺省值是1024，小内存的系统则是128。

```
net.ipv4.tcp_max_syn_backlog = 262144
```

10. 时间戳可以避免序列号的卷绕。一个1Gbps的链路肯定会遇到以前用过的序列号。时间戳能够让内核接受这种“异常”的数据包。这里需要将其关掉。

```
net.ipv4.tcp_timestamps = 0
```

11. tcp\_syn\_retries, 顾名思义, 即握手时syn的最大重发次数, 默认是6. 这是一个客户端行为, 默认值是5, 在网络情况良好的情况下可以调小到 2.

tcp\_synack\_retries, 是指握手时server重发ack的最大次数, 默认是5. 这个值也可以设置到 2, 来提高server的效率.

```
net.ipv4.tcp_synack_retries = 2net.ipv4.tcp_syn_retries = 2
```

12. tcp连接保持在FIN\_WAIT\_2的时间, 默认值是60, 这个参数可以适当调低: 30乃至更低都可以, 从而减少内存的消耗.

```
net.ipv4.tcp_fin_timeout = 30
```

13. 当keepalive选项开启时, tcp连接的超时时间, 默认是7200. 为了提高效率及更高的安全性, 可以调整这个参数到 1800.

但是业务不应该只依赖于tcp的超时机制, 特别是长连接的业务, 应该保证自己的心跳超时机制, 来防止恶意空连接.

```
net.ipv4.tcp_keepalive_time = 300
```

14\. 一个完整的内核优化配置

```
net.ipv4.ip_forward = 0
net.ipv4.conf.default.rp_filter = 1
net.ipv4.conf.default.accept_source_route = 0
kernel.sysrq = 0
kernel.core_uses_pid = 1
net.ipv4.tcp_syncookies = 1
kernel.msgmnb = 65536
kernel.msgmax = 65536
kernel.shmmax = 68719476736
kernel.shmall = 4294967296
net.ipv4.tcp_max_tw_buckets = 6000
net.ipv4.tcp_sack = 1
net.ipv4.tcp_window_scaling = 1
net.ipv4.tcp_rmem = 4096 87380 4194304
net.ipv4.tcp_wmem = 4096 16384 4194304
net.core.wmem_default = 8388608
net.core.rmem_default = 8388608
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.core.netdev_max_backlog = 262144
net.core.somaxconn = 262144
net.ipv4.tcp_max_orphans = 3276800
net.ipv4.tcp_max_syn_backlog = 262144
net.ipv4.tcp_timestamps = 0
net.ipv4.tcp_synack_retries = 1
net.ipv4.tcp_syn_retries = 1
net.ipv4.tcp_tw_recycle = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_mem = 94500000 915000000 927000000
net.ipv4.tcp_fin_timeout = 1
net.ipv4.tcp_keepalive_time = 30
net.ipv4.ip_local_port_range = 1024 65000
```

 15 .配置修改 /etc/sysctl.conf 配置文件添加如上内容

```
[root@nginx sbin]# sysctl -p   #配置生效
```

```
sysctl命令用于运行时配置内核参数，这些参数位于/proc/sys目录下。sysctl配置与显示在/proc/sys目录中的内核参数．可以用sysctl来设置或重新设置联网功能，如IP转发、IP碎片去除以及源路由检查等。用户只需要编辑/etc/sysctl.conf文件，即可手工或自动执行由sysctl控制的功能。
    命令格式：

    sysctl [-n] [-e] -w variable=value

    sysctl [-n] [-e] -p <filename> (default /etc/sysctl.conf)

    sysctl [-n] [-e] -a

    常用参数的意义：

    -w   临时改变某个指定参数的值，如

        sysctl -w net.ipv4.ip_forward=1

    -a   显示所有的系统参数

    -p   从指定的文件加载系统参数，如不指定即从/etc/sysctl.conf中加载

    如果仅仅是想临时改变某个系统参数的值，可以用两种方法来实现,例如想启用IP路由转发功能：

    1) #echo 1 > /proc/sys/net/ipv4/ip_forward

    2) #sysctl -w net.ipv4.ip_forward=1

    以上两种方法都可能立即开启路由功能，但如果系统重启，或执行了

    # service network restart

 命令，所设置的值即会丢失，如果想永久保留配置，可以修改/etc/sysctl.conf文件

 将 net.ipv4.ip_forward=0改为net.ipv4.ip_forward=1



1, sysctl命令的作用
     在运行时配置内核参数
2,用法举例:
      -w 用此选项来改变一个sysctl设置
     例:sysctl -w net.ipv4.ip_forward=1
     -p   载入sysctl配置文件
           如-p后未指定路径，则载入 /etc/sysctl.conf
     例: sysctl -p /etc/sysctl.conf
```

参考:https://www.cnblogs.com/sunsky303/p/10648861.html