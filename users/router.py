from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.orm import Session

from dependencies import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_db,
    get_hashed_password,
    verify_password,
    verify_refresh_token,
)
from users.models import User
from users.schemas import TokenSchema, UserSchema

urls = APIRouter(prefix="", tags=["users"])


@urls.post("/signup", response_model=UserSchema)
def signup(payload: UserSchema, db: Session = Depends(get_db)):
    if db.query(User).filter_by(email=payload.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    user = User(
        username=payload.username,
        email=payload.email,
        password=get_hashed_password(payload.password.get_secret_value()),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@urls.post("/jwt/login", response_model=TokenSchema)
async def jwt_login(
    response: Response,
    payload: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter_by(username=payload.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    access_token = create_access_token(user.email)
    refresh_token = create_refresh_token(user.email)

    response.set_cookie("access_token", access_token)
    response.set_cookie("refresh_token", refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@urls.post("/jwt/refresh", response_model=TokenSchema)
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


@urls.get("/users", response_model=list[UserSchema])
def get_all_users(
    is_authenticated: get_current_user = Depends(),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return db.query(User).offset(skip).limit(limit).all()


@urls.get("/users/{user_id}", response_model=UserSchema)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
