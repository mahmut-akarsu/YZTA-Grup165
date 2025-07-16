from fastapi import APIRouter
from app.models.user import UserLogin, TokenResponse , UserOut , UserRegister
from app.services.auth_service import authenticate_user , register_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin):
    return authenticate_user(user)


@router.post("/register", response_model=UserOut)
def register(user: UserRegister):
    return register_user(user)
