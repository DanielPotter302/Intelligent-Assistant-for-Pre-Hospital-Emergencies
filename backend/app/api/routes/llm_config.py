from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_active_user, require_admin
from app.core.security import generate_session_id
from app.models.user import User
from app.models.llm_config import LLMConfig
from app.schemas.llm_config import (
    LLMConfigCreate,
    LLMConfigUpdate,
    LLMConfigResponse,
    LLMConfigListResponse
)
from app.schemas.common import ApiResponse

router = APIRouter()

@router.get("/configs", response_model=ApiResponse)
async def get_llm_configs(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """获取所有LLM配置（仅管理员）"""
    configs = db.query(LLMConfig).order_by(LLMConfig.created_at.desc()).all()
    
    config_data = []
    for config in configs:
        config_dict = LLMConfigListResponse.from_orm(config).dict()
        config_dict['created_at'] = config.created_at.isoformat()
        config_dict['updated_at'] = config.updated_at.isoformat()
        config_data.append(config_dict)
    
    return ApiResponse(
        message="LLM configs retrieved successfully",
        data=config_data
    )

@router.get("/configs/{config_id}", response_model=ApiResponse)
async def get_llm_config(
    config_id: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """获取单个LLM配置详情（仅管理员）"""
    config = db.query(LLMConfig).filter(LLMConfig.id == config_id).first()
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="LLM config not found"
        )
    
    config_dict = LLMConfigResponse.from_orm(config).dict()
    config_dict['created_at'] = config.created_at.isoformat()
    config_dict['updated_at'] = config.updated_at.isoformat()
    
    return ApiResponse(
        message="LLM config retrieved successfully",
        data=config_dict
    )

@router.post("/configs", response_model=ApiResponse)
async def create_llm_config(
    config_data: LLMConfigCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """创建LLM配置（仅管理员）"""
    # 检查模块名称是否已存在
    existing_config = db.query(LLMConfig).filter(
        LLMConfig.module_name == config_data.module_name
    ).first()
    
    if existing_config:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Module '{config_data.module_name}' already has a configuration"
        )
    
    # 创建新配置
    config = LLMConfig(
        id=generate_session_id(),
        **config_data.dict()
    )
    
    db.add(config)
    db.commit()
    db.refresh(config)
    
    config_dict = LLMConfigResponse.from_orm(config).dict()
    config_dict['created_at'] = config.created_at.isoformat()
    config_dict['updated_at'] = config.updated_at.isoformat()
    
    return ApiResponse(
        message="LLM config created successfully",
        data=config_dict
    )

@router.put("/configs/{config_id}", response_model=ApiResponse)
async def update_llm_config(
    config_id: str,
    config_data: LLMConfigUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """更新LLM配置（仅管理员）"""
    config = db.query(LLMConfig).filter(LLMConfig.id == config_id).first()
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="LLM config not found"
        )
    
    # 更新配置
    update_data = config_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(config, field, value)
    
    db.commit()
    db.refresh(config)
    
    config_dict = LLMConfigResponse.from_orm(config).dict()
    config_dict['created_at'] = config.created_at.isoformat()
    config_dict['updated_at'] = config.updated_at.isoformat()
    
    return ApiResponse(
        message="LLM config updated successfully",
        data=config_dict
    )

@router.delete("/configs/{config_id}", response_model=ApiResponse)
async def delete_llm_config(
    config_id: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """删除LLM配置（仅管理员）"""
    config = db.query(LLMConfig).filter(LLMConfig.id == config_id).first()
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="LLM config not found"
        )
    
    db.delete(config)
    db.commit()
    
    return ApiResponse(message="LLM config deleted successfully")

@router.post("/configs/init-default", response_model=ApiResponse)
async def init_default_configs(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """初始化默认LLM配置（仅管理员）"""
    default_configs = [
        {
            "module_name": "chat_kb",
            "display_name": "智能问答-知识检索",
            "api_key": "sk-693ef3cef5b742c59ae610dec7295199",
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "model_name": "qwen-plus",
            "temperature": "0.7",
            "max_tokens": "2000",
            "enable_thinking": False,
            "description": "智能问答模块的知识检索配置"
        },
        {
            "module_name": "chat_graph",
            "display_name": "智能问答-复杂问答",
            "api_key": "sk-693ef3cef5b742c59ae610dec7295199",
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "model_name": "qwen-plus",
            "temperature": "0.7",
            "max_tokens": "2000",
            "enable_thinking": True,
            "description": "智能问答模块的复杂问答配置，启用思考功能"
        },
        {
            "module_name": "triage",
            "display_name": "智能分诊",
            "api_key": "sk-693ef3cef5b742c59ae610dec7295199",
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "model_name": "qwen-plus",
            "temperature": "0.3",
            "max_tokens": "1500",
            "enable_thinking": False,
            "description": "智能分诊模块的LLM配置"
        },
        {
            "module_name": "emergency_cpr",
            "display_name": "应急指导-心肺复苏",
            "api_key": "sk-693ef3cef5b742c59ae610dec7295199",
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "model_name": "qwen-plus",
            "temperature": "0.2",
            "max_tokens": "1500",
            "enable_thinking": False,
            "description": "心肺复苏应急指导的LLM配置"
        },
        {
            "module_name": "emergency_trauma",
            "display_name": "应急指导-外伤处理",
            "api_key": "sk-693ef3cef5b742c59ae610dec7295199",
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "model_name": "qwen-plus",
            "temperature": "0.2",
            "max_tokens": "1500",
            "enable_thinking": False,
            "description": "外伤处理应急指导的LLM配置"
        },
        {
            "module_name": "emergency_poisoning",
            "display_name": "应急指导-中毒处理",
            "api_key": "sk-693ef3cef5b742c59ae610dec7295199",
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "model_name": "qwen-plus",
            "temperature": "0.2",
            "max_tokens": "1500",
            "enable_thinking": False,
            "description": "中毒处理应急指导的LLM配置"
        },
        {
            "module_name": "emergency_burn",
            "display_name": "应急指导-烧伤处理",
            "api_key": "sk-693ef3cef5b742c59ae610dec7295199",
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "model_name": "qwen-plus",
            "temperature": "0.2",
            "max_tokens": "1500",
            "enable_thinking": False,
            "description": "烧伤处理应急指导的LLM配置"
        }
    ]
    
    created_configs = []
    for config_data in default_configs:
        # 检查是否已存在
        existing = db.query(LLMConfig).filter(
            LLMConfig.module_name == config_data["module_name"]
        ).first()
        
        if not existing:
            config = LLMConfig(
                id=generate_session_id(),
                **config_data
            )
            db.add(config)
            created_configs.append(config_data["display_name"])
    
    db.commit()
    
    return ApiResponse(
        message=f"Default configs initialized successfully. Created: {', '.join(created_configs) if created_configs else 'None (all already exist)'}",
        data={"created_count": len(created_configs)}
    ) 