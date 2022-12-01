from fastapi import APIRouter, Depends
from schemas import ItemCreate, ShowItem
from models import Items
from datetime import datetime
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()


@router.post(
    "/item",
    tags=["items"],
    response_model=ShowItem
)
def create_item(
        item: ItemCreate,
        db: Session = Depends(get_db)
):
    date_posted = datetime.now().date()
    #owner_id = 1
    item = Items(
        **item.dict(),
        date_posted=date_posted,
        #owner_id=owner_id
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
