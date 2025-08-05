# 🚀 院前急救助手系统 - 上线操作指南

## 📋 上线前准备清单

### ✅ 服务器要求

- [ ] 云服务器（推荐2核4GB以上）
- [ ] Ubuntu 20.04+ 或 CentOS 7+
- [ ] 公网IP地址
- [ ] 域名（可选，推荐配置）

### ✅ 必需配置

- [ ] 阿里云通义千问API密钥
- [ ] 域名解析（如果使用域名）

## 🖥️ 第一步：服务器环境准备

### 1.1 连接服务器

```bash
# SSH连接到您的服务器
ssh root@your-server-ip
```

### 1.2 运行环境准备脚本

```bash
# 下载并运行环境准备脚本
wget https://raw.githubusercontent.com/your-repo/Pre_hospital_assistant_front/main/server_setup.sh
chmod +x server_setup.sh
sudo ./server_setup.sh
```

### 1.3 验证Docker安装

```bash
# 重新登录或运行
newgrp docker

# 验证安装
docker --version
docker-compose --version
```

## 📁 第二步：上传项目代码

### 2.1 方式一：Git克隆（推荐）

```bash
# 克隆项目到服务器
git clone https://github.com/your-username/Pre_hospital_assistant_front.git
cd Pre_hospital_assistant_front
```

### 2.2 方式二：手动上传

```bash
# 在本地打包项目
tar -czf pre-hospital-assistant.tar.gz Pre_hospital_assistant_front/

# 上传到服务器
scp pre-hospital-assistant.tar.gz root@your-server-ip:/root/

# 在服务器解压
tar -xzf pre-hospital-assistant.tar.gz
cd Pre_hospital_assistant_front
```

## ⚙️ 第三步：配置环境变量

### 3.1 运行配置脚本

```bash
# 自动生成SECRET_KEY并创建配置文件
./setup_env.sh
```

### 3.2 配置API密钥

```bash
# 编辑后端配置文件
nano backend/.env

# 找到并修改这一行：
# DASHSCOPE_API_KEY=your-dashscope-api-key-here
# 替换为您的实际API密钥：
# DASHSCOPE_API_KEY=sk-your-actual-api-key-here
```

### 3.3 配置域名（可选）

```bash
# 编辑前端配置文件
nano env.production

# 修改API地址为您的域名：
# VITE_API_BASE_URL=http://your-domain.com:8000
```

## 🚀 第四步：部署系统

### 4.1 一键部署（推荐）

```bash
# 生产环境部署
./deploy.sh prod
```

### 4.2 手动部署

```bash
# 构建并启动服务
docker-compose -f docker-compose.prod.yml up -d --build

# 查看服务状态
docker-compose -f docker-compose.prod.yml ps
```

## ✅ 第五步：验证部署

### 5.1 检查服务状态

```bash
# 查看所有容器状态
docker ps

# 查看服务日志
docker-compose -f docker-compose.prod.yml logs -f
```

### 5.2 健康检查

```bash
# 检查后端健康状态
curl http://localhost:8000/health

# 检查前端访问
curl http://localhost
```

### 5.3 访问系统

- **前端地址**: http://your-server-ip
- **后端API**: http://your-server-ip:8000
- **健康检查**: http://your-server-ip:8000/health

## 🔧 常用管理命令

### 查看服务状态

```bash
# 查看所有服务
docker-compose -f docker-compose.prod.yml ps

# 查看特定服务日志
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
```

### 重启服务

```bash
# 重启所有服务
docker-compose -f docker-compose.prod.yml restart

# 重启特定服务
docker-compose -f docker-compose.prod.yml restart backend
```

### 停止服务

```bash
# 停止所有服务
docker-compose -f docker-compose.prod.yml down

# 停止并删除数据卷
docker-compose -f docker-compose.prod.yml down -v
```

### 更新部署

```bash
# 拉取最新代码
git pull

# 重新部署
./deploy.sh prod
```

## 📊 监控和维护

### 查看系统资源

```bash
# 查看容器资源使用
docker stats

# 查看磁盘使用
df -h

# 查看内存使用
free -h
```

### 数据备份

```bash
# 创建备份目录
mkdir -p /backup/$(date +%Y%m%d)

# 备份数据库
docker cp pre-hospital-backend:/app/pre_hospital_assistant.db /backup/$(date +%Y%m%d)/

# 备份上传文件
docker cp pre-hospital-backend:/app/uploads /backup/$(date +%Y%m%d)/
```

### 日志管理

```bash
# 查看错误日志
docker-compose -f docker-compose.prod.yml logs --tail=100 | grep ERROR

# 清理旧日志
docker system prune -f
```

## 🔒 安全配置

### 防火墙设置

```bash
# 只开放必要端口
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw deny 8000/tcp   # 关闭后端直接访问（通过Nginx代理）
```

### SSL证书配置（可选）

```bash
# 安装Certbot
apt-get install certbot python3-certbot-nginx

# 获取SSL证书
certbot --nginx -d your-domain.com

# 自动续期
crontab -e
# 添加：0 12 * * * /usr/bin/certbot renew --quiet
```

## 🆘 故障排除

### 常见问题

#### 1. 端口被占用

```bash
# 查看端口占用
netstat -tulpn | grep :80
netstat -tulpn | grep :8000

# 停止占用进程
kill -9 <PID>
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
# 检查数据库文件
ls -la backend/pre_hospital_assistant.db

# 重新初始化数据库
docker exec -it pre-hospital-backend python -c "from app.core.database import init_db; init_db()"
```

#### 4. API调用失败

```bash
# 检查API密钥配置
grep "DASHSCOPE_API_KEY" backend/.env

# 测试API连接
curl -X POST http://localhost:8000/api/chat/test
```

## 📞 技术支持

如果遇到问题：

1. **查看日志**: `docker-compose -f docker-compose.prod.yml logs -f`
2. **检查状态**: `docker-compose -f docker-compose.prod.yml ps`
3. **重启服务**: `docker-compose -f docker-compose.prod.yml restart`
4. **重新部署**: `./deploy.sh prod`

## 🎉 上线完成！

恭喜！您的院前急救助手系统已经成功上线。

**访问地址**：

- 前端：http://your-server-ip
- 后端API：http://your-server-ip:8000

**下一步**：

1. 配置域名解析（可选）
2. 设置SSL证书（可选）
3. 配置监控告警（可选）
4. 定期备份数据
5. 监控系统运行状态
