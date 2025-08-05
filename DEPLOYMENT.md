# 院前急救助手系统 - 部署指南

本文档提供了院前急救助手系统的详细部署指南，包括开发环境和生产环境的部署方法。

## 🚀 快速部署（开发环境）

### 1. 环境准备

确保您的系统已安装：

- Node.js 16+
- Python 3.8+
- Git

### 2. 克隆项目

```bash
git clone <your-repository-url>
cd Pre_hospital_assistant_front
```

### 3. 后端部署

```bash
# 进入后端目录
cd backend

# 安装Python依赖
pip install -r requirements.txt

# 启动后端服务
python start.py
```

后端服务将在 http://localhost:8000 启动，并自动初始化数据库。

### 4. 前端部署

```bash
# 回到项目根目录
cd ..

# 安装前端依赖
npm install

# 启动前端开发服务器
npm run dev
```

前端服务将在 http://localhost:5173 启动。

### 5. 验证部署

- 访问前端: http://localhost:5173
- 访问 API 文档: http://localhost:8000/docs
- 使用测试账号登录: `test` / `test123`

## 🏭 生产环境部署

### 方案一：Docker 部署（推荐）

#### 1. 创建 Docker 文件

**后端 Dockerfile** (`backend/Dockerfile`):

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "start.py"]
```

**前端 Dockerfile** (`Dockerfile`):

```dockerfile
# 构建阶段
FROM node:18-alpine as build-stage

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# 生产阶段
FROM nginx:alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### 2. 创建 docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - '8000:8000'
    environment:
      - DATABASE_URL=sqlite:///./pre_hospital_assistant.db
      - SECRET_KEY=your-production-secret-key
      - OPENAI_API_KEY=your-openai-api-key
    volumes:
      - ./backend/data:/app/data
    restart: unless-stopped

  frontend:
    build: .
    ports:
      - '80:80'
    depends_on:
      - backend
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - '443:443'
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped
```

#### 3. 部署命令

```bash
# 构建并启动服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 方案二：传统部署

#### 1. 后端部署

```bash
# 安装生产依赖
cd backend
pip install -r requirements.txt
pip install gunicorn

# 创建生产配置
cp .env.example .env
# 编辑.env文件，设置生产环境配置

# 使用gunicorn启动
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### 2. 前端部署

```bash
# 构建生产版本
npm run build

# 将dist目录部署到Web服务器
# 例如：复制到nginx的html目录
sudo cp -r dist/* /var/www/html/
```

#### 3. Nginx 配置

创建 `/etc/nginx/sites-available/pre-hospital-assistant`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /var/www/html;
        try_files $uri $uri/ /index.html;
    }

    # 后端API代理
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API文档
    location /docs {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

启用站点：

```bash
sudo ln -s /etc/nginx/sites-available/pre-hospital-assistant /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🔧 配置说明

### 环境变量配置

创建 `backend/.env` 文件：

```bash
# 应用配置
DEBUG=False
SECRET_KEY=your-very-secure-secret-key-here

# 数据库配置
DATABASE_URL=sqlite:///./pre_hospital_assistant.db
# 或使用PostgreSQL
# DATABASE_URL=postgresql://user:password@localhost:5432/pre_hospital_db

# JWT配置
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# OpenAI配置（可选）
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-3.5-turbo

# CORS配置
ALLOWED_ORIGINS=["https://your-domain.com", "https://www.your-domain.com"]
```

### 数据库配置

#### SQLite（默认）

- 适合小型部署
- 数据文件位于 `backend/pre_hospital_assistant.db`
- 无需额外配置

#### PostgreSQL（推荐生产环境）

```bash
# 安装PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# 创建数据库和用户
sudo -u postgres psql
CREATE DATABASE pre_hospital_db;
CREATE USER pre_hospital_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE pre_hospital_db TO pre_hospital_user;
\q

# 更新环境变量
DATABASE_URL=postgresql://pre_hospital_user:your_password@localhost:5432/pre_hospital_db
```

## 🔒 安全配置

### 1. HTTPS 配置

使用 Let's Encrypt 获取免费 SSL 证书：

```bash
# 安装certbot
sudo apt-get install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo crontab -e
# 添加：0 12 * * * /usr/bin/certbot renew --quiet
```

### 2. 防火墙配置

```bash
# 配置ufw防火墙
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 3. 安全头配置

在 Nginx 配置中添加安全头：

```nginx
# 安全头
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
```

## 📊 监控和日志

### 1. 应用监控

使用 systemd 管理后端服务：

创建 `/etc/systemd/system/pre-hospital-backend.service`:

```ini
[Unit]
Description=Pre-Hospital Assistant Backend
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/path/to/backend
Environment=PATH=/path/to/venv/bin
ExecStart=/path/to/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

启用服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable pre-hospital-backend
sudo systemctl start pre-hospital-backend
```

### 2. 日志配置

配置日志轮转 `/etc/logrotate.d/pre-hospital`:

```
/var/log/pre-hospital/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
}
```

## 🚀 性能优化

### 1. 前端优化

```bash
# 启用gzip压缩
# 在nginx配置中添加：
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

# 设置缓存头
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 2. 后端优化

```bash
# 使用更多worker进程
gunicorn main:app -w 8 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# 配置数据库连接池
# 在配置中设置合适的连接池大小
```

## 🔄 备份和恢复

### 1. 数据库备份

```bash
# SQLite备份
cp backend/pre_hospital_assistant.db backup/pre_hospital_assistant_$(date +%Y%m%d).db

# PostgreSQL备份
pg_dump -U pre_hospital_user -h localhost pre_hospital_db > backup/pre_hospital_db_$(date +%Y%m%d).sql
```

### 2. 自动备份脚本

创建 `/usr/local/bin/backup-pre-hospital.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/backup/pre-hospital"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
cp /path/to/backend/pre_hospital_assistant.db $BACKUP_DIR/db_$DATE.db

# 备份配置文件
cp /path/to/backend/.env $BACKUP_DIR/env_$DATE.bak

# 删除7天前的备份
find $BACKUP_DIR -name "*.db" -mtime +7 -delete
find $BACKUP_DIR -name "*.bak" -mtime +7 -delete

echo "Backup completed: $DATE"
```

添加到 crontab：

```bash
# 每天凌晨2点备份
0 2 * * * /usr/local/bin/backup-pre-hospital.sh
```

## 🆘 故障排除

### 常见问题

1. **服务无法启动**

   ```bash
   # 检查端口占用
   sudo netstat -tlnp | grep :8000

   # 检查服务状态
   sudo systemctl status pre-hospital-backend

   # 查看日志
   sudo journalctl -u pre-hospital-backend -f
   ```

2. **数据库连接失败**

   ```bash
   # 检查数据库文件权限
   ls -la backend/pre_hospital_assistant.db

   # 检查PostgreSQL状态
   sudo systemctl status postgresql
   ```

3. **前端无法访问后端**
   ```bash
   # 检查CORS配置
   # 检查nginx代理配置
   sudo nginx -t
   ```

### 性能问题

1. **响应慢**

   - 检查数据库查询性能
   - 增加 worker 进程数
   - 启用缓存

2. **内存使用高**
   - 调整 worker 进程数
   - 检查内存泄漏
   - 优化数据库查询

## 📞 技术支持

如遇到部署问题，请：

1. 检查系统日志
2. 查看应用日志
3. 确认配置文件
4. 联系技术支持团队

---

**注意**: 生产环境部署前，请务必：

- 更改默认密码和密钥
- 配置 HTTPS
- 设置防火墙
- 配置监控和备份
