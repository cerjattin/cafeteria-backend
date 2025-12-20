from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.user import User


class OrderItem(SQLModel, table=True):
    __tablename__ = "orderitem"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id")
    product_id: int = Field(foreign_key="product.id")
    qty: float = Field(nullable=False)
    price: float = Field(nullable=False)

    # Relaciones
    order: "Order" = Relationship(back_populates="items")
    product: Optional["Product"] = Relationship()  # ✅ relación al producto


class Order(SQLModel, table=True):
    __tablename__ = "order"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    total: float = Field(nullable=False, default=0)
    payment_method: str = Field(default="cash")

    # Relaciones
    items: List[OrderItem] = Relationship(back_populates="order")
    user: Optional["User"] = Relationship()  # opcional (si tienes modelo User)
