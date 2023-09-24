from pydantic import BaseModel, EmailStr, Field, SecretStr

from posts.schemas import PostSchema


class UserSchema(BaseModel):
    id: int | None = None
    email: EmailStr
    username: str
    password: SecretStr = Field(exclude=True)
    is_active: bool = Field(exclude=True, default=True)
    posts: list[PostSchema] = Field(default_factory=list)

    class Config:
        from_attribute = True


class TokenSchema(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None
    sub: str | None = Field(None, exclude=True)
    exp: int | None = Field(None, exclude=True)
