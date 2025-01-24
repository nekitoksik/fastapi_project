from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta, timezone
from pydantic import EmailStr

from jose import jwt

from app.admins.services import AdminService
from app.config import settings
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pbkdf2_sha256.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pbkdf2_sha256.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )

    return encoded_jwt


async def verify_user(email: EmailStr, password: str):
    existing_user = await AdminService.find_one_or_none(email=email)

    if not existing_user and not verify_password(password, existing_user.password):
        return None
    return existing_user 

