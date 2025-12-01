from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select
from app.models.order import Order, OrderItem


class OrderRepository:

    # ---- Crear orden ----
    def create_order(self, session: Session, order: Order, items: list[OrderItem]) -> Order:
        session.add(order)
        session.flush()

        for item in items:
            item.order_id = order.id
            session.add(item)

        session.commit()
        session.refresh(order)
        return order

    # ---- Obtener orden ----
    def get_by_id(self, session: Session, order_id: int) -> Optional[Order]:
        return session.get(Order, order_id)

    # ---- Listar órdenes con filtros ----
    def list(
        self,
        session: Session,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        user_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[Order]:

        statement = select(Order)

        if start:
            statement = statement.where(Order.created_at >= start)

        if end:
            statement = statement.where(Order.created_at <= end)

        if user_id:
            statement = statement.where(Order.user_id == user_id)

        statement = statement.order_by(Order.created_at.desc())
        statement = statement.offset(skip).limit(limit)

        return session.exec(statement).all()

    # ---- Listar órdenes entre fechas (requerido por dashboard/reportes) ----
    def list_between_dates(self, session: Session, start: datetime, end: datetime) -> List[Order]:
        statement = (
            select(Order)
            .where(Order.created_at >= start)
            .where(Order.created_at <= end)
            .order_by(Order.created_at.desc())
        )
        return session.exec(statement).all()

    # ---- Eliminar / anular orden ----
    def delete(self, session: Session, order: Order):
        # 1. Borrar ítems primero
        for item in order.items:
            session.delete(item)

        session.flush()

        # 2. Ahora sí borrar la orden
        session.delete(order)
        session.commit()
