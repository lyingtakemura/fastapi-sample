from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import exc, select

from auth.services import get_current_user
from config.database import get_session
from posts.models import Post
from posts.schemas import PostPayloadSchema, PostResponseSchema

url = APIRouter(prefix="/api/v1/posts", tags=["posts"])


@url.post("/", response_model=PostResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_post(
    payload: PostPayloadSchema,
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):
    row = Post(title=payload.title, body=payload.body, user_id=current_user.id)
    session.add(row)
    session.commit()
    session.refresh(row)
    return row


@url.get("/", response_model=list[PostResponseSchema], status_code=status.HTTP_200_OK)
async def get_all_posts(session=Depends(get_session)):
    statement = select(Post)
    return [row for row in session.execute(statement).scalars().all()]


@url.get("/{id}", response_model=PostResponseSchema, status_code=status.HTTP_200_OK)
async def get_post(id, session=Depends(get_session)):
    try:
        statement = select(Post).filter(Post.id == id)
        return session.execute(statement).scalar_one()
    except exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@url.put("/{id}", response_model=PostResponseSchema, status_code=status.HTTP_200_OK)
async def update_post(id, title: str, body: str, session=Depends(get_session)):
    try:
        statement = select(Post).filter(Post.id == id)
        row = session.execute(statement).scalar_one()
        row.title = title
        row.body = body
        session.commit()
        session.refresh(row)
        return row
    except exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@url.delete("/{id}", response_model=PostResponseSchema, status_code=status.HTTP_200_OK)
async def delete_post(id, session=Depends(get_session)):
    try:
        statement = select(Post).filter(Post.id == id)
        row = session.execute(statement).scalar_one()
        session.delete(row)
        session.commit()
        return row
    except exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
