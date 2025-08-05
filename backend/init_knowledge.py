#!/usr/bin/env python3
"""
知识库初始化脚本
从 classified_grouped_aggregated.txt 文件中导入知识库分类和内容
"""

import re
import os
import sys
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.knowledge import KnowledgeCategory, KnowledgeItem, VideoLink, BookLink
from app.models import knowledge

# 确保数据库表存在
knowledge.Base.metadata.create_all(bind=engine)

def parse_knowledge_file(file_path: str):
    """解析知识库文本文件"""
    categories = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式分割分类
    category_sections = re.split(r'## 分类: (.+?)（共 (\d+) 条）', content)
    
    for i in range(1, len(category_sections), 3):
        if i + 2 < len(category_sections):
            category_name = category_sections[i].strip()
            item_count = int(category_sections[i + 1])
            items_content = category_sections[i + 2].strip()
            
            # 解析该分类下的知识条目
            items = []
            item_matches = re.findall(r'\[(\d+)\] (.+?)(?=\[\d+\]|$)', items_content, re.DOTALL)
            
            for item_num, item_content in item_matches:
                items.append({
                    'number': int(item_num),
                    'content': item_content.strip()
                })
            
            categories.append({
                'name': category_name,
                'item_count': item_count,
                'items': items
            })
    
    return categories

def init_knowledge_categories(db: Session, categories_data):
    """初始化知识库分类"""
    print("正在初始化知识库分类...")
    
    # 清空现有数据
    db.query(KnowledgeItem).delete()
    db.query(KnowledgeCategory).delete()
    db.commit()
    
    # 创建分类
    category_map = {}
    for cat_data in categories_data:
        category = KnowledgeCategory(
            name=cat_data['name'],
            description=f"{cat_data['name']}相关急救知识",
            sort_order=len(category_map) + 1
        )
        db.add(category)
        db.commit()
        db.refresh(category)
        category_map[cat_data['name']] = category
        print(f"创建分类: {cat_data['name']}")
    
    return category_map

def init_knowledge_items(db: Session, categories_data, category_map):
    """初始化知识库内容"""
    print("正在初始化知识库内容...")
    
    for cat_data in categories_data:
        category = category_map[cat_data['name']]
        
        for item in cat_data['items']:
            knowledge_item = KnowledgeItem(
                category_id=category.id,
                title=f"{cat_data['name']} - 第{item['number']}条",
                content=item['content'],
                content_type="document",
                author="急救医学专家团队",
                description=item['content'][:100] + "..." if len(item['content']) > 100 else item['content']
            )
            db.add(knowledge_item)
        
        print(f"导入 {cat_data['name']} 分类下的 {len(cat_data['items'])} 条知识")
    
    db.commit()

def init_video_links(db: Session):
    """初始化视频链接"""
    print("正在初始化视频链接...")
    
    # 清空现有视频链接
    db.query(VideoLink).delete()
    
    # 急救指南分类下的视频
    emergency_category = db.query(KnowledgeCategory).filter(
        KnowledgeCategory.name == "创伤与现场急救处理"
    ).first()
    
    if emergency_category:
        videos = [
            {
                "title": "海姆立克急救法",
                "description": "海姆立克急救法教学视频",
                "video_url": "https://v.douyin.com/rfcywojiLw8/",
                "sort_order": 1
            },
            {
                "title": "心肺复苏",
                "description": "心肺复苏操作教学视频",
                "video_url": "https://v.douyin.com/LSzCMOBDr-w/",
                "sort_order": 2
            },
            {
                "title": "人工呼吸",
                "description": "人工呼吸操作教学视频",
                "video_url": "https://v.douyin.com/-cy50vjdfrA/",
                "sort_order": 3
            },
            {
                "title": "急救止血包扎",
                "description": "急救止血包扎操作教学视频",
                "video_url": "https://v.douyin.com/CG9bKdtbzYA/",
                "sort_order": 4
            },
            {
                "title": "包扎方法",
                "description": "各种包扎方法教学视频",
                "video_url": "https://v.douyin.com/fJ-OlmDkH94/",
                "sort_order": 5
            },
            {
                "title": "骨折后处理",
                "description": "骨折后处理操作教学视频",
                "video_url": "https://v.douyin.com/ovxyNsNoGOU/",
                "sort_order": 6
            }
        ]
        
        for video_data in videos:
            video = VideoLink(
                title=video_data["title"],
                description=video_data["description"],
                video_url=video_data["video_url"],
                category_id=emergency_category.id,
                sort_order=video_data["sort_order"]
            )
            db.add(video)
        
        print(f"导入 {len(videos)} 个视频链接")
    
    db.commit()

def init_book_links(db: Session):
    """初始化书籍链接"""
    print("正在初始化书籍链接...")
    
    # 清空现有书籍链接
    db.query(BookLink).delete()
    
    books = [
        {
            "title": "实用院前急救手册",
            "author": "急救医学专家团队",
            "description": "实用的院前急救操作手册，包含各种急救技能和操作要点",
            "cover_url": "/picture/实用院前急救手册.jpg",
            "book_url": "https://pan.baidu.com/s/1example1",
            "sort_order": 1
        },
        {
            "title": "新编院前急救手册",
            "author": "急救医学专家团队",
            "description": "新版院前急救手册，更新了最新的急救技术和操作规范",
            "cover_url": "/picture/新编院前急救手册.jpg",
            "book_url": "https://pan.baidu.com/s/1example2",
            "sort_order": 2
        }
    ]
    
    for book_data in books:
        book = BookLink(
            title=book_data["title"],
            author=book_data["author"],
            description=book_data["description"],
            cover_url=book_data["cover_url"],
            book_url=book_data["book_url"],
            sort_order=book_data["sort_order"]
        )
        db.add(book)
    
    print(f"导入 {len(books)} 个书籍链接")
    db.commit()

def main():
    """主函数"""
    print("开始初始化知识库...")
    
    # 检查文件是否存在
    file_path = "../classified_grouped_aggregated.txt"
    if not os.path.exists(file_path):
        print(f"错误: 找不到文件 {file_path}")
        sys.exit(1)
    
    # 解析知识库文件
    print("正在解析知识库文件...")
    categories_data = parse_knowledge_file(file_path)
    print(f"解析完成，共找到 {len(categories_data)} 个分类")
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 初始化分类
        category_map = init_knowledge_categories(db, categories_data)
        
        # 初始化知识内容
        init_knowledge_items(db, categories_data, category_map)
        
        # 初始化视频链接
        init_video_links(db)
        
        # 初始化书籍链接
        init_book_links(db)
        
        print("知识库初始化完成！")
        
    except Exception as e:
        print(f"初始化过程中出现错误: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main() 