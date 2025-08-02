from app.models.user import UserLogin, UserRegister, UserOut
from app.repositories.firebase_repo import get_user_by_email, create_user, get_user_by_id
from app.core.security import verify_password, create_access_token, hash_password
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import os
from datetime import datetime

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret")
ALGORITHM = "HS256"

def authenticate_user(credentials: UserLogin):
    user = get_user_by_email(credentials.email)
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = create_access_token({"sub": user["email"], "role": user["role_id"]})
    return {
        "access_token": token,
        "token_type": "bearer"
    }

def authenticate_user_form(username: str, password: str):
    user = get_user_by_email(username)
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user["email"], "role": user["role_id"]})
    return {
        "access_token": token,
        "token_type": "bearer"
    }

def register_user(user: UserRegister):
    # check if user exists
    existing = get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Validate doctor-specific fields
    if user.role_id.lower() == "doctor":
        if not user.hospital or not user.specialization:
            raise HTTPException(
                status_code=400, 
                detail="Hospital and specialization are required for doctors"
            )
    else:
        # Clear doctor-specific fields for non-doctors
        user.hospital = None
        user.specialization = None

    user_dict = {
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
        "password": hash_password(user.password),
        "role_id": user.role_id,
        "birth_date": user.birth_date.isoformat(),  # Convert date to string
        "hospital": user.hospital,
        "specialization": user.specialization,
        "created_at": datetime.now().isoformat()
    }

    user_id = create_user(user_dict)
    return {
        "user_id": user_id,
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
        "role_id": user.role_id,
        "birth_date": user.birth_date.isoformat(),
        "hospital": user.hospital,
        "specialization": user.specialization,
        "created_at": user_dict["created_at"]
    }

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print("=== AUTH DEBUG ===")
    print("get_current_user ÇAĞRILDI")
    print("TOKEN:", token)
    print("SECRET_KEY:", SECRET_KEY)
    print("ALGORITHM:", ALGORITHM)
    
    if not token:
        print("TOKEN BOŞ!")
        raise credentials_exception
        
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("PAYLOAD:", payload)
        user_email: str = payload.get("sub")
        print("USER EMAIL:", user_email)
        
        if not user_email:
            print("USER EMAIL BOŞ!")
            raise credentials_exception
            
    except JWTError as e:
        print("JWT ERROR:", str(e))
        raise credentials_exception
        
    user = get_user_by_email(user_email)
    print("USER:", user)
    if user is None:
        print("USER BULUNAMADI!")
        raise credentials_exception
    
    # Ensure all required fields are present
    user_data = {
        "user_id": user.get("user_id"),
        "name": user.get("name"),
        "surname": user.get("surname"),
        "email": user.get("email"),
        "role_id": user.get("role_id"),
        "birth_date": user.get("birth_date"),
        "hospital": user.get("hospital"),
        "specialization": user.get("specialization"),
        "created_at": user.get("created_at")
    }
    
    print("USER DATA:", user_data)
    print("=== AUTH DEBUG END ===")
    return user_data

