import uuid
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

# Tabel Categories
class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    
    products = relationship("Product", back_populates="category")

# Tabel Products
class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
    unit_price = Column(Numeric(10, 2), nullable=False) 
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))
    
    category = relationship("Category", back_populates="products")