from app.db.dal_generic import DALGeneric
from app.models.user import User
import logging

# Basic logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

class DALUser(DALGeneric):
    def __init__(self, db):
        super().__init__(model=User, collection=db["users"])

    async def get_user_by_email(self, email: str):
        logger.info(f'username email: {email}')
        user_document = await self.collection.find_one({"email": email})
        logger.info(user_document)
        if user_document:
            #return User(**user_document)  # Convert the MongoDB document to a Pydantic User model instance
            return user_document
        return None