from typing import List
from app.db.database import get_database
from fastapi import HTTPException
from app.db.dal_sale import DALSale
from app.schemas.sale_schema import SaleCreate, SaleUpdate, SaleDisplay
from bson import ObjectId

async def create_sale(sale_in: SaleCreate) -> SaleDisplay:
    db = await get_database("inventory-mng-local")  # Ensure this is awaited
    dal_sale = DALSale(db=db)

    try:
        # Additional business logic validations can be added here
        created_sale = await dal_sale.create(sale_in)
        return serialize_sale(created_sale)
    except Exception as e:
        # Log the error here
        raise HTTPException(status_code=500, detail=str(e))

async def update_sale(sale_id: str, sale_in: SaleUpdate) -> SaleDisplay:
    db = await get_database("inventory-mng-local")  # Ensure this is awaited
    dal_sale = DALSale(db=db)

    try:
        existing_sale = await dal_sale.read(sale_id)
        if not existing_sale:
            raise HTTPException(status_code=404, detail="Sale not found")
        updated_sale = await dal_sale.update(sale_id, sale_in)
        return serialize_sale(updated_sale)
    except Exception as e:
        # Log the error here
        raise HTTPException(status_code=500, detail=str(e))

async def delete_sale(sale_id: str):
    db = await get_database("inventory-mng-local")  # Ensure this is awaited
    dal_sale = DALSale(db=db)
    
    try:
        deleted_sale = await dal_sale.delete(sale_id)
        if not deleted_sale:
            raise HTTPException(status_code=404, detail="Sale not found")
        return serialize_sale(deleted_sale)
    except Exception as e:
        # Log the error here
        raise HTTPException(status_code=500, detail=str(e))
    
async def get_sale(sale_id: str):
    db = await get_database("inventory-mng-local")  # Ensure this is awaited
    dal_sale = DALSale(db=db)

    try:
        sale = await dal_sale.read(sale_id)
        if not sale:
            raise HTTPException(status_code=404, detail="Sale not found")
        return serialize_sale(sale)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_all_sales(skip: int = 0, limit: int = 10):
    db = await get_database("inventory-mng-local")  # Ensure this is awaited
    dal_sale = DALSale(db=db)

    try:
        sales = await dal_sale.list(skip=skip, limit=limit)
        return serialize_sales(sales)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def serialize_sale(unserialized):
    return {key: str(value) if isinstance(value, ObjectId) else value for key, value in unserialized.items()}

def serialize_sales(unserialized):
    serialized_sales = []
    for sale in unserialized:
        serialized_sales.append(serialize_sale(sale))
    
    return serialized_sales