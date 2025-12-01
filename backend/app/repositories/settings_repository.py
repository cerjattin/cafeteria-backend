from sqlmodel import Session
from app.models.settings import BusinessSettings

class SettingsRepository:

    def get_settings(self, session: Session) -> BusinessSettings:
        settings = session.get(BusinessSettings, 1)
        if not settings:
            settings = BusinessSettings(id=1)
            session.add(settings)
            session.commit()
            session.refresh(settings)
        return settings

    def update_settings(self, session: Session, data: dict) -> BusinessSettings:
        settings = self.get_settings(session)
        for field, value in data.items():
            setattr(settings, field, value)
        session.add(settings)
        session.commit()
        session.refresh(settings)
        return settings
