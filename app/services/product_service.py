from fastapi import HTTPException
from sqlmodel import Session
from typing import Optional, List
from app.repositories.product_repository import ProductRepository
from app.models.product import Product
from app.models.category import Category
from app.schemas.product import ProductCreate, ProductUpdate

repo = ProductRepository()


class ProductService:

    def create(self, session: Session, data: ProductCreate) -> Product:
        # Código único
        if repo.get_by_code(session, data.code):
            raise HTTPException(status_code=400, detail="El código ya existe")

        # 🔵 Validar categoría si viene
        if data.category_id is not None:
            category = session.get(Category, data.category_id)
            if not category:
                raise HTTPException(
                    status_code=400,
                    detail="La categoría indicada no existe"
                )

        product = Product(
            code=data.code,
            name=data.name,
            category_id=data.category_id,
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

        # 🔵 Validar cambio de categoría
        if "category_id" in update_data and update_data["category_id"] is not None:
            category = session.get(Category, update_data["category_id"])
            if not category:
                raise HTTPException(
                    status_code=400,
                    detail="La categoría indicada no existe"
                )

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
    
    def list(self, session: Session):
        return repo.list(session)
    


    def list(
        self,
        session: Session,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
        category_name: Optional[str] = None,
        active_only: bool = True,
        skip: int = 0,
        limit: int = 50
        ) -> List[Product]:
    
        return repo.list(
            session=session,
            search=search,
            category_id=category_id,
            category_name=category_name,
            active_only=active_only,
            skip=skip,
            limit=limit
        )


