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
    targetWeight: Optional[float] 
    targetPeriod: Optional[int]  
    weightMeasurementPreference: Optional[str]  
