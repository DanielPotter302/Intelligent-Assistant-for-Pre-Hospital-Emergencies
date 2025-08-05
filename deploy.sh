#!/bin/bash

# 院前急救助手系统部署脚本
# 使用方法: ./deploy.sh [dev|prod]

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Docker是否安装
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose 未安装，请先安装 Docker Compose"
        exit 1
    fi
    
    print_message "Docker 环境检查通过"
}

# 检查环境变量文件
check_env_files() {
    if [ ! -f "env.production" ]; then
        print_warning "未找到 env.production 文件，将使用默认配置"
        cp env.example env.production
    fi
    
    if [ ! -f "backend/.env" ]; then
        print_warning "未找到 backend/.env 文件，将使用默认配置"
        cp backend/env.example backend/.env
    fi
}

# 创建必要的目录
create_directories() {
    print_message "创建必要的目录..."
    mkdir -p backend/uploads
    mkdir -p backend/logs
    mkdir -p nginx/logs
    mkdir -p nginx/ssl
}

# 停止现有容器
stop_containers() {
    print_message "停止现有容器..."
    docker-compose -f docker-compose.prod.yml down || true
    docker-compose -f docker-compose.dev.yml down || true
}

# 清理旧镜像
cleanup_images() {
    print_message "清理旧镜像..."
    docker system prune -f
}

# 构建镜像
build_images() {
    print_message "构建 Docker 镜像..."
    if [ "$1" = "prod" ]; then
        docker-compose -f docker-compose.prod.yml build --no-cache
    else
        docker-compose -f docker-compose.dev.yml build --no-cache
    fi
}

# 启动服务
start_services() {
    print_message "启动服务..."
    if [ "$1" = "prod" ]; then
        docker-compose -f docker-compose.prod.yml up -d
    else
        docker-compose -f docker-compose.dev.yml up -d
    fi
}

# 检查服务状态
check_services() {
    print_message "检查服务状态..."
    sleep 10
    
    if [ "$1" = "prod" ]; then
        docker-compose -f docker-compose.prod.yml ps
    else
        docker-compose -f docker-compose.dev.yml ps
    fi
    
    print_message "检查健康状态..."
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_message "后端服务健康检查通过"
    else
        print_warning "后端服务健康检查失败，请检查日志"
    fi
}

# 显示访问信息
show_access_info() {
    echo ""
    print_message "部署完成！"
    echo ""
    if [ "$1" = "prod" ]; then
        echo "🌐 前端访问地址: http://localhost"
        echo "🔧 后端API地址: http://localhost:8000"
        echo "📊 健康检查: http://localhost:8000/health"
    else
        echo "🌐 前端访问地址: http://localhost:5173"
        echo "🔧 后端API地址: http://localhost:8000"
        echo "📊 健康检查: http://localhost:8000/health"
    fi
    echo ""
    print_message "查看日志: docker-compose -f docker-compose.$1.yml logs -f"
    print_message "停止服务: docker-compose -f docker-compose.$1.yml down"
}

# 主函数
main() {
    local environment=${1:-prod}
    
    if [ "$environment" != "dev" ] && [ "$environment" != "prod" ]; then
        print_error "无效的环境参数，请使用 'dev' 或 'prod'"
        echo "使用方法: $0 [dev|prod]"
        exit 1
    fi
    
    print_message "开始部署院前急救助手系统 ($environment 环境)..."
    
    check_docker
    check_env_files
    create_directories
    stop_containers
    cleanup_images
    build_images "$environment"
    start_services "$environment"
    check_services "$environment"
    show_access_info "$environment"
}

# 执行主函数
main "$@" 