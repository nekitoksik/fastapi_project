from app.database import Base
from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship, backref


friendship = Table(
    "friendship",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("friend_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    photo_url = Column(Text)
    height = Column(Integer)
    weight = Column(Integer)
    about = Column(Text)
    city = Column(String(255))
    steps = Column(Integer)
    

    friends = relationship(
        "Users",
        secondary=friendship,
        primaryjoin=(friendship.c.user_id == id),
        secondaryjoin=(friendship.c.friend_id == id),
        backref=backref("friend_of", lazy='selectin'),
        lazy='selectin'
    )