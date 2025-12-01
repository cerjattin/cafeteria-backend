from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


# ---- Base / lectura ----

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: Optional[str] = "user"
    is_active: Optional[bool] = True


class UserResponse(UserBase):
    id: int

    # Pydantic v2: reemplaza orm_mode
    model_config = ConfigDict(from_attributes=True)


# ---- Crear / actualizar ----

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str  # texto plano, se encripta en el service


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None  # si se envía, se actualiza


# ---- Auth / login ----

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
