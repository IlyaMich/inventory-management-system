from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.dependencies.db.db import get_dal_product
from app.schemas.product_schema import ProductCreate, ProductDisplay, ProductUpdate
from app.db.dal_product import DALProduct
from app.controllers import product_controller
import logging
from bson import ObjectId

# Basic logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/products/")#, response_model=ProductDisplay)
async def create_product(product: ProductCreate):
    return await product_controller.create_product(product)

@router.get("/products/{product_id}")#, response_model=ProductDisplay)
async def get_product(product_id: str):
    product = await product_controller.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/products/")#, response_model=List[ProductDisplay])
async def get_all_products(skip: int = 0, limit: int = 10):
    products = await product_controller.get_all_products(skip=skip, limit=limit)
    logger.info(products)

    #serialized_products = []
    #for product in products:
    #    serialized_product = {key: str(value) if isinstance(value, ObjectId) else value for key, value in product.items()}
    #    serialized_products.append(serialized_product)
    return products

@router.put("/products/{product_id}")#, response_model=ProductDisplay)
async def update_product(product_id: str, product: ProductUpdate):
    updated_product = await product_controller.update_product(product_id, product)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/products/{product_id}")#, response_model=ProductDisplay)
async def delete_product(product_id: str):
    deleted_product = await product_controller.delete_product(product_id)
    if deleted_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return deleted_product