from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import exc, select

from config.database import get_session
from posts.models import Post
from posts.schemas import PostInSchema, PostOutSchema

url = APIRouter(prefix="/posts", tags=["posts"])


@url.post("/", response_model=PostOutSchema, status_code=status.HTTP_201_CREATED)
async def create_post(data: PostInSchema, session: get_session = Depends()):
    obj = Post(**data.model_dump())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj.__dict__


@url.get("/", response_model=list[PostOutSchema], status_code=status.HTTP_200_OK)
async def get_all_posts(session: get_session = Depends()):
    return [row.Post.__dict__ for row in session.execute(select(Post)).all()]


@url.get("/{id}", response_model=PostOutSchema, status_code=status.HTTP_200_OK)
async def get_post(id, session: get_session = Depends()):
    try:
        statement = select(Post).filter_by(id=id)
        obj = session.execute(statement).scalar_one()
        return obj.__dict__
    except exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@url.put("/{id}", response_model=PostOutSchema, status_code=status.HTTP_200_OK)
async def update_post(id, title: str, body: str, session: get_session = Depends()):
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
async def delete_post(id, session: get_session = Depends()):
    try:
        statement = select(Post).filter_by(id=id)
        obj = session.execute(statement).scalar_one()
        session.delete(obj)
        session.commit()
        return obj.__dict__
    except exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
