from pydantic import BaseModel, Field

from posts.schemas import PostResponseSchema


class UserSchema(BaseModel):
    username: str
    email: str


class UserPayloadSchema(UserSchema):
    password: str


class UserResponseSchema(UserSchema):
    id: int
    posts: list["PostResponseSchema"] | None = None
