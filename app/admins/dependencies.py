from fastapi import Request, Depends
from app.exceptions import AccessTokenIsNotFound, InccorrectJWTTokenException, TokenExpiredException, UserNotFoundException
from jose import jwt, JWTError
from datetime import datetime, timezone

from app.config import settings
from app.admins.services import AdminService

def get_token(request: Request):
    token = request.cookies.get("tatrun_token")

    if not token:
        raise AccessTokenIsNotFound
    return token


async def get_current_user(token: str = Depends(get_token)):

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )

    except JWTError:
        raise InccorrectJWTTokenException
    
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise TokenExpiredException

    admin_id: str = payload.get("sub")
    if not admin_id:
        raise UserNotFoundException
    
    admin = await AdminService.get_user_by_id(int())
    if not admin:
        raise UserNotFoundException

        
    return admin

