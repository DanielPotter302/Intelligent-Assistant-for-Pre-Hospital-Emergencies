#!/usr/bin/env python3
"""
清空指定用户的聊天记录
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.user import User
from app.models.chat import ChatSession, ChatMessage
from app.models.emergency import EmergencySession, EmergencyMessage

def clear_user_chats(username: str):
    """清空指定用户的聊天记录"""
    print(f"🔧 开始清空用户 '{username}' 的聊天记录...")
    
    db = SessionLocal()
    
    try:
        # 查找用户
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print(f"❌ 未找到用户: {username}")
            return
        
        print(f"✅ 找到用户: {user.username} (ID: {user.id})")
        
        # 统计当前记录数
        chat_sessions = db.query(ChatSession).filter(ChatSession.user_id == user.id).all()
        emergency_sessions = db.query(EmergencySession).filter(EmergencySession.user_id == user.id).all()
        
        print(f"📊 当前记录统计:")
        print(f"  - 聊天会话: {len(chat_sessions)} 个")
        print(f"  - 应急指导会话: {len(emergency_sessions)} 个")
        
        # 显示会话详情
        if chat_sessions:
            print(f"\n📋 聊天会话详情:")
            for session in chat_sessions:
                message_count = db.query(ChatMessage).filter(ChatMessage.session_id == session.id).count()
                print(f"  - {session.title} (ID: {session.id[:8]}...) - {message_count} 条消息")
        
        if emergency_sessions:
            print(f"\n📋 应急指导会话详情:")
            for session in emergency_sessions:
                message_count = db.query(EmergencyMessage).filter(EmergencyMessage.session_id == session.id).count()
                print(f"  - {session.title} ({session.scenario_type}) (ID: {session.id[:8]}...) - {message_count} 条消息")
        
        # 确认删除
        if not chat_sessions and not emergency_sessions:
            print("✅ 该用户没有聊天记录，无需清空")
            return
        
        print(f"\n⚠️  即将删除所有记录，此操作不可撤销！")
        confirm = input("请输入 'YES' 确认删除: ")
        
        if confirm != 'YES':
            print("❌ 操作已取消")
            return
        
        # 删除聊天记录
        deleted_chat_messages = 0
        deleted_emergency_messages = 0
        
        # 删除聊天消息和会话
        for session in chat_sessions:
            messages = db.query(ChatMessage).filter(ChatMessage.session_id == session.id).all()
            for message in messages:
                db.delete(message)
                deleted_chat_messages += 1
            db.delete(session)
        
        # 删除应急指导消息和会话
        for session in emergency_sessions:
            messages = db.query(EmergencyMessage).filter(EmergencyMessage.session_id == session.id).all()
            for message in messages:
                db.delete(message)
                deleted_emergency_messages += 1
            db.delete(session)
        
        # 提交更改
        db.commit()
        
        print(f"\n🎉 清空完成！")
        print(f"✅ 删除统计:")
        print(f"  - 聊天会话: {len(chat_sessions)} 个")
        print(f"  - 聊天消息: {deleted_chat_messages} 条")
        print(f"  - 应急指导会话: {len(emergency_sessions)} 个")
        print(f"  - 应急指导消息: {deleted_emergency_messages} 条")
        
        # 验证删除结果
        remaining_chat_sessions = db.query(ChatSession).filter(ChatSession.user_id == user.id).count()
        remaining_emergency_sessions = db.query(EmergencySession).filter(EmergencySession.user_id == user.id).count()
        
        if remaining_chat_sessions == 0 and remaining_emergency_sessions == 0:
            print(f"✅ 验证成功：用户 '{username}' 的所有聊天记录已清空")
        else:
            print(f"⚠️  验证失败：仍有 {remaining_chat_sessions} 个聊天会话和 {remaining_emergency_sessions} 个应急指导会话")
        
    except Exception as e:
        print(f"❌ 清空失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: python clear_user_chats.py <username>")
        print("示例: python clear_user_chats.py danielpotter")
        sys.exit(1)
    
    username = sys.argv[1]
    clear_user_chats(username) 