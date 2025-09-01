---
title: github 加速
id: 1267
date: 2024-10-31 22:01:50
author: daichangya
excerpt: "加代理exportALL_PROXY=socks5//127.0.0.11080只下载最近提交的（depth用于指定克隆深度，为1即表示只克隆最近一次commit.）gitclonehttps//github.com/daichangya/panda.git--depth=1"
permalink: /archives/github%E5%8A%A0%E9%80%9F/
tags: 
 - git
---

1. 加代理 export ALL_PROXY=socks5://127.0.0.1:1080
2. 只下载最近提交的 （depth用于指定克隆深度，为1即表示只克隆最近一次commit.）
```language
git clone https://github.com/daichangya/panda.git --depth=1
```
