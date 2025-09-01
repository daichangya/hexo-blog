---
title: spymemcached源码深入分析
id: 0b1e629f-ffb5-43c2-91db-08ef1acf139e
date: 2024-11-09 14:05:06
author: daichangya
excerpt: "一、简介 spymemcached 是一款使用 NIO 实现的 memcache 客户端，在理解它之前，需要先了解 NIO、memcached 使用和 memcached 协议相关知识。 （一）NIO 相关概念 在 Java 中，NIO 常被称为异步 IO，在 Linux 系统编程中，它实际上是事件"
permalink: /archives/spymemcachedyuan-ma-shen-ru-fen-xi/
---

## **一、简介**

spymemcached 是一款使用 NIO 实现的 memcache 客户端，在理解它之前，需要先了解 NIO、memcached 使用和 memcached 协议相关知识。

### **（一）NIO 相关概念**

在 Java 中，NIO 常被称为异步 IO，在 Linux 系统编程中，它实际上是事件驱动 IO（event - driven IO），是对 epoll 的封装。

IO 模型还有多种类型：

1.  **阻塞 / 非阻塞**：这是文件描述符（fd）的属性。阻塞情况下，应用会一直睡眠直到 IO 完成被内核唤醒；同步非阻塞时，若第一次读取无数据，应用线程会立刻返回，但后续需要确定系统调用策略，简单的 while 循环可能导致 CPU 100% 占用，复杂策略又会增加编程难度，所以这种方式很少使用。
    
2.  **多路复用**：这是 Linux 早期进程监控多个 fd 的方式，不过其性能较低，每次调用涉及 3 次循环遍历。
    
3.  **事件驱动 IO**：应用注册感兴趣的 socket IO 事件（如 READ、WRITE）后调用 wait 开始睡眠，当条件满足（如数据到达可读、写缓冲区可用可写）时，内核唤醒应用线程，应用线程根据 socket 执行同步读 / 写数据操作。
    

## **二、协议简介**

  

memcached 服务器与客户端采用 TCP 通信，其协议为自定义字节流格式。

### **（一）文本协议**

  

1.  **组成**：文本协议分命令行和数据块行，命令行指明数据块字节数目，命令行和数据块后都跟 \\r\\n。服务器读取数据块依据命令行指定字节数，数据块含 \\r 或 \\n 不影响读块操作，但数据块后必须有 \\r\\n。
    
2.  **存储命令**
    
    +   **发送格式**：
        
        +   `<command name> <key> <flags> <exptime> <bytes> [noreply]\r\n`，其中`command name`可为`"set"`、`"add"`、`"replace"`、`"append"`或`"prepend"`；`flags`是 32 位整数，服务器不操作，`get`时返回客户端；`exptime`是过期时间，可为 unix 时间戳或偏移量，偏移量最大为`30*24*60*60`，超此值视为 unix 时间戳；`bytes`是数据块字节个数。
            
        +   `cas <key> <flags> <exptime> <bytes> <cas unique> [noreply]\r\n`。
            
        +   `<data block>\r\n`。
            
    +   **响应格式**：
        
        +   `<data block>\r\n`。
            
        +   `STORED\r\n`（成功）。
            
        +   `NOT_STORED\r\n`（`add`或`replace`命令未满足条件）。
            
        +   `EXISTS\r\n`（`cas`命令，表明`item`已被修改）。
            
        +   `NOT_FOUND\r\n`（`cas`命令，`item`不存在）。
            
3.  **获取命令**
    
    +   **发送格式**：`get <key>*\r\n`或`gets <key>*\r\n`（`<key>*`是空格分割的一个或多个字符串）。
        
    +   **响应格式**：
        
        +   `VALUE <key> <flags> <bytes> [<cas unique>]\r\n`。
            
        +   `<data block>\r\n`（可能多个）。
            
        +   `END\r\n`。
            
