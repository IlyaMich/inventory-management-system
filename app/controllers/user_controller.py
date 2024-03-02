import logging
from typing import List
from bson import ObjectId
from app.db.database import get_database
from fastapi import HTTPException
from app.db.dal_user import DALUser
from app.schemas.user_schema import UserCreate, UserUpdate, UserDisplay

# Basic logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

async def create_user(user_in: UserCreate):
    db = await get_database("inventory-mng-local")  # Ensure this is awaited
    dal_user = DALUser(db=db)
    
    try:
        existing_user = await dal_user.get_user_by_email(user_in.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        created_user = await dal_user.create(user_in)
        return serialize_user(created_user)
    except Exception as e:
        # Log the error here
        raise HTTPException(status_code=500, detail=str(e))

async def update_user(user_id: str, user_in: UserUpdate):
    db = await get_database("inventory-mng-local")  # Ensure this is awaited
    dal_user = DALUser(db=db)
    
    try:
        existing_user = await dal_user.read(user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        updated_user = await dal_user.update(user_id, user_in)
        return serialize_user(updated_user)
    except Exception as e:
        # Log the error here
        raise HTTPException(status_code=500, detail=str(e))
    
async def get_user(user_id: str):
    db = await get_database("inventory-mng-local")  # Ensure this is awaited
    dal_user = DALUser(db=db)
    
    try:
        user = await dal_user.read(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return serialize_user(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def delete_user(sale_id: str):
    db = await get_database("inventory-mng-local")  # Ensure this is awaited
    dal_user = DALUser(db=db)
    
    try:
        deleted_user = await dal_user.delete(sale_id)
        if not deleted_user:
            raise HTTPException(status_code=404, detail="User not found")
        return serialize_user(deleted_user)
    except Exception as e:
        # Log the error here
        raise HTTPException(status_code=500, detail=str(e))

async def get_all_users(skip: int = 0, limit: int = 10):
    db = await get_database("inventory-mng-local")  # Ensure this is awaited
    dal_user = DALUser(db=db)
    
    try:
        users = await dal_user.list(skip=skip, limit=limit)
        return serialize_users(users)
    except Exception as e:
        logger.info("Thrown from controller")
        raise HTTPException(status_code=500, detail=str(e))
    
def serialize_user(unserialized):
    return {key: str(value) if isinstance(value, ObjectId) else value for key, value in unserialized.items()}

def serialize_users(unserialized):
    serialized_users = []
    for user in unserialized:
        serialized_users.append(serialize_user(user))
    
    return serialized_users