#!/usr/bin/env python3
"""
后端服务启动脚本
"""

import os
import sys
import uvicorn
from pathlib import Path

# 添加项目根目录到Python路径
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def main():
    """启动后端服务"""
    print("=== 院前急救助手系统后端 ===")
    print("正在启动服务...")
    
    # 检查是否需要初始化数据库
    db_file = backend_dir / "pre_hospital_assistant.db"
    if not db_file.exists():
        print("检测到数据库不存在，正在初始化...")
        try:
            from init_db import init_database
            init_database()
        except Exception as e:
            print(f"数据库初始化失败: {e}")
            return
    
    # 启动FastAPI服务
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n服务已停止")
    except Exception as e:
        print(f"服务启动失败: {e}")

if __name__ == "__main__":
    main() 