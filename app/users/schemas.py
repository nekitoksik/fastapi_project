from pydantic import BaseModel, Field
from typing import Optional

class SUser(BaseModel):
    id: int
    name: str
    phone_number: str
    jwt_token: Optional[str] = ""
    photo_url: Optional[str]
    height: int
    weight: int
    about: str
    city: str
    steps: int
    points: int

    class Config:
        from_attributes = True
        
class SUserUpdate(BaseModel):
    name: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    about: Optional[str] = None
    city: Optional[str] = None
    steps: Optional[int] = None
    
    class Config:
        from_attributes = True
       
class SUserCreate(BaseModel):
    name: str
    phone_number: str
    height: int
    weight: int
    about: str
    city: str
    steps: int


class PhoneRequest(BaseModel):
    phone: str = Field(..., exmaple="+79123456789")


class VerifyCodeRequest(BaseModel):
    phone: str
    code: str = Field(..., min_length=6, max_length=6)

