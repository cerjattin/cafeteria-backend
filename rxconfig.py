import reflex as rx
import os

BACKEND_URL = "https://cafeteria-backend-mfg6.onrender.com"

# Pega aquí tu URL de Vercel exacta que copiaste
FRONTEND_URL = "https://favored-coffee.vercel.app" 

config = rx.Config(
    app_name="cafeteria_app", 
    api_url=BACKEND_URL,
    deploy_url=BACKEND_URL, 
    
    cors_allowed_origins=[
        "http://localhost:3000",
        BACKEND_URL,
        FRONTEND_URL,
      

    ],
)