# 用户认证 API

## 概述

用户认证模块提供用户注册、登录、令牌刷新等功能，使用 JWT 进行身份验证。

**基础路径**: `/api/auth`

## 接口列表

### 1. 用户注册

#### 1.1 基本信息

> 请求路径：`/api/auth/register`
>
> 请求方式：`POST`
>
> 接口描述：用户注册接口，创建新用户账户

#### 1.2 请求参数

参数格式：`application/json`

参数说明：

| 参数名     | 类型   | 是否必须 | 备注                |
| ---------- | ------ | -------- | ------------------- |
| username   | string | 必须     | 用户名，3-20 个字符 |
| email      | string | 必须     | 邮箱地址            |
| password   | string | 必须     | 密码，至少 8 个字符 |
| real_name  | string | 必须     | 真实姓名            |
| phone      | string | 可选     | 手机号码            |
| department | string | 可选     | 所属部门            |

请求示例：

```json
{
  "username": "zhangsan",
  "email": "zhangsan@example.com",
  "password": "password123",
  "real_name": "张三",
  "phone": "13800138000",
  "department": "急诊科"
}
```

#### 1.3 响应数据

参数格式：`application/json`

参数说明：

| 参数名        | 类型   | 是否必须 | 备注                         |
| ------------- | ------ | -------- | ---------------------------- |
| code          | number | 必须     | 响应码，200 成功，其他为失败 |
| message       | string | 必须     | 响应消息                     |
| data          | object | 可选     | 返回数据                     |
| \|- userId    | string | 可选     | 用户 ID                      |
| \|- username  | string | 可选     | 用户名                       |
| \|- email     | string | 可选     | 邮箱                         |
| \|- role      | string | 可选     | 用户角色                     |
| \|- createdAt | string | 可选     | 创建时间                     |

响应示例：

```json
{
  "code": 201,
  "message": "User registered successfully",
  "data": {
    "userId": "user_123456789",
    "username": "zhangsan",
    "email": "zhangsan@example.com",
    "role": "user",
    "createdAt": "2024-01-01T12:00:00Z"
  }
}
```

### 2. 用户登录

#### 2.1 基本信息

> 请求路径：`/api/auth/login`
>
> 请求方式：`POST`
>
> 接口描述：用户登录接口，验证用户身份并返回访问令牌

#### 2.2 请求参数

参数格式：`application/json`

参数说明：

| 参数名   | 类型   | 是否必须 | 备注         |
| -------- | ------ | -------- | ------------ |
| username | string | 必须     | 用户名或邮箱 |
| password | string | 必须     | 密码         |

请求示例：

```json
{
  "username": "zhangsan",
  "password": "password123"
}
```

#### 2.3 响应数据

参数说明：

| 参数名           | 类型   | 是否必须 | 备注                     |
| ---------------- | ------ | -------- | ------------------------ |
| code             | number | 必须     | 响应码                   |
| message          | string | 必须     | 响应消息                 |
| data             | object | 可选     | 返回数据                 |
| \|- accessToken  | string | 可选     | 访问令牌                 |
| \|- refreshToken | string | 可选     | 刷新令牌                 |
| \|- tokenType    | string | 可选     | 令牌类型，固定为"bearer" |
| \|- expiresIn    | number | 可选     | 令牌过期时间（秒）       |
| \|- user         | object | 可选     | 用户信息                 |

响应示例：

```json
{
  "code": 200,
  "message": "Login successful",
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "tokenType": "bearer",
    "expiresIn": 1800,
    "user": {
      "id": "user_123456789",
      "username": "zhangsan",
      "email": "zhangsan@example.com",
      "realName": "张三",
      "role": "user",
      "status": "active"
    }
  }
}
```

### 3. 刷新令牌

#### 3.1 基本信息

> 请求路径：`/api/auth/refresh`
>
> 请求方式：`POST`
>
> 接口描述：使用刷新令牌获取新的访问令牌

#### 3.2 请求参数

参数说明：

| 参数名       | 类型   | 是否必须 | 备注     |
| ------------ | ------ | -------- | -------- |
| refreshToken | string | 必须     | 刷新令牌 |

请求示例：

```json
{
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### 3.3 响应数据

响应示例：

```json
{
  "code": 200,
  "message": "Token refreshed successfully",
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "tokenType": "bearer",
    "expiresIn": 1800
  }
}
```

### 4. 用户登出

#### 4.1 基本信息

> 请求路径：`/api/auth/logout`
>
> 请求方式：`POST`
>
> 接口描述：用户登出，使令牌失效

#### 4.2 请求参数

请求头：

| 参数名        | 类型   | 是否必须 | 备注                  |
| ------------- | ------ | -------- | --------------------- |
| Authorization | string | 必须     | Bearer {access_token} |

#### 4.3 响应数据

响应示例：

```json
{
  "code": 200,
  "message": "Logout successful",
  "data": null
}
```

## 错误码说明

| 错误码 | 说明               |
| ------ | ------------------ |
| 400    | 请求参数错误       |
| 401    | 未授权或令牌无效   |
| 403    | 权限不足           |
| 409    | 用户名或邮箱已存在 |
| 422    | 数据验证失败       |
| 500    | 服务器内部错误     |

## 使用示例

### JavaScript/TypeScript

```typescript
// 用户注册
const register = async (userData: RegisterData) => {
  const response = await fetch('/api/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  })
  return response.json()
}

// 用户登录
const login = async (credentials: LoginData) => {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials),
  })
  return response.json()
}

// 使用令牌访问受保护的接口
const fetchProtectedData = async (token: string) => {
  const response = await fetch('/api/protected-endpoint', {
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

# 用户注册
def register_user(user_data):
    response = requests.post(
        'http://localhost:8000/api/auth/register',
        json=user_data
    )
    return response.json()

# 用户登录
def login_user(credentials):
    response = requests.post(
        'http://localhost:8000/api/auth/login',
        json=credentials
    )
    return response.json()

# 使用令牌访问受保护的接口
def fetch_protected_data(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(
        'http://localhost:8000/api/protected-endpoint',
        headers=headers
    )
    return response.json()
```

## 安全注意事项

1. **密码安全**：密码应至少包含 8 个字符，建议包含大小写字母、数字和特殊字符
2. **令牌存储**：访问令牌应存储在安全的地方，避免 XSS 攻击
3. **HTTPS**：生产环境必须使用 HTTPS 传输
4. **令牌过期**：及时处理令牌过期情况，使用刷新令牌获取新的访问令牌
5. **登出处理**：用户登出时应清除本地存储的令牌
