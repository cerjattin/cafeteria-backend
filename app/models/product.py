from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

from app.models.category import Category

class Product(SQLModel, table=True):
    """Producto de inventario."""
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)
    name: str

    # ✅ NUEVO: FK real
    category_id: Optional[int] = Field(default=None, foreign_key="categories.id", index=True)
    category: Optional["Category"] = Relationship(back_populates="products")

    stock: float = 0
    price: float
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
