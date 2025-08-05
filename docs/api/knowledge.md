# 知识库 API

## 概述

知识库模块提供医疗文档、视频资源的分类管理和检索功能，支持分类浏览、搜索、收藏等功能。

**基础路径**: `/api/knowledge`

## 接口列表

### 1. 获取知识分类

#### 1.1 基本信息

> 请求路径：`/api/knowledge/categories`
>
> 请求方式：`GET`
>
> 接口描述：获取知识库的分类树结构

#### 1.2 请求参数

无需参数

#### 1.3 响应数据

响应示例：

```json
{
  "code": 200,
  "message": "Knowledge categories retrieved successfully",
  "data": [
    {
      "id": 1,
      "name": "急救知识",
      "description": "紧急救护相关知识",
      "icon": "fas fa-heartbeat",
      "sortOrder": 1,
      "itemCount": 25,
      "children": [
        {
          "id": 11,
          "name": "心肺复苏",
          "description": "CPR相关知识",
          "parentId": 1,
          "itemCount": 8
        },
        {
          "id": 12,
          "name": "外伤处理",
          "description": "外伤急救处理",
          "parentId": 1,
          "itemCount": 12
        }
      ]
    },
    {
      "id": 2,
      "name": "常见疾病",
      "description": "常见疾病知识",
      "icon": "fas fa-stethoscope",
      "sortOrder": 2,
      "itemCount": 45,
      "children": [
        {
          "id": 21,
          "name": "心血管疾病",
          "description": "心血管相关疾病",
          "parentId": 2,
          "itemCount": 20
        }
      ]
    }
  ]
}
```

### 2. 获取知识条目

#### 2.1 基本信息

> 请求路径：`/api/knowledge/items`
>
> 请求方式：`GET`
>
> 接口描述：获取知识库条目列表，支持分类过滤和搜索

#### 2.2 请求参数

参数格式：`Query String`

参数说明：

| 参数名      | 类型   | 是否必须 | 备注                                  |
| ----------- | ------ | -------- | ------------------------------------- |
| categoryId  | number | 可选     | 分类 ID                               |
| contentType | string | 可选     | 内容类型：document/video/image        |
| search      | string | 可选     | 搜索关键词                            |
| page        | number | 可选     | 页码，默认 1                          |
| pageSize    | number | 可选     | 每页数量，默认 10                     |
| sortBy      | string | 可选     | 排序字段：created_at/updated_at/title |
| sortOrder   | string | 可选     | 排序方向：asc/desc                    |

请求示例：

```
/api/knowledge/items?categoryId=11&contentType=document&search=心肺复苏&page=1&pageSize=10
```

#### 2.3 响应数据

响应示例：

```json
{
  "code": 200,
  "message": "Knowledge items retrieved successfully",
  "data": {
    "total": 8,
    "page": 1,
    "pageSize": 10,
    "items": [
      {
        "id": 101,
        "title": "成人心肺复苏操作指南",
        "description": "详细的成人CPR操作步骤和注意事项",
        "contentType": "document",
        "category": {
          "id": 11,
          "name": "心肺复苏"
        },
        "author": "急救医学专家组",
        "tags": ["CPR", "急救", "心脏骤停"],
        "difficulty": "intermediate",
        "readTime": 15,
        "viewCount": 1250,
        "likeCount": 89,
        "isFavorited": false,
        "thumbnailUrl": "/uploads/thumbnails/cpr-guide.jpg",
        "fileUrl": "/uploads/documents/cpr-guide.pdf",
        "fileSize": 2048576,
        "createdAt": "2024-01-01T09:00:00Z",
        "updatedAt": "2024-01-01T09:00:00Z"
      }
    ]
  }
}
```

### 3. 获取知识详情

#### 3.1 基本信息

> 请求路径：`/api/knowledge/items/{itemId}`
>
> 请求方式：`GET`
>
> 接口描述：获取指定知识条目的详细信息

#### 3.2 请求参数

路径参数：

| 参数名 | 类型   | 是否必须 | 备注        |
| ------ | ------ | -------- | ----------- |
| itemId | number | 必须     | 知识条目 ID |

#### 3.3 响应数据

响应示例：

