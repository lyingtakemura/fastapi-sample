from typing import List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base


class Post(Base):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str]
    # user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    # user: Mapped["User"] = relationship(back_populates="addresses")
