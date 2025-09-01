---
title: Lettuce是如何发送Command命令到redis的
id: 1496
date: 2024-10-31 22:01:58
author: daichangya
permalink: /archives/lettuce%E6%98%AF%E5%A6%82%E4%BD%95%E5%8F%91%E9%80%81command%E5%91%BD%E4%BB%A4%E5%88%B0redis%E7%9A%84/
categories:
 - redis
---

**lettuce-core版本**: 5.1.7.RELEASE

在上一篇介绍了Lettuce是如何基于Netty与Redis建立连接的，其中提到了一个很重要的CommandHandler类，这一期会介绍CommandHandler是如何在发送Command到Lettuce中发挥作用的，以及Lettuce是如何实现多线程共享同一个物理连接的。  
还是先看一下我们的示例代码，这一篇主要是跟进去sync.get方法看看Lettuc是如何发送get命令到Redis以及是如何读取Redis的命令的。

```java
/**
 * @author xiaobing
 * @date 2019/12/20
 */
public class LettuceSimpleUse {
    private void testLettuce() throws ExecutionException, InterruptedException {
        //构建RedisClient对象，RedisClient包含了Redis的基本配置信息，可以基于RedisClient创建RedisConnection
        RedisClient client = RedisClient.create("redis://localhost");

        //创建一个线程安全的StatefulRedisConnection，可以多线程并发对该connection操作,底层只有一个物理连接.
        StatefulRedisConnection<String, String> connection = client.connect();

        //获取SyncCommand。Lettuce支持SyncCommand、AsyncCommands、ActiveCommand三种command
        RedisStringCommands<String, String> sync = connection.sync();
        String value = sync.get("key");
        System.out.println("get redis value with lettuce sync command, value is :"   value);

        //获取SyncCommand。Lettuce支持SyncCommand、AsyncCommands、ActiveCommand三种command
        RedisAsyncCommands<String, String> async = connection.async();
        RedisFuture<String> getFuture = async.get("key");
        value = getFuture.get();
        System.out.println("get redis value with lettuce async command, value is :"   value);
    }

    public static void main(String[] args) throws ExecutionException, InterruptedException {
        new LettuceSimpleUse().testLettuce();
    }
}

```

在看sync.get方法之前先看一下RedisStringCommands是如何生成生成的，从下面的代码可以看到RedisStringCommands其实是对RedisAsyncCommands<String, String>方法调用的同步阻塞版本。

```java
	//创建一个sync版本的RedisCommand
	protected RedisCommands<K, V> newRedisSyncCommandsImpl() {
				//async()方法返回的就是该Connection对应的RedisAsyncCommand
        return syncHandler(async(), RedisCommands.class, RedisClusterCommands.class);
    }
	//返回一个动态代理类，代理类的实现在FutureSyncInvocationHandler类中
	protected <T> T syncHandler(Object asyncApi, Class<?>... interfaces) {
        FutureSyncInvocationHandler h = new FutureSyncInvocationHandler((StatefulConnection<?, ?>) this, asyncApi, interfaces);
				//基于FutureSyncInvocationHandler生成动态代理类
        return (T) Proxy.newProxyInstance(AbstractRedisClient.class.getClassLoader(), interfaces, h);
    }
		//异步转同步的关键
	class FutureSyncInvocationHandler extends AbstractInvocationHandler {

			...

			@Override
			@SuppressWarnings("unchecked")
			protected Object handleInvocation(Object proxy, Method method, Object[] args) throws Throwable {

					try {

							Method targetMethod = this.translator.get(method);
							Object result = targetMethod.invoke(asyncApi, args);

							// RedisAsyncCommand返回的大部分对象类型都是RedisFuture类型的
							if (result instanceof RedisFuture<?>) {

									RedisFuture<?> command = (RedisFuture<?>) result;

									if (isNonTxControlMethod(method.getName()) && isTransactionActive(connection)) {
											return null;
									}
									//获取配置的超时时间
									long timeout = getTimeoutNs(command);
									//阻塞的等待RedisFuture返回结果
									return LettuceFutures.awaitOrCancel(command, timeout, TimeUnit.NANOSECONDS);
							}

							return result;
					} catch (InvocationTargetException e) {
							throw e.getTargetException();
					}
			}
		}
		...

```

所以sync.get操作最终调用的还是async.get操作，接下来看async.get是怎么做的。还是先看一张时序图，心里有一个概念。

