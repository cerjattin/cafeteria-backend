from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlmodel import Session
from typing import Optional
from app.core.database import get_session
from app.services.inventory_service import InventoryService
from app.services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductUpdate, ProductRead
from app.models.product import Product

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
    # dependencies=[Depends(get_current_warehouse_user)]
)

inventory_service = InventoryService()
product_service = ProductService()

# ----------------------------
# Helpers (Punto 5.2)
# ----------------------------
def to_product_read(product: Product) -> ProductRead:
    return ProductRead(
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

# ----------------------------
# Upload de inventario (tu endpoint)
# ----------------------------
@router.post("/upload")
async def upload_inventory(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    if not file:
        raise HTTPException(status_code=400, detail="No se envió ningún archivo")

    content = await file.read()
    return inventory_service.process_inventory_file(session, content, file.content_type)

# ----------------------------
# Productos (para verificación rápida en Swagger)
# ----------------------------
@router.get("/products", response_model=list[ProductRead])
def list_products(session: Session = Depends(get_session)):
    """
    Lista productos incluyendo category_name.
    Nota: para que category_name no salga None, el repo debe traer la relación cargada (punto 5.3).
    """
    products = product_service.list(session)  # necesitas este método en ProductService
    return [to_product_read(p) for p in products]


@router.post("/products", response_model=ProductRead)
def create_product(payload: ProductCreate, session: Session = Depends(get_session)):
    product = product_service.create(session, payload)
    return to_product_read(product)


@router.put("/products/{product_id}", response_model=ProductRead)
def update_product(product_id: int, payload: ProductUpdate, session: Session = Depends(get_session)):
    product = product_service.update(session, product_id, payload)
    return to_product_read(product)


@router.patch("/products/{product_id}/stock", response_model=ProductRead)
def adjust_stock(product_id: int, qty: float, session: Session = Depends(get_session)):
    product = product_service.adjust_stock(session, product_id, qty)
    return to_product_read(product)


@router.get("/products", response_model=list[ProductRead])
def list_products(
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    category_name: Optional[str] = None,
    active_only: bool = True,
    skip: int = 0,
    limit: int = 50,
    session: Session = Depends(get_session),
):
    products = product_service.list(
        session=session,
        search=search,
        category_id=category_id,
        category_name=category_name,
        active_only=active_only,
        skip=skip,
        limit=limit
    )
    return [to_product_read(p) for p in products]
