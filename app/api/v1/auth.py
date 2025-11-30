from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_session
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])
service = UserService()

@router.post("/register")
def register(full_name: str, email: str, password: str, session: Session = Depends(get_session)):
    try:
        return service.register_user(session, full_name, email, password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(email: str, password: str, session: Session = Depends(get_session)):
    try:
        return service.login(session, email, password)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
