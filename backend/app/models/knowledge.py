from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON, Integer, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class KnowledgeCategory(Base):
    __tablename__ = "knowledge_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey("knowledge_categories.id"), nullable=True)
    sort_order = Column(Integer, default=0, nullable=False)
    status = Column(String(20), default="active", nullable=False)  # active, inactive
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # 关系
    children = relationship("KnowledgeCategory", backref="parent", remote_side=[id])
    items = relationship("KnowledgeItem", back_populates="category")
    
    def __repr__(self):
        return f"<KnowledgeCategory(id={self.id}, name={self.name})>"

class KnowledgeItem(Base):
    __tablename__ = "knowledge_items"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("knowledge_categories.id"), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)  # 知识内容
    content_type = Column(String(20), nullable=False)  # document, video, book
    
    # 文档/书籍信息
    author = Column(String(100), nullable=True)
    publisher = Column(String(100), nullable=True)
    publish_date = Column(String(20), nullable=True)
    isbn = Column(String(20), nullable=True)
    description = Column(Text, nullable=True)
    
    # 文件信息
    cover_url = Column(String(255), nullable=True)
    file_url = Column(String(255), nullable=True)  # 书籍PDF链接
    file_size = Column(Integer, nullable=True)
    
    # 统计信息
    view_count = Column(Integer, default=0, nullable=False)
    download_count = Column(Integer, default=0, nullable=False)
    
    status = Column(String(20), default="active", nullable=False)  # active, inactive
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # 关系
    category = relationship("KnowledgeCategory", back_populates="items")
    
    def __repr__(self):
        return f"<KnowledgeItem(id={self.id}, title={self.title}, content_type={self.content_type})>"

class VideoLink(Base):
    __tablename__ = "video_links"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    video_url = Column(String(500), nullable=False)  # 视频链接
    category_id = Column(Integer, ForeignKey("knowledge_categories.id"), nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    status = Column(String(20), default="active", nullable=False)  # active, inactive
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # 关系
    category = relationship("KnowledgeCategory")
    
    def __repr__(self):
        return f"<VideoLink(id={self.id}, title={self.title})>"

class BookLink(Base):
    __tablename__ = "book_links"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    cover_url = Column(String(255), nullable=True)  # 封面图片路径
    book_url = Column(String(500), nullable=False)  # 书籍链接
    sort_order = Column(Integer, default=0, nullable=False)
    status = Column(String(20), default="active", nullable=False)  # active, inactive
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<BookLink(id={self.id}, title={self.title})>"

class UserFavorite(Base):
    __tablename__ = "user_favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    favorite_type = Column(String(20), nullable=False)  # category, video, book
    favorite_id = Column(Integer, nullable=False)  # 对应类型的ID
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # 关系
    user = relationship("User")
    
    def __repr__(self):
        return f"<UserFavorite(id={self.id}, user_id={self.user_id}, type={self.favorite_type})>" 