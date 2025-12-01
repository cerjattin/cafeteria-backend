from typing import List, Optional
from sqlmodel import Session, select
from app.models.product import Product


class ProductRepository:

    # ---- Búsquedas ----

    def get_by_code(self, session: Session, code: str) -> Optional[Product]:
        statement = select(Product).where(Product.code == code)
        return session.exec(statement).first()

    def get_by_id(self, session: Session, product_id: int) -> Optional[Product]:
        return session.get(Product, product_id)

    # ---- Listar con filtros ----

    def list(
        self,
        session: Session,
        search: Optional[str] = None,
        category: Optional[str] = None,
        active_only: bool = True,
        skip: int = 0,
        limit: int = 50
    ) -> List[Product]:

        statement = select(Product)

        if active_only:
            statement = statement.where(Product.is_active == True)

        if search:
            search = f"%{search}%"
            statement = statement.where(
                (Product.name.ilike(search)) |
                (Product.code.ilike(search))
            )

        if category:
            statement = statement.where(Product.category == category)

        statement = statement.offset(skip).limit(limit)

        return session.exec(statement).all()

    # ---- Guardar / actualizar ----

    def save(self, session: Session, product: Product) -> Product:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product
