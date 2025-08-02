from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class MealRelation(str, Enum):
    EMPTY_STOMACH = "NO_FOOD"
    WITH_FOOD = "WITH_FOOD"

class DrugStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class Drug(BaseModel):
    name: str = Field(..., description="İlaç adı")
    frequency_per_day: int = Field(..., description="Günde kaç kez kullanılacak (sayı)", ge=1, le=10)
    quantity_per_dose: int = Field(..., description="Her dozda kaç adet (sayı)", ge=1, le=10)
    meal_relation: MealRelation = Field(..., description="Yemek ile ilişki (aç/tok)")
    duration_days: int = Field(..., description="Kaç gün kullanılacak (sayı)", ge=1, le=365)
    drug_id: Optional[str] = None
    user_id: Optional[str] = None
    status: DrugStatus = Field(default=DrugStatus.ACTIVE, description="İlaç durumu")
    last_used: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class DrugCreate(BaseModel):
    name: str = Field(..., description="İlaç adı")
    frequency_per_day: int = Field(..., description="Günde kaç kez kullanılacak (sayı)", ge=1, le=10)
    quantity_per_dose: int = Field(..., description="Her dozda kaç adet (sayı)", ge=1, le=10)
    meal_relation: MealRelation = Field(..., description="Yemek ile ilişki (aç/tok)")
    duration_days: int = Field(..., description="Kaç gün kullanılacak (sayı)", ge=1, le=365)

class DrugUpdate(BaseModel):
    name: Optional[str] = Field(None, description="İlaç adı")
    frequency_per_day: Optional[int] = Field(None, description="Günde kaç kez kullanılacak (sayı)", ge=1, le=10)
    quantity_per_dose: Optional[int] = Field(None, description="Her dozda kaç adet (sayı)", ge=1, le=10)
    meal_relation: Optional[MealRelation] = Field(None, description="Yemek ile ilişki (aç/tok)")
    duration_days: Optional[int] = Field(None, description="Kaç gün kullanılacak (sayı)", ge=1, le=365)
    status: Optional[DrugStatus] = Field(None, description="İlaç durumu")

class DrugResponse(BaseModel):
    drug_id: str
    name: str
    frequency_per_day: int
    quantity_per_dose: int
    meal_relation: MealRelation
    duration_days: int
    user_id: str
    status: DrugStatus
    last_used: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

class DrugStatusUpdate(BaseModel):
    status: DrugStatus = Field(..., description="Yeni ilaç durumu")

class DrugUsage(BaseModel):
    usage_date: datetime = Field(..., description="İlaç kullanım tarihi")
    quantity: int = Field(..., description="Kullanılan miktar", ge=1)
    notes: Optional[str] = Field(None, description="Kullanım notları")
    times: List[str]

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
   
