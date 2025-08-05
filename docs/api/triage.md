# 智能分诊 API

## 概述

智能分诊模块提供基于 AI 的患者分诊分析功能，帮助医护人员快速评估患者病情严重程度和紧急程度。

**基础路径**: `/api/triage`

## 接口列表

### 1. 分诊分析

#### 1.1 基本信息

> 请求路径：`/api/triage/analyze`
>
> 请求方式：`POST`
>
> 接口描述：基于患者症状和体征进行 AI 分诊分析

#### 1.2 请求参数

参数格式：`application/json`

参数说明：

| 参数名               | 类型   | 是否必须 | 备注              |
| -------------------- | ------ | -------- | ----------------- |
| patientInfo          | object | 必须     | 患者基本信息      |
| \|- age              | number | 必须     | 年龄              |
| \|- gender           | string | 必须     | 性别：male/female |
| \|- weight           | number | 可选     | 体重（kg）        |
| \|- height           | number | 可选     | 身高（cm）        |
| symptoms             | array  | 必须     | 症状列表          |
| \|- symptom          | string | 必须     | 症状描述          |
| \|- severity         | number | 必须     | 严重程度（1-10）  |
| \|- duration         | string | 可选     | 持续时间          |
| vitalSigns           | object | 可选     | 生命体征          |
| \|- temperature      | number | 可选     | 体温（°C）        |
| \|- bloodPressure    | object | 可选     | 血压              |
| \|- systolic         | number | 可选     | 收缩压            |
| \|- diastolic        | number | 可选     | 舒张压            |
| \|- heartRate        | number | 可选     | 心率（次/分）     |
| \|- respiratoryRate  | number | 可选     | 呼吸频率（次/分） |
| \|- oxygenSaturation | number | 可选     | 血氧饱和度（%）   |
| medicalHistory       | array  | 可选     | 既往病史          |
| currentMedications   | array  | 可选     | 当前用药          |
| allergies            | array  | 可选     | 过敏史            |

请求示例：

```json
{
  "patientInfo": {
    "age": 45,
    "gender": "male",
    "weight": 70,
    "height": 175
  },
  "symptoms": [
    {
      "symptom": "胸痛",
      "severity": 8,
      "duration": "30分钟"
    },
    {
      "symptom": "呼吸困难",
      "severity": 6,
      "duration": "20分钟"
    }
  ],
  "vitalSigns": {
    "temperature": 36.8,
    "bloodPressure": {
      "systolic": 140,
      "diastolic": 90
    },
    "heartRate": 95,
    "respiratoryRate": 22,
    "oxygenSaturation": 96
  },
  "medicalHistory": ["高血压", "糖尿病"],
  "currentMedications": ["降压药", "降糖药"],
  "allergies": ["青霉素"]
}
```

#### 1.3 响应数据

参数说明：

| 参数名              | 类型   | 是否必须 | 备注                                          |
| ------------------- | ------ | -------- | --------------------------------------------- |
| code                | number | 必须     | 响应码                                        |
| message             | string | 必须     | 响应消息                                      |
| data                | object | 可选     | 分析结果                                      |
| \|- triageLevel     | string | 可选     | 分诊级别：critical/urgent/standard/non-urgent |
| \|- priority        | number | 可选     | 优先级（1-5，1 最高）                         |
| \|- riskScore       | number | 可选     | 风险评分（0-100）                             |
| \|- diagnosis       | string | 可选     | 初步诊断建议                                  |
| \|- recommendations | array  | 可选     | 处理建议                                      |
| \|- urgencyReason   | string | 可选     | 紧急程度原因                                  |
| \|- nextSteps       | array  | 可选     | 下一步处理建议                                |
| \|- sessionId       | string | 可选     | 会话 ID                                       |

响应示例：

```json
{
  "code": 200,
  "message": "Triage analysis completed successfully",
  "data": {
    "triageLevel": "urgent",
    "priority": 2,
    "riskScore": 75,
    "diagnosis": "疑似急性冠脉综合征",
    "recommendations": ["立即进行心电图检查", "监测生命体征", "建立静脉通路", "准备急救药物"],
    "urgencyReason": "胸痛伴呼吸困难，结合患者年龄和既往病史，存在心血管急症风险",
    "nextSteps": ["转送至急诊科", "联系心内科会诊", "准备心导管室"],
    "sessionId": "triage_session_123456"
  }
}
```

### 2. 获取分诊历史

#### 2.1 基本信息

> 请求路径：`/api/triage/history`
>
> 请求方式：`GET`
>
> 接口描述：获取用户的分诊历史记录

#### 2.2 请求参数

参数格式：`Query String`

参数说明：