4.  **删除命令**
    
    +   **发送格式**：`delete <key> [noreply]\r\n`。
        
    +   **响应格式**：
        
        +   `DELETED\r\n`（成功删除）。
            
        +   `NOT_FOUND\r\n`（删除条目不存在）。
            
5.  **其他命令**：详见参考资料 mc 协议。
    

## **三、spymemcached 中的重要对象**

### **（一）整体架构相关对象**

  

1.  **MemcachedClient**：表示 mc 集群客户端，在应用中常为单例。它内部持有 MemcachedConnection（`mconn`）等重要组件，是客户端操作的入口。
    
2.  **MemcachedConnection**：表示到 mc 集群的连接，内部持有`locator`等。它是与服务器通信的关键连接对象，因使用 NIO，有`selector`用于监控读写事件。
    
3.  **NodeLocator**：根据`key`的哈希值查找节点，默认是`ArrayModNodeLocator`，哈希算法在`DefaultHashAlgorithm`中，默认是`NATIVE_HASH`（即`String.hashCode()`）。它决定了数据存储和获取时如何定位到具体的 memcached 服务器。
    
4.  **TranscodeService**：执行字节数据和对象的转换，实现方式为任务队列 + 线程池，其实例在`client`中。这个对象对于数据的处理和转换至关重要，确保客户端和服务器之间数据格式的正确交互。
    

### **（二）单个节点相关对象**

  

1.  **MemcachedNode**：表示每个 mc 节点，内部含`channel`用于网络连接。它是与单个 memcached 服务器交互的基础对象，有很多重要属性。例如`socketAddress`（服务器地址）、`rbuf`（读缓冲区，默认大小 16384）、`wbuf`（写缓冲区，默认大小 16384）、`writeQ`（写队列）、`readQ`（读队列）、`inputQueue`（输入队列，`memcachclient`添加操作先添加到此队列）、`opQueueMaxBlockTime`（操作最大阻塞时间，默认 10 秒）、`reconnectAttempt`（重连尝试次数，`volatile`）、`channel`（socket 通道）、`toWrite`（要向 socket 发送的字节数）、`optimizedOp`（优化后的`Operation`实现类是`OptimizedGetImpl`）、`sk`（`channel`注册到`selector`后的`key`）、`shouldAuth`（是否需要认证，默认`false`）、`authLatch`（认证所需`Latch`）、`reconnectBlocked`、`defaultOpTimeout`（操作默认超时时间，默认值 2.5 秒）、`continuousTimeout`（连续超时次数）、`opFact`（操作工厂）。
    
2.  **ConnectionFactory**：创建`MemcachedConnection`实例、操作队列、`OperationFactory`并制定`Hash`算法，`DefaultConnectionFactory`是默认连接工厂。它是构建整个连接相关对象的工厂类。
    

### **（三）操作相关对象**

  

1.  **Operation**：所有与服务器操作通信、协议数据发送和解析都抽象为`Operation`，文本协议`get`操作最终实现为`net.spy.memcached.protocol.ascii.GetOperationImpl`。不同类型的操作（如存储、获取、删除等）都有相应的`Operation`实现类。
    
2.  **OperationFactory**：为协议构建操作，如`BaseOperationFactory`、`AsciiOperationFactory`（文本协议操作工厂，默认）、`BinaryOperationFactory`（二进制协议操作工厂），根据`protocol handlers`构建操作。
    
3.  **GetFuture**：为实现工作线程和 IO 线程调度而抽象出的对象，内部持有`OperationFuture`。它在多线程交互中起到协调作用，确保工作线程能正确获取 IO 线程执行操作的结果。
    

### **（四）其他基础对象**

  

1.  **SpyObject**：是 spy 中的基类，定义`Logger`，为其他类提供了日志相关的功能基础。
    
2.  **DefaultHashAlgorithm**：`Hash`算法实现类，决定了如何根据键计算出存储或获取数据的节点位置。
    
