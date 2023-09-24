from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from dependencies import (
    get_current_user,
    get_db,
)
from users.models import User
from posts.schemas import PostSchema

urls = APIRouter(prefix="/posts", tags=["posts"])


@urls.get("/", response_model=list[PostSchema])
def get_posts(db: Session = Depends(get_db)):
    posts = [
        PostSchema(id=1, title="test0", description="desc0", user_id=1),
        PostSchema(id=2, title="test1", description="desc1", user_id=2),
    ]
    return posts
