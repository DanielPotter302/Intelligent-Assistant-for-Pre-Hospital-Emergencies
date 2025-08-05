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
- **PostgreSQL** - 关系型数据库
- **OpenAI API** - AI对话服务
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
- PostgreSQL 12+

### 前端启动

```bash
# 安装依赖
npm install

# 开发模式
npm run dev

# 构建生产版本
npm run build
```

### 后端启动

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
uvicorn app.main:app --reload
```

### 数据库设置

```bash
# 创建数据库
createdb pre_hospital_assistant

# 运行迁移
alembic upgrade head
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
└── nginx/                 # Nginx配置
```

## API文档

启动后端服务后，访问以下地址查看API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 部署

### Docker部署

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d
```

### 生产环境配置

1. 配置环境变量
2. 设置数据库连接
3. 配置Nginx反向代理
4. 设置SSL证书

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
- 邮箱: [your-email@example.com]
- 项目链接: [https://github.com/DanielPotter302/Pre_hospital_assistant_front]

## 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解详细更新历史。
