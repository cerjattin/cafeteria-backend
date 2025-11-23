# rxconfig.py (EN EL REPOSITORIO BACKEND)
import reflex as rx

# Tu URL de Vercel (Cópiala tal cual del navegador)
VERCEL_URL = "https://favored-coffee.vercel.app" 

config = rx.Config(
    app_name="cafeteria_app",
    
    # En el backend, la api_url es él mismo (o puedes dejarla vacía, no afecta tanto aquí)
    api_url="https://cafeteria-backend-mfg6.onrender.com",
    
    # 🚨 ESTO ES LO CRÍTICO EN ESTE REPO:
    cors_allowed_origins=[
        "http://localhost:3000",
        VERCEL_URL  # <--- Sin esto, Render bloqueará a Vercel (Error 403)
    ],
)