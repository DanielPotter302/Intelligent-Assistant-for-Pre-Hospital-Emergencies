# 开发指南

## 📋 概述

本文档为院前急救助手系统的开发人员提供详细的开发环境配置、代码规范、开发流程等指导。

## 🛠️ 开发环境配置

### 系统要求

- **操作系统**: Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **Node.js**: 16.0+
- **Python**: 3.8+
- **Git**: 2.20+
- **IDE**: VS Code (推荐) / PyCharm / WebStorm

### 必需工具

```bash
# Node.js 和 npm
node --version  # v16.0+
npm --version   # v8.0+

# Python 和 pip
python3 --version  # v3.8+
pip3 --version

# Git
git --version  # v2.20+
```

### 推荐工具

- **VS Code 扩展**:
  - Vue Language Features (Volar)
  - TypeScript Vue Plugin (Volar)
  - Python
  - Pylance
  - ESLint
  - Prettier
  - GitLens
  - Thunder Client (API测试)

- **Chrome 扩展**:
  - Vue.js devtools
  - React Developer Tools

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone <repository_url>
cd pre-hospital-assistant
```

### 2. 环境配置

```bash
# 使用一键启动脚本
chmod +x setup_and_start.sh
./setup_and_start.sh

# 或手动配置
npm install
cd backend
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 3. 启动开发服务器

```bash
# 启动后端 (终端1)
cd backend
source venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 启动前端 (终端2)
npm run dev
```

## 📁 项目结构详解

```
院前急救助手系统/
├── src/                     # 前端源代码
│   ├── api/                # API接口封装
│   │   ├── auth.ts         # 认证相关API
│   │   ├── chat.ts         # 聊天相关API
│   │   ├── knowledge.ts    # 知识库API
│   │   ├── triage.ts       # 分诊API
│   │   └── index.ts        # API统一导出
│   ├── components/         # Vue组件
│   │   ├── chat/          # 聊天组件
│   │   ├── emergency/     # 应急组件
│   │   ├── home/          # 首页组件
│   │   ├── knowledge/     # 知识库组件
│   │   ├── layout/        # 布局组件
│   │   └── triage/        # 分诊组件
│   ├── stores/            # Pinia状态管理
│   │   ├── user.ts        # 用户状态
│   │   ├── chat.ts        # 聊天状态
│   │   └── index.ts       # Store统一导出
│   ├── types/             # TypeScript类型定义
│   │   ├── api.ts         # API类型
│   │   ├── user.ts        # 用户类型
│   │   └── index.ts       # 类型统一导出
│   ├── utils/             # 工具函数
│   │   ├── request.ts     # HTTP请求封装
│   │   ├── auth.ts        # 认证工具
│   │   └── format.ts      # 格式化工具
│   ├── views/             # 页面视图
│   ├── router/            # 路由配置
│   └── assets/            # 静态资源
├── backend/               # 后端源代码
│   ├── app/              # 应用代码
│   │   ├── api/          # API路由
│   │   │   ├── routes/   # 路由模块
│   │   │   └── deps.py   # 依赖注入
│   │   ├── core/         # 核心配置
│   │   │   ├── config.py # 配置管理
│   │   │   ├── database.py # 数据库配置
│   │   │   └── security.py # 安全配置
│   │   ├── models/       # 数据模型
│   │   ├── schemas/      # Pydantic模式
│   │   └── services/     # 业务服务
│   ├── tests/            # 测试代码
│   └── requirements.txt  # Python依赖
├── docs/                 # 项目文档
├── tests/                # 前端测试
└── public/               # 静态资源
```

## 🎨 代码规范

### 前端规范

#### TypeScript 规范

```typescript
// ✅ 好的示例
interface UserInfo {
  id: string
  username: string
  email: string
  role: 'admin' | 'user'
}

const fetchUserInfo = async (userId: string): Promise<UserInfo> => {
  const response = await api.get(`/users/${userId}`)
  return response.data
}

// ❌ 避免的写法
const fetchUserInfo = async (userId: any) => {
  const response = await api.get(`/users/${userId}`)
  return response.data
}
```

