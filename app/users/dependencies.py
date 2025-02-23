from fastapi import Depends, HTTPException
from jose import JWTError, jwt

from app.config import settings
from app.users.services import UserService
from app.exceptions import InccorrectJWTTokenException, UserNotFoundException

async def get_current_user(token: str):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
        user_id = payload.get("sub")
        if not user_id:
            raise UserNotFoundException
        
        user = await UserService.find_by_id(int(user_id))
        if not user:
            raise UserNotFoundException
        
        return user
    except JWTError:
        raise InccorrectJWTTokenException
