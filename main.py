from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Query

import Crud.usercrud
import Models.userModel
import Models.workoutModel
import Crud, Models, Schemas
import Schemas.userCreate
import Schemas.sync
from database import SessionLocal, engine
import logging

logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

Models.userModel.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/user/signin")
def sign_in(user: Schemas.userCreate.UserSignIn, db: Session = Depends(get_db)):
    db_user= Crud.usercrud.get_user_by_email(db, user.email)
    if not db_user or user.password != db_user.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"message": "Sign in successful", "user": db_user}

@app.get("/users/", response_model=list[Schemas.userCreate.UserCreate])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = Crud.usercrud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_email}", response_model=Schemas.userCreate.UserCreate)
def read_user(user_email: str, db: Session = Depends(get_db)):
    db_user = Crud.usercrud.get_user_by_email(db, user_email=user_email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/")
def edit_user_profile(
    updates: Schemas.userCreate.UserUpdate,
    user_email: str = Query(..., description="Email of the user to update"),
    db: Session = Depends(get_db)):
    logger.info(f"Updating user with email: {user_email}")
    
    
    db_user = Crud.usercrud.get_user_by_email(db, email=user_email)
    if not db_user:
        logger.warning(f"User with email {user_email} not found.")
        raise HTTPException(status_code=404, detail="User not found")
    
    # Extract updates for allowed fields
    allowed_updates = updates.model_dump(exclude_unset=True)
    logger.info(f"Allowed updates: {allowed_updates}")
    
    
    updated_user = Crud.usercrud.update_user_by_email(
        db, email=user_email, updates=allowed_updates
    )
    logger.info(f"User with email {user_email} updated successfully.")
    return {"message": "User updated successfully", "user": updated_user}



@app.post("/user/signup", response_model=Schemas.userCreate.UserCreate)
def create_user(user: Schemas.userCreate.UserCreate, db: Session = Depends(get_db)):
    db_user = Crud.usercrud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return Crud.usercrud.create_user(db=db, user=user)

@app.post("/sync")
def sync_workouts(sync_data: Schemas.sync.SyncRequest, db: Session = Depends(get_db)):
    """
    Syncs workout data between the client and server.
    """
    try:
        # Call the CRUD function to sync workout data and send back the workouts to be locally stored
        incoming_workouts = Crud.usercrud.sync_workouts(db=db, sync_data=sync_data)
        return {"workouts": incoming_workouts}
    
    except SQLAlchemyError as e:
        # Log SQLAlchemy database errors
        logger.error(f"Database error during workout sync: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error: Database issue")
    
    except AttributeError as e:
        # Handle attribute errors (e.g., missing fields) and display the received data and their types
        logger.error(f"Attribute error during workout sync: {str(e)}")
        logger.error(f"Received data: {sync_data}")
        logger.error(f"Data types: {[(key, type(value)) for key, value in sync_data.dict().items()]}")
        raise HTTPException(status_code=400, detail="Bad request: Missing or incorrect fields")
    
    except Exception as e:
        # Log any other unexpected errors
        logger.error(f"Unexpected error during workout sync: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error: Unexpected issue: {str(e)}")
    


@app.post("/sync/check-sync")
def check_sync_status(
    sync_data: Schemas.sync.CheckSync,
    db: Session = Depends(get_db)
):
    """
    Checks sync status for the given workout IDs and food entries.
    """
    try:
        # Call the CRUD function to check sync status
        status = Crud.usercrud.check_sync_status(
            db=db,
            userId=sync_data.userId,
            workoutsPendingUpload=sync_data.workoutsPendingUpload,
            foodEntriesPendingUpload=sync_data.foodEntriesPendingUpload,
            lastLocalSync=sync_data.lastLocalSync,
        )

        return {"is_synced": status}

    except SQLAlchemyError as e:
        # Log SQLAlchemy database errors
        logger.error(f"Database error during sync status check: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error: Database issue")

    except AttributeError as e:
        # Handle attribute errors (e.g., missing fields) and display the received data and their types
        logger.error(f"Attribute error during sync status check: {str(e)}")
        logger.error(f"Received data: {sync_data}")
        logger.error(f"Data types: {[(key, type(value)) for key, value in sync_data.dict().items()]}")
        raise HTTPException(status_code=400, detail="Bad request: Missing or incorrect fields")

    except Exception as e:
        # Log any other unexpected errors
        logger.error(f"Unexpected error during sync status check: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error: Unexpected issue: {str(e)}")
    
