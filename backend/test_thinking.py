#!/usr/bin/env python3
"""
测试Qwen3思考功能
"""
import asyncio
from app.services.ai_service import AIService

async def test_thinking_feature():
    """测试思考功能"""
    print("开始测试Qwen3思考功能...")
    
    ai_service = AIService()
    
    # 测试消息
    messages = [
        {
            "role": "user",
            "content": "请分析一个复杂的医疗急救场景：一名50岁男性患者突然倒地，意识不清，呼吸急促，面色苍白，血压90/60mmHg，心率120次/分。请详细分析可能的病因和处理方案。"
        }
    ]
    
    print("\n=== 测试Qwen3思考功能 ===\n")
    print("发送复杂问答请求（graph模式）...")
    print(f"消息: {messages[0]['content'][:50]}...")
    print("=" * 50)
    
    thinking_detected = False
    thinking_content_length = 0
    answer_content_length = 0
    
    try:
        async for chunk in ai_service.stream_chat_completion(messages, mode="graph"):
            if chunk["type"] == "thinking":
                if not thinking_detected:
                    print("🧠 检测到思考过程:")
                    thinking_detected = True
                thinking_content_length += len(chunk["content"])
                print(f"思考: {chunk['content']}", end="", flush=True)
            elif chunk["type"] == "answer_start":
                if thinking_detected:
                    print("\n\n💡 开始回答:")
            elif chunk["type"] == "answer":
                answer_content_length += len(chunk["content"])
                print(chunk["content"], end="", flush=True)
            elif chunk["type"] == "done":
                print("\n\n✅ 回答完成")
                if thinking_detected:
                    print(f"📝 思考内容长度: {thinking_content_length} 字符")
                break
    except Exception as e:
        print(f"❌ 错误: {e}")
    
    print("\n" + "=" * 50)
    print(f"思考功能状态: {'✅ 已启用' if thinking_detected else '❌ 未启用'}")
    print(f"回答内容长度: {answer_content_length} 字符")
    
    # 对比测试：知识库模式（不应该有思考过程）
    print("\n=== 测试知识库模式（对比） ===\n")
    print("发送知识库请求（kb模式）...")
    print("消息: 什么是心肺复苏？")
    print("=" * 30)
    
    kb_thinking_detected = False
    kb_answer_length = 0
    
    try:
        async for chunk in ai_service.stream_chat_completion([{"role": "user", "content": "什么是心肺复苏？"}], mode="kb"):
            if chunk["type"] == "thinking":
                kb_thinking_detected = True
                print(f"🧠 思考: {chunk['content']}", end="", flush=True)
            elif chunk["type"] == "answer_start":
                print("💡 开始回答:")
            elif chunk["type"] == "answer":
                kb_answer_length += len(chunk["content"])
                print(chunk["content"], end="", flush=True)
            elif chunk["type"] == "done":
                print("\n\n✅ 回答完成")
                break
    except Exception as e:
        print(f"❌ 错误: {e}")
    
    print("\n" + "=" * 30)
    print(f"思考功能状态: {'✅ 已启用' if kb_thinking_detected else '❌ 未启用'}")
    
    # 总结
    print("\n" + "=" * 60)
    print("🔍 测试总结:")
    print(f"  复杂问答模式 (graph): {'✅ 思考功能正常' if thinking_detected else '❌ 思考功能未启用'}")
    print(f"  知识库模式 (kb): {'✅ 正常（无思考）' if not kb_thinking_detected else '⚠️ 意外启用了思考功能'}")
    
    if thinking_detected and not kb_thinking_detected:
        print("\n🎉 思考功能配置正确！")
    elif not thinking_detected:
        print("\n⚠️ 复杂问答模式的思考功能未启用，请检查配置")
    elif kb_thinking_detected:
        print("\n⚠️ 知识库模式意外启用了思考功能，请检查配置")

if __name__ == "__main__":
    asyncio.run(test_thinking_feature()) 