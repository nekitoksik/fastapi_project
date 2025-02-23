import enum
from datetime import datetime
from app.database import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, Table, ForeignKey, Enum
from sqlalchemy.orm import relationship, backref


class FriendshipStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, nullable=False)
    verification_code = Column(String(6))
    code_expires_at = Column(DateTime)
    jwt_token = Column(String(500), default="")
    name = Column(String(255), nullable=False, default="Новый пользователь")
    photo_url = Column(String(255), default='null_image.png')
    height = Column(Integer, default=0)
    weight = Column(Integer, default=0)
    about = Column(String(255), default=' ')
    city = Column(String(255), default=' ')
    steps = Column(Integer, default=0)
    points = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now())

    # Relationships для удобства доступа к друзьям
    friendships = relationship("Friendship", foreign_keys="Friendship.requester_id")
    friend_requests = relationship("Friendship", foreign_keys="Friendship.recipient_id")



class Friendship(Base):
    __tablename__ = "friendships"

    id = Column(Integer, primary_key=True, index=True)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(FriendshipStatus), default=FriendshipStatus.PENDING)

    requester = relationship("Users", foreign_keys=[requester_id])
    recipient = relationship("Users", foreign_keys=[recipient_id])