# 院前急救助手系统 - Docker 部署指南

## 📋 目录

- [系统要求](#系统要求)
- [快速开始](#快速开始)
- [环境配置](#环境配置)
- [部署方式](#部署方式)
- [生产环境部署](#生产环境部署)
- [开发环境部署](#开发环境部署)
- [监控和维护](#监控和维护)
- [故障排除](#故障排除)

## 🖥️ 系统要求

- Docker 20.10+
- Docker Compose 2.0+
- 至少 2GB 可用内存
- 至少 10GB 可用磁盘空间

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone <your-repository-url>
cd Pre_hospital_assistant_front
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp env.example env.production
cp backend/env.example backend/.env

# 编辑配置文件
nano env.production
nano backend/.env
```

### 3. 一键部署

```bash
# 生产环境部署
./deploy.sh prod

# 开发环境部署
./deploy.sh dev
```

## ⚙️ 环境配置

### 必需的环境变量

#### 后端配置 (backend/.env)

```bash
# 应用配置
APP_NAME=院前急救助手系统
APP_VERSION=1.0.0
DEBUG=false

# 服务器配置
HOST=0.0.0.0
PORT=8000

# 数据库配置
DATABASE_URL=sqlite:///./pre_hospital_assistant.db

# JWT 配置
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# 通义千问 API 配置
DASHSCOPE_API_KEY=your-dashscope-api-key-here
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
QWEN_MODEL=qwen-plus
QWEN_THINKING_MODEL=qwen-plus-2025-04-28

# Redis 配置
REDIS_URL=redis://redis:6379/0

# 文件上传配置
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760

# CORS 配置
CORS_ORIGINS=["http://localhost", "http://your-domain.com"]

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
```

#### 前端配置 (env.production)

```bash
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

## 🐳 部署方式

### 方式一：使用部署脚本（推荐）

```bash
# 生产环境
./deploy.sh prod

# 开发环境
./deploy.sh dev
```

### 方式二：手动部署

#### 生产环境

```bash
# 1. 构建并启动服务
docker-compose -f docker-compose.prod.yml up -d --build

# 2. 查看服务状态
docker-compose -f docker-compose.prod.yml ps

# 3. 查看日志
docker-compose -f docker-compose.prod.yml logs -f
```

#### 开发环境

```bash
# 1. 构建并启动服务
docker-compose -f docker-compose.dev.yml up -d --build

# 2. 查看服务状态
docker-compose -f docker-compose.dev.yml ps

# 3. 查看日志
docker-compose -f docker-compose.dev.yml logs -f
```

## 🌐 生产环境部署

### 1. 服务器准备

```bash
# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. 项目部署

```bash
# 克隆项目
git clone <your-repository-url>
cd Pre_hospital_assistant_front

# 配置环境变量
cp env.example env.production
cp backend/env.example backend/.env

# 编辑配置文件
nano env.production
nano backend/.env

# 部署
./deploy.sh prod
```

### 3. 域名配置（可选）

如果需要使用域名访问，请修改以下文件：

1. 编辑 `nginx/nginx.conf` 中的 `server_name`
2. 配置 SSL 证书
3. 更新 CORS 配置

### 4. 防火墙配置

```bash
# 开放必要端口
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 8000
```

## 🔧 开发环境部署

### 1. 本地开发

```bash
# 启动开发环境
./deploy.sh dev

# 访问地址
# 前端: http://localhost:5173
# 后端: http://localhost:8000
```

### 2. 热重载

开发环境支持热重载，修改代码后会自动重新加载。

## 📊 监控和维护

### 查看服务状态

```bash
# 查看所有容器状态
docker ps

# 查看特定服务状态
docker-compose -f docker-compose.prod.yml ps
```

### 查看日志

```bash
# 查看所有服务日志
docker-compose -f docker-compose.prod.yml logs -f

# 查看特定服务日志
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
```

### 健康检查

```bash
# 检查后端健康状态
curl http://localhost:8000/health

# 检查前端访问
curl http://localhost
```

### 数据备份

```bash
# 备份数据库
docker cp pre-hospital-backend:/app/pre_hospital_assistant.db ./backup/

# 备份上传文件
docker cp pre-hospital-backend:/app/uploads ./backup/
```

### 更新部署

```bash
# 拉取最新代码
git pull

# 重新部署
./deploy.sh prod
```

## 🔍 故障排除

### 常见问题

#### 1. 端口被占用

```bash
# 查看端口占用
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :8000

# 停止占用端口的进程
sudo kill -9 <PID>
```

#### 2. 容器启动失败

```bash
# 查看容器日志
docker logs pre-hospital-backend
docker logs pre-hospital-frontend

# 重新构建镜像
docker-compose -f docker-compose.prod.yml build --no-cache
```

#### 3. 数据库连接失败

```bash
# 检查数据库文件权限
ls -la backend/pre_hospital_assistant.db

# 重新初始化数据库
docker exec -it pre-hospital-backend python -c "from app.core.database import init_db; init_db()"
```

#### 4. Redis 连接失败

```bash
# 检查 Redis 容器状态
docker ps | grep redis

# 重启 Redis 服务
docker-compose -f docker-compose.prod.yml restart redis
```

### 日志分析

```bash
# 查看错误日志
docker-compose -f docker-compose.prod.yml logs --tail=100 | grep ERROR

# 查看访问日志
tail -f nginx/logs/access.log
```

### 性能优化

```bash
# 查看资源使用情况
docker stats

# 清理未使用的资源
docker system prune -a
```

## 📞 技术支持

如果遇到问题，请：

1. 查看日志文件
2. 检查环境变量配置
3. 确认网络连接
4. 联系技术支持团队

## 📝 更新日志

- v1.0.0: 初始版本发布
- 支持 Docker 容器化部署
- 支持开发和生产环境
- 集成 Redis 缓存
- 配置 Nginx 反向代理
