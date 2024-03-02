from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.utils import PyObjectId
from bson import ObjectId

class Transaction(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    type: str  # sale, restock, return, etc.
    product_id: str
    quantity: int
    transaction_date: datetime = datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "type": "sale",
                "product_id": "product_id",
                "quantity": 1,
                "transaction_date": "2023-01-01T00:00:00"
            }
        }

        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: lambda oid: str(oid)
        }