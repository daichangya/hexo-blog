---
title: Socket编程（C语言实现）——基于TCP协议，基于UDP协议(多线程，循环监听）(网络间通信AF_INET，典型的TCP/IP四型模型的通信过程)
id: 1491
date: 2024-10-31 22:01:57
author: daichangya
permalink: /archives/Socket-bian-cheng-C-yu-yan-shi-xian-ji/
tags:
- c
---

**Socket编程**

目前较为流行的网络编程模型是客户机/服务器通信模式

客户进程向服务器进程发出要求某种服务的请求，服务器进程响应该请求。如图所示，通常，一个服务器进程会同时为多个客户端进程服务，图中服务器进程B1同时为客户进程A1、A2和B2提供服务。

![](https://imgconvert.csdnimg.cn/aHR0cHM6Ly9pbWFnZXMyMDE1LmNuYmxvZ3MuY29tL2Jsb2cvNzkxMTAwLzIwMTYwNS83OTExMDAtMjAxNjA1MTAyMzA5NDQ0OTktMTU0ODI5ODQ0Ny5wbmc)

**Socket概述**

①   所谓Socket通常也称作“套接字”，用于描述IP地址和端口，是一个通信链的句柄。应用程序通常通过“套接字”向网络发出请求或者应答网络请求。

②   Socket是连接运行在网络上的两个程序间的双向通信的端点。

③   网络通讯其实指的就是Socket间的通讯。

④   通讯的两端都有Socket，数据在两个Socket之间通过IO来进行传输。

**套接字socket的类型**

（1）流式套接字（SOCK_STREAM)

提供面向连接、可靠的数据传输服务，数据无差错、无重复的发送，且按发送顺序接收（TCP协议）

（2）数据报式套接字（SOCK_DGRAM)

提供无连接服务，数据包以独立包形式发送，不提供无措保证，数据可能丢失，并且接收顺序混乱（UDP协议）

（3）原始套接字（SOCK_RAM)

**套接字（socket）**

socket起源于Unix，而Unix/Linux基本哲学之一就是“一切皆文件”，都可以用“打开open –> 读写write/read –> 关闭close”模式来操作。Socket就是该模式的一个实现,socket即是一种特殊的文件，一些socket函数就是对其进行的操作（读/写IO、打开、关闭）.说白了Socket是应用层与TCP/IP协议族通信的中间软件抽象层，它是一组接口。在设计模中，Socket其实就是一个门面模式，它把复杂的TCP/IP协议族隐藏在Socket接口后面，对用户来说，一组简单的接口就是全部，让Socket去组织数据，以符合指定的协议。

随着Unix的应用推广，套接字有被引进了windows等操作系统。套接字通常只与同一区域的套接字交换数据，windows socket只支持一个通信区域：**网际域（AF_INET)**,这个域被使用忘记协议簇的通信进程使用。

**使用Socket进行网络通信的过程**

①   服务器程序将一个套接字绑定到一个特定的端口，并通过此套接字等待和监听客户的连接请求。

②   客户程序根据服务器程序所在的主机和端口号发出连接请求。

③   如果一切正常，服务器接受连接请求。并获得一个新的绑定到不同端口地址的套接字。

④   客户和服务器通过读、写套接字进行通讯。

