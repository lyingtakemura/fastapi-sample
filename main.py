import uvicorn
from fastapi import FastAPI

from posts.url import url as post_url

app = FastAPI()
app.include_router(post_url)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)
