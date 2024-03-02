from pydantic import BaseModel, Field, validator
from typing import Optional
from app.utils import PyObjectId
from bson import ObjectId

# Product Base Schema
class ProductBase(BaseModel):
    name: str
    category: str
    price: float
    quantity: int
    description: str

# Schema for Product Creation
class ProductCreate(ProductBase):
    pass

# Schema for Product Update
class ProductUpdate(ProductBase):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    description: Optional[str] = None

# Schema for Product in Responses
class ProductDisplay(ProductBase):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        orm_mode = True
        json_encoders = {
            ObjectId: lambda oid: str(oid)
        }