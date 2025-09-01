---
title: SocketChannel 读取ByteBuf 的过程
id: 1535
date: 2024-10-31 22:02:00
author: daichangya
permalink: /archives/socketchannel%E8%AF%BB%E5%8F%96bytebuf%E7%9A%84%E8%BF%87%E7%A8%8B/
categories:
 - netty
---



## SocketChannel 读取ByteBuf 的过程：

　　我们首先看NioEventLoop 的processSelectedKey 方法：

```
private void processSelectedKey(SelectionKey k, AbstractNioChannel ch) {
　　//获取到channel 中的unsafe
　　final AbstractNioChannel.NioUnsafe unsafe = ch.unsafe();
　　//如果这个key 不是合法的, 说明这个channel 可能有问题
　　if (!k.isValid()) {
　　　　//代码省略
　　}
　　try {
　　　　//如果是合法的, 拿到key 的io 事件
　　　　int readyOps = k.readyOps();
　　　　//链接事件
　　　　if ((readyOps & SelectionKey.OP_CONNECT) != 0) {
　　　　　　int ops = k.interestOps();
　　　　　　ops &= ~SelectionKey.OP_CONNECT;
　　　　　　k.interestOps(ops);
　　　　　　unsafe.finishConnect();
　　　　}　　　　//写事件
　　　　if ((readyOps & SelectionKey.OP_WRITE) != 0) {
　　　　　　ch.unsafe().forceFlush();
　　　　}　　　　//读事件和接受链接事件
　　　　//如果当前NioEventLoop 是work 线程的话, 这里就是op_read 事件
　　　　//如果是当前NioEventLoop 是boss 线程的话, 这里就是op_accept 事件
　　　　if ((readyOps & (SelectionKey.OP_READ | SelectionKey.OP_ACCEPT)) != 0 || readyOps == 0) {
　　　　　　unsafe.read();
　　　　　　if (!ch.isOpen()) {
　　　　　　　　return;
　　　　　　}
　　　　}
　　} catch (CancelledKeyException ignored) {
　　　　unsafe.close(unsafe.voidPromise());
　　}
}
```

　　if ((readyOps & (SelectionKey.OP\_READ | SelectionKey.OP\_ACCEPT)) != 0 || readyOps == 0) 这里的判断表示轮询到事件是OP\_READ 或者OP\_ACCEPT 事件。之前我们分析过, 如果当前NioEventLoop 是work 线程的话, 那么这里就是OP_READ 事件, 也就是读事件, 表示客户端发来了数据流，这里会调用unsafe 的redis()方法进行读取。那么这里的channel 是NioServerSocketChannel, 其绑定的unsafe 是NioByteUnsafe, 这里会走进NioByteUnsafe 的read()方法中

```
public final void read() {
    final ChannelConfig config = config();
    final ChannelPipeline pipeline = pipeline();
    final ByteBufAllocator allocator = config.getAllocator();
    final RecvByteBufAllocator.Handle allocHandle = recvBufAllocHandle();
    allocHandle.reset(config);

    ByteBuf byteBuf = null;
    boolean close = false;
    try {
        do {
            byteBuf = allocHandle.allocate(allocator);
            allocHandle.lastBytesRead(doReadBytes(byteBuf));
            if (allocHandle.lastBytesRead() <= 0) {
                  byteBuf.release();
                  byteBuf = null;
                  close = allocHandle.lastBytesRead() < 0;
                  break;
             }

             allocHandle.incMessagesRead(1);
             readPending = false;
             pipeline.fireChannelRead(byteBuf);
             byteBuf = null;
         } while (allocHandle.continueReading());
             allocHandle.readComplete();
             pipeline.fireChannelReadComplete();

             if (close) {
                    closeOnRead(pipeline);
             }
   } catch (Throwable t) {
         handleReadException(pipeline, byteBuf, t, close, allocHandle);
   } finally {
          if (!readPending && !config.isAutoRead()) {
             removeReadOp();
          }
   }
}
```

　　首先获取SocketChannel 的config, pipeline 等相关属性，final ByteBufAllocator allocator = config.getAllocator(); 这一步是获取一个ByteBuf 的内存分配器, 用于分配ByteBuf。这里会走到DefaultChannelConfig 的getAllocator 方法中:

```
public ByteBufAllocator getAllocator() {
    return allocator;
}
```

