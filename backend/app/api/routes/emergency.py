from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import json
from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.core.security import generate_session_id
from app.models.user import User
from app.models.emergency import EmergencySession, EmergencyMessage
from app.schemas.emergency import (
    EmergencyScenario,
    EmergencySessionCreate,
    EmergencySessionResponse,
    EmergencySessionWithMessages,
    EmergencyMessageCreate,
    EmergencyMessageResponse
)
from pydantic import BaseModel
from app.schemas.common import ApiResponse
from app.services.ai_service import ai_service

router = APIRouter()

# 设备位置数据模型
class EquipmentLocation(BaseModel):
    name: str
    latitude: float
    longitude: float
    distance: float

class EmergencyEquipment(BaseModel):
    id: str
    name: str
    type: str
    location: EquipmentLocation
    status: str = "available"

# 预定义的应急场景
EMERGENCY_SCENARIOS = {
    "equipment": {
        "id": "equipment",
        "title": "常用医疗设备操作",
        "description": "AED、血压计等医疗设备使用指导",
        "icon": "fas fa-medkit",
        "category": "guidance"
    },
    "firstAid": {
        "id": "firstAid",
        "title": "紧急救护步骤",
        "description": "心肺复苏、止血等急救操作指导",
        "icon": "fas fa-heartbeat",
        "category": "critical"
    },
    "location": {
        "id": "location",
        "title": "医疗设备定位",
        "description": "查找最近的AED、医疗设备位置",
        "icon": "fas fa-map-marker-alt",
        "category": "guidance"
    },
    "emergency": {
        "id": "emergency",
        "title": "现场应急处置",
        "description": "快速描述现场情况，获取应急处置建议",
        "icon": "fas fa-ambulance",
        "category": "urgent"
    }
}

@router.get("/scenarios", response_model=ApiResponse)
async def get_emergency_scenarios():
    """获取应急场景列表"""
    scenarios = [EmergencyScenario(**scenario) for scenario in EMERGENCY_SCENARIOS.values()]
    
    return ApiResponse(
        message="Emergency scenarios retrieved successfully",
        data=scenarios
    )

@router.get("/equipment/nearby", response_model=ApiResponse)
async def get_nearby_equipment(
    latitude: float,
    longitude: float,
    radius: float = 1000,
    type: str = None
):
    """获取附近的医疗设备"""
    # 模拟设备数据
    mock_equipment = [
        EmergencyEquipment(
            id="aed_001",
            name="自动体外除颤器 AED-001",
            type="aed",
            location=EquipmentLocation(
                name="市中心医院大厅",
                latitude=latitude + 0.001,
                longitude=longitude + 0.001,
                distance=120
            )
        ),
        EmergencyEquipment(
            id="aed_002", 
            name="自动体外除颤器 AED-002",
            type="aed",
            location=EquipmentLocation(
                name="购物中心二楼服务台",
                latitude=latitude - 0.002,
                longitude=longitude + 0.002,
                distance=250
            )
        ),
        EmergencyEquipment(
            id="oxygen_001",
            name="便携式氧气瓶",
            type="oxygen",
            location=EquipmentLocation(
                name="社区卫生服务中心",
                latitude=latitude + 0.003,
                longitude=longitude - 0.001,
                distance=300
            )
        )
    ]
    
    # 根据类型过滤
    if type:
        mock_equipment = [eq for eq in mock_equipment if eq.type == type]
    
    # 根据距离过滤
    mock_equipment = [eq for eq in mock_equipment if eq.location.distance <= radius]
    
    return ApiResponse(
        message="Nearby equipment retrieved successfully",
        data=mock_equipment
    )

