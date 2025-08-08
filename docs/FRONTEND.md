# 前端组件文档

## 📋 概述

院前急救助手系统前端基于Vue 3 + TypeScript构建，采用组合式API和现代化的开发模式。使用Element Plus作为UI框架，Tailwind CSS进行样式定制。

### 🏗️ 技术栈

- **框架**: Vue 3.4+
- **语言**: TypeScript 5.0+
- **构建工具**: Vite 5.0+
- **UI框架**: Element Plus 2.4+
- **样式**: Tailwind CSS 3.4+
- **状态管理**: Pinia 2.1+
- **路由**: Vue Router 4.2+
- **图标**: Font Awesome + Element Plus Icons

## 📁 项目结构

```
src/
├── components/          # 可复用组件
│   ├── chat/           # 聊天相关组件
│   ├── emergency/      # 应急指导组件
│   ├── home/           # 首页组件
│   ├── knowledge/      # 知识库组件
│   ├── layout/         # 布局组件
│   └── triage/         # 分诊组件
├── views/              # 页面视图
├── stores/             # Pinia状态管理
├── api/                # API接口封装
├── router/             # 路由配置
├── types/              # TypeScript类型定义
├── utils/              # 工具函数
└── assets/             # 静态资源
```

## 🎨 页面视图 (Views)

### 首页 (HomeView.vue)

**路径**: `/`  
**组件**: `src/views/HomeView.vue`

系统首页，展示产品介绍和功能概览。

**主要组件**:

- `HeroSection` - 英雄区块
- `FeaturesSection` - 功能介绍
- `WorkflowSection` - 工作流程
- `AdvantagesSection` - 产品优势
- `ContactSection` - 联系信息
- `FooterSection` - 页脚

### 登录页面 (LoginView.vue)

**路径**: `/login`  
**组件**: `src/views/LoginView.vue`

用户登录页面，支持用户名/邮箱登录。

**功能特性**:

- 表单验证
- 记住登录状态
- 错误提示
- 自动跳转

### 注册页面 (RegisterView.vue)

**路径**: `/register`  
**组件**: `src/views/RegisterView.vue`

用户注册页面。

### 智能问答 (AIChat.vue)

**路径**: `/ai-chat`  
**组件**: `src/views/AIChat.vue`

AI智能问答主页面，提供知识库问答和图谱问答两种模式。

**主要组件**:

- `LeftSidebar` - 左侧会话列表
- `ChatPanel` - 中央聊天面板
- `RightSidebar` - 右侧参考资料

**功能特性**:

- 多会话管理
- 流式对话
- 参考资料展示
- 快速问题模板

### 智能分诊 (SmartTriage.vue)

**路径**: `/smart-triage`  
**组件**: `src/views/SmartTriage.vue`

智能分诊系统，通过向导式界面收集患者信息并进行AI分析。

**主要组件**:

- `TriageWizard` - 分诊向导
- `TriageResult` - 分诊结果
- `TriageHistory` - 历史记录

### 应急指导 (EmergencyGuide.vue)

**路径**: `/emergency-guide`  
**组件**: `src/views/EmergencyGuide.vue`

应急指导系统，提供不同场景的应急处理指导。

### 知识库 (KnowledgeView.vue)

**路径**: `/knowledge`  
**组件**: `src/views/KnowledgeView.vue`

知识库主页面，包含文档、视频、收藏等子页面。

**子路由**:

- `/knowledge/documents` - 文档库
- `/knowledge/videos` - 视频库
- `/knowledge/favorites` - 收藏夹

### 管理后台 (AdminView.vue)

**路径**: `/admin`  
**组件**: `src/views/AdminView.vue`  
**权限**: 管理员

管理员后台页面。

## 🧩 组件库

### 布局组件 (Layout)

#### 导航栏 (Navbar.vue)

**位置**: `src/components/layout/Navbar.vue`

顶部导航栏组件，包含Logo、导航菜单、用户信息等。

**Props**:

```typescript
interface NavbarProps {
  // 暂无props
}
```

**功能特性**:

- 响应式设计
- 用户登录状态显示
- 下拉菜单
- 路由高亮

### 聊天组件 (Chat)

#### 左侧边栏 (LeftSidebar.vue)

**位置**: `src/components/chat/LeftSidebar.vue`

聊天页面左侧边栏，显示会话列表和模式切换。

**Props**:

```typescript
interface LeftSidebarProps {
  modelValue: 'kb' | 'graph' // 当前聊天模式
}
```

**Events**:

```typescript
interface LeftSidebarEvents {
  'update:modelValue': (mode: 'kb' | 'graph') => void
  'select-chat': (chatId: string) => void
  'new-chat': () => void
}
```

#### 聊天面板 (ChatPanel.vue)

**位置**: `src/components/chat/ChatPanel.vue`

中央聊天面板，处理消息发送和显示。

**Props**:

```typescript
interface ChatPanelProps {
  sessionId: string
  mode: 'kb' | 'graph'
}
```

**功能特性**:

- 消息流式显示
- Markdown渲染
- 代码高亮
- 参考资料链接
- 消息复制

#### 右侧边栏 (RightSidebar.vue)

**位置**: `src/components/chat/RightSidebar.vue`

右侧参考资料栏，显示相关文档和快速问题。

### 分诊组件 (Triage)

#### 分诊向导 (TriageWizard.vue)

**位置**: `src/components/triage/TriageWizard.vue`