　　这里返回的DefualtChannelConfig 的成员变量, 我们看这个成员变量：

```
private volatile ByteBufAllocator allocator = ByteBufAllocator.DEFAULT;
```

　　这里调用ByteBufAllocator 的属性DEFAULT, 跟进去：

```
ByteBufAllocator DEFAULT = ByteBufUtil.DEFAULT_ALLOCATOR;
```

　　我们看到这里又调用了ByteBufUtil 的静态属性DEFAULT_ALLOCATOR, 再跟进去：

```
static final ByteBufAllocator DEFAULT_ALLOCATOR;
```

　　DEFAULT_ALLOCATOR 这个属性是在static 块中初始化的，我们跟到static 块中：

```
static {
        String allocType = SystemPropertyUtil.get(
                "io.netty.allocator.type", PlatformDependent.isAndroid() ? "unpooled" : "pooled");
        allocType = allocType.toLowerCase(Locale.US).trim();

        ByteBufAllocator alloc;
        if ("unpooled".equals(allocType)) {
            alloc = UnpooledByteBufAllocator.DEFAULT;
            logger.debug("-Dio.netty.allocator.type: {}", allocType);
        } else if ("pooled".equals(allocType)) {
            alloc = PooledByteBufAllocator.DEFAULT;
            logger.debug("-Dio.netty.allocator.type: {}", allocType);
        } else {
            alloc = PooledByteBufAllocator.DEFAULT;
            logger.debug("-Dio.netty.allocator.type: pooled (unknown: {})", allocType);
        }

        DEFAULT_ALLOCATOR = alloc;

        THREAD_LOCAL_BUFFER_SIZE = SystemPropertyUtil.getInt("io.netty.threadLocalDirectBufferSize", 64 * 1024);
        logger.debug("-Dio.netty.threadLocalDirectBufferSize: {}", THREAD_LOCAL_BUFFER_SIZE);

        MAX_CHAR_BUFFER_SIZE = SystemPropertyUtil.getInt("io.netty.maxThreadLocalCharBufferSize", 16 * 1024);
        logger.debug("-Dio.netty.maxThreadLocalCharBufferSize: {}", MAX_CHAR_BUFFER_SIZE);
}
```

　　首先判断运行环境是不是安卓, 如果不是安卓, 在返回"pooled"字符串保存在allocType 中，然后通过if 判断, 最后局部变量alloc = PooledByteBufAllocator.DEFAULT, 最后将alloc 赋值到成员变量DEFAULT_ALLOCATOR ， 我们跟到PooledByteBufAllocator 的DEFAULT 属性中：

```
public static final PooledByteBufAllocator DEFAULT =
            new PooledByteBufAllocator(PlatformDependent.directBufferPreferred());
```

　　我们看到这里直接通过new 的方式, 创建了一个PooledByteBufAllocator 对象, 也就是基于申请一块连续内存进行缓冲区分配的缓冲区分配器。缓冲区分配器的知识, 我们在前面的章节进行了详细的剖析, 这里就不再赘述。回到NioByteUnsafe 的read()方法中：

```
public final void read() {
    final ChannelConfig config = config();
    final ChannelPipeline pipeline = pipeline();
    final ByteBufAllocator allocator = config.getAllocator();
    final RecvByteBufAllocator.Handle allocHandle = recvBufAllocHandle();
    allocHandle.reset(config);

    ByteBuf byteBuf = null;
    boolean close = false;
    try {
        do {
            byteBuf = allocHandle.allocate(allocator);
            allocHandle.lastBytesRead(doReadBytes(byteBuf));
            if (allocHandle.lastBytesRead() <= 0) {
                  byteBuf.release();
                  byteBuf = null;
                  close = allocHandle.lastBytesRead() < 0;
                  break;
             }

             allocHandle.incMessagesRead(1);
             readPending = false;
             pipeline.fireChannelRead(byteBuf);
             byteBuf = null;
         } while (allocHandle.continueReading());
             allocHandle.readComplete();
             pipeline.fireChannelReadComplete();

             if (close) {
                    closeOnRead(pipeline);
             }
   } catch (Throwable t) {
         handleReadException(pipeline, byteBuf, t, close, allocHandle);
   } finally {
          if (!readPending && !config.isAutoRead()) {
             removeReadOp();
          }
   }
}
```

