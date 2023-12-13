from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from config.postgres import engine
from config.settings import settings
from models import Token, User

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="access_token", scheme_name="JWT")

ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.JWT_SECRET_KEY


def is_authenticated(token: str = Depends(oauth2_scheme)):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = Token(**data)
        with Session(engine) as session:
            statement = select(User).where(User.email == token_data.sub)
            user = session.exec(statement).first()

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user


def get_hashed_password(password):
    return password_context.hash(password)


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def create_access_token(sub: str) -> str:
    expires_delta = datetime.utcnow() + timedelta(weeks=1)
    data = {"exp": expires_delta, "sub": sub}
    return jwt.encode(data, SECRET_KEY, ALGORITHM)


def create_refresh_token(sub: str) -> str:
    expires_delta = datetime.utcnow() + timedelta(weeks=4)
    data = {"exp": expires_delta, "sub": sub}
    return jwt.encode(data, SECRET_KEY, ALGORITHM)


def verify_refresh_token(refresh_token):
    try:
        return jwt.decode(refresh_token, SECRET_KEY, ALGORITHM)
    except JWTError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
