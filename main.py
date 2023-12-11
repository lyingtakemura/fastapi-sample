import uvicorn
from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

from controllers.jwt import urls as JWTRouter
from controllers.posts import urls as PostRouter
from controllers.users import urls as UserRouter
from dependencies import get_hashed_password, get_mongodb
from schemas import UserSchema

app = FastAPI()
app.include_router(UserRouter)
app.include_router(PostRouter)
app.include_router(JWTRouter)
templates = Jinja2Templates(directory="templates")


# # ITEMS
# @app.get("/items", response_model=list[schemas.Item])
# def get_all_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# @app.post("/users/{user_id}/items", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, payload: schemas.Item, db: Session = Depends(get_db)
# ):
#     item = models.Item(
#         title=payload.title, description=payload.description, user_id=user_id
#     )
#     db.add(item)
#     db.commit()
#     db.refresh(item)
#     return item


@app.get("/template", response_class=HTMLResponse)
def template(request: Request):
    return templates.TemplateResponse("sample.html", {"request": request})


@app.get("/stream", response_class=FileResponse)
def stream():
    return FileResponse("sample.mp4")


@app.get("/redirect", response_class=RedirectResponse)
def redirect():
    return RedirectResponse("/template")


@app.post("/mongo")
def mongo_post(payload: UserSchema, mongo: MongoClient = Depends(get_mongodb)):
    users = mongo["users"]
    user = UserSchema(
        username=payload.username,
        email=payload.email,
        password=get_hashed_password(payload.password.get_secret_value()),
    )
    new_user = users.insert_one(user.model_dump())
    created_user = users.find_one({"_id": new_user.inserted_id}, {"_id": False})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@app.get("/mongo")
def mongo_get(mongo: MongoClient = Depends(get_mongodb)):
    result = list(mongo["users"].find({}, {"_id": False}))  # find() returns a cursor
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)
