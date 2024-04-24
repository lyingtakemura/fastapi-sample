from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=True,
)
TestSession = sessionmaker(bind=test_engine)


def get_test_session():
    with TestSession() as session:
        yield session