```json
{
  "code": 200,
  "message": "Knowledge item retrieved successfully",
  "data": {
    "id": 101,
    "title": "成人心肺复苏操作指南",
    "description": "详细的成人CPR操作步骤和注意事项",
    "content": "心肺复苏（CPR）是一项重要的急救技能...",
    "contentType": "document",
    "category": {
      "id": 11,
      "name": "心肺复苏",
      "parentName": "急救知识"
    },
    "author": "急救医学专家组",
    "tags": ["CPR", "急救", "心脏骤停"],
    "difficulty": "intermediate",
    "readTime": 15,
    "viewCount": 1251,
    "likeCount": 89,
    "isFavorited": false,
    "relatedItems": [
      {
        "id": 102,
        "title": "AED使用指南",
        "contentType": "video"
      }
    ],
    "attachments": [
      {
        "name": "CPR操作图解",
        "url": "/uploads/attachments/cpr-steps.pdf",
        "type": "pdf",
        "size": 1024000
      }
    ],
    "createdAt": "2024-01-01T09:00:00Z",
    "updatedAt": "2024-01-01T09:00:00Z"
  }
}
```

### 4. 搜索知识库

#### 4.1 基本信息

> 请求路径：`/api/knowledge/search`
>
> 请求方式：`GET`
>
> 接口描述：全文搜索知识库内容

#### 4.2 请求参数

参数格式：`Query String`

参数说明：

| 参数名      | 类型   | 是否必须 | 备注              |
| ----------- | ------ | -------- | ----------------- |
| q           | string | 必须     | 搜索关键词        |
| contentType | string | 可选     | 内容类型过滤      |
| category    | number | 可选     | 分类 ID 过滤      |
| page        | number | 可选     | 页码，默认 1      |
| pageSize    | number | 可选     | 每页数量，默认 10 |

请求示例：

```
/api/knowledge/search?q=心脏病&contentType=document&page=1&pageSize=10
```

#### 4.3 响应数据

响应示例：

```json
{
  "code": 200,
  "message": "Search completed successfully",
  "data": {
    "query": "心脏病",
    "total": 15,
    "page": 1,
    "pageSize": 10,
    "searchTime": 0.25,
    "items": [
      {
        "id": 201,
        "title": "冠心病的预防与治疗",
        "description": "冠心病的病因、症状、预防和治疗方法",
        "contentType": "document",
        "category": {
          "id": 21,
          "name": "心血管疾病"
        },
        "highlights": [
          "冠心病是最常见的<em>心脏病</em>类型之一",
          "预防<em>心脏病</em>需要控制危险因素"
        ],
        "relevanceScore": 0.95,
        "createdAt": "2024-01-01T08:00:00Z"
      }
    ]
  }
}
```

### 5. 收藏/取消收藏

#### 5.1 基本信息

> 请求路径：`/api/knowledge/items/{itemId}/favorite`
>
> 请求方式：`POST`
>
> 接口描述：收藏或取消收藏知识条目

#### 5.2 请求参数

路径参数：

| 参数名 | 类型   | 是否必须 | 备注        |
| ------ | ------ | -------- | ----------- |
| itemId | number | 必须     | 知识条目 ID |

请求体参数：

| 参数名     | 类型    | 是否必须 | 备注                  |
| ---------- | ------- | -------- | --------------------- |
| isFavorite | boolean | 必须     | true 收藏，false 取消 |

请求示例：

```json
{
  "isFavorite": true
}
```

#### 5.3 响应数据

响应示例：

```json
{
  "code": 200,
  "message": "Favorite status updated successfully",
  "data": {
    "itemId": 101,
    "isFavorited": true,
    "favoriteCount": 90
  }
}
```

### 6. 获取收藏列表

#### 6.1 基本信息

> 请求路径：`/api/knowledge/favorites`
>
> 请求方式：`GET`
>
> 接口描述：获取用户的收藏列表

#### 6.2 请求参数

参数格式：`Query String`

参数说明：

| 参数名      | 类型   | 是否必须 | 备注              |
| ----------- | ------ | -------- | ----------------- |
| contentType | string | 可选     | 内容类型过滤      |
| page        | number | 可选     | 页码，默认 1      |
| pageSize    | number | 可选     | 每页数量，默认 10 |

