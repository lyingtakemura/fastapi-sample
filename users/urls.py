from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from config.database import get_session
from users.models import User
from users.schemas import UserResponseSchema

url = APIRouter(prefix="/api/v1/users", tags=["users"])


@url.get("/", response_model=list[UserResponseSchema], status_code=status.HTTP_200_OK)
async def get_all_users(session=Depends(get_session)):
    statement = select(User).options(joinedload(User.posts))
    return [row for row in session.execute(statement).unique().scalars().all()]


@url.get("/{id}", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
async def get_user(id, session=Depends(get_session)):
    try:
        statement = select(User).filter(User.id == id).options(joinedload(User.posts))
        return session.execute(statement).unique().scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@url.delete("/{id}", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
async def delete_user(id, session=Depends(get_session)):
    try:
        statement = select(User).filter(User.id == id)
        row = session.execute(statement).scalar_one()
        session.delete(row)
        session.commit()
        return row
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
