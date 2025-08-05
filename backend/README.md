# 院前急救助手系统 - 后端 API

基于 FastAPI 的院前急救助手系统后端服务，提供智能分诊、应急指导、知识库管理等功能。

## 功能特性

- 🔐 **用户认证系统** - JWT 令牌认证，支持注册/登录
- 🤖 **智能问答** - 基于 AI 的医疗知识问答
- 🏥 **智能分诊** - AI 辅助患者分诊分析
- 🚑 **应急指导** - 紧急情况处理指导
- 📚 **知识库** - 医疗文档、视频资源管理
- 📊 **系统监控** - 健康检查和系统状态

## 技术栈

- **FastAPI** - 现代高性能 Web 框架
- **SQLAlchemy** - ORM 数据库操作
- **SQLite** - 轻量级数据库（可切换 PostgreSQL）
- **JWT** - 身份认证
- **OpenAI API** - AI 功能支持（可选）
- **Pydantic** - 数据验证

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 启动服务

```bash
# 方式1：使用启动脚本（推荐）
python start.py

# 方式2：直接启动
python main.py

# 方式3：使用uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. 初始化数据库（可选）

如果需要手动初始化数据库：

```bash
python init_db.py
```

## 默认账号

系统会自动创建以下测试账号：

- **管理员**: `admin` / `admin123`
- **测试用户**: `test` / `test123`

## API 文档

启动服务后访问：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 主要 API 端点

### 认证相关

- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/refresh` - 刷新令牌

### 用户管理

- `GET /api/users/profile` - 获取用户信息
- `PUT /api/users/profile` - 更新用户信息

### 智能问答

- `GET /api/chat/sessions` - 获取聊天会话
- `POST /api/chat/sessions` - 创建聊天会话
- `POST /api/chat/sessions/{id}/messages` - 发送消息

### 智能分诊

- `POST /api/triage/analyze` - AI 分诊分析
- `GET /api/triage/history` - 分诊历史

### 应急指导

- `GET /api/emergency/scenarios` - 应急场景
- `POST /api/emergency/sessions` - 创建应急会话

### 知识库

- `GET /api/knowledge/categories` - 知识分类
- `GET /api/knowledge/items` - 知识内容

### 系统功能

- `GET /api/features` - 系统功能
- `GET /api/workflows` - 工作流程
- `GET /api/health` - 健康检查

## 配置说明

### 环境变量

可以通过环境变量或`.env`文件配置：

```bash
# 数据库配置
DATABASE_URL=sqlite:///./pre_hospital_assistant.db

# JWT配置
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI配置（可选）
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-3.5-turbo
```

### 数据库

默认使用 SQLite 数据库，数据文件位于 `pre_hospital_assistant.db`。

如需使用 PostgreSQL，修改 `DATABASE_URL`：

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

## 项目结构

```
backend/
├── app/
│   ├── api/
│   │   └── routes/          # API路由
│   ├── core/
│   │   ├── config.py        # 配置管理
│   │   ├── database.py      # 数据库连接
│   │   ├── security.py      # 安全相关
│   │   └── deps.py          # 依赖注入
│   ├── models/              # 数据模型
│   ├── schemas/             # Pydantic模式
│   └── services/            # 业务逻辑
├── main.py                  # FastAPI应用
├── start.py                 # 启动脚本
├── init_db.py              # 数据库初始化
└── requirements.txt         # 依赖列表
```

## 开发说明

### 添加新功能

1. 在 `models/` 中定义数据模型
2. 在 `schemas/` 中定义 API 模式
3. 在 `services/` 中实现业务逻辑
4. 在 `api/routes/` 中创建 API 路由
5. 在 `main.py` 中注册路由

### 数据库迁移

如果修改了数据模型，需要重新初始化数据库：

```bash
rm pre_hospital_assistant.db
python init_db.py
```

## 部署

### Docker 部署（推荐）

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "start.py"]
```

### 生产环境

```bash
# 使用gunicorn
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 故障排除

### 常见问题

1. **数据库连接失败**

   - 检查数据库文件权限
   - 确认 DATABASE_URL 配置正确

2. **AI 功能不可用**

   - 检查 OPENAI_API_KEY 配置
   - 系统会自动降级到模拟响应

3. **端口占用**
   - 修改启动端口：`uvicorn main:app --port 8001`

### 日志查看

服务运行时会输出详细日志，包括：

- API 请求日志
- 数据库操作日志
- 错误信息

## 许可证

MIT License

## 联系方式

如有问题请联系开发团队。