　　这里ByteBufAllocator allocator = config.getAllocator()中的allocator , 就是PooledByteBufAllocator。final RecvByteBufAllocator.Handle allocHandle = recvBufAllocHandle() 是创建一个handle, 我们之前的章节讲过,handle 是对RecvByteBufAllocator 进行实际操作的对象，我们跟进recvBufAllocHandle：

```
public RecvByteBufAllocator.Handle recvBufAllocHandle() {
   if (recvHandle == null) {
        recvHandle = config().getRecvByteBufAllocator().newHandle();
    }
    return recvHandle;
}
```

　　这里是我们之前剖析过的逻辑, 如果不存在, 则创建handle 的实例。同样allocHandle.reset(config)是将配置重置。重置完配置之后, 进行do-while循环, 有关循环终止条件allocHandle.continueReading()。在do-while 循环中, 首先看byteBuf = allocHandle.allocate(allocator) 这一步, 这里传入了刚才创建的allocate 对象, 也就是PooledByteBufAllocator，这里会进入DefaultMaxMessagesRecvByteBufAllocator 类的allocate()方法中：

```
public ByteBuf allocate(ByteBufAllocator alloc) {    return alloc.ioBuffer(guess());}
```

　　这里的guess 方法, 会调用AdaptiveRecvByteBufAllocator 的guess 方法：

```
public int guess() {
    return nextReceiveBufferSize;
}
```

　　这里会返回AdaptiveRecvByteBufAllocator 的成员变量nextReceiveBufferSize, 也就是下次所分配缓冲区的大小,  第一次分配的时候会分配初始大小, 也就是1024 字节。这样, alloc.ioBuffer(guess())就会分配一个PooledByteBuf，我们跟到AbstractByteBufAllocator 的ioBuffer 方法中：

```
public ByteBuf ioBuffer(int initialCapacity) {
    if (PlatformDependent.hasUnsafe()) {
        return directBuffer(initialCapacity);
    }
    return heapBuffer(initialCapacity);
}
```

　　这里首先判断是否能获取jdk 的unsafe 对象, 默认为true, 所以会走到directBuffer(initialCapacity)中, 这里最终会分配一个PooledUnsafeDirectByteBuf 对象。回到NioByteUnsafe 的read()方法中，分配完了ByteBuf 之后, 再看这一步allocHandle.lastBytesRead(doReadBytes(byteBuf))。首先看参数doReadBytes(byteBuf)方法, 这步是将channel 中的数据读取到我们刚分配的ByteBuf 中, 并返回读取到的字节数，这里会调用到NioSocketChannel 的doReadBytes()方法：

```
protected int doReadBytes(ByteBuf byteBuf) throws Exception {
    final RecvByteBufAllocator.Handle allocHandle = unsafe().recvBufAllocHandle();
    allocHandle.attemptedBytesRead(byteBuf.writableBytes());
    return byteBuf.writeBytes(javaChannel(), allocHandle.attemptedBytesRead());
}
```

　　首先拿到绑定在channel 中的handler, 因为我们已经创建了handle, 所以这里会直接拿到。再看allocHandle.attemptedBytesRead(byteBuf.writableBytes())这步, byteBuf.writableBytes()返回byteBuf 的可写字节数,也就是最多能从channel 中读取多少字节写到ByteBuf, allocate 的attemptedBytesRead 会把可写字节数设置到DefaultMaxMessagesRecvByteBufAllocator 类的attemptedBytesRead 属性中， 跟到DefaultMaxMessagesRecvByteBufAllocator 中的attemptedBytesRead 我们会看到：

```
public void attemptedBytesRead(int bytes) {
   attemptedBytesRead = bytes;
}
```

　　继续看doReadBytes()方法。往下看最后, 通过byteBuf.writeBytes(javaChannel(), allocHandle.attemptedBytesRead())将jdk 底层的channel 中的数据写入到我们创建的ByteBuf 中, 并返回实际写入的字节数。回到NioByteUnsafe 的read()方法中继续看allocHandle.lastBytesRead(doReadBytes(byteBuf))这步，刚才我们剖析过doReadBytes(byteBuf)返回的是实际写入ByteBuf 的字节数， 再看lastBytesRead() 方法, 跟到DefaultMaxMessagesRecvByteBufAllocator 的lastBytesRead()方法中：

