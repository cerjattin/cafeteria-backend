from typing import List, Optional

from pydantic import BaseModel


class InventoryUploadSummary(BaseModel):
    updated: int
    created: int
    errors: int = 0


class InventoryUploadResponse(BaseModel):
    status: str
    summary: str
    details: Optional[InventoryUploadSummary] = None
    errors: Optional[List[str]] = None
