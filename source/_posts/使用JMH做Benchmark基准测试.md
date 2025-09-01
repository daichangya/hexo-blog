---
title: 使用JMH做Benchmark基准测试
id: 1513
date: 2024-10-31 22:01:59
author: daichangya
permalink: /archives/%E4%BD%BF%E7%94%A8jmh%E5%81%9Abenchmark%E5%9F%BA%E5%87%86%E6%B5%8B%E8%AF%95/
tags: 
 - 测试
---


# BenchMark介绍

最近大佬叫我做下Benchmark，之前一直没接触过，顺便学习一波。

BenchMark 又叫做基准测试，主要用来测试一些方法的性能，可以根据不同的参数以不同的单位进行计算（例如可以使用吞吐量为单位，也可以使用平均时间作为单位，在 BenchmarkMode 里面进行调整）。

# 开始前的步骤

项目使用的是 Maven，因此只要对 pom.xml 添加依赖即可。

```Java
<dependency>
    <groupId>org.openjdk.jmh</groupId>
    <artifactId>jmh-core</artifactId>
    <version>1.19</version>
</dependency>
<dependency>
    <groupId>org.openjdk.jmh</groupId>
    <artifactId>jmh-generator-annprocess</artifactId>
    <version>1.19</version>
    <scope>provided</scope>
</dependency>

```

# 例子

记得之前和宿友讨论 ArrayList 和 LinkedList 的遍历的性能差别，当时以一种不太妥当的方法进行测试，导致无法得到比较好的结果，刚好这里可以使用这两个来进行比较。

## 代码

```Java
package com.psd.benchmark;

import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.runner.Runner;
import org.openjdk.jmh.runner.RunnerException;
import org.openjdk.jmh.runner.options.Options;
import org.openjdk.jmh.runner.options.OptionsBuilder;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.concurrent.TimeUnit;

/**
 * Author: Shadowdsp
 * Date: 18/07/22
 */

@BenchmarkMode(Mode.Throughput) // 吞吐量
@OutputTimeUnit(TimeUnit.MILLISECONDS) // 结果所使用的时间单位
@State(Scope.Thread) // 每个测试线程分配一个实例
@Fork(2) // Fork进行的数目
@Warmup(iterations = 4) // 先预热4轮
@Measurement(iterations = 10) // 进行10轮测试
public class BenchMark {

    @Param({"10", "40", "70", "100"}) // 定义四个参数，之后会分别对这四个参数进行测试
    private int n;

    private List<Integer> array;
    private List<Integer> list;

    @Setup(Level.Trial) // 初始化方法，在全部Benchmark运行之前进行
    public void init() {
        array = new ArrayList<>(0);
        list = new LinkedList<>();
        for (int i = 0; i < n; i++) {
            array.add(i);
            list.add(i);
        }
    }

    @Benchmark
    public void arrayTraverse() {
        for (int i = 0; i < n; i++) {
            array.get(i);
        }
    }

    @Benchmark
    public void listTraverse() {
        for (int i = 0; i < n; i++) {
            list.get(i);
        }
    }

    @TearDown(Level.Trial) // 结束方法，在全部Benchmark运行之后进行
    public void arrayRemove() {
        for (int i = 0; i < n; i++) {
            array.remove(0);
            list.remove(0);
        }
    }

    public static void main(String[] args) throws RunnerException {
        Options options = new OptionsBuilder().include(BenchMark.class.getSimpleName()).build();
        new Runner(options).run();
    }
}


```

## 报告

