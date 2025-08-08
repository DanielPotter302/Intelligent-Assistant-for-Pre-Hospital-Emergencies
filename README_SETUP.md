# 院前急救助手系统 - 完整启动指南

## 📋 项目概述

院前急救助手系统是一个基于Vue 3 + FastAPI的全栈Web应用，提供智能问答、智能分诊、应急指导等功能，集成通义千问LLM提供AI能力。

### 🏗️ 技术架构

**前端技术栈：**

- Vue 3 + TypeScript + Vite
- Element Plus UI框架
- Tailwind CSS
- 端口：5173

**后端技术栈：**

- FastAPI + Python 3.8+
- SQLite数据库
- 通义千问LLM (OpenAI兼容模式)
- 端口：8000

## 🚀 快速启动

### 方式一：一键启动脚本（推荐）

#### Linux/macOS 系统

```bash
# 给脚本执行权限
chmod +x setup_and_start.sh

# 运行启动脚本
./setup_and_start.sh
```

#### Windows 系统

```cmd
# 双击运行或在命令行执行
setup_and_start.bat
```

### 方式二：手动启动

#### 1. 环境要求

- **Node.js**: 16.0+
- **Python**: 3.8+
- **npm**: 最新版本
- **pip**: 最新版本

#### 2. 安装依赖

**前端依赖：**

```bash
npm install
```

**后端依赖：**

```bash
cd backend
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

#### 3. 环境配置

**后端环境配置 (backend/.env)：**

```env
# 应用配置
APP_NAME=院前急救助手系统
APP_VERSION=1.0.0
DEBUG=true

# 服务器配置
HOST=0.0.0.0
PORT=8000

# 数据库配置
DATABASE_URL=sqlite:///./pre_hospital_assistant.db

# JWT 配置
SECRET_KEY=pre-hospital-assistant-super-secret-key-2024
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# 通义千问 API 配置
DASHSCOPE_API_KEY=sk-693ef3cef5b742c59ae610dec7295199
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
QWEN_MODEL=qwen-plus
QWEN_THINKING_MODEL=qwen-plus-2025-04-28

# 文件上传配置
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760

# CORS 配置
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
```

**前端环境配置 (.env.local)：**

```env
# API 基础地址
VITE_API_BASE_URL=http://localhost:8000

# 应用配置
VITE_APP_TITLE=院前急救助手系统
VITE_APP_VERSION=1.0.0

# 开发模式配置
VITE_DEV_PORT=5173

# 是否启用 Mock 数据
VITE_USE_MOCK=false

# 日志级别
VITE_LOG_LEVEL=info
```

#### 4. 数据库初始化

```bash
cd backend
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

python init_db.py
python init_knowledge.py  # 可选：初始化知识库数据
```

#### 5. 启动服务

**启动后端服务：**

```bash
cd backend
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**启动前端服务：**

```bash
npm run dev -- --port 5173 --host 0.0.0.0
```

## 📁 项目结构

```
院前急救助手系统/
├── frontend/                 # 前端项目
│   ├── src/                 # 源代码
│   ├── public/              # 静态资源
│   ├── package.json         # 前端依赖配置
│   └── .env.local          # 前端环境配置
├── backend/                 # 后端项目
│   ├── app/                # 应用代码
│   ├── venv/               # Python虚拟环境
│   ├── uploads/            # 文件上传目录
│   ├── logs/               # 日志目录
│   ├── requirements.txt    # Python依赖
│   ├── .env               # 后端环境配置
│   ├── main.py            # 主应用文件
│   ├── init_db.py         # 数据库初始化
│   ├── init_knowledge.py  # 知识库初始化
│   ├── classified_grouped_aggregated.txt  # 知识库数据文件
│   └── pre_hospital_assistant.db  # SQLite数据库
├── setup_and_start.sh      # Linux/macOS启动脚本
├── setup_and_start.bat     # Windows启动脚本
├── start_all.sh           # 启动所有服务 (Linux/macOS)
├── start_all.bat          # 启动所有服务 (Windows)
├── start_backend.sh       # 只启动后端 (Linux/macOS)
├── start_backend.bat      # 只启动后端 (Windows)
├── start_frontend.sh      # 只启动前端 (Linux/macOS)
├── start_frontend.bat     # 只启动前端 (Windows)
├── stop_all.sh           # 停止所有服务 (Linux/macOS)
└── stop_all.bat          # 停止所有服务 (Windows)
```

