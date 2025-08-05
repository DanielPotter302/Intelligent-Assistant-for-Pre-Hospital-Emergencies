#!/usr/bin/env python3
"""
知识库数据初始化脚本
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.knowledge import KnowledgeCategory, KnowledgeItem, VideoLink, BookLink
from app.models.user import User
from app.core.security import get_password_hash

def init_database():
    """初始化数据库表"""
    from app.core.database import Base
    Base.metadata.create_all(bind=engine)

def create_admin_user():
    """创建管理员用户"""
    db = SessionLocal()
    try:
        # 检查是否已存在管理员用户
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin_user = User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                is_active=True,
                is_superuser=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ 管理员用户创建成功")
        else:
            print("ℹ️  管理员用户已存在")
    except Exception as e:
        print(f"❌ 创建管理员用户失败: {e}")
        db.rollback()
    finally:
        db.close()

def create_knowledge_categories():
    """创建知识库分类"""
    db = SessionLocal()
    try:
        # 定义分类
        categories_data = [
            {
                "name": "中毒处理",
                "description": "各种中毒情况的急救处理方法",
                "sort_order": 1
            },
            {
                "name": "创伤与现场急救处理", 
                "description": "外伤、出血、骨折等创伤的现场急救",
                "sort_order": 2
            },
            {
                "name": "呼吸系统急救",
                "description": "呼吸困难、窒息等呼吸系统急症的急救",
                "sort_order": 3
            },
            {
                "name": "妇产儿急救",
                "description": "孕妇、产妇和新生儿的急救处理",
                "sort_order": 4
            },
            {
                "name": "循环系统与心脏急救",
                "description": "心脏骤停、休克等循环系统急症的急救",
                "sort_order": 5
            },
            {
                "name": "消化系统与出血",
                "description": "腹痛、呕血等消化系统急症的急救",
                "sort_order": 6
            },
            {
                "name": "神经系统与意识障碍",
                "description": "昏迷、抽搐等神经系统急症的急救",
                "sort_order": 7
            },
            {
                "name": "通用急救与支持治疗",
                "description": "基础生命支持、转运等通用急救技术",
                "sort_order": 8
            }
        ]
        
        # 创建分类
        for cat_data in categories_data:
            existing = db.query(KnowledgeCategory).filter(KnowledgeCategory.name == cat_data["name"]).first()
            if not existing:
                category = KnowledgeCategory(**cat_data)
                db.add(category)
        
        db.commit()
        print("✅ 知识库分类创建成功")
        
        # 返回分类ID映射
        categories = db.query(KnowledgeCategory).all()
        return {cat.name: cat.id for cat in categories}
        
    except Exception as e:
        print(f"❌ 创建知识库分类失败: {e}")
        db.rollback()
        return {}
    finally:
        db.close()

def import_knowledge_content(category_map):
    """导入知识内容"""
    db = SessionLocal()
    try:
        # 读取文本文件
        text_file = project_root / "classified_grouped_aggregated.txt"
        if not text_file.exists():
            print(f"❌ 找不到文件: {text_file}")
            return
        
        with open(text_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析内容
        sections = content.split('## 分类: ')
        
        for section in sections[1:]:  # 跳过第一个空部分
            lines = section.strip().split('\n')
            if not lines:
                continue
                
            category_name = lines[0].split('（')[0].strip()
            category_id = category_map.get(category_name)
            
            if not category_id:
                print(f"⚠️  未找到分类: {category_name}")
                continue
            
            print(f"📝 处理分类: {category_name}")
            
            # 解析知识条目
            current_item = None
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                
                # 检查是否是新的条目 [数字]
                if line.startswith('[') and ']' in line:
                    # 保存前一个条目
                    if current_item:
                        # 检查是否已存在
                        existing = db.query(KnowledgeItem).filter(
                            KnowledgeItem.title == current_item['title'],
                            KnowledgeItem.category_id == category_id
                        ).first()
                        
                        if not existing:
                            item = KnowledgeItem(**current_item)
                            db.add(item)
                    
                    # 开始新条目
                    item_num = line[1:line.find(']')]
                    content_text = line[line.find(']')+1:].strip()
                    
                    current_item = {
                        'category_id': category_id,
                        'title': f"{category_name} - 条目{item_num}",
                        'content': content_text,
                        'content_type': 'document',
                        'author': '急救医学专家团队',
                        'view_count': 0,
                        'status': 'active'
                    }
                else:
                    # 继续当前条目的内容
                    if current_item:
                        current_item['content'] += '\n' + line
            
            # 保存最后一个条目
            if current_item:
                existing = db.query(KnowledgeItem).filter(
                    KnowledgeItem.title == current_item['title'],
                    KnowledgeItem.category_id == category_id
                ).first()
                
                if not existing:
                    item = KnowledgeItem(**current_item)
                    db.add(item)
        
        db.commit()
        print("✅ 知识内容导入成功")
        
    except Exception as e:
        print(f"❌ 导入知识内容失败: {e}")
        db.rollback()
    finally:
        db.close()

def create_video_links(category_map):
    """创建视频链接"""
    db = SessionLocal()
    try:
        # 急救指南分类的视频
        emergency_category_id = category_map.get("创伤与现场急救处理")
        if not emergency_category_id:
            print("⚠️  未找到急救指南分类")
            return
        
        videos_data = [
            {
                "title": "海姆立克急救法",
                "description": "气道异物阻塞的急救方法",
                "video_url": "https://v.douyin.com/rfcywojiLw8/",
                "category_id": emergency_category_id,
                "sort_order": 1
            },
            {
                "title": "心肺复苏",
                "description": "心脏骤停的急救复苏技术",
                "video_url": "https://v.douyin.com/LSzCMOBDr-w/",
                "category_id": emergency_category_id,
                "sort_order": 2
            },
            {
                "title": "人工呼吸",
                "description": "呼吸停止的人工呼吸技术",
                "video_url": "https://v.douyin.com/-cy50vjdfrA/",
                "category_id": emergency_category_id,
                "sort_order": 3
            },
            {
                "title": "急救止血包扎",
                "description": "外伤出血的止血和包扎技术",
                "video_url": "https://v.douyin.com/CG9bKdtbzYA/",
                "category_id": emergency_category_id,
                "sort_order": 4
            },
            {
                "title": "包扎方法",
                "description": "各种伤口的包扎技术",
                "video_url": "https://v.douyin.com/fJ-OlmDkH94/",
                "category_id": emergency_category_id,
                "sort_order": 5
            },
            {
                "title": "骨折后处理",
                "description": "骨折的现场处理和固定技术",
                "video_url": "https://v.douyin.com/ovxyNsNoGOU/",
                "category_id": emergency_category_id,
                "sort_order": 6
            }
        ]
        
        for video_data in videos_data:
            existing = db.query(VideoLink).filter(
                VideoLink.title == video_data["title"],
                VideoLink.category_id == video_data["category_id"]
            ).first()
            
            if not existing:
                video = VideoLink(**video_data)
                db.add(video)
        
        db.commit()
        print("✅ 视频链接创建成功")
        
    except Exception as e:
        print(f"❌ 创建视频链接失败: {e}")
        db.rollback()
    finally:
        db.close()

def create_book_links():
    """创建书籍链接"""
    db = SessionLocal()
    try:
        books_data = [
            {
                "title": "实用院前急救手册",
                "author": "急救医学专家团队",
                "description": "实用的院前急救指导手册，包含各种急症的急救方法",
                "cover_url": "/uploads/books/实用院前急救手册.jpg",
                "book_url": "https://pan.baidu.com/s/1example1",
                "sort_order": 1
            },
            {
                "title": "新编院前急救手册",
                "author": "急救医学专家团队", 
                "description": "新版院前急救手册，更新了最新的急救技术和标准",
                "cover_url": "/uploads/books/新编院前急救手册.jpg",
                "book_url": "https://pan.baidu.com/s/1example2",
                "sort_order": 2
            }
        ]
        
        for book_data in books_data:
            existing = db.query(BookLink).filter(BookLink.title == book_data["title"]).first()
            
            if not existing:
                book = BookLink(**book_data)
                db.add(book)
        
        db.commit()
        print("✅ 书籍链接创建成功")
        
    except Exception as e:
        print(f"❌ 创建书籍链接失败: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """主函数"""
    print("🚀 开始初始化知识库数据...")
    
    # 初始化数据库
    init_database()
    print("✅ 数据库表创建完成")
    
    # 创建管理员用户
    create_admin_user()
    
    # 创建知识库分类
    category_map = create_knowledge_categories()
    
    # 导入知识内容
    import_knowledge_content(category_map)
    
    # 创建视频链接
    create_video_links(category_map)
    
    # 创建书籍链接
    create_book_links()
    
    print("🎉 知识库数据初始化完成！")

if __name__ == "__main__":
    main() 