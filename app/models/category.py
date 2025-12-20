from typing import Optional, List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.product import Product


class Category(SQLModel, table=True):
    """Categoría de productos."""

    __tablename__ = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False, unique=True)
    description: Optional[str] = None

    products: List["Product"] = Relationship(back_populates="category")
