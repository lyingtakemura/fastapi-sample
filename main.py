import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from jose import JWTError
from pymongo import MongoClient
from sqlalchemy.orm import Session

from authentication import (
    create_access_token,
    create_refresh_token,
    get_hashed_password,
    verify_password,
    verify_refresh_token,
)
from dependencies import get_current_user, get_db, get_mongodb
from models import User as UserModel
from schemas import TokenSchema, UserSchema

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/users", response_model=list[UserSchema])
def get_all_users(
    is_authenticated: get_current_user = Depends(),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return db.query(UserModel).offset(skip).limit(limit).all()


@app.get("/users/{user_id}", response_model=UserSchema)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter_by(id=user_id).first()
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


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


# AUTHENTICATION
@app.post("/signup", response_model=UserSchema)
def signup(payload: UserSchema, db: Session = Depends(get_db)):
    if db.query(UserModel).filter_by(email=payload.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    user = UserModel(
        username=payload.username,
        email=payload.email,
        password=get_hashed_password(payload.password.get_secret_value()),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@app.post("/jwt/login", response_model=TokenSchema)
async def jwt_login(
    response: Response,
    payload: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(UserModel).filter_by(username=payload.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    access_token = create_access_token(user.email)
    refresh_token = create_refresh_token(user.email)

    response.set_cookie("access_token", access_token)
    response.set_cookie("refresh_token", refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@app.post("/jwt/refresh", response_model=TokenSchema)
async def jwt_refresh(payload: TokenSchema):
    try:
        is_verified = verify_refresh_token(payload.refresh_token)
        if is_verified:
            return {
                "access_token": create_access_token(is_verified["sub"]),
                "refresh_token": payload.refresh_token,
            }
    except JWTError as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error))


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
