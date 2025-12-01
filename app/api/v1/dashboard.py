from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.core.auth import get_current_user
from app.schemas.dashboard import DashboardSummary
from app.services.dashboard_service import DashboardService
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

service = DashboardService()


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    """
    Devuelve los KPIs principales para el dashboard:
    - Hoy
    - Últimos 7 días
    - Productos con bajo stock
    - Serie de ventas por día (últimos 7 días)
    """
    return service.get_dashboard_summary(session)
