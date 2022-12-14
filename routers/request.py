from fastapi import APIRouter, Depends, HTTPException, status
from db.models import Item,User

from sqlalchemy.orm import Session
from db.database import get_db
from config.db_config import setting
from jose import jwt


router = APIRouter()

def get_user_from_token(db, token):
    ##using try block
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
        username = payload.get("sub")
        # data is dictionary,
        # payload.get is a dictionary method to get data.
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to verify"
            )
        user = db.query(User).filter(User.email == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="email is not in our database"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to verify"
        )
    return user

@router.get("/item/{id}", tags=["request"])
def retrieve_item_by_id(id, db: Session = Depends(get_db)):
        #get_db as we need to retrieve id from the database
    item = db.query(Item).filter(Item.id==id).first()
        #filter to filter whatever
        #.first to return first item
    if not item:    ##if item is null
        raise HTTPException(status_code=404, detail=f"Item {id} does not exist")
    return item
