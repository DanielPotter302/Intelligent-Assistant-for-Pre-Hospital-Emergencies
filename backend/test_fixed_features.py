#!/usr/bin/env python3
"""
测试修复后的功能
"""
import asyncio
from app.services.ai_service import AIService

async def test_fixed_features():
    """测试修复后的功能"""
    print("🔧 测试修复后的功能...")
    
    ai_service = AIService()
    
    # 测试消息
    messages = [
        {
            "role": "user",
            "content": "什么是心肺复苏？"
        }
    ]
    
    print("\n=== 测试知识检索模式（应该没有思考过程）===")
    print("发送请求...")
    
    kb_has_thinking = False
    kb_content_length = 0
    
    try:
        async for chunk in ai_service.stream_chat_completion(messages, mode="kb"):
            if chunk["type"] == "thinking":
                kb_has_thinking = True
                print(f"🧠 意外的思考: {chunk['content'][:50]}...")
            elif chunk["type"] == "answer":
                kb_content_length += len(chunk["content"])
                print(chunk["content"], end="", flush=True)
            elif chunk["type"] == "done":
                print(f"\n✅ 完成 - 思考功能: {'启用' if kb_has_thinking else '禁用'}")
                print(f"内容长度: {kb_content_length} 字符")
                break
    except Exception as e:
        print(f"❌ 错误: {e}")
    
    print("\n" + "=" * 60)
    
    print("\n=== 测试复杂问答模式（应该有思考过程）===")
    print("发送请求...")
    
    graph_has_thinking = False
    graph_thinking_length = 0
    graph_content_length = 0
    
    try:
        async for chunk in ai_service.stream_chat_completion(messages, mode="graph"):
            if chunk["type"] == "thinking":
                if not graph_has_thinking:
                    print("🧠 检测到思考过程:")
                    graph_has_thinking = True
                graph_thinking_length += len(chunk["content"])
                print(f"思考: {chunk['content']}", end="", flush=True)
            elif chunk["type"] == "answer_start":
                if graph_has_thinking:
                    print("\n\n💡 开始回答:")
            elif chunk["type"] == "answer":
                graph_content_length += len(chunk["content"])
                print(chunk["content"], end="", flush=True)
            elif chunk["type"] == "done":
                print(f"\n✅ 完成 - 思考功能: {'启用' if graph_has_thinking else '禁用'}")
                if graph_has_thinking:
                    print(f"思考内容长度: {graph_thinking_length} 字符")
                print(f"回答内容长度: {graph_content_length} 字符")
                break
    except Exception as e:
        print(f"❌ 错误: {e}")
    
    print("\n" + "=" * 60)
    print("🔍 测试结果总结:")
    print(f"  知识检索模式: {'✅ 正确（无思考）' if not kb_has_thinking else '❌ 错误（有思考）'}")
    print(f"  复杂问答模式: {'✅ 正确（有思考）' if graph_has_thinking else '❌ 错误（无思考）'}")
    
    if not kb_has_thinking and graph_has_thinking:
        print("\n🎉 所有功能修复成功！")
    else:
        print("\n⚠️ 仍有问题需要修复")

if __name__ == "__main__":
    asyncio.run(test_fixed_features()) 