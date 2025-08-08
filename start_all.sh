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
