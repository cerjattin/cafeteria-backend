import reflex as rx

# Tu Backend (Render)
BACKEND_URL = "https://cafeteria-backend-mfg6.onrender.com"

# Tu Frontend (Vercel) - ¡ESTA ES LA QUE OBTUVIMOS DEL LOG!
FRONTEND_URL = "https://favored-coffee.vercel.app" 

config = rx.Config(
    app_name="cafeteria_app", 
    
    api_url=BACKEND_URL,
    
    cors_allowed_origins=[
        "http://localhost:3000",
        BACKEND_URL,
        
        FRONTEND_URL, 
    ],
)s