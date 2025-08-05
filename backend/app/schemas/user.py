from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """用户基础信息"""
    username: str
    email: EmailStr
    real_name: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None

class UserCreate(UserBase):
    """创建用户"""
    password: str

class UserUpdate(BaseModel):
    """更新用户"""
    real_name: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    profile_avatar: Optional[str] = None

class UserResponse(BaseModel):
    """用户响应"""
    id: str
    username: str
    email: str
    role: str
    real_name: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    profile_avatar: Optional[str] = None
    status: str
    email_verified: bool
    last_login_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True 