```Java
E:\Java\JDK8\bin\java "-javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2017.3.1\lib\idea_rt.jar=6182:C:\Program Files\JetBrains\IntelliJ IDEA 2017.3.1\bin" -Dfile.encoding=UTF-8 -classpath E:\Java\JDK8\jre\lib\charsets.jar;E:\Java\JDK8\jre\lib\deploy.jar;E:\Java\JDK8\jre\lib\ext\access-bridge-64.jar;E:\Java\JDK8\jre\lib\ext\cldrdata.jar;E:\Java\JDK8\jre\lib\ext\dnsns.jar;E:\Java\JDK8\jre\lib\ext\jaccess.jar;E:\Java\JDK8\jre\lib\ext\jfxrt.jar;E:\Java\JDK8\jre\lib\ext\localedata.jar;E:\Java\JDK8\jre\lib\ext\nashorn.jar;E:\Java\JDK8\jre\lib\ext\sunec.jar;E:\Java\JDK8\jre\lib\ext\sunjce_provider.jar;E:\Java\JDK8\jre\lib\ext\sunmscapi.jar;E:\Java\JDK8\jre\lib\ext\sunpkcs11.jar;E:\Java\JDK8\jre\lib\ext\zipfs.jar;E:\Java\JDK8\jre\lib\javaws.jar;E:\Java\JDK8\jre\lib\jce.jar;E:\Java\JDK8\jre\lib\jfr.jar;E:\Java\JDK8\jre\lib\jfxswt.jar;E:\Java\JDK8\jre\lib\jsse.jar;E:\Java\JDK8\jre\lib\management-agent.jar;E:\Java\JDK8\jre\lib\plugin.jar;E:\Java\JDK8\jre\lib\resources.jar;E:\Java\JDK8\jre\lib\rt.jar;E:\Java\IdeaProjects\Warehouse\target\classes;E:\Java\maven\LocalWarehouse\junit\junit\4.11\junit-4.11.jar;E:\Java\maven\LocalWarehouse\org\hamcrest\hamcrest-core\1.3\hamcrest-core-1.3.jar;E:\Java\maven\LocalWarehouse\org\springframework\spring-core\4.0.2.RELEASE\spring-core-4.0.2.RELEASE.jar;E:\Java\maven\LocalWarehouse\commons-logging\commons-logging\1.1.3\commons-logging-1.1.3.jar;E:\Java\maven\LocalWarehouse\org\springframework\spring-web\4.0.2.RELEASE\spring-web-4.0.2.RELEASE.jar;E:\Java\maven\LocalWarehouse\org\springframework\spring-beans\4.0.2.RELEASE\spring-beans-4.0.2.RELEASE.jar;E:\Java\maven\LocalWarehouse\org\springframework\spring-context\4.0.2.RELEASE\spring-context-4.0.2.RELEASE.jar;E:\Java\maven\LocalWarehouse\org\springframework\spring-oxm\4.0.2.RELEASE\spring-oxm-4.0.2.RELEASE.jar;E:\Java\maven\LocalWarehouse\org\springframework\spring-tx\4.0.2.RELEASE\spring-tx-4.0.2.RELEASE.jar;E:\Java\maven\LocalWarehouse\org\springframework\spring-jdbc\4.0.2.RELEASE\spring-jdbc-4.0.2.RELEASE.jar;E:\Java\maven\LocalWarehouse\org\springframework\spring-webmvc\4.0.2.RELEASE\spring-webmvc-4.0.2.RELEASE.jar;E:\Java\maven\LocalWarehouse\org\springframework\spring-expression\4.0.2.RELEASE\spring-expression-4.0.2.RELEASE.jar;E:\Java\maven\LocalWarehouse\org\springframework\spring-aop\4.0.2.RELEASE\spring-aop-4.0.2.RELEASE.jar;E:\Java\maven\LocalWarehouse\aopalliance\aopalliance\1.0\aopalliance-1.0.jar;E:\Java\maven\LocalWarehouse\org\springframework\spring-context-support\4.0.2.RELEASE\spring-context-support-4.0.2.RELEASE.jar;E:\Java\maven\LocalWarehouse\org\springframework\spring-test\4.0.2.RELEASE\spring-test-4.0.2.RELEASE.jar;E:\Java\maven\LocalWarehouse\org\mybatis\mybatis\3.2.6\mybatis-3.2.6.jar;E:\Java\maven\LocalWarehouse\org\mybatis\mybatis-spring\1.2.2\mybatis-spring-1.2.2.jar;E:\Java\maven\LocalWarehouse\javax\javaee-api\7.0\javaee-api-7.0.jar;E:\Java\maven\LocalWarehouse\com\sun\mail\javax.mail\1.5.0\javax.mail-1.5.0.jar;E:\Java\maven\LocalWarehouse\javax\activation\activation\1.1\activation-1.1.jar;E:\Java\maven\LocalWarehouse\mysql\mysql-connector-java\5.1.30\mysql-connector-java-5.1.30.jar;E:\Java\maven\LocalWarehouse\commons-dbcp\commons-dbcp\1.2.2\commons-dbcp-1.2.2.jar;E:\Java\maven\LocalWarehouse\commons-pool\commons-pool\1.3\commons-pool-1.3.jar;E:\Java\maven\LocalWarehouse\jstl\jstl\1.2\jstl-1.2.jar;E:\Java\maven\LocalWarehouse\log4j\log4j\1.2.17\log4j-1.2.17.jar;E:\Java\maven\LocalWarehouse\com\alibaba\fastjson\1.1.41\fastjson-1.1.41.jar;E:\Java\maven\LocalWarehouse\org\slf4j\slf4j-api\1.7.7\slf4j-api-1.7.7.jar;E:\Java\maven\LocalWarehouse\org\slf4j\slf4j-log4j12\1.7.7\slf4j-log4j12-1.7.7.jar;E:\Java\maven\LocalWarehouse\org\codehaus\jackson\jackson-mapper-asl\1.9.13\jackson-mapper-asl-1.9.13.jar;E:\Java\maven\LocalWarehouse\org\codehaus\jackson\jackson-core-asl\1.9.13\jackson-core-asl-1.9.13.jar;E:\Java\maven\LocalWarehouse\commons-fileupload\commons-fileupload\1.3.1\commons-fileupload-1.3.1.jar;E:\Java\maven\LocalWarehouse\commons-io\commons-io\2.4\commons-io-2.4.jar;E:\Java\maven\LocalWarehouse\commons-codec\commons-codec\1.9\commons-codec-1.9.jar;E:\Java\maven\LocalWarehouse\org\junit\jupiter\junit-jupiter-api\5.3.0-M1\junit-jupiter-api-5.3.0-M1.jar;E:\Java\maven\LocalWarehouse\org\apiguardian\apiguardian-api\1.0.0\apiguardian-api-1.0.0.jar;E:\Java\maven\LocalWarehouse\org\opentest4j\opentest4j\1.1.0\opentest4j-1.1.0.jar;E:\Java\maven\LocalWarehouse\org\junit\platform\junit-platform-commons\1.3.0-M1\junit-platform-commons-1.3.0-M1.jar;E:\Java\maven\LocalWarehouse\org\openjdk\jmh\jmh-core\1.19\jmh-core-1.19.jar;E:\Java\maven\LocalWarehouse\net\sf\jopt-simple\jopt-simple\4.6\jopt-simple-4.6.jar;E:\Java\maven\LocalWarehouse\org\apache\commons\commons-math3\3.2\commons-math3-3.2.jar com.psd.benchmark.BenchMark
# JMH version: 1.19
# VM version: JDK 1.8.0_144, VM 25.144-b01
# VM invoker: E:\Java\JDK8\jre\bin\java.exe
# VM options: -javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2017.3.1\lib\idea_rt.jar=6182:C:\Program Files\JetBrains\IntelliJ IDEA 2017.3.1\bin -Dfile.encoding=UTF-8
# Warmup: 4 iterations, 1 s each
# Measurement: 10 iterations, 1 s each
# Timeout: 10 min per iteration
# Threads: 1 thread, will synchronize iterations
# Benchmark mode: Throughput, ops/time
# Benchmark: com.psd.benchmark.BenchMark.arrayTraverse
# Parameters: (n = 10)

# Run progress: 0.00% complete, ETA 00:03:44
# Fork: 1 of 2
# Warmup Iteration   1: 189538.902 ops/ms
# Warmup Iteration   2: 287165.702 ops/ms
# Warmup Iteration   3: 282388.510 ops/ms
# Warmup Iteration   4: 277296.753 ops/ms
Iteration   1: 288687.174 ops/ms
Iteration   2: 277046.541 ops/ms
Iteration   3: 288680.458 ops/ms
Iteration   4: 279775.705 ops/ms
Iteration   5: 289098.257 ops/ms
Iteration   6: 287462.515 ops/ms
Iteration   7: 255330.788 ops/ms
Iteration   8: 282631.894 ops/ms
Iteration   9: 277038.372 ops/ms
Iteration  10: 277690.784 ops/ms

# Run progress: 6.25% complete, ETA 00:03:42
# Fork: 2 of 2
# Warmup Iteration   1: 286568.900 ops/ms
# Warmup Iteration   2: 288014.591 ops/ms
# Warmup Iteration   3: 281790.934 ops/ms
# Warmup Iteration   4: 279647.288 ops/ms
Iteration   1: 280839.175 ops/ms
Iteration   2: 289208.462 ops/ms
Iteration   3: 282724.949 ops/ms
Iteration   4: 289762.265 ops/ms
Iteration   5: 284551.820 ops/ms
Iteration   6: 283700.745 ops/ms
Iteration   7: 261083.800 ops/ms
Iteration   8: 283651.988 ops/ms
Iteration   9: 284418.725 ops/ms
Iteration  10: 282418.733 ops/ms


Result "com.psd.benchmark.BenchMark.arrayTraverse":
  281290.158 ±(99.9%) 7750.303 ops/ms [Average]
  (min, avg, max) = (255330.788, 281290.158, 289762.265), stdev = 8925.261
  CI (99.9%): [273539.854, 289040.461] (assumes normal distribution)


# JMH version: 1.19
# VM version: JDK 1.8.0_144, VM 25.144-b01
# VM invoker: E:\Java\JDK8\jre\bin\java.exe
# VM options: -javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2017.3.1\lib\idea_rt.jar=6182:C:\Program Files\JetBrains\IntelliJ IDEA 2017.3.1\bin -Dfile.encoding=UTF-8
# Warmup: 4 iterations, 1 s each
# Measurement: 10 iterations, 1 s each
# Timeout: 10 min per iteration
# Threads: 1 thread, will synchronize iterations
# Benchmark mode: Throughput, ops/time
# Benchmark: com.psd.benchmark.BenchMark.arrayTraverse
# Parameters: (n = 40)

# Run progress: 12.50% complete, ETA 00:03:27
# Fork: 1 of 2
# Warmup Iteration   1: 277185.994 ops/ms
# Warmup Iteration   2: 277343.966 ops/ms
# Warmup Iteration   3: 289105.366 ops/ms
# Warmup Iteration   4: 281931.930 ops/ms
Iteration   1: 279532.380 ops/ms
Iteration   2: 278419.091 ops/ms
Iteration   3: 281165.591 ops/ms
Iteration   4: 288999.045 ops/ms
Iteration   5: 277378.462 ops/ms
Iteration   6: 275360.726 ops/ms
Iteration   7: 282858.013 ops/ms
Iteration   8: 283601.524 ops/ms
Iteration   9: 279043.295 ops/ms
Iteration  10: 279976.466 ops/ms

# Run progress: 18.75% complete, ETA 00:03:12
# Fork: 2 of 2
# Warmup Iteration   1: 284211.718 ops/ms
# Warmup Iteration   2: 287327.346 ops/ms
# Warmup Iteration   3: 268548.012 ops/ms
# Warmup Iteration   4: 289429.098 ops/ms
Iteration   1: 283348.446 ops/ms
Iteration   2: 262579.782 ops/ms
Iteration   3: 283534.897 ops/ms
Iteration   4: 266160.111 ops/ms
Iteration   5: 289614.776 ops/ms
Iteration   6: 274270.699 ops/ms
Iteration   7: 267829.186 ops/ms
Iteration   8: 279612.742 ops/ms
Iteration   9: 283569.117 ops/ms
Iteration  10: 288172.441 ops/ms


Result "com.psd.benchmark.BenchMark.arrayTraverse":
  279251.339 ±(99.9%) 6287.385 ops/ms [Average]
  (min, avg, max) = (262579.782, 279251.339, 289614.776), stdev = 7240.561
  CI (99.9%): [272963.955, 285538.724] (assumes normal distribution)


# JMH version: 1.19
# VM version: JDK 1.8.0_144, VM 25.144-b01
# VM invoker: E:\Java\JDK8\jre\bin\java.exe
# VM options: -javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2017.3.1\lib\idea_rt.jar=6182:C:\Program Files\JetBrains\IntelliJ IDEA 2017.3.1\bin -Dfile.encoding=UTF-8
# Warmup: 4 iterations, 1 s each
# Measurement: 10 iterations, 1 s each
# Timeout: 10 min per iteration
# Threads: 1 thread, will synchronize iterations
# Benchmark mode: Throughput, ops/time
# Benchmark: com.psd.benchmark.BenchMark.arrayTraverse
# Parameters: (n = 70)

# Run progress: 25.00% complete, ETA 00:02:57
# Fork: 1 of 2
# Warmup Iteration   1: 276172.253 ops/ms
# Warmup Iteration   2: 284624.007 ops/ms
# Warmup Iteration   3: 288356.101 ops/ms
# Warmup Iteration   4: 284278.064 ops/ms
Iteration   1: 287831.035 ops/ms
Iteration   2: 286518.388 ops/ms
Iteration   3: 287016.992 ops/ms
Iteration   4: 282654.336 ops/ms
Iteration   5: 287899.254 ops/ms
Iteration   6: 287299.594 ops/ms
Iteration   7: 284624.713 ops/ms
Iteration   8: 287280.777 ops/ms
Iteration   9: 268079.560 ops/ms
Iteration  10: 266327.469 ops/ms

# Run progress: 31.25% complete, ETA 00:02:42
# Fork: 2 of 2
# Warmup Iteration   1: 282831.765 ops/ms
# Warmup Iteration   2: 271396.073 ops/ms
# Warmup Iteration   3: 280114.449 ops/ms
# Warmup Iteration   4: 272365.705 ops/ms
Iteration   1: 287276.286 ops/ms
Iteration   2: 258473.510 ops/ms
Iteration   3: 287822.759 ops/ms
Iteration   4: 281849.137 ops/ms
Iteration   5: 281739.415 ops/ms
Iteration   6: 271390.808 ops/ms
Iteration   7: 279252.964 ops/ms
Iteration   8: 280445.016 ops/ms
Iteration   9: 287019.516 ops/ms
Iteration  10: 283679.804 ops/ms


Result "com.psd.benchmark.BenchMark.arrayTraverse":
  281224.067 ±(99.9%) 7376.077 ops/ms [Average]
  (min, avg, max) = (258473.510, 281224.067, 287899.254), stdev = 8494.301
  CI (99.9%): [273847.990, 288600.143] (assumes normal distribution)


# JMH version: 1.19
# VM version: JDK 1.8.0_144, VM 25.144-b01
# VM invoker: E:\Java\JDK8\jre\bin\java.exe
# VM options: -javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2017.3.1\lib\idea_rt.jar=6182:C:\Program Files\JetBrains\IntelliJ IDEA 2017.3.1\bin -Dfile.encoding=UTF-8
# Warmup: 4 iterations, 1 s each
# Measurement: 10 iterations, 1 s each
# Timeout: 10 min per iteration
# Threads: 1 thread, will synchronize iterations
# Benchmark mode: Throughput, ops/time
# Benchmark: com.psd.benchmark.BenchMark.arrayTraverse
# Parameters: (n = 100)

# Run progress: 37.50% complete, ETA 00:02:27
# Fork: 1 of 2
# Warmup Iteration   1: 277758.992 ops/ms
# Warmup Iteration   2: 283193.840 ops/ms
# Warmup Iteration   3: 280441.005 ops/ms
# Warmup Iteration   4: 284059.500 ops/ms
Iteration   1: 288156.207 ops/ms
Iteration   2: 277402.478 ops/ms
Iteration   3: 274760.100 ops/ms
Iteration   4: 280052.747 ops/ms
Iteration   5: 261148.816 ops/ms
Iteration   6: 281093.340 ops/ms
Iteration   7: 278472.671 ops/ms
Iteration   8: 257387.342 ops/ms
Iteration   9: 258938.869 ops/ms
Iteration  10: 281241.529 ops/ms

# Run progress: 43.75% complete, ETA 00:02:12
# Fork: 2 of 2
# Warmup Iteration   1: 261991.159 ops/ms
# Warmup Iteration   2: 272490.286 ops/ms
# Warmup Iteration   3: 283308.053 ops/ms
# Warmup Iteration   4: 262856.702 ops/ms
Iteration   1: 283588.427 ops/ms
Iteration   2: 289665.875 ops/ms
Iteration   3: 242227.467 ops/ms
Iteration   4: 235915.418 ops/ms
Iteration   5: 282235.546 ops/ms
Iteration   6: 262060.151 ops/ms
Iteration   7: 249476.606 ops/ms
Iteration   8: 289452.132 ops/ms
Iteration   9: 249939.347 ops/ms
Iteration  10: 268307.387 ops/ms


Result "com.psd.benchmark.BenchMark.arrayTraverse":
  269576.123 ±(99.9%) 14237.446 ops/ms [Average]
  (min, avg, max) = (235915.418, 269576.123, 289665.875), stdev = 16395.864
  CI (99.9%): [255338.677, 283813.569] (assumes normal distribution)


# JMH version: 1.19
# VM version: JDK 1.8.0_144, VM 25.144-b01
# VM invoker: E:\Java\JDK8\jre\bin\java.exe
# VM options: -javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2017.3.1\lib\idea_rt.jar=6182:C:\Program Files\JetBrains\IntelliJ IDEA 2017.3.1\bin -Dfile.encoding=UTF-8
# Warmup: 4 iterations, 1 s each
# Measurement: 10 iterations, 1 s each
# Timeout: 10 min per iteration
# Threads: 1 thread, will synchronize iterations
# Benchmark mode: Throughput, ops/time
# Benchmark: com.psd.benchmark.BenchMark.listTraverse
# Parameters: (n = 10)

# Run progress: 50.00% complete, ETA 00:01:58
# Fork: 1 of 2
# Warmup Iteration   1: 44140.774 ops/ms
# Warmup Iteration   2: 32207.674 ops/ms
# Warmup Iteration   3: 36260.862 ops/ms
# Warmup Iteration   4: 32678.534 ops/ms
Iteration   1: 35846.579 ops/ms
Iteration   2: 34837.967 ops/ms
Iteration   3: 36439.906 ops/ms
Iteration   4: 36522.320 ops/ms
Iteration   5: 35112.493 ops/ms
Iteration   6: 35687.937 ops/ms
Iteration   7: 35727.530 ops/ms
Iteration   8: 31676.889 ops/ms
Iteration   9: 36219.853 ops/ms
Iteration  10: 35857.764 ops/ms

# Run progress: 56.25% complete, ETA 00:01:43
# Fork: 2 of 2
# Warmup Iteration   1: 34479.354 ops/ms
# Warmup Iteration   2: 34805.614 ops/ms
# Warmup Iteration   3: 37839.045 ops/ms
# Warmup Iteration   4: 38778.482 ops/ms
Iteration   1: 37184.558 ops/ms
Iteration   2: 35340.593 ops/ms
Iteration   3: 37976.310 ops/ms
Iteration   4: 39359.895 ops/ms
Iteration   5: 37142.984 ops/ms
Iteration   6: 38973.376 ops/ms
Iteration   7: 38609.058 ops/ms
Iteration   8: 39516.419 ops/ms
Iteration   9: 33589.403 ops/ms
Iteration  10: 37153.584 ops/ms


Result "com.psd.benchmark.BenchMark.listTraverse":
  36438.771 ±(99.9%) 1680.987 ops/ms [Average]
  (min, avg, max) = (31676.889, 36438.771, 39516.419), stdev = 1935.828
  CI (99.9%): [34757.784, 38119.758] (assumes normal distribution)


# JMH version: 1.19
# VM version: JDK 1.8.0_144, VM 25.144-b01
# VM invoker: E:\Java\JDK8\jre\bin\java.exe
# VM options: -javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2017.3.1\lib\idea_rt.jar=6182:C:\Program Files\JetBrains\IntelliJ IDEA 2017.3.1\bin -Dfile.encoding=UTF-8
# Warmup: 4 iterations, 1 s each
# Measurement: 10 iterations, 1 s each
# Timeout: 10 min per iteration
# Threads: 1 thread, will synchronize iterations
# Benchmark mode: Throughput, ops/time
# Benchmark: com.psd.benchmark.BenchMark.listTraverse
# Parameters: (n = 40)

# Run progress: 62.50% complete, ETA 00:01:28
# Fork: 1 of 2
# Warmup Iteration   1: 6381.367 ops/ms
# Warmup Iteration   2: 6267.589 ops/ms
# Warmup Iteration   3: 6070.546 ops/ms
# Warmup Iteration   4: 6311.543 ops/ms
Iteration   1: 6294.215 ops/ms
Iteration   2: 6221.013 ops/ms
Iteration   3: 6196.371 ops/ms
Iteration   4: 5960.573 ops/ms
Iteration   5: 5748.201 ops/ms
Iteration   6: 5494.775 ops/ms
Iteration   7: 5594.778 ops/ms
Iteration   8: 6345.496 ops/ms
Iteration   9: 6141.148 ops/ms
Iteration  10: 6017.750 ops/ms

# Run progress: 68.75% complete, ETA 00:01:13
# Fork: 2 of 2
# Warmup Iteration   1: 6369.814 ops/ms
# Warmup Iteration   2: 6258.675 ops/ms
# Warmup Iteration   3: 5802.971 ops/ms
# Warmup Iteration   4: 6028.703 ops/ms
Iteration   1: 6192.258 ops/ms
Iteration   2: 5966.093 ops/ms
Iteration   3: 5958.597 ops/ms
Iteration   4: 6171.185 ops/ms
Iteration   5: 5617.002 ops/ms
Iteration   6: 5387.913 ops/ms
Iteration   7: 5299.407 ops/ms
Iteration   8: 5939.628 ops/ms
Iteration   9: 5640.087 ops/ms
Iteration  10: 6057.939 ops/ms


Result "com.psd.benchmark.BenchMark.listTraverse":
  5912.221 ±(99.9%) 271.819 ops/ms [Average]
  (min, avg, max) = (5299.407, 5912.221, 6345.496), stdev = 313.027
  CI (99.9%): [5640.403, 6184.040] (assumes normal distribution)


# JMH version: 1.19
# VM version: JDK 1.8.0_144, VM 25.144-b01
# VM invoker: E:\Java\JDK8\jre\bin\java.exe
# VM options: -javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2017.3.1\lib\idea_rt.jar=6182:C:\Program Files\JetBrains\IntelliJ IDEA 2017.3.1\bin -Dfile.encoding=UTF-8
# Warmup: 4 iterations, 1 s each
# Measurement: 10 iterations, 1 s each
# Timeout: 10 min per iteration
# Threads: 1 thread, will synchronize iterations
# Benchmark mode: Throughput, ops/time
# Benchmark: com.psd.benchmark.BenchMark.listTraverse
# Parameters: (n = 70)

# Run progress: 75.00% complete, ETA 00:00:59
# Fork: 1 of 2
# Warmup Iteration   1: 1904.675 ops/ms
# Warmup Iteration   2: 1829.190 ops/ms
# Warmup Iteration   3: 1799.166 ops/ms
# Warmup Iteration   4: 1823.508 ops/ms
Iteration   1: 1483.423 ops/ms
Iteration   2: 1733.061 ops/ms
Iteration   3: 1752.878 ops/ms
Iteration   4: 1877.448 ops/ms
Iteration   5: 1748.907 ops/ms
Iteration   6: 1836.011 ops/ms
Iteration   7: 1830.008 ops/ms
Iteration   8: 1733.991 ops/ms
Iteration   9: 1821.246 ops/ms
Iteration  10: 1827.086 ops/ms

# Run progress: 81.25% complete, ETA 00:00:44
# Fork: 2 of 2
# Warmup Iteration   1: 1858.409 ops/ms
# Warmup Iteration   2: 1816.699 ops/ms
# Warmup Iteration   3: 1810.298 ops/ms
# Warmup Iteration   4: 1704.668 ops/ms
Iteration   1: 1772.384 ops/ms
Iteration   2: 1619.981 ops/ms
Iteration   3: 1754.014 ops/ms
Iteration   4: 1767.706 ops/ms
Iteration   5: 1706.000 ops/ms
Iteration   6: 1646.038 ops/ms
Iteration   7: 1789.584 ops/ms
Iteration   8: 1746.964 ops/ms
Iteration   9: 1785.779 ops/ms
Iteration  10: 1813.610 ops/ms


Result "com.psd.benchmark.BenchMark.listTraverse":
  1752.306 ±(99.9%) 77.143 ops/ms [Average]
  (min, avg, max) = (1483.423, 1752.306, 1877.448), stdev = 88.838
  CI (99.9%): [1675.163, 1829.449] (assumes normal distribution)


# JMH version: 1.19
# VM version: JDK 1.8.0_144, VM 25.144-b01
# VM invoker: E:\Java\JDK8\jre\bin\java.exe
# VM options: -javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2017.3.1\lib\idea_rt.jar=6182:C:\Program Files\JetBrains\IntelliJ IDEA 2017.3.1\bin -Dfile.encoding=UTF-8
# Warmup: 4 iterations, 1 s each
# Measurement: 10 iterations, 1 s each
# Timeout: 10 min per iteration
# Threads: 1 thread, will synchronize iterations
# Benchmark mode: Throughput, ops/time
# Benchmark: com.psd.benchmark.BenchMark.listTraverse
# Parameters: (n = 100)

# Run progress: 87.50% complete, ETA 00:00:29
# Fork: 1 of 2
# Warmup Iteration   1: 784.637 ops/ms
# Warmup Iteration   2: 803.586 ops/ms
# Warmup Iteration   3: 780.992 ops/ms
# Warmup Iteration   4: 812.284 ops/ms
Iteration   1: 771.280 ops/ms
Iteration   2: 725.038 ops/ms
Iteration   3: 781.465 ops/ms
Iteration   4: 753.939 ops/ms
Iteration   5: 753.920 ops/ms
Iteration   6: 813.238 ops/ms
Iteration   7: 778.423 ops/ms
Iteration   8: 809.902 ops/ms
Iteration   9: 769.837 ops/ms
Iteration  10: 767.709 ops/ms

# Run progress: 93.75% complete, ETA 00:00:14
# Fork: 2 of 2
# Warmup Iteration   1: 703.812 ops/ms
# Warmup Iteration   2: 752.538 ops/ms
# Warmup Iteration   3: 774.776 ops/ms
# Warmup Iteration   4: 813.269 ops/ms
Iteration   1: 796.985 ops/ms
Iteration   2: 687.697 ops/ms
Iteration   3: 808.395 ops/ms
Iteration   4: 736.341 ops/ms
Iteration   5: 761.328 ops/ms
Iteration   6: 746.422 ops/ms
Iteration   7: 767.855 ops/ms
Iteration   8: 814.670 ops/ms
Iteration   9: 772.441 ops/ms
Iteration  10: 731.986 ops/ms


Result "com.psd.benchmark.BenchMark.listTraverse":
  767.444 ±(99.9%) 28.363 ops/ms [Average]
  (min, avg, max) = (687.697, 767.444, 814.670), stdev = 32.662
  CI (99.9%): [739.081, 795.806] (assumes normal distribution)


# Run complete. Total time: 00:03:56
(一般只需要关注这下面的东西)

Benchmark                (n)   Mode  Cnt       Score       Error   Units
BenchMark.arrayTraverse   10  thrpt   20  281290.158 ±  7750.303  ops/ms
BenchMark.arrayTraverse   40  thrpt   20  279251.339 ±  6287.385  ops/ms
BenchMark.arrayTraverse   70  thrpt   20  281224.067 ±  7376.077  ops/ms
BenchMark.arrayTraverse  100  thrpt   20  269576.123 ± 14237.446  ops/ms
BenchMark.listTraverse    10  thrpt   20   36438.771 ±  1680.987  ops/ms
BenchMark.listTraverse    40  thrpt   20    5912.221 ±   271.819  ops/ms
BenchMark.listTraverse    70  thrpt   20    1752.306 ±    77.143  ops/ms
BenchMark.listTraverse   100  thrpt   20     767.444 ±    28.363  ops/ms

Process finished with exit code 0


```

