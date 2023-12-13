from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from config.auth import is_authenticated
from config.postgres import engine
from models import Post

urls = APIRouter(prefix="", tags=["posts"])


@urls.post("/posts", response_model=Post)
def create_post(data: Post, user: is_authenticated = Depends()):
    with Session(engine) as session:
        post = Post(title=data.title, description=data.description, user_id=user.id)
        session.add(post)
        session.commit()
        session.refresh(post)
        return post


@urls.get("/posts", response_model=list[Post])
def get_all_posts():
    with Session(engine) as session:
        statement = select(Post)
        result = session.exec(statement).all()
        return result
