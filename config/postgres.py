from sqlmodel import create_engine

from config.settings import postgres_url

engine = create_engine(postgres_url, echo=True)
