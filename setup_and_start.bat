@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM =============================================================================
REM 院前急救助手系统 - Windows完整启动脚本
REM Pre-hospital Emergency Assistant System - Windows Complete Setup Script
REM =============================================================================

echo.
echo ===============================================
echo 院前急救助手系统 - Windows启动脚本
echo Pre-hospital Emergency Assistant System
echo ===============================================
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [警告] 建议以管理员身份运行此脚本以获得最佳体验
    echo.
)

REM 1. 环境检查
echo [1/9] 检查系统环境...

REM 检查Node.js
node --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [错误] Node.js 未安装，请先安装 Node.js 16.0 或更高版本
    echo 下载地址: https://nodejs.org/
    pause
    exit /b 1
)

REM 检查npm
npm --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [错误] npm 未安装，请重新安装 Node.js
    pause
    exit /b 1
)

REM 检查Python
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [错误] Python 未安装，请先安装 Python 3.8 或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查pip
pip --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [错误] pip 未安装，请重新安装 Python
    pause
    exit /b 1
)

echo [成功] 环境检查通过
echo   Node.js: 
node --version
echo   Python: 
python --version
echo.

REM 2. 检查端口占用
echo [2/9] 检查端口占用情况...
netstat -an | findstr ":5173" >nul 2>&1
if %errorLevel% equ 0 (
    echo [警告] 端口 5173 已被占用，请手动关闭占用该端口的程序
)

netstat -an | findstr ":8000" >nul 2>&1
if %errorLevel% equ 0 (
    echo [警告] 端口 8000 已被占用，请手动关闭占用该端口的程序
)
echo [成功] 端口检查完成
echo.

REM 3. 创建必要目录
echo [3/9] 创建必要目录...
if not exist "backend\logs" mkdir "backend\logs"
if not exist "backend\uploads" mkdir "backend\uploads"
if not exist "uploads" mkdir "uploads"
echo [成功] 目录创建完成
echo.

REM 4. 配置环境变量
echo [4/9] 配置环境变量...

REM 配置后端环境变量
if not exist "backend\.env" (
    echo [信息] 创建后端环境配置文件...
    (
        echo # 后端环境配置
        echo # 应用配置
        echo APP_NAME=院前急救助手系统
        echo APP_VERSION=1.0.0
        echo DEBUG=true
        echo.
        echo # 服务器配置
        echo HOST=0.0.0.0
        echo PORT=8000
        echo.
        echo # 数据库配置
        echo DATABASE_URL=sqlite:///./pre_hospital_assistant.db
        echo.
        echo # JWT 配置
        echo SECRET_KEY=pre-hospital-assistant-super-secret-key-2024
        echo ALGORITHM=HS256
        echo ACCESS_TOKEN_EXPIRE_MINUTES=30
        echo REFRESH_TOKEN_EXPIRE_DAYS=7
        echo.
        echo # 通义千问 API 配置
        echo DASHSCOPE_API_KEY=sk-693ef3cef5b742c59ae610dec7295199
        echo DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
        echo QWEN_MODEL=qwen-plus
        echo QWEN_THINKING_MODEL=qwen-plus-2025-04-28
        echo.
        echo # Redis 配置（可选，用于缓存）
        echo REDIS_URL=redis://localhost:6379/0
        echo.
        echo # 文件上传配置
        echo UPLOAD_DIR=./uploads
        echo MAX_FILE_SIZE=10485760
        echo.
        echo # CORS 配置
        echo CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
        echo.
        echo # 日志配置
        echo LOG_LEVEL=INFO
        echo LOG_FILE=./logs/app.log
        echo.
        echo # 邮件配置（可选）
        echo SMTP_HOST=smtp.gmail.com
        echo SMTP_PORT=587
        echo SMTP_USERNAME=your-email@gmail.com
        echo SMTP_PASSWORD=your-app-password
        echo SMTP_FROM_EMAIL=your-email@gmail.com
    ) > "backend\.env"
    echo [成功] 后端环境配置文件创建完成
) else (
    echo [信息] 后端环境配置文件已存在，跳过创建
)

REM 配置前端环境变量
if not exist ".env.local" (
    echo [信息] 创建前端环境配置文件...
    (
        echo # 前端环境配置
        echo # API 基础地址
        echo VITE_API_BASE_URL=http://localhost:8000
        echo.
        echo # 应用配置
        echo VITE_APP_TITLE=院前急救助手系统
        echo VITE_APP_VERSION=1.0.0
        echo.
        echo # 开发模式配置
        echo VITE_DEV_PORT=5173
        echo.
        echo # 是否启用 Mock 数据（开发环境）
        echo VITE_USE_MOCK=false
        echo.
        echo # 日志级别
        echo VITE_LOG_LEVEL=info
    ) > ".env.local"
    echo [成功] 前端环境配置文件创建完成
) else (
    echo [信息] 前端环境配置文件已存在，跳过创建
)
echo.

REM 5. 安装依赖
echo [5/9] 安装项目依赖...

REM 安装前端依赖
echo [信息] 安装前端依赖...
call npm install
if %errorLevel% neq 0 (
    echo [错误] 前端依赖安装失败
    pause
    exit /b 1
)
echo [成功] 前端依赖安装完成

REM 安装后端依赖
echo [信息] 安装后端依赖...
cd backend

