from typing import List, Optional

from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from app.models.product import Product
from app.models.category import Category


class ProductRepository:

    # ---- Búsquedas ----

    def get_by_code(self, session: Session, code: str) -> Optional[Product]:
        statement = (
            select(Product)
            .where(Product.code == code)
            .options(selectinload(Product.category))
        )
        return session.exec(statement).first()

    def get_by_id(self, session: Session, product_id: int) -> Optional[Product]:
        statement = (
            select(Product)
            .where(Product.id == product_id)
            .options(selectinload(Product.category))
        )
        return session.exec(statement).first()

    # ---- Listar con filtros ----

    def list(
        self,
        session: Session,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
        category_name: Optional[str] = None,
        active_only: bool = True,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Product]:

        statement = select(Product).options(selectinload(Product.category))

        if active_only:
            statement = statement.where(Product.is_active == True)

        if search:
            pattern = f"%{search}%"
            statement = statement.where(
                (Product.name.ilike(pattern)) |
                (Product.code.ilike(pattern))
            )

        if category_id is not None:
            statement = statement.where(Product.category_id == category_id)

        # Compat opcional: filtrar por nombre de categoría
        if category_name:
            statement = statement.join(Category).where(Category.name.ilike(f"%{category_name}%"))

        statement = statement.offset(skip).limit(limit)
        return session.exec(statement).all()

    # ---- Guardar / actualizar ----

    def save(self, session: Session, product: Product) -> Product:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product
