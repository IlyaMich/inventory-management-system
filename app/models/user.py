from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.utils import PyObjectId
from bson import ObjectId

class User(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    password: str  # TODO: This should be hashed
    role: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "hashed_password",
                "role": "admin"
            }
        }

        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: lambda oid: str(oid)
        }