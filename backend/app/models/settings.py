from typing import Optional
from sqlmodel import SQLModel, Field

class BusinessSettings(SQLModel, table=True):
    """Configuración global del negocio (registro único id=1)."""
    id: Optional[int] = Field(default=1, primary_key=True)
    business_name: str = Field(default="Café Sol")
    tax_rate: float = 0.0                # % IVA o similar
    currency_symbol: str = Field(default="$")
    low_stock_threshold: int = 10        # Alerta de bajo stock
