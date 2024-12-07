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
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    weight: Optional[float]
    height: Optional[float]
    targetWeight: Optional[float]
    weightMeasurementPreference: Optional[str]
    targetPeriod: Optional[int]

    class Config:
        orm_mode = True
