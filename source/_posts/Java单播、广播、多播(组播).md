---
title: Java单播、广播、多播(组播)
id: 1489
date: 2024-10-31 22:01:57
author: daichangya
permalink: /archives/java%E5%8D%95%E6%92%AD%E5%B9%BF%E6%92%AD%E5%A4%9A%E6%92%AD%E7%BB%84%E6%92%AD/
tags: 
 - 网络
---



### 一、通信方式分类

　　在当前的网络通信中有三种通信模式：单播、广播和多播(组播)，其中多播出现时间最晚，同时具备单播和广播的优点。

*   单播：单台主机与单台主机之间的通信
*   广播：当台主机与网络中的所有主机通信
*   多播：当台主机与选定的一组主机的通信



### 二、单播　　

单播是网络通信中最常见的，网络节点之间的通信 就好像是人们之间的对话一样。如果一个人对另外一个人说话，

那么用网络技术的术语来描述就是“单播”，此时信息的接收和传递只在两个节点之间进行。

1\. 单播的优点：

(1)服务器以及响应客户端的请求；

(2)服务器能针对每个客户端的不同请求发送不同的响应，容易显示个性化服务；

2\. 单播的缺点：

服务器针对每个客户机发送数据流，服务器流量＝客户机数量×客户机流量；在客户数量大、每个客户机流量大的流媒体应用中服务器不堪重负；

3\. 应用场景：

单播在网络中得到了广泛的应用，网络上绝大部分的数据都 是以单播的形式传输的。例如：收发电子邮件、游览网页时，必须与邮件服务器、网站服务器建立连接，此时使用的就是单播通信方式；



### 三、广播

“广播”可以比方为：一个人通过广播喇叭对在场的全体说话(他才不管你是否乐意听)。换句话说: 广播是一台主机对某一个网络上的所有主机发送数据报包。这个网络可能是网络，也可能是子网，还有可能是所有子网。

广播有两类：本地广播和定向广播

*   定向广播：将数据报包发送到本网络之外的特定网络的所有主机，然而，由于互联网上的大部分路由器都不转发定向广播消息，所以这里不深入介绍了
*   本地广播：将数据报包发送到本地网络的所有主机，IPv4的本地广播地址为“255.255.255.255”，路由器不会转发此广播；

1.广播的优点：

(1)通信的效率高，信息一下子就可以传递到某一个网络上的所有主机。

(2)由于服务器不用向每个客户端单独发送数据，所以服务器流量比较负载低；

2.广播的缺点：

(1)非常占用网络的带宽；

(2)缺乏针对性,也不管主机是否真的需要接收该数据, 就强制的接收数据；

3.应用场景：

(1)有线电视就是典型的广播型网络

　　Java广播示例：

　　客户端发送程序　　

```
//发送端程序
public class BroadcastTest
{
    public static void main(String[] args)
    {
        //广播的实现 :由客户端发出广播，服务器端接收
        String host = "255.255.255.255";//广播地址
        int port = 9999;//广播的目的端口
        String message = "test";//用于发送的字符串
        try
        {
            InetAddress adds = InetAddress.getByName(host);
            DatagramSocket ds = new DatagramSocket();
            DatagramPacket dp = new DatagramPacket(message.getBytes(),message.length(), adds, port);
            ds.send(dp);
            ds.close();
        } 
        catch (Exception e) 
        {
            e.printStackTrace();
        }
    }
}
```

　　服务器端接收程序

```
//服务器端接收程序
public class BroadcastServer
{
     public static void main(String[] args) 
     {
            int port = 9999;//开启监听的端口
            DatagramSocket ds = null;
            DatagramPacket dp = null;
            byte[] buf = new byte[1024];//存储发来的消息
            StringBuffer sbuf = new StringBuffer();
            try 
            {
                //绑定端口的
                ds = new DatagramSocket(port);
                dp = new DatagramPacket(buf, buf.length);
                System.out.println("监听广播端口打开：");
                ds.receive(dp);
                ds.close();
                int i;
                for(i=0;i<1024;i++)
                {
                    if(buf[i] == 0)
                    {
                        break;
                    }
                    sbuf.append((char) buf[i]);
                }           
                System.out.println("收到广播消息：" + sbuf.toString());
            }
            catch (Exception e) 
            {
                e.printStackTrace();
            } 
        }
}
```



### 四、多播(组播)

　　”组播“可以比方为：你对着大街喊：”是男人的来一下，一人发一百块”，那么男的过来，女就不会过来,因为没有钱发她不理你(组播：其中所有的男生就是一个组)，换句话说: 组播是一台主机向指定的一组主机发送数据报包，因为如果采用单播方式，逐个节点传输，有多少个目标节点，就会有多少次传送过程，这种方式显然效率极低，是不可取的；如果采用不区分目标、全部发送的广播方式，虽然一次可以传送完数据，但是显然达不到区分特定数据接收对象的目的，又会占用网络带宽。采用组播方式，既可以实现一次传送所

有目标节点的数据，也可以达到只对特定对象传送数据的目的。

IP网络的组播一般通过组播IP地址来实现。组播IP地址就是D类IP地址，即224.0.0.0至239.255.255.255之间的IP地址。

1.组播的优点：

(1)具备广播所具备的所有优点；

(2)与单播相比，提供了发送数据报包的效率，与广播相比，减少了网络流量；

2.组播的缺点：

(1)与单播协议相比没有纠错机制，发生丢包错包后难以弥补，但可以通过一定的容错机制和QOS加以弥补；

　　组播的简单示例：

　　客户端发送消息

```
//发送端程序
public class SendUdp
{
    public static void main(String[] args) throws IOException
    {
        MulticastSocket ms=null; 
        DatagramPacket dataPacket = null; 
        ms = new MulticastSocket();
        ms.setTimeToLive(32);  
        //将本机的IP（这里可以写动态获取的IP）地址放到数据包里，其实server端接收到数据包后也能获取到发包方的IP的  
         byte[] data = "组播 测试".getBytes();   
         InetAddress address = InetAddress.getByName("239.0.0.255");   
         dataPacket = new DatagramPacket(data, data.length, address,8899);  
         ms.send(dataPacket);  
         ms.close();   
    }
}
```

　　服务器端接收程序：

```
//服务器端程序
public class TestMain
{
    private static MulticastSocket ds;  
    static String multicastHost="239.0.0.255";  
    static InetAddress receiveAddress; 
    public static void main(String[] args) throws IOException
    {
        ds = new MulticastSocket(8899);  
        receiveAddress=InetAddress.getByName(multicastHost);  
        ds.joinGroup(receiveAddress);  
        new Thread(new udpRunnable(ds)).start();  
    }
}
    class udpRunnable implements Runnable
    {
        MulticastSocket ds;
        public udpRunnable(MulticastSocket ds)
        {
            this.ds=ds;
        }
        public void run()
        {
             byte buf[] = new byte[1024];  
             DatagramPacket dp = new DatagramPacket(buf, 1024);  
             while (true) 
             {  
                    try
                    {  
                        ds.receive(dp);  
                        System.out.println("receive client message : "+new String(buf, 0, dp.getLength()));  
                    } 
                    catch (Exception e) 
                    {  
                        e.printStackTrace();  
                    }  
                }  
            
        }
}
```

　　运行结果截图：
![7137212015122410113370250849467.png](https://images.jsdiff.com/713721-20151224101133702-50849467_1602766861626.png)



### 五、参考资料

　　1、[http://www.2cto.com/kf/201312/264488.html](http://www.2cto.com/kf/201312/264488.html)
