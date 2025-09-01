---
title: curl命令分析网站请求耗时
id: 1461
date: 2024-10-31 22:01:56
author: daichangya
permalink: /archives/curl-ming-ling-fen-xi-wang-zhan-qing/
---

  

  

命令：

```bash
curl -w "@curl-format.txt" -o /dev/null -s -L "https://www.jd.com"
```

  

格式：

```bash
# cat curl-format.txt 
   time_namelookup: %{time_namelookup}\n
      time_connect: %{time_connect}\n
   time_appconnect: %{time_appconnect}\n
     time_redirect: %{time_redirect}\n
  time_pretransfer: %{time_pretransfer}\n
time_starttransfer: %{time_starttransfer}\n
                    ----------\n
time_total: %{time_total}\n
```

  

*   time_namelookup： DNS解析时间  
    
*   time_connect：TCP 连接建立的时间，就是三次握手的时间  
    
*   time_appconnect：SSL/SSH 等上层协议建立连接的时间，比如 connect/handshake 的时间  
    
*   time_redirect： 从开始到最后一个请求事务的时间  
    
*   time_pretransfer：从请求开始到响应开始传输的时间  
    
*   time_starttransfer： 从请求开始到第一个字节将要传输的时间  
    
*   time_total：这次请求花费的全部时间
    

  

示例：  

```bash
# curl -w "@curl-format.txt" -o /dev/null -s -L "https://www.jd.com"
   time_namelookup:  0.529108
      time_connect:  0.688685
   time_appconnect:  1.201098
     time_redirect:  0.000000
  time_pretransfer:  1.201304
time_starttransfer:  1.418342
                    ----------
time_total:  1.540865
```

  

*   DNS查询时间：0529108  
    
*   TCP连接时间： time\_connect - time\_namelookup = 0.688685 - 0.529108 = 159ms  
    
*   服务器处理时间：time\_starttransfer - time\_pretransfer = 1.418342 - 1.201304 = 217ms  
    
*   内容传输时间：time\_total - time\_starttransfer = 1.540865 - 1.418342 = 122ms
    

  

  

**命令行指定格式**

```bash
# curl -w "%{time_namelookup}\n%{time_connect}\n%{time_pretransfer}\n%{time_starttransfer}\n%{time_total}" -o /dev/null -s -L "https://www.jd.com"    
0.014314
0.018578
0.044222
0.293051
0.701479
```