from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import models
import schemas
from authentication import oauth2_scheme
from settings import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=False)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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
        token_data = schemas.Token(**payload)
        user = db.query(models.User).filter_by(email=token_data.sub).first()
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
