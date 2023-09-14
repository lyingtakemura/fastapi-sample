### ALEMBIC
```
set sqlalchemy.url in alembic.ini
set base.metadata in env.py

alembic init migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

pydantic model from orm: PYDANTIC_MODEL.from_orm(ORM_MODEL)
orm model from pydantic: ORM_MODEL(**PYDANTIC_MODEL.dict())
```

### SQLALCHEMY
```
- engine.execute:
raw sql
- connection.exectute:
raw sql with greater control over attributes of the connection, when it gets closed, etc
- session.execute:
Used for the ORM aspect of SQLAlchemy. They use connections and transactions under the hood
to run their automatically-generated SQL statements. execute() is a convenience function that
passes through to whatever the session is bound to (usually an engine, but can be a connection)
```

### PYTEST
```
pytest --verbose
change traceback mode: --tb=no // --tb=short
run specific test: pytest ./tests/test_main.py::TestSample::test_type_error
tests matching a name pattern: pytest -k '_' // '_ and not (_ or _)'
test structure: Arrange-Act-Assert
show order of tests and fixtures: pytest --setup-show test_count.py
@pytest.fixture(scope="function(default)|class|module|package|session")
list available fixtures: pytest --fixtures -v // --fixtures-per-test
always run fixture: @pytest.fixture(autouse=True)
allow print: -s // --capture=no
rename fixture: @pytest.fixture(name="_")
before yield - setup code, after yield - teardown code
```

### META
```
models.py - sqlalchemy
schemas.py - pydantic

Without orm_mode, if you returned a SQLAlchemy model from your path operation, it wouldn't include the relationship data.
Even if you declared those relationships in your Pydantic models.

But with ORM mode, as Pydantic itself will try to access the data it needs from attributes (instead of assuming a dict), you can declare the specific data you want to return and it will be able to go and get it, even from ORMs.

Also notice that there are response_models that have standard Python types like List[schemas.Item].
But as the content/parameter of that List is a Pydantic model with orm_mode, the data will be retrieved and returned to the client as normally, without problems.

openssl rand -hex 32
```