#### AbstractRedisAsyncCommands

```java
	@Override
    public RedisFuture<V> get(K key) {
        return dispatch(commandBuilder.get(key));
    }

```

#### commandBuilder.get(key)

这一步骤主要是根据用户的输入参数key、命令类型get、序列化方式来生成一个command对象。而这个command对象会按照Redis的协议格式把命令序列化成字符串。

```java
	Command<K, V, V> get(K key) {
		notNullKey(key);
		//Valueoutput基于序列化
		return createCommand(GET, new ValueOutput<>(codec), key);
    }
		
	protected <T> Command<K, V, T> createCommand(CommandType type, CommandOutput<K, V, T> output, K key) {
        CommandArgs<K, V> args = new CommandArgs<K, V>(codec).addKey(key);
        return createCommand(type, output, args);
    }
		
	protected <T> Command<K, V, T> createCommand(CommandType type, CommandOutput<K, V, T> output, CommandArgs<K, V> args) {
        return new Command<K, V, T>(type, output, args);
    }
		

```

#### AbstractRedisAsyncCommands.dispatch

```java
public <T> AsyncCommand<K, V, T> dispatch(RedisCommand<K, V, T> cmd) {
		//用AsyncCommand对RedisCommand做一个包装处理，这个AsyncCommand实现了RedisFuture接口，最后返回给调用方的就是这个对象。当Lettuce收到Redis的返回结果时会调用AsyncCommand的complete方法，异步的方式返回数据。
		AsyncCommand<K, V, T> asyncCommand = new AsyncCommand<>(cmd);
		//调用connection的dispatch方法把Command发送给Redis，这个connection就是上一篇中说的那个StatefulRedisConnectionImpl
		RedisCommand<K, V, T> dispatched = connection.dispatch(asyncCommand);
		if (dispatched instanceof AsyncCommand) {
				return (AsyncCommand<K, V, T>) dispatched;
		}
		return asyncCommand;
}

```

#### StatefulRedisConnectionImpl.dispatch

```java
	@Override
	public <T> RedisCommand<K, V, T> dispatch(RedisCommand<K, V, T> command) {
				//对command做预处理，当前主要是根据不同的命令配置一些异步处理，如：auth命令之后成功之后把password写入到相应变量中，select db操作成功之后把db值写入到相应变量中等等。
        RedisCommand<K, V, T> toSend = preProcessCommand(command);

        try {
						//真正的dispatch是在父类实现的
            return super.dispatch(toSend);
        } finally {
            if (command.getType().name().equals(MULTI.name())) {
                multi = (multi == null ? new MultiOutput<>(codec) : multi);
            }
        }
    }
	//父类RedisChannelHandler的dispatch方法
	protected <T> RedisCommand<K, V, T> dispatch(RedisCommand<K, V, T> cmd) {

			if (debugEnabled) {
					logger.debug("dispatching command {}", cmd);
			}
			//tracingEnable的代码先不用看
			if (tracingEnabled) {

					RedisCommand<K, V, T> commandToSend = cmd;
					TraceContextProvider provider = CommandWrapper.unwrap(cmd, TraceContextProvider.class);

					if (provider == null) {
							commandToSend = new TracedCommand<>(cmd, clientResources.tracing()
											.initialTraceContextProvider().getTraceContext());
					}

					return channelWriter.write(commandToSend);
			}
			//其实就是直接调用channelWriter.write方法，而这个channelWriter就是上一节说的那个屏蔽底层channel实现的DefaultEndpoint类
			return channelWriter.write(cmd);
	}

```

#### DefaultEndpoint.write

