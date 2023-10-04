from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from dependencies import get_hashed_password
from models import User
from schemas import UserSchema


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def insert_user(self, payload: UserSchema):
        if self.session.query(User).filter_by(email=payload.email).first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="USER_ALREADY_EXIST"
            )

        user = User(
            username=payload.username,
            email=payload.email,
            password=get_hashed_password(payload.password.get_secret_value()),
        )

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def select_users(
        self,
        skip: int = 0,
        limit: int = 100,
    ):
        return self.session.query(User).offset(skip).limit(limit).all()

    def select_user(self, id):
        user = self.session.query(User).filter_by(id=id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="USER_NOT_FOUND"
            )
        return user

    def delete_user(self, id):
        self.session.query(User).filter_by(id=id).delete()
        self.session.commit()
        return status.HTTP_200_OK
