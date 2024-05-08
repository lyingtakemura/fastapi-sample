from os import environ

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

load_dotenv()

POSTGRES_USER = environ.get("POSTGRES_USER")
POSTGRSE_PASSWORD = environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = environ.get("POSTGRES_HOST")
POSTGRES_DATABASE = environ.get("POSTGRES_DATABASE")
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRSE_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DATABASE}"

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)


def get_session():
    with Session() as session:
        yield session
