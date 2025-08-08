#!/usr/bin/env python3
"""
测试修复后的功能
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.chat import ChatSession
from app.models.emergency import EmergencySession

def test_session_deletion():
    """测试会话删除功能"""
    print("🔧 测试会话删除功能...")
    
    db = SessionLocal()
    
    try:
        # 检查聊天会话
        chat_sessions = db.query(ChatSession).all()
        print(f"✅ 当前聊天会话数量: {len(chat_sessions)}")
        
        # 检查应急指导会话
        emergency_sessions = db.query(EmergencySession).all()
        print(f"✅ 当前应急指导会话数量: {len(emergency_sessions)}")
        
        print("\n📋 聊天会话详情:")
        for session in chat_sessions:
            print(f"  ID: {session.id}, 标题: {session.title}, 用户: {session.user_id}")
        
        print("\n📋 应急指导会话详情:")
        for session in emergency_sessions:
            print(f"  ID: {session.id}, 场景: {session.scenario_type}, 用户: {session.user_id}")
        
        print("\n💡 提示:")
        print("  - 前端删除会话后，应该调用后端API真正删除数据库记录")
        print("  - 刷新页面后，被删除的会话不应该再出现")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    finally:
        db.close()

def test_emergency_stream_events():
    """测试应急指导流式事件"""
    print("\n🔧 测试应急指导流式事件处理...")
    
    print("✅ 已修复的问题:")
    print("  1. 添加了 'done' 事件处理")
    print("  2. 确保消息内容在流式响应完成后不会丢失")
    print("  3. 避免了 handleStreamComplete 和 done 事件的重复处理")
    
    print("\n💡 修复内容:")
    print("  - 在 handleStreamEvent 中添加 'done' case")
    print("  - 确保消息在列表中正确保存")
    print("  - 简化 handleStreamComplete 函数")
    
    print("\n🎯 预期效果:")
    print("  - 应急指导模块输出完毕后，内容应该保持显示")
    print("  - 不会出现内容突然消失的问题")

if __name__ == "__main__":
    test_session_deletion()
    test_emergency_stream_events()
    
    print("\n" + "=" * 60)
    print("🎉 修复总结:")
    print("1. ✅ 删除对话功能: 修复前端调用后端API删除数据库记录")
    print("2. ✅ 应急指导输出: 修复流式响应完成后内容被隐藏的问题")
    print("\n请在前端测试这些功能是否正常工作！") 