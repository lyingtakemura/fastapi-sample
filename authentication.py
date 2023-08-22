from datetime import datetime, timedelta

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from settings import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", scheme_name="JWT")


def get_hashed_password(password):
    return password_context.hash(password)


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def create_access_token(sub: str, expires_delta: int = None) -> str:
    if expires_delta:
        expires_delta = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=1)

    payload = {"exp": expires_delta, "sub": sub}
    return jwt.encode(payload, settings.jwt_secret_key, settings.algorithm)


def create_refresh_token(sub: str, expires_delta: int = None) -> str:
    if expires_delta:
        expires_delta = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=60)

    payload = {"exp": expires_delta, "sub": sub}
    return jwt.encode(payload, settings.jwt_secret_key, settings.algorithm)


def verify_refresh_token(refresh_token):
    try:
        return jwt.decode(refresh_token, settings.jwt_secret_key, settings.algorithm)
    except JWTError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
