from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON, Integer, Float
from sqlalchemy.sql import func
from app.core.database import Base

class TriageRecord(Base):
    __tablename__ = "triage_records"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # 患者信息
    patient_name = Column(String(100), nullable=False)
    patient_id_card = Column(String(20), nullable=True)
    patient_age = Column(Integer, nullable=False)
    patient_gender = Column(String(10), nullable=False)  # male, female, other
    patient_weight = Column(Float, nullable=True)
    patient_height = Column(Float, nullable=True)
    patient_allergies = Column(JSON, nullable=True)  # 过敏史
    patient_medications = Column(JSON, nullable=True)  # 用药史
    patient_medical_history = Column(JSON, nullable=True)  # 病史
    
    # 生命体征
    heart_rate = Column(Integer, nullable=True)
    blood_pressure_systolic = Column(Integer, nullable=True)
    blood_pressure_diastolic = Column(Integer, nullable=True)
    respiratory_rate = Column(Integer, nullable=True)
    temperature = Column(Float, nullable=True)
    oxygen_saturation = Column(Float, nullable=True)
    blood_glucose = Column(Float, nullable=True)
    
    # 症状信息
    chief_complaint = Column(Text, nullable=False)  # 主诉
    symptoms = Column(JSON, nullable=True)  # 症状列表
    pain_level = Column(Integer, nullable=True)  # 疼痛等级 1-10
    symptom_duration = Column(String(50), nullable=True)  # 症状持续时间
    
    # AI分析结果
    ai_analysis = Column(JSON, nullable=True)  # AI分析结果
    urgency_level = Column(String(20), nullable=True)  # 紧急程度
    recommended_actions = Column(JSON, nullable=True)  # 推荐行动
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<TriageRecord(id={self.id}, patient_name={self.patient_name}, urgency_level={self.urgency_level})>" 