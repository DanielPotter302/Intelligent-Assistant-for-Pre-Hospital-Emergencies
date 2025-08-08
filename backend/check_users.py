#!/usr/bin/env python3
"""
检查数据库中的用户信息
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.user import User

def check_users():
    """检查数据库中的用户信息"""
    print("🔧 检查数据库中的用户信息...")
    
    db = SessionLocal()
    
    try:
        users = db.query(User).all()
        
        print(f"📊 数据库中共有 {len(users)} 个用户:")
        for user in users:
            print(f"  - 用户名: {user.username}")
            print(f"    邮箱: {user.email}")
            print(f"    角色: {user.role}")
            print(f"    状态: {user.status}")
            print(f"    ID: {user.id}")
            print()
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_users() 