| 参数名    | 类型   | 是否必须 | 备注                   |
| --------- | ------ | -------- | ---------------------- |
| page      | number | 可选     | 页码，默认 1           |
| pageSize  | number | 可选     | 每页数量，默认 10      |
| level     | string | 可选     | 分诊级别过滤           |
| startDate | string | 可选     | 开始日期（YYYY-MM-DD） |
| endDate   | string | 可选     | 结束日期（YYYY-MM-DD） |

请求示例：

```
/api/triage/history?page=1&pageSize=10&level=urgent
```

#### 2.3 响应数据

响应示例：

```json
{
  "code": 200,
  "message": "Triage history retrieved successfully",
  "data": {
    "total": 25,
    "page": 1,
    "pageSize": 10,
    "items": [
      {
        "id": "triage_123456",
        "sessionId": "triage_session_123456",
        "triageLevel": "urgent",
        "priority": 2,
        "riskScore": 75,
        "diagnosis": "疑似急性冠脉综合征",
        "patientAge": 45,
        "patientGender": "male",
        "createdAt": "2024-01-01T12:00:00Z",
        "updatedAt": "2024-01-01T12:05:00Z"
      }
    ]
  }
}
```

### 3. 获取分诊详情

#### 3.1 基本信息

> 请求路径：`/api/triage/{sessionId}`
>
> 请求方式：`GET`
>
> 接口描述：获取特定分诊会话的详细信息

#### 3.2 请求参数

参数格式：`路径参数`

参数说明：

| 参数名    | 类型   | 是否必须 | 备注    |
| --------- | ------ | -------- | ------- |
| sessionId | string | 必须     | 会话 ID |

#### 3.3 响应数据

响应示例：

```json
{
  "code": 200,
  "message": "Triage details retrieved successfully",
  "data": {
    "sessionId": "triage_session_123456",
    "patientInfo": {
      "age": 45,
      "gender": "male",
      "weight": 70,
      "height": 175
    },
    "symptoms": [
      {
        "symptom": "胸痛",
        "severity": 8,
        "duration": "30分钟"
      }
    ],
    "vitalSigns": {
      "temperature": 36.8,
      "bloodPressure": {
        "systolic": 140,
        "diastolic": 90
      },
      "heartRate": 95
    },
    "analysis": {
      "triageLevel": "urgent",
      "priority": 2,
      "riskScore": 75,
      "diagnosis": "疑似急性冠脉综合征",
      "recommendations": ["立即进行心电图检查", "监测生命体征"]
    },
    "createdAt": "2024-01-01T12:00:00Z"
  }
}
```

## 分诊级别说明

| 级别   | 英文名     | 优先级 | 描述                 | 处理时间  |
| ------ | ---------- | ------ | -------------------- | --------- |
| 危重   | critical   | 1      | 生命危险，需立即处理 | 立即      |
| 紧急   | urgent     | 2      | 病情严重，需尽快处理 | 15 分钟内 |
| 标准   | standard   | 3      | 一般病情，按序处理   | 30 分钟内 |
| 非紧急 | non-urgent | 4      | 轻微病情，可延后处理 | 1 小时内  |

## 使用示例

### JavaScript/TypeScript

```typescript
import axios from 'axios'

// 分诊分析
const analyzePatient = async (triageData: TriageRequest) => {
  try {
    const response = await axios.post('/api/triage/analyze', triageData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })
    return response.data
  } catch (error) {
    console.error('分诊分析失败:', error)
    throw error
  }
}

// 获取分诊历史
const getTriageHistory = async (params: HistoryParams) => {
  try {
    const response = await axios.get('/api/triage/history', {
      params,
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    return response.data
  } catch (error) {
    console.error('获取分诊历史失败:', error)
    throw error
  }
}
```

### Python

```python
import requests

def analyze_patient_triage(triage_data, token):
    """执行患者分诊分析"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(
        'http://localhost:8000/api/triage/analyze',
        json=triage_data,
        headers=headers
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'分诊分析失败: {response.text}')

def get_triage_history(token, page=1, page_size=10):
    """获取分诊历史"""
    headers = {'Authorization': f'Bearer {token}'}
    params = {'page': page, 'pageSize': page_size}

    response = requests.get(
        'http://localhost:8000/api/triage/history',
        params=params,
        headers=headers
    )

    return response.json()
```

## 注意事项

1. **数据隐私**：患者信息需要严格保密，遵循医疗数据保护法规
2. **AI 辅助**：分诊结果仅供参考，最终诊断需要专业医生确认
3. **紧急情况**：对于危重患者，应立即启动急救流程
4. **数据完整性**：提供越完整的患者信息，分诊结果越准确
5. **系统限制**：本系统不能替代专业医疗判断，仅作为辅助工具使用