3.  **FailureMode**：定义了 node 失效模式，包括`Redistribute`（节点失效后移到下一个有效节点，默认）、`Retry`（重试失效节点直至恢复）、`Cancel`（取消操作）。这对于处理节点故障情况非常重要，影响着系统的可靠性和数据一致性。
    

## **四、整体流程**

### **（一）初始化流程**

  

客户端执行`new MemcachedClient(new InetSocketAddress("192.168.56.101", 11211))`初始化`MemcachedClient`。在这个过程中，内部会初始化`MemcachedConnection`，包括创建`selector`，将`channel`注册到`selector`，然后启动 IO 线程，准备接收和处理服务器相关的事件。

### **（二）线程模型与交互**

  

1.  **线程模型**：初始化完成后，有专门监听 mc 节点事件的 IO 线程，由`select`调用；当应用执行`c.get("someKey")`等操作时，所在的线程为工作线程（通常由 tomcat 启动，数量可以有多个），工作线程负责创建操作并加入节点操作队列。
    
2.  **工作线程操作**：工作线程调用`asyncGet`方法，首先会创建`CountDownLatch(1)`、`GetFuture`、`GetOperationImpl`，然后选择 mc 节点，对操作`op`进行初始化（生成写缓冲区），将操作放入节点等待队列`inputQueue`，同时将当前节点放入`mc`连接（`mconn`）的`addedQueue`属性，最后唤醒`selector`，并在`latch`上等待（默认超时 2.5 秒）IO 线程执行结果。
    
3.  **IO 线程操作**
    
    +   **handleInputQueue()**：将`Operation`从`inputQueue`移动到`writeQ`，处理`addedQueue`中的节点，把节点`inputQueue`操作复制到`writeQ`，根据节点是否有写操作来注册读写事件（有写操作才处理，否则只注册写事件）。
        
    +   **循环处理读写事件**：当节点无写操作时，根据`writeQ`、`readQ`情况注册读写事件；有写操作时执行`handleWrites`函数，包括填充缓冲区（从`writeQ`取可写操作，复制数据到写缓冲区，改变操作状态，从`writeQ`移除并加入`readQ`，处理`pending`操作）、发送缓冲区内容（若命令大可能多次填充发送），循环直到所有写操作处理完，最后更新`sk`注册的读写事件（`get`操作此时已注册读事件）。然后执行`selector.select()`等待事件就绪，当数据到达时，执行`handleIO(sk)`处理读事件，通过`channel.read(rbuf)`读取数据，`readFromBuffer()`解析数据，读到`END\r\n`将操作状态置为`COMPLETE`。
        

## **五、初始化详细流程**

  

1.  首先，默认连接工厂为`DefaultConnectionFactory`，接着创建`TranscodeService`（解码线程池，默认最多 10 个线程）、`AsciiOperationFactory`（支持 ascii 协议操作工厂）、`MemcachedConnection`，并设置操作超时时间（默认 2.5 秒）。
    
2.  `DefaultConnectionFactory`创建`MemcachedConnection`的详细过程如下：创建`reconnectQueue`、`addedQueue`，设置`shouldOptimize`为`true`、`maxDelay`为 30 秒、`opFact`、`timeoutExceptionThreshold`为 1000（超此值关闭到`mc node`连接），打开`Selector`，创建`nodesToShutdown`，设置`bufSize`为 16384 字节，创建到每个`node`的`MemcachedNode`（默认`AsciiMemcachedNodeImpl`，包括创建`SocketChannel`、连接到`mc`节点、注册到`selector`、设置`sk`），最后启动`MemcachedConnection`线程进入事件处理循环`while(running) handleIO()`。
    

## **六、核心流程代码**

### **（一）工作线程核心代码**

  

1.  从`c.get("someKey")`开始，流程为创建操作（`Operation`）、操作初始化、查找节点、加入节点等待队列、唤醒 IO 线程，然后在`Future`上等待 IO 线程执行结果。关键代码如下：
    

