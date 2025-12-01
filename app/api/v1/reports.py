from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from datetime import datetime
from app.core.database import get_session
from app.services.report_service import ReportService
from app.schemas.report import SalesReport

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)

service = ReportService()

@router.get("/sales", response_model=SalesReport)
def get_sales_report(
    start_date: str = Query(..., description="Fecha inicio en formato YYYY-MM-DD"),
    end_date: str = Query(..., description="Fecha fin en formato YYYY-MM-DD"),
    session: Session = Depends(get_session),
):
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido")

    if end < start:
        raise HTTPException(status_code=400, detail="end_date debe ser >= start_date")

    return service.get_sales_report(session, start, end)
