#!/usr/bin/env python3
"""
重置danielpotter用户的密码
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def reset_danielpotter_password():
    """重置danielpotter用户的密码"""
    print("🔧 重置danielpotter用户的密码...")
    
    db = SessionLocal()
    
    try:
        # 查找danielpotter用户
        user = db.query(User).filter(User.username == "danielpotter").first()
        if not user:
            print("❌ 找不到danielpotter用户")
            return
        
        print(f"📋 找到用户: {user.username} (ID: {user.id})")
        
        # 重置密码为 "danielpotter123"
        new_password = "danielpotter123"
        user.hashed_password = get_password_hash(new_password)
        
        db.commit()
        
        print(f"✅ 密码已重置为: {new_password}")
        print("🔑 现在可以使用以下凭据登录:")
        print(f"   用户名: danielpotter")
        print(f"   密码: {new_password}")
        
    except Exception as e:
        print(f"❌ 重置失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reset_danielpotter_password() 