报告很长，因为这里的n有四种情况，然后有两个 @Benchmark 方法，因此会进行8次测试。

大多数情况只需要关注最下面的结果。

可以结合 Score 和 Unit 这两列，看到方法的效率。这里显然 `arrayTraverse` 的效率比 `listTraverse` 的高很多，因为 `Unit` 单位是 `ops/ms`，即单位时间内执行的操作数。所以显然在遍历的时候，ArrayList的效率是比LinkedList高的。

# 注解介绍

## @BenchmarkMode

Mode 表示 JMH 进行 Benchmark 时所使用的模式。通常是测量的维度不同，或是测量的方式不同。目前 JMH 共有四种模式：

1.  Throughput: 整体吞吐量，例如“1秒内可以执行多少次调用”，单位是操作数/时间。
2.  AverageTime: 调用的平均时间，例如“每次调用平均耗时xxx毫秒”，单位是时间/操作数。
3.  SampleTime: 随机取样，最后输出取样结果的分布，例如“99%的调用在xxx毫秒以内，99.99%的调用在xxx毫秒以内”
4.  SingleShotTime: 以上模式都是默认一次 iteration 是 1s，唯有 SingleShotTime 是只运行一次。往往同时把 warmup 次数设为0，用于测试冷启动时的性能。

## @OutputTimeUnit

