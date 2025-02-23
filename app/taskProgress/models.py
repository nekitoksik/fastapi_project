from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float

class UserTaskProgress(Base):
    __tablename__ = "user_task_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    progress = Column(Integer, default=0)
    completed_at = Column(DateTime)

    user = relationship("Users", backref="task_progress")
    task = relationship("Tasks", backref="user_progress")

    