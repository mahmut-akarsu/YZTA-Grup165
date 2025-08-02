from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    role_id: str  # e.g., "doctor", "patient"

class UserOut(BaseModel):
    user_id: str
    name: str
    surname: str
    email: EmailStr
    role_id: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

