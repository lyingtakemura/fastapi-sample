from datetime import datetime, timedelta, timezone
from os import environ

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select

from auth.schemas import TokenSchema
from config.database import get_session
from users.models import User

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, environ.get("SECRET_KEY"), algorithm="HS256")
    return encoded_jwt


def get_current_user(token=Depends(oauth2_scheme), session=Depends(get_session)):
    try:
        payload = jwt.decode(token, environ.get("SECRET_KEY"), algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    statement = select(User).filter(User.username == username)
    user = session.execute(statement).scalar_one()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user
