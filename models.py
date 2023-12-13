from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from config.postgres import engine


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    email: str
    password: str = Field(exclude=True)
    is_active: bool = Field(exclude=True, default=True)
    is_admin: bool = Field(exclude=True, default=False)
    posts: List["Post"] = Relationship(back_populates="user")


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="posts")


class Token(SQLModel):
    access_token: str | None = None
    refresh_token: str | None = None
    sub: Optional[str] = Field(None, exclude=True)
    exp: Optional[int] = Field(None, exclude=True)


SQLModel.metadata.create_all(engine)
