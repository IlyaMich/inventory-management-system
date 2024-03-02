from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Sale Base Schema
class SaleBase(BaseModel):
    product_id: str
    user_id: str
    quantity: int
    sale_price: float

# Schema for Recording a Sale
class SaleCreate(SaleBase):
    sale_date: datetime = datetime.now()

class SaleUpdate(SaleBase):
    sale_date: datetime

# Schema for Sale in Responses
class SaleDisplay(SaleBase):
    id: str = Field(None, alias="_id")
    sale_date: datetime

    class Config:
        orm_mode = True
