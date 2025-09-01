---
title: 数据管道ChannelPipeline源码分析
id: 1536
date: 2024-10-31 22:02:00
author: daichangya
cover: https://images.jsdiff.com/Netty02.jpg
excerpt: (0) ChannelPipeline的实例 ChannelPipeline的使用实例 private void connect(String host,int
  port){    EventLoopGroup group = new NioEventLoopGroup();    try {
permalink: /archives/shu-ju-guan-dao-ChannelPipeline-yuan-ma/
categories:
- netty
---



## (0) ChannelPipeline的实例

*   ChannelPipeline的使用实例

```

private void connect(String host,int port){
    EventLoopGroup group = new NioEventLoopGroup();
    try {
        Bootstrap b = new Bootstrap();
        b.group(group).channel(NioSocketChannel.class).option(ChannelOption.TCP_NODELAY,true)
                .handler(new ChannelInitializer<SocketChannel>() {
                    @Override
                    protected void initChannel(SocketChannel socketChannel) throws Exception {
                       ChannelPipeline ch = socketChannel.pipeline();
                        ch.addLast(new TimeClientHandler());
                    }
                });

        ChannelFuture f = b.connect(host,port).sync();
        f.channel().closeFuture().sync();
    }catch (Exception e){
        e.printStackTrace();
    }finally {
        group.shutdownGracefully();
    }
}
```

*   bootstrap是启动辅助类，在进行参数设置后通过bootstrap.connect()方法正式启动客户端；connect()方法调用父类AbstractBootstrap的initAndRegister()方法创建ChannelPipeline和初始化Pipeline添加handler；

```

final ChannelFuture initAndRegister() {
    Channel channel = null;

    try {
        channel = this.channelFactory.newChannel();    //创建
        this.init(channel);    //初始化
    } catch (Throwable var3) {
        if(channel != null) {
            channel.unsafe().closeForcibly();
        }

        return (new DefaultChannelPromise(channel, GlobalEventExecutor.INSTANCE)).setFailure(var3);
    }

    ChannelFuture regFuture = this.config().group().register(channel);    //注册
    if(regFuture.cause() != null) {
        if(channel.isRegistered()) {
            channel.close();
        } else {
            channel.unsafe().closeForcibly();
        }
    }

    return regFuture;
}
```

## (1)ChannelPipeline创建

*   ChannelPipeline数据管道是与Channel通道绑定的，一个Channel通道对应一个ChannelPipeline，channelpipeline是在Channel初始化时候被创建；
    
*   在Channel实例化时会通过newInstance()方法调用构造器创建实例，NioServerSocketChannel和NioSocketChannel都继承了AbstractChannel，在创建实例时候也会调用AbstractChannel构造器；在AbstractChannel构造器中会创建pipeline管道实例
    

```

protected AbstractChannel(Channel parent) {
    this.parent = parent;
    unsafe = newUnsafe();
    pipeline = new DefaultChannelPipeline(this);
}
```

*   创建DefaultChannelPipeline类型的对象指向channelPipeline属性
    
    *   pipeline内维护着一个以 AbstractChannelHandlerContext 为节点的双向链表，创建的head和tail节点分别指向链表头尾
        
    *   TailContext和headContext都继承了AbstractChannelHandlerContext并是实现了ChannelHandler接口，AbstractChannelHandlerContext内部维护着next，pre链表指针和inbound，outbound节点方向等；TaileContext实现了ChannelInboundHandler，headContext实现了ChanneloutboundHandler;
        

![20171122154052606.png](https://images.jsdiff.com/20171122154052606_1726491842107.png)

```
public DefaultChannelPipeline(AbstractChannel channel) {
    if (channel == null) {
        throw new NullPointerException("channel");
    }
    this.channel = channel;

    tail = new TailContext(this);
    head = new HeadContext(this);

    head.next = tail;
    tail.prev = head;
}
```

## (2) ChannelPipeline初始化的handler添加过程

*   bootstrap.connect()方法会在pipeline创建之后newChannel()调用init()方法对其进行初始化

```
void init(Channel channel) throws Exception {
    ChannelPipeline p = channel.pipeline();
    p.addLast(new ChannelHandler[]{this.config.handler()});
    Map options = this.options0();
    synchronized(options) {
        setChannelOptions(channel, options, logger);
    }

    Map attrs = this.attrs0();
    synchronized(attrs) {
        Iterator var6 = attrs.entrySet().iterator();

        while(var6.hasNext()) {
            Entry e = (Entry)var6.next();
            channel.attr((AttributeKey)e.getKey()).set(e.getValue());
        }
    }
}
```

*   调用pipeline.addLast()方法添加handler到pipeline管道中，该handler为初始化时配置的ChannelInitializer对象；
    
*   ChannelInitializer继承了ChannelInboundHandlerAdapter，它提供了一个 initChannel 方法供我们初始化自定义ChannelHandler；在调用addLast()方法时会创建一个DefaultChannelHandlerContext节点用来存放ChannelInitializer，因为ChannelInitializer继承了ChannelInboundHandlerAdapter所以节点的inbound属性为true，outbound属性为false；
    

![20171122154207527.png](https://images.jsdiff.com/20171122154207527_1726491871485.png)

```
public final ChannelHandler handler() {
    return this.bootstrap.handler();
}
```

```
 bootstrap.handler(new ChannelInitializer<SocketChannel>() {
                    @Override
                    protected void initChannel(SocketChannel socketChannel) throws Exception {
                       ChannelPipeline ch = socketChannel.pipeline();
                        ch.addLast(new TimeClientHandler());
                    }
 });
```

*   自定义handler添加到pipeline管道中发生在channel通道的注册过程中；在调用 register0()方法注册 Channel过程中调用pipeline.fireChannelRegistered()方法传递通道注册事件；

```
public ChannelPipeline fireChannelRegistered() {
    head.fireChannelRegistered();
    return this;
}
```

*   调用AbstractChannelHandlerContext的invokeChannelRegistered()方法，调用findContextInbound()方法从头遍历双向链表查找第一个inbound类型的节点，这里就是查找ChannelInitializer节点，调用该节点的ChannelRegistered()方法添加自定义的Handler然后删除ChannelInitializer节点；

```
public ChannelHandlerContext fireChannelRegistered() {
    final AbstractChannelHandlerContext next = findContextInbound();
    EventExecutor executor = next.executor();
    if (executor.inEventLoop()) {
        next.invokeChannelRegistered();
    } else {
        executor.execute(new OneTimeTask() {
            @Override
            public void run() {
                next.invokeChannelRegistered();
            }
        });
    }
    return this;
}
```

```
private void invokeChannelRegistered() {
    if(this.invokeHandler()) {
        try {
            ((ChannelInboundHandler)this.handler()).channelRegistered(this);
        } catch (Throwable var2) {
            this.notifyHandlerException(var2);
        }
    } else {
        this.fireChannelRegistered();
    }

}
```

*   调用ChannelInitializer节点的channelRegistered()方法添加自定义节点删除初始节点
    
    *   调用initChannel()方法，通过addLast()向链表尾部添加自定义Handler
        
    *   删除ChannelInitializer节点
        

```
public final void channelRegistered(ChannelHandlerContext ctx) throws Exception {
    initChannel((C) ctx.channel());
    ctx.pipeline().remove(this);
    ctx.fireChannelRegistered();
}
```

![20171122154319469.jpeg](https://images.jsdiff.com/20171122154319469_1726491895465.jpeg)

## (3) ChannelPipeline事件传输机制

*   通过pipeline.addLast()方法添加自定义Handler，为这个 Handler 创建一个对应的 DefaultChannelHandlerContext 实例, 并与之关联起来(Context中有一个handler属性保存着对应的Handler实例).

```
public ChannelPipeline addLast(EventExecutorGroup group, final String name, ChannelHandler handler) {
    synchronized (this) {
        checkDuplicateName(name); // 检查此 handler 是否有重复的名字

        AbstractChannelHandlerContext newCtx = new DefaultChannelHandlerContext(this, group, name, handler);
        addLast0(name, newCtx);
    }

    return this;
}
```

*   在创建DefaultChannelHandlerContext时会通过isInbound()方法和isOutbound()方法判断当前handler是否继承实现了ChannelInboundHanler或者ChannelOutboundHandler接口，进而设置DefaultChannelHandlerContext实例的inbound属性和outbound属性；

```
DefaultChannelHandlerContext(DefaultChannelPipeline pipeline, EventExecutor executor, String name, ChannelHandler handler) {
    super(pipeline, executor, name, isInbound(handler), isOutbound(handler));
    if(handler == null) {
        throw new NullPointerException("handler");
    } else {
        this.handler = handler;
    }
}
```

*   Netty的事件分为Inbound事件和Outbound事件分别代表管道中两个方向的数据流向；pipeline管道中维护的双向链表的节点也根据DefaultChannelHandlerContext实例的inbound属性和outbound属性分为inbound节点和outbound节点，输入时间会依次经过inbound节点的处理，输出事件会依次经过outbound节点的处理；
    
*   读写数据流依次经过相应节点处理，一个节点处理完后会调用ChannelHandlerContext.fireChannelRegistered()传递到下一个节点
    

```

                            read() or write()
               Channel or ChannelHandlerContext
                                                  |
+---------------------------------------------------+---------------+
|                           ChannelPipeline         |               |
|                                                  \|/              |
|    +---------------------+            +-----------+----------+    |
|    | Inbound Handler  N  |            | Outbound Handler  1  |    |
|    +----------+----------+            +-----------+----------+    |
|              /|\                                  |               |
|               |                                  \|/              |
|    +----------+----------+            +-----------+----------+    |
|    | Inbound Handler N-1 |            | Outbound Handler  2  |    |
|    +----------+----------+            +-----------+----------+    |
|              /|\                                  .               |
|               .                                   .               |
| ChannelHandlerContext.fireIN_EVT() ChannelHandlerContext.OUT_EVT()|
|        [ method call]                       [method call]         |
|               .                                   .               |
|               .                                  \|/              |
|    +----------+----------+            +-----------+----------+    |
|    | Inbound Handler  2  |            | Outbound Handler M-1 |    |
|    +----------+----------+            +-----------+----------+    |
|              /|\                                  |               |
|               |                                  \|/              |
|    +----------+----------+            +-----------+----------+    |
|    | Inbound Handler  1  |            | Outbound Handler  M  |    |
|    +----------+----------+            +-----------+----------+    |
|              /|\                                  |               |
+---------------+-----------------------------------+---------------+
              |                                  \|/
+---------------+-----------------------------------+---------------+
|               |                                   |               |
|       [ Socket.read() ]                    [ Socket.write() ]     |
|                                                                   |
|  Netty Internal I/O Threads (Transport Implementation)            |
+-------------------------------------------------------------------+
```

### outbound事件传播机制

*   outbound事件是请求事件，Channel发起具体的事件最终通过Unsafe底层进行处理，数据传输的方向是tail -> head；
    
*   在自定义handle中通过ctx.write()方法向通道中写入数据
    

```

public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
    ByteBuf buf = (ByteBuf)msg;
    ctx.write(buf);
}
```

*   在AbstractChannelHandlerContext中调用write()方法

```

public ChannelFuture write(Object msg) {
    return this.write(msg, this.newPromise());
}

public ChannelFuture write(Object msg, ChannelPromise promise) {
    if(msg == null) {
        throw new NullPointerException("msg");
    } else {
        try {
            if(this.isNotValidPromise(promise, true)) {
                ReferenceCountUtil.release(msg);
                return promise;
            }
        } catch (RuntimeException var4) {
            ReferenceCountUtil.release(msg);
            throw var4;
        }

        this.write(msg, false, promise);
        return promise;
    }
}
```

*   在AbstractChannelHandlerContext中调用重载write()方法，查找下一个outbound节点，也就是当前handler后面的一个outbound类型的handler

```

private void write(Object msg, boolean flush, ChannelPromise promise) {
    AbstractChannelHandlerContext next = this.findContextOutbound();
    Object m = this.pipeline.touch(msg, next);
    EventExecutor executor = next.executor();
    if(executor.inEventLoop()) {
        if(flush) {
            next.invokeWriteAndFlush(m, promise);
        } else {
            next.invokeWrite(m, promise);
        }
    } else {
        Object task;
        if(flush) {
            task = AbstractChannelHandlerContext.WriteAndFlushTask.newInstance(next, m, promise);
        } else {
            task = AbstractChannelHandlerContext.WriteTask.newInstance(next, m, promise);
        }

        safeExecute(executor, (Runnable)task, promise, m);
    }

}
```

*   调用下一个AbstractChannelHandlerContext节点的invoke()方法

```

private void invokeWrite(Object msg, ChannelPromise promise) {
    if(this.invokeHandler()) {
        this.invokeWrite0(msg, promise);
    } else {
        this.write(msg, promise);
    }

}
```

*   执行下一个handler的write()方法，在方法中会再次调用AbstractChannelHandlerContext的write()方法完成一次循环

```

private void invokeWrite0(Object msg, ChannelPromise promise) {
    try {
        ((ChannelOutboundHandler)this.handler()).write(this, msg, promise);
    } catch (Throwable var4) {
        notifyOutboundHandlerException(var4, promise);
    }

}
```

*   outbound事件循环执行流程

```

handler.write() -> context.write() -> context.findContextOutbound -> next.invokeWrite -> handler.write -> context.write()

```

*   outbound事件传播机制
    
    *   Outbound 事件是请求事件(由write方法或者connect方法发起一个请求, 并最终由 unsafe 处理这个请求),,Outbound 事件的发起者是 Channel,Outbound 事件的处理者是 unsafe；
        
    *   Outbound 事件在 Pipeline 中的传输方向是 tail -> head.
        
    *   在 ChannelHandler 中处理事件时, 如果这个 Handler 不是最后一个 Hnalder, 则需要调用 ctx.xxx (例如 ctx.connect) 将此事件继续传播下去. 如果不这样做, 那么此事件的传播会提前终止.如StringDecoder是最后一个Handler则将作为事件传播的终点不再向下传播；
        
    *   Outbound 事件流: Context.xxx -> Connect.findContextOutbound -> nextContext.invokeXxx -> nextHandler.xxx -> nextContext.xxx
        

### inbound事件传播机制

*   inbound事件传播的起点是调用pipeline.fireXxx()方法，在该方法中调用了head链表头结点的fireXxx()方法，因此inbound事件传播方向是head -> tail；

```



public ChannelPipeline fireChannelActive() {
    head.fireChannelActive();

    if (channel.config().isAutoRead()) {
        channel.read();
    }

    return this;
}
```

*   head.fireChannelActive()会调用AbstractChannelHandlerContext的fireChannelXxx()方法，在该方法中会查询下一个inbound类型的节点，并通过invokeChannelXxx()方法调用该节点；

```

public ChannelHandlerContext fireChannelActive() {
    final AbstractChannelHandlerContext next = findContextInbound();
    EventExecutor executor = next.executor();
    ...
    next.invokeChannelActive();
    ...
    return this;
}
```

*   在inbound节点的invokeChannelXxx()方法中执行该节点的handler.ChannlXxx()方法

```

private void invokeChannelActive() {
    try {
        ((ChannelInboundHandler) handler()).channelActive(this);
    } catch (Throwable t) {
        notifyHandlerException(t);
    }
}
```

*   在节点handler.channelXxx()方法中如果该节点不是最后一个处理节点则会调用ctx.fireChannelXxx()方法将数据流传递给下一个inbound节点，完成依次循环；

```

public void channelActive(ChannelHandlerContext ctx) throws Exception {
    ctx.fireChannelActive();
}
```

*   inbound事件传播的流程是

```

pipeline.fireChannelXxx() -> ctx.fireChannelXxx() -> findContextInbound() -> ctx.invokeChannelXxx() -> handler.channelXxx() -> ctx.fireChannelXxx()

```

*   inbound事件传播机制
    
    *   Inbound事件是通知型事件，事件由底层程序产生，通知上层应用程序,Inbound 事件在 Pipeline 中传输方向是 head -> tail；
        
    *   Inbound 事件的处理者是 Channel, 如果用户没有实现自定义的处理方法, 那么Inbound 事件默认的处理者是 TailContext, 并且其处理方法是空实现.
        
    *   在 ChannelHandler 中处理事件时, 如果这个 Handler 不是最后一个 Hnalder, 则需要调用 ctx.fireChannelXxx (例如 ctx.fireChannelActive) 将此事件继续传播下去. 如果不这样做, 那么此事件的传播会提前终止.
        
    *   Outbound 事件流: Context.fireChannelXxx -> Connect.findContextInbound -> nextContext.invokeChannelXxx -> nextHandler.ChannelXxx -> nextContext.fireChannelXxx
        

## 结论

*   pipeline是事件传播的管道，内部维护着一个双向链表，链表节点分为inbound类型和outbount类型；
    
*   输入事件比如read事件，数据流从链表的head到tail依次经过链表inbound类型节点的处理；
    
*   输出事件比如write事件，数据流从链表的tail到head依次经过链表outbound类型节点的处理；