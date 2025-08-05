# 智能问答 API

## 概述

智能问答模块提供基于 AI 的医疗知识问答功能，支持多轮对话、知识库检索、会话管理等功能。

**基础路径**: `/api/chat`

## 接口列表

### 1. 获取聊天会话列表

#### 1.1 基本信息

> 请求路径：`/api/chat/sessions`
>
> 请求方式：`GET`
>
> 接口描述：获取用户的聊天会话列表

#### 1.2 请求参数

参数格式：`Query String`

参数说明：

| 参数名   | 类型   | 是否必须 | 备注              |
| -------- | ------ | -------- | ----------------- |
| page     | number | 可选     | 页码，默认 1      |
| pageSize | number | 可选     | 每页数量，默认 10 |
| search   | string | 可选     | 搜索关键词        |

#### 1.3 响应数据

响应示例：

```json
{
  "code": 200,
  "message": "Chat sessions retrieved successfully",
  "data": {
    "total": 25,
    "page": 1,
    "pageSize": 10,
    "sessions": [
      {
        "sessionId": "chat_session_123456",
        "title": "高血压相关咨询",
        "lastMessage": "谢谢您的详细解答",
        "messageCount": 12,
        "createdAt": "2024-01-01T10:00:00Z",
        "updatedAt": "2024-01-01T10:30:00Z"
      }
    ]
  }
}
```

### 2. 创建聊天会话

#### 2.1 基本信息

> 请求路径：`/api/chat/sessions`
>
> 请求方式：`POST`
>
> 接口描述：创建新的聊天会话

#### 2.2 请求参数

参数格式：`application/json`

参数说明：

| 参数名 | 类型   | 是否必须 | 备注               |
| ------ | ------ | -------- | ------------------ |
| title  | string | 可选     | 会话标题           |
| mode   | string | 可选     | 对话模式：kb/graph |

请求示例：

```json
{
  "title": "糖尿病饮食咨询",
  "mode": "kb"
}
```

#### 2.3 响应数据

响应示例：

```json
{
  "code": 201,
  "message": "Chat session created successfully",
  "data": {
    "sessionId": "chat_session_789012",
    "title": "糖尿病饮食咨询",
    "mode": "kb",
    "createdAt": "2024-01-01T11:00:00Z"
  }
}
```

### 3. 发送消息

#### 3.1 基本信息

> 请求路径：`/api/chat/sessions/{sessionId}/messages`
>
> 请求方式：`POST`
>
> 接口描述：在指定会话中发送消息并获取 AI 回复

#### 3.2 请求参数

路径参数：

| 参数名    | 类型   | 是否必须 | 备注    |
| --------- | ------ | -------- | ------- |
| sessionId | string | 必须     | 会话 ID |

请求体参数：

| 参数名      | 类型   | 是否必须 | 备注                       |
| ----------- | ------ | -------- | -------------------------- |
| message     | string | 必须     | 用户消息内容               |
| messageType | string | 可选     | 消息类型：text/image/voice |
| context     | object | 可选     | 上下文信息                 |

请求示例：

```json
{
  "message": "糖尿病患者应该如何控制饮食？",
  "messageType": "text",
  "context": {
    "patientAge": 45,
    "diabetesType": "type2"
  }
}
```

#### 3.3 响应数据

响应示例：

```json
{
  "code": 200,
  "message": "Message sent successfully",
  "data": {
    "messageId": "msg_123456",
    "userMessage": {
      "id": "msg_123456",
      "content": "糖尿病患者应该如何控制饮食？",
      "type": "text",
      "timestamp": "2024-01-01T11:05:00Z"
    },
    "aiResponse": {
      "id": "msg_123457",
      "content": "糖尿病患者的饮食控制非常重要，以下是一些建议：\n\n1. **控制总热量**：根据身高、体重、活动量确定每日所需热量\n2. **合理分配三大营养素**：\n   - 碳水化合物：50-60%\n   - 蛋白质：15-20%\n   - 脂肪：20-30%\n3. **选择低升糖指数食物**：如全谷物、蔬菜、豆类\n4. **定时定量**：规律进餐，避免暴饮暴食",
      "type": "text",
      "timestamp": "2024-01-01T11:05:30Z",
      "references": [
        {
          "id": "ref_001",
          "title": "糖尿病饮食指南",
          "source": "中华医学会糖尿病学分会",
          "url": "/knowledge/diabetes-diet-guide"
        }
      ],
      "relatedQuestions": [
        "糖尿病患者可以吃水果吗？",
        "如何计算食物的升糖指数？",
        "糖尿病患者运动前后如何调整饮食？"
      ]
    }
  }
}
```

### 4. 获取会话消息历史

#### 4.1 基本信息

> 请求路径：`/api/chat/sessions/{sessionId}/messages`
>
> 请求方式：`GET`
>
> 接口描述：获取指定会话的消息历史

#### 4.2 请求参数

路径参数：

| 参数名    | 类型   | 是否必须 | 备注    |
| --------- | ------ | -------- | ------- |
| sessionId | string | 必须     | 会话 ID |

查询参数：

| 参数名   | 类型   | 是否必须 | 备注                   |
| -------- | ------ | -------- | ---------------------- |
| page     | number | 可选     | 页码，默认 1           |
| pageSize | number | 可选     | 每页数量，默认 20      |
| before   | string | 可选     | 获取指定时间之前的消息 |

#### 4.3 响应数据

