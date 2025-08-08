#!/usr/bin/env python3
"""
清理应急指导中的旧系统自动消息
"""

import sys
import os

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app.core.database import get_db
from app.models.emergency import EmergencySession, EmergencyMessage

def main():
    print("🧹 开始清理应急指导中的旧系统自动消息...")
    
    db = next(get_db())
    
    # 查找所有包含系统自动消息的记录
    system_messages = db.query(EmergencyMessage).filter(
        EmergencyMessage.role == "assistant",
        EmergencyMessage.content.like("%您正在处理%情况。请描述具体情况，我将为您提供专业的应急指导。%")
    ).all()
    
    print(f"\n📊 找到 {len(system_messages)} 条系统自动消息")
    
    if len(system_messages) == 0:
        print("✅ 没有需要清理的系统消息")
        return
    
    # 显示将要删除的消息
    for msg in system_messages:
        session = db.query(EmergencySession).filter(
            EmergencySession.id == msg.session_id
        ).first()
        
        print(f"\n会话: {session.title if session else 'Unknown'}")
        print(f"  消息ID: {msg.id}")
        print(f"  内容: {msg.content[:80]}...")
        print(f"  创建时间: {msg.created_at}")
    
    # 确认删除
    confirm = input(f"\n❓ 确定要删除这 {len(system_messages)} 条系统消息吗？(y/N): ")
    
    if confirm.lower() != 'y':
        print("❌ 取消删除操作")
        return
    
    # 执行删除
    deleted_count = 0
    for msg in system_messages:
        try:
            db.delete(msg)
            deleted_count += 1
            print(f"✅ 删除消息: {msg.id}")
        except Exception as e:
            print(f"❌ 删除消息失败 {msg.id}: {e}")
    
    # 提交更改
    try:
        db.commit()
        print(f"\n🎉 成功删除 {deleted_count} 条系统消息")
    except Exception as e:
        db.rollback()
        print(f"❌ 提交更改失败: {e}")
    
    # 验证清理结果
    remaining_system_messages = db.query(EmergencyMessage).filter(
        EmergencyMessage.role == "assistant",
        EmergencyMessage.content.like("%您正在处理%情况。请描述具体情况，我将为您提供专业的应急指导。%")
    ).all()
    
    if len(remaining_system_messages) == 0:
        print("✅ 所有系统消息已清理完成")
    else:
        print(f"⚠️  仍有 {len(remaining_system_messages)} 条系统消息未清理")

if __name__ == "__main__":
    main() 