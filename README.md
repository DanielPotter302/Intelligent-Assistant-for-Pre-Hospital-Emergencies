# 院前急救助手 (Pre-hospital Assistant)

一个基于Vue.js和FastAPI的院前急救辅助系统，为急救人员提供智能化的急救指导和知识管理。

## 项目特色

- 🚑 **智能急救指导** - 基于AI的急救流程指导
- 📚 **知识库管理** - 急救手册和视频资料管理
- 🗺️ **设备地图** - 急救设备位置可视化
- 📱 **响应式设计** - 支持移动端和桌面端
- 🔐 **用户认证** - 安全的用户登录和权限管理

## 技术栈

### 前端

- **Vue 3** - 渐进式JavaScript框架
- **TypeScript** - 类型安全的JavaScript
- **Element Plus** - Vue 3 UI组件库
- **Vite** - 快速的前端构建工具
- **Pinia** - Vue 3状态管理

### 后端

- **FastAPI** - 现代、快速的Python Web框架
- **SQLAlchemy** - Python ORM
- **SQLite** - 轻量级数据库
- **通义千问API** - AI对话服务
- **JWT** - 用户认证

## 功能模块

### 1. 智能聊天

- AI驱动的急救对话
- 实时语音识别
- 多轮对话支持

### 2. 分诊系统

- 症状快速评估
- 紧急程度分级
- 急救建议生成

### 3. 知识管理

- 急救手册浏览
- 视频资料观看
- 收藏夹功能

### 4. 紧急指南

- 设备地图导航
- 安全提示
- 快速操作指南

### 5. 管理后台

- 用户管理
- 知识库管理
- 消息管理

## 快速开始

### 环境要求

- Node.js 16+
- Python 3.8+
- Docker (可选，用于生产部署)

### 开发环境启动

#### 前端启动

```bash
# 安装依赖
npm install

# 开发模式
npm run dev

# 构建生产版本
npm run build
```

#### 后端启动

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 启动服务
python start.py
```

### 生产环境部署

#### Docker部署（推荐）

```bash
# 一键部署
./deploy.sh prod

# 或手动部署
docker-compose -f docker-compose.prod.yml up -d
```

#### 传统部署

1. **配置环境变量**

   ```bash
   cp env.example env.production
   cp backend/env.example backend/.env
   ```

2. **配置API密钥**
   - 在 `backend/.env` 中设置 `DASHSCOPE_API_KEY`

3. **启动服务**

   ```bash
   # 后端
   cd backend && python start.py

   # 前端
   npm run build
   nginx -s reload
   ```

## 项目结构

```
Pre_hospital_assistant_front/
├── src/                    # 前端源码
│   ├── components/         # Vue组件
│   ├── views/             # 页面视图
│   ├── stores/            # 状态管理
│   ├── router/            # 路由配置
│   └── api/               # API接口
├── backend/               # 后端源码
│   ├── app/              # FastAPI应用
│   │   ├── api/          # API路由
│   │   ├── models/       # 数据模型
│   │   ├── schemas/      # 数据验证
│   │   └── services/     # 业务逻辑
│   └── requirements.txt   # Python依赖
├── docs/                  # 项目文档
├── nginx/                 # Nginx配置
└── docker-compose.yml     # Docker配置
```

## API文档

启动后端服务后，访问以下地址查看API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 配置说明

### 环境变量

#### 后端配置 (backend/.env)

```bash
# 应用配置
APP_NAME=院前急救助手系统
DEBUG=false

# 数据库配置
DATABASE_URL=sqlite:///./pre_hospital_assistant.db

# JWT 配置
SECRET_KEY=your-super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 通义千问 API 配置
DASHSCOPE_API_KEY=your-dashscope-api-key
QWEN_MODEL=qwen-plus
```

#### 前端配置 (env.production)

```bash
VITE_API_BASE_URL=http://your-domain.com:8000
VITE_APP_TITLE=院前急救助手系统
```

## 管理命令

### Docker管理

```bash
# 查看服务状态
docker-compose -f docker-compose.prod.yml ps

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f

# 重启服务
docker-compose -f docker-compose.prod.yml restart

# 停止服务
docker-compose -f docker-compose.prod.yml down
```

### 开发工具

```bash
# 代码检查
npm run lint

# 运行测试
npm run test

# 类型检查
npm run type-check
```

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

- 项目维护者: Daniel Potter
- 邮箱: danielpotter263@gmail.com
- 项目链接: [https://github.com/DanielPotter302/Intelligent-Assistant-for-Pre-Hospital-Emergencies]

## 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解详细更新历史。
