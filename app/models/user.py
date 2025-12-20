from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: str = Field(index=True, unique=True)
    hashed_password: str
    role: str = Field(default="user", index=True)  # "admin", "cashier", etc.
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))