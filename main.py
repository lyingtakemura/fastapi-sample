import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"response": "test"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)
