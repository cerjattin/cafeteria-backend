from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Product(SQLModel, table=True):
    """Producto de inventario."""
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)
    name: str
    category: Optional[str] = None
    stock: float = 0
    price: float
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
