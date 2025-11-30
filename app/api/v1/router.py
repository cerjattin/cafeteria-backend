from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .inventory import router as inventory_router
from .orders import router as orders_router
from .settings import router as settings_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(inventory_router)
api_router.include_router(orders_router)
api_router.include_router(settings_router)
