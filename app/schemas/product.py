from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from decimal import Decimal

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)

# --- PRODUCT SCHEMAS ---

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    unit_price: Decimal
    stock: int = 0
    is_active: bool = True
    category_id: UUID

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: UUID
    
    model_config = ConfigDict(from_attributes=True)