from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select
from app.models.order import Order, OrderItem

class OrderRepository:

    def create_order(self, session: Session, order: Order, items: list[OrderItem]) -> Order:
        session.add(order)
        session.flush()  # para tener order.id

        for item in items:
            item.order_id = order.id
            session.add(item)

        session.commit()
        session.refresh(order)
        return order

    def get_by_id(self, session: Session, order_id: int) -> Optional[Order]:
        return session.get(Order, order_id)

    def list_between_dates(self, session: Session, start: datetime, end: datetime) -> List[Order]:
        statement = select(Order).where(
            Order.created_at >= start,
            Order.created_at <= end
        )
        return session.exec(statement).all()
