from fastapi import APIRouter, Depends
from schemas.items import ItemCreate, ShowItem
from db.models import Item
from datetime import datetime
from sqlalchemy.orm import Session
from db.database import get_db

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
