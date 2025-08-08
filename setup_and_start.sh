#!/bin/bash

# =============================================================================
# 院前急救助手系统 - 完整启动脚本
# Pre-hospital Emergency Assistant System - Complete Setup Script
# =============================================================================

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        log_error "$1 未安装，请先安装 $1"
        exit 1
    fi
}

# 检查端口是否被占用
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        log_warning "端口 $port 已被占用，正在尝试释放..."
        # 尝试杀死占用端口的进程
        lsof -ti:$port | xargs kill -9 2>/dev/null || true
        sleep 2
    fi
}

# 创建目录
create_directory() {
    if [ ! -d "$1" ]; then
        mkdir -p "$1"
        log_info "创建目录: $1"
    fi
}

# 主函数
main() {
    log_info "=== 院前急救助手系统启动脚本 ==="
    log_info "开始环境检查和项目初始化..."

    # 1. 环境检查
    log_info "1. 检查系统环境..."
    check_command "node"
    check_command "npm"
    check_command "python3"
    check_command "pip3"
    
    # 检查Node.js版本
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 16 ]; then
        log_error "Node.js 版本过低，需要 16.0 或更高版本"
        exit 1
    fi
    log_success "Node.js 版本检查通过: $(node --version)"

    # 检查Python版本
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    log_success "Python 版本检查通过: $(python3 --version)"

    # 2. 检查和释放端口
    log_info "2. 检查端口占用情况..."
    check_port 5173  # 前端端口
    check_port 8000  # 后端端口
    log_success "端口检查完成"

    # 3. 创建必要目录
    log_info "3. 创建必要目录..."
    create_directory "backend/logs"
    create_directory "backend/uploads"
    create_directory "uploads"
    log_success "目录创建完成"

    # 4. 配置环境变量
    log_info "4. 配置环境变量..."
    
    # 配置后端环境变量
    if [ ! -f "backend/.env" ]; then
        log_info "创建后端环境配置文件..."
        cat > backend/.env << 'EOF'
# 后端环境配置
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

# Redis 配置（可选，用于缓存）
REDIS_URL=redis://localhost:6379/0

# 文件上传配置
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760

# CORS 配置
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# 邮件配置（可选）
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
EOF
        log_success "后端环境配置文件创建完成"
    else
        log_info "后端环境配置文件已存在，跳过创建"
    fi

    # 配置前端环境变量
    if [ ! -f ".env.local" ]; then
        log_info "创建前端环境配置文件..."
        cat > .env.local << 'EOF'
# 前端环境配置
# API 基础地址
VITE_API_BASE_URL=http://localhost:8000

# 应用配置
VITE_APP_TITLE=院前急救助手系统
VITE_APP_VERSION=1.0.0

# 开发模式配置
VITE_DEV_PORT=5173

# 是否启用 Mock 数据（开发环境）
VITE_USE_MOCK=false

