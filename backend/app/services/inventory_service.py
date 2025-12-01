import pandas as pd
from io import BytesIO
from fastapi import HTTPException
from sqlmodel import Session
from app.repositories.product_repository import ProductRepository
from app.schemas.inventory import InventoryUploadResponse, InventoryUploadSummary

repo = ProductRepository()

class InventoryService:

    def process_inventory_file(self, session: Session, file_content: bytes, file_type: str) -> InventoryUploadResponse:
        """Carga masiva de inventario desde CSV o Excel."""
        try:
            buffer = BytesIO(file_content)

            if file_type == "text/csv":
                df = pd.read_csv(buffer)
            elif file_type in [
                "application/vnd.ms-excel",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ]:
                df = pd.read_excel(buffer)
            else:
                raise HTTPException(status_code=400, detail=f"Tipo de archivo no soportado: {file_type}")

            required_cols = {"code", "name", "price", "stock"}
            if not required_cols.issubset(df.columns.str.lower()):
                raise HTTPException(
                    status_code=400,
                    detail=f"Las columnas requeridas son: {', '.join(required_cols)}"
                )

            updated = 0
            created = 0
            errors = 0
            error_messages: list[str] = []

            for idx, row in df.iterrows():
                try:
                    code = str(row["code"]).strip()
                    name = str(row["name"]).strip()
                    price = float(row["price"])
                    stock = float(row["stock"])
                    category = str(row.get("category", "")).strip() or None

                    existing = repo.get_by_code(session, code)
                    if existing:
                        existing.name = name
                        existing.category = category
                        existing.price = price
                        existing.stock = stock
                        repo.save(session, existing)
                        updated += 1
                    else:
                        from app.models.product import Product
                        product = Product(
                            code=code,
                            name=name,
                            category=category,
                            price=price,
                            stock=stock,
                        )
                        repo.save(session, product)
                        created += 1
                except Exception as e:
                    errors += 1
                    error_messages.append(f"Fila {idx}: {e}")

            summary = InventoryUploadSummary(updated=updated, created=created, errors=errors)
            status = "success" if errors == 0 else "partial"

            return InventoryUploadResponse(
                status=status,
                summary=f"{updated} productos actualizados, {created} creados, {errors} errores",
                details=summary,
                errors=error_messages or None,
            )

        except HTTPException:
            raise
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=f"Transacción fallida: {str(e)}")
