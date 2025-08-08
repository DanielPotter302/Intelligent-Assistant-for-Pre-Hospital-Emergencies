#!/usr/bin/env python3
"""
直接测试阿里云通义千问API的思考功能
"""
import os
import asyncio
import sqlite3
from openai import AsyncOpenAI

def get_api_key_from_db():
    """从数据库获取API密钥"""
    try:
        conn = sqlite3.connect('pre_hospital_assistant.db')
        cursor = conn.cursor()
        cursor.execute('SELECT api_key, base_url FROM llm_configs WHERE module_name = "chat" AND is_enabled = 1')
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0], result[1]
        return None, None
    except Exception as e:
        print(f"获取API密钥失败: {e}")
        return None, None

async def test_direct_api():
    """直接测试阿里云API"""
    print("=== 直接测试阿里云通义千问API ===\n")
    
    # 从数据库获取API密钥
    api_key, base_url = get_api_key_from_db()
    if not api_key:
        print("❌ 未找到API密钥配置")
        return
    
    print(f"使用API密钥: {api_key[:20]}...")
    print(f"Base URL: {base_url}\n")
    
    # 创建客户端
    client = AsyncOpenAI(
        api_key=api_key,
        base_url=base_url
    )
    
    # 测试消息
    messages = [
        {
            "role": "user",
            "content": "请分析一个复杂的医疗急救场景：一名50岁男性患者突然倒地，意识不清，呼吸急促，面色苍白，血压90/60mmHg，心率120次/分。请详细分析可能的病因和处理方案。"
        }
    ]
    
    print("测试1: 不启用思考模式")
    print("=" * 40)
    
    try:
        completion = await client.chat.completions.create(
            model="qwen-plus",
            messages=messages,
            stream=True,
            temperature=0.7,
            max_tokens=2000
        )
        
        thinking_detected = False
        content_length = 0
        
        async for chunk in completion:
            if hasattr(chunk, 'choices') and chunk.choices:
                choice = chunk.choices[0]
                if hasattr(choice, 'delta') and choice.delta:
                    if hasattr(choice.delta, 'content') and choice.delta.content:
                        content_length += len(choice.delta.content)
                        print(choice.delta.content, end="", flush=True)
                    
                    # 检查是否有思考内容
                    if hasattr(choice.delta, 'reasoning_content') and choice.delta.reasoning_content:
                        thinking_detected = True
                        print(f"\n🧠 思考: {choice.delta.reasoning_content}")
        
        print(f"\n\n结果: 思考功能 {'✅ 检测到' if thinking_detected else '❌ 未检测到'}")
        print(f"内容长度: {content_length} 字符")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
    
    print("\n" + "=" * 60 + "\n")
    
    print("测试2: 启用思考模式")
    print("=" * 40)
    
    try:
        completion = await client.chat.completions.create(
            model="qwen-plus",
            messages=messages,
            stream=True,
            temperature=0.7,
            max_tokens=2000,
            extra_body={
                "enable_thinking": True,
                "thinking_budget": 30000
            }
        )
        
        thinking_detected = False
        content_length = 0
        thinking_length = 0
        
        async for chunk in completion:
            if hasattr(chunk, 'choices') and chunk.choices:
                choice = chunk.choices[0]
                if hasattr(choice, 'delta') and choice.delta:
                    # 检查思考内容
                    if hasattr(choice.delta, 'reasoning_content') and choice.delta.reasoning_content:
                        if not thinking_detected:
                            print("🧠 开始思考:")
                            thinking_detected = True
                        thinking_length += len(choice.delta.reasoning_content)
                        print(choice.delta.reasoning_content, end="", flush=True)
                    
                    # 检查回答内容
                    if hasattr(choice.delta, 'content') and choice.delta.content:
                        if thinking_detected and content_length == 0:
                            print("\n\n💡 开始回答:")
                        content_length += len(choice.delta.content)
                        print(choice.delta.content, end="", flush=True)
        
        print(f"\n\n结果: 思考功能 {'✅ 检测到' if thinking_detected else '❌ 未检测到'}")
        print(f"思考内容长度: {thinking_length} 字符")
        print(f"回答内容长度: {content_length} 字符")
        
    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == "__main__":
    asyncio.run(test_direct_api()) 