from sqlalchemy.orm import Session
import Models.userModel, Schemas.userCreate, Schemas.sync
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

    # Dynamically update fields 
    for key, value in updates.items():
        if hasattr(user, key):
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

def check_sync_status(db: Session, userId: str, workoutsPendingUpload: List[Dict[str, str]], foodEntriesPendingUpload: List[Dict[str, str]], lastLocalSync: str):
    lastLocalSync = int(lastLocalSync)
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
    
    # return only whether its synced or not
    return not sync_required

def sync_workouts(db: Session, sync_data: Schemas.sync.SyncRequest):
    user = db.query(Models.userModel.User).filter(Models.userModel.User.id == sync_data.userId).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    workouts = sync_data.workoutsPendingUpload
    exercises = sync_data.exercisesPendingUpload
    sets = sync_data.setsPendingUpload
    
    # save workouts to database
    for workout in workouts:
        db_workout = Models.workoutModel.Workout(
            uuid=workout["UUID"],
            owner=user.id,
            sets=workout["SETS"],
            volume=workout["VOLUME"],
            start_date=int(workout["START_DATE"]),
            end_date=int(workout["END_DATE"]),
            created_at=int(workout["CREATED_AT"])
        )
        db.add(db_workout)
    
    db.commit()
        
    # save exercises to database
    for exercise in exercises:
        db_exercise = Models.workoutModel.Exercise(
            uuid=exercise["UUID"],
            workout_uuid=exercise["WORKOUT_UUID"],
            reference_id=exercise["REFERENCE_ID"]
        )
        db.add(db_exercise)
        
    db.commit()
        
    # save sets to database
    for set in sets:
        db_set = Models.workoutModel.Set(
            uuid=set["UUID"],
            exercise_uuid=set["EXERCISE_UUID"],
            weight=set["WEIGHT"],
            reps=set["REPS"]
        )
        db.add(db_set)
        
    db.commit()
    
    # get workouts that are stored on the cloud but not locally by comparing lastLocalSync with each workout's created_at
    incoming_workouts = db.query(Models.workoutModel.Workout).filter(
        Models.workoutModel.Workout.owner == user.id,
        int(Models.workoutModel.Workout.created_at) > int(lastLocalSync)
    ).all()
    
    # set user last_sync_time to the current time like 1733710186918
    user.last_sync_time = int(time.time() * 1000)
    db.commit()    
    
    return incoming_workouts
    

