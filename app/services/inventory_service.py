import pandas as pd
from io import BytesIO

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.category import Category
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.inventory import InventoryUploadResponse, InventoryUploadSummary

repo = ProductRepository()


class InventoryService:

    def process_inventory_file(self, session: Session, file_content: bytes, file_type: str) -> InventoryUploadResponse:
        """Carga masiva de inventario desde CSV o Excel.

        Columnas requeridas:
        - code, name, price, stock

        Columnas opcionales (para categorías):
        - category_id (int)
        - category (texto) -> busca/crea en tabla categories
        """
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

            # Normalizar nombres de columnas
            df.columns = [str(c).strip().lower() for c in df.columns]

            required_cols = {"code", "name", "price", "stock"}
            if not required_cols.issubset(set(df.columns)):
                raise HTTPException(
                    status_code=400,
                    detail=f"Las columnas requeridas son: {', '.join(sorted(required_cols))}",
                )

            updated = 0
            created = 0
            errors = 0
            error_messages: list[str] = []

            def get_or_create_category_id(category_name: str) -> int:
                name_clean = category_name.strip()
                existing = session.exec(select(Category).where(Category.name == name_clean)).first()
                if existing:
                    return existing.id

                cat = Category(name=name_clean)
                session.add(cat)
                session.commit()
                session.refresh(cat)
                return cat.id

            def parse_category_id(row) -> int | None:
                # 1) category_id
                if "category_id" in row and pd.notna(row["category_id"]) and str(row["category_id"]).strip() != "":
                    try:
                        return int(float(row["category_id"]))
                    except Exception:
                        raise ValueError(f"category_id inválido: {row['category_id']}")

                # 2) category (texto)
                if "category" in row and pd.notna(row["category"]) and str(row["category"]).strip() != "":
                    return get_or_create_category_id(str(row["category"]))

                return None

            for idx, row in df.iterrows():
                try:
                    code = str(row["code"]).strip()
                    name = str(row["name"]).strip()
                    price = float(row["price"])
                    stock = float(row["stock"])

                    if not code:
                        raise ValueError("code vacío")
                    if not name:
                        raise ValueError("name vacío")

                    category_id = parse_category_id(row)

                    existing = repo.get_by_code(session, code)
                    if existing:
                        existing.name = name
                        existing.price = price
                        existing.stock = stock
                        existing.category_id = category_id
                        repo.save(session, existing)
                        updated += 1
                    else:
                        product = Product(
                            code=code,
                            name=name,
                            category_id=category_id,
                            price=price,
                            stock=stock,
                            is_active=True,
                        )
                        repo.save(session, product)
                        created += 1

                except Exception as e:
                    errors += 1
                    error_messages.append(f"Fila {idx + 1}: {e}")

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
