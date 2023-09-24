from pydantic import BaseModel


class PostSchema(BaseModel):
    id: int
    title: str
    description: str | None = None
    user_id: int

    class Config:
        from_attribute = True
