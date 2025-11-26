from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from enum import Enum

# Enum Status (Harus sama kayak di Model)
class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"

# --- ITEM SCHEMA (Input dari User) ---
class OrderItemCreate(BaseModel):
    product_id: UUID
    quantity: int

# --- ORDER SCHEMA (Input dari User) ---
class OrderCreate(BaseModel):
    staff_id: Optional[int] = None
    bill_name: Optional[str] = None 
    items: List[OrderItemCreate]

# --- RESPONSE SCHEMAS ---
class OrderItemResponse(BaseModel):
    id: UUID
    product_id: UUID
    item_name_snapshot: str
    unit_price_snapshot: Decimal
    quantity: int
    sub_total_item: Decimal
    
    model_config = ConfigDict(from_attributes=True)

class OrderResponse(BaseModel):
    id: UUID
    
    order_number: Optional[int] = None 
    
    staff_id: int
    bill_name: Optional[str]
    status: OrderStatus
    
    created_at: datetime 
    
    sub_total: Decimal
    tax_amount: Decimal
    grand_total: Decimal
    
    items: List[OrderItemResponse] 

    model_config = ConfigDict(from_attributes=True)