from sqlalchemy.orm import Session
import Models.userModel, Schemas.userCreate
from Models.userModel import User
from typing import List, Any, Dict
from fastapi.exceptions import HTTPException

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

def update_user_by_email(db: Session, email: str, updates: dict):
    user = db.query(Models.userModel.User).filter(Models.userModel.User.email == email).first()
    if not user:
        return None

    # Dynamically update fields based on the updates dictionary
    for key, value in updates.items():
        if hasattr(user, key):
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

def check_sync_status(db: Session, userId: str, workoutsPendingUpload: List[Dict[str, str]], foodEntriesPendingUpload: List[Dict[str, str]], lastLocalSync: str):
    # Validate user existence
    user = db.query(Models.userModel.User).filter(Models.userModel.User.id == userId).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    has_pending_uploads = bool(workoutsPendingUpload)
    
    # Identify server-side unsynced workouts (created after last sync)
    server_unsynced_workouts = db.query(Models.workoutModel.Workout).filter(
        Models.workoutModel.Workout.owner == user.id,
        Models.workoutModel.Workout.created_at > lastLocalSync
    ).all()
    
    unsynced_food_entries = []  # TODO: Implement food entry sync logic later
    
    sync_required = has_pending_uploads or bool(server_unsynced_workouts)

    # Construct and return the sync status
    return not sync_required