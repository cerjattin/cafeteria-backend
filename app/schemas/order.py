from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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

    class Config:
        orm_mode = True

class OrderResponse(BaseModel):
    id: int
    created_at: datetime
    user_id: Optional[int]
    total: float
    payment_method: str
    items: List[OrderItemResponse]

    class Config:
        orm_mode = True
