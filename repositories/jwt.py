from datetime import datetime, timedelta

from fastapi import HTTPException, Response, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from configuration.settings import settings
from dependencies import verify_password
from models import User
from schemas import TokenSchema


class JWTRepository:
    def __init__(self, session: Session):
        self.session = session

    def login(
        self,
        payload: TokenSchema,
        response: Response,
    ):
        user = self.session.query(User).filter_by(username=payload.username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        if not verify_password(payload.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        access_token = self._create_access_token(user.email)
        refresh_token = self._create_refresh_token(user.email)

        response.set_cookie("access_token", access_token)
        response.set_cookie("refresh_token", refresh_token)

        return TokenSchema(access_token=access_token, refresh_token=refresh_token)

    def refresh(
        self,
        payload: TokenSchema,
    ):
        try:
            is_verified = self._verify_refresh_token(payload.refresh_token)
            if is_verified:
                return TokenSchema(
                    access_token=self._create_access_token(is_verified["sub"]),
                    refresh_token=payload.refresh_token,
                )
        except JWTError as error:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=str(error)
            )

    def _create_access_token(self, sub: str) -> str:
        expires_delta = datetime.utcnow() + timedelta(weeks=1)
        payload = {"exp": expires_delta, "sub": sub}
        return jwt.encode(payload, settings.jwt_secret_key, settings.algorithm)

    def _create_refresh_token(self, sub: str) -> str:
        expires_delta = datetime.utcnow() + timedelta(weeks=4)
        payload = {"exp": expires_delta, "sub": sub}
        return jwt.encode(payload, settings.jwt_secret_key, settings.algorithm)

    def _verify_refresh_token(self, refresh_token):
        try:
            return jwt.decode(
                refresh_token, settings.jwt_secret_key, settings.algorithm
            )
        except JWTError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)
            )
