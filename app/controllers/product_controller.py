from typing import List
from fastapi import HTTPException
from app.db.dal_product import DALProduct
from app.db.database import get_database
from app.dependencies.db.db import database_name
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductDisplay
import logging
from bson import ObjectId

# Basic logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


async def create_product(product_in: ProductCreate):# -> ProductDisplay:
    db = await get_database("inventory-mng-local")  # Ensure this is awaited
    dal_product = DALProduct(db=db)
    
    try:
        # Add specific validation or business logic here
        product = await dal_product.create(product_in)
        return serialize_product(product)
    except Exception as e:
        # Log the error here
        raise HTTPException(status_code=500, detail=str(e))

async def update_product(product_id: str, product_in: ProductUpdate):# -> ProductDisplay:
    db = await get_database("inventory-mng-local")  # Ensure this is awaited
    dal_product = DALProduct(db=db)
    
    try:
        existing_product = await dal_product.read(product_id)
        if not existing_product:
            raise HTTPException(status_code=404, detail="Product not found")
        product = await dal_product.update(product_id, product_in)
        return serialize_product(product)
    except Exception as e:
        # Log the error here
        raise HTTPException(status_code=500, detail=str(e))
    
async def get_product(product_id: str):# -> ProductDisplay:
    db = await get_database("inventory-mng-local")  # Ensure this is awaited
    dal_product = DALProduct(db=db)
    
    try:
        product = await dal_product.read(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return serialize_product(product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def delete_product(sale_id: str):
    db = await get_database("inventory-mng-local")  # Ensure this is awaited
    dal_product = DALProduct(db=db)
    
    try:
        deleted_product = await dal_product.delete(sale_id)
        if not deleted_product:
            raise HTTPException(status_code=404, detail="Sale not found")
        return serialize_product(deleted_product)
    except Exception as e:
        # Log the error here
        raise HTTPException(status_code=500, detail=str(e))

async def get_all_products(skip: int = 0, limit: int = 10):# -> List[ProductDisplay]:
    db = await get_database("inventory-mng-local")  # Ensure this is awaited
    dal_product = DALProduct(db=db)

    try:
        products = await dal_product.list(skip=skip, limit=limit)
        logger.info(products)
        return serialize_products(products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def serialize_product(unserialized):
    return {key: str(value) if isinstance(value, ObjectId) else value for key, value in unserialized.items()}

def serialize_products(unserialized):
    serialized_products = []
    for product in unserialized:
        serialized_products.append(serialize_product(product))
    
    return serialized_products