![](https://imgconvert.csdnimg.cn/aHR0cHM6Ly9pbWFnZXMyMDE1LmNuYmxvZ3MuY29tL2Jsb2cvNzkxMTAwLzIwMTYwNS83OTExMDAtMjAxNjA1MTAyMzEwMjUzMjctNzI5NTE2NzgzLnBuZw)

**客户机/服务器模式**

在TCP/IP网络应用中，通信的两个进程间相互作用的主要模式是客户机/服务器模式*(client/server)，即客户像服务其提出请求，服务器接受到请求后，提供相应的服务。

服务器：

（1）首先服务器方要**先启动**，打开一个通信通道并告知本机，它愿意在某一地址和端口上接收客户请求

（2）等待客户请求到达该端口

（3）接收服务请求，处理该客户请求，服务完成后，关闭此新进程与客户的通信链路，并终止

（4）返回第二步，等待另一个客户请求

（5）关闭服务器

客户方：

（1）打开一个通信通道，并连接到服务器所在的主机特定的端口

（2）向服务器发送请求，等待并接收应答，继续提出请求

（3）请求结束后关闭通信信道并终止

## **基于TCP（面向连接）的socket编程**

![](https://img-blog.csdn.net/20160516213313277)

>  **流式传输：**“客户端”，1.socket()函数；2.bind()函数可有可无，加上指定传输端口，不加随机分配端口；3.connect()函数，填写服务端的地址与端口【网络间通信AF\_STREAM】或者路径【进程间通信AF\_DGRAM】；4.send()函数；5.recv()函数。
> 
> **流式传输：**“服务端”，1.socket()函数；2.bind()函数，必须加上指定传输端口【网络间通信AF\_STREAM】或者是路径【进程间通信AF\_DGRAM】 ；3.listen()函数，使用isockfd；5.accepc()函数，生成新的fd，inewfd；6.send()函数，inewfd；7.recv()函数，inewfd。

服务器端先初始化Socket，然后与端口绑定(bind)，对端口进行监听(listen)，调用accept阻塞，等待客户端连接。在这时如果有个客户端初始化一个Socket，然后连接服务器(connect)，如果连接成功，这时客户端与服务器端的连接就建立了。客户端发送数据请求，服务器端接收请求并处理请求，然后把回应数据发送给客户端，客户端读取数据，最后关闭连接，一次交互结束。

### **基于TCP（面向连接）的socket编程——**流式套接字（SOCK_STREAM)  
网络间通信AF_INET，典型的TCP/IP四型模型的通信过程

服务器：

```objectivec
#include <stdio.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
 
#define PORT 23		//端口号
#define BACKLOG 5	//最大监听数
 
int main()
{
	int iSocketFD = 0;  //socket句柄
	int iRecvLen = 0;   //接收成功后的返回值
	int new_fd = 0; 	//建立连接后的句柄
	char buf[4096] = {0}; //
	struct sockaddr_in stLocalAddr = {0}; //本地地址信息结构图，下面有具体的属性赋值
	struct sockaddr_in stRemoteAddr = {0}; //对方地址信息
	socklen_t socklen = 0;  	
 
	iSocketFD = socket(AF_INET, SOCK_STREAM, 0); //建立socket
	if(0 > iSocketFD)
	{
		printf("创建socket失败！\n");
		return 0;
	}	
 
	stLocalAddr.sin_family = AF_INET;  /*该属性表示接收本机或其他机器传输*/
	stLocalAddr.sin_port = htons(PORT); /*端口号*/
	stLocalAddr.sin_addr.s_addr=htonl(INADDR_ANY); /*IP，括号内容表示本机IP*/
 
	//绑定地址结构体和socket
	if(0 > bind(iSocketFD, (void *)&stLocalAddr, sizeof(stLocalAddr)))
	{
		printf("绑定失败！\n");
		return 0;
	}
 
	//开启监听 ，第二个参数是最大监听数
	if(0 > listen(iSocketFD, BACKLOG))
	{
		printf("监听失败！\n");
		return 0;
	}
 
	printf("iSocketFD: %d\n", iSocketFD);	
	//在这里阻塞知道接收到消息，参数分别是socket句柄，接收到的地址信息以及大小 
	new_fd = accept(iSocketFD, (void *)&stRemoteAddr, &socklen);
	if(0 > new_fd)
	{
		printf("接收失败！\n");
		return 0;
	}else{
		printf("接收成功！\n");
		//发送内容，参数分别是连接句柄，内容，大小，其他信息（设为0即可） 
		send(new_fd, "这是服务器接收成功后发回的信息!", sizeof("这是服务器接收成功后发回的信息!"), 0);
	}
 
	printf("new_fd: %d\n", new_fd);	
	iRecvLen = recv(new_fd, buf, sizeof(buf), 0);	
	if(0 >= iRecvLen)    //对端关闭连接 返回0
	{	
		printf("接收失败或者对端关闭连接！\n");
	}else{
		printf("buf: %s\n", buf);
	}
 
	close(new_fd);
	close(iSocketFD);
 
	return 0;
}
```

客户端：

```objectivec
#include <stdio.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
 
#define PORT 23			//目标地址端口号
#define ADDR "192.168.1.230" //目标地址IP
 
int main()
{
	int iSocketFD = 0; //socket句柄
	unsigned int iRemoteAddr = 0;
	struct sockaddr_in stRemoteAddr = {0}; //对端，即目标地址信息
	socklen_t socklen = 0;  	
	char buf[4096] = {0}; //存储接收到的数据
 
	iSocketFD = socket(AF_INET, SOCK_STREAM, 0); //建立socket
	if(0 > iSocketFD)
	{
		printf("创建socket失败！\n");
		return 0;
	}	
 
	stRemoteAddr.sin_family = AF_INET;
	stRemoteAddr.sin_port = htons(PORT);
	inet_pton(AF_INET, ADDR, &iRemoteAddr);
	stRemoteAddr.sin_addr.s_addr=iRemoteAddr;
	
	//连接方法： 传入句柄，目标地址，和大小
	if(0 > connect(iSocketFD, (void *)&stRemoteAddr, sizeof(stRemoteAddr)))
	{
		printf("连接失败！\n");
		//printf("connect failed:%d",errno);//失败时也可打印errno
	}else{
		printf("连接成功！\n");
		recv(iSocketFD, buf, sizeof(buf), 0); 将接收数据打入buf，参数分别是句柄，储存处，最大长度，其他信息（设为0即可）。 
		printf("Received:%s\n", buf);
	}
	
	close(iSocketFD);//关闭socket	
	return 0;
}
```

测试：

1、编译服务器、客户端代码：

```
[root@localhost tcp_socket]# make socket_server_tcp
cc     socket_server_tcp.c   -o socket_server_tcp
[root@localhost tcp_socket]# make socket_client_tcp
cc     socket_client_tcp.c   -o socket_client_tcp
[root@localhost tcp_socket]# 
```

2、服务器端口监听：

```
[root@localhost tcp_socket]# ./socket_server_tcp 

```

3、执行客户端：

非telnet：

```
服务器端显示：
[root@localhost tcp_socket]# ./socket_server_tcp 
iSocketFD: 3
接收成功！
new_fd: 4
接收失败或者对端关闭连接！
 
客户端显示：
[root@localhost tcp_socket]# ./socket_client_tcp 
连接成功！
Received:这是服务器接收成功后发回的信息!
```

telnet服务器：

```
服务器端显示：
[root@localhost tcp_socket]# ./socket_server_tcp 
iSocketFD: 3
接收成功！
new_fd: 4
buf: �������� ��!��"��'����#
 
客户端显示：
[root@localhost tcp_socket]# telnet 192.168.1.230
Trying 192.168.1.230...
Connected to 192.168.1.230.
Escape character is '^]'.
这是服务器接收成功后发回的信息!Connection closed by foreign host.
```

## **基于UDP（面向无连接）的socket编程**

![](https://img-blog.csdn.net/20160516213559233)

> ** 报式传输：**“客户端”，1.socket()函数；2.bind()函数，绑定客户端的地址与端口【网络间通信AF\_STREAM】或者路径【进程间通信AF\_DGRAM】，以便于后续服务端sendto()函数参数的填写。若服务器端只是收不发数据，即，服务端有recvfrom()函数无sendto()函数，则客户端不需要bind()函数；若服务端要发送数据，即，有sendto（）函数，则客户端需要bind（）函数； 3.客户端sendto()函数参数，填写服务端的地址与端口【网络间通信AF\_STREAM】或者服务端路径【进程间通信AF\_DGRAM】的结构体地址与结构体长度，**服务端必须有bind()函数**；4.客户端recvfrom()函数参数，NULL，会自动识别。
> 
> **报式传输：**“服务端”，1.socket()函数；2.bind()函数，绑定客户端的地址与端口【网络间通信AF\_STREAM】或者路径【进程间通信AF\_DGRAM】，以便于后续客户端sendto()函数参数的填写。若服务器端只是收不发数据，即，服务端有recvfrom()函数无sendto()函数，则客户端不需要bind()函数；3.服务端sendto()函数参数，填写客户端的地址与端口【网络间通信AF\_STREAM】或者客户端路径【进程间通信AF\_DGRAM】的结构体地址与结构体长度，**服务端必须有bind()函数**；4.recvfrom()函数参数，NULL，会自动识别。

## **基于UDP（面向无连接）的socket编程——**数据报式套接字（SOCK_DGRAM)  
网络间通信AF_INET，典型的TCP/IP四型模型的通信过程

服务器：（多线程的【每10秒会打印一行#号】   与   循环监听）

```objectivec
#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <pthread.h>
 
void * test(void *pvData)
{
	while(1)
	{
		sleep(10);
		printf("################################\n");
	}
	return NULL;
}
 
int main(void)
{
	pthread_t stPid = 0; 
	int iRecvLen = 0;
	int iSocketFD = 0;
	char acBuf[4096] = {0};
	struct sockaddr_in stLocalAddr = {0};
 
	struct sockaddr_in stRemoteAddr = {0};
	socklen_t iRemoteAddrLen = 0;
 
	/* 创建socket */
	iSocketFD = socket(AF_INET, SOCK_DGRAM, 0);
	if(iSocketFD < 0)
	{
		printf("创建socket失败!\n");
		return 0;
	}
 
	/* 填写地址 */
	stLocalAddr.sin_family = AF_INET;
	stLocalAddr.sin_port   = htons(12345);
	stLocalAddr.sin_addr.s_addr = 0;
 
	/* 绑定地址 */
	if(0 > bind(iSocketFD, (void *)&stLocalAddr, sizeof(stLocalAddr)))
	{
		printf("绑定地址失败!\n");
		close(iSocketFD);
		return 0;
	}
	pthread_create(&stPid, NULL, test, NULL);   //实现了多线程
	
	while(1)     //实现了循环监听
	{
		iRecvLen = recvfrom(iSocketFD, acBuf, sizeof(acBuf), 0, (void *)&stRemoteAddr, &iRemoteAddrLen);
 
		printf("iRecvLen: %d\n", iRecvLen);
		printf("acBuf:%s\n", acBuf);
	}
	close(iSocketFD);
 
	return 0;
}
```

客户端：

```objectivec
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <arpa/inet.h>
 
int main(void)
{
	int iRecvLen = 0;
	int iSocketFD = 0;
	int iRemotAddr = 0;
	char acBuf[4096] = {0};
	struct sockaddr_in stLocalAddr = {0};
 
	struct sockaddr_in stRemoteAddr = {0};
	socklen_t iRemoteAddrLen = 0;
 
	/* 创建socket */
	iSocketFD = socket(AF_INET, SOCK_DGRAM, 0);
	if(iSocketFD < 0)
	{
		printf("创建socket失败!\n");
		return 0;
	}
 
	/* 填写服务端地址 */
	stLocalAddr.sin_family = AF_INET;
	stLocalAddr.sin_port   = htons(12345);
	inet_pton(AF_INET, "192.168.1.230", (void *)&iRemotAddr);
	stLocalAddr.sin_addr.s_addr = iRemotAddr;
 
	iRecvLen = sendto(iSocketFD, "这是一个测试字符串", strlen("这是一个测试字符串"), 0, (void *)&stLocalAddr, sizeof(stLocalAddr));
 
 
	close(iSocketFD);
 
	return 0;
}
```

测试：

1、编译服务器：因为有多线程，所以服务器端进程要进行pthread编译：

```
[root@localhost udp_socket]# gcc socket_server_UDP.c -pthread -g -o socket_server_UDP

```

2、服务器监听：

```
[root@localhost udp_socket]# ./socket_server_UDP 

```

3、客户端连接服务器：

```
[root@localhost tcp_socket]# ./socket_client_UDP 

```

4、服务器端口显示结果：

```
[root@localhost udp_socket]# ./socket_server_UDP 
iSocketFD: 3
################################
################################
iRecvLen: 27
acBuf:这是一个测试字符串
iSocketFD: 3
################################
```

5、结果解释说明:

服务器端有主线程和辅线程，主线程，打印客户端发送的请求；辅线程每隔10秒钟打印一排#号。

参考链接：[https://blog.csdn.net/zhang___yong/article/details/78702559](https://blog.csdn.net/zhang___yong/article/details/78702559)

java：[https://www.cnblogs.com/wzy330782/p/5479833.html](https://www.cnblogs.com/wzy330782/p/5479833.html)

基于TCP/IP和UDP协议的socket编程结构解析：[https://blog.csdn.net/zhengnice/article/details/51428080](https://blog.csdn.net/zhengnice/article/details/51428080)