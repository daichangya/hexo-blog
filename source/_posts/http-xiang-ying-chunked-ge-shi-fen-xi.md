---
title: http响应chunked格式分析
id: 1454
date: 2024-10-31 22:01:56
author: daichangya
permalink: /archives/http-xiang-ying-chunked-ge-shi-fen-xi/
tags:
- http
---

```language
有的时候服务器生成HTTP回应是无法确定信息大小的，这时用Content-Length就无法事先写入长度，而需要实时生成消息长度，这时服务器一般采用Chunked编码。
在进行Chunked编码传输时，在回复消息的头部有transfer-coding并定义为Chunked，表示将用Chunked编码传输内容。
 
Chunked编码使用若干个Chunk串连而成，由一个标明长度为0的chunk标示结束。每个Chunk分为头部和正文两部分，头部内容指定下一段正文的字符总数（十六进制的数字）和数量单位（一般不写），正文部分就是指定长度的实际内容，两部分之间用回车换行(CRLF)隔开。在最后一个长度为0的Chunk中的内容是称为footer的内容，是一些附加的Header信息（通常可以直接忽略）。
 
我们来模拟一下数据结构：
[Chunk大小][回车][Chunk数据体][回车][Chunk大小][回车][Chunk数据体][回车][0][回车][footer内容（有的话）][回车]
注意chunk-size是以十六进制的ASCII码表示的，比如86AE（实际的十六进制应该是：38366165），计算成长度应该是：34478，表示从回车之后有连续的34478字节的数据。
跟踪了www.yahoo.com的返回数据，发现在chunk-size中，还会多一些空格。可能是固定长度为7个字节，不满7个字节的，就以空格补足，空格的ASCII码是0x20。
 
    解码流程：
    对chunked编码进行解码的目的是将分块的chunk-data整合恢复成一块作为报文体，同时记录此块体的长度。
    RFC2616中附带的解码流程如下：(伪代码）
    length := 0         //长度计数器置0
    read chunk-size, chunk-extension (if any) and CRLF      //读取chunk-size, chunk-extension
                                                          //和CRLF
    while(chunk-size > 0 )   {            //表明不是last-chunk
          read chunk-data and CRLF            //读chunk-size大小的chunk-data,skip CRLF
          append chunk-data to entity-body     //将此块chunk-data追加到entity-body后
          read chunk-size and CRLF          //读取新chunk的chunk-size 和 CRLF
    }
    read entity-header      //entity-header的格式为name:valueCRLF,如果为空即只有CRLF
    while （entity-header not empty)   //即，不是只有CRLF的空行
    {
       append entity-header to existing header fields
       read entity-header
    }
    Content-Length:=length      //将整个解码流程结束后计算得到的新报文体length
                                 //作为Content-Length域的值写入报文中
    Remove "chunked" from Transfer-Encoding  //同时从Transfer-Encoding中域值去除chunked这个标记
 

Sample

Encoded response
HTTP/1.1 200 OK
Content-Type: text/plain
Transfer-Encoding: chunked

25
This is the data in the first chunk

1A
and this is the second one
0


same as above, raw bytes in hex
0000-000F   48 54 54 50 2f 31 2e 31 20 32 30 30 20 4f 4b 0d   HTTP/1.1 200 OK.
0010-001F   0a 43 6f 6e 74 65 6e 74 2d 54 79 70 65 3a 20 74   .Content-Type: t
0020-002F   65 78 74 2f 70 6c 61 69 6e 0d 0a 54 72 61 6e 73   ext/plain..Trans
0030-003F   66 65 72 2d 45 6e 63 6f 64 69 6e 67 3a 20 63 68   fer-Encoding: ch
0040-004F   75 6e 6b 65 64 0d 0a 0d 0a 32 35 0d 0a 54 68 69   unked....25..Thi
0050-005F   73 20 69 73 20 74 68 65 20 64 61 74 61 20 69 6e   s is the data in
0060-006F   20 74 68 65 20 66 69 72 73 74 20 63 68 75 6e 6b    the first chunk
0070-007F   0d 0a 0d 0a 31 41 0d 0a 61 6e 64 20 74 68 69 73   ....1A..and this
0080-008F   20 69 73 20 74 68 65 20 73 65 63 6f 6e 64 20 6f    is the second o
0090-009F   6e 65 0d 0a 30 0d 0a 0d 0a                        ne..0....

same as above, in Java code


public static final byte[] CHUNKED_RESPONSE;
static {		 
	StringBuilder sb = new StringBuilder();
	sb.append("HTTP/1.1 200 OK/r/n");
	sb.append("Content-Type: text/plain/r/n");
	sb.append("Transfer-Encoding: chunked/r/n/r/n");
	sb.append("25/r/n");		
	sb.append("This is the data in the first chunk/r/n"); // 37 bytes of payload
			// (conveniently consisting of ASCII characters only)
	sb.append("/r/n1A/r/n");
	sb.append("and this is the second one"); // 26 bytes of payload
			// (conveniently consisting of ASCII characters only)
	sb.append("/r/n0/r/n/r/n");
	CHUNKED_RESPONSE = sb.toString().getBytes(java.nio.charset.Charset.forName("US-ASCII"));
}



Decoded data
This is the data in the first chunk
and this is the second one

 基本上checked的编码方式。
```
