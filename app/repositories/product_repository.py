from typing import List, Optional
from sqlmodel import Session, select
from app.models.product import Product

class ProductRepository:

    def get_by_code(self, session: Session, code: str) -> Optional[Product]:
        statement = select(Product).where(Product.code == code)
        return session.exec(statement).first()

    def get_by_id(self, session: Session, product_id: int) -> Optional[Product]:
        return session.get(Product, product_id)

    def list_all(self, session: Session) -> List[Product]:
        statement = select(Product).where(Product.is_active == True)
        return session.exec(statement).all()

    def save(self, session: Session, product: Product) -> Product:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product
