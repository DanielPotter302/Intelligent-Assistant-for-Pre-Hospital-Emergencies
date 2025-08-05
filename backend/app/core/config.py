from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # 应用配置
    app_name: str = "院前急救助手系统 API"
    debug: bool = True
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # 数据库配置
    database_url: str = "sqlite:///./pre_hospital_assistant.db"
    
    # JWT配置
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # 通义千问API配置 - OpenAI兼容模式
    dashscope_api_key: str = "sk-693ef3cef5b742c59ae610dec7295199"
    openai_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    
    # 模型配置
    kb_model: str = "qwen-plus"  # 知识库检索模型（不开启思考）
    complex_model: str = "qwen-plus"  # 复杂问答模型（开启思考）
    
    # 文件上传配置
    upload_dir: str = "./uploads"
    max_file_size: int = 10485760  # 10MB
    
    # CORS配置
    allowed_origins: list = ["http://localhost:5173", "http://127.0.0.1:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# 创建全局设置实例
settings = Settings()

# 确保上传目录存在
os.makedirs(settings.upload_dir, exist_ok=True) 