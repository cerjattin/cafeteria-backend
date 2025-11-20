from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, SQLModel

# Importamos el engine (que ya configuraste para Postgres en database.py)
from .database import engine

# --- IMPORTANTE: Importar TODOS los routers ---
from .routers import (
    auth, 
    inventory, 
    products, 
    orders, 
    users, 
    settings, 
    dashboard, 
    reports
)

# Importamos lógica de inicialización
from .logic.logic_users import create_first_admin
from .logic.logic_settings import create_initial_settings

# Función para crear las tablas
def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)

# Inicializamos la App
app = FastAPI(title="Cafetería API v4 (Docker)")

# --- Configuración CORS ---
# En Render es vital permitir los orígenes correctos.
# Por ahora usamos ["*"] para que no te de problemas al probar.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Evento de Inicio (Startup) ---
# Esto se ejecutará automáticamente cada vez que Render reinicie el servidor.
# Reemplaza la necesidad de correr el script "init_db.py" manualmente.
@app.on_event("startup")
def on_startup():
    print("--- INICIANDO API ---")
    
    # 1. Crear Tablas
    print("1. Verificando/Creando tablas en Base de Datos...")
    create_db_and_tables()
    
    # 2. Datos Iniciales
    print("2. Verificando datos iniciales...")
    with Session(engine) as session:
        # Configuración inicial
        create_initial_settings(session)
        
        # Admin inicial
        # Usamos try/except por si ya existe, para que no rompa el despliegue
        try:
            create_first_admin(session)
        except Exception as e:
            print(f"Nota sobre Admin: {e}")
            
    print("--- ARRANQUE COMPLETADO ---")

# --- Incluir Routers ---
# Sin esto, los endpoints darían 404 Not Found
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(settings.router)
app.include_router(products.router)
app.include_router(inventory.router)
app.include_router(orders.router)
app.include_router(dashboard.router)
app.include_router(reports.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"status": "Backend Cafetería v4 (Docker) en línea 🚀"}