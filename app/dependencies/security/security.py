from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError, BaseModel
from ...models.user import User
from ...core.config import settings
#from .security import get_current_active_user
from app.controllers.user_controller import get_user_by_email


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

class TokenData(BaseModel):
    email: str = None

async def get_user(email: str):
    try:
        return await get_user_by_email(email)
    except HTTPException as httpEx:
        # Log the original exception if needed
        print(httpEx)

        # Raise a new HTTPException with a specific status code and a custom detail message
        # Adjust the status code and detail message as needed based on your application's requirements
        raise HTTPException(
            #status_code=status.HTTP_404_NOT_FOUND,  # Use a valid HTTP status code
            #detail=f"User with email {email} not found"  # Custom detail message

            status_code=httpEx.status_code,  # Use a valid HTTP status code
            detail=httpEx.detail  # Custom detail message
        )


async def authenticate_user(email: str, password: str):
    user = await get_user(email)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = await get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Security(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def require_role(required_role: str, current_user: User = Depends(get_current_active_user)):
    if required_role not in current_user.role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
    return current_user