#!/bin/bash

# 院前急救助手系统快速启动脚本

echo "🚀 启动院前急救助手系统..."

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker 未运行，请先启动 Docker"
    exit 1
fi

# 创建必要的目录
mkdir -p backend/uploads
mkdir -p backend/logs
mkdir -p nginx/logs

# 检查环境变量文件
if [ ! -f "backend/.env" ]; then
    echo "📝 创建后端环境变量文件..."
    cp backend/env.example backend/.env
    echo "⚠️  请编辑 backend/.env 文件，配置必要的环境变量"
fi

# 启动服务
echo "🐳 启动 Docker 服务..."
docker-compose up -d --build

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "📊 检查服务状态..."
docker-compose ps

echo ""
echo "✅ 系统启动完成！"
echo ""
echo "🌐 前端访问地址: http://localhost"
echo "🔧 后端API地址: http://localhost:8000"
echo "📊 健康检查: http://localhost:8000/health"
echo ""
echo "📝 查看日志: docker-compose logs -f"
echo "🛑 停止服务: docker-compose down" 