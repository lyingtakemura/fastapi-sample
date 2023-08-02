from typing import Annotated

from fastapi import FastAPI, status, UploadFile
from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(max_length=100)
    age: int = Field(gt=0, le=200)
    location: str | None = None


app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "test"}


@app.get("/users/")
async def users() -> list[User]:
    return [
        User(name="test1", age=22),
        User(name="test2", age=32, location="Italy"),
        User(name="test3", age=42, location="Austria"),
    ]


@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User) -> User:
    return user


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename, "content_type": file.content_type}
