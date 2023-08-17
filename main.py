from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from auth import hash_password
from database import session

app = FastAPI()


@app.on_event("startup")
def on_startup():
    print("__EVENT_APP_STARTUP__")


def db():
    try:
        db = session()
        yield db
    finally:
        db.close()


# USERS
@app.post("/users/", response_model=schemas.User)
def create_user(payload: schemas.UserCreate, db: Session = Depends(db)):
    user = db.query(models.User).filter_by(email=payload.email).first()
    if user:
        raise HTTPException(
            status_code=400, detail="User with provided email already exists"
        )
    else:
        user = models.User(
            email=payload.email,
            hashed_password=hash_password.create_hash(payload.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(db)):
    return db.query(models.User).offset(skip).limit(limit).all()


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(db)):
    user = db.query(models.User).filter_by(id=user_id).first()
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


# ITEMS
@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, payload: schemas.ItemCreate, db: Session = Depends(db)
):
    item = models.Item(
        title=payload.title, description=payload.description, user_id=user_id
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(db)):
    return db.query(models.Item).offset(skip).limit(limit).all()