#### 6.3 响应数据

响应示例：

```json
{
  "code": 200,
  "message": "Favorites retrieved successfully",
  "data": {
    "total": 12,
    "page": 1,
    "pageSize": 10,
    "items": [
      {
        "id": 101,
        "title": "成人心肺复苏操作指南",
        "contentType": "document",
        "category": {
          "id": 11,
          "name": "心肺复苏"
        },
        "favoritedAt": "2024-01-01T10:00:00Z"
      }
    ]
  }
}
```

## 内容类型说明

| 类型     | 名称 | 描述               | 支持格式            |
| -------- | ---- | ------------------ | ------------------- |
| document | 文档 | 文本文档、PDF 等   | pdf, doc, docx, txt |
| video    | 视频 | 教学视频、演示视频 | mp4, avi, mov       |
| image    | 图片 | 图解、流程图等     | jpg, png, gif, svg  |
| audio    | 音频 | 语音指导、讲座录音 | mp3, wav, m4a       |

## 难度级别说明

| 级别 | 英文名       | 描述               | 目标用户     |
| ---- | ------------ | ------------------ | ------------ |
| 初级 | beginner     | 基础知识，易于理解 | 普通用户     |
| 中级 | intermediate | 需要一定医学基础   | 医护学生     |
| 高级 | advanced     | 专业性强，深入详细 | 专业医护人员 |

## 使用示例

### JavaScript/TypeScript

```typescript
// 获取知识分类
const getKnowledgeCategories = async () => {
  const response = await fetch('/api/knowledge/categories', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  return response.json()
}

// 获取知识条目
const getKnowledgeItems = async (params: KnowledgeParams) => {
  const queryString = new URLSearchParams(params).toString()
  const response = await fetch(`/api/knowledge/items?${queryString}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  return response.json()
}

// 搜索知识库
const searchKnowledge = async (query: string, filters?: SearchFilters) => {
  const params = new URLSearchParams({ q: query, ...filters })
  const response = await fetch(`/api/knowledge/search?${params}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  return response.json()
}

// 收藏知识条目
const toggleFavorite = async (itemId: number, isFavorite: boolean) => {
  const response = await fetch(`/api/knowledge/items/${itemId}/favorite`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ isFavorite }),
  })
  return response.json()
}

// 获取收藏列表
const getFavorites = async (page: number = 1) => {
  const response = await fetch(`/api/knowledge/favorites?page=${page}`, {
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

def get_knowledge_categories(token):
    """获取知识分类"""
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(
        'http://localhost:8000/api/knowledge/categories',
        headers=headers
    )
    return response.json()

def get_knowledge_items(token, **params):
    """获取知识条目"""
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(
        'http://localhost:8000/api/knowledge/items',
        params=params,
        headers=headers
    )
    return response.json()

def search_knowledge(query, token, **filters):
    """搜索知识库"""
    headers = {'Authorization': f'Bearer {token}'}
    params = {'q': query, **filters}

    response = requests.get(
        'http://localhost:8000/api/knowledge/search',
        params=params,
        headers=headers
    )
    return response.json()

def toggle_favorite(item_id, is_favorite, token):
    """收藏/取消收藏"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    data = {'isFavorite': is_favorite}

    response = requests.post(
        f'http://localhost:8000/api/knowledge/items/{item_id}/favorite',
        json=data,
        headers=headers
    )
    return response.json()

def get_favorites(token, page=1, page_size=10):
    """获取收藏列表"""
    headers = {'Authorization': f'Bearer {token}'}
    params = {'page': page, 'pageSize': page_size}

    response = requests.get(
        'http://localhost:8000/api/knowledge/favorites',
        params=params,
        headers=headers
    )
    return response.json()
```

## 注意事项

1. **版权保护**：所有知识库内容均受版权保护，仅供学习使用
2. **内容更新**：知识库内容会定期更新，建议关注最新版本
3. **文件大小**：大文件可能需要较长加载时间，建议提供加载提示
4. **离线访问**：部分内容支持离线缓存，提升用户体验
5. **专业性**：高级内容需要专业医学背景才能理解
6. **引用规范**：使用知识库内容时请注明来源
