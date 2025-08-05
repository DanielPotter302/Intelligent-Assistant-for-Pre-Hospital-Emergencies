from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class ChatMessageCreate(BaseModel):
    """创建聊天消息"""
    content: str
    session_id: Optional[str] = None
    mode: Optional[str] = "kb"  # 添加模式字段，用于自动创建会话

class ChatMessageResponse(BaseModel):
    """聊天消息响应"""
    id: str
    role: str  # user, assistant
    content: str
    references: Optional[List[Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ChatSessionCreate(BaseModel):
    """创建聊天会话"""
    title: str
    mode: str = "kb"  # kb, graph

class ChatSessionResponse(BaseModel):
    """聊天会话响应"""
    id: str
    title: str
    mode: str
    created_at: datetime
    updated_at: datetime
    message_count: Optional[int] = 0

    class Config:
        from_attributes = True

class ChatSessionWithMessages(ChatSessionResponse):
    """包含消息的聊天会话"""
    messages: List[ChatMessageResponse] = [] 