from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

# Neon requiere sslmode=require en la URL
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "sslmode": "require"
    }
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
