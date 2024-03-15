from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.utils import PyObjectId
from bson import ObjectId
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    hashedPassword: str
    role: str

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.hashed_password)

    @classmethod
    def hash_password(cls, plain_password):
        return pwd_context.hash(plain_password)

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "hashedPassword": "hashed_password",
                "role": "admin"
            }
        }

        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: lambda oid: str(oid)
        }