```java
	@Override
	public <K, V, T> RedisCommand<K, V, T> write(RedisCommand<K, V, T> command) {

		LettuceAssert.notNull(command, "Command must not be null");

			try {
					//sharedLock是Lettuce自己实现的一个共享排他锁。incrementWriters相当于获取一个共享锁，当channel状态发生变化的时候，如断开连接时会获取排他锁执行一些清理操作。
					sharedLock.incrementWriters();
					// validateWrite是验证当前操作是否可以执行，Lettuce内部维护了一个保存已经发送但是还没有收到Redis消息的Command的stack，可以配置这个stack的长度，防止Redis不可用时stack太长导致内存溢出。如果这个stack已经满了，validateWrite会抛出异常
					validateWrite(1);
					//autoFlushCommands默认为true，即每执行一个Redis命令就执行Flush操作发送给Redis，如果设置为false，则需要手动flush。由于flush操作相对较重，在某些场景下需要继续提升Lettuce的吞吐量可以考虑设置为false。
					if (autoFlushCommands) {
							if (isConnected()) {
									//写入channel并执行flush操作，核心在这个方法的实现中
									writeToChannelAndFlush(command);
							} else {
									// 如果当前channel连接已经断开就先放入Buffer中，直接返回AsyncCommand，重连之后会把Buffer中的Command再次尝试通过channel发送到Redis中
									writeToDisconnectedBuffer(command);
							}

					} else {
							writeToBuffer(command);
					}
			} finally {
					//释放共享锁
					sharedLock.decrementWriters();
					if (debugEnabled) {
							logger.debug("{} write() done", logPrefix());
					}
			}

			return command;
	}

```

#### DefaultEndpoint.writeToChannelAndFlush

```java
	private void writeToChannelAndFlush(RedisCommand<?, ?, ?> command) {
				//queueSize字段做cas  1操作
        QUEUE_SIZE.incrementAndGet(this);
				
        ChannelFuture channelFuture = channelWriteAndFlush(command);
				//Lettuce的可靠性：保证最多一次。由于Lettuce的保证是基于内存的，所以并不可靠（系统crash时内存数据会丢失）
        if (reliability == Reliability.AT_MOST_ONCE) {
            // cancel on exceptions and remove from queue, because there is no housekeeping
            channelFuture.addListener(AtMostOnceWriteListener.newInstance(this, command));
        }
				//Lettuce的可靠性：保证最少一次。由于Lettuce的保证是基于内存的，所以并不可靠（系统crash时内存数据会丢失）
        if (reliability == Reliability.AT_LEAST_ONCE) {
            // commands are ok to stay within the queue, reconnect will retrigger them
            channelFuture.addListener(RetryListener.newInstance(this, command));
        }
    }
		
		//可以看到最终还是调用了channle的writeAndFlush操作，这个Channel就是netty中的NioSocketChannel
		private ChannelFuture channelWriteAndFlush(RedisCommand<?, ?, ?> command) {

        if (debugEnabled) {
            logger.debug("{} write() writeAndFlush command {}", logPrefix(), command);
        }

        return channel.writeAndFlush(command);
    }

```

到这里其实就牵扯到Netty的Channel、EventLoop相关概念了，简单的说channel会把需要write的对象放入Channel对应的EventLoop的队列中就返回了，EventLoop是一个SingleThreadEventExector，它会回调Bootstrap时配置的CommandHandler的write方法

```java
public void write(ChannelHandlerContext ctx, Object msg, ChannelPromise promise) throws Exception {

	if (debugEnabled) {
			logger.debug("{} write(ctx, {}, promise)", logPrefix(), msg);
	}
				
	if (msg instanceof RedisCommand) {
		//如果是单个的RedisCommand就直接调用writeSingleCommand返回
		writeSingleCommand(ctx, (RedisCommand<?, ?, ?>) msg, promise);
		return;
	}

	if (msg instanceof List) {

		List<RedisCommand<?, ?, ?>> batch = (List<RedisCommand<?, ?, ?>>) msg;

		if (batch.size() == 1) {

				writeSingleCommand(ctx, batch.get(0), promise);
				return;
		}
		//批量写操作，暂不关心
		writeBatch(ctx, batch, promise);
		return;
	}

	if (msg instanceof Collection) {
		writeBatch(ctx, (Collection<RedisCommand<?, ?, ?>>) msg, promise);
	}
}

```

#### writeSingleCommand 核心在这里

Lettuce使用单一连接支持多线程并发向Redis发送Command，那Lettuce是怎么把请求Command与Redis返回的结果对应起来的呢，秘密就在这里。

