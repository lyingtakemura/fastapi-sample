### ALEMBIC
```
set sqlalchemy.url in alembic.ini
set base.metadata in env.py

alembic init migrations
alembic revision --autogenerate -m '_'
alembic upgrade head
```

### PYTEST
```
pytest --verbose
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