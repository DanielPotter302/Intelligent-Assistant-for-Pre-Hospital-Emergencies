#!/usr/bin/env python3
"""
检查应急指导数据库中的消息情况
"""

import sys
import os

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app.core.database import get_db
from app.models.emergency import EmergencySession, EmergencyMessage

def main():
    print("🔍 检查应急指导数据库中的消息情况...")
    
    db = next(get_db())
    
    # 获取所有会话
    sessions = db.query(EmergencySession).all()
    print(f"\n📊 总会话数: {len(sessions)}")
    
    problem_sessions = []
    
    for session in sessions:
        messages = db.query(EmergencyMessage).filter(
            EmergencyMessage.session_id == session.id
        ).order_by(EmergencyMessage.created_at.asc()).all()
        
        user_msgs = [m for m in messages if m.role == 'user']
        ai_msgs = [m for m in messages if m.role == 'assistant']
        
        print(f"\n会话 {session.id[:8]}... ({session.title})")
        print(f"  用户消息: {len(user_msgs)} 条")
        print(f"  AI消息: {len(ai_msgs)} 条")
        print(f"  总消息: {len(messages)} 条")
        
        # 检查是否有问题
        if len(user_msgs) > len(ai_msgs):
            print(f"  ⚠️  发现问题: 用户消息多于AI消息")
            problem_sessions.append(session.id)
            
            print("  详细消息:")
            for i, msg in enumerate(messages):
                print(f"    {i+1}. [{msg.role}] {msg.content[:60]}...")
                if msg.role == 'assistant' and msg.steps:
                    print(f"       步骤: {msg.steps}")
        
        # 检查是否有自动添加的系统消息
        system_msgs = [m for m in messages if m.role == 'assistant' and '您正在处理' in m.content]
        if system_msgs:
            print(f"  🤖 发现系统自动消息: {len(system_msgs)} 条")
            for msg in system_msgs:
                print(f"    系统消息: {msg.content}")
    
    print(f"\n📋 总结:")
    print(f"  总会话数: {len(sessions)}")
    print(f"  有问题的会话: {len(problem_sessions)}")
    
    if problem_sessions:
        print(f"  问题会话ID: {problem_sessions}")
        print("\n💡 建议:")
        print("  1. 这些会话可能是在AI消息保存功能修复前创建的")
        print("  2. 可以删除这些有问题的会话")
        print("  3. 或者手动补充缺失的AI回复")
    else:
        print("  ✅ 所有会话的消息都正常")

if __name__ == "__main__":
    main() 