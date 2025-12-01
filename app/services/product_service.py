from fastapi import HTTPException
from sqlmodel import Session

from app.repositories.product_repository import ProductRepository
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

repo = ProductRepository()


class ProductService:

    def create(self, session: Session, data: ProductCreate) -> Product:
        # Código único
        if repo.get_by_code(session, data.code):
            raise HTTPException(status_code=400, detail="El código ya existe")

        product = Product(
            code=data.code,
            name=data.name,
            category=data.category,
            price=data.price,
            stock=data.stock,
            is_active=True
        )

        return repo.save(session, product)

    def update(self, session: Session, product_id: int, data: ProductUpdate) -> Product:
        product = repo.get_by_id(session, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        update_data = data.dict(exclude_unset=True)

        for field, value in update_data.items():
            setattr(product, field, value)

        return repo.save(session, product)

    def deactivate(self, session: Session, product_id: int):
        product = repo.get_by_id(session, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        product.is_active = False
        return repo.save(session, product)

    def adjust_stock(self, session: Session, product_id: int, qty: float):
        product = repo.get_by_id(session, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        product.stock += qty
        return repo.save(session, product)
