#!/usr/bin/env python3
"""
LLM配置数据库迁移脚本
添加enable_thinking字段并更新配置
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine
from app.models.llm_config import LLMConfig
from app.core.security import generate_session_id
from sqlalchemy import text

def migrate_llm_config():
    """迁移LLM配置"""
    print("开始迁移LLM配置...")
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 1. 添加enable_thinking字段（如果不存在）
        print("检查并添加enable_thinking字段...")
        try:
            # 检查字段是否存在
            result = db.execute(text("PRAGMA table_info(llm_configs)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'enable_thinking' not in columns:
                print("添加enable_thinking字段...")
                db.execute(text("ALTER TABLE llm_configs ADD COLUMN enable_thinking BOOLEAN DEFAULT 0"))
                db.commit()
                print("enable_thinking字段添加成功")
            else:
                print("enable_thinking字段已存在")
        except Exception as e:
            print(f"添加字段时出错: {e}")
            db.rollback()
        
        # 2. 检查是否需要分离智能问答配置
        print("检查现有配置...")
        existing_chat = db.query(LLMConfig).filter(LLMConfig.module_name == "chat").first()
        existing_chat_kb = db.query(LLMConfig).filter(LLMConfig.module_name == "chat_kb").first()
        existing_chat_graph = db.query(LLMConfig).filter(LLMConfig.module_name == "chat_graph").first()
        
        if existing_chat and not existing_chat_kb and not existing_chat_graph:
            print("发现旧的chat配置，正在分离为chat_kb和chat_graph...")
            
            # 创建知识检索配置（基于原chat配置）
            chat_kb_config = LLMConfig(
                id=generate_session_id(),
                module_name="chat_kb",
                display_name="智能问答-知识检索",
                api_key=existing_chat.api_key,
                base_url=existing_chat.base_url,
                model_name=existing_chat.model_name,
                temperature=existing_chat.temperature,
                max_tokens=existing_chat.max_tokens,
                is_enabled=existing_chat.is_enabled,
                enable_thinking=False,  # 知识检索不启用思考
                description="智能问答模块的知识检索配置"
            )
            db.add(chat_kb_config)
            
            # 创建复杂问答配置（基于原chat配置）
            chat_graph_config = LLMConfig(
                id=generate_session_id(),
                module_name="chat_graph",
                display_name="智能问答-复杂问答",
                api_key=existing_chat.api_key,
                base_url=existing_chat.base_url,
                model_name=existing_chat.model_name,
                temperature=existing_chat.temperature,
                max_tokens=existing_chat.max_tokens,
                is_enabled=existing_chat.is_enabled,
                enable_thinking=True,  # 复杂问答启用思考
                description="智能问答模块的复杂问答配置，启用思考功能"
            )
            db.add(chat_graph_config)
            
            # 删除旧的chat配置
            db.delete(existing_chat)
            
            # 提交分离操作
            db.commit()
            print("智能问答配置分离完成")
        
        # 3. 为所有现有配置设置默认的enable_thinking值
        print("更新现有配置的enable_thinking字段...")
        all_configs = db.query(LLMConfig).all()
        for config in all_configs:
            if config.enable_thinking is None:
                # 只有chat_graph默认启用思考功能
                config.enable_thinking = (config.module_name == "chat_graph")
                print(f"设置 {config.module_name} 的思考功能为: {config.enable_thinking}")
        
        # 4. 确保所有6个配置都存在
        print("检查并创建缺失的配置...")
        required_configs = [
            {
                "module_name": "chat_kb",
                "display_name": "智能问答-知识检索",
                "enable_thinking": False,
                "description": "智能问答模块的知识检索配置"
            },
            {
                "module_name": "chat_graph",
                "display_name": "智能问答-复杂问答",
                "enable_thinking": True,
                "description": "智能问答模块的复杂问答配置，启用思考功能"
            },
            {
                "module_name": "triage",
                "display_name": "智能分诊",
                "enable_thinking": False,
                "description": "智能分诊模块的LLM配置"
            },
            {
                "module_name": "emergency_cpr",
                "display_name": "应急指导-心肺复苏",
                "enable_thinking": False,
                "description": "心肺复苏应急指导的LLM配置"
            },
            {
                "module_name": "emergency_trauma",
                "display_name": "应急指导-外伤处理",
                "enable_thinking": False,
                "description": "外伤处理应急指导的LLM配置"
            },
            {
                "module_name": "emergency_poisoning",
                "display_name": "应急指导-中毒处理",
                "enable_thinking": False,
                "description": "中毒处理应急指导的LLM配置"
            },
            {
                "module_name": "emergency_burn",
                "display_name": "应急指导-烧伤处理",
                "enable_thinking": False,
                "description": "烧伤处理应急指导的LLM配置"
            }
        ]
        
        created_configs = []
        for config_data in required_configs:
            existing = db.query(LLMConfig).filter(
                LLMConfig.module_name == config_data["module_name"]
            ).first()
            
            if not existing:
                print(f"创建缺失的配置: {config_data['display_name']}")
                new_config = LLMConfig(
                    id=generate_session_id(),
                    module_name=config_data["module_name"],
                    display_name=config_data["display_name"],
                    api_key="sk-693ef3cef5b742c59ae610dec7295199",  # 默认API密钥
                    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                    model_name="qwen-plus",
                    temperature="0.7",
                    max_tokens="2000",
                    is_enabled=True,
                    enable_thinking=config_data["enable_thinking"],
                    description=config_data["description"]
                )
                db.add(new_config)
                created_configs.append(config_data["display_name"])
        
        # 提交所有更改
        db.commit()
        print("LLM配置迁移完成！")
        
        # 显示当前配置
        print("\n=== 当前LLM配置 ===")
        configs = db.query(LLMConfig).order_by(LLMConfig.module_name).all()
        for config in configs:
            thinking_status = "✅" if config.enable_thinking else "❌"
            enabled_status = "启用" if config.is_enabled else "禁用"
            print(f"{config.display_name}: {enabled_status}, 思考功能: {thinking_status}")
        print("==================")
        
    except Exception as e:
        print(f"迁移失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    migrate_llm_config() 