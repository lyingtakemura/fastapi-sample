from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from config.database import Base, engine
from posts.urls import url as post_urls


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(post_urls)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)