## 🔧 配置说明

### 端口配置

- **前端端口**: 5173 (固定)
- **后端端口**: 8000 (固定)

### 数据库配置

- **类型**: SQLite
- **文件位置**: `backend/pre_hospital_assistant.db`
- **自动初始化**: 首次运行时自动创建

### 知识库配置

- **知识库文件**: `backend/classified_grouped_aggregated.txt`
- **总分类数**: 8个专业分类
- **知识条目**: 515条急救知识
- **分类包括**:
  - 中毒处理 (42条)
  - 创伤与现场急救处理 (98条)
  - 呼吸系统急救 (68条)
  - 妇产儿急救 (21条)
  - 循环系统与心脏急救 (75条)
  - 消化系统与出血 (27条)
  - 神经系统与意识障碍 (50条)
  - 通用急救与支持治疗 (134条)

### LLM配置

- **模型提供商**: 阿里云通义千问
- **API模式**: OpenAI兼容模式
- **主要模型**: qwen-plus
- **思考模型**: qwen-plus-2025-04-28

### 默认用户账号

- **管理员**: admin / admin123
- **普通用户**: danielpotter / danielpotter123

## 🌐 访问地址

启动成功后，您可以通过以下地址访问系统：

- **前端应用**: http://localhost:5173
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

## 📝 启动脚本说明

### 自动化启动脚本功能

1. **环境检查**: 检查Node.js、Python、npm、pip是否安装
2. **端口检查**: 检查5173和8000端口是否被占用
3. **目录创建**: 自动创建必要的目录结构
4. **环境配置**: 自动生成前端和后端的环境配置文件
5. **依赖安装**: 自动安装前端和后端依赖
6. **数据库初始化**: 自动初始化SQLite数据库和默认数据
7. **服务启动**: 可选择立即启动所有服务

### 可用的启动脚本

| 脚本名称                 | 功能描述                 | 适用系统    |
| ------------------------ | ------------------------ | ----------- |
| `setup_and_start.sh`     | 完整的环境配置和启动脚本 | Linux/macOS |
| `setup_and_start.bat`    | 完整的环境配置和启动脚本 | Windows     |
| `start_all.sh/.bat`      | 启动前端和后端服务       | 所有系统    |
| `start_backend.sh/.bat`  | 只启动后端服务           | 所有系统    |
| `start_frontend.sh/.bat` | 只启动前端服务           | 所有系统    |
| `stop_all.sh/.bat`       | 停止所有服务             | 所有系统    |

## 🔍 故障排除

### 常见问题

#### 1. 端口被占用

```bash
# 查看端口占用情况
netstat -tulpn | grep :8000  # Linux
netstat -ano | findstr :8000  # Windows

# 杀死占用端口的进程
kill -9 <PID>  # Linux
taskkill /f /pid <PID>  # Windows
```

#### 2. Python虚拟环境问题

```bash
# 删除现有虚拟环境
rm -rf backend/venv  # Linux/macOS
rmdir /s backend\venv  # Windows

# 重新创建虚拟环境
cd backend
python -m venv venv
```

#### 3. 数据库初始化失败

```bash
# 删除现有数据库
rm backend/pre_hospital_assistant.db  # Linux/macOS
del backend\pre_hospital_assistant.db  # Windows

# 重新初始化
cd backend
python init_db.py
```

#### 4. 前端依赖安装失败

```bash
# 清除npm缓存
npm cache clean --force

# 删除node_modules重新安装
rm -rf node_modules package-lock.json  # Linux/macOS
rmdir /s node_modules && del package-lock.json  # Windows
npm install
```

### 日志查看

- **后端日志**: `backend.log`
- **前端日志**: 控制台输出
- **应用日志**: `backend/logs/app.log`

## 🔒 安全注意事项

1. **生产环境部署时请修改以下配置**：
   - JWT密钥 (`SECRET_KEY`)
   - 数据库连接字符串
   - CORS允许的域名
   - 通义千问API密钥

2. **建议使用HTTPS**：
   - 配置SSL证书
   - 修改前端API地址为HTTPS

3. **数据库安全**：
   - 生产环境建议使用PostgreSQL或MySQL
   - 定期备份数据库

## 📞 技术支持

如果您在使用过程中遇到问题，请：

1. 检查日志文件获取详细错误信息
2. 确认环境要求是否满足
3. 参考故障排除部分
4. 联系技术支持团队

---

**祝您使用愉快！** 🎉
