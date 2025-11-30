from fastapi import APIRouter, Depends
from sqlmodel import Session
from datetime import datetime
from typing import List
from app.core.database import get_session
from app.services.order_service import OrderService
from app.schemas.order import OrderCreate, OrderResponse
# from app.core.security import get_current_user

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)

service = OrderService()

@router.post("/", response_model=OrderResponse)
def create_order(
    data: OrderCreate,
    session: Session = Depends(get_session),
    # current_user = Depends(get_current_user)
):
    # user_id = current_user.id if current_user else None
    user_id = None
    order = service.create_order(session, data, user_id=user_id)
    return order

# Extra: puedes añadir GET /{id}, listados, etc. luego
