from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class PatientInfo(BaseModel):
    """患者信息"""
    name: str
    id_card: Optional[str] = None
    age: int
    gender: str  # male, female, other
    weight: Optional[float] = None
    height: Optional[float] = None
    allergies: Optional[List[str]] = None
    medications: Optional[List[str]] = None
    medical_history: Optional[List[str]] = None

class VitalSigns(BaseModel):
    """生命体征"""
    heart_rate: Optional[int] = None
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    respiratory_rate: Optional[int] = None
    temperature: Optional[float] = None
    oxygen_saturation: Optional[float] = None
    blood_glucose: Optional[float] = None

class SymptomInfo(BaseModel):
    """症状信息"""
    chief_complaint: str
    symptoms: Optional[List[str]] = None
    pain_level: Optional[int] = None  # 1-10
    symptom_duration: Optional[str] = None

class TriageRequest(BaseModel):
    """分诊请求"""
    patient_info: PatientInfo
    vital_signs: VitalSigns
    symptom_info: SymptomInfo

class TriageResponse(BaseModel):
    """分诊响应"""
    urgency_level: str  # critical, urgent, semi_urgent, non_urgent
    priority_score: int  # 1-5
    recommended_actions: List[str]
    estimated_wait_time: Optional[str] = None
    department_recommendation: Optional[str] = None
    additional_notes: Optional[str] = None

class TriageHistoryItem(BaseModel):
    """分诊历史项"""
    id: str
    patient_name: str
    urgency_level: str
    chief_complaint: str
    created_at: datetime

    class Config:
        from_attributes = True 