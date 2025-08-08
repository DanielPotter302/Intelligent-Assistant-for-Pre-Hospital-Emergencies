#!/usr/bin/env python3
"""
检查当前数据库中的聊天记录
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.user import User
from app.models.chat import ChatSession, ChatMessage
from app.models.emergency import EmergencySession, EmergencyMessage

def check_current_chats():
    """检查当前数据库中的聊天记录"""
    print("🔧 检查当前数据库中的聊天记录...")
    
    db = SessionLocal()
    
    try:
        # 统计当前记录数
        all_chat_sessions = db.query(ChatSession).all()
        all_emergency_sessions = db.query(EmergencySession).all()
        all_chat_messages = db.query(ChatMessage).all()
        all_emergency_messages = db.query(EmergencyMessage).all()
        
        print(f"📊 当前数据库统计:")
        print(f"  - 聊天会话: {len(all_chat_sessions)} 个")
        print(f"  - 聊天消息: {len(all_chat_messages)} 条")
        print(f"  - 应急指导会话: {len(all_emergency_sessions)} 个")
        print(f"  - 应急指导消息: {len(all_emergency_messages)} 条")
        
        if all_chat_sessions:
            print(f"\n📋 聊天会话详情:")
            for session in all_chat_sessions:
                user = db.query(User).filter(User.id == session.user_id).first()
                username = user.username if user else "未知用户"
                messages = db.query(ChatMessage).filter(ChatMessage.session_id == session.id).all()
                print(f"  - [{username}] {session.title} (ID: {session.id[:8]}...) - {len(messages)} 条消息")
                
                # 显示消息详情
                for i, msg in enumerate(messages[:3]):  # 只显示前3条消息
                    content_preview = msg.content[:50] + "..." if len(msg.content) > 50 else msg.content
                    print(f"    {i+1}. [{msg.role}] {content_preview}")
                if len(messages) > 3:
                    print(f"    ... 还有 {len(messages) - 3} 条消息")
                print()
        
        if all_emergency_sessions:
            print(f"\n📋 应急指导会话详情:")
            for session in all_emergency_sessions:
                user = db.query(User).filter(User.id == session.user_id).first()
                username = user.username if user else "未知用户"
                messages = db.query(EmergencyMessage).filter(EmergencyMessage.session_id == session.id).all()
                print(f"  - [{username}] {session.title} ({session.scenario_type}) (ID: {session.id[:8]}...) - {len(messages)} 条消息")
                
                # 显示消息详情
                for i, msg in enumerate(messages[:3]):  # 只显示前3条消息
                    content_preview = msg.content[:50] + "..." if len(msg.content) > 50 else msg.content
                    print(f"    {i+1}. [{msg.role}] {content_preview}")
                if len(messages) > 3:
                    print(f"    ... 还有 {len(messages) - 3} 条消息")
                print()
        
        if not all_chat_sessions and not all_emergency_sessions:
            print("✅ 数据库中没有聊天记录")
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_current_chats() 