from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import Crud.usercrud
import Models.userModel
import Crud, Models, Schemas
import Schemas.userCreate
from database import SessionLocal, engine

Models.userModel.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/user/signup", response_model=Schemas.userCreate.UserCreate)
def create_user(user: Schemas.userCreate.UserCreate, db: Session = Depends(get_db)):
    db_user = Crud.usercrud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return Crud.usercrud.create_user(db=db, user=user)


@app.post("/user/signin")
def sign_in(user: Schemas.userCreate.UserSignIn, db: Session = Depends(get_db)):
    db_user = Crud.usercrud.get_user_by_email(db, user.email)
    if not db_user or user.password != db_user.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"message": "Sign in successful", "user_email": user.email}


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

