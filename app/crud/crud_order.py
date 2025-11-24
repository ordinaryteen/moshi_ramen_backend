from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.schemas.order import OrderCreate
from fastapi import HTTPException

def create_order(db: Session, order_in: OrderCreate):
    sub_total_accumulated = 0
    db_items = []
    
    for item_in in order_in.items:
        # Fetch Product dari DB buat dapet harga ASLI (Security)
        product = db.query(Product).filter(Product.id == item_in.product_id).first()
        
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item_in.product_id} not found")
        
        if product.stock < item_in.quantity:
             raise HTTPException(status_code=400, detail=f"Not enough stock for {product.name}")

        price_snapshot = product.unit_price 
        item_sub_total = price_snapshot * item_in.quantity
        
        product.stock -= item_in.quantity
        
        # Create OrderItem Object (Belum save ke DB, baru di memory list)
        db_item = OrderItem(
            product_id=product.id,
            quantity=item_in.quantity,
            item_name_snapshot=product.name,    
            unit_price_snapshot=price_snapshot,  
            sub_total_item=item_sub_total
        )
        db_items.append(db_item)
        
        # Akumulasi Subtotal
        sub_total_accumulated += item_sub_total

    # 3. Calculate Tax & Grand Total
    TAX_RATE = 0.15 
    tax_amount = sub_total_accumulated * TAX_RATE
    grand_total = sub_total_accumulated + tax_amount
    
    # 4. Create Order Header
    db_order = Order(
        staff_id=order_in.staff_id,
        bill_name=order_in.bill_name,
        sub_total=sub_total_accumulated,
        tax_amount=tax_amount,
        grand_total=grand_total,
        status=OrderStatus.PENDING
    )
    
    # 5. Transaction Commit
    db.add(db_order)
    db.flush() 
    
    for item in db_items:
        item.order_id = db_order.id
        db.add(item)
        
    db.commit() 
    db.refresh(db_order)
    
    return db_order