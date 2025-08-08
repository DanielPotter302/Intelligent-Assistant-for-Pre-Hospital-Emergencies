#!/usr/bin/env python3
"""
清空数据库中所有用户的聊天记录
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.user import User
from app.models.chat import ChatSession, ChatMessage
from app.models.emergency import EmergencySession, EmergencyMessage

def clear_all_chats():
    """清空数据库中所有用户的聊天记录"""
    print("🔧 开始清空数据库中所有聊天记录...")
    
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
        
        # 按用户分组显示
        user_stats = {}
        for session in all_chat_sessions:
            user = db.query(User).filter(User.id == session.user_id).first()
            username = user.username if user else "未知用户"
            if username not in user_stats:
                user_stats[username] = {"chat_sessions": 0, "emergency_sessions": 0}
            user_stats[username]["chat_sessions"] += 1
        
        for session in all_emergency_sessions:
            user = db.query(User).filter(User.id == session.user_id).first()
            username = user.username if user else "未知用户"
            if username not in user_stats:
                user_stats[username] = {"chat_sessions": 0, "emergency_sessions": 0}
            user_stats[username]["emergency_sessions"] += 1
        
        print(f"\n📋 按用户分组统计:")
        for username, stats in user_stats.items():
            print(f"  - {username}: 聊天会话 {stats['chat_sessions']} 个, 应急指导会话 {stats['emergency_sessions']} 个")
        
        # 显示详细会话信息
        if all_chat_sessions:
            print(f"\n📋 聊天会话详情:")
            for session in all_chat_sessions[:10]:  # 只显示前10个
                user = db.query(User).filter(User.id == session.user_id).first()
                username = user.username if user else "未知用户"
                message_count = db.query(ChatMessage).filter(ChatMessage.session_id == session.id).count()
                print(f"  - [{username}] {session.title} (ID: {session.id[:8]}...) - {message_count} 条消息")
            if len(all_chat_sessions) > 10:
                print(f"  ... 还有 {len(all_chat_sessions) - 10} 个会话")
        
        if all_emergency_sessions:
            print(f"\n📋 应急指导会话详情:")
            for session in all_emergency_sessions:
                user = db.query(User).filter(User.id == session.user_id).first()
                username = user.username if user else "未知用户"
                message_count = db.query(EmergencyMessage).filter(EmergencyMessage.session_id == session.id).count()
                print(f"  - [{username}] {session.title} ({session.scenario_type}) (ID: {session.id[:8]}...) - {message_count} 条消息")
        
        # 确认删除
        if not all_chat_sessions and not all_emergency_sessions:
            print("✅ 数据库中没有聊天记录，无需清空")
            return
        
        print(f"\n⚠️  即将删除所有聊天记录，此操作不可撤销！")
        print(f"总计将删除:")
        print(f"  - 聊天会话: {len(all_chat_sessions)} 个")
        print(f"  - 聊天消息: {len(all_chat_messages)} 条")
        print(f"  - 应急指导会话: {len(all_emergency_sessions)} 个")
        print(f"  - 应急指导消息: {len(all_emergency_messages)} 条")
        
        confirm = input("\n请输入 'DELETE_ALL' 确认删除所有记录: ")
        
        if confirm != 'DELETE_ALL':
            print("❌ 操作已取消")
            return
        
        print("\n🗑️  开始删除...")
        
        # 删除所有聊天消息
        deleted_chat_messages = 0
        for message in all_chat_messages:
            db.delete(message)
            deleted_chat_messages += 1
        
        # 删除所有应急指导消息
        deleted_emergency_messages = 0
        for message in all_emergency_messages:
            db.delete(message)
            deleted_emergency_messages += 1
        
        # 删除所有聊天会话
        deleted_chat_sessions = 0
        for session in all_chat_sessions:
            db.delete(session)
            deleted_chat_sessions += 1
        
        # 删除所有应急指导会话
        deleted_emergency_sessions = 0
        for session in all_emergency_sessions:
            db.delete(session)
            deleted_emergency_sessions += 1
        
        # 提交更改
        db.commit()
        
        print(f"\n🎉 清空完成！")
        print(f"✅ 删除统计:")
        print(f"  - 聊天会话: {deleted_chat_sessions} 个")
        print(f"  - 聊天消息: {deleted_chat_messages} 条")
        print(f"  - 应急指导会话: {deleted_emergency_sessions} 个")
        print(f"  - 应急指导消息: {deleted_emergency_messages} 条")
        
        # 验证删除结果
        remaining_chat_sessions = db.query(ChatSession).count()
        remaining_chat_messages = db.query(ChatMessage).count()
        remaining_emergency_sessions = db.query(EmergencySession).count()
        remaining_emergency_messages = db.query(EmergencyMessage).count()
        
        print(f"\n🔍 验证结果:")
        print(f"  - 剩余聊天会话: {remaining_chat_sessions} 个")
        print(f"  - 剩余聊天消息: {remaining_chat_messages} 条")
        print(f"  - 剩余应急指导会话: {remaining_emergency_sessions} 个")
        print(f"  - 剩余应急指导消息: {remaining_emergency_messages} 条")
        
        if (remaining_chat_sessions == 0 and remaining_chat_messages == 0 and 
            remaining_emergency_sessions == 0 and remaining_emergency_messages == 0):
            print(f"✅ 验证成功：所有聊天记录已完全清空")
        else:
            print(f"⚠️  验证失败：仍有记录残留")
        
    except Exception as e:
        print(f"❌ 清空失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clear_all_chats() 