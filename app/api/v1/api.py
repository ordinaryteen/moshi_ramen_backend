from fastapi import APIRouter
from app.api.v1.endpoints import products, orders 

api_router = APIRouter()

api_router.include_router(auth.router, tags=["Authentication"])
api_router.include_router(products.router, tags=["Products & Categories"])
api_router.include_router(orders.router, tags=["Orders"]) 