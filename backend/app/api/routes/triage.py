from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import json
from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.core.security import generate_session_id
from app.models.user import User
from app.models.triage import TriageRecord
from app.schemas.triage import TriageRequest, TriageResponse, TriageHistoryItem
from app.schemas.common import ApiResponse, PaginatedResponse
from app.services.triage_service import triage_service

router = APIRouter()

@router.post("/analyze", response_model=ApiResponse)
async def analyze_triage_data(
    triage_data: TriageRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """AI分诊分析"""
    try:
        # 执行AI分诊分析
        analysis_result = await triage_service.analyze_triage(triage_data)
        
        # 保存分诊记录
        triage_record = TriageRecord(
            id=generate_session_id(),
            user_id=current_user.id,
            
            # 患者信息
            patient_name=triage_data.patient_info.name,
            patient_id_card=triage_data.patient_info.id_card,
            patient_age=triage_data.patient_info.age,
            patient_gender=triage_data.patient_info.gender,
            patient_weight=triage_data.patient_info.weight,
            patient_height=triage_data.patient_info.height,
            patient_allergies=triage_data.patient_info.allergies,
            patient_medications=triage_data.patient_info.medications,
            patient_medical_history=triage_data.patient_info.medical_history,
            
            # 生命体征
            heart_rate=triage_data.vital_signs.heart_rate,
            blood_pressure_systolic=triage_data.vital_signs.blood_pressure_systolic,
            blood_pressure_diastolic=triage_data.vital_signs.blood_pressure_diastolic,
            respiratory_rate=triage_data.vital_signs.respiratory_rate,
            temperature=triage_data.vital_signs.temperature,
            oxygen_saturation=triage_data.vital_signs.oxygen_saturation,
            blood_glucose=triage_data.vital_signs.blood_glucose,
            
            # 症状信息
            chief_complaint=triage_data.symptom_info.chief_complaint,
            symptoms=triage_data.symptom_info.symptoms,
            pain_level=triage_data.symptom_info.pain_level,
            symptom_duration=triage_data.symptom_info.symptom_duration,
            
            # AI分析结果
            urgency_level=analysis_result.urgency_level,
            recommended_actions=analysis_result.recommended_actions,
            ai_analysis={
                "priority_score": analysis_result.priority_score,
                "estimated_wait_time": analysis_result.estimated_wait_time,
                "department_recommendation": analysis_result.department_recommendation,
                "additional_notes": analysis_result.additional_notes
            }
        )
        
        db.add(triage_record)
        db.commit()
        db.refresh(triage_record)
        
        return ApiResponse(
            message="Triage analysis completed successfully",
            data={
                "record_id": triage_record.id,
                "analysis": analysis_result
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Triage analysis failed: {str(e)}"
        )

@router.post("/analyze/stream")
async def analyze_triage_data_stream(
    triage_data: TriageRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """AI分诊分析（流式输出）"""
    
    async def generate_response():
        try:
            # 发送开始信号
            yield f"data: {json.dumps({'type': 'analysis_start'})}\n\n"
            
            # 获取AI流式响应
            full_content = ""
            async for chunk in triage_service.analyze_triage_stream(triage_data):
                if chunk["type"] == "answer":
                    full_content += chunk["content"]
                    yield f"data: {json.dumps(chunk)}\n\n"
                elif chunk["type"] == "done":
                    full_content = chunk["content"]
                    
                    # 解析AI响应并保存分诊记录
                    try:
                        analysis_result = triage_service._parse_ai_response(full_content, triage_data)
                        
                        # 保存分诊记录
                        triage_record = TriageRecord(
                            id=generate_session_id(),
                            user_id=current_user.id,
                            
                            # 患者信息
                            patient_name=triage_data.patient_info.name,
                            patient_id_card=triage_data.patient_info.id_card,
                            patient_age=triage_data.patient_info.age,
                            patient_gender=triage_data.patient_info.gender,
                            patient_weight=triage_data.patient_info.weight,
                            patient_height=triage_data.patient_info.height,
                            patient_allergies=triage_data.patient_info.allergies,
                            patient_medications=triage_data.patient_info.medications,
                            patient_medical_history=triage_data.patient_info.medical_history,
                            
                            # 生命体征
                            heart_rate=triage_data.vital_signs.heart_rate,
                            blood_pressure_systolic=triage_data.vital_signs.blood_pressure_systolic,
                            blood_pressure_diastolic=triage_data.vital_signs.blood_pressure_diastolic,
                            respiratory_rate=triage_data.vital_signs.respiratory_rate,
                            temperature=triage_data.vital_signs.temperature,
                            oxygen_saturation=triage_data.vital_signs.oxygen_saturation,
                            blood_glucose=triage_data.vital_signs.blood_glucose,
                            
                            # 症状描述
                            chief_complaint=triage_data.symptoms.chief_complaint,
                            symptom_duration=triage_data.symptoms.duration,
                            pain_scale=triage_data.symptoms.pain_scale,
                            additional_symptoms=triage_data.symptoms.additional_symptoms,
                            
                            # 分诊结果
                            urgency_level=analysis_result.urgency_level,
                            priority_score=analysis_result.priority_score,
                            recommended_actions=analysis_result.recommended_actions,
                            estimated_wait_time=analysis_result.estimated_wait_time,
                            department_recommendation=analysis_result.department_recommendation,
                            ai_analysis={
                                "priority_score": analysis_result.priority_score,
                                "estimated_wait_time": analysis_result.estimated_wait_time,
                                "department_recommendation": analysis_result.department_recommendation,
                                "additional_notes": analysis_result.additional_notes
                            }
                        )
                        
                        db.add(triage_record)
                        db.commit()
                        db.refresh(triage_record)
                        
                        # 发送分析结果
                        yield f"data: {json.dumps({'type': 'analysis_result', 'data': {'record_id': triage_record.id, 'analysis': analysis_result.dict()}})}\n\n"
                        
                    except Exception as parse_error:
                        yield f"data: {json.dumps({'type': 'error', 'message': f'结果解析失败: {str(parse_error)}'})}\n\n"
                    
                    yield f"data: {json.dumps({'type': 'done'})}\n\n"
                    break
                elif chunk["type"] == "error":
                    yield f"data: {json.dumps(chunk)}\n\n"
                    break
                else:
                    yield f"data: {json.dumps(chunk)}\n\n"
                    
        except Exception as e:
            error_msg = f"分诊分析失败: {str(e)}"
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

@router.get("/history", response_model=ApiResponse)
async def get_triage_history(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """获取分诊历史"""
    offset = (page - 1) * page_size
    
    # 查询总数
    total = db.query(TriageRecord).filter(
        TriageRecord.user_id == current_user.id
    ).count()
    
    # 查询记录
    records = db.query(TriageRecord).filter(
        TriageRecord.user_id == current_user.id
    ).order_by(TriageRecord.created_at.desc()).offset(offset).limit(page_size).all()
    
    # 转换为响应格式
    history_items = [
        TriageHistoryItem(
            id=record.id,
            patient_name=record.patient_name,
            urgency_level=record.urgency_level,
            chief_complaint=record.chief_complaint,
            created_at=record.created_at
        )
        for record in records
    ]
    
    return ApiResponse(
        message="Triage history retrieved successfully",
        data=PaginatedResponse(
            total=total,
            page=page,
            page_size=page_size,
            records=history_items
        )
    )

@router.get("/history/{record_id}", response_model=ApiResponse)
async def get_triage_record(
    record_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取特定分诊记录详情"""
    record = db.query(TriageRecord).filter(
        TriageRecord.id == record_id,
        TriageRecord.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Triage record not found"
        )
    
    # 构建详细响应
    record_detail = {
        "id": record.id,
        "patient_info": {
            "name": record.patient_name,
            "id_card": record.patient_id_card,
            "age": record.patient_age,
            "gender": record.patient_gender,
            "weight": record.patient_weight,
            "height": record.patient_height,
            "allergies": record.patient_allergies,
            "medications": record.patient_medications,
            "medical_history": record.patient_medical_history
        },
        "vital_signs": {
            "heart_rate": record.heart_rate,
            "blood_pressure_systolic": record.blood_pressure_systolic,
            "blood_pressure_diastolic": record.blood_pressure_diastolic,
            "respiratory_rate": record.respiratory_rate,
            "temperature": record.temperature,
            "oxygen_saturation": record.oxygen_saturation,
            "blood_glucose": record.blood_glucose
        },
        "symptom_info": {
            "chief_complaint": record.chief_complaint,
            "symptoms": record.symptoms,
            "pain_level": record.pain_level,
            "symptom_duration": record.symptom_duration
        },
        "analysis_result": {
            "urgency_level": record.urgency_level,
            "recommended_actions": record.recommended_actions,
            "ai_analysis": record.ai_analysis
        },
        "created_at": record.created_at
    }
    
    return ApiResponse(
        message="Triage record retrieved successfully",
        data=record_detail
    ) 