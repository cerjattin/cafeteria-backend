import reflex as rx

config = rx.Config(
    app_name="cafeteria_app",
    api_url="https://cafeteria-backend-mfg6.onrender.com",
    
    cors_allowed_origins=[
        "http://localhost:3000",  # <--- IMPORTANTE: Permite tu entorno local
        "https://cafeteria-backend-mfg6.onrender.com",
        "https://*.vercel.app"    # Déjalo por si luego volvemos a Vercel
    ],
)