---
title: java socket (回顾)
id: 851
date: 2024-10-31 22:01:46
author: daichangya
excerpt: "最近做项目，回想起了socket，做一个小例子回顾下，长期没有使用，忘记的差不多了。预期目标：客户端向服务器端发送消息，服务器端读取信息，回复客户端，循环往复。"
permalink: /archives/5644660/
categories:
 - java
---

最近做项目，回想起了socket，做一个小例子回顾下，长期没有使用，忘记的差不多了。

预期目标：客户端向服务器端发送消息，服务器端读取信息，回复客户端，循环往复。

server端代码：

```java
package com.dai.socket;
 
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;
 
/**
 * @Title: server.java * @Package com.dai.socket * @Description: TODO(添加描述) * @author 代长亚 * @date 2010-6-3 上午11:09:15 * @version V1.0
 */
public class Server {
    /**
     * @Fields name : TODO(用一句话描述这个变量表示什么)
     */
    private ServerSocket serverSocket = null;
    /**
     * @Fields name : TODO(用一句话描述这个变量表示什么)
     */
    private Socket socket = null;
 
    /**
     * <p>Title: </p> * <p>Description: </p>
     */
    public Server() { // TODO Auto-generated constructor stub
        try {
            serverSocket = new ServerSocket(8888);
            System.out.println("服务器端已经启动.....");
            while (true) {
                socket = serverSocket.accept(); //得到输入流
                DataInputStream dis = new DataInputStream(socket.getInputStream()); //得到输出流
                DataOutputStream dos = new DataOutputStream(socket.getOutputStream());
                System.out.println("客户端发来信息：" + dis.readUTF());
                System.out.print("请求回复信息：");
                Scanner sc = new Scanner(System.in);
                dos.writeUTF(sc.nextLine());
            }
        } catch (IOException e) { // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }
 
    /**
     * @Title: main * @Description: TODO(这里用一句话描述这个方法的作用) * @param args 设定文件 * @return void 返回类型 * @throws * @date 2010-6-3 上午11:09:15
     */
    public static void main(String[] args) { // TODO Auto-generated method stub
        new Server();
    }
}  
```

客户端代码：

```java
package com.dai.socket;
 
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.Scanner;
 
/**
 * @Title: Client.java * @Package com.dai.socket * @Description: TODO(添加描述) * @author 代长亚 * @date 2010-6-3 上午11:33:41 * @version V1.0
 */
public class Client {
    /**
     * @Fields name : TODO(用一句话描述这个变量表示什么)
     */
    private Socket socket = null;
 
    /**
     * <p>Title: </p> * <p>Description: </p>
     */
    public Client() {
        try {
            System.out.println("客户端已经启动.....");
            while (true) {
                socket = new Socket("127.0.0.1", 8888); //得到输入流 
                DataInputStream dis = new DataInputStream(socket.getInputStream()); //得到输出流 
                DataOutputStream dos = new DataOutputStream(socket.getOutputStream());
                System.out.print("请输入要发送的话：");
                Scanner sc = new Scanner(System.in);
                dos.writeUTF(sc.nextLine());
                System.out.println("服务器端：" + dis.readUTF());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
 
    /**
     * @Title: main * @Description: TODO(这里用一句话描述这个方法的作用) * @param args 设定文件 * @return void 返回类型 * @throws * @date 2010-6-3 上午11:33:41
     */
    public static void main(String[] args) {
        new Client();
    }
}  
```

回顾：

概念：

JAVA Socket简介  
所谓socket 通常也称作”套接字“，用于描述IP地址和端口，是一个通信链的句柄。应用程序通常通过”套接字”向网络发出请求或者应答网络请求。

以J2SDK-1.3为例，Socket和ServerSocket类库位于java.net包中。ServerSocket用于服务器端，Socket是建立网络连接时使用的。在连接成功时，应用程序两端都会产生一个Socket实例，操作这个实例，完成所需的会话。对于一个网络连接来说，套接字是平等的，并没有差别，不因为在服务器端或在客户端而产生不同级别。不管是Socket还是ServerSocket它们的工作都是通过SocketImpl类及其子类完成的。

重要的Socket API：

java.net.Socket继承于java.lang.Object，有八个构造器，其方法并不多，下面介绍使用最频繁的三个方法，其它方法大家可以见JDK-1.3文档。

. Accept方法用于产生”阻塞”，直到接受到一个连接，并且返回一个客户端的Socket对象实例。”阻塞”是一个术语，它使程序运行暂时”停留”在这个地方，直到一个会话产生，然后程序继续；通常”阻塞”是由循环产生的。

. getInputStream方法获得网络连接输入，同时返回一个InputStream对象实例。   
. getOutputStream方法连接的另一端将得到输入，同时返回一个OutputStream对象实例。

注意：其中getInputStream和getOutputStream方法均会产生一个IOException，它必须被捕获，因为它们返回的流对象，通常都会被另一个流对象使用。

SocketImpl介绍  
既然不管是Socket还是ServerSocket它们的工作都是通**过SocketImpl类及其子类完成的，那么当然要介绍啦。

抽象类 SocketImpl 是实际实现套接字的所有类的通用超类。创建客户端和服务器套接字都可以使用它。

这里稍微要注意的是端口的分配必须是唯一的.因为端口是为了唯一标识每台计算机唯一服务的.另外端口号是从0~65535之间的,前1024个端口已经被Tcp/Ip 作为保留端口,因此你所分配的端口只能是1024个之后的.