import enum

from app.database import Base
from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, Text
from sqlalchemy.schema import CheckConstraint

class TaskType(enum.Enum):
    DAILY = "daily"
    ONE_TIME = "one-time"


class TargetType(enum.Enum):
    FRIEND = "Друзья"
    STEPS = "Шаги"
    KILOMETER = "Километры"


class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, nullable=False)
    task_type = Column(Enum(TaskType), nullable=False)
    name = Column(String(255), nullable=False)
    target_type = Column(Enum(TargetType), nullable=False)
    target_value = Column(Integer)
    reward = Column(Integer)
    description = Column(Text)
    image_path = Column(String(255), default="null_image.png")
    # is_active = Column(Boolean, default=True)
    # valid_until = Column(DateTime)