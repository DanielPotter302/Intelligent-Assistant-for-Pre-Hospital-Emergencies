from fastapi import APIRouter
from app.schemas.common import ApiResponse, HealthStatus
from datetime import datetime

router = APIRouter()

@router.get("/features", response_model=ApiResponse)
async def get_features():
    """获取系统功能总览"""
    features = [
        {
            "id": "smart-triage",
            "title": "智能分诊",
            "description": "基于AI的患者分诊系统，快速评估病情严重程度",
            "icon": "fas fa-user-md",
            "status": "active"
        },
        {
            "id": "emergency-guide", 
            "title": "应急指导",
            "description": "针对不同紧急情况提供专业的处理指导",
            "icon": "fas fa-ambulance",
            "status": "active"
        },
        {
            "id": "ai-chat",
            "title": "智能问答",
            "description": "医疗知识库智能问答，提供专业医疗咨询",
            "icon": "fas fa-comments",
            "status": "active"
        },
        {
            "id": "knowledge-base",
            "title": "知识库",
            "description": "丰富的医疗文档、视频资源库",
            "icon": "fas fa-book",
            "status": "active"
        }
    ]
    
    return ApiResponse(
        message="Features retrieved successfully",
        data=features
    )

@router.get("/workflows", response_model=ApiResponse)
async def get_workflows():
    """获取工作流程"""
    workflows = [
        {
            "step": 1,
            "title": "患者评估",
            "description": "快速收集患者基本信息和症状",
            "icon": "fas fa-clipboard-list"
        },
        {
            "step": 2,
            "title": "智能分诊",
            "description": "AI分析患者情况，确定紧急程度",
            "icon": "fas fa-brain"
        },
        {
            "step": 3,
            "title": "应急指导",
            "description": "根据分诊结果提供相应的处理指导",
            "icon": "fas fa-hands-helping"
        },
        {
            "step": 4,
            "title": "持续监护",
            "description": "持续监测患者状态，调整处理方案",
            "icon": "fas fa-heartbeat"
        }
    ]
    
    return ApiResponse(
        message="Workflows retrieved successfully",
        data=workflows
    )

@router.get("/health", response_model=HealthStatus)
async def health_check():
    """系统健康检查"""
    return HealthStatus(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        service="pre-hospital-assistant-api",
        version="1.0.0"
    ) 