from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.db.dal_sale import DALSale
from app.dependencies import get_dal_sale
from app.controllers import sale_controller
from app.schemas.sale_schema import SaleCreate, SaleUpdate, SaleDisplay

router = APIRouter()

@router.post("/sales/")
async def create_sale(sale: SaleCreate):
    return await sale_controller.create_sale(sale)

@router.get("/sales/{sale_id}")
async def get_sale(sale_id: str):
    sale = await sale_controller.get_sale(sale_id)
    if sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale

@router.get("/sales/")
async def get_all_sales(skip: int = 0, limit: int = 10):
    sales = await sale_controller.get_all_sales(skip=skip, limit=limit)
    return sales

@router.put("/sales/{sale_id}")
async def update_sale(sale_id: str, sale: SaleUpdate):
    updated_sale = await sale_controller.update_sale(sale_id, sale)
    if updated_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return updated_sale

@router.delete("/sales/{sale_id}")
async def delete_sale(sale_id: str):
    success = await sale_controller.delete_sale(sale_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sale not found")
    return {"detail": "Sale deleted successfully"}