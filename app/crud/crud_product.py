from sqlalchemy.orm import Session
from app.models.product import Category, Product
from app.schemas.product import CategoryCreate, ProductCreate

def create_category(db: Session, category: CategoryCreate):
    db_obj = Category(name=category.name)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    
    return db_obj

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()

def create_product(db: Session, product: ProductCreate):
    db_obj = Product(
        name=product.name,
        description=product.description,
        unit_price=product.unit_price,
        stock=product.stock,
        is_active=product.is_active,
        category_id=product.category_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()