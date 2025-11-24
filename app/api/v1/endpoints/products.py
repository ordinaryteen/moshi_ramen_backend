from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.crud import crud_product
from app.schemas.product import CategoryResponse, CategoryCreate, ProductResponse, ProductCreate

router = APIRouter()

@router.post("/categories", response_model=CategoryResponse)
def create_new_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """
    Create a new product category (e.g., 'Ramen', 'Drinks')
    """
    
    return crud_product.create_category(db=db, category=category)

@router.get("/categories", response_model=List[CategoryResponse])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud_product.get_categories(db, skip=skip, limit=limit)
    return categories


@router.post("/products", response_model=ProductResponse) 
def create_new_product(product: ProductCreate, db: Session = Depends(get_db)):
    category = crud_product.create_product(db=db, product=product)

    if not category:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Category with ID {product.category_id} not found."
        )

    return crud_product.create_product(db=db, product=product)

@router.get("/products", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_product.get_products(db, skip=skip, limit=limit)