from pydantic import BaseModel, EmailStr


class SAdminAuth(BaseModel):
    email: EmailStr
    password: str