响应示例：

```json
{
  "code": 200,
  "message": "Messages retrieved successfully",
  "data": {
    "sessionId": "chat_session_123456",
    "total": 24,
    "page": 1,
    "pageSize": 20,
    "messages": [
      {
        "id": "msg_123456",
        "role": "user",
        "content": "糖尿病患者应该如何控制饮食？",
        "type": "text",
        "timestamp": "2024-01-01T11:05:00Z"
      },
      {
        "id": "msg_123457",
        "role": "assistant",
        "content": "糖尿病患者的饮食控制非常重要...",
        "type": "text",
        "timestamp": "2024-01-01T11:05:30Z",
        "references": [
          {
            "id": "ref_001",
            "title": "糖尿病饮食指南",
            "source": "中华医学会糖尿病学分会"
          }
        ]
      }
    ]
  }
}
```

### 5. 删除聊天会话

#### 5.1 基本信息

> 请求路径：`/api/chat/sessions/{sessionId}`
>
> 请求方式：`DELETE`
>
> 接口描述：删除指定的聊天会话

#### 5.2 请求参数

路径参数：

| 参数名    | 类型   | 是否必须 | 备注    |
| --------- | ------ | -------- | ------- |
| sessionId | string | 必须     | 会话 ID |

#### 5.3 响应数据

响应示例：

```json
{
  "code": 200,
  "message": "Chat session deleted successfully",
  "data": null
}
```

### 6. 获取推荐问题

#### 6.1 基本信息

> 请求路径：`/api/chat/suggestions`
>
> 请求方式：`GET`
>
> 接口描述：获取推荐的常见问题

#### 6.2 请求参数

参数格式：`Query String`

参数说明：

| 参数名   | 类型   | 是否必须 | 备注                                |
| -------- | ------ | -------- | ----------------------------------- |
| category | string | 可选     | 问题分类：general/emergency/disease |
| limit    | number | 可选     | 返回数量，默认 10                   |

#### 6.3 响应数据

响应示例：

```json
{
  "code": 200,
  "message": "Suggestions retrieved successfully",
  "data": {
    "categories": [
      {
        "id": "general",
        "name": "常见问题",
        "questions": ["如何预防感冒？", "正常血压范围是多少？", "如何保持健康的生活方式？"]
      },
      {
        "id": "emergency",
        "name": "急救知识",
        "questions": ["心脏骤停如何急救？", "外伤出血如何处理？", "中暑了应该怎么办？"]
      },
      {
        "id": "disease",
        "name": "疾病咨询",
        "questions": ["糖尿病有哪些症状？", "高血压如何控制？", "如何预防心血管疾病？"]
      }
    ]
  }
}
```

## 对话模式说明

| 模式  | 名称       | 描述                         |
| ----- | ---------- | ---------------------------- |
| kb    | 知识库模式 | 基于医疗知识库的问答         |
| graph | 图谱模式   | 基于医疗知识图谱的结构化问答 |

## 使用示例

### JavaScript/TypeScript

```typescript
// 创建聊天会话
const createChatSession = async (title: string, mode: string = 'kb') => {
  const response = await fetch('/api/chat/sessions', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ title, mode }),
  })
  return response.json()
}

// 发送消息
const sendMessage = async (sessionId: string, message: string) => {
  const response = await fetch(`/api/chat/sessions/${sessionId}/messages`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message, messageType: 'text' }),
  })
  return response.json()
}

// 获取会话列表
const getChatSessions = async (page: number = 1) => {
  const response = await fetch(`/api/chat/sessions?page=${page}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  return response.json()
}

// 获取推荐问题
const getSuggestions = async (category: string = 'general') => {
  const response = await fetch(`/api/chat/suggestions?category=${category}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  return response.json()
}
```

### Python

```python
import requests

def create_chat_session(title, mode='kb', token=None):
    """创建聊天会话"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    data = {'title': title, 'mode': mode}

    response = requests.post(
        'http://localhost:8000/api/chat/sessions',
        json=data,
        headers=headers
    )
    return response.json()

def send_message(session_id, message, token):
    """发送消息"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    data = {
        'message': message,
        'messageType': 'text'
    }

    response = requests.post(
        f'http://localhost:8000/api/chat/sessions/{session_id}/messages',
        json=data,
        headers=headers
    )
    return response.json()

def get_chat_sessions(token, page=1, page_size=10):
    """获取聊天会话列表"""
    headers = {'Authorization': f'Bearer {token}'}
    params = {'page': page, 'pageSize': page_size}

    response = requests.get(
        'http://localhost:8000/api/chat/sessions',
        params=params,
        headers=headers
    )
    return response.json()

def get_suggestions(token, category='general', limit=10):
    """获取推荐问题"""
    headers = {'Authorization': f'Bearer {token}'}
    params = {'category': category, 'limit': limit}

    response = requests.get(
        'http://localhost:8000/api/chat/suggestions',
        params=params,
        headers=headers
    )
    return response.json()
```

## 注意事项

1. **会话管理**：建议定期清理长时间未使用的会话
2. **消息长度**：单条消息建议不超过 2000 字符
3. **频率限制**：为防止滥用，API 可能有频率限制
4. **上下文保持**：系统会自动维护会话上下文，无需重复发送历史消息
5. **知识更新**：AI 回答基于训练数据，可能不包含最新的医疗信息
6. **专业建议**：AI 回答仅供参考，重要医疗决策请咨询专业医生
