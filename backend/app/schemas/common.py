from pydantic import BaseModel
from typing import Any, Optional, List
from datetime import datetime

class ApiResponse(BaseModel):
    """API统一响应格式"""
    code: int = 200
    message: str = "success"
    data: Optional[Any] = None
    timestamp: str = datetime.now().isoformat()

class PaginatedResponse(BaseModel):
    """分页响应格式"""
    total: int
    page: int
    page_size: int
    records: List[Any]

class HealthStatus(BaseModel):
    """健康检查响应"""
    status: str
    timestamp: str
    service: str
    version: str = "1.0.0" 