from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlmodel import Session
from app.core.database import get_session
from app.services.inventory_service import InventoryService
# de tu security.py real puedes recuperar un rol tipo bodeguero/admin
# from app.core.security import get_current_warehouse_user

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
    # dependencies=[Depends(get_current_warehouse_user)]
)

service = InventoryService()

@router.post("/upload")
async def upload_inventory(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    if not file:
        raise HTTPException(status_code=400, detail="No se envió ningún archivo")

    content = await file.read()
    return service.process_inventory_file(session, content, file.content_type)
