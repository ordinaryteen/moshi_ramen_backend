from pydantic import BaseModel, ConfigDict
from uuid import UUID

# 1. Base Schema (Shared properties)
class CategoryBase(BaseModel):
    name: str

# 2. Schema buat CREATE (Input dari user)
class CategoryCreate(CategoryBase):
    pass

# 3. Schema buat RESPONSE (Output ke user)

class CategoryResponse(CategoryBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)