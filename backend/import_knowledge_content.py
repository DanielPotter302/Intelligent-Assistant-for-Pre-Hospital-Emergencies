#!/usr/bin/env python3
"""
知识内容导入脚本
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.knowledge import KnowledgeCategory, KnowledgeItem

def import_knowledge_content():
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
        
        # 获取分类映射
        categories = db.query(KnowledgeCategory).all()
        category_map = {cat.name: cat.id for cat in categories}
        
        total_items = 0
        
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
                            total_items += 1
                    
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
                    total_items += 1
        
        db.commit()
        print(f"✅ 知识内容导入成功，共导入 {total_items} 条内容")
        
    except Exception as e:
        print(f"❌ 导入知识内容失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 开始导入知识内容...")
    import_knowledge_content()
    print("🎉 知识内容导入完成！") 