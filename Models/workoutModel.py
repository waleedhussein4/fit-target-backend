from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from database import Base

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, autoincrement=True)  # Cloud database unique identifier
    uuid = Column(String, nullable=False, unique=True, index=True) 
    owner = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # Reference to User
    sets = Column(Integer, nullable=False)
    volume = Column(Integer, nullable=False)
    start_date = Column(Integer, nullable=False)
    end_date = Column(Integer, nullable=False)
    created_at = Column(Integer, nullable=False)

    def __repr__(self):
      return (f"<Workout(id={self.id}, local_id={self.local_id}, owner={self.owner}, sets={self.sets}, "
        f"volume={self.volume}, start_date={self.start_date}, end_date={self.end_date}, "
        f"last_updated={self.last_updated}, is_synced={self.is_synced})>")

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, autoincrement=True)  # Cloud database unique identifier
    uuid = Column(String, nullable=False, unique=True, index=True)
    workout_uuid = Column(String, ForeignKey("workouts.uuid"), nullable=False, index=True)  # Reference to Workout
    reference_id = Column(Integer, nullable=False, index=True)  # Reference to Workout

    def __repr__(self):
      return (f"<Exercise(id={self.id}, workout_id={self.workout_id}, name={self.name}, "
        f"created_at={self.created_at})>")
      
class Set(Base):
    __tablename__ = "sets"

    id = Column(Integer, primary_key=True, autoincrement=True)  # Cloud database unique identifier
    uuid = Column(String, nullable=False, unique=True, index=True)
    exercise_uuid = Column(String, ForeignKey("exercises.uuid"), nullable=False, index=True)  # Reference to Exercise
    weight = Column(Float, nullable=False)
    reps = Column(Integer, nullable=False)

    def __repr__(self):
      return (f"<Set(id={self.id}, exercise_id={self.exercise_id}, weight={self.weight}, "
        f"reps={self.reps}, created_at={self.created_at})>")
