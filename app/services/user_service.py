from sqlmodel import Session
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, LoginRequest, LoginResponse, UserResponse

repo = UserRepository()

class UserService:

    def register_user(self, session: Session, data: UserCreate) -> User:
        if repo.get_by_email(session, data.email):
            raise ValueError("User already exists")

        user = User(
            full_name=data.full_name,
            email=data.email,
            hashed_password=hash_password(data.password),
        )
        return repo.create(session, user)

    def login(self, session: Session, data: LoginRequest) -> LoginResponse:
        user = repo.get_by_email(session, data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise ValueError("Invalid credentials")

        token = create_access_token({"sub": str(user.id)})

        return LoginResponse(
            access_token=token,
            user=UserResponse.from_orm(user),
        )
