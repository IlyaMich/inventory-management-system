from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from fastapi import FastAPI
import os

class DataBase:
    client: AsyncIOMotorClient = None

db = DataBase()

async def get_database(db_name: str):
    # Ensure the client is initialized
    if db.client is None:
        await connect_to_mongo()
    return db.client[db_name]

async def connect_to_mongo():
    #mongo_details = os.getenv("MONGODB_URL", "mongodb://localhost:27017/inventory-mng-local")
    mongo_details = settings.DATABASE_URL
    db.client = AsyncIOMotorClient(mongo_details)
    #db.client = AsyncIOMotorClient("mongodb://localhost:27017/inventory-mng-local")

async def close_mongo_connection():
    db.client.close()

def create_start_app_handler(app: FastAPI) -> callable:
    async def start_app() -> None:
        await connect_to_mongo()
        app.state._db = get_database("inventory-mng-local")
    return start_app

def create_stop_app_handler(app: FastAPI) -> callable:
    async def stop_app() -> None:
        await close_mongo_connection()
    return stop_app