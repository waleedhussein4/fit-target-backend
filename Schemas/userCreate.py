from pydantic import BaseModel, EmailStr

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