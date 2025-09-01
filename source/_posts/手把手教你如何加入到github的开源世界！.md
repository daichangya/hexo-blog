---
title: 手把手教你如何加入到github的开源世界！
id: 813
date: 2024-10-31 22:01:46
author: daichangya
excerpt: "以提交的一次开源代码为例，教会你步入开源的世界。1,首先登陆到https//github.com平台上注册一个自己的账号，这个过程就不演示了2，然后在左上部分输入一个开源项目的名字,选择的是jvalidator,回车搜索。3,在搜索结果页面找到如下如图所示的项目，单击项目名称。4,此时，你已经进入到了rinh/jvalidator的项目主页了，单击"
permalink: /archives/23884247/
tags: 
 - git
---



以提交的一次开源代码为例，教会你步入开源的世界。


1,首先登陆到[https://github.com](https://github.com/)平台上注册一个自己的账号，这个过程就不演示了


2，然后在左上部分输入一个开源项目的名字,选择的是jvalidator,回车搜索。


<img alt="手把手教你如何加入到github的开源世界！" src="http://static.open-open.com/lib/uploadImg/20140404/20140404105552_308.png" width="363" height="47" style="padding:0px; margin:0px; border:0px">


3,在搜索结果页面找到如下如图所示的项目，单击项目名称。


<img alt="手把手教你如何加入到github的开源世界！" src="http://static.open-open.com/lib/uploadImg/20140404/20140404105552_11.png" width="783" height="116" style="padding:0px; margin:0px; border:0px">


4,此时，你已经进入到了rinh/jvalidator的项目主页了，单击右上角的fork按钮，就把这个项目拉到你的账户下了，你就可以加入到这个项目中了


<img alt="手把手教你如何加入到github的开源世界！" src="http://static.open-open.com/lib/uploadImg/20140404/20140404105552_814.png" width="384" height="148" style="padding:0px; margin:0px; border:0px">


5，此时，页面已经跳转到你的账户下的jvalidator项目里了，单击右下方的复制按钮，将这个地址就复制下来了，稍后有用<br style="padding:0px; margin:0px; line-height:10px">



<img alt="手把手教你如何加入到github的开源世界！" src="http://static.open-open.com/lib/uploadImg/20140404/20140404105553_714.png" width="249" height="219" style="padding:0px; margin:0px; border:0px">


6，此时，你需要安装一个git的客户端工具，当然这就很多了，我们演示就用它了[http://msysgit.github.io](http://msysgit.github.io/)，到这个页面下载此工具,选择一个最新的版本吧，下载到你的电脑里，然后安装它。


<img alt="手把手教你如何加入到github的开源世界！" src="http://static.open-open.com/lib/uploadImg/20140404/20140404105553_655.png" width="727" height="289" style="padding:0px; margin:0px; border:0px">


7，接着，你在你的磁盘里的一个合适位置建立一个目录，专门用来存放开源代码，比如我在我的D盘下建立了一个git文件夹，进入git文件夹


<img alt="手把手教你如何加入到github的开源世界！" src="http://static.open-open.com/lib/uploadImg/20140404/20140404105553_702.png" width="607" height="281" style="padding:0px; margin:0px; border:0px">


8，单击你的鼠标右键，会出现一个Git Bash 命令选项，单击进入。此时你看到的是一个命名窗口


<img alt="手把手教你如何加入到github的开源世界！" src="http://static.open-open.com/lib/uploadImg/20140404/20140404105553_756.png" width="696" height="241" style="padding:0px; margin:0px; border:0px">


9，直接输入命令 git &nbsp;clone &nbsp;接着将起先的地址复制到后面，回车，就开始将你的github上的jvalidator的源码下载到你的电脑里了


<img alt="手把手教你如何加入到github的开源世界！" src="http://static.open-open.com/lib/uploadImg/20140404/20140404105554_635.png" width="544" height="188" style="padding:0px; margin:0px; border:0px">


10，此时，就可以去开发里面的代码了，添加新的功能，修改明显的bug......这里就是你在参与开源开发了


11，通过10后，保存好文件，回到我们的git bash命令界面，输入命令


cd &nbsp;jvalidator &nbsp;//进入到这个文件夹


git add . &nbsp; &nbsp;//将改动的地方添加到版本管理器


git &nbsp;commit -m &quot;some changes&quot; &nbsp;//提交到本地的版本控制库里，引号里面是你对本次提交的说明信息


git push -u origin master &nbsp;//将你本地的仓库提交到你的github账号里，此时需要你输入你的github的账号和密码，你输入就是了


<img alt="手把手教你如何加入到github的开源世界！" src="http://static.open-open.com/lib/uploadImg/20140404/20140404105554_656.png" width="653" height="439" style="padding:0px; margin:0px; border:0px">


12，此时你在你的本的任务就完成了，进入到你的github上面，选择到这个jvalidator项目名，单击进入，右侧有个pull request，单击


<img alt="手把手教你如何加入到github的开源世界！" src="http://static.open-open.com/lib/uploadImg/20140404/20140404105554_881.png" width="315" height="261" style="padding:0px; margin:0px; border:0px">


13，进入跳转的页面单击右侧的New pull Request按钮


<img alt="手把手教你如何加入到github的开源世界！" src="http://static.open-open.com/lib/uploadImg/20140404/20140404105554_404.png" width="294" height="168" style="padding:0px; margin:0px; border:0px">


14，此时，你就能看到你改动的方了，核对下，没有问题后，就单击View pull request按钮


<img alt="手把手教你如何加入到github的开源世界！" src="http://static.open-open.com/lib/uploadImg/20140404/20140404105555_53.png" width="290" height="124" style="padding:0px; margin:0px; border:0px">


&nbsp;


15，此时，你可以在页面中输入你的本次提交的说明信息，输入完后，单击提交按钮 comment


<img alt="手把手教你如何加入到github的开源世界！" src="http://static.open-open.com/lib/uploadImg/20140404/20140404105555_357.png" width="810" height="249" style="padding:0px; margin:0px; border:0px">


16,到此，你的任务就完成了，等到开源项目的管理人员审核，通过了，他就把你的改动合并到相应的开发分支上。


<br style="padding:0px; margin:0px; line-height:10px">
来自：http://www.cnblogs.com/wenber/p/3630921.html
