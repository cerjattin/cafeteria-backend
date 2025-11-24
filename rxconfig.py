import reflex as rx

config = rx.Config(
    app_name="cafeteria_app",
    api_url="https://cafeteria-backend-mfg6.onrender.com",
    
    # 👇 CAMBIA ESTO. Permite entrar a cualquiera.
    cors_allowed_origins=[
        "*"
    ],
)