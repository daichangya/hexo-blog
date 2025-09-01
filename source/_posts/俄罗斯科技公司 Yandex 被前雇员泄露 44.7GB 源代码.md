---
title: 俄罗斯科技公司 Yandex 被前雇员泄露 44.7GB 源代码
id: 1592
date: 2024-10-31 22:02:02
author: daichangya
permalink: /archives/%E4%BF%84%E7%BD%97%E6%96%AF%E7%A7%91%E6%8A%80%E5%85%AC%E5%8F%B8yandex%E8%A2%AB%E5%89%8D%E9%9B%87%E5%91%98%E6%B3%84%E9%9C%B2447gb%E6%BA%90%E4%BB%A3%E7%A0%81/
categories:
 - 其他
---


俄罗斯科技公司 Yandex 前雇员近日在一个流行的黑客论坛上以 Torrent 磁链的形式**[发布](https://breached.vc/Thread-yandex-git-sources)**了总容量为 44.7GB 的源代码仓库。

![Yandex.png](https://images.jsdiff.com/Yandex_1675048762885.png)

泄露者称这是 'Yandex git sources'，于 2022 年 7 月从公司窃取，包含了除反垃圾邮件规则之外的所有源代码。

软件工程师 Arseniy Shestakov 在[分析](http://arseniyshestakov.com/2023/01/26/yandex-services-source-code-leak/)泄露的 Yandex Git 仓库后，发现其中包含以下产品的技术数据和代码：

*   Yandex 搜索引擎和索引机器人
*   Yandex 地图
*   Alice（人工智能助理）
*   Yandex Taxi
*   Yandex Direct（广告服务）
*   Yandex 邮件
*   Yandex Disk（云存储服务）
*   Yandex Market
*   Yandex Travel（旅游预订平台）
*   Yandex360（Workspace 服务）
*   Yandex Cloud
*   Yandex Pay（支付处理服务）
*   Yandex Metrika（互联网分析）

泄露文件的目录：[http://gist.github.com/ArseniyShestakov/53a80e3214601aa20d1075872a1ea989](http://gist.github.com/ArseniyShestakov/53a80e3214601aa20d1075872a1ea989)

Yandex 在回应媒体的声明中[表示](https://www.bleepingcomputer.com/news/security/yandex-denies-hack-blames-source-code-leak-on-former-employee/)，他们的系统没有被黑客入侵，一名前雇员泄露了源代码仓库。目前没有发现对用户数据或平台性能造成任何威胁。

不过安全研究人员表示，此次 Yandex 被泄露的代码使黑客有可能识别出安全漏洞，并创建有针对性的漏洞利用，这只是时间问题。