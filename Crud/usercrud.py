from sqlalchemy.orm import Session
import Models.userModel, Schemas.userCreate

def get_user(db: Session, user_id: int):
    return db.query(Models.userModel.User).filter(Models.userModel.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(Models.userModel.User).filter(Models.userModel.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Models.userModel.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: Schemas.userCreate.UserCreate):
    firstName = user.firstName
    lastName = user.lastName
    email = user.email
    password = user.password
    age = user.age
    gender = user.gender
    weight = user.weight
    height = user.height
    targetWeight = user.targetWeight
    targetPeriod = user.targetPeriod
    measurementPreference = user.weightMeasurementPreference
    db_user = Models.userModel.User(email=user.email,password=user.password,
                                    firstName=user.firstName, lastName=user.lastName,
                                    age = user.age, gender = user.gender,
                                    weight= user.weight, height = user.height,
                                    targetWeight= user.targetWeight,targetPeriod= user.targetPeriod,
                                    weightMeasurementPreference= user.weightMeasurementPreference)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, updates: dict):
    user = db.query(Models.userModel.User).filter(Models.userModel.User.id == user_id).first()
    if not user:
        return None

    # Dynamically update fields based on the updates dictionary
    for key, value in updates.items():
        if hasattr(user, key):
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user
