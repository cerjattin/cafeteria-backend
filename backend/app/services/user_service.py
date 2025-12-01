from sqlmodel import Session, select
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.models.user import User
from app.schemas import user
from app.schemas.user import UserCreate, UserUpdate, LoginRequest, LoginResponse, UserResponse
from app.core.security import create_access_token

pwd_context = CryptContext(
    schemes=["bcrypt"],
    bcrypt__ident="2b",
    deprecated="auto"
)

class UserService:

    # ----------------- UTILIDADES -----------------

    def hash_password(self, password: str) -> str:
        # bcrypt solo soporta 72 bytes, truncamos como buenas prácticas
        safe_password = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
        print("PASSWORD RECIBIDO:", password)
        print("PASSWORD TRUNCADO:", safe_password)
        return pwd_context.hash(safe_password)
    

    def get_by_email(self, session: Session, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()

    # ----------------- REGISTRO -----------------

    def register_user(self, session: Session, data: UserCreate) -> User:
        """Usado por /auth/register"""
        existing = self.get_by_email(session, data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists",
            )

        return self._create_user(session, data, role="admin")  # primer usuario admin

    def _create_user(self, session: Session, data: UserCreate, role: str = "user") -> User:
        hashed = self.hash_password(data.password)

        user = User(
            full_name=data.full_name,
            email=data.email,
            hashed_password=hashed,
            role=role,
            is_active=True,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    # ----------------- AUTENTICACIÓN -----------------

    def authenticate(self, session: Session, email: str, password: str) -> User | None:
        user = self.get_by_email(session, email)
        if not user:
            return None
         # Truncar password para evitar errores de bcrypt en verify()
        safe_password = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")

        if not pwd_context.verify(safe_password, user.hashed_password):
            return None
        
        return user


    def login(self, session: Session, data: LoginRequest) -> LoginResponse:
        user = self.authenticate(session, data.email, data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        token = create_access_token({"sub": str(user.id)})
        
        print("LOGIN USER OBJECT:", user)
        print("HASH GUARDADO:", user.hashed_password)

        return LoginResponse(
            access_token=token,
            user=UserResponse.from_attributes(user),  # Pydantic v2
        )

    # ----------------- ACTUALIZAR USUARIO -----------------

    def update_user(self, session: Session, user: User, data: UserUpdate) -> User:
        if data.full_name is not None:
            user.full_name = data.full_name

        if data.role is not None:
            user.role = data.role

        if data.is_active is not None:
            user.is_active = data.is_active

        if data.password is not None:
            user.hashed_password = self.hash_password(data.password)

        session.add(user)
        session.commit()
        session.refresh(user)
        return user
