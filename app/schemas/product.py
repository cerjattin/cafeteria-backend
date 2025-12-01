from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    code: str
    name: str
    category: Optional[str] = None
    price: float
    stock: float = 0
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[float] = None
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
