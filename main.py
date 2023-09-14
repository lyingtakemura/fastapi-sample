import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.orm import Session

import models
import schemas
from authentication import (
    create_access_token,
    create_refresh_token,
    get_hashed_password,
    verify_password,
    verify_refresh_token,
)
from database import get_db
from dependencies import get_current_user

app = FastAPI()


@app.get("/users", response_model=list[schemas.User])
def get_all_users(
    is_authenticated: get_current_user = Depends(),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return db.query(models.User).offset(skip).limit(limit).all()


@app.get("/users/{user_id}", response_model=schemas.User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(id=user_id).first()
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


# ITEMS
@app.get("/items", response_model=list[schemas.Item])
def get_all_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Item).offset(skip).limit(limit).all()


@app.post("/users/{user_id}/items", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, payload: schemas.Item, db: Session = Depends(get_db)
):
    item = models.Item(
        title=payload.title, description=payload.description, user_id=user_id
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


# AUTHENTICATION
@app.post("/signup", response_model=None)
def signup(payload: schemas.User, db: Session = Depends(get_db)):
    if db.query(models.User).filter_by(email=payload.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Already exists"
        )

    user = models.User(
        username=payload.username,
        email=payload.email,
        password=get_hashed_password(payload.password.get_secret_value()),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@app.post("/jwt/login", response_model=schemas.Token)
async def jwt_login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(models.User).filter_by(username=form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username",
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password",
        )

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }


@app.post("/jwt/refresh", response_model=schemas.Token)
async def jwt_refresh(payload: schemas.Token):
    try:
        is_verified = verify_refresh_token(payload.refresh_token)
        if is_verified:
            return {
                "access_token": create_access_token(is_verified["sub"]),
                "refresh_token": payload.refresh_token,
            }
    except JWTError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)
