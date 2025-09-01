---
title: Ubuntu系统中apt-cache命令：探寻软件包的得力助手
id: 63bec3b6-1d26-4e30-94a4-7704a65f6448
date: 2024-12-10 10:04:05
author: daichangya
cover: https://images.jsdiff.com/Linux.jpg
excerpt: 在Ubuntu及采用相同包管理系统的Linux世界里，你是否曾为寻找特定软件包而感到迷茫？今天，就让我们一同深入了解apt-cache命令，它将为我们开启一扇轻松查找软件包的大门。
  一、apt-cache命令简介 当我们在Ubuntu上想要安装软件时，apt-get是我们常用的工具。但要查找软件仓库
permalink: /archives/Ubuntu-xi-tong-zhong-apt-cache-ming/
categories:
- linux
---

在Ubuntu及采用相同包管理系统的Linux世界里，你是否曾为寻找特定软件包而感到迷茫？今天，就让我们一同深入了解apt-cache命令，它将为我们开启一扇轻松查找软件包的大门。

## 一、apt-cache命令简介
当我们在Ubuntu上想要安装软件时，apt-get是我们常用的工具。但要查找软件仓库中是否存在某个软件包，正确的做法是使用apt-cache命令，而非apt-get search或apt-get - list。apt-cache命令就像是一位贴心的向导，帮助我们在软件包的海洋中快速定位目标。

### （一）apt-cache search：精准查找软件包
语法：apt-cache search <string>

作用：在源软件列表中查找与指定字符串相关的软件包。

### 二、apt-cache search实战
以强大的fping软件包为例，它支持轮询（round - robin）方式进行ping操作，默认情况下系统并不自带。

### （一）查找fping软件包
在终端中输入：
```bash
apt-cache search fping
```
执行结果如下：
```
fping - sends ICMP ECHO_REQUEST packets to network hosts
oping - sends ICMP_ECHO requests to network hosts

Package: fping
Priority: optional
…….
Description: sends ICMP ECHO_REQUEST packets to network hosts
fping is a ping like program which uses the Internet Control Message Protocol
(ICMP) echo request to determine if a target host is responding. fping
differs from ping in that you can specify
any number of targets on the command
line, or specify a file containing the lists of targets to ping. Instead of
sending to one target until it times out or replies, fping will send out a
ping packet and move on to the next target in a round - robin fashion.
Homepage: http://fping.sourceforge.net/
```
从结果中我们可以清晰地看到fping软件包的相关信息，包括名称、优先级、描述以及官网链接等。

### 三、深入挖掘软件包依赖关系
### （一）apt-cache depends：查找软件包依赖
语法：apt-cache depends <package_name>

作用：确定指定软件包所依赖的其他软件包。

### （二）查找fping依赖的软件包
在终端输入：
```bash
apt-cache depends fping
```
结果显示：
```
Depends: libc6
Conflicts: <suidmanager>
Replaces: <netstd>
```
这表明fping依赖于libc6这个软件包，同时与<suidmanager>存在冲突，并替换<netstd>。

### （三）apt-get rdepends：反向查找依赖该软件包的其他软件包
语法：apt-get rdepends <package_name>

作用：查找哪些软件包依赖于指定的软件包。

### （四）查找依赖fping的软件包
在终端输入：
```bash
apt-get rdepends fping
```
结果如下（部分展示）：
```
Reverse Depends:
mplayer
dvdrip
zabbix - server - pgsql
zabbix - server - mysql
zabbix - proxy - pgsql
zabbix - proxy - mysql
whereami
……
```
需要注意的是，只有depends才能确定真正的依赖性，反向的依赖性不一定可靠。例如，fping对于mplayer来说并非必需，而对于zabbix - server - mysql则是必需的，这可以通过进一步查看依赖关系来确认。

### （五）深入分析依赖关系
查看mplayer的依赖关系：
```bash
apt-cache depends mplayer
```
结果中显示：Suggests: fping，这说明fping对mplayer并不是必需的。

查看zabbix - server - mysql的依赖关系：
```bash
apt-cache depends zabbix - server - mysql
```
结果显示fping是Depends，这表明fping对zabbix - server - mysql是必需的。

### 四、安装软件包时的依赖处理
当我们使用apt-get install命令安装软件包时，以Depends或是Recommends开头的行中的包都将被安装，而以Suggests开头的行中的包不会被安装。这一点在我们管理软件包和系统环境时非常重要，能够帮助我们准确把握安装过程中软件包的引入情况。
