from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.utils import PyObjectId
from bson import ObjectId

class UserBase(BaseModel):
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: str

class UserDisplay(UserBase):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    class Config:
        orm_mode = True
    
    class Config:
        orm_mode = True
        json_encoders = {
            ObjectId: lambda oid: str(oid)
        }
