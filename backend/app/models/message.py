from sqlalchemy import Column, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class ContactMessage(Base):
    __tablename__ = "contact_messages"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    
    # 状态信息
    status = Column(String(20), default="unread", nullable=False)  # unread, read, replied
    admin_reply = Column(Text, nullable=True)  # 管理员回复
    replied_at = Column(DateTime(timezone=True), nullable=True)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<ContactMessage(id={self.id}, name={self.name}, email={self.email})>" 