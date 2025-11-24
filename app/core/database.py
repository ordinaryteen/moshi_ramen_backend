from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 1. Create Engine
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

# 2. Create SessionLocal Class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Create Base Class
Base = declarative_base()

# 4. Dependency Injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()