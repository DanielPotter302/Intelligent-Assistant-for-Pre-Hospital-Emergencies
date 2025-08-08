#!/usr/bin/env python3
"""
清理空内容的AI消息
"""

import sys
import os

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app.core.database import get_db
from app.models.emergency import EmergencyMessage

def main():
    print("🧹 开始清理空内容的AI消息...")
    
    db = next(get_db())
    
    # 查找所有空内容的AI消息
    empty_ai_messages = db.query(EmergencyMessage).filter(
        EmergencyMessage.role == "assistant",
        EmergencyMessage.content.is_(None) | (EmergencyMessage.content == "")
    ).all()
    
    print(f"\n📊 找到 {len(empty_ai_messages)} 条空内容的AI消息")
    
    if len(empty_ai_messages) == 0:
        print("✅ 没有需要清理的空消息")
        return
    
    # 显示将要删除的消息
    for msg in empty_ai_messages:
        print(f"\n消息ID: {msg.id}")
        print(f"  会话ID: {msg.session_id}")
        print(f"  内容: {repr(msg.content)}")
        print(f"  创建时间: {msg.created_at}")
    
    # 确认删除
    confirm = input(f"\n❓ 确定要删除这 {len(empty_ai_messages)} 条空消息吗？(y/N): ")
    
    if confirm.lower() != 'y':
        print("❌ 取消删除操作")
        return
    
    # 执行删除
    deleted_count = 0
    for msg in empty_ai_messages:
        try:
            db.delete(msg)
            deleted_count += 1
            print(f"✅ 删除消息: {msg.id}")
        except Exception as e:
            print(f"❌ 删除消息失败 {msg.id}: {e}")
    
    # 提交更改
    try:
        db.commit()
        print(f"\n🎉 成功删除 {deleted_count} 条空消息")
    except Exception as e:
        db.rollback()
        print(f"❌ 提交更改失败: {e}")
    
    # 验证清理结果
    remaining_empty_messages = db.query(EmergencyMessage).filter(
        EmergencyMessage.role == "assistant",
        EmergencyMessage.content.is_(None) | (EmergencyMessage.content == "")
    ).all()
    
    if len(remaining_empty_messages) == 0:
        print("✅ 所有空消息已清理完成")
    else:
        print(f"⚠️  仍有 {len(remaining_empty_messages)} 条空消息未清理")

if __name__ == "__main__":
    main() 