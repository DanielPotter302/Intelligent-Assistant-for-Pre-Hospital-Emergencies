from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    """登录请求"""
    username: str
    password: str

class LoginResponse(BaseModel):
    """登录响应"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserResponse"

class RegisterRequest(BaseModel):
    """注册请求"""
    username: str
    password: str

class RefreshTokenRequest(BaseModel):
    """刷新令牌请求"""
    refresh_token: str

class RefreshTokenResponse(BaseModel):
    """刷新令牌响应"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int

# 避免循环导入
from .user import UserResponse
LoginResponse.model_rebuild() 