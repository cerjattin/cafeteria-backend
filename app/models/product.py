from sqlmodel import SQLModel, Field
from typing import Optional
import uuid

class Product(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    category: Optional[str] = None
    stock: float = 0
    price: float
    created_by: Optional[str] = None
