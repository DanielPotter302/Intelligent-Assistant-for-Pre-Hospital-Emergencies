#!/usr/bin/env python3
"""
测试流式输出功能
"""
import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.ai_service import ai_service

async def test_streaming():
    """测试流式输出功能"""
    print("=== 测试知识库检索模式（无思考）===")
    messages = [
        {"role": "user", "content": "心肺复苏的基本步骤是什么？"}
    ]
    
    async for chunk in ai_service.chat_completion_stream(messages, mode="kb"):
        if chunk["type"] == "answer":
            print(chunk["content"], end="", flush=True)
        elif chunk["type"] == "done":
            print("\n[完成]")
            break
        elif chunk["type"] == "error":
            print(f"\n[错误]: {chunk['message']}")
            break
    
    print("\n" + "="*50)
    print("=== 测试复杂问答模式（有思考）===")
    messages = [
        {"role": "user", "content": "在高速公路上发生车祸，如何进行现场急救？"}
    ]
    
    async for chunk in ai_service.chat_completion_stream(messages, mode="graph"):
        if chunk["type"] == "thinking":
            print(f"[思考]: {chunk['content']}", end="", flush=True)
        elif chunk["type"] == "answer_start":
            print("\n[回答开始]")
        elif chunk["type"] == "answer":
            print(chunk["content"], end="", flush=True)
        elif chunk["type"] == "done":
            print("\n[完成]")
            break
        elif chunk["type"] == "error":
            print(f"\n[错误]: {chunk['message']}")
            break
    
    print("\n" + "="*50)
    print("=== 测试智能分诊模式 ===")
    messages = [
        {"role": "user", "content": "患者胸痛，血压150/90，心率100，需要分诊评估"}
    ]
    
    async for chunk in ai_service.chat_completion_stream(messages, mode="triage"):
        if chunk["type"] == "answer":
            print(chunk["content"], end="", flush=True)
        elif chunk["type"] == "done":
            print("\n[完成]")
            break
        elif chunk["type"] == "error":
            print(f"\n[错误]: {chunk['message']}")
            break
    
    print("\n" + "="*50)
    print("=== 测试应急指导模式 ===")
    messages = [
        {"role": "user", "content": "患者突然倒地，意识不清，如何进行急救？"}
    ]
    
    async for chunk in ai_service.chat_completion_stream(messages, mode="emergency"):
        if chunk["type"] == "answer":
            print(chunk["content"], end="", flush=True)
        elif chunk["type"] == "done":
            print("\n[完成]")
            break
        elif chunk["type"] == "error":
            print(f"\n[错误]: {chunk['message']}")
            break

if __name__ == "__main__":
    print("开始测试流式输出功能...")
    asyncio.run(test_streaming())
    print("\n测试完成！") 