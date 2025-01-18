from app.database import Base
from sqlalchemy import Column, Integer, ForeignKey, Table, CheckConstraint
from sqlalchemy.orm import relationship

from app.users.models import Users

class Friendship(Base):
    __tablename__ = "friendship"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    friend_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

    user = relationship("Users", foreign_keys=[user_id], backref="friendships1")
    friend = relationship("Users", foreign_keys=[friend_id], backref="friendships2")