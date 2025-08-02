from fastapi import APIRouter, Depends, Form, HTTPException, status
from app.models.user import UserLogin, TokenResponse , UserOut , UserRegister
from app.services.auth_service import authenticate_user , register_user, get_current_user, authenticate_user_form
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

def calculate_age(birth_date_str: str) -> int:
    """Calculate age from birth date string"""
    try:
        if not birth_date_str:
            return None
        
        # Parse birth date string
        if isinstance(birth_date_str, str):
            birth_date = datetime.fromisoformat(birth_date_str.replace('Z', '+00:00')).date()
        else:
            birth_date = birth_date_str
        
        today = date.today()
        age = relativedelta(today, birth_date).years
        return age
    except Exception as e:
        print(f"Error calculating age: {str(e)}")
        return None

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(
    username: str = Form(...),  # Swagger'ın gönderdiği alan
    password: str = Form(...)
):
    try:
        return authenticate_user_form(username, password)
    except HTTPException as e:
        if e.status_code == 401:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        raise e


@router.post("/register", response_model=UserOut)
def register(user: UserRegister):
    """
    Register a new user
    
    For patients:
    - name, surname, email, password, role_id, birth_date
    
    For doctors:
    - name, surname, email, password, role_id, birth_date, hospital, specialization
    """
    return register_user(user)

@router.get("/test/register-examples")
def get_register_examples():
    """Get example registration data for testing"""
    return {
        "patient_example": {
            "name": "Ahmet",
            "surname": "Yılmaz",
            "email": "ahmet@example.com",
            "password": "password123",
            "role_id": "patient",
            "birth_date": "1990-05-15"
        },
        "doctor_example": {
            "name": "Dr. Ayşe",
            "surname": "Kaya",
            "email": "ayse@example.com",
            "password": "password123",
            "role_id": "doctor",
            "birth_date": "1985-03-20",
            "hospital": "Ankara Şehir Hastanesi",
            "specialization": "Kardiyoloji"
        }
    }


@router.get("/me")
def read_current_user(current_user=Depends(get_current_user)):
    return current_user

@router.get("/me/doctor")
def read_current_doctor(current_user=Depends(get_current_user)):
    """Get current doctor's information"""
    if current_user.get("role_id", "").lower() != "doctor":
        raise HTTPException(
            status_code=403, 
            detail="Access denied. This endpoint is only for doctors."
        )
    
    return {
        "user_id": current_user.get("user_id"),
        "name": current_user.get("name"),
        "surname": current_user.get("surname"),
        "email": current_user.get("email"),
        "role_id": current_user.get("role_id"),
        "birth_date": current_user.get("birth_date"),
        "hospital": current_user.get("hospital"),
        "specialization": current_user.get("specialization"),
        "created_at": current_user.get("created_at"),
        "full_name": f"{current_user.get('name', '')} {current_user.get('surname', '')}",
        "title": f"Dr. {current_user.get('name', '')} {current_user.get('surname', '')}"
    }

@router.get("/me/patient")
def read_current_patient(current_user=Depends(get_current_user)):
    """Get current patient's information"""
    if current_user.get("role_id", "").lower() != "patient":
        raise HTTPException(
            status_code=403, 
            detail="Access denied. This endpoint is only for patients."
        )
    
    return {
        "user_id": current_user.get("user_id"),
        "name": current_user.get("name"),
        "surname": current_user.get("surname"),
        "email": current_user.get("email"),
        "role_id": current_user.get("role_id"),
        "birth_date": current_user.get("birth_date"),
        "created_at": current_user.get("created_at"),
        "full_name": f"{current_user.get('name', '')} {current_user.get('surname', '')}",
        "age": calculate_age(current_user.get("birth_date")) if current_user.get("birth_date") else None
    }

@router.get("/test/current-user-info")
def test_current_user_info(current_user=Depends(get_current_user)):
    """Test endpoint to see current user information"""
    return {
        "message": "Current user information",
        "user": current_user,
        "role": current_user.get("role_id"),
        "is_doctor": current_user.get("role_id", "").lower() == "doctor",
        "is_patient": current_user.get("role_id", "").lower() == "patient"
    }

@router.get("/test/doctor-endpoint")
def test_doctor_endpoint(current_user=Depends(get_current_user)):
    """Test endpoint for doctors"""
    if current_user.get("role_id", "").lower() != "doctor":
        return {
            "error": "Access denied",
            "message": "This endpoint is only for doctors",
            "your_role": current_user.get("role_id")
        }
    
    return {
        "message": "Doctor access granted",
        "doctor_info": {
            "name": current_user.get("name"),
            "surname": current_user.get("surname"),
            "hospital": current_user.get("hospital"),
            "specialization": current_user.get("specialization")
        }
    }

@router.get("/test/patient-endpoint")
def test_patient_endpoint(current_user=Depends(get_current_user)):
    """Test endpoint for patients"""
    if current_user.get("role_id", "").lower() != "patient":
        return {
            "error": "Access denied",
            "message": "This endpoint is only for patients",
            "your_role": current_user.get("role_id")
        }
    
    return {
        "message": "Patient access granted",
        "patient_info": {
            "name": current_user.get("name"),
            "surname": current_user.get("surname"),
            "age": calculate_age(current_user.get("birth_date"))
        }
    }
