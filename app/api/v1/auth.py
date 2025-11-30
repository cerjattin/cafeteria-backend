from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_session
from app.services.user_service import UserService
from app.schemas.user import UserCreate, LoginRequest, UserResponse, LoginResponse

router = APIRouter(prefix="/auth", tags=["Auth"])
service = UserService()

@router.post("/register", response_model=UserResponse)
def register(
    data: UserCreate,
    session: Session = Depends(get_session),
):
    try:
        user = service.register_user(session, data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=LoginResponse)
def login(
    data: LoginRequest,
    session: Session = Depends(get_session),
):
    try:
        return service.login(session, data)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