```
public final void lastBytesRead(int bytes) {
    lastBytesRead = bytes;
    // Ignore if bytes is negative, the interface contract states it will be detected externally after call.
    // The value may be "invalid" after this point, but it doesn't matter because reading will be stopped.
    totalBytesRead += bytes;
    if (totalBytesRead < 0) {
        totalBytesRead = Integer.MAX_VALUE;
    }
}
```

　　这里会赋值两个属性, lastBytesRead 代表最后读取的字节数, 这里赋值为我们刚才写入ByteBuf 的字节数,totalBytesRead 表示总共读取的字节数, 这里将写入的字节数追加。继续来到NioByteUnsafe 的read()方法，如果最后一次读取数据为0, 说明已经将channel 中的数据全部读取完毕, 将新创建的ByteBuf 释放循环利用, 并跳出循环。allocHandle.incMessagesRead(1)这步是增加消息的读取次数, 因为我们循环最多16 次, 所以当增加消息次数增加到16会结束循环。读取完毕之后, 会通过pipeline.fireChannelRead(byteBuf)将传递channelRead 事件, 有关channelRead事件我们在前面的章节也进行了详细的剖析。至此，小伙伴们应该有个疑问, 如果一次读取不完, 就传递channelRead 事件, 那么server 接收到的数据有可能就是不完整的, 其实关于这点, Netty 也做了相应的处理, 我们会在之后的章节详细剖析Netty 的半包处理机制。循环结束后,会执行到allocHandle.readComplete()这一步。

　　我们知道第一次分配ByteBuf 的初始容量是1024, 但是初始容量不一定一定满足所有的业务场景, netty 中, 将每次读取数据的字节数进行记录, 然后之后次分配ByteBuf 的时候, 容量会尽可能的符合业务场景所需要大小, 具体实现方式,就是在readComplete()这一步体现的。我们跟到AdaptiveRecvByteBufAllocator 的readComplete()方法中：

```
public void readComplete() {
     record(totalBytesRead());
}
```

　　这里调用了record()方法, 并且传入了这一次所读取的字节总数，跟到record()方法中：

```
private void record(int actualReadBytes) {
    if (actualReadBytes <= SIZE_TABLE[Math.max(0, index - INDEX_DECREMENT - 1)]) {
        if (decreaseNow) {
            index = Math.max(index - INDEX_DECREMENT, minIndex);
            nextReceiveBufferSize = SIZE_TABLE[index];
            decreaseNow = false;
        } else {
            decreaseNow = true;
        }
    } else if (actualReadBytes >= nextReceiveBufferSize) {
        index = Math.min(index + INDEX_INCREMENT, maxIndex);
        nextReceiveBufferSize = SIZE_TABLE[index];
        decreaseNow = false;
    }
}
```

　　首先看判断条件if (actualReadBytes <= SIZE\_TABLE\[Math.max(0, index - INDEX\_DECREMENT - 1)\]) 。这里index 是当前分配的缓冲区大小所在的SIZE\_TABLE 中的索引, 将这个索引进行缩进, 然后根据缩进后的所以找出SIZE\_TABLE中所存储的内存值, 再判断是否大于等于这次读取的最大字节数, 如果条件成立, 说明分配的内存过大, 需要缩容操作,我们看if 块中缩容相关的逻辑。首先if (decreaseNow) 会判断是否立刻进行收缩操作, 通常第一次不会进行收缩操作,然后会将decreaseNow 设置为true, 代表下一次直接进行收缩操作。假设需要立刻进行收缩操作, 我们看收缩操作的相关逻辑：

　　index = Math.max(index - INDEX\_DECREMENT, minIndex) 这一步将索引缩进一步, 但不能小于最小索引值；然后通过nextReceiveBufferSize = SIZE\_TABLE\[index\] 获取设置索引之后的内存, 赋值在nextReceiveBufferSize, 也就是下次需要分配的大小, 下次就会根据这个大小分配ByteBuf 了, 这样就实现了缩容操作。再看else if (actualReadBytes >= nextReceiveBufferSize) ，这里判断这次读取字节的总量比上次分配的大小还要大,则进行扩容操作。扩容操作也很简单, 索引步进, 然后拿到步进后的索引所对应的内存值, 作为下次所需要分配的大小在NioByteUnsafe 的read()方法中，经过了缩容或者扩容操作之后, 通过pipeline.fireChannelReadComplete()传播ChannelReadComplete()事件，以上就是读取客户端消息的相关流程。