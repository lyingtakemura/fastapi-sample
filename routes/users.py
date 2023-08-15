from fastapi import APIRouter, HTTPException, status
from models import User, UserResponse

users_router = APIRouter()

users = [User(id=1, username="test_user324")]


@users_router.get("/users", response_model=list[UserResponse])
def get_users():
    return users


@users_router.get("/users/{id}")
def get_user(id: int):
    user = User(id=1, username="test_user324")
    if id == user.id:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")


@users_router.post("/users")
def create_user(user: User) -> list[User]:
    users.append(user)
    return users
