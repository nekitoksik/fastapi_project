from pydantic import BaseModel

from app.users.models import FriendshipStatus

class SendFriendRequestSchema(BaseModel):
    user_id: int
    friend_id: int

class RespondFriendRequestSchema(BaseModel):
    user_id: int
    friend_id: int
    accept: bool

class FriendRequestSchema(BaseModel): # Для отображения запросов в друзья
    id: int
    user_id: int
    status: FriendshipStatus

class FriendSchema(BaseModel):
    id: int
    name: str
    photo_url: str
    city: str
    steps: int
    points: int