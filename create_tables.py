from sqlmodel import SQLModel
from app.core.database import engine

def main():
    print("Creando tablas en NeonDB...")
    SQLModel.metadata.create_all(engine)
    print("¡Tablas creadas exitosamente!")

if __name__ == "__main__":
    main()
