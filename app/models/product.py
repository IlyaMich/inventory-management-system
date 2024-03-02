from pydantic import BaseModel, Field
from typing import Optional
from app.utils import PyObjectId
from bson import ObjectId

class Product(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    category: str
    price: float
    quantity: int
    description: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Product Name",
                "category": "Product Category",
                "price": 9.99,
                "quantity": 100,
                "description": "Product Description"
            }
        }

        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: lambda oid: str(oid)
        }