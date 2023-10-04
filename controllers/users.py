from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_current_user, get_db
from repositories.users import UserRepository
from schemas import UserSchema

urls = APIRouter(prefix="", tags=["users"])


@urls.post("/signup", response_model=UserSchema)
def signup(
    payload: UserSchema,
    session: Session = Depends(get_db),
):
    repository = UserRepository(session)
    return repository.insert_user(payload)


@urls.get("/users", response_model=list[UserSchema])
def select_users(
    is_authenticated: get_current_user = Depends(),
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_db),
):
    repository = UserRepository(session)
    return repository.select_users(skip, limit)


@urls.get("/users/{id}", response_model=UserSchema)
def select_user(id: int, session: Session = Depends(get_db)):
    repository = UserRepository(session)
    return repository.select_user(id)


@urls.delete("/users/{id}")
def delete_user(id: int, session: Session = Depends(get_db)):
    repository = UserRepository(session)
    return repository.delete_user(id)
