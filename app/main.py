from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import create_db_and_tables
from app.api.v1.router import api_router

origins = [ 
    "https://*.vercel.app",
    "http://localhost:5173",
    "http://127.0.0.1:5173",]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    create_db_and_tables()
    yield
    # shutdown (si necesitas cerrar cosas, aquí)

app = FastAPI(title=settings.APP_NAME,lifespan=lifespan)

app.include_router(api_router, prefix=settings.API_PREFIX)

# CORS para React/Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ajustar cuando deployes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Cafeteria Backend API Running 🚀"}