@router.get("/sessions", response_model=ApiResponse)
async def get_emergency_sessions(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取用户的应急会话列表"""
    sessions = db.query(EmergencySession).filter(
        EmergencySession.user_id == current_user.id
    ).order_by(EmergencySession.updated_at.desc()).all()
    
    # 添加最后一条消息信息
    session_data = []
    for session in sessions:
        # 获取最后一条用户消息作为预览
        last_message = db.query(EmergencyMessage).filter(
            EmergencyMessage.session_id == session.id,
            EmergencyMessage.role == "user"
        ).order_by(EmergencyMessage.created_at.desc()).first()
        
        session_dict = EmergencySessionResponse.from_orm(session).dict()
        # 手动处理 datetime 序列化
        session_dict['created_at'] = session.created_at.isoformat()
        session_dict['updated_at'] = session.updated_at.isoformat()
        session_dict["last_message"] = last_message.content if last_message else ""
        session_data.append(session_dict)
    
    return ApiResponse(
        message="Emergency sessions retrieved successfully",
        data=session_data
    )

@router.post("/sessions", response_model=ApiResponse)
async def create_emergency_session(
    session_data: EmergencySessionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建新的应急会话"""
    session = EmergencySession(
        id=generate_session_id(),
        user_id=current_user.id,
        scenario_type=session_data.scenario_type,
        title=session_data.title,
        status="active"
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    # 不再自动创建初始指导消息，让用户主动开始对话
    
    return ApiResponse(
        code=201,
        message="Emergency session created successfully",
        data=EmergencySessionResponse.from_orm(session)
    )

@router.get("/sessions/{session_id}", response_model=ApiResponse)
async def get_emergency_session(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取特定应急会话及其消息"""
    session = db.query(EmergencySession).filter(
        EmergencySession.id == session_id,
        EmergencySession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency session not found"
        )
    
    messages = db.query(EmergencyMessage).filter(
        EmergencyMessage.session_id == session_id
    ).order_by(EmergencyMessage.created_at.asc()).all()
    
    # 只返回消息列表，与前端期望的格式一致
    messages_data = []
    for msg in messages:
        msg_data = EmergencyMessageResponse.from_orm(msg).dict()
        msg_data['created_at'] = msg.created_at.isoformat()
        messages_data.append(msg_data)
    
    return ApiResponse(
        message="Emergency session retrieved successfully",
        data=messages_data
    )

@router.post("/sessions/{session_id}/messages")
async def send_emergency_message(
    session_id: str,
    message_data: EmergencyMessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """发送消息到应急会话（流式响应）"""
    # 验证会话存在且属于当前用户
    session = db.query(EmergencySession).filter(
        EmergencySession.id == session_id,
        EmergencySession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency session not found"
        )
    
    # 创建用户消息
    user_message = EmergencyMessage(
        id=generate_session_id(),
        session_id=session_id,
        role="user",
        content=message_data.content
    )
    
    db.add(user_message)
    db.commit()
    db.refresh(user_message)
    
    # 创建流式响应生成器
    async def generate_response():
        assistant_message_id = generate_session_id()
        full_content = ""
        
        try:
            # 发送用户消息确认
            user_msg_data = EmergencyMessageResponse.from_orm(user_message).dict()
            user_msg_data['created_at'] = user_message.created_at.isoformat()
            yield f"data: {json.dumps({'type': 'user_message', 'data': user_msg_data})}\n\n"
            
            # 获取会话历史用于AI上下文
            messages = db.query(EmergencyMessage).filter(
                EmergencyMessage.session_id == session_id
            ).order_by(EmergencyMessage.created_at.asc()).all()
            
            # 构建AI消息历史
            ai_messages = []
            scenario = EMERGENCY_SCENARIOS.get(session.scenario_type, {})
            
            # 添加场景上下文到第一条消息
            if messages:
                for msg in messages:
                    if msg.role == "user" and len(ai_messages) == 0:
                        # 第一条用户消息添加场景信息
                        ai_messages.append({
                            "role": msg.role,
                            "content": f"""当前处理的是{scenario.get('title', '紧急情况')}。用户问题：{msg.content}"""
                        })
                    else:
                        ai_messages.append({
                            "role": msg.role,
                            "content": msg.content
                        })
            else:
                # 如果没有历史消息，这是第一条消息
                ai_messages.append({
                    "role": "user",
                    "content": f"""当前处理的是{scenario.get('title', '紧急情况')}。用户问题：{message_data.content}"""
                })
            
            # 获取AI流式响应
            async for chunk in ai_service.stream_chat_completion(
                ai_messages, 
                mode="emergency",
                temperature=0.2,
                max_tokens=2000
            ):
                if chunk["type"] == "answer_start":
                    yield f"data: {json.dumps({'type': 'answer_start', 'message_id': assistant_message_id})}\n\n"
                elif chunk["type"] == "answer":
                    full_content += chunk["content"]
                    yield f"data: {json.dumps(chunk)}\n\n"
                elif chunk["type"] == "done":
                    full_content = chunk["content"]
                    
                    # 解析步骤和设备（简单实现）
                    steps = []
                    equipment = []
                    
                    lines = full_content.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line.startswith(('步骤', '1.', '2.', '3.', '4.', '5.')):
                            steps.append(line)
                        elif line.startswith(('设备', '器材', '工具')):
                            equipment.append(line)
                    
                    # 保存AI响应到数据库
                    assistant_message = EmergencyMessage(
                        id=assistant_message_id,
                        session_id=session_id,
                        role="assistant",
                        content=full_content,
                        steps=steps[:5] if steps else None,
                        equipment=equipment[:5] if equipment else None
                    )
                    
                    db.add(assistant_message)
                    
                    # 触发会话的updated_at自动更新（通过修改任意字段）
                    session.status = session.status  # 这会触发onupdate
                    db.commit()
                    db.refresh(assistant_message)
                    
                    # 发送完成消息
                    assistant_msg_data = EmergencyMessageResponse.from_orm(assistant_message).dict()
                    assistant_msg_data['created_at'] = assistant_message.created_at.isoformat()
                    yield f"data: {json.dumps({'type': 'assistant_message', 'data': assistant_msg_data})}\n\n"
                    yield f"data: {json.dumps({'type': 'done'})}\n\n"
                    break
                elif chunk["type"] == "usage":
                    yield f"data: {json.dumps(chunk)}\n\n"
                elif chunk["type"] == "error":
                    yield f"data: {json.dumps(chunk)}\n\n"
                    break
                    
        except Exception as e:
            error_msg = f"应急指导生成失败: {str(e)}"
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

@router.delete("/sessions/{session_id}", response_model=ApiResponse)
async def delete_emergency_session(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """删除应急会话"""
    session = db.query(EmergencySession).filter(
        EmergencySession.id == session_id,
        EmergencySession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency session not found"
        )
    
    db.delete(session)
    db.commit()
    
    return ApiResponse(message="Emergency session deleted successfully") 