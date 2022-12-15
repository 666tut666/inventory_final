from fastapi import APIRouter, Depends, HTTPException, status
from db.schemas.items import ItemCreate, ShowItem
from db.models import Item, Admin, User
from datetime import datetime
from sqlalchemy.orm import Session
from db.database import get_db
from config.db_config import setting
from routers.login import oath2_scheme
from typing import List
from fastapi.encoders import jsonable_encoder
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


@router.get("/item/all", tags=["items"], response_model=List[ShowItem])
    #show item matra rakhda error aayo,
    #so, added List
def retrieve_all_items(db: Session=Depends(get_db)):
    items = db.query(Item).all()
    return items


@router.get("/item/{id}", tags=["items"])
def retrieve_item_by_id(id, db: Session = Depends(get_db)):
        #get_db as we need to retrieve id from the database
    item = db.query(Item).filter(Item.id==id).first()
        #filter to filter whatever
        #.first to return first item
    if not item:    ##if item is null
        raise HTTPException(status_code=404, detail=f"Item {id} does not exist")
    return item


#using jsonable encoder
@router.put("/item/update/{id}", tags=["items"])
def update_item_by_id(
        id:int,
        item:ItemCreate,
        db:Session=Depends(get_db),
        token:str=Depends(oath2_scheme)
):
    user = get_user_from_token(db, token)
    existing_item = db.query(Item).filter(Item.id==id)
        #it only returns query
    if not existing_item.first():
            #.first() to fetch details
        return {"Message": f"Item ID {id} has no details "}
    if existing_item.first().owner_id == user.id:
        existing_item.update(jsonable_encoder(item))
        db.commit()
        return {"message": f"details for {id} Successfully Updated"}
    else:
        return {"message": "you aren`t authorized"}


@router.delete("/item/delete/{id}", tags=["items"])
def delete_item_by_id(
        id:int,
        db:Session=Depends(get_db),
        token:str=Depends(oath2_scheme)
):
    user = get_user_from_token(db, token)
    existing_item = db.query(Item).filter(Item.id == id)
        # it only returns query
    if not existing_item.first():
            #.first() to fetch details
        return {"Message": f"Item ID {id} has no details "}
    if existing_item.first().owner_id == user.id:
        existing_item.delete()
        db.commit()
        return {"message": f"Item id: {id} Successfully Deleted"}
    else:
        return {"message": "you aren`t authorized"}
