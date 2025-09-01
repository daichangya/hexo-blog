---
title: Java设计模式——Reactor模式
id: 1506
date: 2024-10-31 22:01:59
author: daichangya
cover: https://images.jsdiff.com/design02.jpg
excerpt: Reactor模式 一、Web请求处理架构概述 在处理Web请求时，主要存在两种体系结构：thread - based architecture（基于线程）和event
  - driven architecture（事件驱动）。 （一）Thread - based Architecture（基于线程）
permalink: /archives/Java-she-ji-mo-shi-Reactor-mo-shi/
categories:
- 设计模式
tags:
- 设计模式
---

# Reactor模式

## 一、Web请求处理架构概述
在处理Web请求时，主要存在两种体系结构：thread - based architecture（基于线程）和event - driven architecture（事件驱动）。

### （一）Thread - based Architecture（基于线程）

![10345180faaebf9335592620.jpg](https://images.jsdiff.com/10345180-faaebf9335592620_1604030736144.jpg)

基于线程的体系结构通常采用多线程方式来处理客户端请求。每当接收到一个请求，就会开启一个独立的线程进行处理。这种方式在直观上易于理解，但存在一定局限性。每个线程都需要占用一定的内存资源，并且操作系统在线程之间切换时会产生开销。当并发访问量不大时，这种开销可能不明显，但随着线程数量增多，会显著降低Web服务器的性能。此外，当线程处理I/O操作并处于等待输入状态时，线程处于空闲状态，这期间会造成CPU资源的浪费。以下是其典型设计流程：
1. 客户端发起请求。
2. 服务器接收请求后，在单独的线程中进行读取（read）操作。
3. 对读取的数据进行解码（decode）。
4. 调用相应的处理程序（handler）进行业务逻辑处理，如计算（Compute）。
5. 对处理结果进行编码（encode）。
6. 最后将响应发送（send）回客户端。
以Java中简单的基于线程处理Web请求示例代码来看（此处仅示意，简化了诸多细节）：
```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;

public class ThreadBasedWebServer {
    public static void main(String[] args) throws IOException {
        ServerSocket serverSocket = new ServerSocket(8080);
        while (true) {
            final Socket clientSocket = serverSocket.accept();
            new Thread(() -> {
                try {
                    BufferedReader reader = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                    // 读取请求
                    String request = reader.readLine();
                    // 解码、处理逻辑（此处简单模拟，实际复杂得多）
                    String response = "Processed: " + request;
                    OutputStream outputStream = clientSocket.getOutputStream();
                    outputStream.write(response.getBytes());
                    clientSocket.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }).start();
        }
    }
}
```
上述代码在服务器端监听8080端口，每当有客户端连接，就新开一个线程处理请求，先读取输入流中的请求内容，简单加工后写回响应，不过实际场景中解码、复杂业务计算、编码等环节会有大量专业逻辑处理。

### （二）Event - driven Architecture（事件驱动）

![10345180fdaf4d307916cd8f.jpg](https://images.jsdiff.com/10345180-fdaf4d307916cd8f_1604030755918.jpg)

事件驱动体系结构是目前广泛使用的一种方式。它通过定义一系列事件处理器来响应事件的发生，并且将服务端接受连接与对事件的处理分离开来。这里的事件可以理解为一种状态的改变，例如在TCP中，socket的新连接到来（new incoming connection）、准备好读取（ready for read）、准备好写入（ready for write）等都属于事件。

## 二、Reactor模式介绍
Reactor模式是事件驱动体系结构的一种实现方式，主要用于处理多个客户端并发向服务端请求服务的场景。在服务端，每种服务可能由多个方法组成，Reactor模式能够解耦并发请求的服务，并将其分发给对应的事件处理器进行处理。目前，许多流行的开源框架都运用了Reactor模式，如Netty、Node.js等，Java的NIO也采用了该模式。其总体图示如下：
[此处可插入一张类似文中描述的Reactor模式架构图，包含客户端、Reactor、分发（dispatch）、各种处理操作（read、decode、Compute、encode、send）以及接受器（acceptor）等元素，以更直观展示流程]

### （一）Reactor模式的主要角色
1. **Handle**
   - 在Linux中一般称为文件描述符，在Windows中称为句柄，它们的含义相同。Handle是事件的发源地，比如一个网络socket、磁盘文件等都可以是Handle。而发生在Handle上的事件包括连接（connection）、准备好读取、准备好写入等。
2. **Synchronous Event Demultiplexer（同步事件分离器）**
   - 本质上是系统调用，例如Linux中的select、poll、epoll等。以select方法为例，它会一直阻塞，直到Handle上有事件发生时才会返回。在Java NIO中，使用`Selector`类来实现类似功能，示例如下：
```java
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.ServerSocketChannel;
import java.util.Iterator;
import java.util.Set;

public class NIOSelectorExample {
    public static void main(String[] args) throws IOException {
        // 创建ServerSocketChannel
        ServerSocketChannel serverSocketChannel = ServerSocketChannel.open();
        serverSocketChannel.bind(new InetSocketAddress(8080));
        // 设置为非阻塞模式
        serverSocketChannel.configureBlocking(false);
        // 创建Selector
        Selector selector = Selector.open();
        // 将ServerSocketChannel注册到Selector上，关注OP_ACCEPT事件（新连接事件）
        serverSocketChannel.register(selector, SelectionKey.OP_ACCEPT);
        while (true) {
            // 阻塞等待事件发生
            selector.select();
            // 获取发生事件的SelectionKey集合
            Set<SelectionKey> selectedKeys = selector.selectedKeys();
            Iterator<SelectionKey> iterator = selectedKeys.iterator();
            while (iterator.hasNext()) {
                SelectionKey key = iterator.next();
                // 处理不同类型事件，此处只是示例框架，具体处理逻辑要细化
                if (key.isAcceptable()) {
                    // 处理新连接事件
                } else if (key.isReadable()) {
                    // 处理可读事件
                } else if (key.isWritable()) {
                    // 处理可写事件
                }
                // 处理完后移除已处理的SelectionKey，避免重复处理
                iterator.remove();
            }
        }
    }
}
```
这段Java NIO代码中，先打开`ServerSocketChannel`绑定端口并设为非阻塞，通过`Selector`来等待诸如新连接、可读、可写等事件，根据不同事件类型后续会有对应处理分支，不过这里只是搭建了基础框架展示同步事件分离及初步事件判断逻辑。
3. **EventHandler（事件处理器）**
   - 事件处理器会定义一些回调方法（也称为钩子函数）。当Handle上有事件发生时，这些回调方法便会执行，从而实现一种事件处理机制。比如在一个自定义的网络事件处理框架里（伪代码示意结构）：
```java
interface EventHandler {
    void onConnect(Handle handle);
    void onReadable(Handle handle, byte[] data);
    void onWritable(Handle handle);
}
```
上述接口定义了连接、可读、可写等典型事件对应的回调方法，具体子类实现该接口填充对应业务逻辑。
4. **Concrete Event Handler（具体的事件处理器）**
   - 具体的事件处理器实现了EventHandler接口。在其回调方法中会实现具体的业务逻辑，针对不同类型的事件进行相应的处理。以处理HTTP请求的具体事件处理器为例（简化示意，聚焦于处理可读事件部分逻辑）：
```java
class HttpEventHandler implements EventHandler {
    @Override
    public void onConnect(Handle handle) {
        // 连接建立时处理，比如记录日志、初始化资源等
        System.out.println("New connection: " + handle);
    }

    @Override
    public void onReadable(Handle handle, byte[] data) {
        // 假设data是HTTP请求数据
        String request = new String(data);
        // 解析请求，提取方法、路径等信息
        String[] parts = request.split(" ");
        String method = parts[0];
        String path = parts[1];
        // 根据请求生成响应内容，这里简单返回固定响应
        String response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello, World!";
        try {
            // 将响应写回客户端，实际会更复杂涉及编码、状态管理等
            OutputStream outputStream = ((Socket) handle).getOutputStream();
            outputStream.write(response.getBytes());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void onWritable(Handle handle) {
        // 可写事件处理，比如发送缓存数据等，这里暂略具体逻辑细化
    }
}
```
这个`HttpEventHandler`针对HTTP请求中可读事件解析请求、生成并返回简单响应，展示具体业务处理细节在具体事件处理器中的落地。
5. **Initiation Dispatcher（初始分发器）**
   - 这也是Reactor模式中的一个重要角色，它提供了注册、删除与转发event handler的方法。当Synchronous Event Demultiplexer检测到Handle上有事件发生时，会通知Initiation Dispatcher调用特定的event handler的回调方法。以简易的Java类模拟分发器部分功能（省略部分错误处理、优化逻辑）：
```java
import java.util.HashMap;
import java.util.Map;

class InitiationDispatcher {
    private Map<Handle, EventHandler> handlerMap = new HashMap<>();
    // 注册事件处理器与对应Handle
    public void register(Handle handle, EventHandler eventHandler) {
        handlerMap.put(handle, eventHandler);
    }
    // 根据Handle获取对应的事件处理器
    public EventHandler getEventHandler(Handle handle) {
        return handlerMap.get(handle);
    }
    // 事件发生时调用此方法，分发处理逻辑
    public void handleEvent(Handle handle, int eventType) {
        EventHandler eventHandler = getEventHandler(handle);
        if (eventHandler!= null) {
            if (eventType == EventType.CONNECT) {
                eventHandler.onConnect(handle);
            } else if (eventType == EventType.READABLE) {
                byte[] data = readDataFromHandle(handle);  // 假设已有读取数据方法
                eventHandler.onReadable(handle, data);
            } else if (eventType == EventType.WRITABLE) {
                eventHandler.onWritable(handle);
            }
        }
    }
}
```
这个`InitiationDispatcher`类内部用`Map`维护Handle与事件处理器关联，在事件发生时分发调用对应处理器回调方法，虽简化但体现核心分发逻辑。

### （二）Reactor模式的处理流程
1. 应用向Initiation Dispatcher注册Concrete Event Handler时，需要标识出该事件处理器希望Initiation Dispatcher在何种类型的事件发生时向其通知，并且事件与Handle相关联。比如在上述`InitiationDispatcher`示例里，通过`register`方法将`HttpEventHandler`与对应的`Socket`类型`Handle`关联，并注明关注可读、连接等事件类型。
2. Initiation Dispatcher要求注册的Concrete Event Handler传递内部关联的Handle，该Handle会向操作系统标识，以便系统能够识别事件源。对应代码中`register`方法接收`Handle`并存储于`handlerMap`供后续识别事件源调用对应处理器。
3. 当所有的Concrete Event Handler都注册到Initiation Dispatcher上后，应用调用handle_events方法来启动Initiation Dispatcher的事件循环。此时，Initiation Dispatcher会将每个Concrete Event Handler关联的Handle合并，并使用Synchronous Event Demultiplexer来等待这些Handle上事件的发生。类似之前`NIOSelectorExample`中`selector.select()`开启阻塞等待事件循环，配合`InitiationDispatcher`关联处理后续流程。
4. 当与某个事件源对应的Handle变为ready时，例如TCP的socket变为ready for reading，Synchronous Event Demultiplexer便会通知Initiation Dispatcher。在Java NIO场景下就是`selector`检测到对应`SelectionKey`状态变化（如`isReadable`为`true`）后通知分发逻辑。
5. Initiation Dispatcher会触发事件处理器的回调方法。当事件发生时，Initiation Dispatcher会根据一个“key”（表示一个激活的Handle）来定位并分发给特定的EventHandler的回调方法，对应`InitiationDispatcher`类里`handleEvent`方法按`Handle`及事件类型调用对应`EventHandler`回调。
6. Initiation Dispatcher调用特定的Concrete Event Handler的回调方法来响应其关联的Handle上发生的事件，从而完成具体的业务逻辑处理，像`HttpEventHandler`里对可读事件解析请求、生成响应返回客户端实现业务闭环。

### （三）参考资料
 - https://dzone.com/articles/understanding-reactor-pattern-thread-based-and-eve
 - Reactor “An Object Behavioral Pattern for Demultiplexing and Dispatching Handles for Synchronous Events” Douglas C. Schmidt, Department of Computer Science, Washington University, St. Louis, MO
