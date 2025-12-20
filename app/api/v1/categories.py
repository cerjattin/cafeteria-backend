from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional

from sqlmodel import Session, select

from app.core.database import get_session
from app.core.auth import get_current_admin
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryRead
from app.models.user import User


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategoryRead])
def list_categories(
    search: Optional[str] = Query(None, description="Buscar por nombre"),
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
):
    stmt = select(Category)
    if search:
        stmt = stmt.where(Category.name.ilike(f"%{search}%"))
    stmt = stmt.offset(skip).limit(limit)
    return session.exec(stmt).all()


@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, session: Session = Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return category


@router.post("/", response_model=CategoryRead)
def create_category(
    data: CategoryCreate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_admin),
):
    # nombre único
    exists = session.exec(select(Category).where(Category.name == data.name)).first()
    if exists:
        raise HTTPException(status_code=400, detail="La categoría ya existe")

    category = Category(name=data.name.strip(), description=data.description)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_admin),
):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    update_data = data.dict(exclude_unset=True)
    if "name" in update_data and update_data["name"]:
        # validar unique
        exists = session.exec(
            select(Category).where(Category.name == update_data["name"], Category.id != category_id)
        ).first()
        if exists:
            raise HTTPException(status_code=400, detail="Ya existe una categoría con ese nombre")

    for field, value in update_data.items():
        setattr(category, field, value)

    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_admin),
):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    session.delete(category)
    session.commit()
    return {"status": "ok", "message": "Categoría eliminada"}
