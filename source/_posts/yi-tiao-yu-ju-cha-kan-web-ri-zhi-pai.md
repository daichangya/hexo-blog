---
title: 一条语句查看web日志排名前十的IP/URL页面及总数
id: 489
date: 2024-10-31 22:01:43
author: daichangya
excerpt: 查看 Nginx web 访问日志访问量前十的ip 以及访问的网站页面地址 ，可以分析网站哪些页面受欢迎，以及访问量大的ip在干什么！
permalink: /archives/yi-tiao-yu-ju-cha-kan-web-ri-zhi-pai/
categories:
- nginx
tags:
- linux
---

查看 Nginx web 访问日志访问量前十的ip 以及访问的网站页面地址 ，可以分析网站哪些页面受欢迎，以及访问量大的ip在干什么！

```  
awk '{print $1}' access.log | sort | uniq -c | sort -nr | head -n 10 
  
#结果 
 391942 211.**.151.218 
 269168 218.**.103.140 
 142282 112.**.20.133 
 105460 112.**.25.241 
  96016 119.**.155.137 
  89926 112.**.31.16 
  83113 218.**.200.19 
  79975 112.**.28.11 
  79890 119.**.156.14 
  72041 124.**.110.72
```
     
```
#如果想查看某一天的 
cat access.log | grep "07/Nov/2013" | awk '{print $1}' |  uniq -c | sort -nr | head -n 10 
#结果 
   3452 60.**.235.88 
   2297 119.**.195.228 
   2258 113.**.145.91 
   1221 123.**.187.223 
    905 211.**.82.175 
    899 117.**.5.207 
    888 112.**.24.202 
    787 110.**.139.183 
    576 143.**.5.44 
    574 125.**.18.21
```

```   
awk '{print $11}' access.log | sort | uniq -c | sort -nr | head -n 10 
  
#结果 
  
1420617 "http://***.com/forum.php" 
 844547 "http://***.com/?fromuid=1180" 
 760045 "http://www.***.com/" 
 697515 "http://www.***.com/forum.php" 
 436309 "http://www.***.com/?fromuid=1080" 
 279609 "http://www.***.com/?fromuid=21" 
 172784 "http://www.***.com/?fromuid=2123" 
 108563 "http://www.***.com/?fromuid=1090" 
  86906 "http://www.***.com/plugin.php?id=sanree_brand:sanree_brand" 
  80661 "http://www.***.com/plugin.php?id=sanree_brand_goods:sanree_brand_goods"
```