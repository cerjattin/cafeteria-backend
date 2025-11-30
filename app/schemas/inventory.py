from pydantic import BaseModel
from typing import List, Optional

class InventoryUploadSummary(BaseModel):
    updated: int
    created: int
    errors: int = 0

class InventoryUploadResponse(BaseModel):
    status: str
    summary: str
    details: Optional[InventoryUploadSummary] = None
    errors: Optional[List[str]] = None
