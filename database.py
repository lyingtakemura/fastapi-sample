from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker


url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="postgres",
    host="localhost",
    database="fastapi-sample",
    port=5432,
)

engine = create_engine(url, echo=True)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def db():
    try:
        db = session()
        yield db
    finally:
        db.close()
