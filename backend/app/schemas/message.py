from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ContactMessageCreate(BaseModel):
    """创建留言请求"""
    name: str
    email: EmailStr
    content: str

class ContactMessageResponse(BaseModel):
    """留言响应"""
    id: str
    name: str
    email: str
    content: str
    status: str
    admin_reply: Optional[str] = None
    replied_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ContactMessageUpdate(BaseModel):
    """更新留言（管理员回复）"""
    admin_reply: str
    status: str = "replied" 