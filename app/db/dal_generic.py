from typing import Type, List, Any, Dict
from pydantic import BaseModel
from app.db.database import get_database
from bson import ObjectId

class DALGeneric:
    def __init__(self, model: Type[BaseModel], collection: str):
        self.model = model
        self.collection = collection

    async def create(self, document: BaseModel) -> dict:
        document = document.dict(by_alias=True)  # Use by_alias to convert 'id' to '_id'
        result = await self.collection.insert_one(document)
        document['_id'] = result.inserted_id
        return document

    async def read(self, document_id: str) -> dict:
        document = await self.collection.find_one({"_id": ObjectId(document_id)})
        if document:
            return document
        return {}

    async def update(self, document_id: str, document: BaseModel) -> dict:
        updated_document = document.dict(by_alias=True, exclude_unset=True)
        await self.collection.update_one({"_id": ObjectId(document_id)}, {"$set": updated_document})
        return await self.read(document_id)

    async def delete(self, document_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(document_id)})
        return result.deleted_count > 0

    async def list(self, skip: int = 0, limit: int = 10) -> List[dict]:
        cursor = self.collection.find().skip(skip).limit(limit)
        documents: List[dict] = []
        async for document in cursor:
            documents.append(document)
        return documents