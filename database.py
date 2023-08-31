from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=False)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    try:
        db = session()
        yield db
    finally:
        db.close()
