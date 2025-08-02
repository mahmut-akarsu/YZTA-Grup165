from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    name: str = Field(..., description="Ad")
    surname: str = Field(..., description="Soyad")
    email: EmailStr = Field(..., description="E-posta")
    password: str = Field(..., description="Şifre", min_length=6)
    role_id: str = Field(..., description="Rol (doctor/patient)")
    birth_date: date = Field(..., description="Doğum tarihi")
    # Doktor için ek bilgiler
    hospital: Optional[str] = Field(None, description="Çalıştığı hastane (sadece doktorlar için)")
    specialization: Optional[str] = Field(None, description="Uzmanlık alanı (sadece doktorlar için)")

class UserOut(BaseModel):
    user_id: str
    name: str
    surname: str
    email: EmailStr
    role_id: str
    birth_date: date
    hospital: Optional[str] = None
    specialization: Optional[str] = None
    created_at: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

