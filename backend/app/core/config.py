from pydantic_settings import BaseSettings
from typing import Optional, List
import os

class Settings(BaseSettings):
    # 应用配置
    app_name: str = "院前急救助手系统 API"
    app_version: str = "1.0.0"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8001
    
    # 数据库配置
    database_url: str = "sqlite:///./pre_hospital_assistant.db"
    
    # JWT配置
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # 通义千问API配置 - OpenAI兼容模式
    dashscope_api_key: str = "sk-693ef3cef5b742c59ae610dec7295199"
    dashscope_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    openai_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    
    # 模型配置
    qwen_model: str = "qwen-plus"
    qwen_thinking_model: str = "qwen-plus-2025-04-28"
    kb_model: str = "qwen-plus"  # 知识库检索模型（不开启思考）
    complex_model: str = "qwen-plus"  # 复杂问答模型（开启思考）
    
    # Redis配置
    redis_url: str = "redis://localhost:6379/0"
    
    # 文件上传配置
    upload_dir: str = "./uploads"
    max_file_size: int = 10485760  # 10MB
    
    # CORS配置
    cors_origins: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"]
    allowed_origins: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    
    # 日志配置
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"
    
    # SMTP配置
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = "your-email@gmail.com"
    smtp_password: str = "your-app-password"
    smtp_from_email: str = "your-email@gmail.com"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# 创建全局设置实例
settings = Settings()

# 确保上传目录存在
os.makedirs(settings.upload_dir, exist_ok=True) 