from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud import crud_order
from app.schemas.order import OrderCreate, OrderResponse
from app.websockets.manager import manager
from app.schemas.order import OrderStatusUpdate
from app.api.v1 import deps
from app.models.user import User 
import json

router = APIRouter()

@router.post("/orders", response_model=OrderResponse)
async def create_new_order(order: OrderCreate, db: Session = Depends(get_db), current_user = Depends(deps.get_current_user)):
    """
    Create new order with items.
    Server will calculate prices, tax, and total.
    Stock will be reduced automatically.
    """
    order.staff_id = current_user.id
    new_order = crud_order.create_order(db=db, order_in=order)
    
    notification_data = {
        "event": "NEW_ORDER",
        "order_id": str(new_order.id),
        "bill_name": new_order.bill_name,
        "total": float(new_order.grand_total) 
    }

    await manager.broadcast(notification_data)
    
    return new_order

@router.patch("/orders/{order_id}/status", response_model=OrderResponse)
async def update_order_status(order_id: str, status_update: OrderStatusUpdate, db: Session = Depends(get_db), current_user: User = Depends(deps.get_current_user)):
    updated_order = crud_order.update_status(db=db, order_id=order_id, new_status=status_update.status)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    await manager.broadcast({
        "event": "STATUS_UPDATE",
        "order_id": str(updated_order.id),
        "new_status": updated_order.status.value,
        "bill_name": updated_order.bill_name
    })

    return updated_order