# 日志级别
VITE_LOG_LEVEL=info
EOF
        log_success "前端环境配置文件创建完成"
    else
        log_info "前端环境配置文件已存在，跳过创建"
    fi

    # 5. 安装依赖
    log_info "5. 安装项目依赖..."
    
    # 安装前端依赖
    log_info "安装前端依赖..."
    npm install
    log_success "前端依赖安装完成"

    # 安装后端依赖
    log_info "安装后端依赖..."
    cd backend
    
    # 检查是否存在虚拟环境
    if [ ! -d "venv" ]; then
        log_info "创建Python虚拟环境..."
        python3 -m venv venv
        log_success "Python虚拟环境创建完成"
    fi
    
    # 激活虚拟环境并安装依赖
    log_info "激活虚拟环境并安装依赖..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    log_success "后端依赖安装完成"
    
    cd ..

    # 6. 初始化数据库
    log_info "6. 初始化数据库..."
    cd backend
    source venv/bin/activate
    
    if [ ! -f "pre_hospital_assistant.db" ]; then
        log_info "数据库不存在，正在初始化..."
        python3 init_db.py
        log_success "数据库初始化完成"
        
        # 初始化知识库数据
        if [ -f "init_knowledge.py" ] && [ -f "classified_grouped_aggregated.txt" ]; then
            log_info "初始化知识库数据..."
            python3 init_knowledge.py
            log_success "知识库数据初始化完成"
        else
            log_warning "知识库初始化文件不存在，跳过知识库初始化"
        fi
    else
        log_info "数据库已存在，检查是否需要初始化知识库..."
        
        # 检查知识库是否已初始化（通过检查是否有知识分类数据）
        KNOWLEDGE_CHECK=$(python3 -c "
from app.core.database import SessionLocal
from app.models.knowledge import KnowledgeCategory
db = SessionLocal()
try:
    count = db.query(KnowledgeCategory).count()
    print(count)
finally:
    db.close()
" 2>/dev/null || echo "0")
        
        if [ "$KNOWLEDGE_CHECK" -eq 0 ]; then
            if [ -f "init_knowledge.py" ] && [ -f "classified_grouped_aggregated.txt" ]; then
                log_info "知识库为空，正在初始化知识库数据..."
                python3 init_knowledge.py
                log_success "知识库数据初始化完成"
            else
                log_warning "知识库初始化文件不存在，跳过知识库初始化"
            fi
        else
            log_info "知识库已存在 ($KNOWLEDGE_CHECK 个分类)，跳过初始化"
        fi
    fi
    
    cd ..

    # 7. 创建启动脚本
    log_info "7. 创建服务启动脚本..."
    
    # 创建后端启动脚本
    cat > start_backend.sh << 'EOF'
#!/bin/bash
cd backend
source venv/bin/activate
echo "启动后端服务 (端口: 8000)..."
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
EOF
    chmod +x start_backend.sh

    # 创建前端启动脚本
    cat > start_frontend.sh << 'EOF'
#!/bin/bash
echo "启动前端服务 (端口: 5173)..."
npm run dev -- --port 5173 --host 0.0.0.0
EOF
    chmod +x start_frontend.sh

    # 创建完整启动脚本
    cat > start_all.sh << 'EOF'
#!/bin/bash

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== 院前急救助手系统 ===${NC}"
echo -e "${GREEN}正在启动所有服务...${NC}"

# 启动后端服务（后台运行）
echo -e "${GREEN}启动后端服务 (端口: 8000)...${NC}"
cd backend
source venv/bin/activate
nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload > ../backend.log 2>&1 &
echo $! > ../backend.pid
cd ..

# 等待后端启动
sleep 5

# 检查后端是否启动成功
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}后端服务启动成功！${NC}"
else
    echo -e "${RED}后端服务启动失败，请检查日志${NC}"
    exit 1
fi

# 启动前端服务
echo -e "${GREEN}启动前端服务 (端口: 5173)...${NC}"
npm run dev -- --port 5173 --host 0.0.0.0
EOF
    chmod +x start_all.sh

    # 创建停止脚本
    cat > stop_all.sh << 'EOF'
#!/bin/bash

echo "正在停止所有服务..."

# 停止后端服务
if [ -f "backend.pid" ]; then
    PID=$(cat backend.pid)
    if ps -p $PID > /dev/null; then
        kill $PID
        echo "后端服务已停止"
    fi
    rm -f backend.pid
fi

# 停止前端服务（通过端口）
FRONTEND_PID=$(lsof -ti:5173)
if [ ! -z "$FRONTEND_PID" ]; then
    kill $FRONTEND_PID
    echo "前端服务已停止"
fi

echo "所有服务已停止"
EOF
    chmod +x stop_all.sh

    log_success "启动脚本创建完成"

    # 8. 显示系统信息
    log_info "8. 系统配置信息..."
    echo ""
    echo "=== 系统配置信息 ==="
    echo "前端地址: http://localhost:5173"
    echo "后端API: http://localhost:8000"
    echo "API文档: http://localhost:8000/docs"
    echo ""
    echo "=== 默认用户账号 ==="
    echo "管理员账号: admin / admin123"
    echo "普通用户账号: danielpotter / danielpotter123"
    echo ""
    echo "=== 启动命令 ==="
    echo "启动所有服务: ./start_all.sh"
    echo "只启动后端: ./start_backend.sh"
    echo "只启动前端: ./start_frontend.sh"
    echo "停止所有服务: ./stop_all.sh"
    echo ""

    # 9. 自动启动所有服务
    log_info "正在启动所有服务..."
    ./start_all.sh
}

# 执行主函数
main "$@" 