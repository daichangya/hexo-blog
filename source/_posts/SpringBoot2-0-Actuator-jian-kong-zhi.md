---
title: SpringBoot2.0 Actuator监控指标分析
id: 1433
date: 2024-10-31 22:01:55
author: daichangya
permalink: /archives/SpringBoot2-0-Actuator-jian-kong-zhi/
tags:
- 监控
---

 

# 基于SpringBoot2.0+ Actuator metrics的监控(基于Oracle JDK9，G1)

## 引言

SpringBoot2在spring-boot-actuator中引入了micrometer，对1.x的metrics进行了重构，另外支持对接的监控系统也更加丰富(Atlas、Datadog、Ganglia、Graphite、Influx、JMX、NewRelic、Prometheus、SignalFx、StatsD、Wavefront)。本文以Prometheus为例阐述SpringBoot2.0的监控。

## eg. Prometheus
[Prometheus中文文档](https://daichangya.github.io/prometheus.io/#/3-prometheus/basics)
### Maven坐标

```
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>

```

### 配置信息

```php
management.endpoints.web.exposure.include=*

```

## SpringBoot2.0 Actuator监控指标分析

| 序号 | 参数 | 参数说明 | 是否监控 | 监控手段 | 重要度 |
| --- | --- | --- | --- | --- | --- |
| \-\-\- | JVM | \-\-\- |   |   |   |
| 1 | jvm.memory.max | JVM最大内存 |   |   |   |
| 2 | jvm.memory.committed | JVM可用内存 | 是 | 展示并监控堆内存和Metaspace | 重要 |
| 3 | jvm.memory.used | JVM已用内存 | 是 | 展示并监控堆内存和Metaspace | 重要 |
| 4 | jvm.buffer.memory.used | JVM缓冲区已用内存 |   |   |   |
| 5 | jvm.buffer.count | 当前缓冲区数 |   |   |   |
| 6 | jvm.threads.daemon | JVM守护线程数 | 是 | 显示在监控页面 |   |
| 7 | jvm.threads.live | JVM当前活跃线程数 | 是 | 显示在监控页面；监控达到阈值时报警 | 重要 |
| 8 | jvm.threads.peak | JVM峰值线程数 | 是 | 显示在监控页面 |   |
| 9 | jvm.classes.loaded | 加载classes数 |   |   |   |
| 10 | jvm.classes.unloaded | 未加载的classes数 |   |   |   |
| 11 | jvm.gc.memory.allocated | GC时，年轻代分配的内存空间 |   |   |   |
| 12 | jvm.gc.memory.promoted | GC时，老年代分配的内存空间 |   |   |   |
| 13 | jvm.gc.max.data.size | GC时，老年代的最大内存空间 |   |   |   |
| 14 | jvm.gc.live.data.size | FullGC时，老年代的内存空间 |   |   |   |
| 15 | jvm.gc.pause | GC耗时 | 是 | 显示在监控页面 |   |
| \-\-\- | TOMCAT | \-\-\- |   |   |   |
| 16 | tomcat.sessions.created | tomcat已创建session数 |   |   |   |
| 17 | tomcat.sessions.expired | tomcat已过期session数 |   |   |   |
| 18 | tomcat.sessions.active.current | tomcat活跃session数 |   |   |   |
| 19 | tomcat.sessions.active.max | tomcat最多活跃session数 | 是 | 显示在监控页面，超过阈值可报警或者进行动态扩容 | 重要 |
| 20 | tomcat.sessions.alive.max.second | tomcat最多活跃session数持续时间 |   |   |   |
| 21 | tomcat.sessions.rejected | 超过session最大配置后，拒绝的session个数 | 是 | 显示在监控页面，方便分析问题 |   |
| 22 | tomcat.global.error | 错误总数 | 是 | 显示在监控页面，方便分析问题 |   |
| 23 | tomcat.global.sent | 发送的字节数 |   |   |   |
| 24 | tomcat.global.request.max | request最长时间 |   |   |   |
| 25 | tomcat.global.request | 全局request次数和时间 |   |   |   |
| 26 | tomcat.global.received | 全局received次数和时间 |   |   |   |
| 27 | tomcat.servlet.request | servlet的请求次数和时间 |   |   |   |
| 28 | tomcat.servlet.error | servlet发生错误总数 |   |   |   |
| 29 | tomcat.servlet.request.max | servlet请求最长时间 |   |   |   |
| 30 | tomcat.threads.busy | tomcat繁忙线程 | 是 | 显示在监控页面，据此检查是否有线程夯住 |   |
| 31 | tomcat.threads.current | tomcat当前线程数（包括守护线程） | 是 | 显示在监控页面 | 重要 |
| 32 | tomcat.threads.config.max | tomcat配置的线程最大数 | 是 | 显示在监控页面 | 重要 |
| 33 | tomcat.cache.access | tomcat读取缓存次数 |   |   |   |
| 34 | tomcat.cache.hit | tomcat缓存命中次数 |   |   |   |
| \-\-\- | CPU... | \-\-\- |   |   |   |
| 35 | system.cpu.count | CPU数量 |   |   |   |
| 36 | system.load.average.1m | load average | 是 | 超过阈值报警 | 重要 |
| 37 | system.cpu.usage | 系统CPU使用率 |   |   |   |
| 38 | process.cpu.usage | 当前进程CPU使用率 | 是 | 超过阈值报警 |   |
| 39 | http.server.requests | http请求调用情况 | 是 | 显示10个请求量最大，耗时最长的URL；统计非200的请求量 | 重要 |
| 40 | process.uptime | 应用已运行时间 | 是 | 显示在监控页面 |   |
| 41 | process.files.max | 允许最大句柄数 | 是 | 配合当前打开句柄数使用 |   |
| 42 | process.start.time | 应用启动时间点 | 是 | 显示在监控页面 |   |
| 43 | process.files.open | 当前打开句柄数 | 是 | 监控文件句柄使用率，超过阈值后报警 | 重要 |

监控dashboard可使用grafana。

