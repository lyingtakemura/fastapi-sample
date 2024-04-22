from fastapi import APIRouter, HTTPException, status
from sqlalchemy import exc, select
from sqlalchemy.orm import Session

from config.database import engine
from posts.models import Post
from posts.schemas import PostInSchema, PostOutSchema

url = APIRouter(prefix="/posts", tags=["posts"])


@url.get("/", response_model=list[PostOutSchema], status_code=status.HTTP_200_OK)
async def select_all():
    with Session(engine) as session:
        return [row.Post.__dict__ for row in session.execute(select(Post)).all()]


@url.get("/{id}", response_model=PostOutSchema, status_code=status.HTTP_200_OK)
async def select_one(id):
    with Session(engine) as session:
        try:
            statement = select(Post).filter_by(id=id)
            obj = session.execute(statement).scalar_one()
            return obj.__dict__
        except exc.NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@url.post("/", response_model=PostOutSchema, status_code=status.HTTP_201_CREATED)
async def create_post(payload: PostInSchema):
    with Session(engine) as session:
        obj = Post(**payload.model_dump())
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj.__dict__


@url.put("/{id}", response_model=PostOutSchema, status_code=status.HTTP_200_OK)
async def update_post(id: int, title: str, body: str):
    with Session(engine) as session:
        try:
            statement = select(Post).filter_by(id=id)
            obj = session.execute(statement).scalar_one()
            obj.title = title
            obj.body = body
            session.commit()
            session.refresh(obj)
            return obj.__dict__
        except exc.NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@url.delete("/{id}", response_model=PostOutSchema, status_code=status.HTTP_200_OK)
async def delete_post(id: int):
    with Session(engine) as session:
        try:
            statement = select(Post).filter_by(id=id)
            obj = session.execute(statement).scalar_one()
            session.delete(obj)
            session.commit()
            return obj.__dict__
        except exc.NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
