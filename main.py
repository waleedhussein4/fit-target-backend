from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

import Crud.usercrud
import Models.userModel
import Crud, Models, Schemas
import Schemas.userCreate
import Schemas.sync
from database import SessionLocal, engine
import logging

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


@app.put("/users/{user_email}")
def edit_user_profile(
    user_email: str, 
    updates: Schemas.userCreate.UserUpdate, 
    db: Session = Depends(get_db)):
    # Get the user by email
    db_user = Crud.usercrud.get_user_by_email(db, email=user_email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update the user using email
    updated_user = Crud.usercrud.update_user_by_email(
        db, email=user_email, updates=updates.model_dump(exclude_unset=True)
    )
    return {"message": "User updated successfully", "user": updated_user}


logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@app.post("/user/signup", response_model=Schemas.userCreate.UserCreate)
def create_user(user: Schemas.userCreate.UserCreate, db: Session = Depends(get_db)):
    db_user = Crud.usercrud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return Crud.usercrud.create_user(db=db, user=user)

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
            user_id=sync_data.user_id,
            workout_ids=sync_data.workoutsPendingUpload,
            food_entries=sync_data.foodEntriesPendingUpload,
            last_local_sync=sync_data.lastLocalSync,
        )

        return {"sync_status": status}

    except SQLAlchemyError as e:
        # Log SQLAlchemy database errors
        logger.error(f"Database error during sync status check: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error: Database issue")

    except AttributeError as e:
        # Handle attribute errors (e.g., missing fields) and display the received data
        logger.error(f"Attribute error during sync status check: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid data: {sync_data.dict()}")

    except Exception as e:
        # Log any other unexpected errors
        logger.error(f"Unexpected error during sync status check: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error: Unexpected issue")