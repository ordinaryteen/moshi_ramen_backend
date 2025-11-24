from sqlalchemy.orm import Session
from app.models.product import Category
from app.schemas.product import CategoryCreate

def create_category(db: Session, category: CategoryCreate):
    db_obj = Category(name=category.name)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    
    return db_obj

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()