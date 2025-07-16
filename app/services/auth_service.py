from app.models.user import UserLogin , UserRegister , UserOut
from app.repositories.firebase_repo import get_user_by_email , create_user
from app.core.security import verify_password, create_access_token , hash_password
from fastapi import HTTPException, status

def authenticate_user(credentials: UserLogin):
    user = get_user_by_email(credentials.email)
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = create_access_token({"sub": user["user_id"], "role": user["role_id"]})
    return {
        "access_token": token,
        "token_type": "bearer"
    }

def register_user(user: UserRegister):
    # check if user exists
    existing = get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_dict = {
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
        "password": hash_password(user.password),
        "role_id": user.role_id,
    }

    user_id = create_user(user_dict)
    return {
        "user_id": user_id,
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
        "role_id": user.role_id
    }

