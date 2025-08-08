# 部署指南

## 📋 概述

本文档详细说明如何将院前急救助手系统部署到生产环境。系统支持多种部署方式，包括传统服务器部署、容器化部署和云平台部署。

## 🏗️ 系统架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   前端 (Vue3)    │    │   后端 (FastAPI) │    │   数据库 (SQLite)│
│   Port: 80/443   │────│   Port: 8000     │────│   本地文件       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
    ┌─────────┐            ┌─────────┐            ┌─────────┐
    │  Nginx  │            │ Gunicorn│            │ 文件系统 │
    │ 反向代理 │            │  WSGI   │            │  存储   │
    └─────────┘            └─────────┘            └─────────┘
```

## 🚀 快速部署

### 方式一：一键部署脚本

使用项目提供的部署脚本进行快速部署：

```bash
# 生产环境部署
chmod +x deploy_production.sh
./deploy_production.sh
```

### 方式二：手动部署

按照以下步骤进行手动部署。

## 📋 环境要求

### 服务器配置

**最低配置**:

- CPU: 2核
- 内存: 4GB
- 存储: 20GB
- 操作系统: Ubuntu 20.04+ / CentOS 8+ / RHEL 8+

**推荐配置**:

- CPU: 4核
- 内存: 8GB
- 存储: 50GB SSD
- 操作系统: Ubuntu 22.04 LTS

### 软件依赖

- **Node.js**: 18.0+
- **Python**: 3.9+
- **Nginx**: 1.18+
- **PM2**: 5.0+ (可选)
- **SSL证书**: Let's Encrypt 或商业证书

## 🔧 环境准备

### 1. 系统更新

```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/RHEL
sudo yum update -y
```

### 2. 安装Node.js

```bash
# 使用NodeSource仓库
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 验证安装
node --version
npm --version
```

### 3. 安装Python

```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip python3-venv -y

# CentOS/RHEL
sudo yum install python3 python3-pip -y

# 验证安装
python3 --version
pip3 --version
```

### 4. 安装Nginx

```bash
# Ubuntu/Debian
sudo apt install nginx -y

# CentOS/RHEL
sudo yum install nginx -y

# 启动并设置开机自启
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 5. 安装PM2 (可选)

```bash
sudo npm install -g pm2
```

## 📦 应用部署

### 1. 获取代码

```bash
# 克隆代码到服务器
git clone <repository_url> /opt/pre-hospital-assistant
cd /opt/pre-hospital-assistant

# 或者上传代码包
scp -r ./pre-hospital-assistant user@server:/opt/
```

### 2. 后端部署

```bash
cd /opt/pre-hospital-assistant/backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
nano .env
```

**生产环境配置 (.env)**:

```env
# 应用配置
APP_NAME=院前急救助手系统
APP_VERSION=1.0.0
DEBUG=false

# 服务器配置
HOST=127.0.0.1
PORT=8000

# 数据库配置
DATABASE_URL=sqlite:///./pre_hospital_assistant.db

# JWT 配置 (请修改为强密码)
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# 通义千问 API 配置
DASHSCOPE_API_KEY=your-dashscope-api-key
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
QWEN_MODEL=qwen-plus
QWEN_THINKING_MODEL=qwen-plus-2025-04-28

# CORS 配置
CORS_ORIGINS=["https://yourdomain.com"]

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# 文件上传配置
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760
```

```bash
# 初始化数据库
python init_db.py
python init_knowledge.py

# 测试启动
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

### 3. 前端构建

```bash
cd /opt/pre-hospital-assistant

# 安装依赖
npm install

# 配置生产环境变量
cp .env.example .env.production
nano .env.production
```

**生产环境配置 (.env.production)**:

```env
# API 基础地址
VITE_API_BASE_URL=https://yourdomain.com/api

# 应用配置
VITE_APP_TITLE=院前急救助手系统
VITE_APP_VERSION=1.0.0

# 生产模式配置
NODE_ENV=production
```

```bash
# 构建生产版本
npm run build

# 构建产物在 dist/ 目录
ls -la dist/
```

## 🌐 Nginx 配置

### 1. 创建站点配置

```bash
sudo nano /etc/nginx/sites-available/pre-hospital-assistant
```

**Nginx配置文件**:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # 重定向到HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL配置
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # 安全头
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # 前端静态文件
    location / {
        root /opt/pre-hospital-assistant/dist;
        index index.html;
        try_files $uri $uri/ /index.html;

        # 缓存配置
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # API代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # 超时配置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 健康检查
    location /health {
        proxy_pass http://127.0.0.1:8000/health;
        access_log off;
    }

    # 文件上传大小限制
    client_max_body_size 10M;

    # 日志配置
    access_log /var/log/nginx/pre-hospital-assistant.access.log;
    error_log /var/log/nginx/pre-hospital-assistant.error.log;
}
```

### 2. 启用站点

```bash
# 创建软链接
sudo ln -s /etc/nginx/sites-available/pre-hospital-assistant /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重载配置
sudo systemctl reload nginx
```

## 🔒 SSL证书配置

