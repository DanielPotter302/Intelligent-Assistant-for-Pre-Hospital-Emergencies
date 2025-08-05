#!/usr/bin/env python3
"""
数据库初始化脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import create_tables, SessionLocal
from app.core.security import get_password_hash, generate_user_id
from app.models.user import User
from app.models.knowledge import KnowledgeCategory, KnowledgeItem
from app.models.message import ContactMessage
from datetime import datetime

def init_database():
    """初始化数据库"""
    print("正在创建数据库表...")
    create_tables()
    print("数据库表创建完成")
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 清除所有现有用户
        print("正在清除现有用户数据...")
        db.query(User).delete()
        db.commit()
        print("现有用户数据已清除")
        
        # 创建管理员用户
        print("正在创建管理员用户...")
        admin_user = User(
            id=generate_user_id(),
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            role="admin",
            real_name="系统管理员",
            status="active",
            email_verified=True
        )
        db.add(admin_user)
        print("管理员用户创建完成 (用户名: admin, 密码: admin123)")
        
        # 创建普通用户danielpotter
        print("正在创建普通用户...")
        daniel_user = User(
                id=generate_user_id(),
            username="danielpotter",
            email="danielpotter@example.com",
            hashed_password=get_password_hash("danielpotter123"),
                role="user",
            real_name="Daniel Potter",
                status="active",
                email_verified=True
            )
        db.add(daniel_user)
        print("普通用户创建完成 (用户名: danielpotter, 密码: danielpotter123)")
        
        # 创建知识库分类
        categories_data = [
            {"name": "急救指南", "description": "各类急救处理指南", "sort_order": 1},
            {"name": "医疗设备", "description": "医疗设备使用说明", "sort_order": 2},
            {"name": "药物手册", "description": "常用药物使用指南", "sort_order": 3},
            {"name": "培训视频", "description": "医疗培训视频资源", "sort_order": 4},
            {"name": "法规标准", "description": "医疗相关法规标准", "sort_order": 5}
        ]
        
        for cat_data in categories_data:
            existing_cat = db.query(KnowledgeCategory).filter(
                KnowledgeCategory.name == cat_data["name"]
            ).first()
            
            if not existing_cat:
                category = KnowledgeCategory(**cat_data, status="active")
                db.add(category)
        
        # 创建示例知识库内容
        knowledge_items_data = [
            {
                "category_id": 1,
                "title": "心肺复苏术(CPR)操作指南",
                "content": "心肺复苏术(CPR)是一种紧急医疗技术，用于在心脏骤停时维持血液循环和呼吸。本指南详细介绍了CPR的操作步骤、注意事项和最新标准。",
                "content_type": "document",
                "author": "中华医学会",
                "description": "详细的心肺复苏术操作步骤和注意事项",
                "status": "active"
            },
            {
                "category_id": 1,
                "title": "外伤急救处理手册",
                "content": "外伤急救是院前急救的重要组成部分，包括止血、包扎、固定、搬运等基本技能。本手册涵盖了各类外伤的紧急处理方法。",
                "content_type": "document",
                "author": "急救医学专家组",
                "publisher": "医学出版社",
                "description": "各类外伤的紧急处理方法",
                "status": "active"
            },
            {
                "category_id": 4,
                "title": "急救技能培训视频",
                "content": "本视频系列涵盖了急救技能的核心内容，包括心肺复苏、止血包扎、骨折固定等操作演示，适合医护人员和急救志愿者学习。",
                "content_type": "document",
                "author": "医疗培训中心",
                "description": "专业的急救技能演示视频",
                "status": "active"
            }
        ]
        
        for item_data in knowledge_items_data:
            existing_item = db.query(KnowledgeItem).filter(
                KnowledgeItem.title == item_data["title"]
            ).first()
            
            if not existing_item:
                item = KnowledgeItem(**item_data)
                db.add(item)
        
        # 提交所有更改
        db.commit()
        print("数据库初始化完成！")
        
        print("\n=== 系统信息 ===")
        print("管理员账号: admin / admin123")
        print("普通用户账号: danielpotter / danielpotter123")
        print("API文档: http://localhost:8000/docs")
        print("==================")
        
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database() 