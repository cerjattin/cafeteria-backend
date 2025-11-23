import reflex as rx
BACKEND_URL = "https://cafeteria-backend-mfg6.onrender.com"

config = rx.Config(
    app_name="FavoredCoffee",
    api_url=BACKEND_URL,
    deploy_url= "https://FavoredCoffee.reflex.run",

    cors_allowed_origins=[
        "http://localhost:3000",
        BACKEND_URL,
        "https://*.vercel.app",
    ],
    # Deshabilitar plugins innecesarios
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
)