from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

# --- Tabla de Configuración Global (¡Nueva!) ---
class BusinessSettings(SQLModel, table=True):
    id: Optional[int] = Field(default=1, primary_key=True)
    business_name: str = Field(default="Café Sol")
    # Tasa de impuesto como porcentaje, ej. 12.0 para 12%
    tax_rate: float = Field(default=12.0)
    currency_symbol: str = Field(default="$")
    low_stock_threshold: int = Field(default=10)

# --- Modelos de Usuario y Roles (Actualizados) ---
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True) # <-- Login con Email
    hashed_password: str
    full_name: Optional[str] = None
    # Roles actualizados
    role: str = Field(default="Vendedor") # Admin, Vendedor, Bodeguero
    is_active: bool = Field(default=True)
    
    orders: List["Order"] = Relationship(back_populates="user")

# --- Modelos de Producto (Actualizados) ---
class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sku: str = Field(unique=True, index=True)
    name: str
    category: str = Field(index=True)
    price: float = Field(gt=0)
    stock: int = Field(default=0)
    image_url: Optional[str] = None # <-- Nuevo campo para imagen
    
    order_items: List["OrderItem"] = Relationship(back_populates="product")

# --- Modelos de Órdenes (Actualizados) ---
class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="Pagada") # Pagada, Cancelada
    
    # Nuevos campos de UI
    payment_method: str = Field(default="Efectivo") # Efectivo, Tarjeta, Otros
    subtotal: float # Calculado ANTES de impuestos
    tax_amount: float # El monto de impuesto calculado
    total_amount: float # El total final (subtotal + tax_amount)
    
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")

# --- OrderItem (Sin cambios) ---
class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    quantity: int = Field(gt=0)
    price_at_purchase: float # Precio histórico
    
    order_id: int = Field(foreign_key="order.id")
    order: Order = Relationship(back_populates="items")
    product_id: int = Field(foreign_key="product.id")
    product: Product = Relationship(back_populates="order_items")