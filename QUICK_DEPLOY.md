# 🚀 快速上线操作清单

## 📋 上线前准备

### ✅ 必需物品

- [ ] 云服务器（2核4GB以上）
- [ ] 阿里云通义千问API密钥
- [ ] 服务器公网IP

## 🖥️ 服务器操作步骤

### 1️⃣ 连接服务器

```bash
ssh root@your-server-ip
```

### 2️⃣ 安装Docker环境

```bash
# 一键安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 安装Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 启动Docker
systemctl start docker
systemctl enable docker
```

### 3️⃣ 上传项目

```bash
# 方式一：Git克隆（推荐）
git clone https://github.com/your-username/Pre_hospital_assistant_front.git
cd Pre_hospital_assistant_front

# 方式二：手动上传
# 在本地打包：tar -czf project.tar.gz Pre_hospital_assistant_front/
# 上传到服务器：scp project.tar.gz root@your-server-ip:/root/
# 在服务器解压：tar -xzf project.tar.gz && cd Pre_hospital_assistant_front
```

### 4️⃣ 配置环境变量

```bash
# 自动配置
./setup_env.sh

# 手动配置API密钥
nano backend/.env
# 找到：DASHSCOPE_API_KEY=your-dashscope-api-key-here
# 替换为：DASHSCOPE_API_KEY=sk-your-actual-api-key-here
```

### 5️⃣ 一键部署

```bash
# 生产环境部署
./deploy.sh prod
```

### 6️⃣ 验证部署

```bash
# 查看服务状态
docker ps

# 健康检查
curl http://localhost:8000/health

# 访问系统
# 前端：http://your-server-ip
# 后端：http://your-server-ip:8000
```

## 🔧 常用管理命令

### 查看状态

```bash
# 服务状态
docker-compose -f docker-compose.prod.yml ps

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f
```

### 重启服务

```bash
docker-compose -f docker-compose.prod.yml restart
```

### 停止服务

```bash
docker-compose -f docker-compose.prod.yml down
```

### 更新部署

```bash
git pull
./deploy.sh prod
```

## ⚠️ 重要提醒

1. **API密钥**：必须配置真实的通义千问API密钥
2. **防火墙**：确保开放80和8000端口
3. **备份**：定期备份数据库文件
4. **监控**：关注系统运行状态

## 🆘 遇到问题？

1. 查看日志：`docker-compose -f docker-compose.prod.yml logs -f`
2. 重启服务：`docker-compose -f docker-compose.prod.yml restart`
3. 重新部署：`./deploy.sh prod`

---

## 🎉 完成！

您的院前急救助手系统已成功上线！
访问地址：http://your-server-ip
