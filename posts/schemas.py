from pydantic import BaseModel, Field


class PostSchema(BaseModel):
    title: str
    body: str


class PostInSchema(PostSchema):
    pass


class PostOutSchema(PostSchema):
    id: int
    user_id: int
