from sqlmodel import Session, select
from app.models.user import User

class UserRepository:

    def get_by_email(self, session: Session, email: str):
        return session.exec(select(User).where(User.email == email)).first()

    def create(self, session: Session, user: User):
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    def get_all(self, session: Session):
        return session.exec(select(User)).all()
