from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.security import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    create_refresh_token,
    verify_token,
    generate_user_id
)
from app.core.config import settings
from app.models.user import User
from app.schemas.auth import (
    LoginRequest, 
    LoginResponse, 
    RegisterRequest, 
    RefreshTokenRequest, 
    RefreshTokenResponse
)
from app.schemas.user import UserResponse
from app.schemas.common import ApiResponse

router = APIRouter()

@router.post("/register", response_model=ApiResponse)
async def register(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """用户注册"""
    # 检查用户名是否已存在
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # 创建新用户
    user = User(
        id=generate_user_id(),
        username=user_data.username,
        email=f"{user_data.username}@example.com",  # 自动生成邮箱
        hashed_password=get_password_hash(user_data.password),
        role="user",
        status="active",
        email_verified=False
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return ApiResponse(
        code=201,
        message="User registered successfully",
        data={
            "userId": user.id,
            "username": user.username,
            "role": user.role,
            "createdAt": user.created_at.isoformat()
        }
    )

@router.post("/login", response_model=ApiResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """用户登录"""
    # 查找用户（支持用户名或邮箱登录）
    user = db.query(User).filter(
        (User.username == login_data.username) | 
        (User.email == login_data.username)
    ).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is inactive"
        )
    
    # 更新最后登录时间
    user.last_login_at = datetime.utcnow()
    db.commit()
    
    # 创建令牌
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    return ApiResponse(
        message="Login successful",
        data=LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.access_token_expire_minutes * 60,
            user=UserResponse.from_orm(user)
        )
    )

@router.post("/refresh", response_model=ApiResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """刷新访问令牌"""
    payload = verify_token(refresh_data.refresh_token, "refresh")
    user_id = payload.get("sub")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # 创建新的访问令牌
    access_token = create_access_token(data={"sub": user.id})
    
    return ApiResponse(
        message="Token refreshed successfully",
        data=RefreshTokenResponse(
            access_token=access_token,
            expires_in=settings.access_token_expire_minutes * 60
        )
    ) 