分步式分诊信息收集向导。

**功能特性**:

- 多步骤表单
- 数据验证
- 进度指示
- 动态字段

**步骤流程**:

1. 基本信息 - 年龄、性别、主诉
2. 症状描述 - 症状选择和描述
3. 生命体征 - 血压、心率、体温等
4. 病史信息 - 既往病史、过敏史、用药史
5. 确认提交 - 信息确认和提交

### 应急组件 (Emergency)

#### 场景选择 (ScenarioSelector.vue)

**位置**: `src/components/emergency/ScenarioSelector.vue`

应急场景选择组件。

#### 设备定位 (EquipmentLocator.vue)

**位置**: `src/components/emergency/EquipmentLocator.vue`

医疗设备定位组件，集成地图显示。

### 知识库组件 (Knowledge)

#### 文档视图 (DocumentView.vue)

**位置**: `src/components/knowledge/DocumentView.vue`

知识库文档展示组件。

**功能特性**:

- 分类筛选
- 关键词搜索
- 分页显示
- 收藏功能

#### 视频视图 (VideoView.vue)

**位置**: `src/components/knowledge/VideoView.vue`

教学视频展示组件。

#### 收藏视图 (FavoriteView.vue)

**位置**: `src/components/knowledge/FavoriteView.vue`

用户收藏内容展示。

### 首页组件 (Home)

#### 英雄区块 (HeroSection.vue)

**位置**: `src/components/home/HeroSection.vue`

首页顶部英雄区块，包含主标题和CTA按钮。

#### 功能介绍 (FeaturesSection.vue)

**位置**: `src/components/home/FeaturesSection.vue`

系统功能介绍卡片组。

#### 工作流程 (WorkflowSection.vue)

**位置**: `src/components/home/WorkflowSection.vue`

系统使用流程展示。

## 🗂️ 状态管理 (Stores)

### 用户状态 (user.ts)

**位置**: `src/stores/user.ts`

管理用户登录状态、个人信息等。

**State**:

```typescript
interface UserState {
  isAuthenticated: boolean
  user: User | null
  token: string | null
  refreshToken: string | null
}
```

**Actions**:

- `login(credentials)` - 用户登录
- `logout()` - 用户登出
- `refreshToken()` - 刷新令牌
- `updateProfile(data)` - 更新个人信息

### 聊天状态 (chat.ts)

**位置**: `src/stores/chat.ts`

管理聊天会话、消息等状态。

**State**:

```typescript
interface ChatState {
  sessions: ChatSession[]
  currentSession: ChatSession | null
  messages: ChatMessage[]
  isLoading: boolean
}
```

## 🔌 API 接口 (API)

### 认证接口 (auth.ts)

**位置**: `src/api/auth.ts`

用户认证相关API封装。

**主要方法**:

- `login(credentials)` - 登录
- `register(userData)` - 注册
- `refreshToken(token)` - 刷新令牌
- `logout()` - 登出

### 聊天接口 (chat.ts)

**位置**: `src/api/chat.ts`

聊天功能API封装。

### 分诊接口 (triage.ts)

**位置**: `src/api/triage.ts`

智能分诊API封装。

### 知识库接口 (knowledge.ts)

**位置**: `src/api/knowledge.ts`

知识库相关API封装。

## 🎨 样式规范

### Tailwind CSS 配置

**配置文件**: `tailwind.config.js`

自定义主题色彩、字体、间距等。

**主要颜色**:

- Primary: 蓝色系 (#3B82F6)
- Success: 绿色系 (#10B981)
- Warning: 黄色系 (#F59E0B)
- Danger: 红色系 (#EF4444)

### 组件样式约定

1. **布局**: 使用Flexbox和Grid
2. **响应式**: 移动优先设计
3. **间距**: 使用Tailwind间距系统
4. **颜色**: 使用主题色彩变量
5. **字体**: 系统字体栈

## 🔧 开发规范

### 组件开发

1. **命名**: 使用PascalCase
2. **文件结构**: 单文件组件(.vue)
3. **Props**: 使用TypeScript接口定义
4. **Events**: 明确事件类型
5. **样式**: 优先使用Tailwind类

### TypeScript 规范

1. **类型定义**: 统一放在types目录
2. **接口命名**: 使用I前缀或描述性名称
3. **严格模式**: 启用strict模式
4. **类型导入**: 使用type关键字

### 代码风格

1. **ESLint**: 使用Vue官方配置
2. **Prettier**: 统一代码格式
3. **注释**: 重要逻辑添加注释
4. **命名**: 使用有意义的变量名

## 🧪 测试

### 单元测试

使用Vitest进行组件单元测试。

**测试文件**: `src/components/__tests__/`

### E2E测试

使用Playwright进行端到端测试。

**测试文件**: `tests/e2e/`

## 📱 响应式设计

### 断点设置

- **sm**: 640px+
- **md**: 768px+
- **lg**: 1024px+
- **xl**: 1280px+
- **2xl**: 1536px+

### 移动端适配

1. **导航**: 汉堡菜单
2. **布局**: 单列布局
3. **表格**: 横向滚动
4. **表单**: 全宽输入

## 🚀 构建部署

### 开发环境

```bash
npm run dev
```

### 生产构建

```bash
npm run build
```

### 预览构建

```bash
npm run preview
```

---

**注意**: 本文档基于前端 v1.0.0 版本，组件API可能会随版本更新而变化。
