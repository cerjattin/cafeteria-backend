from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List
from datetime import datetime
from sqlmodel import Session

from app.core.database import get_session
from app.core.auth import get_current_user, get_current_admin
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import OrderService
from app.models.user import User

router = APIRouter(prefix="/orders", tags=["Orders"])

service = OrderService()


# ---- Crear una orden ----
@router.post("/", response_model=OrderResponse)
def create_order(
    data: OrderCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return service.create_order(session, data, user_id=user.id)


# ---- Obtener orden por ID ----
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    return service.get_order(session, order_id)


# ---- Listar órdenes con filtros ----
@router.get("/", response_model=List[OrderResponse])
def list_orders(
    start_date: str | None = Query(None),
    end_date: str | None = Query(None),
    user_id: int | None = Query(None),
    skip: int = 0,
    limit: int = 50,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    start = datetime.fromisoformat(start_date) if start_date else None
    end = datetime.fromisoformat(end_date) if end_date else None

    return service.list_orders(session, start, end, user_id, skip, limit)


# ---- Cancelar/anular orden ----
@router.delete("/{order_id}")
def cancel_order(
    order_id: int,
    session: Session = Depends(get_session),
    admin: User = Depends(get_current_admin),
):
    return service.cancel_order(session, order_id)
