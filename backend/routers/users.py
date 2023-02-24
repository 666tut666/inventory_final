from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.schemas.user import UserCreate, ShowUser
from db.database import get_db
from config.hashing import Hasher
from db.models import User
from typing import List

router=APIRouter()

@router.get(
    "/user",
    tags=['user']
)
##tags=["..."] to manage kun tag ma halnae
def get_user():
    return {"message": "hello user"}



@router.post(
    "/user",
    tags=['user'],
    response_model= ShowUser
)
def register(
        user: UserCreate,
        db: Session = Depends(get_db)
):
    user = User(
        email=user.email,
        password=Hasher.get_hash_password(user.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get(
    "/user/all",
    tags=['user'],
    response_model=List[ShowUser]
)
def get_all_users(
        db: Session = Depends(get_db)
):
    users = db.query(User).all()
    return users



@router.get("/user/{id}", tags=["user"])
def retrieve_user_by_id(id, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {id} does not exist")
    return user
