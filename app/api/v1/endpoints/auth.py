from fastapi import APIRouter, Depends, Form, HTTPException, status
from app.models.user import UserLogin, TokenResponse , UserOut , UserRegister
from app.services.auth_service import authenticate_user , register_user, get_current_user, authenticate_user_form

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
    return register_user(user)


@router.get("/me")
def read_current_user(current_user=Depends(get_current_user)):
    return current_user
