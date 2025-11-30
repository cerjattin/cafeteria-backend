from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import create_db_and_tables
from app.api.v1.router import api_router

app = FastAPI(title=settings.APP_NAME)

# CORS para React/Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajustar cuando deployes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(api_router, prefix=settings.API_PREFIX)