REM 检查是否存在虚拟环境
if not exist "venv" (
    echo [信息] 创建Python虚拟环境...
    python -m venv venv
    if %errorLevel% neq 0 (
        echo [错误] Python虚拟环境创建失败
        cd ..
        pause
        exit /b 1
    )
    echo [成功] Python虚拟环境创建完成
)

REM 激活虚拟环境并安装依赖
echo [信息] 激活虚拟环境并安装依赖...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorLevel% neq 0 (
    echo [错误] 后端依赖安装失败
    cd ..
    pause
    exit /b 1
)
echo [成功] 后端依赖安装完成

cd ..
echo.

REM 6. 初始化数据库
echo [6/9] 初始化数据库...
cd backend
call venv\Scripts\activate.bat

if not exist "pre_hospital_assistant.db" (
    echo [信息] 数据库不存在，正在初始化...
    python init_db.py
    if %errorLevel% neq 0 (
        echo [错误] 数据库初始化失败
        cd ..
        pause
        exit /b 1
    )
    echo [成功] 数据库初始化完成
    
    REM 初始化知识库数据
    if exist "init_knowledge.py" (
        if exist "classified_grouped_aggregated.txt" (
            echo [信息] 初始化知识库数据...
            python init_knowledge.py
            if %errorLevel% equ 0 (
                echo [成功] 知识库数据初始化完成
            ) else (
                echo [警告] 知识库数据初始化失败
            )
        ) else (
            echo [警告] 知识库数据文件不存在，跳过知识库初始化
        )
    ) else (
        echo [警告] 知识库初始化脚本不存在，跳过知识库初始化
    )
) else (
    echo [信息] 数据库已存在，检查是否需要初始化知识库...
    
    REM 检查知识库是否已初始化
    python -c "from app.core.database import SessionLocal; from app.models.knowledge import KnowledgeCategory; db = SessionLocal(); count = db.query(KnowledgeCategory).count(); db.close(); exit(0 if count > 0 else 1)" >nul 2>&1
    if %errorLevel% neq 0 (
        if exist "init_knowledge.py" (
            if exist "classified_grouped_aggregated.txt" (
                echo [信息] 知识库为空，正在初始化知识库数据...
                python init_knowledge.py
                if %errorLevel% equ 0 (
                    echo [成功] 知识库数据初始化完成
                ) else (
                    echo [警告] 知识库数据初始化失败
                )
            ) else (
                echo [警告] 知识库数据文件不存在，跳过知识库初始化
            )
        ) else (
            echo [警告] 知识库初始化脚本不存在，跳过知识库初始化
        )
    ) else (
        echo [信息] 知识库已存在，跳过初始化
    )
)

cd ..
echo.

REM 7. 创建启动脚本
echo [7/9] 创建服务启动脚本...

REM 创建后端启动脚本
(
    echo @echo off
    echo cd backend
    echo call venv\Scripts\activate.bat
    echo echo 启动后端服务 ^(端口: 8000^)...
    echo python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    echo pause
) > "start_backend.bat"

REM 创建前端启动脚本
(
    echo @echo off
    echo echo 启动前端服务 ^(端口: 5173^)...
    echo npm run dev -- --port 5173 --host 0.0.0.0
    echo pause
) > "start_frontend.bat"

REM 创建完整启动脚本
(
    echo @echo off
    echo chcp 65001 ^>nul
    echo echo.
    echo echo ===============================================
    echo echo 院前急救助手系统
    echo echo ===============================================
    echo echo.
    echo echo [信息] 正在启动所有服务...
    echo.
    echo echo [信息] 启动后端服务 ^(端口: 8000^)...
    echo cd backend
    echo call venv\Scripts\activate.bat
    echo start /B python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload ^> ..\backend.log 2^>^&1
    echo cd ..
    echo.
    echo echo [信息] 等待后端启动...
    echo timeout /t 10 /nobreak ^>nul
    echo.
    echo echo [信息] 启动前端服务 ^(端口: 5173^)...
    echo npm run dev -- --port 5173 --host 0.0.0.0
) > "start_all.bat"

REM 创建停止脚本
(
    echo @echo off
    echo echo 正在停止所有服务...
    echo.
    echo REM 停止占用端口的进程
    echo for /f "tokens=5" %%%%a in ^('netstat -aon ^| findstr ":8000"'^) do taskkill /f /pid %%%%a ^>nul 2^>^&1
    echo for /f "tokens=5" %%%%a in ^('netstat -aon ^| findstr ":5173"'^) do taskkill /f /pid %%%%a ^>nul 2^>^&1
    echo.
    echo echo 所有服务已停止
    echo pause
) > "stop_all.bat"

echo [成功] 启动脚本创建完成
echo.

REM 8. 显示系统信息
echo [8/9] 系统配置信息...
echo.
echo ===============================================
echo 系统配置信息
echo ===============================================
echo 前端地址: http://localhost:5173
echo 后端API: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo.
echo ===============================================
echo 默认用户账号
echo ===============================================
echo 管理员账号: admin / admin123
echo 普通用户账号: danielpotter / danielpotter123
echo.
echo ===============================================
echo 启动命令
echo ===============================================
echo 启动所有服务: start_all.bat
echo 只启动后端: start_backend.bat
echo 只启动前端: start_frontend.bat
echo 停止所有服务: stop_all.bat
echo.

REM 9. 自动启动所有服务
echo [9/9] 正在启动所有服务...
echo.
call start_all.bat

endlocal 