#### Vue 组件规范

```vue
<!-- ✅ 好的示例 -->
<template>
  <div class="user-profile">
    <h1 class="text-2xl font-bold">{{ user.username }}</h1>
    <p class="text-gray-600">{{ user.email }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { User } from '@/types/user'
import { fetchUserProfile } from '@/api/user'

// Props定义
interface Props {
  userId: string
}

const props = defineProps<Props>()

// 响应式数据
const user = ref<User | null>(null)
const loading = ref(false)

// 方法
const loadUser = async () => {
  loading.value = true
  try {
    user.value = await fetchUserProfile(props.userId)
  } catch (error) {
    console.error('Failed to load user:', error)
  } finally {
    loading.value = false
  }
}

// 生命周期
onMounted(() => {
  loadUser()
})
</script>

<style scoped>
.user-profile {
  @apply p-4 bg-white rounded-lg shadow;
}
</style>
```

#### 命名规范

```typescript
// 组件名称 - PascalCase
UserProfile.vue
ChatPanel.vue
TriageWizard.vue

// 文件名 - kebab-case
user - profile.ts
chat - service.ts
triage - utils.ts

// 变量和函数 - camelCase
const userName = 'admin'
const fetchUserData = () => {}

// 常量 - UPPER_SNAKE_CASE
const API_BASE_URL = 'http://localhost:8000'
const MAX_RETRY_COUNT = 3

// 类型和接口 - PascalCase
interface UserInfo {}
type ChatMode = 'kb' | 'graph'
```

### 后端规范

#### Python 代码规范

```python
# ✅ 好的示例
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True

async def create_user(
    user_data: UserCreate,
    db: Session
) -> UserResponse:
    """创建新用户"""
    # 检查用户是否已存在
    existing_user = db.query(User).filter(
        User.username == user_data.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # 创建用户
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return UserResponse.from_orm(user)
```

