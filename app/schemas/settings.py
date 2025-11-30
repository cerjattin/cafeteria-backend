from pydantic import BaseModel

class BusinessSettingsBase(BaseModel):
    business_name: str
    tax_rate: float
    currency_symbol: str
    low_stock_threshold: int

class BusinessSettingsUpdate(BusinessSettingsBase):
    pass

class BusinessSettingsResponse(BusinessSettingsBase):
    id: int

    class Config:
        orm_mode = True
