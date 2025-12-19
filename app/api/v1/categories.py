from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryRead)
def create_category(payload: CategoryCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(Category).where(Category.name == payload.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="La categoría ya existe")
    cat = Category(**payload.dict())
    session.add(cat)
    session.commit()
    session.refresh(cat)
    return cat

@router.get("/", response_model=list[CategoryRead])
def list_categories(session: Session = Depends(get_session)):
    return session.exec(select(Category)).all()

@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, payload: CategoryUpdate, session: Session = Depends(get_session)):
    cat = session.get(Category, category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    data = payload.dict(exclude_unset=True)
    for k, v in data.items():
        setattr(cat, k, v)
    session.add(cat)
    session.commit()
    session.refresh(cat)
    return cat

@router.delete("/{category_id}")
def delete_category(category_id: int, session: Session = Depends(get_session)):
    cat = session.get(Category, category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    session.delete(cat)
    session.commit()
    return {"message": "Categoría eliminada"}
