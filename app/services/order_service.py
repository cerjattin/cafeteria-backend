from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate

order_repo = OrderRepository()
product_repo = ProductRepository()


class OrderService:

    # ---- Crear orden (ya existente, solo la dejamos tal cual) ----
    def create_order(self, session: Session, data: OrderCreate, user_id: int | None = None) -> Order:
        if not data.items:
            raise HTTPException(status_code=400, detail="La orden no tiene items")

        items_models: list[OrderItem] = []
        total = 0.0

        # Validar stock
        for item in data.items:
            product = product_repo.get_by_id(session, item.product_id)
            if not product:
                raise HTTPException(status_code=404, detail=f"Producto {item.product_id} no encontrado")

            if product.stock < item.qty:
                raise HTTPException(
                    status_code=400,
                    detail=f"Stock insuficiente para producto {product.name} (disponible: {product.stock})"
                )

            total += product.price * item.qty

            items_models.append(OrderItem(
                product_id=product.id,
                qty=item.qty,
                price=product.price
            ))

        # Actualizar stock
        for item in data.items:
            product = product_repo.get_by_id(session, item.product_id)
            product.stock -= item.qty
            product_repo.save(session, product)

        # Crear orden
        order = Order(
            user_id=user_id,
            total=total,
            payment_method=data.payment_method,
            created_at=datetime.utcnow()
        )

        return order_repo.create_order(session, order, items_models)

    # -------- Obtener orden --------
    def get_order(self, session: Session, order_id: int) -> Order:
        order = order_repo.get_by_id(session, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Orden no encontrada")
        return order

    # -------- Listar órdenes --------
    def list_orders(
        self,
        session: Session,
        start: datetime | None,
        end: datetime | None,
        user_id: int | None,
        skip: int,
        limit: int
    ):
        return order_repo.list(session, start, end, user_id, skip, limit)

    # -------- Cancelar orden --------
    def cancel_order(self, session: Session, order_id: int):
        order = order_repo.get_by_id(session, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Orden no encontrada")

        # Devolver stock
        for item in order.items:
            product = product_repo.get_by_id(session, item.product_id)
            product.stock += item.qty
            product_repo.save(session, product)

        order_repo.delete(session, order)

        return {"status": "ok", "message": "Orden anulada"}
