#!/usr/bin/env python3
"""
检查会话的详细信息
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.user import User
from app.models.chat import ChatSession, ChatMessage

def check_session_details():
    """检查会话的详细信息"""
    print("🔧 检查会话的详细信息...")
    
    db = SessionLocal()
    
    try:
        # 获取所有用户
        users = db.query(User).all()
        print(f"📊 数据库中的用户:")
        user_map = {}
        for user in users:
            user_map[user.id] = user.username
            print(f"  - {user.username} (ID: {user.id})")
        
        # 获取所有会话
        sessions = db.query(ChatSession).all()
        print(f"\n📊 数据库中的会话详情:")
        for session in sessions:
            username = user_map.get(session.user_id, "未知用户")
            print(f"  - 标题: {session.title}")
            print(f"    ID: {session.id}")
            print(f"    用户: {username} ({session.user_id})")
            print(f"    模式: {session.mode}")
            print(f"    创建时间: {session.created_at}")
            print(f"    更新时间: {session.updated_at}")
            
            # 获取消息数量
            message_count = db.query(ChatMessage).filter(ChatMessage.session_id == session.id).count()
            print(f"    消息数量: {message_count}")
            print()
        
        # 检查admin用户的会话
        admin_user = db.query(User).filter(User.username == "admin").first()
        if admin_user:
            admin_sessions = db.query(ChatSession).filter(ChatSession.user_id == admin_user.id).all()
            print(f"📋 admin用户的会话: {len(admin_sessions)} 个")
            for session in admin_sessions:
                print(f"  - {session.title} (模式: {session.mode})")
        
        # 检查danielpotter用户的会话
        daniel_user = db.query(User).filter(User.username == "danielpotter").first()
        if daniel_user:
            daniel_sessions = db.query(ChatSession).filter(ChatSession.user_id == daniel_user.id).all()
            print(f"📋 danielpotter用户的会话: {len(daniel_sessions)} 个")
            for session in daniel_sessions:
                print(f"  - {session.title} (模式: {session.mode})")
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_session_details() 