
from pydantic import BaseModel, EmailStr

class SUser(BaseModel):
    id: int
    name: str
    password: str
    email: str


    class Config:
        from_attributes = True

       
       
class SUserAuth(BaseModel):
    email: EmailStr
    password: str
    

class SUserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str


class SUserSecure(BaseModel):
    id: int
    email: EmailStr
    name: str