#### API 路由规范

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/", response_model=ApiResponse)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    创建新用户

    - **username**: 用户名
    - **email**: 邮箱地址
    - **password**: 密码
    """
    try:
        user = await create_user(user_data, db)
        return ApiResponse(
            message="User created successfully",
            data=user
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

## 🔧 开发工具配置

### VS Code 配置

创建 `.vscode/settings.json`:

```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "typescript.preferences.importModuleSpecifier": "relative",
  "python.defaultInterpreterPath": "./backend/venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "files.associations": {
    "*.vue": "vue"
  }
}
```

创建 `.vscode/extensions.json`:

```json
{
  "recommendations": [
    "Vue.volar",
    "Vue.vscode-typescript-vue-plugin",
    "ms-python.python",
    "ms-python.pylance",
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "eamodio.gitlens"
  ]
}
```

### ESLint 配置

`.eslintrc.cjs`:

```javascript
module.exports = {
  root: true,
  env: {
    node: true,
    browser: true,
    es2022: true,
  },
  extends: [
    'plugin:vue/vue3-essential',
    '@vue/eslint-config-typescript',
    '@vue/eslint-config-prettier/skip-formatting',
  ],
  parserOptions: {
    ecmaVersion: 'latest',
  },
  rules: {
    'vue/multi-word-component-names': 'off',
    '@typescript-eslint/no-unused-vars': 'error',
    'prefer-const': 'error',
    'no-var': 'error',
  },
}
```

### Prettier 配置

`.prettierrc`:

```json
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 80,
  "endOfLine": "lf"
}
```

## 🧪 测试

### 前端测试

#### 单元测试

使用 Vitest 进行单元测试：

```typescript
// tests/unit/components/UserProfile.test.ts
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import UserProfile from '@/components/UserProfile.vue'

describe('UserProfile', () => {
  it('renders user information correctly', () => {
    const user = {
      id: '1',
      username: 'testuser',
      email: 'test@example.com',
    }

    const wrapper = mount(UserProfile, {
      props: { user },
    })

    expect(wrapper.text()).toContain('testuser')
    expect(wrapper.text()).toContain('test@example.com')
  })
})
```

#### E2E 测试

使用 Playwright 进行端到端测试：

```typescript
// tests/e2e/login.spec.ts
import { test, expect } from '@playwright/test'

test('user can login successfully', async ({ page }) => {
  await page.goto('http://localhost:5173/login')

  await page.fill('[data-testid="username"]', 'admin')
  await page.fill('[data-testid="password"]', 'admin123')
  await page.click('[data-testid="login-button"]')

  await expect(page).toHaveURL('http://localhost:5173/')
  await expect(page.locator('[data-testid="user-menu"]')).toBeVisible()
})
```

### 后端测试

#### 单元测试

```python
# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_success():
    response = client.post(
        "/api/auth/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "accessToken" in data["data"]
    assert data["data"]["user"]["username"] == "admin"

def test_login_invalid_credentials():
    response = client.post(
        "/api/auth/login",
        json={
            "username": "admin",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
```

### 运行测试

```bash
# 前端测试
npm run test:unit
npm run test:e2e

# 后端测试
cd backend
python -m pytest
python -m pytest --cov=app tests/
```

## 🔄 Git 工作流

### 分支策略

```
main (生产分支)
├── develop (开发分支)
│   ├── feature/user-auth (功能分支)
│   ├── feature/chat-system (功能分支)
│   └── bugfix/login-issue (修复分支)
└── hotfix/security-patch (热修复分支)
```

### 提交规范

使用 Conventional Commits 规范：

```bash
# 功能开发
git commit -m "feat: add user authentication system"

# 修复bug
git commit -m "fix: resolve login redirect issue"

# 文档更新
git commit -m "docs: update API documentation"

# 样式调整
git commit -m "style: improve button hover effects"

# 重构代码
git commit -m "refactor: optimize database queries"

# 性能优化
git commit -m "perf: improve chat message loading speed"

# 测试相关
git commit -m "test: add unit tests for auth service"
```

### 开发流程

1. **创建功能分支**

```bash
git checkout develop
git pull origin develop
git checkout -b feature/new-feature
```

2. **开发和提交**

```bash
git add .
git commit -m "feat: implement new feature"
git push origin feature/new-feature
```

3. **创建 Pull Request**

- 在 GitHub/GitLab 创建 PR
- 填写详细的描述
- 请求代码审查

4. **代码审查和合并**

- 通过代码审查
- 合并到 develop 分支
- 删除功能分支

## 🐛 调试技巧

### 前端调试

#### Vue DevTools

```javascript
// 在组件中添加调试信息
export default {
  name: 'ChatPanel',
  setup() {
    const messages = ref([])

    // 开发环境下暴露到全局
    if (process.env.NODE_ENV === 'development') {
      window.debugMessages = messages
    }

    return { messages }
  },
}
```

#### 浏览器调试

```typescript
// 使用 console.group 组织日志
console.group('API Request')
console.log('URL:', url)
console.log('Method:', method)
console.log('Data:', data)
console.groupEnd()

// 使用 debugger 断点
const processData = (data: any) => {
  debugger // 浏览器会在此处暂停
  return data.map((item) => ({ ...item, processed: true }))
}
```

### 后端调试

#### 日志记录

```python
import logging

logger = logging.getLogger(__name__)

async def process_chat_message(message: str):
    logger.info(f"Processing message: {message[:50]}...")

    try:
        result = await ai_service.generate_response(message)
        logger.info(f"Generated response length: {len(result)}")
        return result
    except Exception as e:
        logger.error(f"Failed to process message: {e}")
        raise
```

#### 使用 pdb 调试

```python
import pdb

def complex_function(data):
    pdb.set_trace()  # 设置断点
    processed_data = process_data(data)
    return processed_data
```

## 📊 性能优化

### 前端优化

#### 代码分割

```typescript
// 路由懒加载
const routes = [
  {
    path: '/chat',
    component: () => import('@/views/ChatView.vue'),
  },
  {
    path: '/triage',
    component: () => import('@/views/TriageView.vue'),
  },
]
```

#### 组件优化

```vue
<template>
  <div>
    <!-- 使用 v-memo 缓存渲染结果 -->
    <div v-memo="[user.id, user.lastUpdate]">
      {{ user.name }}
    </div>

    <!-- 虚拟滚动大列表 -->
    <VirtualList :items="messages" :item-height="60" v-slot="{ item }">
      <MessageItem :message="item" />
    </VirtualList>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

// 使用 computed 缓存计算结果
const filteredMessages = computed(() => {
  return messages.value.filter((msg) => msg.visible)
})
</script>
```

### 后端优化

#### 数据库查询优化

```python
# 使用 select_related 减少查询次数
users = db.query(User).options(
    selectinload(User.profile),
    selectinload(User.sessions)
).all()

# 使用索引
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)  # 添加索引
    email = Column(String, unique=True, index=True)     # 添加索引
```

#### 缓存策略

```python
from functools import lru_cache
import redis

# 内存缓存
@lru_cache(maxsize=128)
def get_user_permissions(user_id: str):
    return db.query(Permission).filter(
        Permission.user_id == user_id
    ).all()

# Redis 缓存
redis_client = redis.Redis(host='localhost', port=6379, db=0)

async def get_cached_data(key: str):
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)

    data = await fetch_data_from_db()
    redis_client.setex(key, 3600, json.dumps(data))  # 缓存1小时
    return data
```

## 📝 文档编写

### API 文档

使用 FastAPI 自动生成的文档，并添加详细的描述：

```python
@router.post(
    "/chat/sessions/{session_id}/messages",
    response_model=ApiResponse,
    summary="发送聊天消息",
    description="向指定的聊天会话发送消息并获取AI回复"
)
async def send_message(
    session_id: str = Path(..., description="聊天会话ID"),
    message: ChatMessageCreate = Body(..., description="消息内容"),
    current_user: User = Depends(get_current_active_user)
):
    """
    发送聊天消息

    Args:
        session_id: 聊天会话的唯一标识符
        message: 包含消息内容和类型的对象
        current_user: 当前登录用户

    Returns:
        包含AI回复的响应对象

    Raises:
        HTTPException: 当会话不存在或用户无权限时
    """
    pass
```

### 组件文档

```vue
<!--
UserProfile 组件

用于显示用户基本信息的组件

Props:
- user: User - 用户信息对象
- editable: boolean - 是否可编辑，默认 false

Events:
- update:user - 用户信息更新时触发
- avatar-click - 点击头像时触发

Slots:
- actions - 自定义操作按钮区域

Example:
<UserProfile 
  :user="currentUser" 
  :editable="true"
  @update:user="handleUserUpdate"
>
  <template #actions>
    <el-button @click="editProfile">编辑</el-button>
  </template>
</UserProfile>
-->
```

## 🚀 部署和发布

### 开发环境部署

```bash
# 使用开发脚本
./start_all.sh

# 或分别启动
./start_backend.sh
./start_frontend.sh
```

### 生产环境构建

```bash
# 前端构建
npm run build

# 后端打包
cd backend
pip freeze > requirements.txt
```

### 版本发布

```bash
# 更新版本号
npm version patch  # 或 minor, major

# 创建发布标签
git tag -a v1.0.1 -m "Release version 1.0.1"
git push origin v1.0.1

# 创建发布分支
git checkout -b release/v1.0.1
git push origin release/v1.0.1
```

## 📞 获取帮助

### 常见问题

1. **端口冲突**: 修改配置文件中的端口号
2. **依赖安装失败**: 清除缓存后重新安装
3. **数据库连接失败**: 检查数据库配置和权限
4. **API 请求失败**: 检查 CORS 配置和网络连接

### 技术支持

- **文档**: 查看项目 docs 目录
- **Issue**: 在 GitHub 提交问题
- **讨论**: 参与项目讨论区
- **邮件**: 联系维护团队

---

**祝您开发愉快！** 🎉
