---
title: OpenAI接口说明（其他）
id: 5ce09032-f1bb-4c21-abae-35e646592a9f
date: 2025-02-16 08:41:32
author: daichangya
excerpt: 除了 Chat Completions API，OpenAI 还提供了其他接口，例如 生成文本（Completions）、生成图片（DALL·E）、语音转录（Whisper）、Embeddings
  等。以下是常用接口的说明及 curl 请求示例： 1. Text Completions（旧版文本生成
permalink: /archives/OpenAI-jie-kou-shuo-ming-qi-ta/
categories:
- 大模型
---

除了 **Chat Completions API**，OpenAI 还提供了其他接口，例如 **生成文本（Completions）**、**生成图片（DALL·E）**、**语音转录（Whisper）**、**Embeddings** 等。以下是常用接口的说明及 `curl` 请求示例：

---

### **1. Text Completions（旧版文本生成）**
用于生成单轮文本（如 GPT-3 模型）。  
**接口地址**: `POST https://api.openai.com/v1/completions`

#### **参数示例**  
```bash
curl https://api.openai.com/v1/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "text-davinci-003",
    "prompt": "写一首关于秋天的诗：",
    "temperature": 0.7,
    "max_tokens": 100
  }'
```

#### **响应示例**  
```json
{
  "id": "cmpl-xxx",
  "choices": [
    {
      "text": "秋风轻拂叶纷飞，金黄满地映斜晖...",
      "index": 0
    }
  ]
}
```

---

### **2. Image Generation（生成图片，DALL·E）**
生成或编辑图片，支持通过文本描述创建图像。  
**接口地址**: `POST https://api.openai.com/v1/images/generations`

#### **参数示例**  
```bash
curl https://api.openai.com/v1/images/generations \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "一只戴着墨镜的柯基犬在海滩上冲浪",
    "n": 1,          // 生成图片数量
    "size": "1024x1024", // 图片尺寸（256x256, 512x512, 1024x1024）
    "response_format": "url" // 返回格式（url 或 b64_json）
  }'
```

#### **响应示例**  
```json
{
  "data": [
    {
      "url": "https://example.com/image.png"
    }
  ]
}
```

---

### **3. Audio Transcription（语音转文本，Whisper）**
将音频文件转录为文本，支持多语言。  
**接口地址**: `POST https://api.openai.com/v1/audio/transcriptions`

#### **参数示例**  
```bash
curl https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file="@audio.mp3" \
  -F model="whisper-1" \
  -F response_format="text"
```

#### **响应示例**  
```text
今天天气很好，适合去公园散步。
```

---

### **4. Embeddings（文本向量化）**
将文本转换为高维向量，用于语义分析、搜索等场景。  
**接口地址**: `POST https://api.openai.com/v1/embeddings`

#### **参数示例**  
```bash
curl https://api.openai.com/v1/embeddings \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "text-embedding-ada-002",
    "input": "机器学习是什么？"
  }'
```

#### **响应示例**  
```json
{
  "data": [
    {
      "embedding": [0.1, -0.2, 0.3, ...], // 1536 维向量（ada-002）
      "index": 0
    }
  ]
}
```

---

### **5. Moderations（内容审核）**
检测文本是否包含敏感或违规内容。  
**接口地址**: `POST https://api.openai.com/v1/moderations`

#### **参数示例**  
```bash
curl https://api.openai.com/v1/moderations \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "这段话包含暴力内容吗？"
  }'
```

#### **响应示例**  
```json
{
  "results": [
    {
      "flagged": false,
      "categories": {
        "violence": false,
        "hate": false
      }
    }
  ]
}
```

---

### **6. Fine-tuning（模型微调）**
基于自定义数据微调模型（需先上传训练文件）。  
**接口地址**: `POST https://api.openai.com/v1/fine_tuning/jobs`

#### **步骤示例**  
1. **上传文件**：
   ```bash
   curl https://api.openai.com/v1/files \
     -H "Authorization: Bearer $OPENAI_API_KEY" \
     -F purpose="fine-tune" \
     -F file="@data.jsonl"
   ```

2. **创建微调任务**：
   ```bash
   curl https://api.openai.com/v1/fine_tuning/jobs \
     -H "Authorization: Bearer $OPENAI_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "training_file": "file-xxx",
       "model": "gpt-3.5-turbo"
     }'
   ```

---

### **7. Files（文件管理）**
管理上传到 OpenAI 的文件（如微调数据）。  
**接口地址**: `GET https://api.openai.com/v1/files`

#### **示例：列出所有文件**  
```bash
curl https://api.openai.com/v1/files \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

---

### **注意事项**
1. **API 密钥**：所有请求需在 Header 中传递 `Authorization: Bearer $OPENAI_API_KEY`。
2. **费用**：不同接口的计费方式不同，需参考 [OpenAI 定价页](https://openai.com/pricing)。
3. **模型支持**：部分接口仅限特定模型（如 Whisper 仅支持 `whisper-1`）。
4. **流式响应**：若需流式传输（如逐字输出），可添加 `"stream": true` 参数。

建议结合 [OpenAI 官方文档](https://platform.openai.com/docs/api-reference) 使用最新接口！