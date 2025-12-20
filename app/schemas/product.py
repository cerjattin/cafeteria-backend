from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    code: str
    name: str
    price: float
    stock: float = 0
    is_active: bool = True


class ProductCreate(ProductBase):
    # ✅ FK real hacia categories
    category_id: Optional[int] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[float] = None
    is_active: Optional[bool] = None
    category_id: Optional[int] = None


class ProductRead(ProductBase):
    id: int
    created_at: datetime
    category_id: Optional[int] = None
    category_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# Alias por compatibilidad con routers existentes
ProductResponse = ProductRead
