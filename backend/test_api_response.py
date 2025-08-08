#!/usr/bin/env python3
"""
测试API响应是否包含enable_thinking字段
"""
import requests
import json

def test_llm_config_api():
    """测试LLM配置API"""
    print("🔧 测试LLM配置API响应...")
    
    # API基础URL
    base_url = "http://localhost:8000"
    
    try:
        # 获取所有配置
        response = requests.get(f"{base_url}/api/admin/llm/configs")
        
        if response.status_code == 200:
            data = response.json()
            configs = data.get("data", [])
            
            print(f"✅ 成功获取 {len(configs)} 个配置")
            
            # 检查每个配置是否包含enable_thinking字段
            for config in configs:
                module_name = config.get("module_name", "unknown")
                enable_thinking = config.get("enable_thinking")
                display_name = config.get("display_name", "unknown")
                
                thinking_status = "✅ 启用" if enable_thinking else "❌ 禁用"
                print(f"  {display_name} ({module_name}): 思考功能 {thinking_status}")
            
            # 特别检查chat_kb和chat_graph配置
            chat_kb = next((c for c in configs if c.get("module_name") == "chat_kb"), None)
            chat_graph = next((c for c in configs if c.get("module_name") == "chat_graph"), None)
            
            print("\n🔍 重点检查:")
            if chat_kb:
                print(f"  知识检索 (chat_kb): 思考功能 {'✅ 启用' if chat_kb.get('enable_thinking') else '❌ 禁用'}")
            else:
                print("  ⚠️ 未找到chat_kb配置")
                
            if chat_graph:
                print(f"  复杂问答 (chat_graph): 思考功能 {'✅ 启用' if chat_graph.get('enable_thinking') else '❌ 禁用'}")
            else:
                print("  ⚠️ 未找到chat_graph配置")
            
            # 检查API响应格式
            if configs:
                sample_config = configs[0]
                required_fields = ["id", "module_name", "display_name", "enable_thinking", "is_enabled"]
                missing_fields = [field for field in required_fields if field not in sample_config]
                
                if missing_fields:
                    print(f"\n⚠️ API响应缺少字段: {missing_fields}")
                else:
                    print("\n✅ API响应格式正确，包含所有必需字段")
            
        else:
            print(f"❌ API请求失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_llm_config_api() 