---
title: LINUX常用命令（基础）
id: 252
date: 2024-10-31 22:01:41
author: daichangya
excerpt: "LINUX常用命令（基础）

startx 切换到图形界面

1. man 对你熟悉或不熟悉的命令提供帮助解释

egman ls 就可以查看ls相关的用法

注：按q键或者ctrl+c退出，在linux下可以使用ctrl+c终止当前程序运行。

2. ls"
permalink: /archives/6831527/
tags: 
 - linux
---

LINUX常用命令（基础）

startx 切换到图形界面

1. man 对你熟悉或不熟悉的命令提供帮助解释

eg:man ls 就可以查看ls相关的用法

注：按q键或者ctrl+c退出，在linux下可以使用ctrl+c终止当前程序运行。

2. ls 查看目录或者文件的属*，列举出任一目录下面的文件

eg: ls /usr/man

ls -l

a.d表示目录(directory)，如果是一个"-"表示是文件，如果是l则表示是一个连接文件(link)

b.表示文件或者目录许可权限.分别用可读(r)，可写(w)，可运行(x)。

3. cp 拷贝文件

eg: cp filename1 filename2 //把filename1拷贝成filename2

cp 1.c netseek/2.c //将1.c拷到netseek目录下命名为2.c

4. rm 删除文件和目录

eg: rm 1.c //将1.c这个文件删除

5. mv 移走目录或者改文件名

eg: mv filename1 filename2 //将filename1 改名为filename2

mv qib.tgz ../qib.tgz //移到上一级目录

6. cd 改变当前目录 pwd 查看当前所在目录完整路径

eg: pwd //查看当前所在目录路径

cd netseek //进入netseek这个目录

cd //退出当前目录

7. cat，more命令

将某个文件的内容显示出来。两个命令所不同的是:cat把文件内容一直打印出来，而 more则分屏显示

eg; cat>1.c //就可以把代码粘帖到1.c文件里，按ctrl+d 保存代码。

cat 1.c 或more 1.c //都可以查看里面的内容。

gcc -o 1 1.c //将1.c编译成.exe文件，我们可以用此命编译出代码。

8.chmod 命令 权限修改 用法：chmod 一位8进制数 filename。

eg: chmod u+x filenmame //只想给自己运行，别人只能读

//u表示文件主人， g 表示文件文件所在组。 o 表示其他人 ;r 表可读，w 表可写，x 表可以运行

chmod g+x filename //同组的人来执行

9. clear，date命令

clear:清屏，相当与DOS下的cls;date:显示当前时间。

10. mount 加载一个硬件设备

用法:mount [参数] 要加载的设备 载入点

eg: mount /dev/cdrom

cd /mnt/cdrom //进入光盘目录

11. su 在不退出登陆的情况下，切换到另外一个人的身份

用法: su -l 用户名(如果用户名缺省，则切换到root状态)

eg:su -l netseek (切换到netseek这个用户，将提示输入密码)

12.whoami，whereis，which，id

//whoami:确认自己身份

//whereis:查询命令所在目录以及帮助文档所在目录

//which:查询该命令所在目录(类似whereis)

//id:打印出自己的UID以及GID。(UID:用户身份唯一标识。GID:用户组身份唯一标识。每一个用户只能有一个唯一的UID和 GID)

eg: whoami //显示你自已登陆的用户名

whereis bin 显示bin所在的目录，将显示为：/usr/local/bin

which bin

13. grep，find

grep:文本内容搜索;find:文件或者目录名以及权限属主等匹配搜索

eg: grep success * 　　 /*查找当前目录下面所有文件里面含有success字符的文件

14. kill 可以杀死某个正在进行或者已经是dest状态的进程

eg; ps ax

15. passwd 可以设置口令

16. history 用户用过的命令

eg: history //可以显示用户过去使用的命令

17. !! 执行最近一次的命令

18. mkdir命令

eg: mkdir netseek //创建netseek这个目录

19. tar 解压命令

eg: tar -zxvf nmap-3.45.tgz //将这个解压到nmap-3.45这个目录里

20. finger 可以让使用者查询一些其他使用者的资料

eg: finger //查看所用用户的使用资料

finger root //查看root的资料

Linux中常用的关机和重新启动命令有shutdown、halt、reboot以及init，它们都可以达到关机和重新启动的目的，但是每个命令的内部工作过程是不同的，下面将逐一进行介绍。

## 1. shutdown

shutdown命令用于安全关闭Linux系统。有些用户会使用直接断掉电源的方式来关闭Linux，这是十分危险的。因为Linux与Windows不同，其后台运行着许多进程，所以强制关机可能会导致进程的数据丢失，使系统处于不稳定的状态，甚至会损坏硬件设备。

执行shutdown命令时，系统会通知所有登录的用户系统将要关闭，并且login指令会被 冻结，即新的用户不能再登录系统。使用shutdown命令可以直接关闭系统，也可以延迟指定的时间再关闭系统，还可以重新启动。延迟指定的时间再关闭系 统，可以让用户有时间储存当前正在处理的文件和关闭已经打开的程序。

#### shutdown命令的部分参数如下：

　　[-t] 指定在多长时间之后关闭系统

　　[-r] 重启系统

　　[-k] 并不真正关机，只是给每个登录用户发送警告信号

　　[-h] 关闭系统（halt）

shutdown命令的工作实质是给init程序发送信号（signal），要求其切换系统的运行级别（Runlevel）。系统的运行级别包括：

　　0：关闭系统

1：单用户模式，如果没有为shutdown命令指定-h或-r参数而直接执行，则默认将切换到此运行级别

2：多用户模式（不支持NFS）

3：多用户模式（支持NFS），一般常用此种运行级别

5：多用户模式（GUI模式）

6：重新启动系统

## 2. halt

halt是最简单的关机命令，其实际上是调用shutdown -h命令。halt执行时，杀死应用进程，文件系统写操作完成后就会停止内核。

halt命令的部分参数如下：

　　[-f] 没有调用shutdown而强制关机或重启

　　[-i] 关机或重新启动之前，关掉所有的网络接口

　　[-p] 关机时调用poweroff，此选项为缺省选项

## 3.reboot

reboot的工作过程与halt类似，其作用是重新启动，而halt是关机。其参数也与halt类似。

## 4.init

init是所有进程的祖先，其进程号始终为1。init用于切换系统的运行级别，切换的工作是立即完成的。init 0命令用于立即将系统运行级别切换为0，即关机；init 6命令用于将系统运行级别切换为6，即重新启动。