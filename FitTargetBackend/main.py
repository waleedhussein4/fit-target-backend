from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from Models.userModel import User as UserModel 
from Schemas.userCreate import UserCreate  

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/user/signup")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    if db.query(UserModel).filter(UserModel.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = UserModel(
        firstName=user.firstName,
        lastName=user.lastName,
        email=user.email,
        password=user.password,
        age=user.age,
        gender=user.gender,
        weight=user.weight,
        height=user.height,
        targetWeight=user.targetWeight,
        weightMeasurementPreference=user.weightMeasurementPreference,
        targetPeriod=user.targetPeriod,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User successfully created"}
