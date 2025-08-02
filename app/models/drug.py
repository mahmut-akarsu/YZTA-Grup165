from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Drug(BaseModel):
    name: str
    dosage: str
    frequency: str
    barcode: Optional[str] = None
    drug_id: Optional[str] = None

class DrugUsage(BaseModel):
    drug_id: str
    usage_time: Optional[datetime] = None
    notes: Optional[str] = None

class DrugUsageResponse(BaseModel):
    usage_id: str
    drug_id: str
    drug_name: str
    usage_time: datetime
    notes: Optional[str] = None

class DrugSummary(BaseModel):
    total_usage_count: int = 0
    last_used: Optional[datetime] = None
    first_used: Optional[datetime] = None
    average_interval_hours: Optional[float] = None
    recent_usage_count: int = 0  # Son 30 kullanım

class DrugUsageSummary(BaseModel):
    date: str
    usage_count: int
    times: List[str]
   
