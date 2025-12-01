from sqlmodel import Session
from app.repositories.settings_repository import SettingsRepository
from app.schemas.settings import BusinessSettingsUpdate

repo = SettingsRepository()

class SettingsService:

    def get_settings(self, session: Session):
        return repo.get_settings(session)

    def update_settings(self, session: Session, data: BusinessSettingsUpdate):
        return repo.update_settings(session, data.dict())
