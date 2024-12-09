from sqlalchemy import Column, Integer, String, Float, Boolean, BIGINT

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    age = Column(Integer)
    gender = Column(String)
    weight = Column (Float)
    height = Column(Float)
    targetWeight = Column(Float)
    weightMeasurementPreference = Column(String)
    targetPeriod = Column(Integer)
    last_sync_time = Column(BigInt, nullable=True)






