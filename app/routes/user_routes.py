from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.dependencies.db.db import get_dal_user
from app.schemas.user_schema import UserCreate, UserDisplay, UserUpdate
from app.db.dal_user import DALUser
from app.controllers import user_controller
from ..models.user import User
from ..dependencies.security.security import get_current_active_user

router = APIRouter()

@router.post("/users/")
async def create_user(user: UserCreate):
    return await user_controller.create_user(user)

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    user = await user_controller.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/")
async def get_all_users(skip: int = 0, limit: int = 10):#, current_user: User = Depends(get_current_active_user)):
    users = await user_controller.get_all_users(skip=skip, limit=limit)
    return users

@router.put("/users/{user_id}")
async def update_user(user_id: str, user: UserUpdate):
    updated_user = await user_controller.update_user(user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    deleted_user = await user_controller.delete_user(user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user