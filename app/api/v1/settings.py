from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.services.settings_service import SettingsService
from app.schemas.settings import BusinessSettingsResponse, BusinessSettingsUpdate
# from app.core.security import get_current_admin_user

router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
    # dependencies=[Depends(get_current_admin_user)]
)

service = SettingsService()

@router.get("/", response_model=BusinessSettingsResponse)
def read_settings(session: Session = Depends(get_session)):
    return service.get_settings(session)

@router.put("/", response_model=BusinessSettingsResponse)
def update_settings(
    settings_data: BusinessSettingsUpdate,
    session: Session = Depends(get_session),
):
    return service.update_settings(session, settings_data)
