#!/usr/bin/env python3
"""
直接查询数据库测试LLM配置
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.llm_config import LLMConfig

def test_db_config():
    """测试数据库中的LLM配置"""
    print("🔧 测试数据库中的LLM配置...")
    
    db = SessionLocal()
    
    try:
        # 获取所有配置
        configs = db.query(LLMConfig).order_by(LLMConfig.module_name).all()
        
        print(f"✅ 数据库中共有 {len(configs)} 个配置")
        print("\n📋 配置详情:")
        print("-" * 80)
        
        for config in configs:
            thinking_status = "✅ 启用" if config.enable_thinking else "❌ 禁用"
            enabled_status = "✅ 启用" if config.is_enabled else "❌ 禁用"
            
            print(f"显示名称: {config.display_name}")
            print(f"模块名称: {config.module_name}")
            print(f"模型名称: {config.model_name}")
            print(f"状态: {enabled_status}")
            print(f"思考功能: {thinking_status}")
            print(f"描述: {config.description or '无'}")
            print("-" * 80)
        
        # 重点检查智能问答配置
        print("\n🔍 智能问答配置检查:")
        chat_kb = db.query(LLMConfig).filter(LLMConfig.module_name == "chat_kb").first()
        chat_graph = db.query(LLMConfig).filter(LLMConfig.module_name == "chat_graph").first()
        
        if chat_kb:
            print(f"✅ 知识检索 (chat_kb): 思考功能 {'启用' if chat_kb.enable_thinking else '禁用'}")
        else:
            print("❌ 未找到知识检索配置 (chat_kb)")
            
        if chat_graph:
            print(f"✅ 复杂问答 (chat_graph): 思考功能 {'启用' if chat_graph.enable_thinking else '禁用'}")
        else:
            print("❌ 未找到复杂问答配置 (chat_graph)")
        
        # 检查字段完整性
        print("\n🔍 字段完整性检查:")
        for config in configs:
            missing_fields = []
            if not hasattr(config, 'enable_thinking') or config.enable_thinking is None:
                missing_fields.append('enable_thinking')
            if not hasattr(config, 'is_enabled') or config.is_enabled is None:
                missing_fields.append('is_enabled')
            
            if missing_fields:
                print(f"⚠️ {config.display_name}: 缺少字段 {missing_fields}")
            else:
                print(f"✅ {config.display_name}: 字段完整")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_db_config() 