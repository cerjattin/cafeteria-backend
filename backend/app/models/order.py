from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id")
    product_id: int = Field(foreign_key="product.id")
    qty: float
    price: float

    order: "Order" = Relationship(back_populates="items")

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    total: float
    payment_method: str = "cash"

    items: List[OrderItem] = Relationship(back_populates="order")
