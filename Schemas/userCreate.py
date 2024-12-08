from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str
    age: int
    gender: str
    weight: float
    height: float
    targetWeight: float
    weightMeasurementPreference: str
    targetPeriod: int

class UserSignIn(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    age: Optional[int]
    weight: Optional[float]
    height: Optional[float]
    target_weight: Optional[float]
    target_period: Optional[int]
    weight_measurement_preference: Optional[str]
