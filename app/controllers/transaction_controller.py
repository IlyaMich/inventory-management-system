from typing import List
from bson import ObjectId
from app.db.database import get_database
from fastapi import HTTPException
from app.db.dal_transaction import DALTransaction
from app.schemas.transaction_schema import TransactionCreate, TransactionUpdate, TransactionDisplay


async def create_transaction(transaction_in: TransactionCreate):
    db = await get_database("inventory-mng-local")  # Ensure this is awaited
    dal_transaction = DALTransaction(db=db)
    
    try:
        # Additional business logic validations can be added here
        created_transaction = await dal_transaction.create(transaction_in)
        return serialize_transaction(created_transaction)
    except Exception as e:
        # Log the error here
        raise HTTPException(status_code=500, detail=str(e))

async def update_transaction(transaction_id: str, transaction_in: TransactionUpdate):
    db = await get_database("inventory-mng-local")  # Ensure this is awaited
    dal_transaction = DALTransaction(db=db)
    
    try:
        existing_transaction = await dal_transaction.read(transaction_id)
        if not existing_transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        updated_transaction = await dal_transaction.update(transaction_id, transaction_in)
        return serialize_transaction(updated_transaction)
    except Exception as e:
        # Log the error here
        raise HTTPException(status_code=500, detail=str(e))

async def delete_transaction(transaction_id: str):
    db = await get_database("inventory-mng-local")  # Ensure this is awaited
    dal_transaction = DALTransaction(db=db)
    
    try:
        deleted_transaction = await dal_transaction.delete(transaction_id)
        if not deleted_transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return serialize_transaction(deleted_transaction)
    except Exception as e:
        # Log the error here
        raise HTTPException(status_code=500, detail=str(e))
    
async def get_transaction(transaction_id: str) -> TransactionDisplay:
    db = await get_database("inventory-mng-local")  # Ensure this is awaited
    dal_transaction = DALTransaction(db=db)
    
    try:
        transaction = await dal_transaction.read(transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return serialize_transaction(transaction)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_all_transactions(skip: int = 0, limit: int = 10) -> List[TransactionDisplay]:
    db = await get_database("inventory-mng-local")  # Ensure this is awaited
    dal_transaction = DALTransaction(db=db)
    
    try:
        transactions = await dal_transaction.list(skip=skip, limit=limit)
        return serialize_transactions(transactions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def serialize_transaction(unserialized):
    return {key: str(value) if isinstance(value, ObjectId) else value for key, value in unserialized.items()}

def serialize_transactions(unserialized):
    serialized_transactions = []
    for transaction in unserialized:
        serialized_transactions.append(serialize_transaction(transaction))
    
    return serialized_transactions