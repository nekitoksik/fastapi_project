from pydantic import BaseModel

class SUser(BaseModel):
    id: int
    name: str
    photo_url: str
    height: int
    weight: int
    about: str
    city: str
    steps: int


    class Config:
        from_attributes = True

       
       
class SUserCreate(BaseModel):
    name: str
    height: int
    weight: int
    about: str
    city: str
    steps: int