```java
private void writeSingleCommand(ChannelHandlerContext ctx, RedisCommand<?, ?, ?> command, ChannelPromise promise)
 {

	if (!isWriteable(command)) {
			promise.trySuccess();
			return;
	}
	//把当前command放入一个特定的栈中，这一步是关键
	addToStack(command, promise);
	// Trace操作，暂不关心
	if (tracingEnabled && command instanceof CompleteableCommand) {
			...
	}
	//调用ChannelHandlerContext把命令真正发送给Redis，当然在发送给Redis之前会由CommandEncoder类对RedisCommand进行编码后写入ByteBuf
	ctx.write(command, promise);
	
	private void addToStack(RedisCommand<?, ?, ?> command, ChannelPromise promise) {

		try {
			//再次验证队列是否满了，如果满了就抛出异常
			validateWrite(1);
			//command.getOutput() == null意味这个这个Command不需要Redis返回影响。一般不会走这个分支
			if (command.getOutput() == null) {
					// fire&forget commands are excluded from metrics
					complete(command);
			}
			//这个应该是用来做metrics统计用的，暂时先不考虑
			RedisCommand<?, ?, ?> redisCommand = potentiallyWrapLatencyCommand(command);
			//无论promise是什么类型的，最终都会把command放入到stack中，stack是一个基于数组实现的双向队列
			if (promise.isVoid()) {
					//如果promise不是Future类型的就直接把当前command放入到stack
					stack.add(redisCommand);
			} else {
					//如果promise是Future类型的就等future完成后把当前command放入到stack中，当前场景下就是走的这个分支
					promise.addListener(AddToStack.newInstance(stack, redisCommand));
			}
		} catch (Exception e) {
			command.completeExceptionally(e);
			throw e;
		}
	}
}

```

那么Lettuce收到Redis的回复消息之后是怎么通知RedisCommand，并且把结果与RedisCommand对应上的呢。Netty在收到Redis服务端返回的消息之后就会回调CommandHandler的channelRead方法

```java
public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {

        ByteBuf input = (ByteBuf) msg;

        ...

        try {
            ...
						//重点在这里
            decode(ctx, buffer);
        } finally {
            input.release();
        }
    }
		
		protected void decode(ChannelHandlerContext ctx, ByteBuf buffer) throws InterruptedException {
				//如果stack为空，则直接返回，这个时候一般意味着返回的结果找到对应的RedisCommand了
        if (pristine && stack.isEmpty() && buffer.isReadable()) {

            ...

            return;
        }

        while (canDecode(buffer)) {
						//重点来了。从stack的头上取第一个RedisCommand
            RedisCommand<?, ?, ?> command = stack.peek();
            if (debugEnabled) {
                logger.debug("{} Stack contains: {} commands", logPrefix(), stack.size());
            }

            pristine = false;

            try {
								//直接把返回的结果buffer给了stack头上的第一个RedisCommand。
								//decode操作实际上拿到RedisCommand的commandoutput对象对Redis的返回结果进行反序列化的。
                if (!decode(ctx, buffer, command)) {
                    return;
                }
            } catch (Exception e) {

                ctx.close();
                throw e;
            }

            if (isProtectedMode(command)) {
                onProtectedMode(command.getOutput().getError());
            } else {

                if (canComplete(command)) {
                    stack.poll();

                    try {
                        complete(command);
                    } catch (Exception e) {
                        logger.warn("{} Unexpected exception during request: {}", logPrefix, e.toString(), e);
                    }
                }
            }

            afterDecode(ctx, command);
        }

        if (buffer.refCnt() != 0) {
            buffer.discardReadBytes();
        }
    }

```

从上面的代码可以看出来，当Lettuce收到Redis的回复消息时就从stack的头上取第一个RedisCommand，这个RedisCommand就是与该Redis返回结果对应的RedisCommand。为什么这样就能对应上呢，是因为Lettuce与Redis之间只有一条tcp连接，在Lettuce端放入stack时是有序的，tcp协议本身是有序的，redis是单线程处理请求的，所以Redis返回的消息也是有序的。这样就能保证Redis中返回的消息一定对应着stack中的第一个RedisCommand。当然如果连接断开又重连了，这个肯定就对应不上了，Lettuc对断线重连也做了特殊处理，防止对应不上。

#### Command.encode

```java
public void encode(ByteBuf buf) {
				
        buf.writeByte('*');
				//写入参数的数量
        CommandArgs.IntegerArgument.writeInteger(buf, 1   (args != null ? args.count() : 0));
				//换行
        buf.writeBytes(CommandArgs.CRLF);
				//写入命令的类型，即get
        CommandArgs.BytesArgument.writeBytes(buf, type.getBytes());

        if (args != null) {
						//调用Args的编码，这里面就会使用我们之前配置的codec序列化，当前使用的是String.UTF8
            args.encode(buf);
        }
    }

```