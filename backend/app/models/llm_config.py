from sqlalchemy import Column, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class LLMConfig(Base):
    """LLM配置模型"""
    __tablename__ = "llm_configs"
    
    id = Column(String, primary_key=True, index=True)
    module_name = Column(String(50), unique=True, nullable=False, index=True)  # 模块名称：chat_kb, chat_graph, triage, emergency_cpr, emergency_trauma, emergency_poisoning, emergency_burn
    display_name = Column(String(100), nullable=False)  # 显示名称
    api_key = Column(Text, nullable=False)  # API密钥
    base_url = Column(String(255), nullable=False)  # API基础URL
    model_name = Column(String(100), nullable=False)  # 模型名称
    temperature = Column(String(10), default="0.7")  # 温度参数
    max_tokens = Column(String(10), default="2000")  # 最大token数
    is_enabled = Column(Boolean, default=True)  # 是否启用
    enable_thinking = Column(Boolean, default=False)  # 是否启用思考功能
    description = Column(Text)  # 配置描述
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<LLMConfig(id={self.id}, module_name={self.module_name}, display_name={self.display_name})>" 