### 使用Let's Encrypt

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# 设置自动续期
sudo crontab -e
# 添加以下行
0 12 * * * /usr/bin/certbot renew --quiet
```

## 🔄 进程管理

### 使用Systemd

创建后端服务文件：

```bash
sudo nano /etc/systemd/system/pre-hospital-assistant.service
```

**服务配置**:

```ini
[Unit]
Description=Pre-hospital Assistant Backend
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/opt/pre-hospital-assistant/backend
Environment=PATH=/opt/pre-hospital-assistant/backend/venv/bin
ExecStart=/opt/pre-hospital-assistant/backend/venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8000 --workers 4
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
# 启动服务
sudo systemctl daemon-reload
sudo systemctl start pre-hospital-assistant
sudo systemctl enable pre-hospital-assistant

# 查看状态
sudo systemctl status pre-hospital-assistant
```

### 使用PM2 (可选)

```bash
cd /opt/pre-hospital-assistant/backend

# 创建PM2配置
cat > ecosystem.config.js << 'EOF'
module.exports = {
  apps: [{
    name: 'pre-hospital-assistant',
    script: 'venv/bin/python',
    args: '-m uvicorn main:app --host 127.0.0.1 --port 8000',
    instances: 4,
    exec_mode: 'cluster',
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production'
    }
  }]
}
EOF

# 启动应用
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## 📊 监控和日志

### 1. 日志配置

```bash
# 创建日志目录
sudo mkdir -p /var/log/pre-hospital-assistant
sudo chown www-data:www-data /var/log/pre-hospital-assistant

# 配置日志轮转
sudo nano /etc/logrotate.d/pre-hospital-assistant
```

**日志轮转配置**:

```
/var/log/pre-hospital-assistant/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload pre-hospital-assistant
    endscript
}
```

### 2. 监控脚本

```bash
# 创建健康检查脚本
sudo nano /opt/scripts/health-check.sh
```

```bash
#!/bin/bash
# 健康检查脚本

API_URL="http://127.0.0.1:8000/health"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $API_URL)

if [ $RESPONSE -eq 200 ]; then
    echo "$(date): API健康检查通过"
else
    echo "$(date): API健康检查失败，状态码: $RESPONSE"
    # 重启服务
    systemctl restart pre-hospital-assistant
fi
```

```bash
# 设置定时检查
sudo chmod +x /opt/scripts/health-check.sh
sudo crontab -e
# 添加以下行
*/5 * * * * /opt/scripts/health-check.sh >> /var/log/health-check.log 2>&1
```

## 🔐 安全配置

### 1. 防火墙配置

```bash
# 使用UFW
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw deny 8000  # 禁止直接访问后端端口
```

### 2. 文件权限

```bash
# 设置正确的文件权限
sudo chown -R www-data:www-data /opt/pre-hospital-assistant
sudo chmod -R 755 /opt/pre-hospital-assistant
sudo chmod 600 /opt/pre-hospital-assistant/backend/.env
```

### 3. 数据库安全

```bash
# 设置数据库文件权限
sudo chmod 600 /opt/pre-hospital-assistant/backend/pre_hospital_assistant.db
sudo chown www-data:www-data /opt/pre-hospital-assistant/backend/pre_hospital_assistant.db
```

## 📈 性能优化

### 1. 后端优化

- 使用多个Worker进程
- 启用Gzip压缩
- 配置连接池
- 使用Redis缓存（可选）

### 2. 前端优化

- 启用Gzip压缩
- 配置CDN（可选）
- 设置适当的缓存策略

### 3. 数据库优化

- 定期备份数据库
- 监控数据库大小
- 考虑迁移到PostgreSQL（大规模部署）

## 🔄 更新部署

### 1. 创建更新脚本

```bash
sudo nano /opt/scripts/update-app.sh
```

```bash
#!/bin/bash
# 应用更新脚本

APP_DIR="/opt/pre-hospital-assistant"
BACKUP_DIR="/opt/backups/$(date +%Y%m%d_%H%M%S)"

echo "开始更新应用..."

# 创建备份
mkdir -p $BACKUP_DIR
cp -r $APP_DIR $BACKUP_DIR/

# 停止服务
systemctl stop pre-hospital-assistant

# 更新代码
cd $APP_DIR
git pull origin main

# 更新后端依赖
cd backend
source venv/bin/activate
pip install -r requirements.txt

# 更新前端
cd ..
npm install
npm run build

# 重启服务
systemctl start pre-hospital-assistant
systemctl reload nginx

echo "应用更新完成"
```

## 🚨 故障排除

### 常见问题

1. **502 Bad Gateway**
   - 检查后端服务是否运行
   - 检查端口是否正确
   - 查看Nginx错误日志

2. **静态文件404**
   - 检查前端构建是否成功
   - 检查Nginx配置路径
   - 检查文件权限

3. **API请求失败**
   - 检查CORS配置
   - 检查API路径配置
   - 查看后端日志

### 日志查看

```bash
# 查看应用日志
sudo journalctl -u pre-hospital-assistant -f

# 查看Nginx日志
sudo tail -f /var/log/nginx/pre-hospital-assistant.error.log

# 查看系统日志
sudo tail -f /var/log/syslog
```

## 📞 技术支持

如果在部署过程中遇到问题，请：

1. 检查系统日志获取详细错误信息
2. 确认所有依赖都已正确安装
3. 验证配置文件格式和内容
4. 联系技术支持团队

---

**注意**: 生产环境部署前请务必修改所有默认密码和密钥，确保系统安全。
