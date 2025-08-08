from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import json
import uuid
from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.core.security import generate_session_id
from app.models.user import User
from app.models.chat import ChatSession, ChatMessage
from app.schemas.chat import (
    ChatSessionCreate,
    ChatSessionResponse,
    ChatSessionWithMessages,
    ChatMessageCreate,
    ChatMessageResponse
)
from app.schemas.common import ApiResponse
from app.services.ai_service import ai_service

router = APIRouter()

@router.get("/sessions", response_model=ApiResponse)
async def get_chat_sessions(
    mode: str = "kb",  # 添加模式参数
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取用户的聊天会话列表"""
    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id,
        ChatSession.mode == mode  # 按模式过滤
    ).order_by(ChatSession.updated_at.desc()).all()
    
    # 添加消息数量和最后一条消息
    session_data = []
    for session in sessions:
        # 获取最后一条用户消息作为预览
        last_message = db.query(ChatMessage).filter(
            ChatMessage.session_id == session.id,
            ChatMessage.role == "user"
        ).order_by(ChatMessage.created_at.desc()).first()
        
        message_count = db.query(ChatMessage).filter(
            ChatMessage.session_id == session.id
        ).count()
        
        session_dict = ChatSessionResponse.from_orm(session).dict()
        # 手动处理 datetime 序列化
        session_dict['created_at'] = session.created_at.isoformat()
        session_dict['updated_at'] = session.updated_at.isoformat()
        session_dict["message_count"] = message_count
        session_dict["last_message"] = last_message.content if last_message else ""
        session_data.append(session_dict)
    
    return ApiResponse(
        message="Chat sessions retrieved successfully",
        data=session_data
    )

@router.post("/sessions", response_model=ApiResponse)
async def create_chat_session(
    session_data: ChatSessionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建新的聊天会话"""
    session = ChatSession(
        id=generate_session_id(),
        user_id=current_user.id,
        title=session_data.title,
        mode=session_data.mode
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    session_response = ChatSessionResponse.from_orm(session).dict()
    session_response['created_at'] = session.created_at.isoformat()
    session_response['updated_at'] = session.updated_at.isoformat()
    
    return ApiResponse(
        message="Chat session created successfully",
        data=session_response
    )

@router.get("/sessions/{session_id}", response_model=ApiResponse)
async def get_chat_session(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取聊天会话详情和消息"""
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    
    # 获取会话消息
    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.created_at.asc()).all()
    
    session_data = ChatSessionWithMessages.from_orm(session).dict()
    # 手动处理 datetime 序列化
    session_data['created_at'] = session.created_at.isoformat()
    session_data['updated_at'] = session.updated_at.isoformat()
    
    messages_data = []
    for msg in messages:
        msg_data = ChatMessageResponse.from_orm(msg).dict()
        msg_data['created_at'] = msg.created_at.isoformat()
        messages_data.append(msg_data)
    session_data["messages"] = messages_data
    
    return ApiResponse(
        message="Chat session retrieved successfully",
        data=session_data["messages"]  # 只返回消息列表
    )

@router.post("/sessions/{session_id}/messages")
async def send_message_stream(
    session_id: str,
    message_data: ChatMessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """发送消息到聊天会话（流式响应）"""
    # 验证会话存在且属于当前用户
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    
    # 创建用户消息
    user_message = ChatMessage(
        id=generate_session_id(),
        session_id=session_id,
        role="user",
        content=message_data.content
    )
    
    db.add(user_message)
    db.commit()
    db.refresh(user_message)
    
    # 获取会话历史用于AI上下文
    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.created_at.asc()).all()
    
    # 构建AI消息历史
    ai_messages = []
    for msg in messages:
        ai_messages.append({
            "role": msg.role,
            "content": msg.content
        })
    
    # 创建流式响应生成器
    async def generate_response():
        assistant_message_id = generate_session_id()
        full_content = ""
        reasoning_content = ""
        
        try:
            # 发送会话信息（用于前端同步）
            session_info = {
                'id': session.id,
                'title': session.title,
                'mode': session.mode,
                'created_at': session.created_at.isoformat(),
                'updated_at': session.updated_at.isoformat()
            }
            yield f"data: {json.dumps({'type': 'session_info', 'data': session_info})}\n\n"
            
            # 发送用户消息确认
            user_msg_data = ChatMessageResponse.from_orm(user_message).dict()
            user_msg_data['created_at'] = user_message.created_at.isoformat()
            yield f"data: {json.dumps({'type': 'user_message', 'data': user_msg_data})}\n\n"
            
            # 获取AI流式响应
            async for chunk in ai_service.stream_chat_completion(
                ai_messages, 
                mode=session.mode,
                temperature=0.7,
                max_tokens=2000
            ):
                if chunk["type"] == "thinking":
                    yield f"data: {json.dumps(chunk)}\n\n"
                elif chunk["type"] == "answer_start":
                    yield f"data: {json.dumps({'type': 'answer_start', 'message_id': assistant_message_id})}\n\n"
                elif chunk["type"] == "answer":
                    full_content += chunk["content"]
                    yield f"data: {json.dumps(chunk)}\n\n"
                elif chunk["type"] == "done":
                    # 不要覆盖累积的内容，使用已经累积的full_content
                    reasoning_content = chunk.get("reasoning", "")
                    
                    # 保存AI响应到数据库
                    assistant_message = ChatMessage(
                        id=assistant_message_id,
                        session_id=session_id,
                        role="assistant",
                        content=full_content  # 使用累积的完整内容
                    )
                    
                    db.add(assistant_message)
                    
                    # 更新会话时间和标题（如果是第一条消息）
                    if len(ai_messages) <= 2:  # 系统消息 + 用户消息
                        # 生成会话标题（取用户消息的前20个字符）
                        session.title = message_data.content[:20] + ("..." if len(message_data.content) > 20 else "")
                    
                    # 让数据库自动更新 updated_at 字段
                    # session.updated_at 会通过 onupdate=func.now() 自动更新
                    db.commit()
                    db.refresh(assistant_message)
                    
                    # 发送完成消息
                    assistant_msg_data = ChatMessageResponse.from_orm(assistant_message).dict()
                    assistant_msg_data['created_at'] = assistant_message.created_at.isoformat()
                    yield f"data: {json.dumps({'type': 'assistant_message', 'data': assistant_msg_data})}\n\n"
                    yield f"data: {json.dumps({'type': 'done'})}\n\n"
                    break
                elif chunk["type"] == "usage":
                    yield f"data: {json.dumps(chunk)}\n\n"
                    
        except Exception as e:
            error_msg = f"AI响应生成失败: {str(e)}"
            yield f"data: {json.dumps({'type': 'error', 'message': error_msg})}\n\n"
    
    return StreamingResponse(
        generate_response(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream"
        }
    )

# 新增：自动创建会话的消息发送接口
@router.post("/messages")
async def send_message_auto_session(
    message_data: ChatMessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """发送消息（自动创建会话）"""
    # 检查用户是否有该模式的活跃会话
    mode = getattr(message_data, 'mode', 'kb')
    
    # 查找最近的会话
    recent_session = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id,
        ChatSession.mode == mode
    ).order_by(ChatSession.updated_at.desc()).first()
    
    # 如果没有会话或最近会话超过24小时，创建新会话
    if not recent_session:
        # 创建新会话
        session = ChatSession(
            id=generate_session_id(),
            user_id=current_user.id,
            title=message_data.content[:20] + ("..." if len(message_data.content) > 20 else ""),
            mode=mode
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        session_id = session.id
    else:
        session_id = recent_session.id
    
    # 重定向到流式消息接口
    return await send_message_stream(session_id, message_data, current_user, db)

@router.delete("/sessions/{session_id}", response_model=ApiResponse)
async def delete_chat_session(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """删除聊天会话"""
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    
    # 先删除相关的消息
    messages = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).all()
    for message in messages:
        db.delete(message)
    
    # 再删除会话
    db.delete(session)
    db.commit()
    
    return ApiResponse(message="Chat session deleted successfully")

@router.delete("/sessions", response_model=ApiResponse)
async def clear_all_chat_sessions(
    mode: str = "kb",  # 添加模式参数，只清空指定模式的会话
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """清空用户的所有聊天会话"""
    # 获取用户在指定模式下的所有会话
    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id,
        ChatSession.mode == mode
    ).all()
    
    deleted_count = 0
    for session in sessions:
        # 先删除相关的消息
        messages = db.query(ChatMessage).filter(ChatMessage.session_id == session.id).all()
        for message in messages:
            db.delete(message)
        
        # 再删除会话
        db.delete(session)
        deleted_count += 1
    
    db.commit()
    
    return ApiResponse(message=f"Successfully cleared {deleted_count} chat sessions") 