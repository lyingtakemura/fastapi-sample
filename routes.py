from fastapi import APIRouter, HTTPException, status, Depends
from schemas import User
from hash import HashPassword

users_router = APIRouter(tags=["User"])
hash_password = HashPassword()


# @users_router.post("/register")
# async def register(user: User) -> list[User]:
#     user = User(email=user.email, password=hash_password.create_hash(user.password))
#     return user


# @users_router.post("/login")
# async def login(user: User) -> str:
#     hashed_password = hash_password.create_hash(user.password)
#     verified = hash_password.verify_hash(user.password, hashed_password)
#     if verified:
#         return "loged in"
#     else:
#         return "wrong credentials"
