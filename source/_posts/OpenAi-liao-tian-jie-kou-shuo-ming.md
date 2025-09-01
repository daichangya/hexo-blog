---
title: OpenAi 聊天接口说明
id: c8c24903-47ba-4b0f-a68a-d6743d61291b
date: 2025-02-16 08:20:23
author: daichangya
excerpt: 以下以OpenAI中最常用的聊天完成接口（Chat Completions API）为例，为你提供详细的接口说明，包括请求（Request）和响应（Response）示例，以及字段说明：
  1. 接口基本信息 接口地址：https//api.openai.com/v1/chat/completion
permalink: /archives/OpenAi-liao-tian-jie-kou-shuo-ming/
categories:
- 大模型
---

以下以OpenAI中最常用的聊天完成接口（Chat Completions API）为例，为你提供详细的接口说明，包括请求（Request）和响应（Response）示例，以及字段说明：

### 1. 接口基本信息
- **接口地址**：`https://api.openai.com/v1/chat/completions`
- **请求方法**：`POST`
- **认证方式**：在请求头中设置`Authorization`字段，值为`Bearer YOUR_API_KEY`，`YOUR_API_KEY`是你在OpenAI平台获取的API密钥。

### 2. 请求（Request）示例
```python
import requests

url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}
data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {
            "role": "system",
            "content": "你是一个知识渊博的助手"
        },
        {
            "role": "user",
            "content": "请介绍一下人工智能的发展历史"
        }
    ],
    "temperature": 0.7,
    "max_tokens": 200
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```
上述Python代码中，使用`requests`库发送POST请求，`headers`中包含认证信息和内容类型，`data`字典中包含了请求的具体参数：
- **model**：指定使用的模型，这里是`gpt-3.5-turbo`。
- **messages**：是一个数组，记录对话历史。第一个元素是系统消息，设定助手的角色；第二个元素是用户消息，表明用户的提问。
- **temperature**：设置为0.7，生成的文本会有一定的随机性。
- **max_tokens**：限制生成文本的最大令牌数为200。

### 3. 请求字段说明
| 字段名 | 类型 | 是否必填 | 描述 |
| ---- | ---- | ---- | ---- |
| model | 字符串 | 是 | 要使用的模型名称，如`gpt-3.5-turbo`、`gpt-4`等 |
| messages | 数组 | 是 | 对话消息数组，每个元素是一个包含`role`（`system`、`user`、`assistant`）和`content`的对象 |
| temperature | 浮点数 | 否 | 控制生成文本的随机性，取值范围0 - 2，默认1 |
| max_tokens | 整数 | 否 | 生成文本的最大令牌数，默认值由模型决定 |
| top_p | 浮点数 | 否 | 另一种控制生成文本多样性的方式，与`temperature`类似，取值范围0 - 1，默认1 |
| n | 整数 | 否 | 生成的回复数量，默认1 |
| stop | 字符串或数组 | 否 | 遇到指定的字符串或数组中的元素时，停止生成文本 |
| presence_penalty | 浮点数 | 否 | 控制新生成内容中引入新话题的惩罚系数，取值范围 -2.0 - 2.0，默认0 |
| frequency_penalty | 浮点数 | 否 | 控制新生成内容中重复内容的惩罚系数，取值范围 -2.0 - 2.0，默认0 |

### 4. 响应（Response）示例
```json
{
    "choices": [
        {
            "finish_reason": "stop",
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "人工智能的发展历史可以追溯到20世纪中叶。1956年，达特茅斯会议被广泛认为是人工智能诞生的标志，在这次会议上，“人工智能”这一术语正式被提出。此后，人工智能经历了多个发展阶段。在早期，研究主要集中在符号推理和专家系统方面。到了20世纪80年代，专家系统得到了广泛应用，但也暴露出一些局限性。随着计算机技术的不断发展，尤其是计算能力的大幅提升和数据的大量积累，机器学习逐渐成为人工智能的核心领域。特别是在21世纪初，深度学习的兴起，使得人工智能在图像识别、语音识别、自然语言处理等领域取得了突破性进展。如今，人工智能已经广泛应用于各个行业，如医疗、金融、交通等，对社会产生了深远的影响。"
            }
        }
    ],
    "created": 1695371246,
    "id": "chatcmpl-7O6x24y1G7V5c1234567890abcdef",
    "model": "gpt-3.5-turbo-0613",
    "object": "chat.completion",
    "usage": {
        "completion_tokens": 186,
        "prompt_tokens": 30,
        "total_tokens": 216
    }
}
```
### 5. 响应字段说明
| 字段名 | 类型 | 描述 |
| ---- | ---- | ---- |
| choices | 数组 | 包含生成的回复选项，通常只有一个元素，除非`n`参数设置大于1 |
| choices[].finish_reason | 字符串 | 表示生成结束的原因，常见值有`stop`（达到停止条件）、`length`（达到`max_tokens`限制）等 |
| choices[].index | 整数 | 回复在`choices`数组中的索引，通常为0 |
| choices[].message | 对象 | 包含生成的回复消息，`role`为`assistant`，`content`是具体的回复内容 |
| created | 整数 | 响应创建的时间戳（以秒为单位） |
| id | 字符串 | 此次请求的唯一标识符 |
| model | 字符串 | 实际使用的模型名称 |
| object | 字符串 | 固定值`chat.completion`，表示响应的对象类型 |
| usage | 对象 | 包含使用的令牌数量信息，`completion_tokens`是生成回复使用的令牌数，`prompt_tokens`是输入提示使用的令牌数，`total_tokens`是两者之和 | 