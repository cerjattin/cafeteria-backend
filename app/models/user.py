from sqlmodel import SQLModel, Field
from typing import Optional
import uuid

class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    full_name: str
    email: str = Field(index=True, unique=True)
    hashed_password: str
    role: str = "user"
    is_active: bool = True
