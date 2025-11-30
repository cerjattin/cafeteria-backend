from sqlmodel import SQLModel, Field
import uuid

class AppSettings(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    business_name: str
    tax_percentage: float = 0
