from pydantic import BaseModel, Field
from datetime import datetime

# Transaction Base Schema
class TransactionBase(BaseModel):
    product_id: str
    type: str  # "sale", "restock", "return", etc.
    quantity: int

# Schema for Logging a Transaction
class TransactionCreate(TransactionBase):
    transaction_date: datetime = datetime.now()

class TransactionUpdate(TransactionBase):
    transaction_date: datetime

# Schema for Transaction in Responses
class TransactionDisplay(TransactionBase):
    id: str = Field(None, alias="_id")
    transaction_date: datetime

    class Config:
        orm_mode = True
