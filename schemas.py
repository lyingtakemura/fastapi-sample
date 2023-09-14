from pydantic import BaseModel, EmailStr, Field, SecretStr


class Item(BaseModel):
    id: int
    title: str
    description: str | None = None
    user_id: int

    class Config:
        from_attribute = True


class User(BaseModel):
    id: int | None = None
    email: EmailStr
    username: str
    password: SecretStr = Field(exclude=True)
    is_active: bool = Field(exclude=True, default=True)
    items: list[Item] = Field(default_factory=list)

    class Config:
        from_attribute = True


class Token(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None
    sub: str | None = Field(None, exclude=True)
    exp: int | None = Field(None, exclude=True)
