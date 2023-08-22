from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

import models
import schemas
from authentication import oauth2_scheme
from database import db
from settings import settings


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(db)
):
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.algorithm]
        )
        token_data = schemas.TokenPayload(**payload)
        user = db.query(models.User).filter_by(email=token_data.sub).first()
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user
