---
title: Redis通讯协议
id: 1582
date: 2024-10-31 22:02:02
author: daichangya
permalink: /archives/Redis-tong-xun-xie-yi/
categories:
- redis
tags:
- 协议
---

Redis的通信协议是Redis Serialization Protocol，简称RESP，是二进制安全的，有如下特性：实现简单、快速解析、可读性好

RESP是Redis客户端和服务端通信的协议

Redis 客户端向服务端发送一组命令，服务端根据不同的命令回复不同类型的数据。但是协议的每部分都是以回车换行\r\n结尾。

```
/**
set
abc
123456
*/
 
*3\r\n          //消息一共有三行
$3\r\n          //第一行有字节数为3
set\r\n         //第一行的消息
$3\r\n          //第二行字节数为3
abc\r\n        //第二行的消息
$6\r\n          //第三行字节数为6
123456\r\n      //第三行的消息
+OK\r\n         //操作成功
```

```

daichangyadeMacBook-Pro:~ daichangya$ redis-cli -h localhost -p 6379
localhost:6379> set abc 123456
OK
localhost:6379> get abc
"123456"
localhost:6379> quit
daichangyadeMacBook-Pro:~ daichangya$ telnet localhost  6379
Trying ::1...
Connected to localhost.
Escape character is '^]'.
*2
$3
get
$3
abc
$6
123456
quit
+OK
Connection closed by foreign host.
```