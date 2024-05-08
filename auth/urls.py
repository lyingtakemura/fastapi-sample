from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_, select
from sqlalchemy.exc import NoResultFound

from auth.schemas import TokenSchema
from auth.services import create_access_token, get_password_hash, verify_password
from config.database import get_session
from users.models import User
from users.schemas import UserPayloadSchema, UserResponseSchema

url = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@url.post(
    "/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED
)
async def register(payload: UserPayloadSchema, session=Depends(get_session)):
    statement = select(User).filter(
        or_(User.username == payload.username, User.email == payload.email)
    )
    if session.execute(statement).scalar():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    row = User(
        email=payload.email,
        username=payload.username,
        password=get_password_hash(payload.password),
    )
    session.add(row)
    session.commit()
    session.refresh(row)
    return row


@url.post("/login", response_model=TokenSchema, status_code=status.HTTP_200_OK)
async def login(
    payload=Depends(OAuth2PasswordRequestForm), session=Depends(get_session)
):
    try:
        statement = select(User).filter(User.username == payload.username)
        row = session.execute(statement).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if not verify_password(payload.password, row.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token({"sub": row.username})
    return {"access_token": access_token, "token_type": "bearer"}
