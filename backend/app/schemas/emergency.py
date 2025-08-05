from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class EmergencyScenario(BaseModel):
    """应急场景"""
    id: str
    title: str
    description: str
    icon: str
    category: str

class EmergencySessionCreate(BaseModel):
    """创建应急会话"""
    scenario_type: str
    title: str

class EmergencySessionResponse(BaseModel):
    """应急会话响应"""
    id: str
    scenario_type: str
    title: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EmergencyMessageCreate(BaseModel):
    """创建应急消息"""
    content: str

class EmergencyMessageResponse(BaseModel):
    """应急消息响应"""
    id: str
    role: str  # user, assistant
    content: str
    steps: Optional[List[str]] = None
    equipment: Optional[List[str]] = None
    created_at: datetime

    class Config:
        from_attributes = True

class EmergencySessionWithMessages(EmergencySessionResponse):
    """包含消息的应急会话"""
    messages: List[EmergencyMessageResponse] = [] 