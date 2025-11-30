from pydantic import BaseModel
from typing import List
from datetime import datetime

class ReportItem(BaseModel):
    name: str
    units: int

class SalesTimePoint(BaseModel):
    timestamp: datetime
    total: float

class SalesReport(BaseModel):
    start_date: datetime
    end_date: datetime
    total_revenue: float
    total_orders: int
    average_ticket: float
    top_products: List[ReportItem]
    sales_by_category: List[ReportItem]
    sales_over_time: List[SalesTimePoint]
