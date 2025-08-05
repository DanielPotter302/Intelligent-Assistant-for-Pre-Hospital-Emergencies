from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from datetime import datetime
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建FastAPI应用
app = FastAPI(
    title="院前急救助手系统 API",
    description="Pre-hospital Emergency Assistant System API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 导入路由
from app.api.routes import auth, chat, triage, emergency, knowledge, system, users, messages

# 静态文件配置
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(users.router, prefix="/api/users", tags=["用户"])
app.include_router(chat.router, prefix="/api/chat", tags=["智能问答"])
app.include_router(triage.router, prefix="/api/triage", tags=["智能分诊"])
app.include_router(emergency.router, prefix="/api/emergency", tags=["应急指导"])
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["知识库"])
app.include_router(messages.router, prefix="/api", tags=["留言管理"])
app.include_router(system.router, prefix="/api", tags=["系统"])

# 根路径
@app.get("/")
async def root():
    return {
        "message": "院前急救助手系统 API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "docs": "/docs"
    }

# 健康检查
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "pre-hospital-assistant-api"
    }

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "内部服务器错误",
            "data": None,
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 