from app.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.schema import CheckConstraint

class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, nullable=False)
    task_type = Column(String(255), CheckConstraint("type IN ('daily', 'one-time')"), nullable=False)
    name = Column(String(255), nullable=False)
    target_type = Column(String(255), CheckConstraint("target_type IN ('friend', 'steps', 'kilometer')"), nullable=False)
    target_value = Column(Integer)
    reward = Column(Integer)
    image_path = Column(String(255))
