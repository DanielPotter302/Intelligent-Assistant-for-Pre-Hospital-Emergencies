from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class EmergencySession(Base):
    __tablename__ = "emergency_sessions"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    scenario_type = Column(String(50), nullable=False)  # 场景类型
    title = Column(String(200), nullable=False)
    status = Column(String(20), default="active", nullable=False)  # active, completed, cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # 关系
    messages = relationship("EmergencyMessage", back_populates="session", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<EmergencySession(id={self.id}, scenario_type={self.scenario_type}, user_id={self.user_id})>"

class EmergencyMessage(Base):
    __tablename__ = "emergency_messages"
    
    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("emergency_sessions.id"), nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    steps = Column(JSON, nullable=True)  # 操作步骤
    equipment = Column(JSON, nullable=True)  # 所需设备
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # 关系
    session = relationship("EmergencySession", back_populates="messages")
    
    def __repr__(self):
        return f"<EmergencyMessage(id={self.id}, role={self.role}, session_id={self.session_id})>" 