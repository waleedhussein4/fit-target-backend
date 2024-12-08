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

    # Dynamically update fields 
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
    
    # return only whether its synced or not
    return not sync_required

def sync_workouts(db: Session, sync_data: Schemas.sync.SyncRequest):
    # add new workouts to the server database
    # add new exercises to the server database
    # add new sets to the server database
    
    # Fetch unsynced server-side workouts where created_at is later than sync_data.lastLocalSync
    unsynced_workouts = db.query(Models.workoutModel.Workout).filter(
        Models.workoutModel.Workout.owner == sync_data.userId,
        Models.workoutModel.Workout.created_at > sync_data.lastLocalSync
    ).all()
    
    # Process client-pending workouts
    for workout in sync_data.workoutsPendingUpload:
        existing_workout = db.query(Models.workoutModel.Workout).filter(Models.workoutModel.Workout.uuid == workout["UUID"]).first()
        if not existing_workout:
            # Add new workout to the server database
            new_workout = Models.workoutModel.Workout(
                uuid=workout["UUID"],
                owner=sync_data.userId,
                volume=workout["VOLUME"],
                start_date=workout["START_DATE"],
                end_date=workout.get("END_DATE"),
                created_at=workout["CREATED_AT"]
            )
            db.add(new_workout)
        
        # Process exercises for the current workout
        for exercise in workout["EXERCISES"]:
            existing_exercise = db.query(Models.workoutModel.Exercise).filter(Models.workoutModel.Exercise.uuid == exercise["UUID"]).first()
            if not existing_exercise:
                # Add new exercise to the server database
                new_exercise = Models.workoutModel.Exercise(
                    uuid=exercise["UUID"],
                    workout_uuid=workout["UUID"],
                    reference_id=exercise["REFERENCE_ID"]
                )
                db.add(new_exercise)
            
            # Process sets for the current exercise
            for set in exercise["SETS"]:
                existing_set = db.query(Models.workoutModel.Set).filter(Models.workoutModel.Set.uuid == set["UUID"]).first()
                if not existing_set:
                    # Add new set to the server database
                    new_set = Models.workoutModel.Set(
                        uuid=set["UUID"],
                        exercise_uuid=exercise["UUID"],
                        weight=set["WEIGHT"],
                        reps=set["REPS"]
                    )
                    db.add(new_set)
    
    db.commit()
    #return unsynced_workouts to be locally stored
    return unsynced_workouts

