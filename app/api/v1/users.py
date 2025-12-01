from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session

from app.core.database import get_session
from app.core.auth import get_current_admin, get_current_user
from app.schemas.user import UserResponse, UserUpdate
from app.repositories.user_repository import UserRepository
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

repo = UserRepository()


@router.get("/", response_model=List[UserResponse])
def list_users(
    session: Session = Depends(get_session),
    admin: User = Depends(get_current_admin),
):
    """Lista todos los usuarios (solo admin)."""
    return repo.get_all(session)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    session: Session = Depends(get_session),
    current: User = Depends(get_current_user),
):
    """Obtiene un usuario por ID (admin o el mismo usuario)."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if current.role != "admin" and current.id != user_id:
        raise HTTPException(status_code=403, detail="Acceso no autorizado")

    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    session: Session = Depends(get_session),
    admin: User = Depends(get_current_admin)
):
    """Actualiza usuario (rol, activo, nombre, password)."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if data.full_name is not None:
        user.full_name = data.full_name

    if data.role is not None:
        user.role = data.role

    if data.is_active is not None:
        user.is_active = data.is_active

    if data.password is not None:
        from app.core.security import hash_password
        user.hashed_password = hash_password(data.password)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user
