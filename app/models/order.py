from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
import uuid

class OrderItem(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    order_id: str = Field(foreign_key="order.id")
    product_id: str = Field(foreign_key="product.id")
    qty: float
    price: float

class Order(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    total: float
    items: List["OrderItem"] = Relationship()
