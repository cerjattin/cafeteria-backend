from sqlmodel import Session
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User

repo = UserRepository()

class UserService:

    def register_user(self, session: Session, full_name: str, email: str, password: str):
        if repo.get_by_email(session, email):
            raise ValueError("User already exists")

        user = User(
            full_name=full_name,
            email=email,
            hashed_password=hash_password(password)
        )
        return repo.create(session, user)

    def login(self, session: Session, email: str, password: str):
        user = repo.get_by_email(session, email)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        token = create_access_token({"sub": user.id})
        return {"access_token": token, "user": user}
