from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from dependencies import get_db
from repositories.jwt import JWTRepository
from schemas import TokenSchema

urls = APIRouter(prefix="", tags=["jwt"])


@urls.post("/jwt/login", response_model=TokenSchema)
async def jwt_login(
    response: Response,
    payload: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db),
):
    repository = JWTRepository(session)
    return repository.login(payload, response)


@urls.post("/jwt/refresh", response_model=TokenSchema)
async def jwt_refresh(
    payload: TokenSchema,
    session: Session = Depends(get_db),
):
    repository = JWTRepository(session)
    return repository.refresh(payload)
