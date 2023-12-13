import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from urls.posts import urls as POST_ROUTER
from urls.users import urls as USER_ROUTER

app = FastAPI()
app.include_router(POST_ROUTER)
app.include_router(USER_ROUTER)
templates = Jinja2Templates(directory="templates")


@app.get("/template", response_class=HTMLResponse)
def template(request: Request):
    return templates.TemplateResponse("sample.html", {"request": request})


@app.get("/stream", response_class=FileResponse)
def stream():
    return FileResponse("sample.mp4")


@app.get("/redirect", response_class=RedirectResponse)
def redirect():
    return RedirectResponse("/template")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)
