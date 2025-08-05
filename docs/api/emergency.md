# 应急指导 API

## 概述

应急指导模块提供紧急情况处理指导、医疗设备定位、急救操作指南等功能，帮助用户在紧急情况下快速获得专业指导。

**基础路径**: `/api/emergency`

## 接口列表

### 1. 获取应急场景

#### 1.1 基本信息

> 请求路径：`/api/emergency/scenarios`
>
> 请求方式：`GET`
>
> 接口描述：获取所有可用的应急场景类型

#### 1.2 请求参数

无需参数

#### 1.3 响应数据

响应示例：

```json
{
  "code": 200,
  "message": "Emergency scenarios retrieved successfully",
  "data": [
    {
      "id": "equipment",
      "title": "常用医疗设备操作",
      "description": "AED、血压计等医疗设备使用指导",
      "icon": "fas fa-medkit",
      "category": "guidance"
    },
    {
      "id": "firstAid",
      "title": "紧急救护步骤",
      "description": "心肺复苏、止血等急救操作指导",
      "icon": "fas fa-heartbeat",
      "category": "critical"
    },
    {
      "id": "location",
      "title": "医疗设备定位",
      "description": "查找最近的AED、医疗设备位置",
      "icon": "fas fa-map-marker-alt",
      "category": "guidance"
    },
    {
      "id": "emergency",
      "title": "现场应急处置",
      "description": "快速描述现场情况，获取应急处置建议",
      "icon": "fas fa-ambulance",
      "category": "urgent"
    }
  ]
}
```

### 2. 创建应急会话

#### 2.1 基本信息

> 请求路径：`/api/emergency/sessions`
>
> 请求方式：`POST`
>
> 接口描述：创建新的应急指导会话

#### 2.2 请求参数

参数格式：`application/json`

参数说明：

| 参数名        | 类型   | 是否必须 | 备注        |
| ------------- | ------ | -------- | ----------- |
| scenarioId    | string | 必须     | 应急场景 ID |
| title         | string | 可选     | 会话标题    |
| description   | string | 可选     | 情况描述    |
| location      | object | 可选     | 位置信息    |
| \|- latitude  | number | 可选     | 纬度        |
| \|- longitude | number | 可选     | 经度        |
| \|- address   | string | 可选     | 地址描述    |

请求示例：

```json
{
  "scenarioId": "firstAid",
  "title": "心脏骤停急救",
  "description": "患者突然倒地，无意识无呼吸",
  "location": {
    "latitude": 39.9042,
    "longitude": 116.4074,
    "address": "北京市朝阳区某医院"
  }
}
```

#### 2.3 响应数据

响应示例：

```json
{
  "code": 201,
  "message": "Emergency session created successfully",
  "data": {
    "sessionId": "emergency_session_123456",
    "scenarioId": "firstAid",
    "title": "心脏骤停急救",
    "status": "active",
    "createdAt": "2024-01-01T12:00:00Z"
  }
}
```

### 3. 发送应急消息

#### 3.1 基本信息

> 请求路径：`/api/emergency/sessions/{sessionId}/messages`
>
> 请求方式：`POST`
>
> 接口描述：在应急会话中发送消息，获取 AI 指导

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
| urgency     | string | 可选     | 紧急程度：low/medium/high  |

请求示例：

```json
{
  "message": "患者已经没有呼吸和脉搏，我应该怎么办？",
  "messageType": "text",
  "urgency": "high"
}
```

#### 3.3 响应数据

响应示例：

```json
{
  "code": 200,
  "message": "Emergency guidance provided successfully",
  "data": {
    "messageId": "msg_123456",
    "response": {
      "content": "立即开始心肺复苏（CPR）：\n1. 确保现场安全\n2. 检查患者反应\n3. 呼叫急救电话120\n4. 开始胸外按压",
      "steps": [
        {
          "step": 1,
          "title": "确保现场安全",
          "description": "检查周围环境，确保施救者和患者安全",
          "duration": "10秒"
        },
        {
          "step": 2,
          "title": "检查患者反应",
          "description": "轻拍患者肩膀，大声呼叫'你还好吗？'",
          "duration": "5秒"
        },
        {
          "step": 3,
          "title": "呼叫急救",
          "description": "立即拨打120急救电话，说明情况和位置",
          "duration": "30秒"
        },
        {
          "step": 4,
          "title": "开始胸外按压",
          "description": "双手重叠，掌根放在胸骨下半部，用力快速按压",
          "duration": "持续进行"
        }
      ],
      "urgencyLevel": "critical",
      "nextActions": ["继续CPR直到急救人员到达", "如有AED设备，立即使用", "记录按压时间和次数"]
    },
    "timestamp": "2024-01-01T12:01:00Z"
  }
}
```

### 4. 获取设备位置

#### 4.1 基本信息

> 请求路径：`/api/emergency/equipment/nearby`
>
> 请求方式：`GET`
>
> 接口描述：获取附近的医疗设备位置信息

#### 4.2 请求参数

参数格式：`Query String`

参数说明：

