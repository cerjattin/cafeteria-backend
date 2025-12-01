from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.database import get_session
from app.core.security import create_access_token
from app.services.user_service import UserService
from app.schemas.user import UserCreate, LoginRequest, UserResponse, LoginResponse

router = APIRouter(prefix="/auth", tags=["Auth"])
service = UserService()


# -----------------------------------------------------------------------
# REGISTER (solo admin inicial)
# -----------------------------------------------------------------------
@router.post("/register", response_model=UserResponse)
def register(
    data: UserCreate,
    session: Session = Depends(get_session),
):
    """
    Crea solo el primer usuario admin.
    """

    try:
        user = service.register_user(session, data)

        # 🔥 CORRECTO para Pydantic v2 + SQLModel
        return UserResponse.model_validate(user, from_attributes=True)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}",
        )


# -----------------------------------------------------------------------
# LOGIN
# -----------------------------------------------------------------------
@router.post("/login", response_model=LoginResponse)
def login(
    data: LoginRequest,
    session: Session = Depends(get_session),
):
    """
    Realiza login y devuelve token + usuario.
    """
    try:
        user = service.authenticate(session, data.email, data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        token = create_access_token({"sub": str(user.id)})

        # Convertir SQLModel → Pydantic v2 manualmente
        user_schema = UserResponse.model_validate(user, from_attributes=True)

        # Devolver estructura final sin que FastAPI revalide internamente
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user_schema.dict(),
        }

    except HTTPException:
        raise

    except Exception as e:
        print("ERROR LOGIN:", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

