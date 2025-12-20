from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlmodel import Session
from app.core.database import get_session
from app.core.auth import get_current_admin
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService
from app.models.product import Product


router = APIRouter(prefix="/products", tags=["Products"])

repo = ProductRepository()
service = ProductService()


# -------------- LISTAR -----------------

def _to_product_response(product: Product) -> ProductResponse:
    return ProductResponse(
        id=product.id,
        code=product.code,
        name=product.name,
        price=product.price,
        stock=product.stock,
        is_active=product.is_active,
        created_at=product.created_at,
        category_id=product.category_id,
        category_name=product.category.name if product.category else None,
    )


@router.get("/", response_model=List[ProductResponse])
def list_products(
    search: Optional[str] = Query(None, description="Buscar por nombre o código"),
    category_id: Optional[int] = None,
    category_name: Optional[str] = None,
    active_only: bool = True,
    skip: int = 0,
    limit: int = 50,
    session: Session = Depends(get_session),
):
    products = repo.list(session, search, category_id, category_name, active_only, skip, limit)
    return [_to_product_response(p) for p in products]


# -------------- VER -----------------

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    session: Session = Depends(get_session)
):
    product = repo.get_by_id(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return _to_product_response(product)


# -------------- CREAR -----------------

@router.post("/", response_model=ProductResponse)
def create_product(
    data: ProductCreate,
    session: Session = Depends(get_session),
    admin = Depends(get_current_admin)
):
    product = service.create(session, data)
    # Asegurar category cargada para category_name
    product = repo.get_by_id(session, product.id) or product
    return _to_product_response(product)


# -------------- EDITAR -----------------

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    data: ProductUpdate,
    session: Session = Depends(get_session),
    admin = Depends(get_current_admin)
):
    product = service.update(session, product_id, data)
    product = repo.get_by_id(session, product.id) or product
    return _to_product_response(product)


# -------------- DESACTIVAR -----------------

@router.delete("/{product_id}")
def deactivate_product(
    product_id: int,
    session: Session = Depends(get_session),
    admin = Depends(get_current_admin)
):
    service.deactivate(session, product_id)
    return {"status": "ok", "message": "Producto desactivado"}


# -------------- AJUSTAR STOCK -----------------

@router.patch("/{product_id}/stock", response_model=ProductResponse)
def adjust_stock(
    product_id: int,
    qty: float = Query(..., description="Cantidad a ajustar (+ o -)"),
    session: Session = Depends(get_session),
    admin = Depends(get_current_admin),
):
    """
    Ajusta el stock manualmente (para correcciones, mermas, inventarios).
    qty puede ser positivo o negativo.
    """
    product = service.adjust_stock(session, product_id, qty)
    product = repo.get_by_id(session, product.id) or product
    return _to_product_response(product)


