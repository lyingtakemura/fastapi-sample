from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    posts: Mapped[list["Post"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
