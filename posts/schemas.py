from pydantic import BaseModel, Field


class PostSchema(BaseModel):
    title: str
    body: str


class PostPayloadSchema(PostSchema):
    pass


class PostResponseSchema(PostSchema):
    id: int
    user_id: int 
