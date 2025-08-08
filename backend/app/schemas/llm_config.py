from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LLMConfigBase(BaseModel):
    """LLM配置基础模型"""
    module_name: str = Field(..., description="模块名称")
    display_name: str = Field(..., description="显示名称")
    api_key: str = Field(..., description="API密钥")
    base_url: str = Field(..., description="API基础URL")
    model_name: str = Field(..., description="模型名称")
    temperature: str = Field(default="0.7", description="温度参数")
    max_tokens: str = Field(default="2000", description="最大token数")
    is_enabled: bool = Field(default=True, description="是否启用")
    enable_thinking: bool = Field(default=False, description="是否启用思考功能")
    description: Optional[str] = Field(None, description="配置描述")

class LLMConfigCreate(LLMConfigBase):
    """创建LLM配置"""
    pass

class LLMConfigUpdate(BaseModel):
    """更新LLM配置"""
    display_name: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model_name: Optional[str] = None
    temperature: Optional[str] = None
    max_tokens: Optional[str] = None
    is_enabled: Optional[bool] = None
    enable_thinking: Optional[bool] = None
    description: Optional[str] = None

class LLMConfigResponse(LLMConfigBase):
    """LLM配置响应"""
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class LLMConfigListResponse(BaseModel):
    """LLM配置列表响应"""
    id: str
    module_name: str
    display_name: str
    model_name: str
    is_enabled: bool
    enable_thinking: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 