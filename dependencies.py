from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from models import User
from schemas import TokenSchema
from settings import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=False)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="jwt/login", scheme_name="JWT")


def get_db():
    try:
        db = session()
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.algorithm]
        )
        token_data = TokenSchema(**payload)
        user = db.query(User).filter_by(email=token_data.sub).first()
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user


def get_mongodb():
    try:
        client = MongoClient("localhost", 27017)
        db = client["test-db"]
        yield db
    finally:
        client.close()


def get_hashed_password(password):
    return password_context.hash(password)


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def create_access_token(sub: str) -> str:
    expires_delta = datetime.utcnow() + timedelta(weeks=1)
    payload = {"exp": expires_delta, "sub": sub}
    return jwt.encode(payload, settings.jwt_secret_key, settings.algorithm)


def create_refresh_token(sub: str) -> str:
    expires_delta = datetime.utcnow() + timedelta(weeks=4)
    payload = {"exp": expires_delta, "sub": sub}
    return jwt.encode(payload, settings.jwt_secret_key, settings.algorithm)


def verify_refresh_token(refresh_token):
    try:
        return jwt.decode(refresh_token, settings.jwt_secret_key, settings.algorithm)
    except JWTError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
