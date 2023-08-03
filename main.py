from typing import Annotated

from fastapi import FastAPI, status, UploadFile, HTTPException
from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(ge=1)
    name: str = Field(max_length=100)
    age: int = Field(gt=0, le=200)
    location: str | None = None


app = FastAPI()

users_model = [
    User(id=1, name="test1", age=22),
    User(id=2, name="test2", age=32, location="Italy"),
    User(id=3, name="test3", age=42, location="Austria"),
]


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "test"}


@app.get("/users/")
async def users() -> list[User]:
    return users_model


@app.get("/users/{user_id}")
async def users(user_id: int) -> User:
    try:
        user = users_model[user_id - 1]
        return user
    except Exception as e:
        raise HTTPException(status_code=404, detail="NOT_FOUND")


@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User) -> User:
    return user


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename, "content_type": file.content_type}
