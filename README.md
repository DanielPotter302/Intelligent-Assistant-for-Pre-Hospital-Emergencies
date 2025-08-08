# 院前急救助手系统

> 基于AI的智能院前急救辅助系统，提供智能分诊、应急指导、知识问答等功能

## 📋 项目概述

院前急救助手系统是一个现代化的医疗急救辅助平台，集成了人工智能技术，为医护人员和急救人员提供专业的决策支持和操作指导。

### 🏗️ 技术架构

**前端技术栈：**

- Vue 3 + TypeScript + Vite
- Element Plus UI框架
- Tailwind CSS
- Pinia 状态管理
- Vue Router 路由管理

**后端技术栈：**

- FastAPI + Python 3.8+
- SQLAlchemy ORM
- SQLite 数据库
- 通义千问 LLM (OpenAI兼容模式)
- JWT 认证

### 🚀 核心功能

- **🩺 智能分诊**: AI驱动的患者分诊系统，快速评估病情严重程度
- **🚑 应急指导**: 针对不同紧急情况提供专业的处理指导
- **💬 智能问答**: 基于医疗知识库的AI问答系统
- **📚 知识库**: 丰富的医疗文档、视频资源库
- **👥 用户管理**: 完整的用户认证和权限管理系统

## 🚀 快速开始

### 一键启动（推荐）

#### Linux/macOS

```bash
chmod +x setup_and_start.sh
./setup_and_start.sh
```

#### Windows

```cmd
setup_and_start.bat
```

### 手动启动

#### 环境要求

- Node.js 16.0+
- Python 3.8+
- npm 最新版本

#### 安装依赖

```bash
# 前端依赖
npm install

# 后端依赖
cd backend
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

#### 启动服务

```bash
# 启动后端
cd backend
source venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 启动前端
npm run dev -- --port 5173 --host 0.0.0.0
```

## 🌐 访问地址

- **前端应用**: http://localhost:5173
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

## 📁 项目结构

```
院前急救助手系统/
├── src/                     # 前端源代码
│   ├── components/          # Vue组件
│   │   ├── chat/           # 聊天相关组件
│   │   ├── emergency/      # 应急指导组件
│   │   ├── home/           # 首页组件
│   │   ├── knowledge/      # 知识库组件
│   │   ├── layout/         # 布局组件
│   │   └── triage/         # 分诊组件
│   ├── views/              # 页面视图
│   ├── stores/             # Pinia状态管理
│   ├── api/                # API接口
│   └── router/             # 路由配置
├── backend/                # 后端源代码
│   ├── app/                # 应用代码
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic模式
│   │   └── services/       # 业务服务
│   ├── venv/               # Python虚拟环境
│   ├── uploads/            # 文件上传目录
│   ├── logs/               # 日志目录
│   ├── requirements.txt    # Python依赖
│   ├── .env               # 环境配置
│   ├── main.py            # 主应用文件
│   ├── init_db.py         # 数据库初始化
│   ├── init_knowledge.py  # 知识库初始化
│   ├── classified_grouped_aggregated.txt  # 知识库数据
│   └── pre_hospital_assistant.db  # SQLite数据库
├── public/                 # 静态资源
├── docs/                   # 项目文档
├── setup_and_start.sh      # Linux/macOS启动脚本
├── setup_and_start.bat     # Windows启动脚本
└── README.md              # 项目说明
```

## 📖 文档

- [API接口文档](./docs/API.md) - 完整的API接口说明
- [前端组件文档](./docs/FRONTEND.md) - 前端组件和页面说明
- [部署指南](./docs/DEPLOYMENT.md) - 生产环境部署指南
- [开发指南](./docs/DEVELOPMENT.md) - 开发环境配置和规范

## 🔧 配置说明

### 端口配置

- **前端端口**: 5173 (固定)
- **后端端口**: 8000 (固定)

### 数据库配置

- **类型**: SQLite
- **文件位置**: `backend/pre_hospital_assistant.db`
- **自动初始化**: 首次运行时自动创建

### 知识库配置

- **总分类数**: 8个专业分类
- **知识条目**: 515条急救知识
- **视频资源**: 6个教学视频
- **书籍资源**: 2本急救手册

### LLM配置

- **模型提供商**: 阿里云通义千问
- **API模式**: OpenAI兼容模式
- **主要模型**: qwen-plus
- **思考模型**: qwen-plus-2025-04-28

### 默认用户账号

- **管理员**: admin / admin123
- **普通用户**: danielpotter / danielpotter123

## 🛠️ 开发

### 代码规范

- 前端使用 ESLint + Prettier
- 后端遵循 PEP 8 规范
- 使用 TypeScript 严格模式

### 测试

```bash
# 前端测试
npm run test:unit
npm run test:e2e

# 后端测试
cd backend
python -m pytest
```

### 构建

```bash
# 前端构建
npm run build

# 预览构建结果
npm run preview
```

## 📝 更新日志

### v1.0.0 (2024-08-08)

- ✨ 初始版本发布
- 🩺 智能分诊功能
- 🚑 应急指导系统
- 💬 AI智能问答
- 📚 知识库管理
- 👥 用户认证系统

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进项目。

## 📄 许可证

本项目采用 MIT 许可证。

## 📞 联系我们

如有问题或建议，请联系项目维护团队。

---

**院前急救助手系统** - 让急救更智能，让生命更安全 🏥✨
