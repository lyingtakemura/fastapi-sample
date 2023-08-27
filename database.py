from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import settings

engine = create_engine(settings.database_url, echo=True)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def db():
    try:
        db = session()
        yield db
    finally:
        db.close()
