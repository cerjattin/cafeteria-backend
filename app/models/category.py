from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from app.models.product import Product

class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    description: Optional[str] = None

    products: List["Product"] = Relationship(back_populates="category")
