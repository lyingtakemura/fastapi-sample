import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.orm import Session

from authentication import (
    create_access_token,
    create_refresh_token,
    get_hashed_password,
    verify_password,
    verify_refresh_token,
)
from database import get_db
from dependencies import get_current_user
from models import User as UserModel
from schemas import Token as TokenSchema
from schemas import User as UserSchema

app = FastAPI()


@app.get("/users", response_model=list[UserSchema])
def get_all_users(
    is_authenticated: get_current_user = Depends(),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return db.query(UserModel).offset(skip).limit(limit).all()


@app.get("/users/{user_id}", response_model=UserSchema)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter_by(id=user_id).first()
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


# # ITEMS
# @app.get("/items", response_model=list[schemas.Item])
# def get_all_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# @app.post("/users/{user_id}/items", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, payload: schemas.Item, db: Session = Depends(get_db)
# ):
#     item = models.Item(
#         title=payload.title, description=payload.description, user_id=user_id
#     )
#     db.add(item)
#     db.commit()
#     db.refresh(item)
#     return item


# AUTHENTICATION
@app.post("/signup", response_model=UserSchema)
def signup(payload: UserSchema, db: Session = Depends(get_db)):
    if db.query(UserModel).filter_by(email=payload.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    user = UserModel(
        username=payload.username,
        email=payload.email,
        password=get_hashed_password(payload.password.get_secret_value()),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@app.post("/jwt/login", response_model=TokenSchema)
async def jwt_login(
    payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter_by(username=payload.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }


@app.post("/jwt/refresh", response_model=TokenSchema)
async def jwt_refresh(payload: TokenSchema):
    try:
        is_verified = verify_refresh_token(payload.refresh_token)
        if is_verified:
            return {
                "access_token": create_access_token(is_verified["sub"]),
                "refresh_token": payload.refresh_token,
            }
    except JWTError as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error))


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)
