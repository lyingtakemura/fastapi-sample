from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from auth.urls import url as auth_router
from config.database import Base, engine
from posts.urls import url as post_router
from users.urls import url as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(post_router)
app.include_router(auth_router)
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)
