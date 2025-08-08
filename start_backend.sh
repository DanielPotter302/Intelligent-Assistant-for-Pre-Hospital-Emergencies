#!/bin/bash
cd backend
source venv/bin/activate
echo "启动后端服务 (端口: 8000)..."
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
