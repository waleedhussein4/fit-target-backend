from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from datetime import datetime
from database import Base

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, autoincrement=True)  # Cloud database unique identifier
    uuid = Column(String, nullable=False, unique=True, index=True) 
    owner = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # Reference to User
    sets = Column(Integer, nullable=False)
    volume = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
      return (f"<Workout(id={self.id}, local_id={self.local_id}, owner={self.owner}, sets={self.sets}, "
        f"volume={self.volume}, start_date={self.start_date}, end_date={self.end_date}, "
        f"last_updated={self.last_updated}, is_synced={self.is_synced})>")
