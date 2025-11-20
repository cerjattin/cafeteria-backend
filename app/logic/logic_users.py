from sqlmodel import Session, select
from ..models import User
from ..security import get_password_hash
from ..schemas import UserCreate, UserUpdate
from fastapi import HTTPException

# ... (get_user_by_email, get_users, update_user) ...

def create_user(db: Session, user_data: UserCreate) -> User:
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        role=user_data.role,
        is_active=user_data.is_active,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_first_admin(session: Session):
    """Crea un usuario admin (v3) por defecto si no existe ninguno."""
    user = session.exec(select(User)).first()
    if not user:
        hashed_password = get_password_hash("admin123")
        admin_user = User(
            email="admin@cafe.com", # <-- Campo actualizado
            full_name="Admin de la Tienda",
            hashed_password=hashed_password,
            role="Admin",
            is_active=True
        )
        session.add(admin_user)
        session.commit()
        print("INFO:     Usuario 'admin@cafe.com' (pass: 'admin123') creado.")

# ... (resto de funciones de lógica de usuario) ...