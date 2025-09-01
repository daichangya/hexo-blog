---
title: eclipse maven plugin 插件 安装 和 配置
id: 557
date: 2024-10-31 22:01:44
author: daichangya
excerpt: "maven3 安装：    安装 Maven 之前要求先确定你的 JDK 已经安装配置完成。Maven是 Apache 下的一个项目，目前最新版本是 3.0.4，我用的也是这个。    首先去官网下载 Maven：http//www.apache.org/dyn/closer.cgi"
permalink: /archives/18516669/
tags: 
 - eclipse
---

 环境准备：
```
eclipse（Helios） 3.6  
maven 3.0.4  
```
  

maven3 安装：

    安装 Maven 之前要求先确定你的 JDK 已经安装配置完成。Maven是 Apache 下的一个项目，目前最新版本是 3.0.4，我用的也是这个。

    首先去官网下载 Maven：[http://www.apache.org/dyn/closer.cgi/maven/binaries/apache-maven-3.0.4-bin.tar.gz](http://www.apache.org/dyn/closer.cgi/maven/binaries/apache-maven-3.0.4-bin.tar.gz)

    下载完成之后将其解压，我将解压后的文件夹重命名成 maven，并将它放在 D:\\Server 目录下，即 maven 最终的路径是：D:\\Server\\maven  

  
配置 maven 环境变量：

    系统变量：MAVEN_HOME = D:\\Server\\maven

    用户变量：path = %MAVEN_HOME%\\bin

    相信大家都有配过环境变量的，详细步骤就不说了，对着把属性名和属性值配上的OK了。

    打开 cmd，在里面敲：mvn -version  
  
 ![](http://www.blogjava.net/images/blogjava_net/fancydeepin/111.jpg)  

  
    如果能打印如上信息，说明到此 Maven3 已经在你的电脑上安装完成。  
    mvn 是 mavn 的一个指令，mvn -version 是查看版本信息，我的操作系统是 32位的 WIN7，安装的 maven 是 3.0.4

    如果能打印如上信息，说明到此 Maven3 已经在你的电脑上安装完成。  

  
修改 maven 仓库存放位置：

    找到 maven 下的 conf 下的 settings.xml 配置文件，我的是在 D:\\Server\\maven\\conf\\settings.xml

![](http://www.blogjava.net/images/blogjava_net/fancydeepin/222.jpg)  
  
    maven 的仓库默认是放在本地用户的临时文件夹下面的 .m2 文件夹下的 repository 下，我的是在 C:\\Users\\admcnm\\.m2\\repository 目录下，

    现在我们来修改将它指定到我们自己的路径下，我现在要将仓库指定到 D:\\Repositories\\Maven 目录下，只需要将上面注销的本地仓库打开，

    然后把相应的路径值写到里面去就行了：

![](http://www.blogjava.net/images/blogjava_net/fancydeepin/333.jpg)  

OK，先来体会一下 maven，在 cmd 中敲并回车执行：mvn help:system

    这时候 maven 就会从远程仓库开始下载一大堆的东西，没事，让它下载着，迟早都要下载的，接下来是在 eclipse 中安装 maven 插件，

    使用 eclipse 与 使用 myeclipse 的一个最明显的差异就是，在 eclipse 中，你需要安装好多好多的插件，像 myeclipse 这样高度集成的工具，

    还是不要用太多为好，我这只是说说，至于选 eclipse 还是 myeclipse 还是要看自己或环境来选择，上面就当我扯淡。好咧，说正事，  
  

eclipse 安装插件的方式最常见的有两种：  
    1\. 一种是在线安装，这，貌似是用的最多的，就是：Help  -->  Install New Software，然后输入 HTTP 地址来安装，但有一个很明显的缺点，就是慢！  
    2\. 一种是离线安装，用 link 的方式来安装，这种方式可拔性更好，可以随时将插件插上和拔下，非常方便。  

  
eclipse maven3 安装：

    1\. 使用第一种方式来安装谁都会，只要输入 http 地址：[http://m2eclipse.sonatype.org/sites/m2e](http://m2eclipse.sonatype.org/sites/m2e)，把选项勾上，然后等待它下载安装，完成之后重启 eclipse 即可。  
    2\. 这里我不说上面的那种在线安装，原因有二：第一，安装后不好管理；第二，下载太慢；我接下来要说的是使用 link 方式来离线安装 maven3 插件。

    官网并不提供 maven 插件的离线安装包，一般的，你在网上搜一下，幸运的话应该可以找得到。我已经将 maven 的离线安装包整理出来，供有需要的人下载，

    你可以在我博客的左侧栏中找得到链接下载地址，你也可以直接点击这里的链接下载：[http://115.com/file/dpk80gj0#eclipse-maven3-plugin.7z](http://115.com/file/dpk80gj0#eclipse-maven3-plugin.7z)  
  

link 离线安装 eclipse maven 插件

        1\. 在你的 eclipse 安装的根目录下创建两个文件夹：links，myplugins（名字可以随便取），我的这两个文件夹位于：D:/IDE/HELIOS/eclipse/（作为参考，下面用到）

        2\. 将我 115 网盘提供下载的 eclipse-maven3-plugin.7z 解压缩到 myplugins 目录下

        3\. 在 links 目录下创建一个 maven.txt（名字可以随便取），打开并输入：path=D:/IDE/HELIOS/eclipse/myplugins/maven（请参照上面对应你的 maven 插件）

        4\. 保存关闭 maven.txt，并将后缀改成 maven.link，重启 eclipse（如果你的 eclipse 没有开着，直接打开就行）  
  

检查 eclipse 的 maven 插件是否安装成功：Window  -->  Preferences  
  
![](http://www.blogjava.net/images/blogjava_net/fancydeepin/01.png)  
  
  

配置 maven：  
    1\. 点击 Add 按钮，选到你本机安装 maven 的路径值  
  
![](http://www.blogjava.net/images/blogjava_net/fancydeepin/02.png)  
  
  

    2\. 点击 Browse 按钮，选到你 maven 的 setting.xml 配置文件，然后点击 OK，这样就完成了 eclipse maven 插件的配置  
![](http://www.blogjava.net/images/blogjava_net/fancydeepin/03.png)

 
 

  
  