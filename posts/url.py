from fastapi import APIRouter, status

from posts.schema import PostInSchema, PostOutSchema

url = APIRouter(prefix="/posts", tags=["posts"])


@url.get("/", response_model=list[PostOutSchema], status_code=status.HTTP_200_OK)
async def select_all():
    return [{"id": 0, "title": "title", "body": "body", "user_id": 0}]


@url.post("/", response_model=PostOutSchema, status_code=status.HTTP_201_CREATED)
async def insert(post: PostInSchema):
    return {"id": 0, "title": post.title, "body": post.body, "user_id": 0}
