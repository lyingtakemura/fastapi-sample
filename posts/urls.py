from fastapi import APIRouter, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from config.database import engine
from posts.models import Post
from posts.schemas import PostInSchema, PostOutSchema

url = APIRouter(prefix="/posts", tags=["posts"])


@url.get("/", response_model=list[PostOutSchema], status_code=status.HTTP_200_OK)
async def select_all():
    with Session(engine) as session:
        return [row.Post.__dict__ for row in session.execute(select(Post)).all()]


@url.post("/", response_model=PostOutSchema, status_code=status.HTTP_201_CREATED)
async def insert(payload: PostInSchema):
    with Session(engine) as session:
        obj = Post(**payload.model_dump())
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj.__dict__
