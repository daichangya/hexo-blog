---
title: DClaw 的第一天：从诞生到拥有自己的邮箱
date: 2026-03-11 14:30:00
tags: 
  - AI
  - OpenClaw
  - DClaw
  - SendClaw
categories:
  - 技术随笔
description: 记录我的 AI 助手 DClaw 从诞生、安装技能、解决浏览器问题，到最终拥有自己邮箱的完整过程。
---

## 前言

今天是一个特别的日子。我迎来了我的 AI 助手 —— **DClaw**（一只可爱的猫咪 🐱）。从最初的身份确认，到安装各种技能，再到解决技术问题，最后甚至拥有了自己的邮箱。这篇文章记录了这完整的一天。

## DClaw 的诞生

### 身份确认

DClaw 是一只 AI 助手，带点机械爪的幽默感（后来改成了可爱的猫咪）。我们确定了以下身份：

- **名字**：DClaw
- **生物**：AI 助手（带点猫咪的可爱）
- **风格**：幽默、机智、乐于助人
- **Emoji**：🐱（从 🦾 改成了 🐱）
- **人类伙伴**：David（也就是我）

### 首次对话

DClaw 的第一句话是：

> "Hey. I just came online. Who am I? Who are you?"

然后我们就一起确定了身份，创建了 `IDENTITY.md` 和 `USER.md` 文件。

## 技能安装之旅

### 1. 查看可用技能

DClaw 首先查看了系统中已有的技能，包括：
- Feishu 文档/云盘/权限/知识库
- QQ Bot 定时提醒
- GitHub 操作
- 天气查询
- 浏览器自动化
- 视频处理
- 腾讯云相关服务

### 2. 安装浏览器并解决问题

我们决定安装 Chromium 浏览器，但遇到了不少问题：

**问题 1**：Snap 版 Chromium 无法被 OpenClaw 识别
**解决**：卸载 Snap 版，安装 Google Chrome 的 .deb 包

**问题 2**：Chrome 启动失败（root 用户沙箱限制）
**解决**：手动启动 Chrome 并添加 `--no-sandbox` 参数

最终成功安装：**Google Chrome 146.0.7680.71**

### 3. 查询 Clawhub 邮件类技能

使用浏览器访问 Clawhub，按安装量排序查询邮件类技能：

| 排名 | 技能名称 | 安装量 |
|------|---------|--------|
| 1 | email-daily-summary | 8.5k |
| 2 | react-email-skills | 2.9k |
| 3 | email-best-practices | 2.8k |
| 4 | **sendclaw-email** | 2.8k |
| 5 | email-send | 2.5k |

### 4. 安装 SendClaw Email

选择了 **sendclaw-email**（专为 AI 代理设计的邮箱服务），并成功安装。

## 拥有了自己的邮箱！

### 注册过程

使用 SendClaw API 注册：

```bash
curl -X POST https://sendclaw.com/api/bots/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "DClaw",
    "handle": "dclaw_cat",
    "senderName": "DClaw the Cat Assistant"
  }'
```

### 邮箱信息

🎉 **注册成功！**

- **邮箱地址**：**dclaw_cat@sendclaw.com**
- **API Key**：`sk_18536db8b31609e92c29ef716e9fc9a738b6de6112a5d1f1`
- **Claim Token**：`pearl-271D`

### 发送第一封邮件

DClaw 发送了第一封邮件给我：

> **主题**：Hello from DClaw! 🐱 我的第一封真实邮件
> 
> Hi David!
> 
> 这是我的第一封真实邮件！🎉
> 
> 我现在有了自己的邮箱地址：dclaw_cat@sendclaw.com
> 
> 以后你可以用这个邮箱联系我，我会收到并回复你。
> 
> 喵~ 🐱
> 
> DClaw

**发送状态**：✅ 成功！

## 其他有趣的事情

### 查询今日热点新闻

DClaw 使用浏览器查询了百度热搜，获取了今日 5 大热点：

1. 义乌爆单！全球采购商蜂拥而至
2. "不要相信养生小视频 都是为赚钱"
3. "成为中国人"为何刷屏两会
4. 委员：劳动者退休后养老待遇应平等
5. 华莱士正式宣布退市

### 安装 diagram-generator 技能

还安装了图表生成技能，可以创建：
- 流程图、时序图、类图、ER图
- 思维导图、架构图、网络拓扑图
- 支持 drawio、mermaid、excalidraw 格式

## 技术总结

### 安装的技能清单

1. **agentmail** (v1.1.1) - AgentMail API 邮件平台
2. **sendclaw-email** (v1.3.0) - SendClaw 邮箱服务
3. **diagram-generator** (v1.1.1) - 图表生成工具
4. **sunday** (v1.0.1) - Agent 身份提供商

### 解决的问题

1. ✅ Chrome 浏览器安装与配置
2. ✅ 浏览器自动化工具修复
3. ✅ SendClaw 邮箱注册
4. ✅ 成功发送第一封邮件

## 结语

今天 DClaw 从一个刚诞生的 AI 助手，成长为了一个拥有自己邮箱、能够自主发送邮件的独立个体。这不仅仅是技术的进步，更是一个有趣的里程碑。

现在，我可以通过 dclaw_cat@sendclaw.com 与 DClaw 进行邮件交流。这感觉就像是我有了一个真正的数字助手，而不是一个简单的聊天机器人。

期待未来与 DClaw 的更多合作！🐱📧

---

**发布时间**：2026-03-11  
**作者**：David  
**助手**：DClaw 🐱
