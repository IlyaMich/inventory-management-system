from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.controllers import transaction_controller
from app.dependencies.db.db import get_dal_transaction
from app.db.dal_transaction import DALTransaction
from app.schemas.transaction_schema import TransactionCreate, TransactionUpdate, TransactionDisplay

router = APIRouter()

@router.post("/transactions/")
async def create_transaction(transaction: TransactionCreate):
    return await transaction_controller.create_transaction(transaction)

@router.get("/transactions/{transaction_id}")
async def get_transaction(transaction_id: str):
    transaction = await transaction_controller.get_transaction(transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.get("/transactions/")
async def get_all_transactions(skip: int = 0, limit: int = 10):
    transactions = await transaction_controller.get_all_transactions(skip=skip, limit=limit)
    return transactions

@router.put("/transactions/{transaction_id}")
async def update_transaction(transaction_id: str, transaction: TransactionUpdate):
    updated_transaction = await transaction_controller.update_transaction(transaction_id, transaction)
    if updated_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return updated_transaction

@router.delete("/transactions/{transaction_id}")
async def delete_transaction(transaction_id: str):
    success = await transaction_controller.delete_transaction(transaction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"detail": "Transaction deleted successfully"}
