from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float

class RunStats(Base):
    __tablename__ = "run_stats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    distance = Column(Float)
    steps = Column(Integer)
    calories_burned = Column(Float)
    average_speed = Column(Float)

    user = relationship("Users", backref="run_stats")