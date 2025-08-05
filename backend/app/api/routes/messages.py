from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.security import generate_user_id
from app.models.user import User
from app.models.message import ContactMessage
from app.schemas.message import (
    ContactMessageCreate, 
    ContactMessageResponse, 
    ContactMessageUpdate
)
from app.schemas.common import ApiResponse
from datetime import datetime

router = APIRouter()

@router.post("/contact", response_model=ApiResponse)
async def create_contact_message(
    message_data: ContactMessageCreate,
    db: Session = Depends(get_db)
):
    """创建联系留言"""
    try:
        # 创建新留言
        message = ContactMessage(
            id=generate_user_id(),
            name=message_data.name,
            email=message_data.email,
            content=message_data.content,
            status="unread"
        )
        
        db.add(message)
        db.commit()
        db.refresh(message)
        
        return ApiResponse(
            code=201,
            message="留言提交成功",
            data={
                "messageId": message.id,
                "name": message.name,
                "createdAt": message.created_at.isoformat()
            }
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"留言提交失败: {str(e)}"
        )

@router.get("/admin/messages", response_model=ApiResponse)
async def get_contact_messages(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    status_filter: Optional[str] = Query(None, description="状态筛选: unread, read, replied"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量")
):
    """获取联系留言列表（仅管理员）"""
    # 检查管理员权限
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    
    # 构建查询
    query = db.query(ContactMessage)
    
    # 状态筛选
    if status_filter:
        query = query.filter(ContactMessage.status == status_filter)
    
    # 分页
    offset = (page - 1) * size
    messages = query.order_by(ContactMessage.created_at.desc()).offset(offset).limit(size).all()
    
    # 获取总数
    total = query.count()
    
    return ApiResponse(
        message="获取留言列表成功",
        data={
            "messages": [ContactMessageResponse.from_orm(msg) for msg in messages],
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size
        }
    )

@router.put("/admin/messages/{message_id}", response_model=ApiResponse)
async def update_contact_message(
    message_id: str,
    update_data: ContactMessageUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新留言状态/回复（仅管理员）"""
    # 检查管理员权限
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    
    # 查找留言
    message = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="留言不存在"
        )
    
    # 更新留言
    message.admin_reply = update_data.admin_reply
    message.status = update_data.status
    message.replied_at = datetime.utcnow()
    
    db.commit()
    db.refresh(message)
    
    return ApiResponse(
        message="留言更新成功",
        data=ContactMessageResponse.from_orm(message)
    )

@router.patch("/admin/messages/{message_id}/read", response_model=ApiResponse)
async def mark_message_as_read(
    message_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """标记留言为已读（仅管理员）"""
    # 检查管理员权限
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    
    # 查找留言
    message = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="留言不存在"
        )
    
    # 标记为已读
    if message.status == "unread":
        message.status = "read"
        db.commit()
    
    return ApiResponse(
        message="留言已标记为已读"
    ) 