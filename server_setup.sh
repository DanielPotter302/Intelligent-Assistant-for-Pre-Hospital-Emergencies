#!/bin/bash

# 服务器环境准备脚本
echo "🖥️  准备服务器环境..."

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  请使用 sudo 运行此脚本"
    exit 1
fi

# 更新系统
echo "📦 更新系统包..."
apt-get update && apt-get upgrade -y

# 安装必要的工具
echo "🔧 安装必要工具..."
apt-get install -y curl wget git nano

# 安装Docker
echo "🐳 安装Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 启动Docker服务
systemctl start docker
systemctl enable docker

# 安装Docker Compose
echo "📦 安装Docker Compose..."
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 创建docker用户组并添加当前用户
usermod -aG docker $SUDO_USER

# 配置防火墙（可选）
echo "🔥 配置防火墙..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 8000/tcp
ufw --force enable

echo "✅ 服务器环境准备完成！"
echo ""
echo "📝 请重新登录或运行以下命令使docker组权限生效："
echo "   newgrp docker"
echo ""
echo "🔍 验证安装："
echo "   docker --version"
echo "   docker-compose --version" 