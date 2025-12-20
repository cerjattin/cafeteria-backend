from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ProductBase(BaseModel):
    code: str
    name: str
    price: float
    stock: float = 0


class ProductCreate(ProductBase):
    # ✅ Nuevo: FK real
    category_id: Optional[int] = None


class ProductUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[float] = None
    is_active: Optional[bool] = None

    # ✅ Nuevo: permitir cambio de categoría
    category_id: Optional[int] = None


class ProductRead(ProductBase):
    id: int
    is_active: bool
    created_at: datetime

    # ✅ devolver FK
    category_id: Optional[int] = None

    # ✅ para que el frontend vea el nombre sin otra consulta
    category_name: Optional[str] = None

    class Config:
        orm_mode = True