| 参数名    | 类型   | 是否必须 | 备注                            |
| --------- | ------ | -------- | ------------------------------- |
| latitude  | number | 必须     | 当前位置纬度                    |
| longitude | number | 必须     | 当前位置经度                    |
| radius    | number | 可选     | 搜索半径（米），默认 1000       |
| type      | string | 可选     | 设备类型：aed/defibrillator/all |

请求示例：

```
/api/emergency/equipment/nearby?latitude=39.9042&longitude=116.4074&radius=500&type=aed
```

#### 4.3 响应数据

响应示例：

```json
{
  "code": 200,
  "message": "Nearby equipment retrieved successfully",
  "data": {
    "userLocation": {
      "latitude": 39.9042,
      "longitude": 116.4074
    },
    "equipment": [
      {
        "id": "aed_001",
        "name": "AED设备 - 大厅",
        "type": "aed",
        "location": {
          "name": "医院大厅一楼",
          "latitude": 39.9045,
          "longitude": 116.407,
          "distance": 45.2
        },
        "status": "available",
        "description": "位于医院主入口大厅，24小时可用",
        "instructions": "设备位于信息台旁边的红色急救箱内"
      },
      {
        "id": "aed_002",
        "name": "AED设备 - 急诊科",
        "type": "aed",
        "location": {
          "name": "急诊科护士站",
          "latitude": 39.904,
          "longitude": 116.4078,
          "distance": 78.5
        },
        "status": "available",
        "description": "急诊科护士站旁，医护人员协助使用"
      }
    ]
  }
}
```

### 5. 获取会话历史

#### 5.1 基本信息

> 请求路径：`/api/emergency/sessions`
>
> 请求方式：`GET`
>
> 接口描述：获取用户的应急会话历史

#### 5.2 请求参数

参数格式：`Query String`

参数说明：

| 参数名   | 类型   | 是否必须 | 备注                    |
| -------- | ------ | -------- | ----------------------- |
| page     | number | 可选     | 页码，默认 1            |
| pageSize | number | 可选     | 每页数量，默认 10       |
| scenario | string | 可选     | 场景类型过滤            |
| status   | string | 可选     | 会话状态：active/closed |

#### 5.3 响应数据

响应示例：

```json
{
  "code": 200,
  "message": "Emergency sessions retrieved successfully",
  "data": {
    "total": 15,
    "page": 1,
    "pageSize": 10,
    "sessions": [
      {
        "sessionId": "emergency_session_123456",
        "scenarioId": "firstAid",
        "title": "心脏骤停急救",
        "status": "closed",
        "messageCount": 8,
        "createdAt": "2024-01-01T12:00:00Z",
        "updatedAt": "2024-01-01T12:15:00Z"
      }
    ]
  }
}
```

## 应急场景类型

| 场景 ID   | 名称         | 描述                  | 紧急程度 |
| --------- | ------------ | --------------------- | -------- |
| equipment | 医疗设备操作 | AED、血压计等设备使用 | 中等     |
| firstAid  | 紧急救护     | CPR、止血等急救操作   | 高       |
| location  | 设备定位     | 查找附近医疗设备      | 低       |
| emergency | 现场应急处置 | 综合性紧急情况处理    | 高       |

## 使用示例

### JavaScript/TypeScript

```typescript
// 创建应急会话
const createEmergencySession = async (sessionData: EmergencySessionData) => {
  const response = await fetch('/api/emergency/sessions', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(sessionData),
  })
  return response.json()
}

// 发送应急消息
const sendEmergencyMessage = async (sessionId: string, message: string) => {
  const response = await fetch(`/api/emergency/sessions/${sessionId}/messages`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message, urgency: 'high' }),
  })
  return response.json()
}

// 获取附近设备
const getNearbyEquipment = async (lat: number, lng: number) => {
  const response = await fetch(
    `/api/emergency/equipment/nearby?latitude=${lat}&longitude=${lng}&type=aed`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  )
  return response.json()
}
```

### Python

```python
import requests

def create_emergency_session(session_data, token):
    """创建应急会话"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(
        'http://localhost:8000/api/emergency/sessions',
        json=session_data,
        headers=headers
    )
    return response.json()

def send_emergency_message(session_id, message, token):
    """发送应急消息"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    data = {
        'message': message,
        'urgency': 'high'
    }

    response = requests.post(
        f'http://localhost:8000/api/emergency/sessions/{session_id}/messages',
        json=data,
        headers=headers
    )
    return response.json()

def get_nearby_equipment(latitude, longitude, token, radius=1000):
    """获取附近设备"""
    headers = {'Authorization': f'Bearer {token}'}
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'radius': radius,
        'type': 'aed'
    }

    response = requests.get(
        'http://localhost:8000/api/emergency/equipment/nearby',
        params=params,
        headers=headers
    )
    return response.json()
```

## 注意事项

1. **紧急情况优先**：在真正的紧急情况下，应首先拨打急救电话（120）
2. **设备可用性**：设备位置信息仅供参考，实际使用前请确认设备状态
3. **专业指导**：AI 提供的指导仅供参考，不能替代专业医疗人员的判断
4. **位置隐私**：位置信息仅用于提供附近设备信息，不会被存储或共享
5. **网络依赖**：确保网络连接稳定，以便及时获取指导信息
