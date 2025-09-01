---
title: siege概述
id: 12
date: 2024-10-31 22:01:40
author: daichangya
excerpt: "Siege是一款高性能的Http压力测试工具。Siege支持身份验证、cookies、http、https和ftp协议。安装Siege如果要支持https，需要先下载安装openssl,下载地址：https//github.com/openssl/openssl1.开始安装opensslgitcl"
permalink: /archives/siege/
tags: 
 - 测试
---

```前言
Siege是一款高性能的Http压力测试工具。
Siege支持身份验证、cookies、http、https和ftp协议。

安装Siege
如果要支持https，需要先下载安装openssl, 下载地址：https://github.com/openssl/openssl
1.开始安装openssl

git clone https://github.com/openssl/openssl
cd openssl
./config --prefix=/usr/local/openssl
make
make install
openssl version
2.开始安装siege
下载地址：http://download.joedog.org/siege/siege-4.0.4.tar.gz

tar zxvf siege-4.0.4.tar.gz
cd siege-4.0.4
make clean
./configure --prefix=/usr/local/siege --with-ssl=/usr/local/openssl
make 
make install
siege安装完毕
注意：siege默认只支持255个并发数，可以自己自定义，修改/root/.siege/siege.conf下的limit数值。

命令参数
参数	描述
-V, --version	打印版本号
-h, --help	打印帮助信息
-C, --config	打印当前配置信息
-g, --get	拉取http头信息
-p, --print	打印整个页面的内容
-c, --concurrent=NUM	并发用户数量，默认10个
-r, --reps=NUM	运行次数
-d, --delay=NUM	随机时间延迟(秒）
-b, --benchmark	请求没有延迟
-i, --internet	模拟网络用户随机点击URL
-f, --file=FILE	选择指定的URL文件
-R, --rc=FILE	指定siegerc文件
-l, --log[=FILE]	日志文件，默认是 PREFIX/var/siege.log
-H, --header="text"	给请求添加头，支持多个
-A, --user-agent="text"	给请求设置User-Agent
-T, --content-type="text"	给请求设置Content-Type
性能参数
参数	描述
Transactions	命中次数
Availability	命中率
Elapsed time	整个压测花费的时间，从第一个开始到最后一个结束
Data transferred	整个压测数据传输的总和
Response time	响应时间是响应每个模拟用户请求所花费的平均时间
Transaction rate	事务速率是服务器每秒能够处理的平均事务数. 简而言之：事务除以经过的时间。
Throughput	吞吐量是从服务器到所有模拟用户每秒传输的平均字节数
Concurrency	并发是同时连接的平均数，这是一个随服务器性能下降而上升的数字。
Successful transactions	成功事务次数
Failed transactions	失败事务次数
Longest transaction	最长事务时间
Shortest transaction	最短事务时间
应用举例
1.基础应用
siege -c10 -r1 -p url

2.支持多个Header参数
siege -c10 -r1 -p --header="Authorization: Bearer b7c75bae-9d68-4a74-bffb-95eb08a40918" --header="sg: 123456"

3.支持application/json方式请求
siege -c1 -r1 "http://192.168.16.101:6005/bpm/processInstances/review PUT <./1.json "

4.支持从文件读取url
siege -c9 -r1 -f url.txt

```
