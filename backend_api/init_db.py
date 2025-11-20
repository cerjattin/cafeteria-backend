# init_db.py
import sys
import os

# Aseguramos que Python encuentre el módulo 'app'
sys.path.append(os.getcwd())

from sqlmodel import Session
from app.database import engine
from app.models import SQLModel
# Importamos las lógicas de inicialización
from app.logic.logic_users import create_first_admin
from app.logic.logic_settings import create_initial_settings

def init():
    print("--- INICIANDO CONFIGURACIÓN DE BASE DE DATOS ---")
    
    print("1. Creando tablas en MySQL...")
    # Esto crea todas las tablas definidas en models.py si no existen
    SQLModel.metadata.create_all(bind=engine)
    
    print("2. Insertando datos iniciales (Admin y Configuración)...")
    with Session(engine) as session:
        # Crear configuración inicial (IVA, Moneda, etc.)
        create_initial_settings(session)
        # Crear usuario admin
        create_first_admin(session)
    
    print("--- ¡ÉXITO! BASE DE DATOS LISTA ---")

if __name__ == "__main__":
    init()