输出的时间单位。

## @Iteration

Iteration 是 JMH 进行测试的最小单位。在大部分模式下，一次 iteration 代表的是一秒，JMH 会在这一秒内不断调用需要 Benchmark 的方法，然后根据模式对其采样，计算吞吐量，计算平均执行时间等。

## @WarmUp

Warmup 是指在实际进行 Benchmark 前先进行预热的行为。

为什么需要预热？因为 JVM 的 JIT 机制的存在，如果某个函数被调用多次之后，JVM 会尝试将其编译成为机器码从而提高执行速度。为了让 Benchmark 的结果更加接近真实情况就需要进行预热。

## @State

类注解，JMH测试类必须使用 @State 注解，它定义了一个类实例的生命周期，可以类比 Spring Bean 的 Scope。由于 JMH 允许多线程同时执行测试，不同的选项含义如下：

1.  Scope.Thread：默认的 State，每个测试线程分配一个实例；
2.  Scope.Benchmark：所有测试线程共享一个实例，用于测试有状态实例在多线程共享下的性能；
3.  Scope.Group：每个线程组共享一个实例；

## @Fork

进行 fork 的次数。如果 fork 数是2的话，则 JMH 会 fork 出两个进程来进行测试。

## @Meansurement

提供真正的测试阶段参数。指定迭代的次数，每次迭代的运行时间和每次迭代测试调用的数量(通常使用 @BenchmarkMode(Mode.SingleShotTime) 测试一组操作的开销——而不使用循环)

## @Setup

方法注解，会在执行 benchmark 之前被执行，正如其名，主要用于初始化。

## @TearDown

方法注解，与@Setup 相对的，会在所有 benchmark 执行结束以后执行，主要用于资源的回收等。

@Setup/@TearDown注解使用Level参数来指定何时调用fixture：

| 名称 | 描述 |
| --- | --- |
| Level.Trial | 默认level。全部benchmark运行(一组迭代)之前/之后 |
| Level.Iteration | 一次迭代之前/之后(一组调用) |
| Level.Invocation | 每个方法调用之前/之后(不推荐使用，除非你清楚这样做的目的) |

## @Benchmark

方法注解，表示该方法是需要进行 benchmark 的对象。

## @Param

成员注解，可以用来指定某项参数的多种情况。特别适合用来测试一个函数在不同的参数输入的情况下的性能。@Param 注解接收一个String数组，在 @Setup 方法执行前转化为为对应的数据类型。多个 @Param 注解的成员之间是乘积关系，譬如有两个用 @Param 注解的字段，第一个有5个值，第二个字段有2个值，那么每个测试方法会跑5*2=10次。
