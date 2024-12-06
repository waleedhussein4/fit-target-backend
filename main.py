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
    user = Crud.usercrud.get_user_by_email(db, email)
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"message": "Sign in successful", "user_id": user.id, "email": user.email}


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