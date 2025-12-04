from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class OrderItemCreate(BaseModel):
    product_id: int
    qty: float


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    payment_method: str = "cash"


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    qty: float
    price: float

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: int
    created_at: datetime
    user_id: Optional[int]
    total: float
    payment_method: str
    items: List[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)
