from app.database import Base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    photo_url = Column(Text)
    height = Column(Integer)
    weight = Column(Integer)
    about = Column(Text)
    city = Column(String(255))

    friends = relationship(
        "app.users.models.Users",  # Полный путь
        secondary="app.friendship.models.Friendship",  # Полный путь к Friendship
        primaryjoin="app.users.models.Users.id==app.friendship.models.Friendship.user_id",  # Полный путь
        secondaryjoin="app.users.models.Users.id==app.friendship.models.Friendship.friend_id",  # Полный путь
        backref="friend_of",
        lazy='selectin'
    )
