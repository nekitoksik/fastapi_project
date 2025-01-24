import enum
from app.database import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, Table, ForeignKey, Enum
from sqlalchemy.orm import relationship, backref

class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"


class FriendshipStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    photo_url = Column(String(255))
    height = Column(Integer)
    weight = Column(Integer)
    about = Column(String(255))
    city = Column(String(255))
    steps = Column(Integer, default=0)
    points = Column(Integer, default=0)
    created_at = Column(DateTime)
    is_admin = Column(Boolean, default=False)
    role = Column(Enum(UserRole), default=UserRole.USER)

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