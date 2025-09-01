---
title: 线程池EventLoopGroup源码分析
id: 1539
date: 2024-10-31 22:02:00
author: daichangya
excerpt: (0)Reactor模型Reactor模型是一种经典的线程模型，一般分为三种类型：Reactor单线程模型Reactor多线程模型Reactor主从多线程模型Reactor单线程模型Reactor单线程模型是指所有的IO操作包括acceptor操作和handler操作都由一个线程完成；Netty中R
permalink: /archives/xian-cheng-chi-EventLoopGroup-yuan-ma/
categories:
- netty
---



## (0) Reactor模型

*   Reactor模型是一种经典的线程模型，一般分为三种类型：
    
    *   Reactor单线程模型
        
    *   Reactor多线程模型
        
    *   Reactor主从多线程模型
        

### Reactor单线程模型

*   Reactor单线程模型是指所有的IO操作包括acceptor操作和handler操作都由一个线程完成；

![20171123185646647.png](https://images.jsdiff.com/20171123185646647_1726491378941.png)

*   Netty中Reactor单线程的实现

```
ServerBootstrap b = new ServerBootstrap();
EventLoopGroup group = new NioEventLoopGroup(1);    //创建只有一个线程的线程池
b.group(group);    //acceptor操作和handler操作共用group线程池中的一个线程；

```

*   单线程模型适用在小容量，低并发的应用场景上，对于高负载高并发的应用场景不适用：
    
    *   如果handler操作是计算密集型操作，在高并发情况下即便CPU负荷达到100%也可能完成不了海量数据的处理，这就可能造成消息堆积和延迟处理；
        
    *   如果handler操作中出现阻塞则可能会导致acceptor操作无法进行进而可能导致客户连接超时，服务端接收不到新的客户端；
        
    *   一旦单线程程序跑飞或者进入死循环就会导致整个模块的不可用，不能接收处理外部消息，造成系统的不可靠问题；
        

### Reactor多线程模型

*   Reactor线程模型是指专门有一个线程处理acceptor操作(服务端的监听和客户端连接请求的处理)，而具体的handler操作(数据具体处理)则交由线程池处理；Reactor多线程模型中，服务端可以同时处理多条链路数据，但是一条链路也就是一个channel只对应一个线程，通道数据的整个处理流程全部由这个线程完成；

![20171123185706442.png](https://images.jsdiff.com/20171123185706442_1726491461526.png)
 
\- Netty中Reactor多线程模型的实现

```

ServerBootstrap b = new ServerBootstrap();
EventLoopGroup bossGroup = new NioEventLoopGroup(1);    //创建只有一个线程的线程池
EventLoopGroup workGroup = new NioEventLoopGroup();    //创建多线程线程池
b.group(bossGroup,workGroup);  

```

*   Reactor多线程模型的特点：
    
    *   一个线程用于监听服务端，处理客户端的连接请求
        
    *   具体的IO操作由线程池负责，线程池中的一个任务队列和N个可用线程用于负责消息的读取发送和编码解码等数据处理操作；
        
    *   一条链路也就是一个channel的处理由连接池中的一个线程服务，防止发生并发操作问题；
        
*   Reactor多线程模型适用于大多数情景，但是在个别情境下一个线程负责服务端的监听和多个客户端的连接请求可能出现性能问题，比如在处理客户端连接请求时要对客户端的握手进行安全认证，安全认证的过程非常消耗性能这就可能造成单线程处理性能上的不足；
    

### Reactor主从多线程模型

*   Reactor主从多线程模式是指不再由一个线程独立处理客户端的连接请求而是由一个线程池，Acceptor线程池仅仅用于客户端的登录，握手和验证等，一旦链路建立成功，就将链路的处理交由subReactor线程池，由线程池中的线程进行后续的IO操作；  
![20171123185806756.png](https://images.jsdiff.com/20171123185806756_1726491522118.png)
    
*   Netty中Reactor主从多线程模型的实现
    

```
ServerBootstrap b = new ServerBootstrap();
EventLoopGroup bossGroup = new NioEventLoopGroup();    //创建多线程线程池
EventLoopGroup workGroup = new NioEventLoopGroup();    //创建多线程线程池
b.group(bossGroup,workGroup);   

```

*   服务端Acceptor操作主要包括服务端监听和客户端连接请求处理两部分，在Reactor多线程模式下，服务端监听和处理客户端连接请求这两部分都由一个线程解决，而在Reactor主从多线程模式下，如果存在客户端的验证则处理客户连接请求部分会交由线程池处理；

## (1) EventLoopGroup线程池的初始化

*   在bootstrap启动辅助类中实例化EventLoopGroup

```
ServerBootstrap b = new ServerBootstrap();
EventLoopGroup bossGroup = new NioEventLoopGroup(); 
EventLoopGroup workGroup = new NioEventLoopGroup();
b.group(bossGroup,workGroup);

```

*   NioEventLoopGroup最终都是调用父类MultithreadEventLoopGroup的构造器

```
protected MultithreadEventLoopGroup(int nThreads, ThreadFactory threadFactory, Object... args) {
    super(nThreads == 0? DEFAULT_EVENT_LOOP_THREADS : nThreads, threadFactory, args);
}
```

*   如果传入的线程数量是０，则设置为默认线程数目DEFAULT\_EVENT\_LOOP_THREADS，默认线程数目是：处理器核心数*2

```
static {
    DEFAULT_EVENT_LOOP_THREADS = Math.max(1, SystemPropertyUtil.getInt(
            "io.netty.eventLoopThreads", Runtime.getRuntime().availableProcessors() * 2));
}
```

*   通过父类MultiThreadEventExecutorGroup构造器创建NioEventLoopGroup实例，内部维护了一个SingleThreadEventExecutor类型的数组，通过newChild()方法进行实例化

```
protected MultithreadEventExecutorGroup(int nThreads, ThreadFactory threadFactory, Object... args) {
    // 去掉了参数检查, 异常处理 等代码.
    children = new SingleThreadEventExecutor[nThreads];
    if (isPowerOfTwo(children.length)) {
        chooser = new PowerOfTwoEventExecutorChooser();
    } else {
        chooser = new GenericEventExecutorChooser();
    }

    for (int i = 0; i < nThreads; i ++) {
        children[i] = newChild(threadFactory, args);
    }
}
```

*   newChild()方法实例化的是NioEventLoop类型的EventLoop对象

```
protected EventExecutor newChild(
        ThreadFactory threadFactory, Object... args) throws Exception {
    return new NioEventLoop(this, threadFactory, (SelectorProvider) args[0]);
}
```

*   NioEventLoopGroup内部维护着一个NioEventLoop类型实例数组，NioEventLoop类的继承链：

```
NioEventLoop -> SingleThreadEventLoop -> SingleThreadEventExecutor -> AbstractScheduledEventExecutor
```

*   NioEventLoop类继承了SingleThreadEventExecutor类，该类中有一个thread属性用来绑定本地线程
    
    *   在SingleThreadEventExecutor的构造器中会通过threadFactory.newThread 创建了一个新的 Java 线程与当前NioEventLoop绑定，在这个线程中所做的事情主要就是调用 SingleThreadEventExecutor.this.run() 方法, 而因为 NioEventLoop 实现了这个方法, 因此根据多态性, 其实调用的是 NioEventLoop.run() 方法.

```
protected SingleThreadEventExecutor(
        EventExecutorGroup parent, ThreadFactory threadFactory, boolean addTaskWakesUp) {
    this.parent = parent;
    this.addTaskWakesUp = addTaskWakesUp;

    thread = threadFactory.newThread(new Runnable() {
        @Override
        public void run() {
            boolean success = false;
            updateLastExecutionTime();
            try {
                SingleThreadEventExecutor.this.run();
                success = true;
            } catch (Throwable t) {
                logger.warn("Unexpected exception from an event executor: ", t);
            } finally {
                // 省略清理代码
                ...
            }
        }
    });
    threadProperties = new DefaultThreadProperties(thread);
    taskQueue = newTaskQueue();
}
```

*   NioEventLoop.run() 方法是任务执行的关键，循环执行IO任务和任务队列中的任务
    
    *   轮询并处理IO事件
        
    *   处理任务队列中事件
        

```
protected void run() {
    for (;;) {
        try {
            switch (selectStrategy.calculateStrategy(selectNowSupplier, hasTasks())) {
                case SelectStrategy.CONTINUE:
                    continue;
                case SelectStrategy.SELECT:
                    select(wakenUp.getAndSet(false));    //轮询IO事件
                    if (wakenUp.get()) {
                        selector.wakeup();
                    }
                default:
                    // fallthrough
            }
            processSelectedKeys();    //处理IO时间
            runAllTasks(...);    //处理任务队列中事件
            }
        } catch (Throwable t) {
            handleLoopException(t);
        }
        ...
    }

```

*   NioEventLoop类继承了AbstractScheduledEventExecutor类，实现了NioEventLoop的schedule定时执行功能；NioEventLoop 肩负着两种任务, 第一个是作为 IO 线程, 执行与 Channel 相关的 IO 操作, 包括 调用 select 等待就绪的 IO 事件、读写数据与数据的处理等; 而第二个任务是作为任务队列, 执行 taskQueue 中的任务, 例如用户调用 eventLoop.schedule 提交的定时任务也是这个线程执行的，主要用于定时心跳检测.

## (2) EventLoop与Channel的关联

*   客户端在通过bootstrap启动时会创建一个Channel实例并进行初始化，在初始化过程中会绑定一个EventLoop

```
bootstrap.connect() -> bootstrap.doConnect() -> AbstractBootstrap.initAndRegister() -> channelFactory.newChannel()  -> group().register(channel) -> MultiThreadEventLoopGroup.regiser()

```

*   NioEventLoopGroup调用父类的register()方法将获取一个EventLoop与通道绑定；

```
public ChannelFuture register(Channel channel) {
    return this.next().register(channel);
}
```

*   调用next()方法通过轮询的方式将通道平均地绑定到初始化的EventLoop数组上

```
public EventExecutor next() {
    return this.executors[this.idx.getAndIncrement() & this.executors.length - 1];
}
```

*   获取得到EventLoop后调用SingleThreadEventLoop类的register()方法

```

public ChannelFuture register(Channel channel) {
    return this.register((ChannelPromise)(new DefaultChannelPromise(channel, this)));
}
```

```
public ChannelFuture register(ChannelPromise promise) {
    ObjectUtil.checkNotNull(promise, "promise");
    promise.channel().unsafe().register(this, promise);
    return promise;
}
```

*   最终调用了 AbstractChannel#AbstractUnsafe.register 后完成了 Channel 和 EventLoop 的关联，将获取的EventLoop值赋值给AbstractChannel内的一个eventLoop属性；

```
public final void register(EventLoop eventLoop, final ChannelPromise promise) {
    // 删除条件检查.
    ...
    AbstractChannel.this.eventLoop = eventLoop;

    if (eventLoop.inEventLoop()) {
        register0(promise);
    } else {
        try {
            eventLoop.execute(new OneTimeTask() {
                @Override
                public void run() {
                    register0(promise);
                }
            });
        } catch (Throwable t) {
            ...
        }
    }
}
```

*   调用AbstractChannel的register0()方法最终完成通道的注册

```
private void register0(ChannelPromise promise) {
    boolean firstRegistration = neverRegistered;
    doRegister();
    neverRegistered = false;
    registered = true;
    safeSetSuccess(promise);
    pipeline.fireChannelRegistered();
    // Only fire a channelActive if the channel has never been registered. This prevents firing
    // multiple channel actives if the channel is deregistered and re-registered.
    if (firstRegistration && isActive()) {
        pipeline.fireChannelActive();
    }
}
```

*   调用AbstractNioChannel.doRegister()方法将通道与EventLoop线程的selector绑定

```
protected void doRegister() throws Exception {
    // 省略错误处理
    selectionKey = javaChannel().register(eventLoop().selector, 0, this);
}
```

## (3) EventLoop线程启动

*   在通过调用 AbstractChannel#AbstractUnsafe.register完成通道channel和eventLoop线程绑定后会执行eventLoop.execute()方法启动线程

```
public final void register(EventLoop eventLoop, final ChannelPromise promise) {
    // 删除条件检查.
    ...
    AbstractChannel.this.eventLoop = eventLoop;

    if (eventLoop.inEventLoop()) {
        register0(promise);
    } else {
        try {
            eventLoop.execute(new OneTimeTask() {
                @Override
                public void run() {
                    register0(promise);
                }
            });
        } catch (Throwable t) {
            ...
        }
    }
}
```

*   执行eventLoop.execute()方法时会判断eventLoop线程时候执行，如果没有执行则调用startThread()方法启动线程
    
    *   通过调用inEventLoop()方法判断eventLoop线程是否执行，是通过判断当前线程是main主线程还是evnetLoop线程

```
public void execute(Runnable task) {
    if (task == null) {
        throw new NullPointerException("task");
    }

    boolean inEventLoop = inEventLoop();
    if (inEventLoop) {
        addTask(task);
    } else {
        startThread(); // 调用 startThread 方法, 启动EventLoop 线程.
        addTask(task);
        if (isShutdown() && removeTask(task)) {
            reject();
        }
    }

    if (!addTaskWakesUp && wakesUpForTask(task)) {
        wakeup(inEventLoop);
    }
}
```

*   调用startThread()方法启动EventLoop内部绑定的线程

```
private void startThread() {
    if (STATE_UPDATER.get(this) == ST_NOT_STARTED) {
        if (STATE_UPDATER.compareAndSet(this, ST_NOT_STARTED, ST_STARTED)) {
            thread.start();
        }
    }
}
```

## (4) EventLoop线程的运行

*   在connect()方法中通道初始化和注册时会调用eventLoop.execute()方法，在方法中会调用startThread()方法启动与EventLoop绑定的Thread线程，线程启动后受内核调度执行run()方法；
    
    *   Run()方法中主要处理两种事件：监控IO事件和处理任务队列中的Task任务

```
protected void run() {
    for (;;) {
        boolean oldWakenUp = wakenUp.getAndSet(false);
        try {
            if (hasTasks()) {
                selectNow();
            } else {
                select(oldWakenUp);
                if (wakenUp.get()) {
                    selector.wakeup();
                }
            }

            cancelledKeys = 0;
            needsToSelectAgain = false;
            final int ioRatio = this.ioRatio;
            if (ioRatio == 100) {
                processSelectedKeys();
                runAllTasks();
            } else {
                final long ioStartTime = System.nanoTime();

                processSelectedKeys();

                final long ioTime = System.nanoTime() - ioStartTime;
                runAllTasks(ioTime * (100 - ioRatio) / ioRatio);
            }
        } catch (Throwable t) {
            ...
        }
    }
}
```

*   通过hasTasks()方法判断任务队列中是否有未执行的任务；

```
protected boolean hasTasks() {
    assert inEventLoop();
    return !taskQueue.isEmpty();
}
```

*   如果有任务则执行selectNow()方法立即返回

```
void selectNow() throws IOException {
    try {
        selector.selectNow();
    } finally {
        // restore wakup state if needed
        if (wakenUp.get()) {
            selector.wakeup();
        }
    }
}
```

*   如果没有任务则执行select(oldWakenUp)方法阻塞当前线程timeout时间，这样可以避免长时间的线程空转；

```
private void select(boolean oldWakenUp) throws IOException {
    Selector selector = this.selector;
    try {
        ...
        int selectedKeys = selector.select(timeoutMillis);
        ...
    } catch (CancelledKeyException e) {
        ...
    }
}
```

*   ioRatio参数设定用来表示IO事件处理和任务队列任务处理时间的占比，如果ioRatio为100则表示Netty 就不考虑 IO 耗时的占比, 而是分别调用 processSelectedKeys()、runAllTasks();如果ioRatio不为100则表示需要根据ioTime以及ioRatio比例计算出taskTime，计算公式为：

```
taskTime = ioTime * (100 - ioRatio) / ioRatio
```

*   计算出执行 task 所占用的时间, 然后以此为参数调用 runAllTasks(timeout)，如果时间超出taskTime时间则跳出循环执行IO事件

```
protected boolean runAllTasks(long timeoutNanos) {
    this.fetchFromScheduledTaskQueue();
    Runnable task = this.pollTask();
    if(task == null) {
        this.afterRunningAllTasks();
        return false;
    } else {
        long deadline = ScheduledFutureTask.nanoTime() + timeoutNanos;
        long runTasks = 0L;

        long lastExecutionTime;
        while(true) {
            safeExecute(task);
            ++runTasks;
            if((runTasks & 63L) == 0L) {
                lastExecutionTime = ScheduledFutureTask.nanoTime();
                if(lastExecutionTime >= deadline) {
                    break;
                }
            }

            task = this.pollTask();
            if(task == null) {
                lastExecutionTime = ScheduledFutureTask.nanoTime();
                break;
            }
        }

        this.afterRunningAllTasks();
        this.lastExecutionTime = lastExecutionTime;
        return true;
    }
}
```

## (5) IO事件的处理

*   在run()方法中听过processSelectedKeys()方法处理IO事件

```
private void processSelectedKeys() {
    if (selectedKeys != null) {
        processSelectedKeysOptimized(selectedKeys.flip());
    } else {
        processSelectedKeysPlain(selector.selectedKeys());
    }
}
```

*   迭代selectedKeys获取就绪的 IO 事件, 然后为每个事件都调用processSelectedKey来处理它.

```
private void processSelectedKeysOptimized(SelectionKey[] selectedKeys) {
    for (int i = 0;; i ++) {
        final SelectionKey k = selectedKeys[i];
        if (k == null) {
            break;
        }
        selectedKeys[i] = null;

        final Object a = k.attachment();

        if (a instanceof AbstractNioChannel) {
            processSelectedKey(k, (AbstractNioChannel) a);
        } else {
            @SuppressWarnings("unchecked")
            NioTask<SelectableChannel> task = (NioTask<SelectableChannel>) a;
            processSelectedKey(k, task);
        }
        ...
    }
}
```

*   在processSelectedKey()方法中将IO事件分为三种分别进行处理：
    
    *   OP_READ, 可读事件, 即 Channel 中收到了新数据可供上层读取.
        
    *   OP_WRITE, 可写事件, 即上层可以向 Channel 写入数据.
        
    *   OP_CONNECT, 连接建立事件, 即 TCP 连接已经建立, Channel 处于 active 状态.
        

```
rivate static void processSelectedKey(SelectionKey k, AbstractNioChannel ch) {
    final NioUnsafe unsafe = ch.unsafe();
    ...
    try {
        int readyOps = k.readyOps();

        // 可读事件
        if ((readyOps & (SelectionKey.OP_READ | SelectionKey.OP_ACCEPT)) != 0 || readyOps == 0) {
            unsafe.read();
            if (!ch.isOpen()) {
                // Connection already closed - no need to handle write.
                return;
            }
        }

        // 可写事件
        if ((readyOps & SelectionKey.OP_WRITE) != 0) {
            // Call forceFlush which will also take care of clear the OP_WRITE once there is nothing left to write
            ch.unsafe().forceFlush();
        }

        // 连接建立事件
        if ((readyOps & SelectionKey.OP_CONNECT) != 0) {
            // remove OP_CONNECT as otherwise Selector.select(..) will always return without blocking
            // See https://github.com/netty/netty/issues/924
            int ops = k.interestOps();
            ops &= ~SelectionKey.OP_CONNECT;
            k.interestOps(ops);

            unsafe.finishConnect();
        }
    } catch (CancelledKeyException ignored) {
        unsafe.close(unsafe.voidPromise());
    }
}
```

## 总结

*   NioEventLoopGroup实例化过程：
    
    *   EventLoopGroup(其实是MultithreadEventExecutorGroup) 内部维护一个类型为EventExecutor children数组, 其大小是 nThreads, 这样就构成了一个线程池；
        
    *   MultithreadEventExecutorGroup中会调用 newChild 抽象方法来初始化children数组,抽象方法newChild是在 NioEventLoopGroup 中实现的, 它返回一个 NioEventLoop 实例；每个Channel通道注册时都会轮流注册到children数组上的一个EventLoop对象上；
        
    *   NioEventLoop属性:
        
        *   SelectorProvider provider 属性: NioEventLoopGroup 构造器中通过 SelectorProvider.provider() 获取一个 SelectorProvider对象；
            
        *   Selector selector 属性: NioEventLoop 构造器中通过调用通过 selector = provider.openSelector() 获取一个 selector 对象.每个EventLoop绑定一个selector对象，每个EventLoop对应一个或者多个Channel通道；