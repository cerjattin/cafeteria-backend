from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.category import Category


class Product(SQLModel, table=True):
    """Producto de inventario."""
    __tablename__ = "product"

    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)
    name: str

    # ✅ Relación real con categorías
    category_id: Optional[int] = Field(default=None, foreign_key="categories.id", index=True)
    category: Optional["Category"] = Relationship(back_populates="products")

    stock: float = 0
    price: float
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