```
// 默认等待2.5秒
return asyncGet(key, tc).get(2500, TimeUnit.MILLISECONDS);

public <T> GetFuture<T> asyncGet(final String key, final Transcoder<T> tc) {
    final CountDownLatch latch = new CountDownLatch(1);
    final GetFuture<T> rv = new GetFuture<T>(latch, operationTimeout, key);
    Operation op = opFact.get(key, new GetOperation.Callback() {
        private Future<T> val = null;
        public void receivedStatus(OperationStatus status) {
            rv.set(val, status);
        }
        public void gotData(String k, int flags, byte[] data) {
            val = tcService.decode(tc, new CachedData(flags, data, tc.getMaxSize()));
        }
        public void complete() {
            latch.countDown();
        }
    });
    rv.setOperation(op);
    mconn.enqueueOperation(key, op);
    return rv;  
}

protected void addOperation(final String key, final Operation o) {
    MemcachedNode placeIn = null;
    MemcachedNode primary = locator.getPrimary(key);
    if (primary.isActive() || failureMode == FailureMode.Retry) {
        placeIn = primary;
    } else if (failureMode == FailureMode.Cancel) {
        o.cancel();
    } else {
        for (Iterator<MemcachedNode> i = locator.getSequence(key); placeIn == null
                && i.hasNext();) {
            MemcachedNode n = i.next();
            if (n.isActive()) {
                placeIn = n;
            }
        }
        if (placeIn == null) {
            placeIn = primary;
        }
    }
    if (placeIn!= null) {
        addOperation(placeIn, o);
    } else {
    }
}

protected void addOperation(final MemcachedNode node, final Operation o) {
    o.setHandlingNode(node);
    o.initialize();  
    node.addOp(o);  
    addedQueue.offer(node);  
    Selector s = selector.wakeup(); 
}
```

  

2.  工作线程和 IO 线程传递的`Future`对象结构：`GetFuture ---> OperationFuture ---> latch`，工作线程最终在`OperationFuture`的`get`方法上等待`latch`，`objRef`引用`TranscodeService.Task`（`FutureTask`）对象，无压缩序列化时，工作线程调用`tc.decode`方法获取返回值。
    

### **（二）IO 线程核心代码**

  

1.  **操作循环**：`public void run() { while (running) { handleIO(); } }`，`handleIO`方法处理输入队列、注册写事件、执行写操作、注册读事件、处理读操作并解析结果。
    
2.  **handleInputQueue**：处理`addedQueue`中的节点，复制`inputQueue`操作到`writeQ`，注册读写事件。关键代码如下：
    

```
private void handleInputQueue() {
    if (!addedQueue.isEmpty()) {
        Collection<MemcachedNode> toAdd = new HashSet<MemcachedNode>();
        Collection<MemcachedNode> todo = new HashSet<MemcachedNode>();
        MemcachedNode qaNode = null;
        while ((qaNode = addedQueue.poll())!= null) {
            todo.add(qaNode);
        }
        for (MemcachedNode qa : todo) {
            boolean readyForIO = false;
            if (qa.isActive()) {
                if (qa.getCurrentWriteOp()!= null) {
                    readyForIO = true;
                }
            } else {
                toAdd.add(qa);
            }
            qa.copyInputQueue();
            if (readyForIO) {
                try {
                    if (qa.getWbuf().hasRemaining()) {
                        handleWrites(qa.getSk(), qa);
                    }
                } catch (IOException e) {
                    lostConnection(qa);
                }
            }
            qa.fixupOps();
        }
        addedQueue.addAll(toAdd);
    }
}
```

  

3.  **handleWrites(SelectionKey sk, MemcachedNode qa)**：处理节点`writeQ`和`inputQueue`操作，循环填充发送缓冲区并发送数据，将发送缓冲区内容放入`readQ`，根据`writeQ`和`readQ`状态注册读写事件。关键代码如下：
    

