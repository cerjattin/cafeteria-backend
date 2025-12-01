from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.schemas.report import SalesTimePoint


class DashboardKPIs(BaseModel):
    start_date: datetime
    end_date: datetime
    total_revenue: float
    total_orders: int
    average_ticket: float


class LowStockProduct(BaseModel):
    id: int
    code: str
    name: str
    stock: float


class DashboardSummary(BaseModel):
    today: DashboardKPIs
    last_7_days: DashboardKPIs
    low_stock_products: List[LowStockProduct]
    sales_over_time: List[SalesTimePoint]
