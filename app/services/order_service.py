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

    def create_order(self, session: Session, data: OrderCreate, user_id: int | None = None) -> Order:
        if not data.items:
            raise HTTPException(status_code=400, detail="La orden no tiene items")

        items_models: list[OrderItem] = []
        total = 0.0

        # Validar stock y calcular total
        for item in data.items:
            product = product_repo.get_by_id(session, item.product_id)
            if not product:
                raise HTTPException(status_code=404, detail=f"Producto {item.product_id} no encontrado")

            if product.stock < item.qty:
                raise HTTPException(
                    status_code=400,
                    detail=f"Stock insuficiente para producto {product.name} (disponible: {product.stock})",
                )

            line_total = product.price * item.qty
            total += line_total

            # Reservamos la reducción de stock para después
            order_item = OrderItem(
                product_id=product.id,
                qty=item.qty,
                price=product.price,
            )
            items_models.append(order_item)

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
            created_at=datetime.utcnow(),
        )

        return order_repo.create_order(session, order, items_models)
