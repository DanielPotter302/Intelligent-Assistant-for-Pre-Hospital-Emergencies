from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.common import ApiResponse

router = APIRouter()

@router.get("/profile", response_model=ApiResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """获取用户个人信息"""
    return ApiResponse(
        message="User profile retrieved successfully",
        data=UserResponse.from_orm(current_user)
    )

@router.put("/profile", response_model=ApiResponse)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新用户个人信息"""
    # 更新用户信息
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return ApiResponse(
        message="User profile updated successfully",
        data=UserResponse.from_orm(current_user)
    )

@router.get("/info", response_model=ApiResponse)
async def get_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """获取用户信息（用于前端路由守卫）"""
    return ApiResponse(
        message="User info retrieved successfully",
        data=UserResponse.from_orm(current_user)
    ) 