```
private void handleWrites(SelectionKey sk, MemcachedNode qa) throws IOException {
    qa.fillWriteBuffer(shouldOptimize); 
    boolean canWriteMore = qa.getBytesRemainingToWrite() > 0;
    while (canWriteMore) {
        int wrote = qa.writeSome(); 
        qa.fillWriteBuffer(shouldOptimize);
        canWriteMore = wrote > 0 && qa.getBytesRemainingToWrite() > 0;
    }
}

public final int writeSome() throws IOException {
    int wrote = channel.write(wbuf);
    toWrite -= wrote;
    return wrote;
}

public final void fillWriteBuffer(boolean shouldOptimize) {
    if (toWrite == 0 && readQ.remainingCapacity() > 0) {
        getWbuf().clear();
        Operation o = getNextWritableOp(); 
        while (o!= null && toWrite < getWbuf().capacity()) {
            synchronized (o) {
                ByteBuffer obuf = o.getBuffer();
                int bytesToCopy = Math.min(getWbuf().remaining(), obuf.remaining());
                byte[] b = new byte[bytesToCopy];
                obuf.get(b);
                getWbuf().put(b);
                if (!o.getBuffer().hasRemaining()) {
                    o.writeComplete();
                    transitionWriteItem();
                    preparePending(); 
                    if (shouldOptimize) {
                        optimize();
                    }
                    o = getNextWritableOp();
                }
                toWrite += bytesToCopy;
            }
        }
        getWbuf().flip();
    } else {
    }
}
```

4.  **handleReads**：从网络中读取数据放入`rbuf`，然后解析`rbuf`得到结果。关键代码如下：
    

```
private void handleReads(SelectionKey sk, MemcachedNode qa) throws IOException {
    Operation currentOp = qa.getCurrentReadOp();
    if (currentOp instanceof TapAckOperationImpl) { 
        qa.removeCurrentReadOp();
        return;
    }
    ByteBuffer rbuf = qa.getRbuf();
    final SocketChannel channel = qa.getChannel();
    int read = channel.read(rbuf);
    if (read < 0) {
        // 处理连接关闭等情况
    } else {
        // 解析数据
    }
}
```

### **（三）代码流程总结**

  

1.  **工作线程与 IO 线程协作**
    
    +   工作线程创建操作并将其放入节点的输入队列，同时唤醒 IO 线程。IO 线程在被唤醒后，处理输入队列中的操作，将其移动到写队列并准备发送数据。在发送数据过程中，涉及缓冲区的填充和数据的实际发送，操作状态也会相应改变。数据发送完成后，IO 线程等待服务器响应数据，收到数据后进行解析，并根据解析结果更新操作状态。工作线程则在`Future`上等待 IO 线程完成操作，获取最终结果。
        
2.  **数据流向与处理**
    
    +   客户端要存储数据时，工作线程构建存储命令的字节流数据（包含命令名、键、标志、过期时间、字节数等），放入写缓冲区，然后通过 IO 线程将数据发送到服务器。服务器根据协议解析数据并存储，返回相应状态（如`STORED`等）。获取数据时，工作线程发送获取命令，IO 线程接收服务器返回的数据（包含键、标志、字节数、数据块等），经过解析后，将数据转换为对象返回给工作线程。在整个过程中，数据在缓冲区之间进行转移和处理，确保数据的正确传输和转换。
        

### **（四）性能优化与注意事项**

  

