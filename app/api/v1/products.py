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

@router.get("/", response_model=List[ProductResponse])
def list_products(
    search: Optional[str] = Query(None, description="Buscar por nombre o código"),
    category: Optional[str] = None,
    active_only: bool = True,
    skip: int = 0,
    limit: int = 50,
    session: Session = Depends(get_session),
):
    return repo.list(session, search, category, active_only, skip, limit)


# -------------- VER -----------------

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    session: Session = Depends(get_session)
):
    product = repo.get_by_id(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product


# -------------- CREAR -----------------

@router.post("/", response_model=ProductResponse)
def create_product(
    data: ProductCreate,
    session: Session = Depends(get_session),
    admin = Depends(get_current_admin)
):
    return service.create(session, data)


# -------------- EDITAR -----------------

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    data: ProductUpdate,
    session: Session = Depends(get_session),
    admin = Depends(get_current_admin)
):
    return service.update(session, product_id, data)


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
    return service.adjust_stock(session, product_id, qty)
