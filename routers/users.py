from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.schemas.user import UserCreate, ShowUser
from db.database import get_db
from config.hashing import Hasher
from db.models import User

router=APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get()
@router.post(
    "/register",
    tags=['user','staff'],
    response_model=ShowUser
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