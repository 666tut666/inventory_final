from fastapi import APIRouter, Depends, HTTPException, status
from db.schemas.items import ItemCreate, ShowItem
from db.models import Item,User
from datetime import datetime
from sqlalchemy.orm import Session
from db.database import get_db
from config.db_config import setting


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

@router.post(
    "/item",
    tags=["items"],
    response_model=ShowItem
)
def create_item(
        item: ItemCreate,
        db: Session = Depends(get_db)
):
    creation_date = datetime.now().date()
    #owner_id = 1
    item = Item(
        **item.dict(),
        creation_date=creation_date,
        #owner_id=owner_id
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

