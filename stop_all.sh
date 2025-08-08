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
