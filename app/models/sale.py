from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.utils import PyObjectId
from bson import ObjectId

class Sale(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    product_id: str
    user_id: str
    quantity: int
    sale_price: float
    sale_date: datetime = datetime.now()
    customer_details: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "product_id": "product_id",
                "user_id": "user_id",
                "quantity": 1,
                "sale_price": 9.99,
                "sale_date": "2023-01-01T00:00:00",
                "customer_details": {
                    "name": "Customer Name",
                    "contact": "Contact Information"
                }
            }
        }

        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: lambda oid: str(oid)
        }