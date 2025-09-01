---
title: EJB 工作原理
id: 864
date: 2024-10-31 22:01:47
author: daichangya
excerpt: "前两天在这个版块的精华区里翻到了Robbin关于EJB的调用原理的分析，受益非浅，但感觉用纯文字来表达效果似乎不够直观，而且对RMI的阐述也略嫌少了些。这里我根据自己的一点体会，在Robbin帖子的基础上再来说说这个话题，供大家参考。 

首先，我想先说说RMI的工作原理，因为EJB毕竟是基于RMI的嘛。废话就不多讲了，RMI的本质就是实现在不同JVM之间的调用，工作原理图如下："
permalink: /archives/7417273/
categories:
 - java
---



前两天在这个版块的精华区里翻到了Robbin关于EJB的调用原理的分析，受益非浅，但感觉用纯文字来表达效果似乎不够直观，而且对RMI的阐述也略嫌少了些。这里我根据自己的一点体会，在Robbin帖子的基础上再来说说这个话题，供大家参考。  
  
首先，我想先说说RMI的工作原理，因为EJB毕竟是基于RMI的嘛。废话就不多讲了，RMI的本质就是实现在不同JVM之间的调用，工作原理图如下：  
  
![](http://hi.csdn.net/attachment/201011/15/0_1289809392O430.gif)  
  
它的实现方法就是在两个JVM中各开一个Stub和Skeleton，二者通过socket通信来实现参数和返回值的传递。  
  
有关RMI的例子代码网上可以找到不少，但绝大部分都是通过extend the interface java.rmi.Remote实现，已经封装的很完善了，不免使人有雾里看花的感觉。下面的例子是我在《Enterprise JavaBeans》里看到的，虽然很粗糙，但很直观，利于很快了解它的工作原理。  
  
1\. 定义一个Person的接口，其中有两个business method, getAge() 和getName()  


	public interface Person {
		public int getAge(); throws Throwable;
		public String getName(); throws Throwable;
	}

  
  
2\. Person的实现PersonServer类  


	public class PersonServer implements Person {
		int age;
		String name;

		public PersonServer(String name, int age); {
			this.age = age;
			this.name = name;
		}

		public int getAge(); {
			return age;
		}

		public String getName(); {
			return name;
		}
	}

  
  
3\. 好，我们现在要在Client机器上调用getAge()和getName()这两个business method，那么就得编写相应的Stub(Client端)和Skeleton(Server端)程序。这是Stub的实现：  


	import java.io.ObjectOutputStream;
	import java.io.ObjectInputStream;
	import java.net.Socket;

	public class Person_Stub implements Person {
		Socket socket;

		public Person_Stub(); throws Throwable {
			// connect to skeleton
			socket = new Socket("computer_name", 9000);;
		}

		public int getAge(); throws Throwable {
			// pass method name to skeleton
			ObjectOutputStream outStream =
				new ObjectOutputStream(socket.getOutputStream(););;
			outStream.writeObject("age");;
			outStream.flush();;

			ObjectInputStream inStream =
				new ObjectInputStream(socket.getInputStream(););;
			return inStream.readInt();;
		}

		public String getName(); throws Throwable {
			// pass method name to skeleton
			ObjectOutputStream outStream =
				new ObjectOutputStream(socket.getOutputStream(););;
			outStream.writeObject("name");;
			outStream.flush();;

			ObjectInputStream inStream =
				new ObjectInputStream(socket.getInputStream(););;
			return (String);inStream.readObject();;
		}
	}

  
  
注意，Person\_Stub和PersonServer一样，都implements Person。它们都实现了getAge()和getName()两个business method，不同的是PersonServer是真的实现，Person\_Stub是建立socket连接，并向Skeleton发请求，然后通过Skeleton调用PersonServer的方法，最后接收返回的结果。  
  
4\. Skeleton实现  



	import java.io.ObjectOutputStream;
	import java.io.ObjectInputStream;
	import java.net.Socket;
	import java.net.ServerSocket;

	public class Person_Skeleton extends Thread {
		PersonServer myServer;

		public Person_Skeleton(PersonServer server); {
			// get reference of object server
			this.myServer = server;
		}

		public void run(); {
			try {
				// new socket at port 9000
				ServerSocket serverSocket = new ServerSocket(9000);;
				// accept stub's request
				Socket socket = serverSocket.accept();;

				while (socket != null); {
					// get stub's request
					ObjectInputStream inStream =
						new ObjectInputStream(socket.getInputStream(););;
					String method = (String);inStream.readObject();;

					// check method name
					if (method.equals("age");); {
						// execute object server's business method
						int age = myServer.getAge();;
						ObjectOutputStream outStream =
							new ObjectOutputStream(socket.getOutputStream(););;

						// return result to stub
						outStream.writeInt(age);;
						outStream.flush();;
					}

					if(method.equals("name");); {
						// execute object server's business method
						String name = myServer.getName();;
						ObjectOutputStream outStream =
							new ObjectOutputStream(socket.getOutputStream(););;

						// return result to stub
						outStream.writeObject(name);;
						outStream.flush();;
					}
				}
			} catch(Throwable t); {
				t.printStackTrace();;
				System.exit(0);;
			}
		}

		public static void main(String args \[\]); {
			// new object server
			PersonServer person = new PersonServer("Richard", 34);;

			Person\_Skeleton skel = new Person\_Skeleton(person);;
			skel.start();;
		}
	}

  
  
Skeleton类 extends from Thread，它长驻在后台运行，随时接收client发过来的request。并根据发送过来的key去调用相应的business method。  
  
5\. 最后一个，Client的实现  

```
	public class PersonClient {
		public static void main(String \[\] args); {
			try {
				Person person = new Person_Stub();;
				int age = person.getAge();;
				String name = person.getName();;
				System.out.println(name + " is " + age + " years old");;
			} catch(Throwable t); {
				t.printStackTrace();;
			}
		}
	}
```
  
  
Client的本质是，它要知道Person接口的定义，并实例一个Person_Stub，通过Stub来调用business method，至于Stub怎么去和Server沟通，Client就不用管了。  
  
注意它的写法：  

	Person person = new Person_Stub();  

而不是  

	Person_Stub person = new Person_Stub();  
  
为什么？因为要面向接口编程嘛，呵呵。  
  
感谢您有耐心看到这里，关于RMI，我想说的就这么多了。但是好象还没写到EJB，本人就累了个半死，算了，我还是先去睡觉，明天再往下续吧。。。