1.  **性能优化点**
    
    +   **缓冲区管理**：写缓冲区（`wbuf`）和读缓冲区（`rbuf`）的合理利用对性能有影响。例如，在`fillWriteBuffer`方法中，会尽量填满写缓冲区后再发送数据，减少网络 IO 次数。同时，缓冲区大小的设置（默认 16384 字节）也需要根据实际情况进行调整，如果数据量较大且频繁，可以适当增大缓冲区大小，但也要考虑内存占用。
        
    +   **操作优化**：`shouldOptimize`属性用于优化多个连续的`get`操作（默认为`true`），会将多个`get`操作合并为一个`gets`操作，减少网络请求开销。在`fillWriteBuffer`方法中，如果`shouldOptimize`为`true`，还会进行一些额外的优化操作（如`optimize`方法，虽然文章未详细给出其实现，但可推测是针对连续`get`操作的进一步优化）。
        
    +   **连接管理**：`MemcachedConnection`中的`reconnectQueue`、`addedQueue`等队列用于管理连接相关操作，合理处理连接的重连、节点的添加等操作，可以提高系统的稳定性和性能。例如，在`handleInputQueue`方法中，对节点的状态进行判断和处理，确保只有活动节点才进行 IO 操作，避免无效操作。
        
2.  **注意事项**
    
    +   **操作超时处理**：每个操作都有默认的超时时间（`defaultOpTimeout`，默认 2.5 秒），如果操作超时未完成，工作线程会进行相应处理（如抛出异常等）。在`asyncGet`方法中可以看到，工作线程在`Future`上等待结果时，会判断是否超时。因此，在实际应用中，需要根据业务需求合理设置超时时间，避免因超时而导致业务逻辑错误或性能下降。
        
    +   **节点失效处理**：`FailureMode`定义了节点失效后的处理方式，不同的处理方式对系统的可用性和数据一致性有不同影响。例如，`Redistribute`模式会将操作移到下一个有效节点，可能会导致数据在不同节点间的重新分布，需要考虑数据一致性问题；`Retry`模式会重试失效节点，可能会增加延迟；`Cancel`模式则直接取消操作，可能会影响业务流程。在实际应用中，需要根据系统需求选择合适的节点失效处理模式。
        
    +   **并发控制**：多个工作线程可能同时对节点进行操作，需要注意并发控制。例如，在`addOperation`方法中，对节点的选择和操作入队需要考虑并发情况，避免数据竞争。同时，在操作节点的队列（如`writeQ`、`readQ`等）时，也需要进行适当的同步（如使用`synchronized`关键字），确保操作的正确性。
        

### **（五）应用场景与扩展**

  

1.  **适用场景**
    
    +   spymemcached 适用于需要高性能缓存的场景，如 Web 应用中对频繁访问的数据进行缓存，减轻数据库压力，提高响应速度。例如，在电商网站中，可以缓存商品信息、用户购物车数据等，减少对数据库的查询次数。在社交网络应用中，缓存用户动态、好友列表等信息，提升用户体验。
        
    +   由于其支持分布式集群，可以方便地扩展缓存容量，适用于大规模数据缓存需求。比如大型互联网公司的多个服务之间共享缓存数据，通过多个 memcached 节点组成集群，spymemcached 客户端可以根据键的哈希值将数据分布存储在不同节点上，实现数据的分布式存储和高效访问。
        
2.  **扩展方向**
    
    +   **协议支持扩展**：可以根据需求扩展支持更多的 memcached 协议特性或自定义协议。例如，当前支持文本协议和二进制协议，如果未来 memcached 服务器有新的协议特性，可以在`OperationFactory`等相关类中进行扩展，添加新的操作实现类来支持新协议。
        
    +   **性能优化扩展**：进一步优化客户端性能，如改进缓冲区管理策略，动态调整缓冲区大小以适应不同数据量的操作。或者优化节点选择算法，提高数据分布的均匀性和缓存命中率。例如，研究更先进的一致性哈希算法替代现有的`ArrayModNodeLocator`或`KetamaNodeLocator`，以更好地应对节点的动态增减情况。
        
    +   **功能增强扩展**：增加一些高级功能，如数据压缩功能，在客户端发送数据前进行压缩，减少网络传输带宽占用，服务器接收后再解压；或者添加数据加密功能，保障缓存数据的安全性，适用于对数据安全要求较高的应用场景。还可以实现与其他分布式系统的集成，如与分布式文件系统结合，实现缓存数据的持久化存储和快速恢复。