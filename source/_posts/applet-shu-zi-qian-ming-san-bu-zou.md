---
title: applet 数字签名——三步走
id: 1141
date: 2024-10-31 22:01:49
author: daichangya
excerpt: keytool -genkey -keystore capture.store -alias capturekeytool -export -keystore
  capture.store -alias capture -file capture.cerjarsigner -keystore capture.store  capture.jar
  capture
permalink: /archives/applet-shu-zi-qian-ming-san-bu-zou/
categories:
- java
---


keytool -genkey -keystore capture.store -alias capture<br />keytool -export -keystore capture.store -alias capture -file capture.cer<br />jarsigner -keystore capture.store&nbsp; capture.jar capture
