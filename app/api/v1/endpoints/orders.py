from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud import crud_order
from app.schemas.order import OrderCreate, OrderResponse

router = APIRouter()

@router.post("/orders", response_model=OrderResponse)
def create_new_order(order: OrderCreate, db: Session = Depends(get_db)):
    """
    Create new order with items.
    Server will calculate prices, tax, and total.
    Stock will be reduced automatically.
    """
    return crud_order.create_order(db=db, order_in=order)