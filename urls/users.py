from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from sqlmodel import Session, or_, select

from config.auth import (
    create_access_token,
    create_refresh_token,
    get_hashed_password,
    is_authenticated,
    verify_password,
    verify_refresh_token,
)
from config.postgres import engine
from models import Token, User

urls = APIRouter(prefix="", tags=["users"])


@urls.post("/users", response_model=User)
def create_user(data: User):
    with Session(engine) as session:
        statement = select(User).where(
            or_(User.email == data.email, User.username == data.username)
        )
        result = session.exec(statement).first()
        if result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="already registered"
            )

        user = User(
            username=data.username,
            email=data.email,
            password=get_hashed_password(data.password),
        )

        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@urls.get("/users", response_model=list[User], dependencies=[Depends(is_authenticated)])
def get_all_users(skip: int = 0, limit: int = 100):
    with Session(engine) as session:
        statement = select(User).offset(skip).limit(limit)
        return session.exec(statement).all()


@urls.get("/users/{id}", response_model=User)
def get_user_by_id(id: int):
    with Session(engine) as session:
        statement = select(User).where(User.id == id)
        user = session.exec(statement).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="USER_NOT_FOUND"
            )
        return user


@urls.delete("/users/{id}", dependencies=[Depends(is_authenticated)])
def delete_user_by_id(id: int):
    with Session(engine) as session:
        statement = select(User).where(User.id == id)
        result = session.exec(statement).one()
        session.delete(result)
        session.commit()
        return status.HTTP_200_OK


@urls.post("/access_token", response_model=Token)
def access_token(response: Response, data: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as session:
        statement = select(User).where(User.username == data.username)
        user = session.exec(statement).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        if not verify_password(data.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        access_token = create_access_token(user.email)
        refresh_token = create_refresh_token(user.email)

        response.set_cookie("access_token", access_token)
        response.set_cookie("refresh_token", refresh_token)

        return {"access_token": access_token, "refresh_token": refresh_token}


@urls.post("/refresh_token", response_model=Token)
def refresh_token(data: Token):
    try:
        is_verified = verify_refresh_token(data.refresh_token)
        if is_verified:
            return {
                "access_token": create_access_token(is_verified["sub"]),
                "refresh_token": data.refresh_token,
            }

    except JWTError as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error))
