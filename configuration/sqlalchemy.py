from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from configuration.settings import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=False)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    try:
        db = session()
        yield db
    finally:
        db.close()


# from database import engine
# Base.metadata.create_all(engine)
